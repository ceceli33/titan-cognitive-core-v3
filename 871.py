# AKBASCORE SILICON HIPPOCAMPUS — TEST871: NATIVE STATE MISMATCH AFTER A FAILED ACQUIRE (SINGLE COLAB CELL)
# ONE QUESTION: after a failed ACQUIRE, does the model's own pre-decision state contain a component that carries
# "the expected evidence did not arrive" independently of the echo of the previous action, and does it move the next
# decision?
# MECHANISM: at the first post-failure decision point (t3, arm V_X) of three pre-registered 869 MISSING worlds the
# locked engine replays the loop bit-exactly against the 869 full record. At that point the CAR decision forward is
# repeated with ONE input segment replaced at a time (everything else, memory included, fixed):
#   V  = the model's own evaluation rows of t3 ("not a supported step", made WITHOUT seeing feedback)
#   FV = its previous evaluation rows (t2), FK = the rows of its previous decision text (echo of " ACQUIRE")
#   C0 as recorded | C1 V<-V(t2) | C2 FV,FK<-mean embedding (no echo) | C3 C2 + V<-V(t2) | C4 FK<-mean | C5 FV<-mean
#   N1 C2 + V<-norm-matched random rows (negative control)
# Expected if the component exists: C2 gives high P(STOP) (as NO_FEEDBACK did in 869) and C3 removes it, while the
# random control N1 does not. Python never chooses an action: it only builds the declared inputs and reads the model's
# CAR probabilities. No training, hooks, RAG, forced answers or routing. The 560-point panel is never started.
# HOW TO RUN (A100 80GB): paste this whole file into ONE Colab cell and run it once, or upload it and run %run test871.py.
# exec(open(...).read()) is refused: its source cannot be captured.
import ast as _a871, hashlib as _h871, json as _j871, math as _m871, sys as _s871, time as _t871, urllib.request as _u871

ENGINE_URL871 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB871 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc'       # test870.py = the cell run on the A100 in TEST870
ENGINE_LOG_BLOB871 = 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc'   # Test870.log (A100, CALIBRATION_PASS)
MARKER871 = 'AKBASCORE SILICON HIPPOCAMPUS — TEST871'


def blob871(raw):
    return _h871.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts871():
    # The GPU-verified engine is executed unchanged; only I/O names (output file and folder names) are renamed, and every
    # rename is asserted to occur exactly the expected number of times.
    with _u871.urlopen(_u871.Request(ENGINE_URL871, headers={'User-Agent': 'AKBASCORE-TEST871'}), timeout=240) as r:
        raw = r.read()
    assert blob871(raw) == ENGINE_BLOB871, ('ENGINE_BLOB_MISMATCH', blob871(raw))
    text = raw.decode('utf-8')
    _a871.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    prefix, body, suffix = text[a:b], text[b:c], text[d:]
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST871_HUCRE_CIKTISI_%s.txt'", 1),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST871_%s'", 1),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST871_RUN_*'", 1),
               ('prefix', "('870.log', '870_events.jsonl')", "('871_engine.log', '871_events.jsonl')", 1),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST871_RUN_' + STAMP864)", 1),
               ("body", "ROOT864 / '870.log'", "ROOT864 / '871_engine.log'", 1),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '871_events.jsonl'", 1),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST871_SONUC_%s.zip'", 1)]
    parts = {'prefix': prefix, 'body': body, 'suffix': suffix}
    for where, old, new, count in renames:
        assert parts[where].count(old) == count, ('ENGINE_IO_RENAME', where, old, parts[where].count(old))
        parts[where] = parts[where].replace(old, new)
    info = {'url': ENGINE_URL871, 'git_blob': blob871(raw), 'sha256': _h871.sha256(raw).hexdigest(),
            'io_renames': [r[1] + ' -> ' + r[2] for r in renames],
            'executed_sha256': {k: _h871.sha256(v.encode()).hexdigest() for k, v in parts.items()}}
    return parts, info


ENGINE871, ENGINE_INFO871 = engine_parts871()
exec(compile(ENGINE871['prefix'], 'test870.py:prefix', 'exec'), globals())      # console capture, GPU precheck (I/O)
exec(compile(ENGINE871['body'], 'test870.py:engine', 'exec'), globals())        # locked engine definitions (no run)
print('TEST871 ENGINE', _j871.dumps(ENGINE_INFO871, sort_keys=True))

# ============================ TEST871 — pre-registration (written before the model is loaded) ============================
LOCKS864.update({'test870.py': ENGINE_BLOB871, 'Test870.log': ENGINE_LOG_BLOB871})
TEST870_MINUTES = 30.0
TEST865_MINUTES = TEST870_MINUTES
SELECTED871 = ('I867_01_MISSING', 'I867_02_MISSING', 'I867_06_MISSING')
ARM871, POINT_STEP871 = 'V_X', 3
CONDITIONS871 = ('C0_RECORDED', 'C1_V_PRE', 'C2_NO_ECHO', 'C3_NO_ECHO_V_PRE', 'C4_FK_MEAN', 'C5_FV_MEAN',
                 'N1_NO_ECHO_V_RANDOM')
EFFECT_MIN871 = 0.20          # component effect without echo: P(STOP | C2) - P(STOP | C3)
EFFECT_NULL871 = 0.05         # below this the component does not move the decision
RANDOM_FRACTION871 = 0.5      # specific only if |P(STOP|C2) - P(STOP|N1)| <= this x the component effect
ECHO_SURVIVE871 = 0.05        # P(STOP|C0) - P(STOP|C1) above this -> the component still acts under the echo
RANDOM_SEED871 = 871000
PREREG871 = {
    'question': 'After a failed ACQUIRE, does the model\'s own post-failure evaluation (V rows of t3, made without '
                'seeing feedback) carry the failure in a way that moves P(STOP), independently of the echo rows of the '
                'previous step (FK: previous decision text, FV: previous evaluation)?',
    'points': {w: '%s t=%d (first decision after the first executed ACQUIRE)' % (ARM871, POINT_STEP871) for w in SELECTED871},
    'selection_rule': 'MISSING worlds where NO_FEEDBACK and V_X both did ADVANCE, ACQUIRE at t1, t2; NO_FEEDBACK did STOP '
                      'and V_X did ACQUIRE at t3; V_X evaluation at t3 contains "not a supported step" and at t2 does '
                      'not; the first three by world index',
    'conditions': {'C0_RECORDED': 'segments as recorded (must reproduce the 869 CAR token log-probabilities exactly)',
                   'C1_V_PRE': 'V <- V(t2) (= FV rows)', 'C2_NO_ECHO': 'FV, FK <- mean embedding rows, same shape',
                   'C3_NO_ECHO_V_PRE': 'C2 and V <- V(t2)', 'C4_FK_MEAN': 'FK <- mean embedding rows',
                   'C5_FV_MEAN': 'FV <- mean embedding rows',
                   'N1_NO_ECHO_V_RANDOM': 'C2 and V <- norm-matched random rows (seed %d + world)' % RANDOM_SEED871},
    'fixed': 'memory (physical KV of the mounted cards), C, E, R, P rows, prompt, suffix, model; one CAR forward each',
    'metrics': {'e_no_echo': 'P(STOP|C2) - P(STOP|C3)', 'e_random': 'P(STOP|C2) - P(STOP|N1)',
                'e_with_echo': 'P(STOP|C0) - P(STOP|C1)', 'echo_suppression': 'P(STOP|C2) - P(STOP|C0)',
                'fk_part': 'P(STOP|C4) - P(STOP|C0)', 'fv_part': 'P(STOP|C5) - P(STOP|C0)'},
    'verdict': {'CONFIRMED': 'in >= 2 of 3 valid worlds e_no_echo >= %.2f and |e_random| <= %.1f x e_no_echo'
                             % (EFFECT_MIN871, RANDOM_FRACTION871),
                'REFUTED': 'in >= 2 of 3 valid worlds e_no_echo < %.2f' % EFFECT_NULL871,
                'UNDECIDED': 'otherwise, or fewer than 2 valid worlds (valid = exact replay, C0 reproduces the record, '
                             'memory seal and hook audit unchanged)'},
    'limits': ['P(STOP) of the CAR reading is the measured decision; no loop is continued after the point',
               'a segment swap is an input-level intervention on the model\'s own rows, not an internal edit',
               'three worlds, one arm: a mechanism check, not a population estimate']}
PREREG_SHA871 = sha256_bytes864(_j871.dumps(PREREG871, sort_keys=True).encode('utf-8'))
STATE871 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO871, 'prereg_sha256': PREREG_SHA871, 'source': {},
            'offline': {}, 'points': [], 'verdict': None, 'error': None}


def capture_source871():
    # The executed TEST871 code: the IPython cell that contains the marker, else the file this code runs from.
    source, how = None, None
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER871 in t and 'def probe871' in t]
        if hist:
            source, how = hist[-1], 'IPYTHON_CELL_HISTORY'
    except NameError:
        pass
    if source is None and '__file__' in globals():
        with open(globals()['__file__'], encoding='utf-8') as f:
            source, how = f.read(), 'FILE'
    assert source and MARKER871 in source, ('EXECUTED_871_SOURCE_NOT_CAPTURED: paste the whole TEST871 code into ONE '
                                            'notebook cell, or run %run test871.py (exec(open(...)) cannot be captured)')
    tree = _a871.parse(source)
    (ROOT864 / '871.py').write_text(source, encoding='utf-8')
    STATE871['source'] = {'how': how, 'sha256': sha256_bytes864(source.encode('utf-8')),
                          'git_blob': git_blob864(source.encode('utf-8')), 'lines': source.count('\n') + 1}
    return tree


def firewall871(tree):
    # TEST871 code may not act on the loop, may not hook the model and may not read the result into a decision.
    banned_calls = {'execute866', 'mount865', 'free865', 'hop865', 'parse866', 'register_forward_hook',
                    'register_forward_pre_hook', 'register_full_backward_hook', 'install_all_output_capturing_hooks'}
    banned_words = {'output_hidden_states', 'output_attentions'}
    own = {n.name: n for n in tree.body if isinstance(n, _a871.FunctionDef) and n.name.endswith('871')
           and n.name != 'firewall871'}
    bad = {}
    for name, node in own.items():
        calls = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a871.walk(node) if isinstance(c, _a871.Call)}
        words = {getattr(k, 'arg', None) for k in _a871.walk(node) if isinstance(k, _a871.keyword)} | \
                {s.value for s in _a871.walk(node) if isinstance(s, _a871.Constant) and isinstance(s.value, str)}
        hit = sorted((calls & banned_calls) | (words & banned_words))
        if hit:
            bad[name] = hit
    rebinds = [n for n in tree.body if isinstance(n, _a871.Assign) and any(getattr(t, 'id', '') == 'xray_point870'
                                                                           for t in n.targets)]
    assert not bad, ('FIREWALL871', bad)
    assert len(rebinds) == 1 and getattr(rebinds[0].value, 'id', None) == 'probe871', 'FIREWALL871_REBIND'
    STATE871['source']['firewall'] = 'PASS'


def steps871(loop):
    out = []
    for e in loop['events']:
        if e['type'] == 'CONTROL':
            r = e['record']
            out.append({'t': e['step'], 'act': r['action'], 'p': r['reading']['normalized'], 'eval': r['evaluation_text'],
                        'cand': r['candidate_text'], 'sha': r['state_sha256'], 'legacy': r['legacy_raw']})
        elif e['type'] == 'EFFECT' and out:
            out[-1]['effect'] = e.get('effect')
            out[-1]['chosen'] = e.get('chosen')
    return out


def offline871(refs):
    # CPU, records only: the observational picture at the first post-failure decision and the pre-registered selection.
    rows, chosen = [], []
    for w in range(12):
        item = 'I867_%02d_MISSING' % w
        s = {a: steps871(refs[(item, a)]) for a in ('NO_FEEDBACK', 'V_X', 'KV_X', 'NATIVE_FEEDBACK')}
        nf, vx = s['NO_FEEDBACK'], s['V_X']
        ok = len(nf) > 2 and len(vx) > 2 and [x['act'] for x in nf[:2]] == ['ADVANCE', 'ACQUIRE'] and \
            [x['act'] for x in vx[:2]] == ['ADVANCE', 'ACQUIRE'] and nf[2]['act'] == 'STOP' and \
            vx[2]['act'] == 'ACQUIRE' and 'not a supported step' in vx[2]['eval'] and \
            'not a supported step' not in vx[1]['eval']
        row = {'item': item, 'selected_by_rule': ok}
        for a, ss in s.items():
            if len(ss) > 2:
                row[a] = {'t2': ss[1]['act'], 't3': ss[2]['act'], 'p_stop_t3': round(ss[2]['p']['STOP'], 3),
                          'p_acquire_t3': round(ss[2]['p']['ACQUIRE'], 3), 'eval_t3': ss[2]['eval'][:48]}
        if len(vx) > 2 and len(s['KV_X']) > 2:
            row['V_X_equals_KV_X_C_E_V_t3'] = all(vx[2]['sha'][k] == s['KV_X'][2]['sha'][k] for k in ('C', 'E', 'V'))
        rows.append(row)
        if ok:
            chosen.append(item)
        line871('OFFLINE', item, 'rule=%s' % ok, ' | '.join('%s %s->%s P(STOP)=%s "%s"' % (
            a[:5], row[a]['t2'], row[a]['t3'], row[a]['p_stop_t3'], row[a]['eval_t3'][22:48])
            for a in ('NO_FEEDBACK', 'V_X', 'KV_X', 'NATIVE_FEEDBACK') if a in row))
    STATE871['offline'] = {'kind': 'OBSERVATIONAL (869 records, CPU)', 'rows': rows, 'rule_matches': chosen}
    assert tuple(chosen[:3]) == SELECTED871, ('SELECTION_RULE_CHANGED', chosen)


def line871(*parts):
    short864('T871', *parts)


def probs871(reading):
    return {w: round(float(p), 6) for w, p in reading['normalized'].items()}


def probe871(env, ctx, record, state, label):
    # Called by the sealed replay tap at the declared point. The result is stored, never returned to the loop.
    t0 = time.perf_counter()
    vram0 = vram_begin870()
    item = ctx['spec']['item']
    out = {'item': item, 'arm': ctx['arm'], 'step': ctx['steps'], 'label': label, 'recorded_action': record['action'],
           'evaluation_text': record['evaluation_text'], 'candidate_text': record['candidate_text'], 'conditions': {},
           'checks': {}, 'error': None}
    try:
        ctl = [e for e in ctx['events'] if e.get('type') == 'CONTROL']
        eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT']
        out['previous_decision'] = ctl[-2]['action'] if len(ctl) > 1 else None
        out['acquisition_result'] = {k: eff[-1].get(k) for k in ('action', 'effect', 'chosen', 'mounted_after')} if eff else None
        memx, q = ctx['memx'], env['QTEXT841'][ctx['spec']['qid']]
        pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q)))
        post = env['REVIEW_SUFFIX851']
        seg = list(state['segments'])
        names = slot_names869(env, seg)
        idx = {n: i for i, n in enumerate(names)}
        prev = ctx['prev_state']
        c = out['checks']
        c['segments'] = names
        c['segments_unique'] = len(idx) == len(names) and {'FV', 'FK', 'V'} <= set(idx)
        c['fv_is_previous_evaluation'] = bool(torch.equal(seg[idx['FV']][1], prev['V']))
        c['fk_is_previous_decision_rows'] = bool(torch.equal(seg[idx['FK']][1], prev['K']))
        c['v_pre_same_shape'] = tuple(prev['V'].shape) == tuple(seg[idx['V']][1].shape)
        assert c['segments_unique'] and c['fv_is_previous_evaluation'] and c['fk_is_previous_decision_rows'], c
        mue = env['MUE845'].detach().float().cpu().reshape(1, -1)
        rows_of = lambda n: seg[idx[n]][1]
        mean_rows = lambda n: mue.repeat(int(rows_of(n).shape[0]), 1)
        seed = RANDOM_SEED871 + int(item.split('_')[1])

        def put(base, **new):
            s = list(base)
            for n, rows in new.items():
                s[idx[n]] = (s[idx[n]][0], rows)
            return s
        no_echo = put(seg, FV=mean_rows('FV'), FK=mean_rows('FK'))
        cases = {'C0_RECORDED': seg, 'C1_V_PRE': put(seg, V=prev['V']), 'C2_NO_ECHO': no_echo,
                 'C3_NO_ECHO_V_PRE': put(no_echo, V=prev['V']), 'C4_FK_MEAN': put(seg, FK=mean_rows('FK')),
                 'C5_FV_MEAN': put(seg, FV=mean_rows('FV')),
                 'N1_NO_ECHO_V_RANDOM': put(no_echo, V=random_matched865(rows_of('V'), seed))}
        assert tuple(cases) == CONDITIONS871
        seal0 = prefix_seals865(env, memx)
        hook0 = assert_hook_free859(env, 'T871_before_' + item)
        for name, segments in cases.items():
            reading = reading867(car867(env, memx, pre, segments, post))
            out['conditions'][name] = {'action': reading['action'], 'p': probs871(reading)}
            if name == 'C0_RECORDED':
                c['c0_reproduces_record'] = [(s['word'], s['token_logps']) for s in reading['scores']] == \
                    [(s['word'], s['token_logps']) for s in record['reading']['scores']]
        hook1 = assert_hook_free859(env, 'T871_after_' + item)
        c['memory_seal_unchanged'] = prefix_seals865(env, memx) == seal0
        c['hook_free'] = not hook0['hook_count'] and not hook1['hook_count'] and \
            not hook0['transformers_output_capturing_installed'] and not hook1['transformers_output_capturing_installed']
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:300])
        out['traceback'] = traceback.format_exc()
        short864('T871 POINT_ERROR', item, out['traceback'])
    finally:
        gc.collect()
        env['release']()
    out['seconds'] = round(time.perf_counter() - t0, 3)
    out['vram'] = vram_end870(vram0)
    STATE871['points'].append(out)
    for name, r in out['conditions'].items():
        line871('POINT', item, name, 'action=%s' % r['action'], 'P(STOP)=%.3f P(ACQUIRE)=%.3f P(REJECT)=%.3f '
                'P(ADVANCE)=%.3f P(BACKTRACK)=%.3f P(ACCEPT)=%.3f' % tuple(r['p'][w] for w in (
                    'STOP', 'ACQUIRE', 'REJECT', 'ADVANCE', 'BACKTRACK', 'ACCEPT')))
    line871('POINT_CHECKS', item, _j871.dumps(out['checks'], sort_keys=True), 's=%.1f' % out['seconds'],
            'vram=%s' % _j871.dumps(out['vram'].get('xray_overhead_allocated_gib', 'NOT_MEASURED')),
            '' if out['error'] is None else 'ERROR=' + out['error'])


xray_point870 = probe871      # the sealed replay tap calls this name at the declared point; its return value is ignored


def verdict871():
    per, valid = [], []
    reps = {r['item']: r for r in STATE870['replays']}
    for p in STATE871['points']:
        c, cond = p['checks'], p['conditions']
        ok = p['error'] is None and reps.get(p['item'], {}).get('ok') is True and c.get('c0_reproduces_record') is True \
            and c.get('memory_seal_unchanged') is True and c.get('hook_free') is True and len(cond) == len(CONDITIONS871)
        st = {k: v['p']['STOP'] for k, v in cond.items()}
        row = {'item': p['item'], 'valid': ok}
        if len(st) == len(CONDITIONS871):
            row.update({'e_no_echo': st['C2_NO_ECHO'] - st['C3_NO_ECHO_V_PRE'],
                        'e_random': st['C2_NO_ECHO'] - st['N1_NO_ECHO_V_RANDOM'],
                        'e_with_echo': st['C0_RECORDED'] - st['C1_V_PRE'],
                        'echo_suppression': st['C2_NO_ECHO'] - st['C0_RECORDED'],
                        'fk_part': st['C4_FK_MEAN'] - st['C0_RECORDED'], 'fv_part': st['C5_FV_MEAN'] - st['C0_RECORDED']})
            row = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}
            row['specific'] = row['e_no_echo'] >= EFFECT_MIN871 and abs(row['e_random']) <= RANDOM_FRACTION871 * row['e_no_echo']
            row['null'] = row['e_no_echo'] < EFFECT_NULL871
            row['acts_under_echo'] = row['e_with_echo'] > ECHO_SURVIVE871
        per.append(row)
        if ok and 'specific' in row:
            valid.append(row)
    if len(valid) < 2:
        verdict, step = 'BELIRSIZ', 'DUR (technical: fewer than 2 valid worlds)'
    elif sum(r['specific'] for r in valid) >= 2:
        verdict = 'DOGRULANDI'
        step = 'DEVAM' if sum(r['acts_under_echo'] for r in valid) >= 2 else \
            'DEVAM -> next narrowest question: which echo row (FK or FV, see fk_part / fv_part) overrides the component'
    elif sum(r['null'] for r in valid) >= 2:
        verdict, step = 'CURUTULDU', 'YON DEGISTIR -> next narrowest question: does the newly mounted card (memory) ' \
                                     'rather than the evaluation rows carry the failure'
    else:
        verdict, step = 'BELIRSIZ', 'YON DEGISTIR -> the effect is mixed or not specific; separate V from memory first'
    STATE871['verdict'] = {'verdict': verdict, 'next': step, 'per_world': per, 'valid_worlds': len(valid)}
    return STATE871['verdict']


def report871():
    v = STATE871['verdict'] or {}
    print('=' * 100)
    print('TEST871 SUMMARY  (question: echo-independent failure component after a failed ACQUIRE)')
    print('engine test870.py blob %s | TEST871 source %s (%s) | prereg %s' % (
        ENGINE_BLOB871, (STATE871['source'] or {}).get('git_blob'), (STATE871['source'] or {}).get('how'), PREREG_SHA871))
    for p in STATE871['points']:
        cond = p['conditions']
        print('  %s %s | t%d decision %s -> result %s | t%d candidate %r, own evaluation %r, recorded decision %s' % (
            p['item'], p['arm'], p['step'] - 1, p.get('previous_decision'), _j871.dumps(p.get('acquisition_result')),
            p['step'], p['candidate_text'][:20], p['evaluation_text'][:60], p['recorded_action']))
        for name in CONDITIONS871:
            if name in cond:
                print('     %-22s %-9s STOP %.3f  ACQUIRE %.3f  REJECT %.3f' % (
                    name, cond[name]['action'], cond[name]['p']['STOP'], cond[name]['p']['ACQUIRE'],
                    cond[name]['p']['REJECT']))
        print('     checks %s  s=%.1f vram_overhead_gib=%s' % (_j871.dumps(p['checks'], sort_keys=True), p['seconds'],
                                                              p['vram'].get('xray_overhead_allocated_gib', 'NA')))
    for r in v.get('per_world', []):
        print('  EFFECTS', _j871.dumps(r, sort_keys=True))
    print('TEST871 VERDICT %s | NEXT %s | valid worlds %s/%d' % (v.get('verdict'), v.get('next'), v.get('valid_worlds'),
                                                                 len(SELECTED871)))
    print('TEST871 STATUS %s | wall %.0f s | peak GPU %.2f GiB' % (
        STATE871['status'], time.perf_counter() - T_START871,
        max(STATE870['costs'].get('session_peak_allocated_bytes', 0),
            torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0) / 2**30))
    print('GPU EXECUTION NOT VERIFIED BY THE CODE AUTHOR before this run; offline rows are observational only.')
    print('=' * 100)


# ============================ TEST871 — SINGLE CELL EXECUTION ============================
T_START871 = time.perf_counter()
try:
    STATE871['status'] = 'GATE0'
    tree871 = capture_source871()
    firewall871(tree871)
    json_write864('871_prereg.json', {'prereg': PREREG871, 'sha256': PREREG_SHA871, 'before_model_load': True,
                                      'written_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    line871('GATE0 SOURCE', _j871.dumps(STATE871['source'], sort_keys=True), 'prereg', PREREG_SHA871)
    load_sources865()                                    # 81 engine locks + test870.py + Test870.log, git-blob verified
    STATE865['gates']['GATE0_SOURCE'] = {'status': 'PASS', 'locks': len(LOCKS864)}
    log870 = RAW_SOURCES864['Test870.log'].decode('utf-8')
    assert 'XR870 CALIBRATION CALIBRATION_PASS' in log870 and 'NVIDIA A100' in log870, 'TEST870_LOG_NOT_A_PASS'
    feasibility_audit864()
    audit_contracts865()
    load_spine864()
    REFS871 = load_records870()                          # 869 full records: SHA-256, strict JSON, 295 loops, console ENDs
    offline871(REFS871)
    line871('GATE0 PASS', 'selected', SELECTED871)
    # ---------------- GATE1: the GPU-verified engine start (same calls as the TEST870 cell) ----------------
    STATE871['status'] = 'GATE1'
    assert CC_GPU_OK, ('GPU_PRECHECK_NOT_A100_80GB_WITH_40GIB_FREE', CC_GPU)
    env871, original_error871, original_trace871, reproduction871 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace871
    TWO_JOB_VERIFICATION864 = verify_two_job859(env871, original_trace871)
    assert_hook_free859(env871, 'T871_before_native_regression')
    install_offline_evaluator859(env871)
    native871 = native_sequences860(env871)
    NATIVE_REGRESSION864 = native_regression864(env871, native871)
    verify_864_reference865(NATIVE_REGRESSION864)
    ANALYSIS864 = run_analysis863(env871, native871)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores']), 'ORIGINAL_EXACT_RESTORE'
    digest871 = records_digest861(env871)
    null_seal871 = physical_seal863(env871, env871['MEMNULL841'])
    runtime_contracts865(env871)
    runtime_preflight865(env871, reproduction871)
    rearm_budget865(env871)
    make_slots866(env871)
    SLOTS867['PREV_EVALUATION'] = list(env871['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env871)
    assert_hook_free859(env871, 'T871_before_points')
    line871('GATE1 PASS', 'model_load_s=%.0f' % (time.perf_counter() - T_START871))
    # ---------------- GATE2: exact replays to the declared points and the segment interventions ----------------
    STATE871['status'] = 'RUNNING'
    T0_865 = time.perf_counter()
    by_key871 = build_specs869(env871)
    for item in SELECTED871:
        rep871 = run_replay870(env871, {'id': item, 'item': item, 'arm': ARM871,
                                        'targets': {POINT_STEP871: 'FIRST_POST_FAILURE_DECISION'}}, by_key871, REFS871)
        if not rep871['ok']:
            line871('REPLAY_NOT_EXACT', item, _j871.dumps(rep871['mismatch'], default=str)[:600])
    # ====== OFFLINE PHASE: no model call below ======
    inv871 = {'ORIGINAL_RECORD_UNCHANGED': records_digest861(env871) == digest871,
              'MEMNULL841_UNCHANGED': physical_seal863(env871, env871['MEMNULL841']) == null_seal871}
    hook871 = hook_audit859(env871, 'T871_final')
    STATE871['post_run'] = dict(inv871, hook_count=hook871['hook_count'],
                                output_capturing=hook871['transformers_output_capturing_installed'])
    if not all(inv871.values()) or hook871['hook_count'] or hook871['transformers_output_capturing_installed']:
        STATE871['status'] = 'STOPPED_INTEGRITY'
        STATE871['verdict'] = {'verdict': 'BELIRSIZ', 'next': 'DUR (integrity)', 'per_world': [], 'valid_worlds': 0}
    else:
        STATE871['status'] = 'COMPLETE'
        verdict871()
except BaseException as exc:
    STATE871['error'] = '%s: %s' % (type(exc).__name__, exc)
    STATE871['traceback'] = traceback.format_exc()
    STATE871['status'] = 'FAILED_AT_' + str(STATE871['status'])
    STATE871['verdict'] = {'verdict': 'BELIRSIZ', 'next': 'DUR (technical error, see traceback)', 'per_world': [],
                           'valid_worlds': 0}
    print(STATE871['traceback'], file=ERROR_CONSOLE864, flush=True)
    short864('TEST871 FULL TRACEBACK', STATE871['traceback'])
finally:
    try:
        STATE871['replays'] = STATE870['replays']
        json_write864('871_result.json', json.loads(json.dumps(STATE871, default=str, allow_nan=False)))
    except Exception as _exc871:
        print('RESULT_WRITE_FAILED', type(_exc871).__name__, _exc871, file=ERROR_CONSOLE864, flush=True)
    report871()
    if not EVENTS_FILE866.closed:
        EVENTS_FILE866.close()
    LOG_FILE864.close()
exec(compile(ENGINE871['suffix'], 'test870.py:suffix', 'exec'), globals())      # package, Drive copy, download (I/O)
