# TEST893 BODY-SHA256 cd91c021f1830b58e6d882ce554629600b9b0fb316796b1ffb2c2d2c356019fc
# AKBASCORE SILICON HIPPOCAMPUS - TEST893 (redefined) - PRE-POST-DELTA appraisal-transition cartridge on TEST892 (one Colab cell, one Run)
# Contract: K3.1 "TEST893 Bagimsiz Mekanizma Denetimi ve Karar Raporu" (17 Nov 2026, decision DENEYI YENIDEN TANIMLA) + "CLAUDE ICIN
# TEST893 YENIDEN TANIMLAMA VE ASGARI KOD GOREVI" (17 Nov 2026). Frozen Qwen2.5-72B-Instruct NF4 / BF16, one A100-SXM4-80GB.
# What changed against the first TEST893 draft (blob fde22235): (1) no pre-action "forecast": a pre-action successor forecast with
# the same observables is not constructible here (the successor hop, evidence and mount result are environment outputs of
# execute866), so the F component is withdrawn and nothing is called a forecast; (2) no cross-world donor: every cartridge is made
# from the episode's OWN exact transition; (3) world 10 FORK, where all TEST892 arms ended Y = 0 (headroom), not 09 FORK (Y = 1
# ceiling); (4) the attribution control is an equal-geometry PLACEBO cartridge (same tokens, slots, positions, O rows, label and
# row count; delta rows = 0), so NEW - PLACEBO isolates the delta content and PLACEBO - OLD the added geometry.
# Unit: the step-2 transition E2 = [X2_2][A_2][EVALUATION + O = V_3 (+ DELTA label + delta rows)], written at t3, read once at t4
# (FULL executed), t1-t3 and t >= 5 native. delta_w = p_post_w - p_pre_w: p_pre = the native CAR reading at t2 (the reading that
# chose A_2), p_post = the native CAR reading at t3; both are locked control_step867 readings with the same slot contract
# (checked). delta is an observed appraisal transition, not a prediction error, not a reward, not an action gate.
# Run: NONE_10_FORK (native reference), OLD_10_FORK (O only), NEW_10_FORK (O + delta, executes NEW), PLACEBO_10_FORK (O + zero
# delta, executes PLACEBO). The model alone decides: the executed action is reading['action'] of the arm's FULL CAR reading,
# literally through execute866. No training, LoRA, backward, RAG, text replay, hooks, router, oracle, answer fixing, override.
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
NEW893 = ('fo_inputs893', 'fo_checks893', 'fo_record893', 'fo_point893', 'expected893', 'hex64_893', 'seal_ok893')
PATCHES893 = (                                                                  # (label, old, new, count) on the renamed TEST892 text
    ('prereg', 'PREREG889.update(PREREG892)\n', 'PREREG889.update(PREREG892)\nPREREG889.update(PREREG893)\n', 1),
    ('runtime_scan', "'point_view892', 'v_only_final892')", "'point_view892', 'v_only_final892',\n                  %s)" %
     ', '.join(repr(n) for n in NEW893), 1),
    ('ledger_reading', "'episode_id': ep_id, 'step': t}",
     "'episode_id': ep_id, 'step': t, 'p': {w_: float(record['reading']['normalized'][w_]) for w_ in ACTIONS_M867},\n"
     "                          'slots': [[int(x_) for x_ in s_[0]] for s_ in state['segments']]}   # TEST893: p and the slot contract", 1),
    ('single_write', "                if arm != 'NONE' and not terminal:\n",
     "                if arm != 'NONE' and not terminal and t == WRITE_STEP893:     # TEST893: only E2 is written (the single read point)\n", 1),
    ('effect_seq', "if pend is not None: pend['effect_action'] = eff.get('action')",
     "if pend is not None: pend['effect_action'] = eff.get('action'); STATE889['seq'] += 1; pend['effect_seq'] = STATE889['seq']", 1),
    ('own_transition', 'donor = donor_v889(donor_ledger, t, ep_id)',
     'donor = led[t]                                             # TEST893: no cross-world donor; the own exact post-step O', 1),
    ('fo_inputs', 'w = write_pair889(env, pend, led[t], donor, t, cdir, key)',
     'vt_, dn_ = fo_inputs893(env, led[t], led[s_], ep_id)              # TEST893: TRUE = OLD or NEW payload, WRONG = OLD or PLACEBO\n'
     '                        w = write_pair889(env, pend, vt_, dn_, t, cdir, key)', 1),
    ('closure_v_after', "'checks': {'v_after_is_post_step_ledger': w['true'][0]['provenance']['V_rows_sha256'] == led[t]['sha'],",
     "'checks': {'v_after_is_post_step_ledger': w['true'][0]['provenance']['V_rows_sha256'] == vt_['payload_sha'] and vt_['O_sha'] == led[t]['sha'],\n"
     "                                         'fo893_pre_execute_post_commit_order': fo_checks893(pend, led[s_], led[t], STATE889['seq'], vt_, dn_, w),", 1),
    ('fo_record', 'written[s_] = w; pend = None', "w['fo893'] = fo_record893(w, vt_, dn_, ep_id); written[s_] = w; pend = None", 1),
    ('single_read', 'ev = eligible889(t)', 'ev = eligible889(t) if t == WRITE_STEP893 + LAG889 else None       # TEST893: the single read of E2 at t4', 1),
    ('point_fields', 'pt.update(v_only_fields892(rT, rW, cT, cW))', 'pt.update(v_only_fields892(rT, rW, cT, cW)); pt.update(fo_point893(d, B, ctx))', 1),
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
     "    plan889 = list(PLAN893)                                         # TEST893: NONE + OLD / NEW / PLACEBO on 10_FORK\n"
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
     "        STATE889['t893'] = {'VERDICT': 'TECHNICAL_BLOCK', 'PHYSICAL_VALIDITY': 'TECHNICAL_BLOCK', 'error': 'VERDICT893_ERROR %s: %s' % (type(exc).__name__, exc)}\n"
     "    U_ = unique_safe891(pts_)\n", 1),
    ('report893', "'test': 'TEST893', 'verdict': STATE889['verdict'],",
     "'test': 'TEST893', 't893': STATE889.get('t893'), 'base892': B892_INFO893,\n"
     "        'executed_892_gpu_cell': EXEC892_GPU893, 'legacy_889_892_note': 'verdict / payload / component / v_only fields are the inherited '\n"
     "        'TEST889-892 diagnostics on this smaller run; they are not the TEST893 verdict', 'verdict': STATE889['verdict'],", 1),
    ('console_legacy', "print('TEST893 | %s'", "print_t893(STATE889.get('t893')); print('LEGACY_889_892_DIAGNOSTICS (not the TEST893 verdict) | %s'", 1),
    ('receipt893', "    _rc['v_only_final'] = v_only_final892(STATE889.get('v_only_audit'), artifact_gates892(CC_ZIP, _zip_ok, _rc['drive_zip_sha256_equal'], CC_DRIVE_DIR, STATE889))\n",
     "    _g893 = artifact_gates892(CC_ZIP, _zip_ok, _rc['drive_zip_sha256_equal'], CC_DRIVE_DIR, STATE889)\n"
     "    _rc['v_only_final'] = v_only_final892(STATE889.get('v_only_audit'), _g893)\n"
     "    _rc['test893_final'] = final893(STATE889.get('t893'), _g893)\n"
     "    print('TEST893_FINAL VERDICT=%s | PHYSICAL_VALIDITY=%s | SCIENTIFIC_VALIDITY=%s | OUTCOME=%s | ARTIFACT_STATUS=%s | failed_gates=%s' % tuple(\n"
     "        _rc['test893_final'].get(k_) for k_ in ('VERDICT', 'PHYSICAL_VALIDITY', 'SCIENTIFIC_VALIDITY', 'OUTCOME', 'ARTIFACT_STATUS', 'failed_gates')))\n", 1),
    ('receipt893_fail', "        _rcx['receipt_error'] = '%s: %s' % (type(_exc).__name__, _exc)\n",
     "        _rcx['receipt_error'] = '%s: %s' % (type(_exc).__name__, _exc)\n"
     "        _rcx['test893_final'] = dict(_rcx.get('test893_final') or {}, VERDICT='TECHNICAL_BLOCK', ARTIFACT_STATUS='TECHNICAL_BLOCK',\n"
     "                                     preliminary=(STATE889.get('t893') or {}).get('VERDICT'))\n", 1),
    ('console893_fail', "    _rpx = str(CC_ZIP).replace('.zip', '_RECEIPT.json')",
     "    print('TEST893_FINAL VERDICT=TECHNICAL_BLOCK | ARTIFACT_STATUS=TECHNICAL_BLOCK (receipt failed) | preliminary=%s' % ((STATE889.get('t893') or {}).get('VERDICT'),))\n"
     "    _rpx = str(CC_ZIP).replace('.zip', '_RECEIPT.json')", 1))
CHANGED_FUNCS893 = ('capture889', 'episode889')                    # against the renamed TEST892 text; every other function AST-identical
LOCKED893 = ('execute866', 'control_step867', 'donor_v889', 'verdict889', 'read889', 'read_contract889', 'write_appraisal889', 'full_seal881',
             'write_pair889', 'write_exp878', 'load_exp878', 'append_exp878', 'xappend878', 'xcar878', 'xspan878', 'same_reading881',
             'budget849', 'comp_masks891', 'calls_gate891', 'v_only_fields892', 'v_only_mask892', 'record_problems892')
OWN_FUNCS893 = ('canon893', 'base892_893', 'lockdiag893', 'ep_id893', 'verdict893', 'final893', 'print_t893', 'source893', 'st893') + NEW893
# LINEDIG893: sha256[:4] of every canonical body line except its own data lines (paste diagnostics only, not a lock)
LINEDIG893 = (
    '012800a4e6052bf1a73ed76347b770bbfd519f6e8ac419c411210bf6e6c549c47e0934325c10871661fe4488f63c12fb'  #LD890
    '1d3b3689a2554a6652c9b294d426a565c9d6de59ea04c82d0ec6132befbcef4db99c463b7261377f3fa6efebd0bfac8e'  #LD890
    '95e4b9f41aada74321581785dbbd91dd20a6de5d8b8c93d9077f214f36d1aad28848930027c94296dea1533367dd4751'  #LD890
    'de107abf8cb814eb4d23a974dcc4d9ecacb7a1c70480e2283552a9003f809eb6f771e228ef677e8448073f80a33ebcc9'  #LD890
    '4ab64341014cfb6676b21fe5db64e21fbd51ed343efd3bcd19b59091ba0e44ec3add05a08100682cd16add0822e44767'  #LD890
    '566d1f84252764569ed754b1c47e133291e6c50d99636f7832b2515154079d3fc76cb0891bde9fb95d6af3a26ff5d7ef'  #LD890
    '9b30e896cfb1dfa76fc3521ff1998761e185d417389ef06fc0d4cf2ac94f675404dc2140f33034e77a4fd5e91f7b3e6a'  #LD890
    'bf8c18c8e9f5f36f851f1f7128ed429b05576ed386ef51b4815d11dec3fb5449382e839e9061cf88633f37481154f1e7'  #LD890
    'b9051efa0793015ff6cc1a78aef373dc26dc0325c375d91e6499b0f08d40d50c4ad64a7430f7660996201970e4d471c5'  #LD890
    '0376bc29d54b925b709cae2b1a2b24b55227c852c8ac9880e2245488c92a44c38055b4dd29aed21b94d29757bff4f88b'  #LD890
    '12ecff46bc78188855b9ffee3fe08b84a49c58e4d5e4c51d63d463bbba9162181435ad48f1d9eb2ac51c9099b9353c11'  #LD890
    'a46b902dc68bb5d89282221423a58fc2b1e390cb268aa926a5909937becf17d35648e1b4c8b04b5580bcca79b8ca4248'  #LD890
    'b7a2b3f8ce2513bab5bf84dc04cb30d9284f3c1ca74bee7297a033d189d908b4606c1c6b533b1307995c9b0ee0478060'  #LD890
    'ae446cf574dbf8a3c16b79590c333b2fa5776a3b3c3bc80a1b194bad4e54c5a41ca5743e1029f969d92d68470535ff84'  #LD890
    '82d2965fd08af6f1d36cfdfd8c943afff4d3d3d3dabd6dbca453886b3a258d1b65c3f6515b7bb8cd10883650e64f6d58'  #LD890
    '8faa968aad13e17620e136219230cb52835b0545f31333b8a66b1d94386b9e59da1e40b9d21615995eb5e781102c1d94'  #LD890
    '7f89c94f2f372dac2ac62a3acca48d2944528bf87e5da50d7fbe10ec9ca01e8946e08ecd9b0370486d0b567f809c3334'  #LD890
    'b5431b4b830ba68310223d32a2daf98449e6717150a8fcfa0b7bc321da05ec31734aca1aaa8b09c32925a179ea2ed276'  #LD890
    '6ccac4b552df1cbba3de0abacb00b6ca794dac40db0bd4065a794a801cb648220b71980254869ca7677e73ee191414f0'  #LD890
    'b0740b9d5857da9ecfcddf4e2cb559a59ed1c5716da311870e6407d5b231815c46fefb457fd6254926be65923468a649'  #LD890
    '2d4d5adfedbec45270ddb0b53be618e6cfdb4ebc371c0052252e3f71e37d013688e243757a31d5ebaad128bcd3abcc3e'  #LD890
    '7598f4c44aab'  #LD890
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
PLAN893 = (('NONE', 'NONE', '10', 'FORK'), ('OLD', 'D_TRUE', '10', 'FORK'), ('NEW', 'D_TRUE', '10', 'FORK'), ('NEW', 'D_WRONG', '10', 'FORK'))
EP893 = ('NONE_10_FORK', 'OLD_10_FORK', 'NEW_10_FORK', 'PLACEBO_10_FORK')
ARM_ID893 = {('NONE', 'NONE'): 'NONE', ('OLD', 'D_TRUE'): 'OLD', ('NEW', 'D_TRUE'): 'NEW', ('NEW', 'D_WRONG'): 'PLACEBO'}
EXEC_ROLE893 = {'OLD_10_FORK': 'a_true', 'NEW_10_FORK': 'a_true', 'PLACEBO_10_FORK': 'a_wrong'}   # which FULL reading the arm executes
WRITE_STEP893 = 2                 # E2 = the step-2 transition; closed at t3, read once at t4 (= WRITE_STEP893 + LAG889)
SLOT_TEXT893 = {'DELTA': 'Appraisal change numerical state:'}
SLOTS893 = {}                     # token ids, filled at G1 with the model tokenizer (as SLOTS867['PREV_EVALUATION'])
FORMAT893 = None                  # set by the plan loop before each episode: 'NONE', 'OLD' or 'NEW'
VERDICTS893 = ('TECHNICAL_BLOCK', 'INCONCLUSIVE', 'FAIL', 'PASS')
PREREG893 = {
    'test893': 'TEST893 (redefined): PRE-POST-DELTA appraisal-transition cartridge, world 10 FORK, OLD / NEW / PLACEBO + NONE reference',
    'contract893': 'K3.1 TEST893 Bagimsiz Mekanizma Denetimi (17 Nov 2026, DENEYI YENIDEN TANIMLA) + CLAUDE ICIN TEST893 YENIDEN TANIMLAMA '
                   've ASGARI KOD GOREVI (17 Nov 2026)',
    'withdrawn893': 'no pre-action successor forecast is claimed: the successor hop, evidence and mount result are outputs of '
                    'execute866 and cannot be produced natively before it with the same observables; no cross-world donor; no 09_FORK',
    'selection893': 'world 10 FORK and the E2 / t4 read point were fixed from the TEST892 GPU log before this run: every TEST892 10_FORK '
                    'arm (NONE, D_TRUE, D_WRONG) ended Y = 0 (headroom), and steps 2 and 3 carry the same control slot set (C, E, R, '
                    'pointer, PREV_EVALUATION, K, EVALUATION), so the pre and post readings share one slot contract. No other world, '
                    'read point, threshold or arm is chosen after the run',
    'episodes893': list(EP893),
    'unit893': 'E2 = [X2_2][A_2][EVALUATION slot + O = V_3 (+ DELTA label + delta rows)], closed at t3 from the own episode ledger, '
               'read once at t4 (FULL executed); t1-t3 and t >= 5 native (the NONE reading, bitwise = control_step867)',
    'delta893': 'delta_w = p_post_w - p_pre_w over the six CAR words; p_pre = normalized native CAR reading at t2 (the reading that chose '
                'A_2), p_post = the same at t3; an observed appraisal transition, not a prediction error, not a reward, not a gate; '
                'delta rows = delta_w x embed(first native id of word w) in the fixed action order: a representation hypothesis (the '
                'model is not shown to decode it)',
    'arms893': {'OLD': 'O only (the TEST892 body)', 'NEW': 'O + DELTA label + delta rows (executes NEW)',
                'PLACEBO': 'O + DELTA label + zero rows: same tokens, slots, positions, O rows and row count as NEW (executes PLACEBO)',
                'NONE': 'native reference, no cartridge'},
    'identification893': 'NEW and PLACEBO differ only in the six delta row values (gated: same spans, body tokens, O rows, X2 / A '
                         'rows), so Y_NEW - Y_PLACEBO is attributed to the delta content; PLACEBO - OLD is the added geometry / label; '
                         'all arms share the same world, initial snapshot and own transition (gated: X sha, B tokens, full B KV seal, '
                         'mounted set, path, NONE action and actions t1-t3)',
    'PHYSICAL_VALIDITY': 'PASS only if: run COMPLETE, no physical failure, post-run integrity, clean cleanup, negatives refused; the four '
                         'episodes present with natural ends; each D episode exactly one closure (ok, pre reading seq < execute seq < '
                         'post reading seq < commit seq) and one t4 point (E2); exact O geometry (no padding); explicit == native append, '
                         'B seal unchanged for TRUE and WRONG, repeat reload bitwise; file SHA-256 64-hex and tensor seal schema per '
                         'cartridge; same full start state; executed t4 action == the arm FULL reading action; Y binary; else TECHNICAL_BLOCK',
    'SCIENTIFIC_VALIDITY': 'PASS only if: pre / post slot contract equal; NEW delta not all zero and equal in both NEW-format episodes; '
                           'headroom Y(OLD) = 0; cross-episode determinism (the PLACEBO reading inside NEW_10_FORK equals the action '
                           'executed in PLACEBO_10_FORK and vice versa); else INCONCLUSIVE',
    'OUTCOME': 'PASS_DELTA_SPECIFIC_GAIN if Y(NEW) = 1, Y(PLACEBO) = 0, Y(OLD) = 0 and the executed t4 actions of NEW and PLACEBO differ; '
               'FAIL_NO_GAIN if Y(NEW) = 0; FAIL_NOT_DELTA_SPECIFIC if Y(NEW) = Y(PLACEBO) = 1; INCONCLUSIVE_SAME_DECISION if Y(NEW) = 1, '
               'Y(PLACEBO) = 0 but the t4 actions are equal (no decision path). Action separation alone is never PASS',
    'VERDICT': 'TECHNICAL_BLOCK > INCONCLUSIVE > FAIL / PASS as above; PRELIMINARY in the report; FINAL (receipt test893_final, console '
               'TEST893_FINAL) is TECHNICAL_BLOCK unless every artifact gate is True (report read-back, ZIP testzip, SHA256SUMS, report in '
               'ZIP, Drive copy SHA; Drive not attempted = NOT_RUN = not True)',
    'not_claimed893': 'one pair at one read point is local causal evidence only: not general recursive learning, not semantic decoding of '
                      'delta, not a forecast, not a reliability or correctness probability; a negative result falsifies only this setup'}


def lockdiag893(src):
    # the TEST890 line diagnostics with the TEST893 line table (same '#LD890' data-line marker)
    keep = LINEDIG890; globals()['LINEDIG890'] = LINEDIG893
    try: return lockdiag890(src)
    finally: globals()['LINEDIG890'] = keep


def ep_id893(f, a, w, c):
    return '%s_%s_%s' % (ARM_ID893[(f, a)], w, c)


def expected893(n_steps):
    # TEST893 schedule: E2 closed at t3 (step 2 nonterminal and a step 3 exists), read once at t4
    n = int(n_steps)
    return (1 if n >= WRITE_STEP893 + 1 else 0), (1 if n >= WRITE_STEP893 + LAG889 else 0)


def hex64_893(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def seal_ok893(s):
    # the structured tensor seal of tsha878: {'h': sha256 hex, 'lower': CUT + 1 pairs of sha256 hex}; never a file hash
    return isinstance(s, dict) and set(s) == {'h', 'lower'} and hex64_893(s['h']) and isinstance(s['lower'], (list, tuple)) and \
        len(s['lower']) == APPEND873.get('CUT', 3) + 1 and all(isinstance(x, (list, tuple)) and len(x) == 2 and all(hex64_893(y) for y in x)
                                                                for x in s['lower'])


def fo_inputs893(env, post, pre, ep_id):
    # the after-action payload rows of the pair; O = the own exact post-step rows (never a donor, never padded / cropped).
    # OLD: TRUE = WRONG = O. NEW: TRUE = [O][DELTA label][delta rows] (NEW), WRONG = [O][DELTA label][zero rows] (PLACEBO).
    sha = lambda r: env['stats849'](r)['sha256']
    if sha(post['rows']) != post['sha'] or sha(pre['rows']) != pre['sha']: raise Gate883('PHYSICAL_APPRAISAL_LEDGER_SHA %s' % ep_id)
    base = dict(post, O_sha=post['sha'])
    if FORMAT893 != 'NEW': return dict(base, payload_sha=post['sha']), dict(base, payload_sha=post['sha'])
    d = {w: float(post['p'][w]) - float(pre['p'][w]) for w in ACTIONS_M867}
    lab = env['embed841'](list(SLOTS893['DELTA'])).detach().float().cpu().contiguous()
    first = {w: env['embed841'](list(dict(ACTION_IDS867)[w])[:1]).detach().float().cpu().reshape(-1) for w in ACTIONS_M867}
    o = post['rows'].detach().float().cpu().contiguous(); nE = len(SLOTS866['EVALUATION'])
    def one(role):
        drows = torch.stack([d[w] * first[w] for w in ACTIONS_M867]).float().contiguous()
        if role == 'PLACEBO': drows = torch.zeros(tuple(drows.shape), dtype=torch.float32)
        rows = torch.cat([o, lab, drows], dim=0).contiguous()
        a = nE + int(o.shape[0]); c = a + int(lab.shape[0]) + int(drows.shape[0])
        fo = {'role': role, 'p_pre': {w: float(pre['p'][w]) for w in ACTIONS_M867}, 'p_post': {w: float(post['p'][w]) for w in ACTIONS_M867},
              'delta': dict(d) if role == 'NEW' else {w: 0.0 for w in ACTIONS_M867}, 'delta_l1': sum(abs(x) for x in d.values()) if role == 'NEW' else 0.0,
              'pre_sha': pre['sha'], 'pre_seq': pre['seq'], 'pre_step': pre['step'], 'post_sha': post['sha'], 'post_seq': post['seq'],
              'post_step': post['step'], 'delta_rows_sha256': sha(drows), 'delta_rows_abs_sum': float(drows.abs().sum()), 'payload_rows': int(rows.shape[0]),
              'slot_contract_equal': pre['slots'] == post['slots'], 'slots_pre': pre['slots'], 'slots_post': post['slots'],
              'spans_in_V_AFTER': {'EVALUATION_LABEL': [0, nE], 'O_OBSERVED': [nE, a], 'DELTA': [a, c]}}
        return dict(base, rows=rows, payload_sha=sha(rows), fo=fo)
    return one('NEW'), one('PLACEBO')


def fo_checks893(pend, pre, post, commit_seq, vt, dn, w):
    # closure check: pre reading -> execute866 -> post reading -> commit, the own exact transition, the pair bound to its payload rows
    pv, wv = w['true'][0]['provenance'], w['wrong'][0]['provenance']
    order = pre['seq'] < pend.get('effect_seq', -1) < post['seq'] < commit_seq and pre['sha'] == pend['v_before_sha'] and \
        pv['V_rows_sha256'] == vt['payload_sha'] and wv['V_rows_sha256'] == dn['payload_sha'] and vt['O_sha'] == dn['O_sha'] == post['sha']
    if FORMAT893 != 'NEW': return order and 'fo' not in vt and 'fo' not in dn and vt['payload_sha'] == dn['payload_sha']
    ft, fw = vt.get('fo'), dn.get('fo')
    if not (isinstance(ft, dict) and isinstance(fw, dict)): return False
    sv = pv['spans_body']['V_AFTER']
    return order and ft['role'] == 'NEW' and fw['role'] == 'PLACEBO' and ft['spans_in_V_AFTER'] == fw['spans_in_V_AFTER'] and \
        ft['spans_in_V_AFTER']['DELTA'][1] == sv[1] - sv[0] and pv['spans_body'] == wv['spans_body'] and \
        ft['p_pre'] == fw['p_pre'] and ft['p_post'] == fw['p_post'] and ft['payload_rows'] == fw['payload_rows']   # delta values: scientific


def fo_record893(w, vt, dn, ep_id):
    # LINKS: the append-only manifest row binding each cartridge (id, file SHA, tensor seal, payload rows SHA) to its pre / post / delta
    rows = []
    for role, (entry, rec), src in (('TRUE', w['true'], vt), ('WRONG', w['wrong'], dn)):
        rows.append({'episode_id': ep_id, 'format': FORMAT893, 'cartridge_role': role,
                     'content': 'OLD' if FORMAT893 != 'NEW' else ('NEW' if role == 'TRUE' else 'PLACEBO'),
                     'cartridge_id': entry['id'], 'file_sha256': rec['sha256'], 'tensor_seal': rec.get('tensor_sha'),
                     'V_rows_sha256': entry['provenance']['V_rows_sha256'], 'payload_sha': src['payload_sha'], 'O_sha': src['O_sha'],
                     'O_source': {'episode_id': src['episode_id'], 'step': src['step']}, 'body_tokens': rec['body_tokens'],
                     'spans_body': entry['provenance']['spans_body'], 'fo': src.get('fo')})
    with open(ROOT864 / 'TEST893_fo_manifest.jsonl', 'a', encoding='utf-8') as f:
        for r in rows: f.write(_j889.dumps(jsafe878(r), sort_keys=True) + '\n')
    return {'format': FORMAT893, 'true': rows[0], 'wrong': rows[1]}


def fo_point893(d, B, ctx):
    # TEST893 point fields: the full start state at the read (B KV seal, mounted set, path) and the two separate hash schemas
    t, w = d['true'][1], d['wrong'][1]
    pt_, pw_ = d['true'][0]['provenance'], d['wrong'][0]['provenance']; fo_ = d.get('fo893') or {}
    e2 = {r: {'X_sha256': pv['X_sha256'], 'action_token_ids': [int(x) for x in pv['action_token_ids']], 'pre_C_seal': rc['pre_C_seal'],
              'O_sha': (fo_.get(rl) or {}).get('O_sha'), 'step_written': pv['step_written'], 'spans_body': pv['spans_body'],
              'body_tokens': rc['body_tokens'], 'payload_rows': ((fo_.get(rl) or {}).get('fo') or {}).get('payload_rows')}
          for r, rl, pv, rc in (('true', 'true', pt_, t), ('wrong', 'wrong', pw_, w))}
    return {'format893': FORMAT893, 'fo893': d.get('fo893'), 'e2_identity893': e2, 'B_seal893': full_seal881(B)['all'], 'mounted893': list(ctx['M']),
            'path893': [p['text'] for p in ctx['path']], 'cartridge_sha_true': t['sha256'], 'cartridge_sha_wrong': w['sha256'],
            'cartridge_tensor_seal_true': t.get('tensor_sha'), 'cartridge_tensor_seal_wrong': w.get('tensor_sha'),
            'cartridge_schema893': {'file_sha_true': hex64_893(t['sha256']), 'file_sha_wrong': hex64_893(w['sha256']),
                                    'tensor_seal_true': seal_ok893(t.get('tensor_sha')), 'tensor_seal_wrong': seal_ok893(w.get('tensor_sha'))}}


def verdict893(state, phys):
    # post-run only; physical validity -> scientific validity -> outcome; never feeds back into any decision
    E = {e['episode_id']: e for e in state.get('episodes') or []}
    Y = {k: ((state.get('scores') or {}).get(k) or {}).get('Y') for k in EP893}
    D = EP893[1:]
    pts, cls = {}, {}
    for p in state.get('points') or []: pts.setdefault(p['episode_id'], []).append(p)
    for c in state.get('closures') or []: cls.setdefault(c['episode_id'], []).append(c)
    P1 = {k: (pts.get(k) or [None])[0] for k in D}
    ex = lambda k: (E.get(k) or {}).get('actions') or []
    t4 = {k: (ex(k)[3] if len(ex(k)) > 3 else None) for k in D}
    out = {'Y': Y, 'actions': {k: ex(k) for k in EP893}, 'ends': {k: (E.get(k) or {}).get('end') for k in EP893}, 'executed_t4': t4}
    ck = {'run_complete': state.get('technical_status') == 'COMPLETE' and not state.get('blocked_episodes') and state.get('error') is None,
          'physical_facts': all((phys or {}).get(k) is True for k in ('no_physical_failure', 'post_run_integrity', 'cleanup_clean', 'negatives_refused')),
          'four_episodes': sorted(E) == sorted(EP893), 'natural_ends': all((E.get(k) or {}).get('end') in NATURAL_ENDS883 for k in EP893)}
    ck['one_closure_one_read'] = all(len(cls.get(k) or []) == 1 and cls[k][0].get('ok') is True and cls[k][0]['post_appraisal_step'] == WRITE_STEP893 + 1
                                     and len(pts.get(k) or []) == 1 and P1[k]['step'] == WRITE_STEP893 + LAG889 and P1[k]['step_written'] == WRITE_STEP893
                                     for k in D)
    okp = ck['one_closure_one_read']
    ck['exact_geometry'] = okp and all(P1[k]['donor_fit']['donor_rows'] == P1[k]['donor_fit']['true_rows'] and P1[k]['donor_fit']['padded_mue'] == 0 for k in D)
    ck['reload_parity_true_and_wrong'] = okp and all(P1[k].get('repeat_reload_bitwise') is True and all(
        P1[k][r].get('explicit_equals_native_append_bitwise') is True and P1[k][r].get('B_full_seal_unchanged') is True for r in ('read_true', 'read_wrong'))
        for k in D)
    ck['cartridge_schemas'] = okp and all(all(v is True for v in (P1[k].get('cartridge_schema893') or {'x': False}).values()) for k in D)
    ck['format_recorded'] = okp and [P1[k].get('format893') for k in D] == ['OLD', 'NEW', 'NEW']
    ck['same_full_start_state'] = okp and len({_j893.dumps([P1[k]['X_sha256'], P1[k]['B_tokens'], P1[k].get('B_seal893'), P1[k].get('mounted893'),
                                                            P1[k].get('path893'), P1[k]['a_none'], ex(k)[:3]], sort_keys=True) for k in D}) == 1
    ck['executed_equals_full_reading'] = okp and all(t4[k] is not None and t4[k] == P1[k][EXEC_ROLE893[k]] for k in D)
    ck['Y_binary'] = all(Y[k] in (0, 1) for k in EP893)
    out['physical_checks'] = ck
    out['PHYSICAL_VALIDITY'] = 'PASS' if all(v is True for v in ck.values()) else 'TECHNICAL_BLOCK'
    out['SCIENTIFIC_VALIDITY'] = out['OUTCOME'] = 'NOT_MEASURED'
    if out['PHYSICAL_VALIDITY'] != 'PASS':
        out['VERDICT'] = 'TECHNICAL_BLOCK'; out['why'] = sorted(k for k, v in ck.items() if v is not True); return out
    fo = lambda k, r: (((P1[k].get('fo893') or {}).get(r) or {}).get('fo') or {})
    fn, fp = fo('NEW_10_FORK', 'true'), fo('PLACEBO_10_FORK', 'true')
    pl = [fo(k, 'wrong') for k in ('NEW_10_FORK', 'PLACEBO_10_FORK')]
    out['delta'] = fn.get('delta'); out['p_pre'] = fn.get('p_pre'); out['p_post'] = fn.get('p_post')
    e2 = {k: P1[k].get('e2_identity893') or {} for k in D}
    key = lambda x: _j893.dumps([x.get(f_) for f_ in ('X_sha256', 'action_token_ids', 'pre_C_seal', 'O_sha', 'step_written')], sort_keys=True)
    sc = {'slot_contract_equal': fn.get('slot_contract_equal') is True and fp.get('slot_contract_equal') is True,
          'e2_identity_three_arms': all(set(e2[k]) == {'true', 'wrong'} and e2[k]['true'].get('O_sha') is not None for k in D) and
                                    len({key(e2[k][r]) for k in D for r in ('true', 'wrong')}) == 1,
          'pre_post_identical_NEW_PLACEBO': isinstance(fn.get('p_pre'), dict) and fn.get('p_pre') == fp.get('p_pre') and fn.get('p_post') == fp.get('p_post')
                                            and all(f.get('p_pre') == fn['p_pre'] and f.get('p_post') == fn.get('p_post') for f in pl),
          'new_placebo_same_geometry': all(_j893.dumps([e2[k][r].get(f_) for f_ in ('spans_body', 'body_tokens', 'payload_rows')]) ==
                                           _j893.dumps([e2['NEW_10_FORK']['true'].get(f_) for f_ in ('spans_body', 'body_tokens', 'payload_rows')])
                                           for k in ('NEW_10_FORK', 'PLACEBO_10_FORK') for r in ('true', 'wrong')),
          'new_delta_rows_nonzero_and_reproduced': (fn.get('delta_rows_abs_sum') or 0.0) > 0.0 and (fp.get('delta_rows_abs_sum') or 0.0) > 0.0 and
                                                   fn.get('delta_rows_sha256') == fp.get('delta_rows_sha256') is not None,
          'placebo_delta_rows_zero': all(f.get('delta_rows_abs_sum') == 0.0 and f.get('role') == 'PLACEBO' and f.get('delta') and
                                         all(x == 0.0 for x in f['delta'].values()) for f in pl),
          'headroom_old_Y0': Y['OLD_10_FORK'] == 0,
          'cross_episode_determinism': P1['NEW_10_FORK']['a_wrong'] == t4['PLACEBO_10_FORK'] and P1['PLACEBO_10_FORK']['a_true'] == t4['NEW_10_FORK']}
    out['scientific_checks'] = sc
    out['SCIENTIFIC_VALIDITY'] = 'PASS' if all(sc.values()) else 'INCONCLUSIVE'
    out['ACTION_SEPARATION_NEW_VS_PLACEBO'] = t4['NEW_10_FORK'] != t4['PLACEBO_10_FORK']                       # supporting only
    out['GEOMETRY_EFFECT_PLACEBO_VS_OLD'] = {'t4': [t4['OLD_10_FORK'], t4['PLACEBO_10_FORK']], 'Y': [Y['OLD_10_FORK'], Y['PLACEBO_10_FORK']]}
    out['NONE_reference_Y'] = Y['NONE_10_FORK']
    if out['SCIENTIFIC_VALIDITY'] != 'PASS':
        out['VERDICT'] = 'INCONCLUSIVE'; out['why'] = sorted(k for k, v in sc.items() if not v); return out
    yn, yp, yo = Y['NEW_10_FORK'], Y['PLACEBO_10_FORK'], Y['OLD_10_FORK']
    if yn == 0: out['OUTCOME'], out['VERDICT'] = 'FAIL_NO_GAIN', 'FAIL'
    elif yp == 1: out['OUTCOME'], out['VERDICT'] = 'FAIL_NOT_DELTA_SPECIFIC', 'FAIL'
    elif not out['ACTION_SEPARATION_NEW_VS_PLACEBO']: out['OUTCOME'], out['VERDICT'] = 'INCONCLUSIVE_SAME_DECISION', 'INCONCLUSIVE'
    elif yo == 0: out['OUTCOME'], out['VERDICT'] = 'PASS_DELTA_SPECIFIC_GAIN', 'PASS'
    else: out['OUTCOME'], out['VERDICT'] = 'INCONCLUSIVE_NO_HEADROOM', 'INCONCLUSIVE'                        # unreachable after headroom gate
    out['why'] = [out['OUTCOME']]
    out['stage'] = 'PRELIMINARY_BEFORE_ARTIFACT_GATES (final verdict: receipt test893_final)'
    return out


def final893(prelim, gates):
    # FINAL: the preliminary TEST893 verdict survives only if every artifact gate is True; the scientific fields are kept as recorded
    fail = [k for k in ARTIFACT_GATES892 if not isinstance(gates, dict) or gates.get(k) is not True]
    ok = isinstance(prelim, dict) and prelim.get('VERDICT') in VERDICTS893 and not fail
    out = {'VERDICT': prelim['VERDICT'] if ok else 'TECHNICAL_BLOCK', 'ARTIFACT_STATUS': 'TECHNICAL_BLOCK' if fail else 'PASS',
           'failed_gates': fail, 'gates': gates if isinstance(gates, dict) else None,
           'preliminary': prelim.get('VERDICT') if isinstance(prelim, dict) else None}
    for k in ('PHYSICAL_VALIDITY', 'SCIENTIFIC_VALIDITY', 'OUTCOME', 'ACTION_SEPARATION_NEW_VS_PLACEBO', 'executed_t4', 'Y', 'delta'):
        out[k] = prelim.get(k) if isinstance(prelim, dict) else None
    return out


def print_t893(v):
    try:
        v = v or {}
        print('TEST893 PRELIMINARY VERDICT=%s | PHYSICAL_VALIDITY=%s | SCIENTIFIC_VALIDITY=%s | OUTCOME=%s | why=%s' % (
            v.get('VERDICT'), v.get('PHYSICAL_VALIDITY'), v.get('SCIENTIFIC_VALIDITY'), v.get('OUTCOME'), v.get('why')))
        print('T893 physical=%s' % _j893.dumps(v.get('physical_checks'), sort_keys=True))
        print('T893 scientific=%s' % _j893.dumps(v.get('scientific_checks'), sort_keys=True))
        print('T893 executed_t4=%s | Y=%s | action_separation_NEW_vs_PLACEBO=%s | geometry PLACEBO vs OLD=%s | NONE Y=%s' % (
            v.get('executed_t4'), v.get('Y'), v.get('ACTION_SEPARATION_NEW_VS_PLACEBO'), v.get('GEOMETRY_EFFECT_PLACEBO_VS_OLD'), v.get('NONE_reference_Y')))
        r4 = lambda d: None if d is None else {k: round(x, 4) for k, x in d.items()}
        print('T893 p_pre=%s p_post=%s delta=%s' % (r4(v.get('p_pre')), r4(v.get('p_post')), r4(v.get('delta'))))
        print('T893 actions=%s' % v.get('actions'))
        if v.get('error'): print('T893 ERROR', v['error'])
    except Exception as exc:
        print('T893 VERDICT NOT PRINTABLE %s: %s' % (type(exc).__name__, exc))


# ============================ G0 source facts + CPU selftests (before the model) ============================
def source893():
    # the executed text differs from the renamed TEST892 text only in capture889 + episode889 (+ module statements); every cartridge
    # comes from the own transition; the executed action is untouched
    T, R0 = _a893.parse(SRC889_893), _a893.parse(RENAMED892_893)
    f = {n.name: n for n in T.body if isinstance(n, _a893.FunctionDef)}; f0 = {n.name: n for n in R0.body if isinstance(n, _a893.FunctionDef)}
    C = _a893.parse((ROOT864 / 'TEST893.py').read_text(encoding='utf-8')); fc = {n.name: n for n in C.body if isinstance(n, _a893.FunctionDef)}
    fw = {n.name for t in (_a893.parse(W892_893), _a893.parse(W891_892), _a893.parse(W890_891)) for n in t.body if isinstance(n, _a893.FunctionDef)}
    changed = sorted(k for k in set(f) | set(f0) if k not in f or k not in f0 or _a893.dump(f[k]) != _a893.dump(f0[k]))
    ep = f['episode889']; src_ep = _a893.unparse(ep)
    reading = sorted({_a893.unparse(n.value) for n in _a893.walk(ep) if isinstance(n, _a893.Assign)
                      and any(isinstance(x, _a893.Name) and x.id == 'reading' for x in n.targets)})
    banned = {'write_exp878', 'append_exp878', 'xappend878', 'execute866', 'control_step867', 'donor_v889', 'write_pair889',
              'write_appraisal889', 'load_exp878', 'xcar878', 'car873', 'hop865', 'mount865', 'exec', 'eval', 'setattr', 'globals', 'compile'}
    facts = {'chain_892_reproduced': _h893.sha256(SRC889_892.encode()).hexdigest() == SRC889_892_SHA893,
             'changed_functions': changed == list(CHANGED_FUNCS893),
             'locked_not_redefined': not any(k in fc for k in LOCKED893) and all(_a893.dump(f[k]) == _a893.dump(f0[k]) for k in LOCKED893 if k in f),
             'own_names_unique': not (set(OWN_FUNCS893) & (set(f) | fw)) and set(OWN_FUNCS893) <= set(fc),
             'no_cross_world_donor': 'donor = led[t]' in src_ep and 'donor_v889(' not in src_ep,
             'single_write_t2': "if arm != 'NONE' and (not terminal) and (t == WRITE_STEP893):" in src_ep,
             'single_read_t4': 'ev = eligible889(t) if t == WRITE_STEP893 + LAG889 else None' in src_ep,
             'payload_before_writer': 0 < src_ep.find('fo_inputs893(') < src_ep.find('write_pair889('),
             'executed_reading_unchanged': reading == ["rT['FULL'] if arm == 'D_TRUE' else rW['FULL']", 'r_none', "record['reading']"],
             'action_only_from_reading': [_a893.unparse(n.value) for n in _a893.walk(ep) if isinstance(n, _a893.Assign) and
                                          any(isinstance(x, _a893.Name) and x.id == 'action' for x in n.targets)] == ["reading['action']"],
             'execute866_once': src_ep.count('execute866(') == 1,
             'no_writer_donor_execute_in_new_functions': not any(isinstance(x, _a893.Name) and x.id in banned for n in [fc[k] for k in NEW893]
                                                                 for x in _a893.walk(n)),
             'plan_is_one_world_four_arms': tuple(ep_id893(*p) for p in PLAN893) == EP893 and {p[2] for p in PLAN893} == {'10'},
             'verdict889_untouched': _a893.dump(f['verdict889']) == _a893.dump(f0['verdict889'])}
    if not all(facts.values()): raise Gate_m867('SOURCE893_FACTS %s' % sorted(k for k, v in facts.items() if not v))
    (ROOT864 / 'TEST893_executed_889_890_891_892_893.py').write_text(SRC889_893, encoding='utf-8')
    STATE889['source']['base892'] = B892_INFO893; STATE889['source']['facts893'] = facts
    json_write864('TEST893_base892.json', {'base892': B892_INFO893, 'executed_892_gpu_cell': EXEC892_GPU893, 'facts893': facts,
                                          'changed_functions': changed, 'before_model_load': True})
    print('T893 BASE892 PATCH facts=%s executed_sha256=%s' % (all(facts.values()), B892_INFO893['executed_sha256']), flush=True)


def st893():
    r = {}
    r['expected_schedule'] = [expected893(n) for n in (2, 3, 4, 6)] == [(0, 0), (1, 0), (1, 1), (1, 1)]
    r['episode_ids'] = tuple(ep_id893(*p) for p in PLAN893) == EP893
    h = _h893.sha256(b'x').hexdigest(); cut = APPEND873.get('CUT', 3)
    r['seal_schemas_separate'] = hex64_893(h) and not hex64_893(h.upper()) and not hex64_893({'h': h}) and \
        seal_ok893({'h': h, 'lower': [[h, h]] * (cut + 1)}) and not seal_ok893(h) and not seal_ok893({'h': h, 'lower': [[h, h]] * cut})
    def mk(t4, Y, bad=None, delta=0.1, slots_eq=True, det=True):
        eps, pts, cls = [], [], []
        for k in EP893:
            acts = ['ADVANCE', 'ADVANCE', 'ACQUIRE'] + ([t4[k]] if k in t4 else ['ADVANCE']) + ['ADVANCE', 'ADVANCE']
            eps.append({'episode_id': k, 'actions': acts, 'end': 'HORIZON_6'})
            if k == 'NONE_10_FORK': continue
            nw = k != 'OLD_10_FORK'
            fo = {'role': 'NEW', 'delta': {'x': delta}, 'slot_contract_equal': slots_eq, 'p_pre': {'x': 0.5}, 'p_post': {'x': 0.5 + delta},
                  'delta_rows_abs_sum': abs(delta), 'delta_rows_sha256': 'D%s' % delta} if nw else None
            fz = {'role': 'PLACEBO', 'delta': {'x': 0.0}, 'slot_contract_equal': slots_eq, 'p_pre': {'x': 0.5}, 'p_post': {'x': 0.5 + delta},
                  'delta_rows_abs_sum': 0.0, 'delta_rows_sha256': 'Z'} if nw else None
            e2r = {'X_sha256': 'X2', 'action_token_ids': [1, 2], 'pre_C_seal': 'PC', 'O_sha': 'O', 'step_written': 2,
                   'spans_body': {'V_AFTER': [9, 30 if nw else 22]}, 'body_tokens': 30 if nw else 22, 'payload_rows': 16 if nw else None}
            rd = {'explicit_equals_native_append_bitwise': True, 'B_full_seal_unchanged': True}
            pa = t4['NEW_10_FORK'] if nw else t4[k]; pw = (t4['PLACEBO_10_FORK'] if det or k != 'NEW_10_FORK' else 'STOP') if nw else t4[k]   # det=False: only the PLACEBO read inside NEW differs
            pts.append({'episode_id': k, 'step': 4, 'step_written': 2, 'donor_fit': {'donor_rows': 8, 'true_rows': 8, 'padded_mue': 0},
                        'repeat_reload_bitwise': True, 'read_true': dict(rd), 'read_wrong': dict(rd), 'cartridge_schema893': {'f': True},
                        'format893': 'NEW' if nw else 'OLD', 'X_sha256': 'X', 'B_tokens': 9, 'B_seal893': 'S', 'mounted893': ['a'], 'path893': ['p'],
                        'a_none': 'ADVANCE', 'a_true': pa, 'a_wrong': pw, 'fo893': {'true': {'fo': fo}, 'wrong': {'fo': fz}} if nw else {},
                        'e2_identity893': {'true': dict(e2r), 'wrong': dict(e2r)}})
            cls.append({'episode_id': k, 'ok': True, 'post_appraisal_step': 3})
        st = {'episodes': eps, 'points': pts, 'closures': cls, 'technical_status': 'COMPLETE', 'blocked_episodes': [], 'error': None,
              'scores': {k: {'Y': v} for k, v in Y.items()}}
        if bad: bad(st)
        return verdict893(st, {k: True for k in ('no_physical_failure', 'post_run_integrity', 'cleanup_clean', 'negatives_refused')})
    T4 = lambda o, n, p: {'OLD_10_FORK': o, 'NEW_10_FORK': n, 'PLACEBO_10_FORK': p}
    G = T4('ADVANCE', 'BACKTRACK', 'ADVANCE')
    YY = lambda o, n, p, z=0: {'NONE_10_FORK': z, 'OLD_10_FORK': o, 'NEW_10_FORK': n, 'PLACEBO_10_FORK': p}
    q = lambda v: (v['VERDICT'], v['OUTCOME'])
    YG = YY(0, 1, 0)
    r['pass_reachable'] = q(mk(T4('ADVANCE', 'BACKTRACK', 'ADVANCE'), YY(0, 1, 0))) == ('PASS', 'PASS_DELTA_SPECIFIC_GAIN')
    r['fail_no_gain'] = q(mk(T4('ADVANCE', 'BACKTRACK', 'ADVANCE'), YY(0, 0, 0))) == ('FAIL', 'FAIL_NO_GAIN')
    r['fail_placebo_also_gains'] = q(mk(T4('ADVANCE', 'BACKTRACK', 'BACKTRACK'), YY(0, 1, 1))) == ('FAIL', 'FAIL_NOT_DELTA_SPECIFIC')
    r['fail_delta_harm_vs_placebo'] = q(mk(T4('ADVANCE', 'BACKTRACK', 'ACQUIRE'), YY(0, 0, 1))) == ('FAIL', 'FAIL_NO_GAIN')
    r['same_decision_inconclusive'] = q(mk(T4('ADVANCE', 'BACKTRACK', 'BACKTRACK'), YY(0, 1, 0))) == ('INCONCLUSIVE', 'INCONCLUSIVE_SAME_DECISION')
    r['no_headroom_inconclusive'] = mk(T4('ADVANCE', 'BACKTRACK', 'ADVANCE'), YY(1, 1, 0))['VERDICT'] == 'INCONCLUSIVE'
    r['slot_contract_inconclusive'] = mk(T4('ADVANCE', 'BACKTRACK', 'ADVANCE'), YY(0, 1, 0), slots_eq=False)['VERDICT'] == 'INCONCLUSIVE'
    v0 = mk(T4('ADVANCE', 'BACKTRACK', 'ADVANCE'), YY(0, 1, 0), delta=0.0)
    r['zero_delta_inconclusive_not_block'] = v0['VERDICT'] == 'INCONCLUSIVE' and v0['PHYSICAL_VALIDITY'] == 'PASS' and \
        v0['why'] == ['new_delta_rows_nonzero_and_reproduced']
    for nm_, fn_ in (('e2_pre_C_seal', lambda s: s['points'][2]['e2_identity893']['true'].update(pre_C_seal='PX')),
                     ('e2_X_sha', lambda s: s['points'][0]['e2_identity893']['wrong'].update(X_sha256='XX')),
                     ('e2_action_ids', lambda s: s['points'][1]['e2_identity893']['true'].update(action_token_ids=[1, 3])),
                     ('e2_O_sha', lambda s: s['points'][0]['e2_identity893']['true'].update(O_sha='O2')),
                     ('p_pre', lambda s: s['points'][2]['fo893']['true']['fo'].update(p_pre={'x': 0.4})),
                     ('p_post_placebo_role', lambda s: s['points'][1]['fo893']['wrong']['fo'].update(p_post={'x': 0.7})),
                     ('placebo_nonzero', lambda s: s['points'][1]['fo893']['wrong']['fo'].update(delta_rows_abs_sum=0.5)),
                     ('delta_not_reproduced', lambda s: s['points'][2]['fo893']['true']['fo'].update(delta_rows_sha256='D9')),
                     ('geometry_new_placebo', lambda s: s['points'][2]['e2_identity893']['wrong'].update(body_tokens=31))):
        v_ = mk(G, YG, bad=fn_)
        r['scientific_%s_inconclusive' % nm_] = (v_['VERDICT'], v_['PHYSICAL_VALIDITY']) == ('INCONCLUSIVE', 'PASS')
    r['nondeterminism_inconclusive'] = mk(T4('ADVANCE', 'BACKTRACK', 'ADVANCE'), YY(0, 1, 0), det=False)['VERDICT'] == 'INCONCLUSIVE'
    r['block_missing_episode'] = mk(G, YG, bad=lambda s: s['episodes'].pop())['VERDICT'] == 'TECHNICAL_BLOCK'
    r['block_padding'] = mk(G, YG, bad=lambda s: s['points'][1]['donor_fit'].update(padded_mue=1))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['block_wrong_parity'] = mk(G, YG, bad=lambda s: s['points'][2]['read_wrong'].update(explicit_equals_native_append_bitwise=False))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['block_start_seal'] = mk(G, YG, bad=lambda s: s['points'][2].update(B_seal893='T'))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['block_executed_ne_reading'] = mk(G, YG, bad=lambda s: s['points'][1].update(a_true='STOP'))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['block_non_binary_Y'] = mk(G, dict(YG, NEW_10_FORK=None))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['block_run_status'] = mk(G, YG, bad=lambda s: s.update(technical_status='TECHNICAL_BLOCK'))['VERDICT'] == 'TECHNICAL_BLOCK'
    gates = {k: True for k in ARTIFACT_GATES892}; pv = mk(G, YG)
    r['final_needs_all_gates'] = final893(pv, gates)['VERDICT'] == 'PASS' and \
        all(final893(pv, dict(gates, **{k: x}))['VERDICT'] == 'TECHNICAL_BLOCK' for k in ARTIFACT_GATES892 for x in (False, 'NOT_RUN', None)) and \
        final893(None, gates)['VERDICT'] == 'TECHNICAL_BLOCK' and final893({'VERDICT': 'MAYBE'}, gates)['VERDICT'] == 'TECHNICAL_BLOCK'
    return r


exec(compile(SRC889_893, '889.py:patched_for_TEST890_TEST891_TEST892_TEST893', 'exec'), globals())   # 889 + ... + 893 counted patches
