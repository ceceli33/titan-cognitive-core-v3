# ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio Interface, User Interaction, Research Presentation and Session Logging
# Same working method and interface as the previous Qwen2.5-72B / Siemens demonstrations: start-up runs everything
# automatically (sources, preflight, the original Siemens PDF, the sealed question panel, process 1, process 2, verification,
# the C11 memory, three JPEG figures, ZIP), then the Gradio interface opens with the five raw answer pairs, the figures,
# individual downloads and the package. The interface calls the engine, records and displays. It never computes or edits an answer.
# =====================================================================================================================
# TEST719 program files (part 2 of 2): process 1 (build) and process 2 (C11 alone). Written here with their SHA-256 checked;
# they run as separate Python processes started by step [5] and step [6].
_program_write('TEST719_demo_build.py',r'''# AKBASCORE TEST719-DEMO — PROCESS 1 (build). Real Qwen2.5-72B, unchanged TEST709 engine via unchanged TEST716 setup.
# C01-C10 (716) -> five physical pairs (initialize Ca -> append Cb, 80-layer exact SHA) -> question-independent general pair
# syntheses -> S1-S5 cartridges -> physical S1-S5 joint memory -> general final synthesis -> C11 cartridge (CUT3 WRITE).
# The five demo questions and their expected answers are never read by this process (the build has no access to them).
import os, sys, io, re, gc, json, time, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import TEST719_common as C

RUNS = Path(os.environ.get('T719_RUNS', '/content/T719_RUNS'))
CART716 = Path('/content/AKBASCORE_TEST714/cartridges'); ROOT716 = Path('/content/AKBASCORE_TEST714')
CFG = json.loads((C.HERE / 'TEST719_demo_build_config.json').read_text(encoding='utf-8'))   # prompts, pairs, ceilings only (no questions)

def end_marker(text):
    t = text.rstrip()
    return {'present': 'END OF SYNTHESIS' in text, 'at_end': t.endswith('END OF SYNTHESIS') or t.endswith('END OF SYNTHESIS.')}

def synthesis_status(r, em):
    """Acceptance of a synthesis as cartridge text.
    ACCEPTED  : the end of generation is observed as a stop token (EOS) — or, when the three-way observation cannot confirm it,
                the loop stopped below the ceiling (the unchanged 709 loop stops only at a stop token or at MAX_NEW); the latter is
                flagged FINISH_UNVERIFIED. A missing or misplaced END OF SYNTHESIS line is a format flag, not a reason to stop.
    INCOMPLETE: the safety ceiling was reached (text cut) — no cartridge is written from it."""
    r['generation_status'] = r['status']; flags = []
    if r.get('finish_reason') == 'CEILING' or r['status'] == 'INCOMPLETE':
        return 'INCOMPLETE', ['CEILING_REACHED'], False
    if r.get('finish_reason') != 'EOS':
        flags.append('FINISH_UNVERIFIED')
    if not em['present']:
        flags.append('END_MARKER_MISSING')
    elif not em['at_end']:
        flags.append('END_MARKER_NOT_LAST_LINE')
    return ('COMPLETE' if not flags else 'ACCEPTED_WITH_FLAGS'), flags, True

def npz_bytes(**a):
    import numpy as np
    b = io.BytesIO(); np.savez_compressed(b, **a); return b.getvalue()

class Build:
    def __init__(self):
        import torch
        self.torch = torch; self.prov = C.provenance(torch); self.mode = self.prov['mode']
        self.log = C.EventLog(RUNS / 'build' / 'events.jsonl'); self.store = C.Store(RUNS / 'build_store', None, self.mode, self.log)
        self.eng = C.Engine(self.log, self.mode); self.res = {'status': 'STARTED', 'provenance': self.prov, 'runtime': C.runtime_identity(), 'pairs': [], 'stages': []}
        self.t0 = time.time()

    def save(self):
        self.store.put_json('build_result.json', self.res, 'result')

    def stage(self, name, fn, *a):
        st = C.utc(); t = time.time(); self.log.ev('STAGE_START', name)
        try:
            return fn(*a)
        finally:
            self.res['stages'].append({'stage': name, 'start_utc': st, 'end_utc': C.utc(), 'seconds': round(time.time() - t, 1)})
            self.log.ev('STAGE_END', name, seconds=round(time.time() - t, 1)); self.save()

    def xray(self, h, label):
        K, V, meta = self.eng.xray(h['m'], label)
        self.store.put_bytes(f'xray/{label}.npz', npz_bytes(K=K, V=V), 'xray'); self.store.put_json(f'xray/{label}.json', meta, 'xray_meta'); return meta

    def base_check(self, what):
        self.eng.free_cached(); m = self.eng.mem()
        if m['allocated'] > self.base['allocated'] + 64 * 2 ** 20:      # recorded, not a reason to stop (no effect on the computation)
            self.res.setdefault('memory_notes', []).append({'after': what, 'allocated_above_baseline': m['allocated'] - self.base['allocated'], 'utc': C.utc()})
            self.log.ev('MEMORY_NOTE', f'memory above the model baseline after {what}', allocated_above_baseline=m['allocated'] - self.base['allocated'])
        return m['allocated']

    def with_memory_recovery(self, name, fn, *a):
        """runs a stage; after a GPU memory failure (709 GPU_SAFETY_STOP or CUDA OOM) the partial memory is dropped, unused cached
        memory is released and the stage is rebuilt from the SHA-checked cartridges with the next memory profile (smaller CUT3 chunk,
        then a smaller reserve). Integrity checks are identical in every attempt."""
        for i, (chunk, reserve) in enumerate(C.MEMORY_LADDER):
            self.eng.set_memory_profile(chunk, reserve); err = None
            try:
                out = self.stage(name if i == 0 else f'{name}_retry{i}', fn, *a)
                self.res.setdefault('memory_profile', {})[name] = {'chunk_tokens': chunk, 'reserve_gib': reserve, 'attempt': i + 1}
                return out
            except Exception as e:
                if not C.is_memory_error(e) or i == len(C.MEMORY_LADDER) - 1:
                    raise
                err = f'{type(e).__name__}: {e}'
            gc.collect(); self.eng.free_cached(); m = self.eng.mem()        # the failed attempt's frames are gone here
            nxt = C.MEMORY_LADDER[i + 1]
            self.res.setdefault('memory_recoveries', []).append({'stage': name, 'attempt': i + 1, 'error': err, 'utc': C.utc(), 'free_after_cleanup_gib': round(m['free'] / C.GIB, 2),
                                                                 'next_chunk_tokens': nxt[0], 'next_reserve_gib': nxt[1]})
            self.log.ev('MEMORY_RECOVERY', f'{name}: {err[:160]} - memory released, stage rebuilt from the cartridges', next_chunk_tokens=nxt[0], next_reserve_gib=nxt[1],
                        free_gib=round(m['free'] / C.GIB, 2))

    def forge(self, bid, text, meta):
        # S1-S5 / C11 come from THIS run's generated text: a cartridge left over from an earlier run is removed first, so the
        # 716-style reuse test (file SHA + token count) can never pick up a stale synthesis cartridge of equal length.
        for ext in ('.pt', '.sha256'):
            (CART716 / (bid + ext)).unlink(missing_ok=True)
        rec = self.eng.forge_register(bid, text, meta)
        if rec['reused']:
            raise C.StageError('STALE_SYNTHESIS_CARTRIDGE_REUSED ' + bid)
        for ext in ('.pt', '.sha256'):
            self.store.put_file(f'cartridges/{bid}{ext}', CART716 / (bid + ext), 'cartridge')
        self.store.put_json(f'cartridges/{bid}.book.json', rec, 'book'); return rec

    def gen(self, h, prompt, ceiling, label):
        r = self.eng.answer(h['m'], prompt, ceiling, 9.0, label)
        self.log.ev('GENERATION', label, status=r['status'], n=r['n_generated'], seconds=r['seconds'], peak_gib=round(r['peak'] / C.GIB, 2))
        return r

    # ------------------------------------------------------------------ stages
    def boot(self):
        self.res['model_pin'] = C.pin_model_revision(self.log, self.mode)
        info = self.eng.boot(model_only=False); E = self.eng.E
        self.base = self.eng.mem(); info['baseline'] = self.base
        books = [dict(b) for b in E['R']['books']]; self.res['sources'] = books; self.res['sentinel_before'] = E['before']
        self.res['engine'] = {k: v for k, v in info.items() if k != 'books'}
        self.res['reuse_lines'] = [l for l in self.eng.tee.lines if 'REUSE_SHA_VERIFIED' in l]
        for b in books:
            for ext in ('.pt', '.sha256'):
                self.store.put_file(f'cartridges/{b["id"]}{ext}', CART716 / (b['id'] + ext), 'cartridge')

    def pair(self, k):
        a, b = CFG['pairs'][k]; bounds = self.res['sources']; ia, ib = int(a[1:]) - 1, int(b[1:]) - 1
        rec = {'pair': f'P{k + 1}', 'cartridges': [a, b]}; h = {'m': None}
        h['m'], rec['mount'] = self.eng.mount(a)
        rec['xray_alone'] = self.xray(h, f'P{k + 1}_{a}_alone')
        h['m'], rec['append'] = self.eng.append(h['m'], b)                     # PASS APPEND_ALL_80_LAYERS_EXACT_SHA256 verified
        rec['rows_expected'] = int(self.eng.E['P']) + bounds[ia]['body_tokens'] + bounds[ib]['body_tokens']
        if rec['append']['rows'] != rec['rows_expected']:
            raise C.StageError('PAIR_ROWS ' + rec['pair'])
        rec['kv_gib'] = round(self.eng.kv_bytes(h['m']) / C.GIB, 3)
        seal = self.eng.seals(h['m']); self.store.put_json(f'seals/P{k + 1}.json', seal, 'seal'); rec['seal_seconds'] = seal['seconds']
        rec['xray_joint'] = self.xray(h, f'P{k + 1}_{a}+{b}_joint')
        (a1, a2), (b1, b2) = bounds[ia]['page_range'], bounds[ib]['page_range']
        prompt = CFG['synthesis_prompts']['pair'].format(a=a, b=b, a1=a1, a2=a2, b1=b1, b2=b2)
        syn = self.gen(h, prompt, CFG['ceilings']['pair_synthesis'], f'SYNTHESIS_P{k + 1}')
        syn.update({'prompt': prompt, 'mounted': [a, b], 'memory': 'JOINT_PHYSICAL_PAIR', 'end_marker': end_marker(syn['text'])})
        syn['status'], syn['flags'], syn['accepted'] = synthesis_status(syn, syn['end_marker']); syn['incomplete_reason'] = ','.join(syn['flags']) or None
        self.store.put_json(f'synthesis/P{k + 1}.json', syn, 'synthesis'); self.store.put_text(f'synthesis/P{k + 1}.txt', syn['text'], 'synthesis_text')
        rec['memory_profile'] = {'chunk_tokens': self.eng.E['CHUNK'], 'reserve_gib': self.eng.E['GPU_RESERVE_GIB']}
        rec['synthesis'] = {k2: syn[k2] for k2 in ('status', 'accepted', 'flags', 'generation_status', 'incomplete_reason', 'finish_reason', 'finish_evidence', 'end_marker', 'n_generated', 'ceiling', 'seconds', 'tok_per_s', 'peak', 'sha256')}
        self.eng.release(h); rec['released_alloc'] = self.base_check(rec['pair'])
        self.res['pairs'] = [p for p in self.res['pairs'] if p['pair'] != rec['pair']] + [rec]
        if not syn['accepted']:   # no cartridge is ever written from a cut (ceiling) synthesis
            raise C.StageError(f"PAIR_SYNTHESIS_NOT_COMPLETE P{k + 1}: {syn['status']} ({syn['incomplete_reason']}, finish {syn['finish_reason']}, {syn['n_generated']} tokens, ceiling {syn['ceiling']})")

    def joint(self):
        recs = []
        for k in range(5):
            syn = self.store.get_json(f'synthesis/P{k + 1}.json'); a, b = CFG['pairs'][k]
            if not syn.get('accepted'):
                raise C.StageError(f'PAIR_SYNTHESIS_NOT_COMPLETE P{k + 1}')
            recs.append(self.forge(f'S{k + 1}', syn['text'], {'kind': 'pair synthesis cartridge', 'source_pair': [a, b], 'synthesis_status': syn['status']}))
        self.res['S'] = recs; h = {'m': None}; apps = []
        h['m'], m1 = self.eng.mount('S1')
        for k in range(1, 5):
            h['m'], ar = self.eng.append(h['m'], f'S{k + 1}'); apps.append(ar)
        exp = int(self.eng.E['P']) + sum(r['body_tokens'] for r in recs)
        if self.eng.rows(h['m']) != exp:
            raise C.StageError('JOINT_S_ROWS')
        seal = self.eng.seals(h['m']); self.store.put_json('seals/S_joint.json', seal, 'seal')
        xm = self.xray(h, 'S1-S5_joint')
        fin = self.gen(h, CFG['synthesis_prompts']['final'], CFG['ceilings']['final_synthesis'], 'FINAL_SYNTHESIS')
        fin.update({'prompt': CFG['synthesis_prompts']['final'], 'mounted': ['S1', 'S2', 'S3', 'S4', 'S5'], 'memory': 'JOINT_PHYSICAL_S1-S5', 'end_marker': end_marker(fin['text'])})
        fin['status'], fin['flags'], fin['accepted'] = synthesis_status(fin, fin['end_marker']); fin['incomplete_reason'] = ','.join(fin['flags']) or None
        self.store.put_json('synthesis/FINAL.json', fin, 'synthesis'); self.store.put_text('synthesis/FINAL.txt', fin['text'], 'synthesis_text')
        self.res['joint'] = {'rows': exp, 'appends': [{k2: x[k2] for k2 in ('bid', 'old_rows', 'rows', 'verified', 'pass_line', 'seconds')} for x in apps],
                             'xray': xm, 'memory_profile': {'chunk_tokens': self.eng.E['CHUNK'], 'reserve_gib': self.eng.E['GPU_RESERVE_GIB']},
                             'final': {k2: fin[k2] for k2 in ('status', 'accepted', 'flags', 'generation_status', 'incomplete_reason', 'finish_reason', 'finish_evidence', 'end_marker', 'n_generated', 'ceiling', 'seconds', 'tok_per_s', 'peak', 'sha256')}}
        self.eng.release(h); self.base_check('joint S1-S5')
        if not fin['accepted']:   # C11 is never written from a cut (ceiling) final synthesis
            raise C.StageError(f"FINAL_SYNTHESIS_NOT_COMPLETE: {fin['status']} ({fin['incomplete_reason']}, finish {fin['finish_reason']}, {fin['n_generated']} tokens, ceiling {fin['ceiling']}) - C11 not written")

    def c11(self):
        fin = self.store.get_json('synthesis/FINAL.json')
        if not fin.get('accepted'):
            raise C.StageError('FINAL_SYNTHESIS_NOT_COMPLETE - C11 not written')
        rec = self.forge('C11', fin['text'], {'kind': 'C11 general synthesis cartridge',
                                              'provenance_text': 'model-generated general synthesis of five physical pairs -> physical S1-S5 joint memory -> final general synthesis -> CUT3 WRITE',
                                              'not_a_lossless_physical_merge_of_C01_C10': True, 'final_status': fin['status']})
        self.res['C11'] = rec
        # hand-off: only the sealed C11 cartridge + integrity data for the new process
        hand = RUNS / 'handoff'; shutil.rmtree(hand, ignore_errors=True); hand.mkdir(parents=True)
        for ext in ('.pt', '.sha256'):
            shutil.copyfile(CART716 / ('C11' + ext), hand / ('C11' + ext))
        forbidden = {b['cartridge_sha256']: b['id'] for b in self.eng.E['R']['books'] if b['id'] != 'C11'}
        sizes = sorted({(CART716 / (b['id'] + '.pt')).stat().st_size for b in self.eng.E['R']['books'] if b['id'] != 'C11'})
        import pymupdf as fitz
        doc = fitz.open(str(ROOT716 / 'siemens.pdf')); pdf_text = ''.join(doc[i].get_text(sort=True) for i in range(len(doc)))
        excl = set(C.shingle_hashes(pdf_text, keep=10 ** 9)); sh = set()
        for k in range(5):
            sh.update(sorted(set(C.shingle_hashes(self.store.get_json(f'synthesis/P{k + 1}.json')['text'], keep=10 ** 9)) - excl)[:2000])
        hd = {'allowed': {'C11': {k2: rec[k2] for k2 in ('id', 'cartridge_sha256', 'body_tokens', 'bytes')}}, 'forbidden_cartridge_sha256': forbidden,
              'forbidden_sizes': sizes, 'forbidden_text_shingles': sorted(sh), 'build_runtime': self.res['runtime'], 'sentinel_before': self.eng.E['before'],
              'baseline_allocated': self.base['allocated'], 'kv_row_bytes': self.eng.kv_row_bytes, 'P': self.eng.E['P'],
              'note': 'forbidden_text_shingles cover the five pair syntheses (C11 body text itself is the allowed cartridge content)'}
        (hand / 'handoff.json').write_text(json.dumps(hd, indent=1)); self.store.put_file('handoff/handoff.json', hand / 'handoff.json', 'handoff')
        self.res['handoff_sha256'] = C.sha256_file(hand / 'handoff.json')

    def run(self):
        try:
            self.stage('boot_and_C01-C10', self.boot)
            for k in range(5):
                self.with_memory_recovery(f'pair{k + 1}', self.pair, k)
            self.with_memory_recovery('S1-S5_joint_and_final_synthesis', self.joint)
            self.stage('C11_write_and_handoff', self.c11)
            after = self.eng.E['sentinel'](); self.res['sentinel_after'] = after; self.res['weights_unchanged'] = after == self.eng.E['before']
            if not self.res['weights_unchanged']:
                raise C.StageError('WEIGHTS_CHANGED')
            self.res['status'] = 'BUILD_COMPLETE'
        except Exception as e:
            import traceback
            self.res['status'] = 'ERROR'; self.res['error'] = f'{type(e).__name__}: {e}'; self.res['traceback'] = traceback.format_exc()[-6000:]; raise
        finally:
            self.res['ensure_room_recoveries'] = {'count': len(getattr(self.eng, 'recoveries', [])), 'first': getattr(self.eng, 'recoveries', [])[:5], 'last': getattr(self.eng, 'recoveries', [])[-5:]}
            self.res['wall_seconds'] = round(time.time() - self.t0, 1); self.res['engine_tail'] = self.eng.tee.lines[-40:] if self.eng.tee else []
            self.save(); self.log.ev('BUILD_RESULT', self.res['status']); self.log.close()
            if self.eng.tee:
                self.store.put_text('engine_stdout.log', '\n'.join(self.eng.tee.lines), 'log')
                sys.stdout = self.eng.tee.stream

if __name__ == '__main__':
    Build().run()
''','62a32db92bbadc4f32aef5bfee5003b15c0d45ab292146758128bbc7c079979f')
_program_write('TEST719_demo_ask.py',r'''# AKBASCORE TEST719-DEMO — PROCESS 2 (ask). Started only after process 1 has exited. Same Colab VM, NEW Python process.
# Loads the frozen model (unchanged 716 model-load statements) and ONLY the sealed C11 cartridge. The build directories are
# quarantined: an audit hook refuses (and counts) every file access below them, so this process cannot read C01-C10, S1-S5,
# the syntheses or the source PDF. Then: the five fixed questions to C11, and the same questions to the document-free model.
import os, sys, io, gc, json, time, shutil
from pathlib import Path

QUARANTINE = tuple(str(Path(x)) for x in os.environ.get('T719_QUARANTINE', '').split(':') if x)
QLOG = {'installed': bool(QUARANTINE), 'roots': list(QUARANTINE), 'blocked': [], 'events_checked': 0}
def _hook(event, args):
    if event in ('open', 'os.listdir', 'os.scandir', 'shutil.copyfile', 'shutil.copytree', 'os.rename', 'os.remove') and args:
        QLOG['events_checked'] += 1; p = args[0]
        if isinstance(p, (str, bytes, os.PathLike)):
            try:
                ps = os.path.abspath(os.fsdecode(p))
            except Exception:
                return
            if any(ps == q or ps.startswith(q + os.sep) for q in QUARANTINE):
                if len(QLOG['blocked']) < 50:
                    QLOG['blocked'].append({'event': event, 'path': ps})
                raise PermissionError('TEST719 quarantine: access denied to ' + ps)
if QUARANTINE:
    sys.addaudithook(_hook)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import TEST719_common as C

RUNS_ASK = Path(os.environ.get('T719_ASK_OUT', '/content/T719_ASK')); HAND = Path(os.environ.get('T719_HANDOFF', '/content/T719_ASK_IN'))
QFILE = C.HERE / 'TEST719_demo_questions.json'
CART716 = Path('/content/AKBASCORE_TEST714/cartridges')

def npz_bytes(**a):
    import numpy as np
    b = io.BytesIO(); np.savez_compressed(b, **a); return b.getvalue()

class Ask:
    def __init__(self):
        import torch
        self.torch = torch; self.prov = C.provenance(torch); self.mode = self.prov['mode']
        self.log = C.EventLog(RUNS_ASK / 'events.jsonl'); self.store = C.Store(RUNS_ASK / 'store', None, self.mode, self.log)
        self.eng = C.Engine(self.log, self.mode); self.res = {'status': 'STARTED', 'provenance': self.prov, 'runtime': C.runtime_identity(), 'independence': {}, 'answers': []}
        self.t0 = time.time()

    def save(self):
        self.store.put_json('ask_result.json', self.res, 'result')

    def independence_before_boot(self):
        ind = self.res['independence']; raw = (HAND / 'handoff.json').read_bytes(); self.hd = json.loads(raw)
        ind['handoff_sha256'] = C.sha256_bytes(raw)
        files = sorted(x.name for x in HAND.iterdir())
        ind['handoff_files'] = files
        if files != ['C11.pt', 'C11.sha256', 'handoff.json']:
            raise C.StageError('HANDOFF_DIRECTORY_NOT_C11_ONLY ' + repr(files))
        c11 = self.hd['allowed']['C11']
        if C.sha256_file(HAND / 'C11.pt') != c11['cartridge_sha256']:
            raise C.StageError('C11_SHA_MISMATCH')
        rt = self.res['runtime']; b = self.hd['build_runtime']
        ind['process'] = {'mode': 'NEW_PYTHON_PROCESS_SAME_VM', 'build_pid': b.get('pid'), 'ask_pid': rt['pid'], 'build_exit_code': os.environ.get('T719_BUILD_EXIT_CODE'),
                          'build_ended_utc': os.environ.get('T719_BUILD_ENDED_UTC'), 'ask_started_utc': rt['utc'], 'same_boot_id_as_build': rt['boot_id'] == b.get('boot_id'),
                          'statement': 'new Python process on the same Colab VM; NOT a separate VM or runtime'}
        ind['process']['pass'] = (rt['pid'] != b.get('pid') and ind['process']['build_exit_code'] == '0' and bool(ind['process']['build_ended_utc'])
                                  and ind['process']['build_ended_utc'] < rt['utc'])
        g = C.gpu_processes(); ind['gpu_before_model_load'] = dict(g, **{'pass': g.get('apps') == [] and g.get('memory_used_mib') is not None and g['memory_used_mib'] < 1024})
        ind['engine_cartridge_dir_before_boot'] = sorted(x.name for x in CART716.iterdir()) if CART716.exists() else []
        hf = Path(os.environ.get('HF_HOME', str(Path.home() / '.cache' / 'huggingface')))
        skips = [str(hf), str(RUNS_ASK)] + list(QUARANTINE); t = time.time()
        findings, scanned = C.independence_scan(['/content', '/root', '/tmp', '/home', '/mnt', '/var/tmp'], self.hd['forbidden_cartridge_sha256'], self.hd['forbidden_sizes'],
                                                self.hd['forbidden_text_shingles'], skip_dirs=skips)
        ind['filesystem_scan'] = {'skipped': skips, 'scanned': scanned, 'findings': findings, 'pass': not findings, 'seconds': round(time.time() - t, 1),
                                  'note': 'quarantined build directories are on the same disk; the audit hook shows they were not read'}
        ok = ind['process']['pass'] and ind['gpu_before_model_load']['pass'] and ind['filesystem_scan']['pass'] and not ind['engine_cartridge_dir_before_boot'] and QLOG['installed']
        ind['pre_boot_pass'] = ok; self.save()
        self.log.ev('INDEPENDENCE', 'pre-boot', process=ind['process']['pass'], gpu_empty=ind['gpu_before_model_load']['pass'], fs=ind['filesystem_scan']['pass'])
        if not ok:   # recorded and reported (the isolation claim is then NOT supported); the experiment continues
            self.note('INDEPENDENCE_PRE_BOOT_FAILED', {k: (v.get('pass') if isinstance(v, dict) else v) for k, v in ind.items() if k in ('process', 'gpu_before_model_load', 'filesystem_scan', 'engine_cartridge_dir_before_boot')})

    def boot(self):
        self.res['model_pin'] = C.pin_model_revision(self.log, self.mode)
        info = self.eng.boot(model_only=True); E = self.eng.E
        CART = Path(E['CART']); CART.mkdir(parents=True, exist_ok=True)
        if any(CART.iterdir()):   # recorded; only C11 is registered, so cart_load can load nothing else
            self.note('CARTRIDGE_DIR_NOT_EMPTY', sorted(x.name for x in CART.iterdir()))
        E['R']['books'] = []
        shutil.copyfile(HAND / 'C11.pt', CART / 'C11.pt'); shutil.copyfile(HAND / 'C11.sha256', CART / 'C11.sha256'); self.eng.register_existing(self.hd['allowed']['C11'])
        ind = self.res['independence']
        ind['cartridge_directory'] = {'listing': sorted(x.name for x in CART.iterdir()), 'books': [b['id'] for b in E['R']['books']]}
        ind['cartridge_directory']['pass'] = ind['cartridge_directory']['listing'] == ['C11.pt', 'C11.sha256'] and ind['cartridge_directory']['books'] == ['C11']
        ind['same_weights_as_build'] = {'build': self.hd['sentinel_before'], 'ask': E['before'], 'pass': E['before'] == self.hd['sentinel_before']}
        self.warmup()
        self.base = self.eng.mem(); self.base_ptrs = self.eng.cuda_storage_ptrs(); self.res['engine'] = {k: v for k, v in info.items() if k != 'books'}
        if not (ind['cartridge_directory']['pass'] and ind['same_weights_as_build']['pass']):
            self.note('BOOT_CHECK_FAILED', {'cartridge_directory': ind['cartridge_directory']['pass'], 'same_weights_as_build': ind['same_weights_as_build']['pass']})

    def warmup(self):
        """Observer-only forward over the 716 system prefix (no document, nothing kept). It creates the persistent CUDA
        workspaces (cuBLAS etc.) BEFORE the model-only baseline is taken, so they are not mistaken for foreign memory later."""
        E = self.eng.E; torch = E['torch']; ids = list(E['PIDS']); t = time.time(); m0 = self.eng.mem()
        with torch.no_grad():
            x = torch.tensor([ids], device='cuda:0'); pos = torch.arange(0, len(ids), device='cuda:0').unsqueeze(0)
            out = E['model'](input_ids=x, position_ids=pos, use_cache=False, return_dict=True); del out, x, pos
        E['free_gpu'](); m1 = self.eng.mem()
        self.res['warmup'] = {'tokens': len(ids), 'seconds': round(time.time() - t, 2), 'allocated_before': m0['allocated'], 'allocated_after': m1['allocated'],
                              'note': 'system-prefix forward only; no document; output discarded'}

    def mount_c11(self):
        before = self.eng.mem(); h = {'m': None}; h['m'], mrec = self.eng.mount('C11'); after = self.eng.mem()
        flat = [t for kv in h['m'] for t in kv]
        rows = self.eng.rows(h['m']); exp_rows = int(self.eng.E['P']) + int(self.hd['allowed']['C11']['body_tokens']); exp_bytes = rows * self.eng.kv_row_bytes
        mem_storage, n_storage = self.eng.storage_bytes(flat)
        census = self.eng.cuda_tensor_census(known=flat, baseline_ptrs=self.base_ptrs); tol = 32 * 2 ** 20   # allocator rounding + small temporaries (~100 K/V rows)
        logical = self.eng.kv_bytes(h['m'])   # numel x element size of the 160 mounted K/V tensors
        audit = {'rows': rows, 'rows_expected': exp_rows, 'expected_kv_bytes': exp_bytes, 'memory_logical_bytes': logical,
                 'memory_tensors_all_cuda': all(getattr(t, 'is_cuda', False) for t in flat), 'memory_unique_storage_bytes': mem_storage, 'memory_unique_storages': n_storage,
                 'allocated_model_only_baseline': self.base['allocated'], 'allocated_before_mount': before['allocated'], 'allocated_after_mount': after['allocated'],
                 'allocated_delta': after['allocated'] - before['allocated'], 'allocated_above_model_baseline': after['allocated'] - self.base['allocated'],
                 'census_supporting': census, 'mount': mrec, 'nvidia_smi': C.nvidia_smi(),
                 'what_is_proven': ('(1) the mounted memory has exactly the rows of C11, its 160 K/V tensors hold exactly rows x 327,680 bytes and their unique storages are not smaller (and at most allocator rounding larger); '
                                    '(2) the allocator holds no more than that above the model-only baseline (+ allocator rounding), so no other K/V memory of '
                                    'material size is resident; (3) the content is C11 because cart_load verified the C11 file SHA-256 and the 80-layer seal of the '
                                    'mounted memory is recorded. Detection floor: resident foreign memory smaller than 32 MiB (about 100 K/V rows) cannot be '
                                    'excluded by the allocator check. The gc census (new non-model CUDA storages since the model-only baseline) is supporting '
                                    'only (fails the audit above 4 MiB): it cannot see tensors held inside C/C++ objects, and it can only fail the audit, never pass it.')}
        # logical bytes must match exactly; unique storages may be slightly larger (shared / padded storage) but never smaller
        audit['pass'] = (rows == exp_rows and audit['memory_tensors_all_cuda'] and logical == exp_bytes and exp_bytes <= mem_storage <= exp_bytes + tol
                         and abs(before['allocated'] - self.base['allocated']) <= tol and 0 <= audit['allocated_above_model_baseline'] - exp_bytes <= tol
                         and (census['new_storage_bytes_not_in_memory_since_baseline'] or 0) <= 4 * 2 ** 20)
        self.res['independence']['c11_memory_audit'] = audit
        seal = self.eng.seals(h['m']); self.store.put_json('seals/C11.json', seal, 'seal')
        K, V, meta = self.eng.xray(h['m'], 'C11'); self.store.put_bytes('xray/C11.npz', npz_bytes(K=K, V=V), 'xray'); self.store.put_json('xray/C11.json', meta, 'xray_meta')
        self.res['c11'] = {'rows': rows, 'cartridge_sha256': self.hd['allowed']['C11']['cartridge_sha256'], 'xray': meta, 'memory_audit_pass': audit['pass']}
        self.log.ev('C11_MOUNTED', 'only C11 in GPU memory', rows=rows, audit=audit['pass'])
        if not audit['pass']:   # recorded; the answers are still produced and the report marks the isolation claim as not supported
            self.note('C11_MEMORY_AUDIT_FAILED', {k: audit[k] for k in ('rows', 'rows_expected', 'memory_logical_bytes', 'expected_kv_bytes', 'allocated_above_model_baseline')})
        return h

    def ask_all(self):
        Q = json.loads(QFILE.read_text(encoding='utf-8')); ceil = int(Q['ceilings']['answer'])
        h = self.mount_c11()
        for q in Q['questions']:
            self.one(h['m'], q, ceil, 'C11', 'C11 only (cart_load -> initialize)')
        self.eng.release(h); self.eng.free_cached()
        m = self.eng.mem(); self.res['after_c11_release_allocated'] = m['allocated']
        if m['allocated'] > self.base['allocated'] + 64 * 2 ** 20:
            self.note('C11_NOT_RELEASED', {'allocated_above_baseline': m['allocated'] - self.base['allocated']})
        for q in Q['questions']:
            self.one(None, q, ceil, 'NO_DOCUMENT', 'none: answer(None, question) as in TEST718 vanilla')

    def one(self, memory, q, ceil, cond, mem_label):
        """one sealed question; after a GPU memory failure the unused cached memory is released and the question is asked again
        (same memory, same greedy decoding). A failure that persists is recorded as an ERROR answer; the run continues."""
        r = None; errs = []
        for attempt in (1, 2):
            err = None
            try:
                r = self.eng.answer(memory, q['text'], ceil, 9.0, f'{cond}:{q["id"]}'); break
            except Exception as e:
                err = f'{type(e).__name__}: {e}'
                if not C.is_memory_error(e):
                    errs.append(err); break
            errs.append(err); gc.collect(); self.eng.free_cached(); self.log.ev('MEMORY_RECOVERY', f'{cond} {q["id"]}: {err[:160]} - cached memory released, asking again')
        if r is None:
            r = {'text': '', 'sha256': C.sha256_bytes(b''), 'n_generated': 0, 'ceiling': ceil, 'finish_reason': 'ERROR', 'finish_evidence': {}, 'status': 'ERROR',
                 'seconds': 0, 'utc': C.utc(), 'memory_rows': self.eng.rows(memory), 'error': errs[-1]}
            self.note('ANSWER_FAILED', {'question': q['id'], 'condition': cond, 'errors': errs})
        r.update({'id': q['id'], 'question': q['text'], 'condition': cond, 'memory': mem_label, 'attempt_errors': errs}); self.res['answers'].append(r)
        self.log.ev('ANSWER', f'{cond} {q["id"]}', status=r['status'], n=r['n_generated'], seconds=r['seconds']); self.save()

    def note(self, kind, detail):
        self.res.setdefault('notes', []).append({'kind': kind, 'detail': detail, 'utc': C.utc()}); self.log.ev('NOTE', kind, detail=detail); self.save()

    def run(self):
        try:
            for name, fn in (('independence_before_boot', self.independence_before_boot), ('model_boot_C11_only', self.boot), ('questions', self.ask_all)):
                t = time.time(); self.log.ev('STAGE_START', name); fn(); self.res.setdefault('stages', []).append({'stage': name, 'seconds': round(time.time() - t, 1)})
            after = self.eng.E['sentinel'](); self.res['weights_unchanged'] = after == self.eng.E['before']
            if not self.res['weights_unchanged']:
                self.note('WEIGHTS_CHANGED', {'after': after})
            n_ok = sum(1 for a in self.res['answers'] if a['status'] != 'ERROR')
            self.res['status'] = 'ASK_COMPLETE' if n_ok == 10 else 'ASK_PARTIAL'
        except Exception as e:
            import traceback
            self.res['status'] = 'ERROR'; self.res['error'] = f'{type(e).__name__}: {e}'; self.res['traceback'] = traceback.format_exc()[-6000:]; raise
        finally:
            self.res['independence']['quarantine_audit'] = {'installed': QLOG['installed'], 'roots': QLOG['roots'], 'events_checked': QLOG['events_checked'],
                                                            'blocked_attempts': len(QLOG['blocked']), 'blocked': QLOG['blocked'], 'pass': QLOG['installed'] and not QLOG['blocked']}
            self.res['wall_seconds'] = round(time.time() - self.t0, 1); self.save(); self.log.ev('ASK_RESULT', self.res['status']); self.log.close()
            if self.eng.tee:
                self.store.put_text('engine_stdout.log', '\n'.join(self.eng.tee.lines), 'log'); sys.stdout = self.eng.tee.stream

if __name__ == '__main__':
    Ask().run()
''','3ae13ddb17367bf069b9d369695a51ec7f3f151d3e3f638513a3b517fc1e8106')

def esc(x):return html.escape(str(x))
def card_html(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chip(bid):
    if not bid:return "<span class='chip' style='color:#374151;border-color:#9ca3af'>no document · no cartridge</span>"
    if bid=="C11":return f'<span class="chip" style="color:#fff;background:{C11_COLOR};border-color:{C11_COLOR}">C11</span>'
    i=int(bid[1:])-1 if re.fullmatch(r"C\d\d",bid) else 0;c=ccol(i);return f'<span class="chip" style="color:#fff;background:{c};border-color:{c}">{esc(bid)}</span>'
IND_COL={"CORRECT":"#047857","INCORRECT":"#B91C1C","UNCLEAR":"#B45309","INCOMPLETE":"#6D28D9","UNVERIFIED_FINISH":"#92400E","NOT_PRODUCED":"#6B7280"}

CSS="""
:root{--kz-on:#0f766e;--kz-fg:#111827;--kz-card:#ffffff;--kz-bd:#d1d5db;--kz-a:#1d4ed8;--kz-err:#b91c1c;--kz-warn:#b45309}
.dark{--kz-on:#2dd4bf;--kz-fg:#f3f4f6;--kz-card:#111827;--kz-bd:#4b5563;--kz-a:#60a5fa;--kz-err:#f87171;--kz-warn:#fbbf24}
html,body{overflow-x:hidden!important}
.gradio-container{width:100%!important;max-width:960px!important;margin:0 auto!important;padding-left:10px!important;padding-right:10px!important;box-sizing:border-box!important}
.gradio-container *{box-sizing:border-box}
.kz{color:var(--kz-fg)!important;max-width:100%;overflow-wrap:anywhere;line-height:1.45}
.kz *{color:inherit}
.hero{background:#0b1220;border-radius:6px;padding:18px 18px 14px;margin:4px 0 8px}
.hero,.hero *{color:#f9fafb!important}
.rec{font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;opacity:.85;border:1px solid rgba(255,255,255,.35);display:inline-block;padding:2px 8px;border-radius:3px}
.brand{font-size:clamp(20px,5.6vw,30px);font-weight:800;letter-spacing:.4px;line-height:1.15;margin-top:10px}
.title{font-size:clamp(14px,3.8vw,18px);font-weight:600;margin-top:6px;color:#fde68a!important}
.by{font-size:13.5px;margin-top:10px}
.msg{margin:8px 0 0;padding-left:18px;font-size:13.5px}
.lic{font-size:12px;opacity:.85;margin-top:8px}
.card{background:var(--kz-card);border:1px solid var(--kz-bd);border-left:4px solid var(--kz-bd);border-radius:4px;padding:10px 12px;margin:6px 0}
.card.on{border-left-color:var(--kz-on)}.card.err{border-left-color:var(--kz-err)}.card.warn{border-left-color:var(--kz-warn)}.card.info{border-left-color:var(--kz-a)}
.card .h{font-weight:700;font-size:15px;margin-bottom:4px}
.small{font-size:13.5px}
.mono,.kz code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.chip{display:inline-block;border:1px solid;border-radius:3px;padding:0 6px;font-size:12px;font-weight:700;white-space:nowrap}
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl td,.tbl th{border-bottom:1px solid var(--kz-bd);padding:5px 4px;vertical-align:top;text-align:left}
.tbl th{font-size:12px;opacity:.75}
.stg{font-size:13.5px;margin:2px 0}.stg.done{color:var(--kz-on)!important}.stg.run{color:var(--kz-a)!important;font-weight:700}.stg.wait{opacity:.55}.stg.fail{color:var(--kz-err)!important;font-weight:700}
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0;max-height:420px;overflow:auto}
.ind{font-weight:800;font-size:12.5px;letter-spacing:.3px}
#kz_ask button,#kz_ask{font-size:clamp(15px,4.2vw,18px)!important;font-weight:700!important;min-height:52px!important}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
HERO=(f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B · real industrial manual · measured in this session</span>'
      f'<div class="brand">AKBASCORE AI TECHNOLOGY<br>SILICON HIPPOCAMPUS · SIEMENS SINUMERIK ONE</div><div class="title">FROM TEN PHYSICAL CARTRIDGES TO ONE NEW MEMORY — five physical pair memories, S1–S5, and the cartridge C11</div>'
      '<ul class="msg">'
      f'<li>The original <b>{esc(DOC_TITLE)}, edition {DOC_EDITION_MARK}</b> is downloaded from Siemens in this session and locked by SHA-256. Its 486 pages become <b>ten physical CUT3 cartridges C01–C10</b> (unchanged TEST716/TEST709 engine).</li>'
      '<li><b>Five physical pairs</b> are built on the GPU: initialize(C01) → append(C02) … initialize(C09) → append(C10). Every append is verified by the engine on <b>all 80 layers by exact SHA-256</b>.</li>'
      '<li>From each joint pair memory the frozen model writes one <b>question-independent general synthesis</b> → cartridges <b>S1–S5</b> → physically joined → general final synthesis → new cartridge <b>C11</b>. A synthesis is accepted only if its end is observed as a stop token and it ends with “END OF SYNTHESIS”.</li>'
      '<li><b>Five fixed questions</b> — each verified on the real PDF and sealed before any model was loaded — go to <b>C11 alone in a new Python process</b> (same Colab VM, empty GPU, quarantined build files) and to the same model <b>without any document</b>.</li>'
      '<li>Answers are shown <b>raw and unedited</b>. The indicator is an automatic text rule, <b>not expert verification</b>. C11 is a new memory written from a model-generated synthesis, <b>not a lossless merge</b> of C01–C10.</li></ul>'
      f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(VERSION_NOTE)}</div>'
      f'<div class="lic">{esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a> · Siemens manual © Siemens AG (not redistributed)</div></div>')
SCOPE_HTML=card_html("What this demo shows — and what it does not",
    "Shown, measured in this session: ten physical cartridges from the original 2025 Siemens manual; five physical pair memories, each append verified on all 80 layers by exact "
    "SHA-256 and X-rayed read-only; five question-independent syntheses written as S1–S5; S1–S5 physically joined; a general final synthesis written as the new cartridge C11; "
    "C11 loaded alone in a new Python process with an empty GPU and quarantined build files; five sealed questions answered by C11 and by the model without any document; the "
    "weights stay frozen and every file is SHA-256 verified. Not shown: verified technical correctness (answers are raw; the indicator is automatic); a statistical result (five "
    "questions); a lossless merge of C01–C10 (C11 holds only what the syntheses kept); a separate machine (process 2 runs on the same VM). A correct no-document answer may come "
    "from pre-training. The GPU memory audit cannot exclude foreign memory below 32 MiB.","warn")
PREV_HTML=card_html(PREV_TITLE,f"{esc(PREV_TEXT)}<br><br>For the implementation, experimental evidence, and multi-cartridge question-answering observations, see: "
                    f"<b>Research Record III — Qwen2.5-72B, Direct Internal-State Injection</b> · Zenodo Record 23434686 · "
                    f"<a href='https://zenodo.org/records/23434686' target='_blank' rel='noopener'>https://zenodo.org/records/23434686</a><br>"
                    f"<i>Previously published research — not a result of this Siemens experiment.</i>","info")

def final_card():
    f=INIT.get("final") or {}
    if not f:return ""
    ok=f.get("result")=="VALID"
    body=(f"<b>Scientific result:</b> {esc(f.get('result'))}<br><b>C11 isolation:</b> {esc(f.get('isolation'))}<br><b>Provenance:</b> {esc(f.get('provenance'))}"+
          ("".join(f"<br>⚠ reported gap · {esc(g.get('step'))} · {esc(g.get('kind'))} · {esc(short(g.get('gap'),220))}" for g in f.get("gaps") or []) or "<br>No reported gaps."))
    return card_html("Final status of this run — "+f.get("headline",""),body,"on" if ok and not f.get("gaps") else ("warn" if ok else "err"))

def engine_card_html():
    a=engine_architecture() or {};v=STATE.get("verification") or {};B=build_result();A=ask_result();ph=phases();c11=B.get("C11") or {}
    rows=[("Model",f"{MODEL_ID} · NF4 4-bit, BF16 compute · frozen · pinned snapshot {str((B.get('model_pin') or {}).get('commit'))[:12]}"),
          ("Model release",f"first public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']})"),
          ("Architecture",f"{a.get('layers')} layers · hidden {a.get('hidden')} · {a.get('q_heads')} Q / {a.get('kv_heads')} KV heads · head dim {a.get('head_dim')} · CUT{a.get('cut')}"),
          ("Source document",f"{DOC_TITLE} · edition {DOC_EDITION_MARK} (on {DOC.get('edition_mark_pages')} pages) · {DOC.get('pages')} pages · SHA-256 {str(DOC.get('sha256'))[:16]}… · downloaded {str(DOC.get('download_end_utc'))[:19]} UTC"),
          ("Engine",f"716.py {LOCKS['716.py'][:12]}… · 709.py {LOCKS['709.py'][:12]}… · executed unchanged (only MAX_NEW set per call)"),
          ("Process 1",f"pid {ph.get('BUILD',{}).get('pid')} · {ph.get('BUILD',{}).get('start_utc')} → {ph.get('BUILD',{}).get('end_utc')} · exit {ph.get('BUILD',{}).get('exit_code')} · {B.get('status')}"),
          ("Process 2",f"pid {ph.get('ASK',{}).get('pid')} · {ph.get('ASK',{}).get('start_utc')} → {ph.get('ASK',{}).get('end_utc')} · exit {ph.get('ASK',{}).get('exit_code')} · {A.get('status')} · same Colab VM, new process"),
          ("C11",f"{c11.get('body_tokens')} tokens · SHA-256 {str(c11.get('cartridge_sha256'))[:16]}… · mounted here: {STATE['mount']['rows'] if STATE.get('mount') else '—'} rows"),
          ("Live verification",f"{v.get('passed')}/{v.get('total')} passed · provenance {LIVE.get('provenance')}"),
          ("Generation",f"greedy · sealed panel ≤ {(LIVE.get('questions') or [{}])[0].get('answers',{}).get('C11',{}).get('ceiling','—')} new tokens (safety ceiling) · interface ≤ {INTERACTIVE_MAX_NEW}"),
          ("Engine ready",f"{INIT.get('ready_utc')} · start-up {INIT.get('total_seconds',0)/60:.1f} min")]
    return card_html("Engine (measured at start-up in this session)",'<table class="tbl">'+"".join(f"<tr><th>{esc(x)}</th><td class='mono'>{esc(y)}</td></tr>" for x,y in rows)+"</table>","on")

def stages_html():
    done={s["step"]:s for s in INIT["steps"]};out=[]
    for i,(key,title) in enumerate(INIT_STEPS.items(),1):
        if key in done:cl,mk,m="done","✓",f" — <span class='small'>{done[key]['seconds']:.0f} s</span>"
        elif INIT.get("failed") and INIT["failed"]["step"]==key:cl,mk,m="fail","✗",f" — <span class='small'>{esc(INIT['failed']['error'])}</span>"
        else:cl,mk,m="wait","○",""
        out.append(f"<div class='stg {cl}'>{mk} {i}/{len(INIT_STEPS)} · {esc(title)}{m}</div>")
    pc=100.0*len(done)/len(INIT_STEPS)
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px"><div style="width:{pc:.0f}%;height:10px;background:#0f766e"></div></div>'
    v=STATE.get("verification") or {}
    ver="".join(f"<div class='small'>{'✓' if i['passed'] else '✗'} <span class='mono'>{esc(i['name'])}</span></div>" for i in v.get("items",[]))
    return card_html(f"Full research run at start-up · completed in {INIT.get('total_seconds',0)/60:.1f} min · live verification {v.get('passed')}/{v.get('total')}","".join(out)+bar+
                     "<div style='margin-top:8px'><b>Live verification</b></div>"+ver,"on" if INIT.get("ready") else "err")

def panel_html():
    """the sealed five-question panel: question, PDF evidence, and the two raw answers (C11 alone · no document), unedited"""
    out=[]
    for q in LIVE.get("questions") or []:
        pe=q.get("pdf_evidence") or {};evs=[]
        for ev in pe.get("evidence",[]):
            f=ev.get("found") or {}
            if ev["cartridge"]=="EVERY":evs.append(f"found in {len(f)}/{N_CART} cartridges")
            elif f:evs.append(f"{esc(f['cartridge'])} · PDF page {f['pdf_page']} · “{esc(short(f['snippets'][-1],160))}”")
        t=(f"<b>{esc(q['id'])}</b> · {esc(q['text'])}<div class='small' style='margin-top:4px'>expected (PDF): <b>{esc(q['verifiable_answer'])}</b> · {esc(q['source'])} · region {esc(q.get('region'))}"
           f"<br>source check before model load: {'✓ verified' if pe.get('verified') else '✗ not verified'} — "+" · ".join(evs)+"</div>")
        t+="<table class='tbl'><tr><th>memory</th><th>raw model answer (unedited)</th></tr>"
        for c in ("C11","NO_DOCUMENT"):
            a=q["answers"].get(c) or {};ind=a.get("evaluation","—")
            t+=(f"<tr><td>{chip('C11' if c=='C11' else None)}<div class='ind' style='color:{IND_COL.get(ind,'#6b7280')}'>{esc(ind.replace('_',' '))}</div>"
                f"<div class='small mono'>{esc(a.get('status'))} · finish {esc(a.get('finish_reason'))}<br>{a.get('n_generated')} tok · {a.get('seconds')} s</div></td>"
                f"<td><div class='ans'>{esc(a.get('text',''))}</div><div class='small mono' style='opacity:.75'>{esc(a.get('why',''))}</div></td></tr>")
        t+="</table>"
        if q.get("note"):t+=f"<div class='small' style='opacity:.8'><i>{esc(q['note'])}</i></div>"
        out.append(t)
    return card_html("The five sealed questions — C11 alone (new process) vs no document · raw answers","<hr style='border:0;border-top:1px solid #d1d5db'>".join(out) or "not available","on")

def pdf_card():
    d=DOC
    return card_html("Original Siemens PDF used in this session",
        f"<b>{esc(DOC_TITLE)}</b> · edition {esc(DOC_EDITION_MARK)} (printed on {esc(d.get('edition_mark_pages'))} of {esc(d.get('pages'))} pages) · order no. {esc(d.get('order_number'))} · {esc(d.get('software_version'))}<br>"
        f"downloaded {esc(d.get('download_start_utc'))} → {esc(d.get('download_end_utc'))} UTC · {d.get('bytes',0):,} bytes · SHA-256 <span class='mono'>{esc(d.get('sha256'))}</span> (= TEST716 lock)<br>"
        f"⬇ <a href='{PDF_URL}' target='_blank' rel='noopener'><b>Download the original PDF from the official Siemens address</b></a> and compare its SHA-256 with the value above "
        f"(record: SOURCE_DOCUMENT_RECORD.json).<br><i>{esc(PDF_POLICY)}</i> <a href='{PDF_TERMS_URL}' target='_blank' rel='noopener'>Siemens terms</a>. "
        f"The verified copy stays only inside this Colab runtime: <span class='mono'>{esc(d.get('verified_local_copy'))}</span>","info")
def cond_choices():
    c=build_result().get("C11") or {}
    return [(f"C11 · new cartridge from the general final synthesis · {c.get('body_tokens','—')} tokens","C11"),("No document · frozen model only","NONE")]
def question_choices():return [q["text"] for q in (LIVE.get("questions") or [])]
def condition_info(sel):
    m=STATE.get("mount") or {}
    head=f"Mounted now: {chip('C11')} · {m.get('rows','—'):,} rows · loaded in this notebook process after process 2 ended" if m else "No memory mounted."
    if sel=="NONE":head+="<br><b>No document selected</b> — the question is answered without any cartridge."
    head+=(f"<br>Questions asked here are <b>not part of the sealed panel</b>. Up to {INTERACTIVE_MAX_NEW} new tokens; the end of generation is reported "
           "(EOS = stop token observed; CEILING = cut at the limit; UNVERIFIED = not confirmed).")
    return card_html("Memory condition",head,"info")

def answer_html(r,c):
    t="<table class='tbl'><tr><th>memory</th><th>raw model answer</th><th class='hide-m'>time</th></tr>"
    for x in (r,c):
        if x is None:continue
        t+=(f"<tr><td>{chip(x['cartridge'])}<div class='small mono'>{x['cache_tokens']:,} rows · {x['n_generated']} tok<br>{esc(x['status'])} · finish {esc(x['finish_reason'])}</div></td>"
            f"<td><div class='ans'>{esc(x['raw'])}</div></td><td class='hide-m mono'>{x['seconds']} s</td></tr>")
    t+="</table>";x=r or c
    t+=(f"<div class='small mono' style='margin-top:8px;opacity:.8'>question {esc(x['question'])}<br>max new tokens {INTERACTIVE_MAX_NEW} · NOT VERIFIED — check against the Siemens PDF · "
        f"not part of the sealed panel · GPU free {x['gpu'].get('free_gib')} GiB · {esc(x['utc'])}</div>")
    return card_html("Answer of the frozen Qwen2.5-72B — raw output, unedited",t,"on")

GPU_LOCK=threading.Lock()
def busy_card():return card_html("Busy","Another run is using the GPU. Please wait until it has finished and press the button again.","warn")
def err_card(ex):
    oom="OutOfMemoryError" in type(ex).__name__ or "GPU_SAFETY_STOP" in str(ex) or "PRE_GENERATION_CHECK" in str(ex)
    hint=" The TEST709 GPU safety reserve stopped the operation (or CUDA ran out of memory). Press ASK again." if oom else ""
    return card_html("Error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code>{esc(hint)}<br>Nothing was hidden or replaced; the full traceback is in the Error log tab.","err")

def all_files():
    figs=[FIG_FILES[k]["jpg"] for k in FIGURES if k in FIG_FILES]
    return figs+[str(ZIP_PATH)]+[p for _,p in download_items() if Path(p).is_file()]
def gallery_items():return [(FIG_FILES[k]["jpg"],FIGURES[k]) for k in FIGURES if k in FIG_FILES]
def summary_text():
    try:return RUN_SUMMARY.read_text(encoding="utf-8")
    except Exception:return ""
def refresh_package():
    try:package_session()
    except Exception as ex:slog("PACKAGE_FAILED",str(ex))
    return all_files(),(str(ZIP_PATH) if ZIP_PATH.is_file() else None),summary_text()

def ask_handler(sel,question,control):
    NO=("","",None)
    keep=(gr.update(),gr.update(),gr.update(),condition_info(sel))
    if not GPU_LOCK.acquire(blocking=False):yield (busy_card(),)+NO+keep;return
    try:
        q=(question or "").strip()
        if not q:raise OpError("Type a question first.")
        r=None;c=None
        if sel=="C11":
            yield (card_html("Running",f"C11 mounted · asking the frozen model{' and the model without any document' if control else ''} (up to {INTERACTIVE_MAX_NEW} tokens each) …","info"),)+NO+keep
            r=ask_live(q[:3000],True)
            if control:c=ask_live(q[:3000],False)
        else:
            yield (card_html("Running","Asking the model without any document …","info"),)+NO+keep
            c=ask_live(q[:3000],False)
        rec=dict(question=q,selection=sel,memory=r,no_document=c,session=SESSION_ID,sealed_panel=False)
        d=SESSION_DIR/"single_runs";d.mkdir(exist_ok=True)
        p=dump_json(d/f"ASK_{sel}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json",rec)
        files,z,summ=refresh_package()
        yield (answer_html(r,c),json.dumps(jsafe(rec),ensure_ascii=False,indent=1)[:200000],"",str(p),files,z,summ,condition_info(sel))
    except Exception as ex:
        slog("UI_ERROR","ask",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:])
        files,z,summ=refresh_package()
        yield (err_card(ex),"",traceback.format_exc(),None,files,z,summ,condition_info(sel))
    finally:GPU_LOCK.release()

def verify_handler():
    if not GPU_LOCK.acquire(blocking=False):return busy_card()
    try:
        w=verify_weights();d=verify_disk()
        rows=[("time (UTC)",w["utc"]),("weight sentinel of process 1 at load",w["before"]),("weight sentinel now (this process)",w["after"]),("sentinel unchanged",w["passed"]),
              ("trainable tensors",sum(1 for p in E["model"].parameters() if p.requires_grad))]+[(f"cartridge {f['cartridge']} SHA-256 on disk = record",f["equals_record"]) for f in d["files"]]
        ok=w["passed"] and d["passed"] and rows[4][1]==0
        return card_html("Weight and cartridge verification · measured now","<table class='tbl'>"+"".join(f"<tr><th>{esc(a)}</th><td class='mono'>{esc(b)}</td></tr>" for a,b in rows)+"</table>","on" if ok else "err")
    except Exception as ex:return err_card(ex)
    finally:GPU_LOCK.release()

def _tb(**kw):
    for extra in (([{"buttons":["copy"]}] if _GR_MAJOR>=6 else [])+[{"show_copy_button":True},{}]):
        try:return gr.Textbox(**extra,**kw)
        except TypeError:continue
def _gallery(**kw):
    try:return gr.Gallery(columns=1,height="auto",object_fit="contain",preview=False,**kw)
    except TypeError:return gr.Gallery(**kw)

def build_ui():
    blocks=gr.Blocks(title=APP_SHORT) if _GR_MAJOR>=6 else gr.Blocks(css=CSS,title=APP_SHORT)
    qs=question_choices()
    with blocks as demo:
        gr.HTML(HERO);gr.HTML(final_card());gr.HTML(engine_card_html())
        gr.HTML(panel_html())
        cond_dd=gr.Dropdown(choices=cond_choices(),value="C11",label="Memory condition (the new cartridge C11, or the model without any document)",interactive=True)
        info=gr.HTML(condition_info("C11"))
        cq=gr.Dropdown(choices=qs,value=(qs[0] if qs else None),allow_custom_value=True,label="Question (pick one of the sealed questions or type your own; raw output, not verified)",interactive=True)
        ctl=gr.Checkbox(value=True,label="Also ask the same question to the model without any document")
        ask_b=gr.Button("ASK",variant="primary",elem_id="kz_ask")
        status=gr.HTML(stages_html())
        gallery=_gallery(label=f"Figures 1–{len(FIGURES)} (JPEG, 300 dpi) — measured in this session",value=gallery_items())
        files=gr.File(label="Individual downloads · figures, ZIP, run summary, process outputs, records, syntheses, manifest, historical logs",value=all_files(),file_count="multiple",interactive=False)
        gr.HTML(pdf_card())
        zipb=gr.DownloadButton(label="⬇ Download the complete experiment package (.zip)",value=str(ZIP_PATH),interactive=True)
        single_file=gr.File(label="Record of the last question (.json)",interactive=False)
        with gr.Tabs():
            with gr.Tab("Run summary"):summ=_tb(lines=14,max_lines=40,label="RUN_SUMMARY.txt",value=summary_text())
            with gr.Tab("Raw record (last question)"):raw=_tb(lines=14,max_lines=40,label="JSON")
            with gr.Tab("Error log"):errs=_tb(lines=10,max_lines=40,label="traceback (empty = no error)")
        with gr.Accordion("Verify the frozen weights and all cartridge files now",open=False):
            vb=gr.Button("Verify now");vout=gr.HTML()
        gr.HTML(SCOPE_HTML);gr.HTML(PREV_HTML)
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:8px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · '
                f'TEST716 <a href="{URL_716}" target="_blank" rel="noopener">716.py</a> · TEST709 <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · '
                +" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{esc(t.split(" — ")[0])}</a>' for t,u in LINEAGE)+
                ' · Qwen2.5-72B-Instruct, the Siemens manual and third-party libraries remain under their own licences.</div>')
        cond_dd.change(condition_info,inputs=cond_dd,outputs=info)
        outs=[status,raw,errs,single_file,files,zipb,summ,info]
        ask_b.click(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs)
        vb.click(verify_handler,outputs=vout)
    try:demo.queue(default_concurrency_limit=1)
    except TypeError:demo.queue(concurrency_count=1)
    return demo

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (as in the previous demonstrations): the experiment runs automatically, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
try:run_initialization()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m or "BLOB" in _m or "DRIFT" in _m else
           "A program file of this cell was altered while copying: paste PART 1, PART 2 and PART 3 again, unchanged." if "PROGRAM FILE" in _m else
           "The expected answer of a fixed question was not found on the real PDF: the run stopped BEFORE any model was loaded. The question panel must be corrected; see QUESTION_PANEL_SOURCE_CHECK.json." if "SOURCE CHECK" in _m else
           "GPU memory: process 1 stopped after all memory recoveries (cached-memory release, smaller CUT3 chunk, smaller reserve). The cartridges already written on disk are reused by the next run: Runtime → Restart session, then run again." if "GPU_SAFETY_STOP" in _m or "out of memory" in _m.lower() else
           "A synthesis was cut at its safety ceiling: no cartridge was written from it and the run stopped. The records show where." if "SYNTHESIS_NOT_COMPLETE" in _m else
           "Process 1 stopped; its last lines are above and in records_console/BUILD.log. Completed parts (C01–C10 on disk) are reused by the next run." if "PROCESS 1" in _m or "BUILD process" in _m else
           "The Siemens PDF could not be downloaded or no longer matches the locked SHA-256: check the network or the Siemens address and run again." if "SOURCE DOCUMENT" in _m else
           "Hugging Face refused the model download: add your token as the Colab secret HF_TOKEN (allow notebook access) and run again." if any(x in _m for x in ("401","403","gated","Unauthorized","token")) else
           "GPU memory: the TEST709 safety reserve or CUDA stopped the run. Use an A100 80 GB runtime (Runtime → Change runtime type), restart the session and run again." if any(x in _m for x in ("GPU_SAFETY_STOP","out of memory","PRE_GENERATION_CHECK")) else
           "The GPU is in use by another process: Runtime → Restart session, then run again (completed phases are reused)." if "not empty" in _m or "another process" in _m else
           "This runtime is not an A100 80 GB: Runtime → Change runtime type → A100, then run again." if any(x in _m for x in ("A100","CUDA is not available","exactly one GPU")) else
           "Disk: free space in the Colab runtime (or use a runtime with more disk) and run again." if "disk" in _m.lower() else
           "Network error while downloading a locked source, the Siemens PDF or the model: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection")) else
           "See the traceback above; nothing was changed in the engine.")
    _OUT.write("\n"+"="*110+f"\nENGINE START FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}\n"
               f"All files of this attempt (ZIP): {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}\n"+"="*110+"\n");_OUT.flush()
    raise
GRADIO_LINK=DEMO_ROOT/"GRADIO_LINK.txt"
def launch_interface():
    """(re)starts the Gradio interface of THIS session. A public share link is tried first; if the tunnel is not available,
    the interface is opened through Colab's own port window. The link is printed in a banner and written to GRADIO_LINK.txt.
    Nothing is recomputed. The same function is used by the reconnect cell."""
    global demo
    try:demo.close()
    except Exception:pass
    demo=build_ui()
    kw=dict(share=True,allowed_paths=[str(SESSION_DIR)],show_error=True,inline=False,prevent_thread_lock=True)
    if _GR_MAJOR>=6:kw["css"]=CSS
    err=None
    for _ in range(5):
        try:demo.launch(**kw);break
        except TypeError as ex:
            bad=next((k for k in ("css","prevent_thread_lock") if k in str(ex) and k in kw),None)
            if bad is None:raise
            kw.pop(bad)
        except Exception as ex:
            if not kw.get("share"):raise
            err=f"{type(ex).__name__}: {ex}";kw["share"]=False;slog("LAUNCH_NOTE","public share link not available — opening the local interface",error=err)
    share=getattr(demo,"share_url",None);local=getattr(demo,"local_url",None);window=None
    if not share:
        try:
            from google.colab import output as _co
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST719 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    rec=dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err,
             note="gradio.live links are temporary; run the reconnect cell to obtain a new link (nothing is recomputed)")
    dump_json(GRADIO_LINK.with_suffix(".json"),rec);GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or '— (tunnel not available; use the Colab window link above)'}\n"
           f"  local       : {local}\n  also saved in {GRADIO_LINK}","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
launch_interface()
# ===== END OF PART 3/3 =====
