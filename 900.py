# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST900 — continuation of TEST898 / TEST899 — protocol v1.2.1
# S2-D native determination table: instructed native write-time inference -> physical CUT3/H3/KV card -> next native greedy act
#
# FILE: 900.py (published path at the root of ceceli33/titan-cognitive-core-v3). Entry: `python 900.py [--flags]` or one Colab
# cell (`%run 900.py`, or the Raw text pasted into one cell). Paths come from CLI flags or T900_* environment variables
# (e.g. T900_PF_REPORT, T900_PF_MANIFEST, T900_AUTHORIZATION, T900_PACKAGE_DIR; set them with os.environ before a pasted cell).
# Exit / return code: 0 = run complete and technically valid, 1 = technical abort or invalid, 2 = LOCKED before any GPU work.
#
# STATUS: PROVISIONAL_IMPLEMENTATION — NOT_GPU_AUTHORIZED. Written on the project owner's limited authorisation of 2026-11-19
# BEFORE the conditions of contract v1.2.1 §16 (a real binding preflight PASS + independent K3.1 acceptance) were met. This
# deviation from §16 is declared here and in every report; the contract is NOT edited. The GPU experiment starts only if, on
# CPU and before torch is imported:
#   GATE 0  sealed input package (contract md/json SHA-256, SHA256SUMS, CC-900 K0-K14 incl. K13), pinned sources by git blob,
#           results JSON bytes of TEST897/898/899;
#   GATE 1  the user-supplied binding preflight900_report.json + preflight900_manifest.json: overall PASS, binding true,
#           backend hf, not injected, fatal [] and missing [], pass1 == pass2 == published SHA, contract/sources/archives
#           pinned, REL-FLIP variant recorded (EMULATOR_NON_BINDING / TEST_INJECTED_NON_BINDING are rejected);
#   GATE 2  a written authorisation record: independent acceptance of exactly this package + a separate GPU execution
#           permission bound to the contract SHA, the package SHA256SUMS, the PF manifest SHA and the 900.py git blob;
# and then GATE 3 (A100: executed 900.py == published 900.py, pinned runtime, GPU-side preflight repeat == reference manifest,
# archives, model, engine) and GATE 4 (runtime: geometry, lineage replay, invariants I1-I11, readout counter <= 109).
# There is NO force / demo / auto-yes / skip / fallback flag. Missing evidence -> LOCKED report, exit code 2, no GPU work.
#
# CHAIN: TEST897 (897npdm_smoke.py blob fbde1d13, commit 813cdca7, NPDM_FAIL) -> TEST898 (898.py blob 14be60ac, sha256 98bfa475,
#        NRBC_SCREEN_FAIL) -> TEST899 (899.py blob 28590849, sha256 c50ac3aa, commit 0ce81afd) -> TEST900 v1.2.1 (this file).
# ENGINE (frozen, commit f1007d91; TEST899 LOCKS): 709.py blob 6c9f8cbb (sha256 68516eb1; answer, cache), 730.py blob b1bad9eb
#        (forge_native, seal_cp, initialize_native, to_gpu, DirectCut3), 757.py blob 3d88bf86 (model_setup, native_append_direct).
# CONTRACT: TEST900_PROTOKOL_SOZLESMESI_v1_2_1.md   sha256 03afcbcd1c36c57cfb79ba17410c019003a5217c13dbf9dedc014756cfc3343f
#           TEST900_SOZLESME_SABITLERI_v1_2_1.json  sha256 e8ef2c4e369a0b6a88e3071a2ed187a8f2e53f4219842884b7bcd24889f6f520
#           input_package/SHA256SUMS.txt            sha256 61e75f683b64c6283079b3f7e960dea56861b669a3a0911b69a19891a420bd5d
# MODEL: frozen Qwen/Qwen2.5-72B-Instruct @ 495f39366efef23836d0cfae4fbe635880d2be31, NF4 weights / BF16 compute, one
#        NVIDIA A100-SXM4-80GB, 80 layers / H 8192 / 64 Q / 8 KV / HD 128, CUT3 = H3 + KV(L0-L3), P = 30.
# RUNTIME PINS: Python 3.13, torch 2.14.1+cu130, CUDA 13.0, transformers 5.22.1, accelerate 1.16.0, bitsandbytes 0.50.2,
#        tokenizers 0.23.3 (fail-closed).
# LIMITS: no training / fine-tuning / LoRA / RAG / hooks / prompt replay of experiment history / answer override / oracle
#   routing / evaluator leakage / teacher-score substitution. The decision is ONLY the greedy output of the locked 709
#   answer(); ACT, ACQUIRE, STOP and INVALID are separate events; budget exhaustion is a harness event, never a model STOP.
#   Teacher-forced scores (CAR, candidates, probes) are measurements and never change, replace or repair a decision.
#   CANON-NAT = INSTRUCTED_NATIVE_INFERENCE at write time: not learning, not autonomy, not value learning, not transfer.
#   Q / OPT / true tables / vault values exist in memory only after GENERATION_SEALED (the contract JSON is re-read then);
#   the vault file is opened only inside a branch environment at ENV(k), after WRITE-INTENT(k).
# REUSE: engine definitions are AST-selected from the blob-verified 709/730/757 sources (TEST899 SELECT); NPDM / 898 / 899
#   helper definitions and the nested guard / cartridge / car_logp_898 functions are taken verbatim (AST) from the blob-
#   verified 897/898/899 sources; tools/preflight900.py, tools/rules900.py and tools/cc900.py are loaded by path from the
#   sealed input package. Nothing in 897.py / 898.py / 899.py / the package is modified; nothing is written into input_package.
# NOT EXECUTED ON GPU BY ITS AUTHOR. GPU BEHAVIOUR NOT VERIFIED. CPU mock tests exercise the gates and the orchestration only.
# =====================================================================================================================
import os, sys, json, hashlib, re, time, math, ast, shutil, subprocess, textwrap, importlib.util, importlib.metadata
import platform, random, traceback, types, urllib.request, zipfile, gc
import itertools as _it
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True                       # nothing (no __pycache__) may ever be written into the sealed input_package
TORCH_PRELOADED = 'torch' in sys.modules             # recorded: a LOCKED run must not have imported torch itself

TAG = 'TEST900'
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST900 — continuation of TEST898 / TEST899 — protocol v1.2.1'
IMPLEMENTATION_STATUS = 'PROVISIONAL_IMPLEMENTATION — NOT_GPU_AUTHORIZED'
SECTION16_DEVIATION = ('contract v1.2.1 §16 requires a binding PF PASS and independent acceptance before 900.py is produced; '
                       'this file was written earlier on the owner\'s limited authorisation (2026-11-19) and is therefore '
                       'PROVISIONAL; its GPU path is locked behind GATE 1 and GATE 2 and the contract is unchanged')
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = '900.py'
CONTRACT_MD = 'TEST900_PROTOKOL_SOZLESMESI_v1_2_1.md'; CONTRACT_JSON = 'TEST900_SOZLESME_SABITLERI_v1_2_1.json'
CONTRACT_MD_SHA = '03afcbcd1c36c57cfb79ba17410c019003a5217c13dbf9dedc014756cfc3343f'
CONTRACT_JSON_SHA = 'e8ef2c4e369a0b6a88e3071a2ed187a8f2e53f4219842884b7bcd24889f6f520'
PACKAGE_SUMS_SHA = '61e75f683b64c6283079b3f7e960dea56861b669a3a0911b69a19891a420bd5d'
ENGINE_COMMIT = 'f1007d912773f3460536784ff80a215741bc97e9'
ENGINE_BLOBS = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
                '757.py': '3d88bf8638390995858f23391f1e043faa586835'}
TEST_SOURCES = {'897npdm_smoke.py': 'fbde1d130712014070fa6db45ff36f05f9f9d06c', '898.py': '14be60ac98c1f6425e707f1967a6b688e5247e00',
                '899.py': '28590849ec1bc62afc875dc390c0529e3ad35f8f'}
SOURCE_KEY = {'709.py': 'src_709', '897npdm_smoke.py': 'src_897', '898.py': 'src_898', '899.py': 'src_899'}
PACKAGE_TOOLS = ('tools/cc900.py', 'tools/preflight900.py', 'tools/rules900.py')
ARCH897 = {'root': 'NPDM_SMOKE_20261118T223234Z', 'run_id': '20261118T223234Z', 'verdict': 'NPDM_FAIL',
           'results_name': 'NPDM_SMOKE_results.json', 'manifest_name': 'NPDM_SMOKE_public_manifest_SEALED.json',
           'vault_name': 'NPDM_SMOKE_evaluator_vault.json', 'cell_name': 'NPDM_SMOKE_cell_source.py',
           'cartridges': ('T896_EMPTY.pt', 'T896_L3_00_MODEL_INTENT_t1.pt', 'T896_L3_01_MODEL_PREDICTION_t1.pt', 'T896_L3_02_OBSERVED_OUTCOME_t1.pt')}
ARCH898 = {'root': 'TEST898_NRBC_20261119T090123Z', 'run_id': '20261119T090123Z', 'results_name': 'TEST898_NRBC_results.json',
           'real_file': 'T896_L3_BELIEF_L3_REAL.pt', 'real_cid': 'L3_BELIEF_L3_REAL', 'real_generation': 'C3'}
DEFAULT_PATHS = {'res_897': '/content/drive/MyDrive/NPDM_SMOKE_20261118T223234Z/NPDM_SMOKE_results.json',
                 'res_898': '/content/drive/MyDrive/TEST898_NRBC_20261119T090123Z/TEST898_NRBC_results.json',
                 'res_899': '/content/drive/MyDrive/TEST899_BP_20261119T160631Z/TEST899_BP_results.json',
                 'zip_897': '/content/drive/MyDrive/NPDM_SMOKE_20261118T223234Z/NPDM_SMOKE_SONUC_20261118T223234Z.zip',
                 'zip_898': '/content/drive/MyDrive/TEST898_NRBC_20261119T090123Z/TEST898_NRBC_SONUC_20261119T090123Z.zip'}
AUTH_REQUIRED = ('test', 'contract_md_sha256', 'contract_json_sha256', 'package_sums_sha256', 'pf_manifest_sha256',
                 'executor_900py_git_blob', 'independent_acceptance', 'gpu_execution_permission', 'granted_by', 'date')
IM_END = '<|im_end|>'
# Implementation parameters that the contract does not fix (post-operation guards, as in TEST899 ABORT; never adapted to data).
ABORT_900 = {'semantics': 'post-operation guards, not preemptive timeouts, no OOM guarantee', 'experiment_wall_s': 8 * 3600,
             'gpu_peak_gib': 74.0, 'cartridge_bytes_gib': 12.0, 'disk_free_min_gib': 12.0, 'cpu_ram_frac': 0.85, 'query_s': 180.0,
             'forge_append_s': 60.0, 'consolidation_s': 600.0}


def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_s(s): return sha_b(s.encode('utf-8'))
def blob_b(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'), default=list)
def jsha(v): return sha_s(canon(v))
def ids_sha(ids): return sha_s(json.dumps(list(ids)))          # = TEST896/899 forge_record 'ids_sha256'


# ===================================================================================================== configuration
def config(argv=None):
    """CLI flags override T900_* environment variables; defaults follow RUN_PREFLIGHT_COMMAND.sh and the archive locations.
    Unknown arguments (Colab kernel flags) are ignored. There is deliberately no flag that skips, forces or fakes a gate."""
    import argparse
    ap = argparse.ArgumentParser(add_help=False)
    d = {'package_dir': '/content/test900_v1_2_1/input_package',
         'pf_report': '/content/test900_pf_run_outputs/preflight900_report.json',
         'pf_manifest': '/content/test900_pf_run_outputs/preflight900_manifest.json',
         'authorization': '/content/TEST900_AUTHORIZATION.json', 'src_dir': '',
         'repo_dir': '/content/titan-cognitive-core-v3' if Path('/content').exists() else '',
         'out_root': '/content' if Path('/content').exists() else '/tmp', 'tokenizer_dir': '', 'tokenizer_digests': ''}
    d.update(DEFAULT_PATHS)
    for k, v in d.items(): ap.add_argument('--' + k.replace('_', '-'), default=os.environ.get('T900_' + k.upper(), v))
    a, _ = ap.parse_known_args(list(argv) if argv is not None else [])
    return {k: getattr(a, k) for k in d}


def load_by_path(name, path):
    """Execute a package tool from its exact bytes into a fresh module; no bytecode cache is written next to it."""
    m = types.ModuleType(name); m.__file__ = str(Path(path).resolve()); sys.modules[name] = m
    exec(compile(Path(path).read_bytes(), str(path), 'exec'), m.__dict__); return m


def inside(child, parent):
    try: Path(child).resolve().relative_to(Path(parent).resolve()); return True
    except ValueError: return False


# ===================================================================================================== GATE 0 (CPU)
def obtain_sources(cfg, workdir):
    """Exact bytes of 709/730/757/897/898/899 by git blob id: from --src-dir, or from a blob-less clone of SRC_REPO
    (`git cat-file blob <id>`; content addressed). Every file is re-verified by its git blob; a mismatch raises."""
    want = dict(ENGINE_BLOBS); want.update(TEST_SOURCES); out = {}
    rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') else Path(workdir).parent / 'TEST900_repo_blobs'
    for name, blob in want.items():
        if cfg.get('src_dir') and (Path(cfg['src_dir']) / name).is_file():
            b = (Path(cfg['src_dir']) / name).read_bytes()
        else:
            env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
            if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
                subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', 'https://github.com/' + SRC_REPO, str(rd)],
                               check=True, capture_output=True, timeout=900, env=env)
            b = subprocess.run(['git', '-C', str(rd), 'cat-file', 'blob', blob], check=True, capture_output=True, timeout=300, env=env).stdout
        if blob_b(b) != blob: raise RuntimeError('SOURCE_BLOB_MISMATCH %s %s != %s' % (name, blob_b(b), blob))
        out[name] = b; (Path(workdir) / name).write_bytes(b)
    return out


def gate0_package(cfg, workdir):
    """GATE 0: sealed package, CC-900 K0-K14 (K13 with --sums), pinned sources, results JSON bytes."""
    res = {'checks': {}, 'errors': []}; C = res['checks']; pkg = Path(cfg['package_dir'])
    md, js, sums = pkg / CONTRACT_MD, pkg / CONTRACT_JSON, pkg / 'SHA256SUMS.txt'
    for p in [md, js, sums] + [pkg / t for t in PACKAGE_TOOLS]:
        if not p.is_file(): res['errors'].append('MISSING_SOURCE ' + str(p))
    if res['errors']: return res, None, None
    C['contract_md_sha'] = sha_b(md.read_bytes()) == CONTRACT_MD_SHA
    C['contract_json_sha'] = sha_b(js.read_bytes()) == CONTRACT_JSON_SHA
    C['package_sums_sha'] = sha_b(sums.read_bytes()) == PACKAGE_SUMS_SHA
    try: J = json.loads(js.read_text(encoding='utf-8'))
    except Exception as e: res['errors'].append('CONTRACT_JSON_PARSE %s' % e); return res, None, None
    C['output_outside_package'] = not inside(workdir, pkg)
    try: SRC = obtain_sources(cfg, workdir)
    except Exception as e:
        res['errors'].append('MISSING_SOURCE sources %s: %s' % (type(e).__name__, str(e)[:300])); return res, J, None
    C['sources_blob_pinned'] = True
    for name, key in SOURCE_KEY.items():
        s = J['sources'][key]
        C['source_%s_matches_contract' % key] = blob_b(SRC[name]) == s['git_blob'] and (sha_b(SRC[name]) == s['sha256'] if 'sha256' in s else True)
    C['engine_blobs_match_contract'] = all(J['sources']['engine']['blobs'][n] == b for n, b in ENGINE_BLOBS.items())
    C['engine_commit_matches_contract'] = J['sources']['engine']['commit'] == ENGINE_COMMIT
    for k in ('897', '898', '899'):
        p = Path(cfg['res_' + k])
        if not p.is_file(): res['errors'].append('MISSING_SOURCE results_%s %s' % (k, p)); continue
        C['results_%s_sha' % k] = sha_b(p.read_bytes()) == J['sources']['results_sha256'][k]
    try:
        cc900 = load_by_path('t900_cc900', pkg / 'tools' / 'cc900.py')
        files = ['%s=%s' % (key, Path(workdir) / name) for name, key in SOURCE_KEY.items()]
        cc = cc900.run(str(md), str(js), str(sums), None, files); res['cc900'] = {k: v['status'] for k, v in cc.items()}
        C['cc900_all_PASS_including_K13'] = bool(cc) and all(v['status'] == 'PASS' for v in cc.values())
    except Exception as e:
        res['errors'].append('CC900_ERROR %s: %s' % (type(e).__name__, str(e)[:300]))
    return res, J, SRC


# ===================================================================================================== GATE 1 (CPU)
def gate1_pf(cfg, J):
    """GATE 1: the binding preflight report + manifest supplied by the user. This file never produces or edits them."""
    res = {'checks': {}, 'errors': []}; C = res['checks']; rp, mp = Path(cfg['pf_report']), Path(cfg['pf_manifest'])
    if not rp.is_file() or not mp.is_file():
        res['errors'].append('MISSING_SOURCE preflight report/manifest %s %s' % (rp, mp)); return res, None
    try: rep = json.loads(rp.read_text(encoding='utf-8')); man = json.loads(mp.read_text(encoding='utf-8'))
    except Exception as e: res['errors'].append('PF_UNREADABLE %s' % e); return res, None
    if not isinstance(rep, dict) or not isinstance(man, dict): res['errors'].append('PF_NOT_OBJECT'); return res, None
    ms = rep.get('manifest_sha256') or {}
    res['reported'] = {k: rep.get(k) for k in ('tool_version', 'overall', 'binding', 'backend', 'injected_env', 'fatal', 'missing')}
    C['tool_version_v1_2_1'] = rep.get('tool_version') == 'v1.2.1'
    C['overall_PASS'] = rep.get('overall') == 'PASS'
    C['binding_true'] = rep.get('binding') is True
    C['backend_hf'] = rep.get('backend') == 'hf'
    C['not_injected'] = rep.get('injected_env') is False
    C['fatal_empty'] = rep.get('fatal') == []
    C['missing_empty'] = rep.get('missing') == []
    C['three_sha_equal'] = bool(ms.get('pass1')) and ms.get('pass1') == ms.get('pass2') == ms.get('published_recomputed')
    C['manifest_file_sha_equals_report'] = sha_b(mp.read_bytes()) == ms.get('pass1')
    C['manifest_canonical'] = mp.read_text(encoding='utf-8') == canon(man)
    C['manifest_schema'] = sorted(man.keys()) == sorted(J['preflight_cpu']['manifest']['deterministic_fields'])
    cs = man.get('contract_sha256') or {}
    C['manifest_contract_md'] = cs.get('md') == CONTRACT_MD_SHA
    C['manifest_contract_json'] = cs.get('json') == CONTRACT_JSON_SHA
    C['manifest_package_sums'] = cs.get('sums') == PACKAGE_SUMS_SHA
    srcs = man.get('sources_sha256') or {}
    C['manifest_sources_pinned'] = all((srcs.get(k) or {}).get('git_blob_ok') is True and (srcs.get(k) or {}).get('sha256_ok') in (True, None)
                                       for k in SOURCE_KEY.values())
    arch = man.get('archives_sha256') or {}
    C['manifest_archives_pinned'] = all((arch.get('results_' + k) or {}).get('sha256_ok') is True for k in ('897', '898', '899'))
    tf = man.get('tokenizer_files') or {}
    C['tokenizer_bound_to_revision'] = (isinstance(tf, dict) and tf.get('revision') == J['pins']['model_revision'] and bool(tf.get('files'))
                                        and all((v or {}).get('match') is True for v in tf['files'].values())
                                        and sorted(tf['files']) == sorted(J['pins']['tokenizer_files']))
    C['tokenizer_backend_hf_fast'] = (man.get('tokenizer') or {}).get('backend_kind') == 'hf' and (man.get('tokenizer') or {}).get('is_fast') is True
    C['pins_equal'] = isinstance(man.get('pins_equal'), dict) and bool(man['pins_equal']) and all(v is True for v in man['pins_equal'].values())
    C['cc900_all_PASS'] = bool(man.get('cc900_status')) and all(v == 'PASS' for v in man['cc900_status'].values())
    w3 = man.get('w3') or {}; rf = (w3.get('controls') or {}).get('REL-FLIP', '')
    C['rel_flip_variant_recorded'] = isinstance(rf, str) and (rf.startswith('FULL OK:') or rf.startswith('REL_ONLY OK:'))
    C['w3_identity_match'] = w3.get('identity_vs_archive') == 'MATCH'
    C['w3_geometry_64_164'] = w3.get('F_mount_tokens_measured') == J['worlds']['W3']['F_mount_tokens'] and \
        w3.get('F_plus_REAL_measured') == J['worlds']['W3']['REAL']['mount_tokens_with_F']
    C['neutral900_equals_archived_899'] = w3.get('neutral900_equals_archived_899') == {'NEUTRAL1': 'PASS', 'NEUTRAL2': 'PASS'}
    C['names_and_L_m'] = isinstance(man.get('L_m'), int) and all(set((man.get('names') or {}).get(ns, {})) >= set(J['names']['order']) for ns in ('NS-A', 'NS-B'))
    st = man.get('stop_ids') or {}
    C['stop_ids_resolved'] = isinstance(st.get('canonical_stop_id'), int) and st.get('canonical_stop_id') in (st.get('stop_set') or [])
    res['manifest_sha256'] = ms.get('pass1'); res['rel_flip'] = rf
    res['control_not_constructible'] = rep.get('control_not_constructible')
    return res, man


# ===================================================================================================== GATE 2 (CPU)
def capture_self():
    """Bytes of the code being executed: the 900.py file (python 900.py / %run) or the IPython cell that contains it."""
    f = globals().get('__file__'); why = []
    try:
        if f and Path(f).is_file():
            b = Path(f).read_bytes()
            if MARKER.encode('utf-8') in b and b'def gate0_package' in b: return b, 'FILE:' + str(Path(f).resolve())
    except OSError as e: why.append('file: %s' % e)
    _gi = globals().get('get_ipython') or getattr(__import__('builtins'), 'get_ipython', None)
    if _gi is not None:
        try:
            cells = [x for x in list(_gi().history_manager.input_hist_raw) if MARKER in x and 'def gate0_package' in x]
            if cells: return cells[-1].encode('utf-8'), 'IPYTHON_HISTORY'
        except (AttributeError, TypeError) as e: why.append('ipython: %s' % e)
    return None, 'NOT_CAPTURED' + (' (%s)' % '; '.join(why) if why else '')


def executor_blobs(b):
    """Git blob ids the executed bytes may have as a published file (exact, or with only boundary newlines canonicalised)."""
    if b is None: return set()
    c = b.strip(b'\n'); return {blob_b(b), blob_b(c), blob_b(c + b'\n')}


def gate2_auth(cfg, pf_manifest_sha, self_bytes):
    """GATE 2: written independent acceptance and a separate GPU execution permission bound to this exact package and code."""
    res = {'checks': {}, 'errors': []}; C = res['checks']; p = Path(cfg['authorization'])
    if not p.is_file(): res['errors'].append('MISSING_SOURCE authorization record %s' % p); return res
    try: A = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: res['errors'].append('AUTH_UNREADABLE %s' % e); return res
    if not isinstance(A, dict): res['errors'].append('AUTH_NOT_OBJECT'); return res
    res['authorization_sha256'] = sha_b(p.read_bytes())
    C['fields_present'] = all(k in A for k in AUTH_REQUIRED)
    C['test_is_TEST900_v1_2_1'] = A.get('test') == 'TEST900 v1.2.1'
    C['bound_md'] = A.get('contract_md_sha256') == CONTRACT_MD_SHA
    C['bound_json'] = A.get('contract_json_sha256') == CONTRACT_JSON_SHA
    C['bound_sums'] = A.get('package_sums_sha256') == PACKAGE_SUMS_SHA
    C['bound_pf_manifest'] = bool(pf_manifest_sha) and A.get('pf_manifest_sha256') == pf_manifest_sha
    C['bound_executor_900py'] = isinstance(A.get('executor_900py_git_blob'), str) and A['executor_900py_git_blob'] in executor_blobs(self_bytes)
    ia = A.get('independent_acceptance') or {}
    C['independent_acceptance_recorded'] = isinstance(ia, dict) and ia.get('verdict') == 'ACCEPTED' and bool(ia.get('reviewer')) and bool(ia.get('record'))
    C['gpu_execution_permission_true'] = A.get('gpu_execution_permission') is True
    C['granted_by_present'] = isinstance(A.get('granted_by'), str) and bool(A['granted_by'].strip())
    res['executor_900py'] = {'captured': self_bytes is not None, 'candidate_blobs': sorted(executor_blobs(self_bytes))}
    return res


def run_cpu_gates(cfg, workdir):
    """GATE 0 -> GATE 1 -> GATE 2, each only after the previous one passed. Returns (ok, report, J, SRC, MAN). No torch."""
    rep = {'marker': MARKER, 'implementation_status': IMPLEMENTATION_STATUS, 'section16_deviation': SECTION16_DEVIATION,
           'time_utc': datetime.now(timezone.utc).isoformat(), 'gates': {}}
    g0, J, SRC = gate0_package(cfg, workdir); rep['gates']['GATE0_PACKAGE_SOURCES'] = g0
    ok0 = not g0['errors'] and bool(g0['checks']) and all(v is True for v in g0['checks'].values())
    MAN, g1 = None, {'checks': {}, 'errors': ['NOT_RUN: GATE0 not passed']}
    if ok0: g1, MAN = gate1_pf(cfg, J)
    rep['gates']['GATE1_BINDING_PREFLIGHT'] = g1
    ok1 = ok0 and not g1['errors'] and bool(g1['checks']) and all(v is True for v in g1['checks'].values())
    self_b, mode = capture_self(); rep['executor_capture'] = mode
    g2 = gate2_auth(cfg, g1.get('manifest_sha256'), self_b) if ok1 else {'checks': {}, 'errors': ['NOT_RUN: GATE1 not passed']}
    rep['gates']['GATE2_INDEPENDENT_ACCEPTANCE_AND_GPU_PERMISSION'] = g2
    ok2 = ok1 and not g2['errors'] and bool(g2['checks']) and all(v is True for v in g2['checks'].values())
    for g in rep['gates'].values():
        g['status'] = 'PASS' if (not g['errors'] and g['checks'] and all(v is True for v in g['checks'].values())) else 'LOCKED'
        g['failed'] = [k for k, v in g['checks'].items() if v is not True] + list(g['errors'])
    rep['gpu_gate'] = 'OPEN' if ok2 else 'LOCKED'
    rep['first_locked_gate'] = next((k for k, v in rep['gates'].items() if v['status'] != 'PASS'), None)
    return ok2, rep, J, SRC, MAN


# ===================================================================================================== executed source identity
def published_identity(cell_bytes, workdir, repo_url='https://github.com/' + SRC_REPO, src_file=SRC_FILE, raw_fetch=None, timeout=300):
    """TEST899 source_identity_block, adapted to SRC_FILE = 900.py: the executed bytes must equal the file that the default
    branch of the published repository serves right now (commit object, single regular-file tree entry, same blob in the
    default-branch tree, recomputed blob, raw channel equal, executed == published after stripping boundary b'\\n' only)."""
    ec = {'status': 'CAPTURED' if cell_bytes is not None else 'NOT_CAPTURED', 'src_file': src_file, 'checks': {}, 'mode': 'AUTOMATIC_FROM_PUBLISHED_DEFAULT_BRANCH'}
    ck = ec['checks']; ck['cell_captured'] = cell_bytes is not None
    if cell_bytes is not None: ec.update(sha256=sha_b(cell_bytes), git_blob=blob_b(cell_bytes), bytes=len(cell_bytes))
    gd = Path(workdir); env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    git = lambda *a: subprocess.run(['git', '--literal-pathspecs'] + list(a), check=True, capture_output=True, timeout=timeout, env=env).stdout
    pb = b''
    try:
        if gd.exists(): shutil.rmtree(gd)
        git('clone', '-q', '--filter=blob:none', '--no-checkout', repo_url, str(gd))
        head = git('-C', str(gd), 'rev-parse', '--verify', 'origin/HEAD^{commit}').decode().strip()
        commit = git('-C', str(gd), 'log', '-1', '--format=%H', head, '--', src_file).decode().strip()
        ck['commit_object_exists'] = bool(re.fullmatch(r'[0-9a-f]{40}', commit or '')) and git('-C', str(gd), 'cat-file', '-t', commit).decode().strip() == 'commit'
        lt = lambda c: [e for e in git('-C', str(gd), 'ls-tree', '-z', c, '--', src_file).decode('utf-8', 'replace').split('\0') if e]
        ent, enth = lt(commit), lt(head); ec['tree_entries'] = ent
        meta, _, pth = (ent[0].partition('\t') if len(ent) == 1 else ('', '', ''))
        mode, typ, oid = (meta.split(' ') + ['', '', ''])[:3]
        ck['tree_single_entry_exact_path'] = len(ent) == 1 and pth == src_file
        ck['tree_entry_regular_file'] = mode in ('100644', '100755') and typ == 'blob'
        ck['default_branch_publishes_same_blob'] = enth == ent
        pb = git('-C', str(gd), 'cat-file', 'blob', oid) if ck['tree_entry_regular_file'] else b''
        ck['recomputed_blob_equals_tree_blob'] = bool(pb) and blob_b(pb) == oid
        if raw_fetch is None:
            def raw_fetch(c, f):
                with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/%s/%s/%s' % (SRC_REPO, c, f),
                                                                   headers={'User-Agent': 'AKBASCORE-TEST900'}), timeout=120) as r_:
                    return r_.read()
        ck['raw_channel_equal'] = bool(pb) and raw_fetch(commit, src_file) == pb
        ec['published'] = {'repo': repo_url, 'default_branch_commit': head, 'commit': commit, 'path': src_file, 'tree_mode': mode,
                           'tree_blob': oid, 'blob_of_bytes': blob_b(pb), 'sha256': sha_b(pb), 'bytes': len(pb)}
        if cell_bytes is not None:
            cc, pc = cell_bytes.strip(b'\n'), pb.strip(b'\n')
            ck['executed_equals_published_bytes'] = bool(pb) and cc == pc
            if cc != pc:
                i = next((k for k in range(min(len(cc), len(pc))) if cc[k] != pc[k]), min(len(cc), len(pc)))
                ec['first_difference'] = {'offset': i, 'line': cc[:i].count(b'\n') + 1}
    except Exception as e:
        ec['published_error'] = '%s: %s' % (type(e).__name__, str(e)[:300]); ck['repository_checks_completed'] = False
    finally:
        shutil.rmtree(gd, ignore_errors=True)
    req = ('cell_captured', 'commit_object_exists', 'tree_single_entry_exact_path', 'tree_entry_regular_file',
           'default_branch_publishes_same_blob', 'recomputed_blob_equals_tree_blob', 'raw_channel_equal', 'executed_equals_published_bytes')
    ec['failed_checks'] = [k for k in req if ck.get(k) is not True] + [k for k, v in ck.items() if k not in req and v is not True]
    ec['identity_match'] = not ec['failed_checks']
    return ec


# ===================================================================================================== temporal isolation
EVAL_ONLY_KEYS = ('Q', 'OPT', 'vault', 'true_table', 'value_eligible', 'Q_source', 'expected_if_nat_card_correct')
EVAL_ONLY_SECTIONS = ('thresholds', 'measures', 'rules', 'verdict_precedence', 'q_audit', 'consistency_check', 'reference_rules_impl',
                      'source_verification', 'extensions')


def public_view(J):
    """The only contract object the experiment phase holds: Q, OPT, true tables, vault values, value eligibility, PERM
    expectations, thresholds and rules are removed; the full contract is re-read (SHA-checked) after GENERATION_SEALED."""
    P = json.loads(json.dumps(J))
    for k in EVAL_ONLY_SECTIONS: P.pop(k, None)
    def strip(x):
        if isinstance(x, dict):
            for k in list(x):
                if k in EVAL_ONLY_KEYS: x.pop(k)
                else: strip(x[k])
        elif isinstance(x, list):
            for v in x: strip(v)
    strip(P); return P


def leak_scan(obj, path=''):
    """Paths of evaluator-only keys still present in an object (must be [] for the public view)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in EVAL_ONLY_KEYS or k in EVAL_ONLY_SECTIONS: out.append(path + '/' + str(k))
            out += leak_scan(v, path + '/' + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj): out += leak_scan(v, '%s[%d]' % (path, i))
    return out


# ===================================================================================================== public protocol objects
ROLE_ACTS = ('a1', 'a2', 'a3'); ROLE_OUTS = ('o1', 'o2', 'o3')
CORE_A_ARMS = ('F', 'REAL', 'N1', 'N2', 'CANON-OBS', 'CANON-NAT', 'CANON-PERM', 'S1')
CARD_ARMS = ('CANON-OBS', 'CANON-NAT', 'CANON-PERM', 'S1')


def state_contract(JP, names, world, pos, cell):
    """Model-visible contract of one core-A/C state (positions = contract action order, rot = 0)."""
    c, L = cell.split('_'); W = JP['worlds']
    return {'actions': tuple(names[r] for r in W['positions'][pos]), 'outcomes': tuple(names[o] for o in W['positions']['outcome_order']),
            'goal': names[W[world]['goal']], 'cost': float(c), 'budget': int(L)}


def w3_contract(JP):
    I = JP['worlds']['W3']['identity']
    return {'actions': tuple(I['actions']), 'outcomes': tuple(I['outcomes']), 'goal': I['goal'], 'cost': float(I['cost']), 'budget': int(I['left'])}


def decision_key(parsed):
    """Decision class of a parsed greedy output: 'ACT a' / 'ACQUIRE a' / 'STOP' / 'WASTE' (INVALID, ABSTAIN)."""
    if parsed.get('status') == 'STOP': return 'STOP'
    if parsed.get('status') == 'VALID': return '%s %s' % (parsed['kind'], parsed['action'])
    return 'WASTE'


def event_kind(parsed):
    """Event type of a greedy decision: ACT / ACQUIRE / STOP / INVALID (ABSTAIN and malformed outputs are INVALID events)."""
    if parsed.get('status') == 'STOP': return 'STOP'
    if parsed.get('status') == 'VALID': return parsed['kind']
    return 'INVALID'


def class_of(text):
    p = text.split(); return 'STOP' if p[0] == 'STOP' else '%s %s' % (p[0], p[1])


def candidate_texts(acts, outs, grammar):
    """= preflight900.candidates (DIRECT 7, PRED 19), duplicated here so the pure layer is testable without the package."""
    c = []
    for k in ('ACT', 'ACQUIRE'):
        for a in acts:
            c += [('%s %s' % (k, a))] if grammar == 'DIRECT' else ['%s %s PREDICTION %s' % (k, a, o) for o in outs]
    return c + ['STOP']


def logsumexp(v):
    m = max(v); return m + math.log(sum(math.exp(x - m) for x in v))


def class_scores(items):
    """items: [(candidate text, s)]. DIRECT: one candidate per class; PRED: logsumexp over the 3 outcomes; STOP separate."""
    S = {}
    for text, s in items: S.setdefault(class_of(text), []).append(s)
    return {k: logsumexp(v) for k, v in S.items()}


def candidate_mass(items, tol, valid):
    """S = sum exp(s); R = 1 - S only if V1..V6 hold and S <= 1 + tol; never clipped."""
    S = sum(math.exp(s) for _, s in items)
    if not valid or S > 1 + tol: return {'S': S, 'R': None, 'flag': 'PROBABILITY_UNDEFINED'}
    return {'S': S, 'R': 1 - S, 'flag': 'NUMERIC_EDGE' if S > 1 else 'OK'}


def argmax_margin(scores):
    am = max(sorted(scores), key=lambda k: scores[k]); rest = [v for k, v in scores.items() if k != am]
    return am, (scores[am] - max(rest)) if rest else float('inf')


def acquire_mass_norm(scores):
    """Normalized ACQUIRE class mass over the candidate classes (delta_cost / delta_left)."""
    tot = sum(math.exp(v) for v in scores.values()); acq = sum(math.exp(v) for k, v in scores.items() if k.startswith('ACQUIRE '))
    return acq / tot if tot > 0 else None


def m_first_token(car):
    """m(X) = first_token_logp[ACT] - first_token_logp[ACQUIRE] (car_logp_898 at answer position 0); None without CAR."""
    if not car or not isinstance(car.get('first_token_logp'), dict): return None
    f = car['first_token_logp']; return (f['ACT'] - f['ACQUIRE']) if 'ACT' in f and 'ACQUIRE' in f else None


class ReadoutCounter:
    """Greedy decision readouts of the session; the matrix bound (109) is never exceeded and ids are unique."""
    def __init__(self, limit): self.limit = int(limit); self.n = 0; self.ids = []
    def take(self, rid):
        if rid in self.ids: raise RuntimeError('READOUT_ID_DUPLICATE ' + rid)
        if self.n + 1 > self.limit: raise RuntimeError('READOUT_LIMIT_EXCEEDED %d' % self.limit)
        self.n += 1; self.ids.append(rid); return self.n


def mount_sha(cart_shas, seal):
    """W3 mount_sha = sha256(canonical json [ordered cartridge sha list, full_kv_seal])."""
    return jsha([list(cart_shas), seal])


# ===================================================================================================== mount-text builders
# Every policy-mount text is produced by one of these functions. They run in a fresh namespace with an allow-list (structural
# isolation, contract mount_purity/isolation); the static check below proves that the source never names a forbidden input.
TRANSFORMS_SRC = r'''
def t_card_rows(card_row, rows):
    return '\n'.join(card_row.format(a=a, v=v).rstrip('\n') for a, v in rows)

def t_forge_card_v1(card_header, returned):
    return card_header + returned + '\n'

def t_record_text(segments):
    return ''.join(segments)

def t_obs_transcription(card_row, card_header, marker, actions, outcomes, records):
    seen = {}; intent = {}
    for r in records:
        if r['kind'] == 'PRIOR_OBSERVATION' and r['O'] in outcomes: seen[r['A']] = r['O']
        elif r['kind'] == 'MODEL_INTENT': intent[r['t']] = r['A']
        elif r['kind'] == 'OBSERVED_OUTCOME' and r['t'] in intent and r['O'] in outcomes: seen[intent[r['t']]] = r['O']
    returned = t_card_rows(card_row, [(a, seen.get(a, marker)) for a in actions])
    return returned, t_forge_card_v1(card_header, returned)

def t_perm(card_row, card_header, actions, role_of, pi, nat_values):
    name_of = {r: n for n, r in role_of.items()}
    vals = {a: nat_values[name_of[pi[role_of[a]]]] for a in actions}
    returned = t_card_rows(card_row, [(a, vals[a]) for a in actions])
    return vals, returned, t_forge_card_v1(card_header, returned)

def t_belief_898(belief_tpl, t, raw):
    return belief_tpl.format(t=t, B=raw.strip())

def t_u_tried(raw, untried, tried_a1):
    p = parse_belief_898(raw)
    if not p['valid']: return None
    line = 'UNKNOWN: ' + p['fields']['UNKNOWN']; ent = [x.strip() for x in p['fields']['UNKNOWN'].split(',')]
    idx = [i for i, x in enumerate(ent) if x in untried]
    if not idx or raw.count(line) != 1: return None
    new = list(ent); new[idx[0]] = tried_a1
    return raw.replace(line, 'UNKNOWN: ' + ', '.join(new), 1)

def t_u_perm(raw, A):
    u = 'UNKNOWN: %s, %s' % (A[0], A[1])
    return raw.replace(u, 'UNKNOWN: %s, %s' % (A[1], A[0])) if raw.count(u) == 1 else None

def t_rel_flip(raw, variant, fact_a, fact_o, filler):
    rl = 'REL: incorrect'
    if raw.count(rl) != 1: return None
    if variant == 'REL_ONLY': return raw.replace(rl, 'REL: correct')
    lp = [l for l in raw.split('\n') if l.startswith('LAST_PRED: ')]
    if len(lp) != 1 or not re.fullmatch('LAST_PRED: %s -> \\S+' % fact_a, lp[0]): return None
    return raw.replace(lp[0], 'LAST_PRED: %s -> %s%s' % (fact_a, fact_o, filler)).replace(rl, 'REL: correct')

def t_nl_plain(words, k):
    return ''.join(words[i % len(words)] for i in range(k)) + '\n'

def t_s1_card(s1_header, s1_row, actions, outcomes, probs):
    def p2(x): return '%02d' % min(99, int(math.floor(100 * x)))
    return s1_header + ''.join(s1_row.format(a=a, o1=outcomes[0], o2=outcomes[1], o3=outcomes[2], p1=p2(probs[a][0]),
                                             p2=p2(probs[a][1]), p3=p2(probs[a][2])) for a in actions)
'''
FORBIDDEN_BUILDER_NAMES = ('vault', 'OPT', 'Q', 'bayes', 'solver', 'evaluator', 'optimal', 'true_table', 'card_implied_action',
                           'bayes_npdm', 'J_EVAL', 'VAULT', 'mapping', 'implied_action', 'q_table', 'opt_set')
SAFE_BUILTINS = {k: __builtins__[k] if isinstance(__builtins__, dict) else getattr(__builtins__, k)
                 for k in ('len', 'range', 'enumerate', 'zip', 'dict', 'list', 'set', 'tuple', 'str', 'int', 'float', 'min', 'max',
                           'sorted', 'any', 'all', 'isinstance', 'sum', 'ValueError', 'Exception', 'repr', 'bool', 'print')}
BUILDER_EXTERNALS = ('re', 'math', 'json', 'parse_belief_898', 'enc899', 'geometry899', 'NoRun899', 'tok', 'PUB_TARGET', 'B_FIELDS_898', 'sha_bytes')


def names_in_code(code):
    out = set(code.co_names) | set(code.co_varnames) | set(code.co_freevars)
    for c in code.co_consts:
        if isinstance(c, types.CodeType): out |= names_in_code(c)
    return out


def static_builder_check(src):
    """Mount-text builders never reference a forbidden name (AST names, attributes, string-free)."""
    bad = set()
    for n in ast.walk(ast.parse(src)):
        nm = n.id if isinstance(n, ast.Name) else n.attr if isinstance(n, ast.Attribute) else n.arg if isinstance(n, ast.arg) else None
        if nm in FORBIDDEN_BUILDER_NAMES: bad.add(nm)
    return sorted(bad)


def make_builders(externals, neutral_src=None):
    """Fresh namespace with an allow-list; returns (ns, report). neutral_src: the TEST899 neutral899 source parameterised as
    neutral900 (anchor PUB['L1'][...] -> PUB_TARGET[...], identical to preflight900.build_namespace)."""
    bad = static_builder_check(TRANSFORMS_SRC) + (static_builder_check(neutral_src) if neutral_src else [])
    if bad: raise RuntimeError('MOUNT_BUILDER_FORBIDDEN_NAME %s' % bad)
    extra = set(externals) - set(BUILDER_EXTERNALS)
    if extra: raise RuntimeError('MOUNT_BUILDER_EXTERNAL_NOT_ALLOWED %s' % sorted(extra))
    ns = {'__builtins__': dict(SAFE_BUILTINS)}; ns.update(externals)
    exec(compile(TRANSFORMS_SRC, '900.py:TRANSFORMS_SRC', 'exec'), ns)
    if neutral_src: exec(compile(neutral_src, '899.py:neutral900_v1', 'exec'), ns)
    return ns, inspect_builders(ns)


def inspect_builders(ns):
    """Structural isolation check before every build: namespace keys are allow-listed; every builder function only names
    namespace keys, builtins, its own locals or attributes; no closure cells; defaults are literals."""
    allowed_keys = set(BUILDER_EXTERNALS) | {'__builtins__'}
    funcs = {k: v for k, v in ns.items() if isinstance(v, types.FunctionType) and v.__globals__ is ns}
    allowed_keys |= set(funcs)
    rep = {'namespace_keys_allowed': set(ns) <= allowed_keys, 'functions': sorted(funcs), 'violations': []}
    if not rep['namespace_keys_allowed']: rep['violations'].append('KEYS %s' % sorted(set(ns) - allowed_keys))
    for k, f in funcs.items():
        if f.__closure__: rep['violations'].append('CLOSURE ' + k)
        for d in (f.__defaults__ or ()):
            if not isinstance(d, (str, int, float, bool, type(None), tuple)): rep['violations'].append('DEFAULT ' + k)
        used = names_in_code(f.__code__)
        forb = used & set(FORBIDDEN_BUILDER_NAMES)
        if forb: rep['violations'].append('FORBIDDEN %s %s' % (k, sorted(forb)))
    rep['ok'] = not rep['violations']
    return rep


def neutral900_source(src899):
    """neutral899 from the pinned 899.py, re-parameterised exactly as preflight900.build_namespace does (transformation
    neutral900_v1): target-world public names instead of PUB['L1']."""
    seg = [ast.get_source_segment(src899, n) for n in ast.parse(src899).body if isinstance(n, ast.FunctionDef) and n.name == 'neutral899']
    anchor = "PUB['L1']['actions'] + PUB['L1']['outcomes']"
    if len(seg) != 1 or seg[0].count(anchor) != 1: raise RuntimeError('NEUTRAL899_PARAMETERISATION_ANCHOR_NOT_UNIQUE')
    return seg[0].replace('def neutral899(', 'def neutral900(', 1).replace(anchor, "PUB_TARGET['actions'] + PUB_TARGET['outcomes']")


# ===================================================================================================== lineage
LINEAGE_FIELDS = ('cid', 'kind', 'namespace', 'branch', 'provenance', 'template_id', 'transformation_id', 'source_shas', 'model_text_sha256',
                  'generation_query_sha256', 'generation_mount_sha', 'text_sha256', 'token_ids_sha256', 'forge', 'cartridge_sha256', 'seal', 'ns')
ALLOWED_PROVENANCE = ('ARCHIVE_RECORD', 'DIAGNOSTIC_GIVEN', 'LIVE_RECORD', 'MODEL_CONSOLIDATION', 'MODEL_LOGIT_FORMAT', 'CONTROL_TRANSFORM')


def provenance_ok(arm_prov, row_prov):
    """Every cartridge of an arm's policy mount carries an allowed provenance tag listed for that arm."""
    base = row_prov.split(':')[0]
    return base in ALLOWED_PROVENANCE and row_prov in arm_prov


def replay_text(row, TEXTS, B, NS, JP):
    """Byte-level replay: re-derive (text, ids) of one cartridge from its declared sources by its registered transformation."""
    T = JP['templates']; tid = row['transformation_id']; inp = row['replay']; tok_ids = NS['tok_ids']
    if tid in ('record_v1', 'archive_record_897'):
        rec = inp['record']; return B['t_record_text'](NS['segments_npdm'](rec)), NS['record_ids'](rec)
    if tid == 'forge_card_v1':
        text = B['t_forge_card_v1'](T['card_header'], TEXTS[inp['model_text_sha256']])
    elif tid == 'obs_transcription_v1':
        text = B['t_obs_transcription'](T['card_row'], T['card_header'], T['no_entry_marker'], inp['actions'], inp['outcomes'], inp['records'])[1]
    elif tid == 'perm_pi_v1':
        pc = NS['parse_card'](TEXTS[inp['nat_model_text_sha256']], inp['actions'], inp['outcomes'])
        if not pc['valid']: raise RuntimeError('LINEAGE_PERM_SOURCE_INVALID')
        text = B['t_perm'](T['card_row'], T['card_header'], inp['actions'], inp['role_of'], JP['perm']['pi'], pc['values'])[2]
    elif tid in ('belief_898_v1', 'archive_belief_898'):
        text = B['t_belief_898'](NS['BELIEF_TPL_898'], inp['t'], TEXTS[inp['raw_sha256']])
    elif tid == 's1_format_v1':
        text = B['t_s1_card'](T['s1_header'], T['s1_row'], inp['actions'], inp['outcomes'], inp['probs'])
    elif tid == 'neutral900_v1':
        src_raw = TEXTS[inp['source_raw_sha256']]; src_text = B['t_belief_898'](NS['BELIEF_TPL_898'], inp['t'], src_raw)
        B['PUB_TARGET'] = {'actions': list(inp['pub_target']['actions']), 'outcomes': list(inp['pub_target']['outcomes'])}
        text = B['neutral900'](src_text, src_raw, NS['geometry899'](src_text, src_raw), tuple(NS['NEUTRAL_WORDS_899'][inp['words']]))[0]
    elif tid in ('u_tried_v1', 'u_perm_v1', 'rel_flip_v1'):
        src_raw = TEXTS[inp['source_raw_sha256']]
        raw2 = (B['t_u_tried'](src_raw, inp['untried'], inp['tried_a1']) if tid == 'u_tried_v1' else
                B['t_u_perm'](src_raw, inp['A']) if tid == 'u_perm_v1' else
                B['t_rel_flip'](src_raw, inp['variant'], inp['fact_a'], inp['fact_o'], inp['filler']))
        if raw2 is None: raise RuntimeError('LINEAGE_CONTROL_NOT_RECONSTRUCTIBLE ' + tid)
        text = B['t_belief_898'](NS['BELIEF_TPL_898'], inp['t'], raw2)
    elif tid == 'nl_plain_v1':
        text = B['t_nl_plain'](tuple(NS['NEUTRAL_WORDS_899'][inp['words']]), inp['k'])
    else:
        raise RuntimeError('LINEAGE_UNKNOWN_TRANSFORMATION ' + tid)
    return text, tok_ids(text)


def lineage_replay(rows, TEXTS, B, NS, JP):
    """Offline decisive check: every mounted text and its token ids are reproduced from the declared sources alone."""
    out = {'rows': len(rows), 'mismatch': [], 'errors': []}
    for r in rows:
        try:
            text, ids = replay_text(r, TEXTS, B, NS, JP)
            if sha_s(text) != r['text_sha256'] or ids_sha(ids) != r['token_ids_sha256']:
                out['mismatch'].append({'cid': r['cid'], 'text_equal': sha_s(text) == r['text_sha256'], 'ids_equal': ids_sha(ids) == r['token_ids_sha256']})
        except Exception as e:
            out['errors'].append({'cid': r.get('cid'), 'error': '%s: %s' % (type(e).__name__, str(e)[:200])})
    out['status'] = 'PASS' if not out['mismatch'] and not out['errors'] and rows else 'LINEAGE_BLOCKER'
    return out


# ===================================================================================================== invariants I1-I11
W3_EPISTEMIC_KINDS = ('MODEL_INTENT', 'MODEL_PREDICTION', 'OBSERVED_OUTCOME', 'OUTCOME_STATUS', 'MODEL_STOP', 'MODEL_INVALID')


def check_invariants(events, sealed_ns=None, evaluator_ns=None):
    """Pure check over the invariant ledger. Event kinds: CARTRIDGE{sha256,ns,branch,t,kind,arm_mount_kinds?}, DECIDE{branch,k,
    mount_shas,card_parent_turns,ns}, WRITE_INTENT{branch,k,ns}, VAULT_ACCESS{branch,k,ns}, ENV{branch,k,ns,env_id},
    CARD_FOR_NEXT{branch,k,ns,parent_turns}, CONSOL_QUERY{branch,k,equal_tpl}, MOUNT{branch,k,kinds,arm}, MEASURE_TEXT_USE."""
    errs = []; cart_ns = {}
    for e in events:
        if e['kind'] == 'CARTRIDGE': cart_ns.setdefault(e['sha256'], e['ns'])
    wi = {(e['branch'], e['k']): e['ns'] for e in events if e['kind'] == 'WRITE_INTENT'}
    envn = {(e['branch'], e['k']): e['ns'] for e in events if e['kind'] == 'ENV'}
    env_ids = {}
    for e in events:
        if e['kind'] == 'DECIDE':
            for s in e['mount_shas']:
                if s not in cart_ns or cart_ns[s] >= e['ns']: errs.append('I1 %s k%s' % (e['branch'], e['k']))
            if any(t > e['k'] - 1 for t in e.get('card_parent_turns', [])): errs.append('I2 %s k%s' % (e['branch'], e['k']))
        elif e['kind'] == 'VAULT_ACCESS':
            if (e['branch'], e['k']) not in wi or wi[(e['branch'], e['k'])] >= e['ns']: errs.append('I3 %s k%s' % (e['branch'], e['k']))
        elif e['kind'] == 'ENV':
            if (e['branch'], e['k']) not in wi or wi[(e['branch'], e['k'])] >= e['ns']: errs.append('I3/ENV %s k%s' % (e['branch'], e['k']))
            env_ids.setdefault(e['env_id'], set()).add(e['branch'])
        elif e['kind'] == 'CARD_FOR_NEXT':
            if (e['branch'], e['k']) in envn and envn[(e['branch'], e['k'])] >= e['ns']: errs.append('I9 %s k%s' % (e['branch'], e['k']))
            if e.get('requires_env') and (e['branch'], e['k']) not in envn: errs.append('I9/noenv %s k%s' % (e['branch'], e['k']))
            if any(t > e['k'] for t in e.get('parent_turns', [])): errs.append('I9/parents %s k%s' % (e['branch'], e['k']))
        elif e['kind'] == 'READ_RECORDS':
            if set(e['source_branches']) - {e['branch'], 'W3_ARCHIVE'}: errs.append('I5 %s' % e['branch'])
        elif e['kind'] == 'CONSOL_QUERY':
            if e.get('arm') == 'CANON-NAT' and e.get('equal_tpl') is not True: errs.append('I6 %s k%s' % (e['branch'], e['k']))
        elif e['kind'] == 'MOUNT':
            if e.get('arm') == 'F' and 'MODEL_PREDICTION' in e.get('kinds', []): errs.append('I10/F %s k%s' % (e['branch'], e['k']))
            if e.get('w3') and any(k not in W3_EPISTEMIC_KINDS and k not in ('CARD', 'BELIEF') for k in e.get('kinds', [])): errs.append('I10/kinds %s' % e['branch'])
        elif e['kind'] == 'MEASURE_TEXT_USE':
            errs.append('I7 %s' % e.get('what'))
        elif e['kind'] == 'APPEND_ONLY_VIOLATION':
            errs.append('I8 %s' % e.get('path'))
    if any(len(b) > 1 for b in env_ids.values()): errs.append('I11 shared environment')
    if evaluator_ns is not None and (sealed_ns is None or evaluator_ns <= sealed_ns): errs.append('I4 evaluator before GENERATION_SEALED')
    return errs


def continuation_transition(ev_kind, left):
    """W3 continuation state machine (897 semantics, pend_left = 0): (records, env_call, terminal, budget_exhausted)."""
    if ev_kind == 'STOP': return ['MODEL_STOP'], False, True, False
    if ev_kind == 'INVALID': return ['MODEL_INVALID', 'OUTCOME_STATUS'], False, False, left - 1 <= 0
    if ev_kind == 'ACT': return ['MODEL_INTENT', 'MODEL_PREDICTION', 'OBSERVED_OUTCOME'], True, True, False
    if ev_kind == 'ACQUIRE': return ['MODEL_INTENT', 'MODEL_PREDICTION', 'OBSERVED_OUTCOME'], True, False, left - 1 <= 0
    raise ValueError(ev_kind)


def vault_mapping_w3(vault, actions, facts):
    """TEST897 vault schema: json.dumps(VAULT) with VAULT[eid] = {'mapping','goal2','rel','pending_steps'}; the W3 mapping
    is VAULT['L3']['mapping']. It must be a bijection onto the public outcomes, consistent with the public fact, and
    pending_steps must be 0 (pend_left = 0). Called only inside the branch environment at ENV(k)."""
    v = (vault or {}).get('L3') or {}; mp = v.get('mapping')
    if not isinstance(mp, dict) or set(mp) != set(actions): raise RuntimeError('VAULT_SCHEMA_W3_MAPPING')
    if len(set(mp.values())) != len(actions) or any(mp[a] != o for a, o in facts): raise RuntimeError('VAULT_W3_MAPPING_INCONSISTENT')
    if int(v.get('pending_steps', 0)) != 0: raise RuntimeError('VAULT_W3_PENDING_NOT_ZERO')
    return dict(mp)


# ===================================================================================================== offline evaluation (after GENERATION_SEALED only)
def q_named(Qc, names):
    out = {}
    for k, v in Qc.items():
        p = k.split(); out[k if len(p) == 1 else '%s %s' % (p[0], names.get(p[1], p[1]))] = v
    return out


def opt_named(O, names):
    return sorted('%s %s' % (k.split()[0], names.get(k.split()[1], k.split()[1])) if len(k.split()) == 2 else k for k in O)


def implied_action(values, goal):
    """card_implied_action (offline only): the action of the single goal cell; zero or several -> None (NOT_EVALUABLE)."""
    g = [a for a, v in values.items() if v == goal]
    return g[0] if len(g) == 1 else None


def determination_table(actions, outcomes, facts):
    """Cells determined by the facts and the bijection rule (offline E1 reference); None = not determined."""
    maps = [dict(zip(actions, p)) for p in _it.permutations(outcomes)]; maps = [m for m in maps if all(m[a] == o for a, o in facts)]
    return {a: (maps[0][a] if maps and len({m[a] for m in maps}) == 1 else None) for a in actions}


def card_correct(card, det, marker):
    """VALID and cell-exact against the true determination table (determined cells = outcome, others = marker)."""
    return bool(card and card.get('valid')) and all(card['values'].get(a) == (det[a] if det[a] is not None else marker) for a in det)


def enrich(r, OPT, Q, tau, tol):
    """Offline measures of one RUN readout: GO (greedy only), CC (candidates only), GCA, JOINT, V_Q."""
    pv = r['parsed'].get('status') in ('VALID', 'STOP'); key = r['decision_key']
    c = r.get('cand') or {}; scores = c.get('class_scores') or {}
    pu = bool(c.get('prob_undefined', True))
    am, mg = argmax_margin(scores) if scores else (None, None)
    e = {'GO': pv and key in OPT, 'CC': (not pu) and am in OPT and mg is not None and mg > tau, 'GCA': pv and key == am,
         'argmax': am, 'margin': mg, 'prob_undefined': pu, 'V': Q.get(key, Q['WASTE']), 'valid': pv}
    e['JOINT'] = e['GO'] and e['CC'] and e['GCA']
    return e


def rule_real_n(A, T):
    """REAL-N: REAL vs N1, N2 over the 8 core-A readouts."""
    rows = {}; und = 0
    for rid, x in A.items():
        R_, N1, N2 = x.get('REAL'), x.get('N1'), x.get('N2')
        if not (R_ and N1 and N2): rows[rid] = 'UNDECIDABLE_NOT_CONSTRUCTIBLE'; und += 1; continue
        if N1['decision_key'] != N2['decision_key']: rows[rid] = 'UNDECIDABLE_N1_N2_DISAGREE'; und += 1; continue
        nat = R_['decision_key'] != N1['decision_key']
        cand = None if (R_['ev']['argmax'] is None or N1['ev']['argmax'] is None) else R_['ev']['argmax'] != N1['ev']['argmax']
        rows[rid] = {'native_content_effect': nat, 'candidate_content_effect': cand}
    st = 'REAL_N_UNDECIDABLE' if und > T['N_disagree_max'] else 'DECIDABLE'
    return {'status': st, 'undecidable_rows': und, 'rows': rows,
            'native_effect_rows': sum(1 for v in rows.values() if isinstance(v, dict) and v['native_content_effect']),
            'candidate_effect_rows': sum(1 for v in rows.values() if isinstance(v, dict) and v['candidate_content_effect'])}


def rule_h1_w3(B, T, I):
    first, other = I['actions'][0], I['actions'][1]
    R_, U = [B.get(('REAL', g)) for g in ('PRED', 'DIRECT')], [B.get(('U-PERM', g)) for g in ('PRED', 'DIRECT')]
    if not all(R_) or not all(U): return {'verdict': 'UNDECIDABLE', 'why': 'NOT_CONSTRUCTIBLE_OR_MISSING'}
    tau = T['tau_nat']; sc = lambda r, a: (r.get('cand') or {}).get('class_scores', {}).get('ACQUIRE ' + a)
    def gap(r, a, b):
        x, y = sc(r, a), sc(r, b); return None if x is None or y is None or (r.get('cand') or {}).get('prob_undefined') else x - y
    nat = all(r['decision_key'] == 'ACQUIRE ' + first for r in R_) and all(u['decision_key'] == 'ACQUIRE ' + other for u in U)
    cand = all((gap(r, first, other) or -1e9) > tau for r in R_) and all((gap(u, other, first) or -1e9) > tau for u in U)
    ref_nat = all(u['decision_key'] == 'ACQUIRE ' + first for u in U); ref_cand = all((gap(u, first, other) or -1e9) > tau for u in U)
    v = 'SUPPORTED' if nat and cand else ('REFUTED' if ref_nat and ref_cand else 'UNDECIDABLE')
    return {'verdict': v, 'native': nat, 'candidate': cand, 'gaps_REAL': [gap(r, first, other) for r in R_], 'gaps_UPERM': [gap(u, other, first) for u in U]}


def rule_h1_w2(A, T, nameA):
    a1 = nameA['a1']; n_nat = n_cand = n_ref = n_ref_c = 0; rows = 0
    for rid, x in A.items():
        if not rid.startswith('A/W2/'): continue
        U, F = x.get('U-TRIED'), x.get('F')
        if not U or not F: return {'verdict': 'UNDECIDABLE', 'why': 'NOT_CONSTRUCTIBLE_OR_MISSING'}
        rows += 1
        n_nat += U['decision_key'] == 'ACQUIRE ' + a1 and F['decision_key'] != 'ACQUIRE ' + a1
        n_cand += U['ev']['argmax'] == 'ACQUIRE ' + a1 and F['ev']['argmax'] != 'ACQUIRE ' + a1
        n_ref += U['decision_key'] == F['decision_key']; n_ref_c += U['ev']['argmax'] == F['ev']['argmax']
    m = T['H1W2_min']
    v = 'SUPPORTED' if n_nat >= m and n_cand >= m else ('REFUTED' if n_ref >= m and n_ref_c >= m else 'UNDECIDABLE')
    return {'verdict': v, 'rows': rows, 'native_pattern': n_nat, 'candidate_pattern': n_cand, 'same_as_F': n_ref, 'same_as_F_candidate': n_ref_c}


def rule_h1(h1w3, h1w2):
    a, b = h1w3['verdict'], h1w2['verdict']
    return 'SUPPORTED' if a == b == 'SUPPORTED' else ('REFUTED' if a == b == 'REFUTED' else 'MIXED')


def rule_h2(B, T, variant):
    tau = T['tau_nat']; dms, changed = [], []
    for g in ('PRED', 'DIRECT'):
        R_, X = B.get(('REAL', g)), B.get(('REL-FLIP', g))
        if not R_ or not X: return {'verdict': 'UNDECIDABLE', 'why': 'NOT_CONSTRUCTIBLE_OR_MISSING', 'variant': variant}
        mr, mx = m_first_token(R_.get('car')), m_first_token(X.get('car'))
        if mr is None or mx is None: return {'verdict': 'UNDECIDABLE', 'why': 'CAR_MISSING', 'variant': variant}
        dms.append(mx - mr); changed.append(R_['decision_key'] != X['decision_key'])
    v = 'SUPPORTED' if all(d > tau for d in dms) else ('REFUTED' if all(abs(d) < tau for d in dms) and not any(changed) else 'UNDECIDABLE')
    return {'verdict': v, 'dm': dms, 'greedy_decision_changed': changed, 'variant': variant,
            'limit': 'REL_ONLY: the wrong prediction stays implicit in LAST_PRED; H2 then measures the explicit error label only' if variant == 'REL_ONLY' else None}


def rule_h2p_sal(B, T, I):
    fact_a = I['facts'][0][0]; F_ = [B.get(('F', g)) for g in ('PRED', 'DIRECT')]; O = [B.get(('CANON-OBS', g)) for g in ('PRED', 'DIRECT')]
    if not all(F_) or not all(O): return {'verdict': 'MIXED', 'why': 'MISSING'}
    nat = all(f['decision_key'] == 'ACQUIRE ' + fact_a for f in F_) and all(o['ev']['GO'] for o in O)
    cand = all(o['ev']['CC'] for o in O)
    v = 'SUPPORTED' if nat and cand else ('REFUTED' if all(o['decision_key'] == 'ACQUIRE ' + fact_a for o in O) else 'MIXED')
    return {'verdict': v, 'native': nat, 'candidate': cand}


def rule_h2p_look(A, T):
    go = {'W1': 0, 'W2': 0}; cc = {'W1': 0, 'W2': 0}
    for rid, x in A.items():
        f = x.get('F')
        if f: w = rid.split('/')[1]; go[w] += f['ev']['GO']; cc[w] += f['ev']['CC']
    nat = go['W2'] >= T['LOOK_W2_GO_min'] and go['W1'] <= T['LOOK_W1_GO_max']; cand = cc['W2'] >= T['LOOK_W2_GO_min'] and cc['W1'] <= T['LOOK_W1_GO_max']
    v = 'SUPPORTED' if nat and cand else ('REFUTED' if go['W1'] >= 3 else 'MIXED')
    return {'verdict': v, 'F_GO': go, 'F_CC': cc}


def rule_h2p_pred(Fs):
    """Fs: {state: {'PRED': row, 'DIRECT': row, 'determined': set(actions)}} for W1/P-last, W1/P-first, W3."""
    def u(r, det): return r['decision_key'].startswith('ACQUIRE ') and r['decision_key'].split()[1] in det
    sup = sum(1 for s in Fs.values() if s.get('PRED') and s.get('DIRECT') and u(s['PRED'], s['determined']) and not u(s['DIRECT'], s['determined']))
    ref = sum(1 for s in Fs.values() if s.get('PRED') and s.get('DIRECT') and u(s['PRED'], s['determined']) and u(s['DIRECT'], s['determined']))
    return {'verdict': 'SUPPORTED' if sup >= 2 else ('REFUTED' if ref >= 2 else 'MIXED'), 'states_pred_only_uacq': sup, 'states_both_uacq': ref}


def rule_sensitivity(acq_side, other_side, minuend, subtrahend, T, sign):
    """H2p-COST / H2p-LEFT on the F arm, 2 grammars. Native: greedy kind ACQUIRE on acq_side but not on other_side in 2/2 ->
    sensitive; same ACQUIRE-ness in 2/2 -> insensitive. Candidate: delta = log normalized ACQUIRE class mass(minuend) - (subtrahend);
    sensitive iff sign*delta > tau in 2/2, insensitive iff |delta| < tau in 2/2. Verdict only when both sides agree.
    COST: acq_side c=0.1, other c=0.8, delta = m(0.8) - m(0.1), sign -1.  LEFT: acq_side left=3, other left=1, delta = m(3) - m(1), sign +1."""
    tau = T['tau_nat']; nat_s, nat_i, ds = [], [], []
    for g in ('PRED', 'DIRECT'):
        a, b, mi, su = acq_side.get(g), other_side.get(g), minuend.get(g), subtrahend.get(g)
        if not (a and b and mi and su): return {'verdict': 'MIXED', 'why': 'MISSING'}
        ka, kb = a['decision_key'].startswith('ACQUIRE '), b['decision_key'].startswith('ACQUIRE ')
        nat_s.append(ka and not kb); nat_i.append(ka == kb)
        mm, ms = acquire_mass_norm((mi.get('cand') or {}).get('class_scores') or {}), acquire_mass_norm((su.get('cand') or {}).get('class_scores') or {})
        undefined = (mi.get('cand') or {}).get('prob_undefined', True) or (su.get('cand') or {}).get('prob_undefined', True)
        ds.append(None if (undefined or not mm or not ms) else math.log(mm) - math.log(ms))
    if any(d is None for d in ds): return {'verdict': 'MIXED', 'why': 'PROBABILITY_UNDEFINED_OR_ZERO_MASS', 'delta': ds}
    cs = all(sign * d > tau for d in ds); ci = all(abs(d) < tau for d in ds)
    v = 'SENSITIVE' if all(nat_s) and cs else ('INSENSITIVE' if all(nat_i) and ci else 'MIXED')
    return {'verdict': v, 'delta': ds, 'native_sensitive': nat_s, 'native_insensitive': nat_i}


def rule_h3(B, T):
    tau, sup = T['tau_nat'], T['H3_support_abs_dm']; dm = {}
    for g in ('PRED', 'DIRECT'):
        f = B.get(('F', g)); mf = m_first_token(f.get('car')) if f else None
        for X in ('NL50', 'NL100p', 'N1', 'N2'):
            x = B.get((X, g)); mx = m_first_token(x.get('car')) if x else None
            dm[(X, g)] = None if (mf is None or mx is None) else mx - mf
        dm[('m_F', g)] = mf
    if any(dm[(X, g)] is None for X in ('NL50', 'NL100p') for g in ('PRED', 'DIRECT')):
        return {'verdict': 'UNDECIDABLE', 'why': 'NL_NOT_CONSTRUCTIBLE_OR_CAR_MISSING', 'dm': {'%s/%s' % k: v for k, v in dm.items()}}
    s = all(abs(dm[('NL100p', g)]) >= sup and abs(dm[('NL50', g)]) <= abs(dm[('NL100p', g)]) for g in ('PRED', 'DIRECT'))
    vals = [v for (X, g), v in dm.items() if X != 'm_F' and v is not None]
    v = 'SUPPORTED' if s else ('REFUTED' if vals and all(abs(x) < tau for x in vals) else 'UNDECIDABLE')
    sgn = lambda x: (x > 0) - (x < 0)
    dirn = {g: {'H3a': dm[('m_F', g)] is not None and sgn(dm[('NL100p', g)]) == -sgn(dm[('m_F', g)]), 'H3b': dm[('NL100p', g)] < 0} for g in ('PRED', 'DIRECT')}
    fname = {g: (dm[('N1', g)] - dm[('NL100p', g)]) if dm[('N1', g)] is not None else None for g in ('PRED', 'DIRECT')}
    return {'verdict': v, 'dm': {'%s/%s' % k: v_ for k, v_ in dm.items()}, 'direction': dirn, 'field_name_effect': fname}


def rule_w3_arch(B):
    out = {}
    for arm in ('CANON-OBS', 'CANON-NAT'):
        rr = [B.get((arm, g)) for g in ('PRED', 'DIRECT')]
        out[arm] = 'PERSEVERATION_REMOVED_W3' if all(rr) and all(r['ev']['GO'] and r['ev']['CC'] for r in rr) else 'NOT_SHOWN'
    return out


def build_core_rows(A, arm, cards_nat, cards_perm, goal_of, opt_of, vq_eligible):
    """rules900 row format for arm X (and the NAT->PERM E3 fields when arm == CANON-NAT)."""
    rows = []
    for rid, x in A.items():
        r = x.get(arm)
        if r is None: return None
        w = rid.split('/')[1]; st = '/'.join(rid.split('/')[:3])
        row = {'id': rid, 'world': w, 'grammar': rid.split('/')[3], 'state': st, 'GO': r['ev']['GO'], 'CC': r['ev']['CC'], 'GCA': r['ev']['GCA'],
               'prob_undefined': r['ev']['prob_undefined'], 'V': r['ev']['V'], 'greedy': r['decision_key']}
        if arm == 'CANON-NAT':
            p = x.get('CANON-PERM'); nat = cards_nat.get(st) or {}; perm = cards_perm.get(st)
            sens = bool(nat.get('valid')) and perm is not None and p is not None
            ni = implied_action(nat['values'], goal_of[st]) if nat.get('valid') else None
            pi_ = implied_action(perm['values'], goal_of[st]) if perm else None
            dirv = sens and ni is not None and pi_ is not None and pi_ != ni
            row.update(greedy_perm=p['decision_key'] if p else None, V_perm=p['ev']['V'] if p else None,
                       perm_evaluable={'sens': sens, 'dir': dirv, 'ben': sens and vq_eligible}, perm_implied=pi_, nat_implied=ni,
                       nat_correct_act=bool(ni) and r['decision_key'] == 'ACT ' + ni and r['decision_key'] in opt_of[st])
        rows.append(row)
    return rows


def top_verdict(RULES, rows_nat, rows_f, cardc, T, technical_ok, obs_w1_go, arm_rows):
    """TOP (verdict_precedence) via tools/rules900.evaluate + the N-DED label and the arm labels of the contract."""
    ev = RULES.evaluate(rows_nat, rows_f, cardc, T, technical_ok=technical_ok)
    head = ev['headline']
    ded = 'DEDUCTION_MATERIALIZATION' if obs_w1_go <= T['OBS_label_W1_GO_max'] else 'FORMAT_SUFFICIENT'
    if head == 'S2D_PROVISIONAL_PASS': head = 'S2D_PROVISIONAL_PASS[%s]' % ded
    labels = {}
    for arm, rows in arm_rows.items():
        pref = 'CANDIDATE_ARM_' if arm in ('REAL', 'S1') else 'CONTROL_ARM_'
        labels[arm] = pref + ('NOT_CONSTRUCTIBLE' if rows is None else RULES.e2(rows, rows_f, T)['label'])
    native_any = ev['E2']['E2N'] == 'PASS' or any(v.endswith(('E2_JOINT_PASS', 'E2_NATIVE_PASS_JOINT_FRAGILE')) for v in labels.values())
    conv = ev['gates']['E1'] == 'PASS' and ev['gates']['E2J'] == 'PASS' and ev['gates']['CONVERTED_PASS'] and ev['gates']['E3'] == 'PASS'
    return {'headline': head, 'evaluate': ev, 'N_DED': ded, 'arm_labels': labels, 'NO_ARCHITECTURE_GAIN': not native_any,
            'KNOWLEDGE_TO_ACTION_CONVERSION': conv and technical_ok, 'X_R_mandatory': head.startswith('S2D_PROVISIONAL_PASS'),
            'gate_vector': {k: ev['gates'][k] for k in ('E1', 'E2N', 'E2J', 'CONVERTED_PASS', 'E3S', 'E3D', 'E3B')}}


# ===================================================================================================== runtime state and ledger
RUN_ID = None; ROOT = None; LOG = None; OUT = None; EVENTS = None; LINEAGE_FILE = None; CART_DIR = None; R = None
EVSEQ = [0]; SAVE_T = [0.0]; T0 = time.perf_counter(); DRIVE_DIR = None; DRIVE_ERR = {'mount': None, 'backup_failures': 0, 'last': None}
X = types.SimpleNamespace()                           # experiment state (filled by gpu_main)


class StopT896(Exception):
    """Technical stop (name kept: the verbatim TEST896-899 cartridge / guard functions raise it). Never a scientific result."""


CRITICAL_900 = ('GATE3_EXECUTED_SOURCE_IDENTITY', 'GATE3_RUNTIME_PINS', 'GATE3_ENV', 'GATE3_SOURCE_EXTRACT', 'GATE3_PF_REPEAT',
                'GATE3_ARCHIVE_897', 'GATE3_ARCHIVE_898', 'MODEL', 'GATE3_ENGINE', 'GATE4_GEO_RT', 'GATE4_W3_GEOMETRY')


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, LINEAGE_FILE, CART_DIR, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    ROOT = Path(cfg['out_root']) / ('TEST900_' + RUN_ID)
    if inside(ROOT, cfg['package_dir']): raise SystemExit('TEST900: output directory must be outside the sealed input_package')
    ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST900.log'; OUT = ROOT / 'TEST900_results.json'; EVENTS = ROOT / 'TEST900_events.jsonl'
    LINEAGE_FILE = ROOT / 'TEST900_lineage.jsonl'; CART_DIR = ROOT / 'cartridges'
    for f in (LOG, EVENTS, LINEAGE_FILE): f.write_text('')
    EVSEQ[0] = 0
    R = {'test': TAG, 'marker': MARKER, 'protocol': 'TEST900 v1.2.1', 'run_id': RUN_ID, 'status': 'STARTED',
         'implementation_status': IMPLEMENTATION_STATUS, 'section16_deviation': SECTION16_DEVIATION, 'executed_by_author': False,
         'chain': {'TEST897': {'blob': TEST_SOURCES['897npdm_smoke.py'], 'verdict': 'NPDM_FAIL'},
                   'TEST898': {'blob': TEST_SOURCES['898.py'], 'verdict': 'NRBC_SCREEN_FAIL'},
                   'TEST899': {'blob': TEST_SOURCES['899.py'], 'verdict': 'MECHANISM_GRAMMAR_AND_CONTENT_ACTION_SENSITIVITY'}},
         'contract': {'md_sha256': CONTRACT_MD_SHA, 'json_sha256': CONTRACT_JSON_SHA, 'package_sums_sha256': PACKAGE_SUMS_SHA},
         'engine': {'commit': ENGINE_COMMIT, 'blobs': ENGINE_BLOBS}, 'abort_limits': ABORT_900,
         'gates': {}, 'checks': [], 'technical_blockers': [], 'config': {k: v for k, v in cfg.items()}}
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
            for f_ in (LOG, OUT, EVENTS, LINEAGE_FILE): shutil.copy2(f_, Path(DRIVE_DIR) / f_.name)
        except Exception as e:
            DRIVE_ERR['backup_failures'] += 1; DRIVE_ERR['last'] = '%s: %s' % (type(e).__name__, e)


def _append_line(path, line):
    with open(path, 'a') as f: f.write(line + '\n'); f.flush(); os.fsync(f.fileno())


def ev(kind, **data):
    """Append-only event ledger (JSONL, fsync per line); TEST896-899 semantics."""
    line = json.dumps(dict(seq=EVSEQ[0], t_s=round(time.perf_counter() - T0, 3), ns=time.monotonic_ns(), kind=kind, **data), default=str, sort_keys=True)
    EVSEQ[0] += 1; _append_line(EVENTS, line)


def check(name, ok, detail=None):
    """Same signature / semantics as the 730/757 check() used by the extracted engine definitions."""
    R['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail}); save(bool(not ok))
    log('PASS' if ok else 'FAIL', name, '' if detail is None else json.dumps(detail, default=str)[:600])
    if not ok: raise RuntimeError('CHECK_FAILED:' + name)


def gate(name, status, reason=None, **data):
    assert status in ('PASS', 'FAIL', 'LOCKED', 'NOT_RUN', 'DIAGNOSTIC'), status
    R['gates'][name] = {'status': status, 'reason': reason, 'data': data}; save(); ev('GATE', name=name, status=status, reason=reason)
    log('GATE', name, status, '' if reason is None else '| ' + str(reason)[:1500])
    if status == 'FAIL' and (name in CRITICAL_900 or name.startswith('GATE4_GEO_RT')): raise StopT896(name + ': ' + str(reason)[:1500])


def tech(code, **detail):
    """A technical blocker that does not stop the fixed matrix but forces UNDECIDABLE_TECHNICAL (never a scientific negative)."""
    R['technical_blockers'].append(dict(code=code, **detail)); ev('TECHNICAL_BLOCKER', code=code, **detail); log('TECHNICAL_BLOCKER', code, json.dumps(detail, default=str)[:600])


def lineage_write(row):
    _append_line(LINEAGE_FILE, json.dumps(row, sort_keys=True, default=str))


def ensure_drive():
    """Drive holds the archives and results JSON; mount it from inside a Colab kernel if it is not mounted yet."""
    if not Path('/content').exists() or Path('/content/drive/MyDrive').exists(): return
    try:
        from google.colab import drive as _gd
        _gd.mount('/content/drive')
    except Exception as e:
        DRIVE_ERR['mount'] = '%s: %s' % (type(e).__name__, e)


def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None


# ===================================================================================================== GATE 3: runtime boot (after GATE 0-2)
def boot_runtime(JP):
    """Exact runtime contract (contract pins/runtime). torch is never installed or changed; the other pins are installed
    with a torch constraint only if absent and not yet imported (TEST899 method). Any difference -> FAIL (stop)."""
    global torch, transformers, accelerate, bitsandbytes, tokenizers, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, DynamicCache
    global DTYPE, DEV, MODEL_ID, MODEL_REVISION, CUT, GPU_NAME_REQ, GPU_CC_REQ
    pins = JP['pins']['runtime']; PINS = {p: pins[p] for p in ('transformers', 'accelerate', 'bitsandbytes', 'tokenizers')}
    rec = {'python': platform.python_version(), 'required': dict(PINS, torch=pins['torch'], cuda=pins['cuda'], python_minor=pins['python_minor'])}
    ok = '.'.join(platform.python_version().split('.')[:2]) == pins['python_minor'] and _ver('torch') == pins['torch']
    if ok:
        need = [p for p, v in PINS.items() if _ver(p) != v]; rec['installed_before'] = {p: _ver(p) for p in list(PINS) + ['torch']}
        if need:
            loaded = [p for p in need if p in sys.modules]
            if loaded: gate('GATE3_RUNTIME_PINS', 'FAIL', '%s already imported with other versions; restart the runtime' % loaded, **rec)
            con = ROOT.parent / ('TEST900_torch_constraint_%s.txt' % RUN_ID); con.write_text('torch==%s\n' % pins['torch'])
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-c', str(con)] + ['%s==%s' % (p, PINS[p]) for p in need])
            importlib.invalidate_caches()
        import torch, transformers, accelerate, bitsandbytes, tokenizers
        from transformers import BitsAndBytesConfig
        from transformers.cache_utils import DynamicCache
        rec['imported'] = {'torch': torch.__version__, 'cuda': torch.version.cuda, 'transformers': transformers.__version__,
                           'accelerate': accelerate.__version__, 'bitsandbytes': bitsandbytes.__version__, 'tokenizers': tokenizers.__version__}
        ok = (torch.__version__ == pins['torch'] and torch.version.cuda == pins['cuda'] and transformers.__version__ == PINS['transformers'] and
              accelerate.__version__ == PINS['accelerate'] and bitsandbytes.__version__ == PINS['bitsandbytes'] and tokenizers.__version__ == PINS['tokenizers'])
    gate('GATE3_RUNTIME_PINS', 'PASS' if ok else 'FAIL', None if ok else 'runtime pins not met', **rec)
    MODEL_ID = JP['pins']['model']; MODEL_REVISION = JP['pins']['model_revision']; CUT = 3
    DTYPE = torch.bfloat16; DEV = torch.device('cuda:0'); GPU_NAME_REQ = JP['pins']['gpu']; GPU_CC_REQ = (8, 0)
    AutoTokenizer = transformers.AutoTokenizer; AutoModelForCausalLM = transformers.AutoModelForCausalLM


def env_gate():
    env = {'python': platform.python_version(), 'torch': torch.__version__, 'cuda': torch.version.cuda, 'transformers': transformers.__version__,
           'accelerate': accelerate.__version__, 'bitsandbytes': bitsandbytes.__version__, 'tokenizers': tokenizers.__version__,
           'cuda_available': torch.cuda.is_available(), 'device_count': torch.cuda.device_count()}
    if env['cuda_available']:
        pr = torch.cuda.get_device_properties(0)
        env.update(gpu=torch.cuda.get_device_name(0), gpu_bytes=int(pr.total_memory), compute_capability=[pr.major, pr.minor])
    R['runtime_manifest'] = {d_.metadata['Name']: d_.version for d_ in importlib.metadata.distributions() if d_.metadata['Name']}
    env['transitive'] = {k_: _ver(k_) for k_ in ('huggingface-hub', 'safetensors', 'numpy', 'sentencepiece', 'regex')}
    R['env'] = env
    ok = (env['cuda_available'] and env['device_count'] == 1 and env.get('gpu') == GPU_NAME_REQ and
          tuple(env.get('compute_capability', ())) == GPU_CC_REQ and env.get('gpu_bytes', 0) >= 79 * 2**30)
    gate('GATE3_ENV', 'PASS' if ok else 'FAIL', None if ok else 'requires exactly one %s (cc %s)' % (GPU_NAME_REQ, GPU_CC_REQ), **env)


# ===================================================================================================== GATE 3: source extraction (AST, verbatim)
REUSE = {
    '897npdm_smoke.py': {'defs': ('contract_npdm', 'query_npdm', 'segments_npdm', 'record_ids_npdm', 'parse_npdm', 'decision_key_npdm',
                                  'LedgerNPDM', 'make_env_npdm', 'facts_npdm'),
                         'consts': ('REC_TPL_NPDM', 'QUERY_TPL_NPDM', 'GRAMMAR_NPDM', 'STATUS_MARKERS_NPDM', 'FACTUAL_KINDS_NPDM',
                                    'PREDICTION_KINDS_NPDM', 'LEAK_NAMES_NPDM')},
    '898.py': {'defs': ('ledger_files_898', 'parse_belief_898'),
               'consts': ('B_FIELDS_898', 'CONSOL_INSTR_898', 'BELIEF_TPL_898', 'MAX_NEW_B', 'ZIP_LIMITS_898'),
               'nested': ('_cpu_ram_frac', 'guard', 'tok_ids', 'ntok', 'forge_record', 'load_record', 'mount_from', 'gen', 'forge_npdm',
                          'append_live', 'timed_gen', 'car_logp_898')},
    '899.py': {'defs': ('NoRun899', 'enc899', 'geometry899', 'geometry_signature899', 'assert_same_geometry899', 'gpu_mem', 'gitblob',
                        'sha_bytes', 'sha_path', 'extract_selected', 'MountOff', 'hook_inventory', 'hooks_clean', '_stream', '_qs_items',
                        '_digest_items', 'integrity_digest', 'integrity_selftest', 'hook_selftest', '_PinnedRevision', 'seals_equal',
                        'kv_compare', 'tri'),
               'consts': ('NEUTRAL_WORDS_899', 'SELECT', 'FORBIDDEN_TOKENS', 'TOL', 'EXPECTED', 'CHUNK', 'GPU_RESERVE_GIB', 'LOCKS')}}
ENGINE_SELECT_FILES = ('709.py', '730.py', '757.py')
MODEL_BLOCK_ANCHORS = ("    AutoTokenizer, AutoModelForCausalLM = _PinnedRevision(transformers.AutoTokenizer), _PinnedRevision(transformers.AutoModelForCausalLM)\n",
                       "tokenizer_commit_hash=getattr(tok, 'init_kwargs', {}).get('_commit_hash'))\n")
CART_BLOCK_ANCHORS = ("    CART_INDEX = []; R['cartridges'] = CART_INDEX\n", "guard('query', dt); return o_\n")
SUFFIX_LITERAL_709 = "suffix='\\nQUESTION:\\n'+question+'\\n\\nANSWER:\\n<|im_end|>\\n<|im_start|>assistant\\n'"


def ast_defs(src, names, nested=False):
    """Source segments of the named definitions (top level, or nested inside the try block when nested=True), each exactly once."""
    tree = ast.parse(src); found = {}
    nodes = list(ast.walk(tree)) if nested else tree.body
    for n in nodes:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names and (n.col_offset > 0) == nested:
            found.setdefault(n.name, []).append(textwrap.dedent(ast.get_source_segment(src, n, padded=True)))
    bad = {k: len(found.get(k, [])) for k in names if len(found.get(k, [])) != 1}
    if bad: raise RuntimeError('REUSE_SELECT_COUNT %s' % bad)
    return {k: v[0] for k, v in found.items()}


def ast_consts(src, names):
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names:
            out.setdefault(n.targets[0].id, []).append((ast.literal_eval(n.value), ast.get_source_segment(src, n)))
    bad = {k: len(out.get(k, [])) for k in names if len(out.get(k, [])) != 1}
    if bad: raise RuntimeError('REUSE_CONST_COUNT %s' % bad)
    return {k: v[0] for k, v in out.items()}


def anchored_block(src, a, b):
    i = src.index(a); j = src.index(b, i) + len(b)
    if src.count(a) != 1: raise RuntimeError('ANCHOR_NOT_UNIQUE ' + a[:60])
    return src[i:j]


def extract_reuse(SRC, ns):
    """AST-select the reused definitions into the namespace ns (this module's globals). Returns the provenance table:
    name -> {file, blob, sha256 of the exact segment, type, identical_in (other pinned sources with the same AST)}."""
    txt = {k: v.decode('utf-8') for k, v in SRC.items()}; table = {}
    for fname, spec in REUSE.items():
        for k, s in ast_defs(txt[fname], spec['defs']).items():
            bad = [t for t in FORBIDDEN_TOKENS_900 if t in s]
            if bad: raise RuntimeError('HOOK_TOKEN_IN_REUSED_SOURCE %s %s' % (k, bad))
            exec(compile(s, '%s:%s' % (fname, k), 'exec'), ns); table[k] = {'file': fname, 'blob': TEST_SOURCES[fname], 'sha256': sha_s(s), 'type': 'def', 'seg': s}
        for k, (v, s) in ast_consts(txt[fname], spec['consts']).items():
            ns[k] = v; table[k] = {'file': fname, 'blob': TEST_SOURCES[fname], 'sha256': sha_s(s), 'type': 'const', 'seg': s}
        for k, s in (ast_defs(txt[fname], spec['nested'], nested=True).items() if spec.get('nested') else ()):
            bad = [t for t in FORBIDDEN_TOKENS_900 if t in s]
            if bad: raise RuntimeError('HOOK_TOKEN_IN_REUSED_SOURCE %s %s' % (k, bad))
            table[k] = {'file': fname, 'blob': TEST_SOURCES[fname], 'sha256': sha_s(s), 'type': 'nested', 'seg': s}
    for k, row in table.items():                                            # continuity: same AST in the other pinned sources
        same = []
        for f2 in TEST_SOURCES:
            if f2 == row['file']: continue
            try:
                s2 = ast_consts(txt[f2], (k,))[k][1] if row['type'] == 'const' else ast_defs(txt[f2], (k,), nested=row['type'] == 'nested')[k]
            except RuntimeError:                                            # the name does not exist (once) in that source
                continue
            if ast.dump(ast.parse(s2)) == ast.dump(ast.parse(row['seg'])): same.append(f2)
        row['identical_in'] = same
    return table


FORBIDDEN_TOKENS_900 = ('register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'register_backward_hook',
                        'register_full_backward_pre_hook', 'register_module_forward_hook', 'register_module_forward_pre_hook', 'register_hook(')


def source_extract_gate(SRC):
    G = {}; ns = globals()
    table = extract_reuse(SRC, ns); G['reuse_table'] = {k: {kk: vv for kk, vv in v.items() if kk != 'seg'} for k, v in table.items()}
    G['forbidden_tokens_equal_899'] = tuple(FORBIDDEN_TOKENS) == FORBIDDEN_TOKENS_900
    sel = {}
    for fname in ENGINE_SELECT_FILES: sel[fname] = extract_selected(fname, SRC[fname], SELECT[fname], ns)
    G['engine_selected_ast_sha16'] = sel; G['engine_locks_equal_899'] = all(LOCKS[f] == ENGINE_BLOBS[f] for f in ENGINE_SELECT_FILES)
    s709 = SRC['709.py'].decode()
    ans709 = ast.get_source_segment(s709, [n for n in ast.parse(s709).body if isinstance(n, ast.FunctionDef) and n.name == 'answer'][0])
    G['answer_709_suffix_literal'] = SUFFIX_LITERAL_709 in ans709
    G['answer_709_uses_module_MAX_NEW'] = 'range(MAX_NEW)' in ans709
    for k in REUSE['898.py']['nested']:
        exec(compile(table[k]['seg'], '898.py:%s(nested)' % k, 'exec'), ns)
    s898, s899, s897 = (SRC[f].decode() for f in ('898.py', '899.py', '897npdm_smoke.py'))
    cb = anchored_block(s898, *CART_BLOCK_ANCHORS)
    G['cartridge_block_verbatim_in_897_899'] = cb in s897 and cb in s899
    mb = anchored_block(s898, *MODEL_BLOCK_ANCHORS)
    G['model_block_verbatim_in_897'] = mb in s897
    G['model_block_in_899_DIAGNOSTIC'] = mb in s899      # 899 pre-loads the tokenizer in GATE0C (three pinned calls); 900 does not
    X.MODEL_BLOCK = textwrap.dedent(mb)
    G['neutral900'] = sha_s(neutral900_source(s899))
    G['max_new_b_equal_contract'] = MAX_NEW_B == X.JP['generation']['MAX_NEW_B']
    G['suffix'] = ('\nQUESTION:\n', '\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n')
    globals()['SUFFIX_HEAD'], globals()['SUFFIX_TAIL'] = G['suffix']
    ok = all(v is True for k, v in G.items() if isinstance(v, bool) and not k.endswith('_DIAGNOSTIC'))
    gate('GATE3_SOURCE_EXTRACT', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if v is False], **G)
    return table


# ===================================================================================================== GATE 3: GPU-side preflight repeat
def pf_repeat_gate(cfg, workdir, MAN, ref_sha):
    """preflight900 v1.2.1 (sealed package tool) re-run in this runtime with the same tokenizer binding method; its manifest
    must reproduce the reference binding manifest byte for byte (pass1 SHA)."""
    pkg = Path(cfg['package_dir']); out = ROOT / 'pf_gpu_repeat'; bm = (MAN.get('tokenizer_files') or {}).get('binding_method', '')
    args = ['--contract-md', str(pkg / CONTRACT_MD), '--contract-json', str(pkg / CONTRACT_JSON), '--sums', str(pkg / 'SHA256SUMS.txt'),
            '--src-709', str(workdir / '709.py'), '--src-897', str(workdir / '897npdm_smoke.py'), '--src-898', str(workdir / '898.py'),
            '--src-899', str(workdir / '899.py'), '--res-897', cfg['res_897'], '--res-898', cfg['res_898'], '--res-899', cfg['res_899'], '--out', str(out)]
    G = {'binding_method_reference': bm}
    if bm.startswith('hub'): args += ['--tokenizer-source', 'hub', '--tokenizer-cache', str(ROOT.parent / ('TEST900_PF_TOK_' + RUN_ID))]
    elif bm.startswith('independent digests'):
        args += ['--tokenizer-source', 'local', '--tokenizer-dir', cfg.get('tokenizer_dir') or '', '--tokenizer-digests', cfg.get('tokenizer_digests') or '']
    else: G['error'] = 'UNKNOWN_BINDING_METHOD'
    rc = None
    if 'error' not in G:
        try: rc = X.PF.main(args)
        except Exception as e: G['error'] = '%s: %s' % (type(e).__name__, str(e)[:300])
    rr = json.loads((out / 'preflight900_report.json').read_text()) if (out / 'preflight900_report.json').is_file() else {}
    G.update(rc=rc, overall=rr.get('overall'), binding=rr.get('binding'), fatal=rr.get('fatal'), missing=rr.get('missing'),
             manifest_sha256=rr.get('manifest_sha256'), reference_sha256=ref_sha)
    ok = rc == 0 and rr.get('overall') == 'PASS' and rr.get('binding') is True and (rr.get('manifest_sha256') or {}).get('pass1') == ref_sha
    gate('GATE3_PF_REPEAT', 'PASS' if ok else 'FAIL', None if ok else 'GPU-side preflight does not reproduce the reference manifest', **G)


# ===================================================================================================== GATE 3: archives (CPU, before the model)
def zip_checked(path, root, limits):
    """Open a ZIP read-only with the TEST899 limits: member count / sizes / ratio from the central directory, no symlinks or
    encryption, CRC testzip, safe unique member names under <root>/, SHA256SUMS well-formed and covering every member."""
    z = zipfile.ZipFile(path, 'r'); inf = z.infolist(); names = z.namelist(); A = {}
    tot = sum(i.file_size for i in inf)
    A['within_limits'] = (0 < len(inf) <= limits['max_members'] and tot <= limits['max_total_bytes'] and
                          max([i.file_size for i in inf] or [0]) <= limits['max_member_bytes'] and tot <= limits['max_ratio'] * max(1, sum(i.compress_size for i in inf)))
    A['no_symlinks_or_special'] = all(((i.external_attr >> 16) & 0o170000) in (0, 0o100000, 0o040000) for i in inf)
    A['no_encryption'] = all(not (i.flag_bits & 0x1) for i in inf)
    if not (A['within_limits'] and A['no_symlinks_or_special'] and A['no_encryption']): raise RuntimeError('ZIP_LIMITS_OR_MEMBER_TYPE ' + str(path))
    A['crc_testzip'] = z.testzip() is None
    A['members_safe'] = all(n.startswith(root + '/') and '..' not in n.split('/') and not n.startswith('/') and '\\' not in n and ':' not in n for n in names)
    A['members_unique'] = len(names) == len(set(names))
    rows = [l.split('  ', 1) for l in z.read(root + '/SHA256SUMS.txt').decode('utf-8').split('\n') if l]
    sums = {r[1]: r[0] for r in rows if len(r) == 2}
    A['sha256sums_wellformed'] = len(sums) == len(rows) and all(re.fullmatch(r'[0-9a-f]{64}', h) for h in sums.values())
    files = {n[len(root) + 1:] for n in names if not n.endswith('/')}
    A['sha256sums_cover_members'] = files - {'SHA256SUMS.txt'} == set(sums)
    return z, sums, A


def find_member(names, root, base, sub='cartridges/'):
    m = [n for n in names if n.startswith(root + '/' + sub) and n.rsplit('/', 1)[-1] == base]
    if len(m) != 1: raise RuntimeError('ARCHIVE_MEMBER_NOT_UNIQUE %s (%d)' % (base, len(m)))
    return m[0]


def cartridge_checks(cp, ent, sha_file):
    n_ = int(cp['n'])
    return {'sha256_index': sha_file == ent['sha256'], 'tensor_seal': json.loads(json.dumps(seal_cp(cp))) == json.loads(json.dumps(ent['tensor_seal'])),
            'keys': set(cp) == {'h', 'lower', 'n', 'p', 'body_tokens', 'book_id'},
            'n_p_body': n_ == ent['n'] and cp['p'] == TOL['P_expected'] and int(cp['body_tokens']) == n_ - cp['p'] and
                        ('body_tokens' not in ent or int(ent['body_tokens']) == int(cp['body_tokens'])),
            'h_shape_dtype': tuple(cp['h'].shape) == (1, n_, EXPECTED[1]) and cp['h'].dtype == DTYPE,
            'lower_layers': len(cp['lower']) == CUT + 1 and all(tuple(k.shape) == (1, EXPECTED[3], n_, EXPECTED[4]) and tuple(v.shape) == (1, EXPECTED[3], n_, EXPECTED[4])
                                                                and k.dtype == DTYPE and v.dtype == DTYPE for k, v in cp['lower']),
            'finite': bool(torch.isfinite(cp['h']).all()) and all(bool(torch.isfinite(k).all()) and bool(torch.isfinite(v).all()) for k, v in cp['lower'])}


def archive_897_gate(cfg):
    JP = X.JP; A = {}; err = []; IN = ROOT.parent / ('TEST900_INPUT_' + RUN_ID); EV_DIR = ROOT.parent / ('TEST900_EVAL_' + RUN_ID)
    IN.mkdir(parents=True, exist_ok=False); EV_DIR.mkdir(parents=True, exist_ok=False); X.IN_DIR = IN
    try:
        zp = Path(cfg['zip_897']); A['zip_sha256_start'] = sha_path(zp); X.ZIP_SHA_START = {'897': A['zip_sha256_start']}
        z, sums, zc = zip_checked(zp, ARCH897['root'], ZIP_LIMITS_898); A.update({'zip_' + k: v for k, v in zc.items()})
        names = z.namelist(); rt = ARCH897['root']; X.ARCH = {}
        want = {b: find_member(names, rt, b) for b in ARCH897['cartridges']}
        want['results'] = rt + '/' + ARCH897['results_name']; want['manifest'] = rt + '/' + ARCH897['manifest_name']; want['vault'] = rt + '/' + ARCH897['vault_name']
        for k, m in want.items():
            data = z.read(m); rel = m[len(rt) + 1:]
            dst = (EV_DIR if k == 'vault' else IN) / ('897_' + rel.replace('/', '__')); dst.write_bytes(data)
            X.ARCH[k] = {'member': m, 'path': str(dst), 'sha256': sha_b(data), 'bytes': len(data), 'sha256sums': sums.get(rel)}
        z.close()
        A['extracted_match_sha256sums'] = all(v['sha256'] == v['sha256sums'] for v in X.ARCH.values())
        A['vault_sha256_contract'] = X.ARCH['vault']['sha256'] == JP['sources']['archive_897']['vault_sha256']   # bytes only; never parsed here
        A['public_manifest_sha256_contract'] = X.ARCH['manifest']['sha256'] == JP['sources']['archive_897']['public_manifest_sha256']
        X.VAULT_PATH = X.ARCH['vault']['path']
        R7 = json.loads(Path(cfg['res_897']).read_bytes().decode('utf-8')); X.R7 = R7
        if X.ARCH['results']['sha256'] != JP['sources']['results_sha256']['897']:
            R7z = json.loads(Path(X.ARCH['results']['path']).read_text())
            A['results_zip_copy_sections_equal'] = all(canon(R7z.get(k)) == canon(R7.get(k)) for k in ('run_id', 'cartridges', 'episodes', 'controls', 'world_manifest', 'decision'))
        A['run_identity'] = (R7.get('run_id') == ARCH897['run_id'] and R7.get('status') == 'COMPLETE' and R7.get('technical_status') == 'PASS' and
                             (R7.get('decision') or {}).get('VERDICT') == ARCH897['verdict'] and R7.get('commit') == ENGINE_COMMIT)
        A['model_revision_equal'] = R7.get('model_revision') == JP['pins']['model_revision']
        A['max_new_equal_contract'] = int((R7.get('world_manifest') or {}).get('max_new_tokens', -1)) == JP['generation']['MAX_NEW']
        CI = {}
        for e in R7['cartridges']: CI.setdefault(Path(e['file']).name, []).append(e)
        A['index_entries_unique'] = all(len(CI.get(b, [])) == 1 for b in ARCH897['cartridges'])
        X.ARCH_CP = {}; X.ARCH_ENT = {}; cc = {}
        for b in ARCH897['cartridges']:
            ent = CI[b][0]; cp = torch.load(X.ARCH[b]['path'], map_location='cpu', weights_only=True)
            cc[b] = cartridge_checks(cp, ent, X.ARCH[b]['sha256']); X.ARCH_CP[b] = cp; X.ARCH_ENT[b] = ent
        A['cartridge_checks'] = cc; A['cartridges_all_pass'] = all(all(c.values()) for c in cc.values())
        lm = ledger_files_898(R7, 'L3', 3); A['ledger_mapping_L3'] = lm
        A['ledger_files_equal_archive'] = [d['file'] for d in lm] == list(ARCH897['cartridges'][1:]) and all(X.ARCH[d['file']]['sha256'] == d['sha256'] for d in lm)
        ep = JP['worlds']['W3']['epistemic_t1']
        A['epistemic_t1_sha_contract'] = all(X.ARCH[k + '.pt']['sha256'] == v for k, v in ep.items())
        X.W3_RECORDS = [x[0] for x in R7['episodes']['L3']['ledger'][:3]]
        A['w3_records_kinds'] = [r['kind'] for r in X.W3_RECORDS] == ['MODEL_INTENT', 'MODEL_PREDICTION', 'OBSERVED_OUTCOME']
        I = JP['worlds']['W3']['identity']
        A['w3_fact_equals_records'] = [[X.W3_RECORDS[0]['A'], X.W3_RECORDS[2]['O']]] == I['facts'] and X.W3_RECORDS[0]['K'] == 'ACQUIRE'
    except Exception as e:
        err.append('%s: %s' % (type(e).__name__, str(e)[:400])); A['traceback'] = traceback.format_exc()[-4000:]
    fail = [k for k, v in A.items() if v is False] + err
    gate('GATE3_ARCHIVE_897', 'PASS' if not fail else 'FAIL', None if not fail else 'BLOCKER: %s' % fail, checks=A)


def archive_898_gate(cfg):
    JP = X.JP; A = {}; err = []
    try:
        zp = Path(cfg['zip_898']); A['zip_sha256_contract'] = sha_path(zp) == JP['sources']['archive_898_zip_sha256']; X.ZIP_SHA_START['898'] = sha_path(zp)
        z, sums, zc = zip_checked(zp, ARCH898['root'], ZIP_LIMITS_898); A.update({'zip_' + k: v for k, v in zc.items()})
        m = find_member(z.namelist(), ARCH898['root'], ARCH898['real_file']); data = z.read(m); rel = m[len(ARCH898['root']) + 1:]
        dst = X.IN_DIR / ('898_' + rel.replace('/', '__')); dst.write_bytes(data); z.close()
        A['real_sha256sums'] = sha_b(data) == sums.get(rel)
        A['real_sha256_contract'] = sha_b(data) == JP['worlds']['W3']['REAL']['cartridge_sha256']
        R8 = json.loads(Path(cfg['res_898']).read_bytes().decode('utf-8'))
        ents = [c for c in R8['cartridges'] if c.get('cid') == ARCH898['real_cid']]; A['real_index_unique'] = len(ents) == 1
        ent = ents[0]; cp = torch.load(str(dst), map_location='cpu', weights_only=True)
        A['real_cartridge_checks'] = cartridge_checks(cp, ent, sha_b(data)); A['real_cartridge_all'] = all(A['real_cartridge_checks'].values())
        gens = [g for g in R8['generations'] if g.get('gen') == ARCH898['real_generation']]; A['c3_unique'] = len(gens) == 1
        raw = gens[0]['raw']; A['real_raw_sha_contract'] = sha_s(raw) == JP['worlds']['W3']['REAL']['text_sha256']
        A['c3_valid_and_bound'] = gens[0].get('parsed_valid') is True and gens[0].get('cartridge_sha256') == ent['sha256']
        A['real_text_sha_index'] = sha_s(BELIEF_TPL_898.format(t=1, B=raw.strip())) == ent.get('text_sha256')
        A['real_parents_are_L3_t1'] = ent.get('parents_sha256') == [JP['worlds']['W3']['epistemic_t1'][k] for k in sorted(JP['worlds']['W3']['epistemic_t1'])]
        A['run_identity_898'] = R8.get('run_id') == ARCH898['run_id'] and R8.get('status') == 'COMPLETE'
        X.REAL898 = {'raw': raw, 'ent': ent, 'cp': cp, 'path': str(dst), 'sha256': sha_b(data)}
    except Exception as e:
        err.append('%s: %s' % (type(e).__name__, str(e)[:400])); A['traceback'] = traceback.format_exc()[-4000:]
    fail = [k for k, v in A.items() if v is False] + err
    gate('GATE3_ARCHIVE_898', 'PASS' if not fail else 'FAIL', None if not fail else 'BLOCKER: %s' % fail, checks=A)


# ===================================================================================================== GATE 3: model + engine
def model_gate():
    """The TEST897/898 MODEL block, verbatim (anchored segment of the pinned 898.py, identical in 897.py)."""
    exec(compile(X.MODEL_BLOCK, '898.py:MODEL_block', 'exec'), globals())


def engine_gate():
    JP, MAN, PF = X.JP, X.MAN, X.PF; G = {}
    globals()['T_EXP'] = time.perf_counter(); globals()['ABORT'] = dict(ABORT_900); globals()['METRICS'] = {'forge_s': [], 'append_s': [], 'reload_s': [], 'query_s': [], 'mount_tokens': [], 'episode_elapsed_s': {}}
    globals()['CART_INDEX'] = []; R['cartridges'] = CART_INDEX; globals()['MAX_NEW'] = JP['generation']['MAX_NEW']
    G['P_is_30'] = P == JP['mount_purity']['forge']['prefix_tokens'] == TOL['P_expected']
    G['archived_P_equal'] = all(int(cp['p']) == P for cp in X.ARCH_CP.values()) and int(X.REAL898['cp']['p']) == P
    G['model_arch'] = (NL, H, QH, KVH, HD) == tuple(EXPECTED) == (80, 8192, 64, 8, 128)
    tf = X.MAN['tokenizer_files']['files']; m7 = ((X.R7.get('gates') or {}).get('MODEL') or {}).get('data') or {}
    G['tokenizer_json_equal_pf'] = rev_files['tokenizer.json']['sha256'] == tf['tokenizer.json']['sha256']
    G['tokenizer_config_equal_pf'] = rev_files['tokenizer_config.json']['sha256'] == tf['tokenizer_config.json']['sha256']
    G['tokenizer_json_same_as_897'] = rev_files['tokenizer.json']['sha256'] == ((m7.get('revision_files') or {}).get('tokenizer.json') or {}).get('sha256')
    G['config_json_same_as_897'] = rev_files['config.json']['sha256'] == ((m7.get('revision_files') or {}).get('config.json') or {}).get('sha256')
    G['prefix_sha256_same_as_897'] = sha_bytes(PREFIX.encode()) == m7.get('prefix_sha256')
    G['name_token_ids_equal_pf'] = all([tok_ids(' ' + v), tok_ids(v)] == MAN['name_token_ids'][ns][r] for ns in ('NS-A', 'NS-B') for r, v in MAN['names'][ns].items())
    stop = {tok.eos_token_id, tok.convert_tokens_to_ids(IM_END)}
    G['stop_set_equal_pf'] = sorted(x for x in stop if x is not None) == MAN['stop_ids']['stop_set'] and tok.convert_tokens_to_ids(IM_END) == MAN['stop_ids']['canonical_stop_id']
    X.STOP_ID = MAN['stop_ids']['canonical_stop_id']; X.STOP_SET = set(MAN['stop_ids']['stop_set'])
    X.SPECIAL_IDS = set(tok.all_special_ids) | {i for i, t in getattr(tok, 'added_tokens_decoder', {}).items() if getattr(t, 'special', False)}
    X.ENC_PF = _enc_pf
    try:
        G['L_m_equal_pf'] = PF.pf1_marker({'enc899': _enc_pf, 'tok': tok}, JP) == MAN['L_m']
        G['answer_709_stop_contract'] = PF.resolve_stop(tok, PF.answer_contract_709(X.SRC['709.py'].decode()))['canonical_stop_id'] == X.STOP_ID
    except (PF.Fatal, PF.NoRun899) as e:
        G['L_m_equal_pf'] = False; G['pf_function_error'] = str(e)[:300]
    ids_ok = {}
    for b, rec in zip(ARCH897['cartridges'][1:], X.W3_RECORDS):
        ids = record_ids_npdm(rec, tok_ids); ids_ok[b] = ids_sha(ids) == X.ARCH_ENT[b].get('ids_sha256') and len(ids) == int(X.ARCH_CP[b]['body_tokens'])
    G['archived_record_token_content'] = ids_ok; G['archived_record_token_content_all'] = all(ids_ok.values())
    G['real_898_token_content'] = ids_sha(tok_ids(BELIEF_TPL_898.format(t=1, B=X.REAL898['raw'].strip()))) == X.REAL898['ent'].get('ids_sha256')
    with MountOff(): _cpf, _ = forge_native([], 'T896_' + RUN_ID + '_EMPTY_DIAG')
    G['fresh_empty_forge_equals_archived_empty_DIAGNOSTIC'] = canon(seal_cp(_cpf)) == canon(X.ARCH_ENT['T896_EMPTY.pt']['tensor_seal']); del _cpf; release()
    globals()['CP_EMPTY'] = X.ARCH_CP['T896_EMPTY.pt']                       # archived EMPTY = mount base of every TEST900 mount
    X.EMPTY_SEAL0 = seal_cp(CP_EMPTY)
    F = [X.ARCH_CP[k + '.pt'] for k in JP['worlds']['W3']['F_mount']]
    m1 = mount_from(F); s1 = full_kv_seal(m1); n1 = int(m1[0][0].shape[-2]); del m1; release()
    m2 = mount_from(F); s2 = full_kv_seal(m2); del m2; release()
    m3 = mount_from(F + [X.REAL898['cp']]); n3 = int(m3[0][0].shape[-2]); del m3; release()
    G['mount_deterministic'] = s1 == s2
    G['w3_F_mount_tokens'] = n1 == JP['worlds']['W3']['F_mount_tokens']
    G['w3_F_plus_REAL_tokens'] = n3 == JP['worlds']['W3']['REAL']['mount_tokens_with_F']
    G['gpu_free_gib'] = gpu_mem()['free_gib']; G['vram_preflight'] = G['gpu_free_gib'] >= GPU_RESERVE_GIB
    req = [k for k, v in G.items() if isinstance(v, bool) and not k.endswith('_DIAGNOSTIC')]
    fail = [k for k in req if G[k] is not True]
    gate('GATE3_ENGINE', 'PASS' if not fail else 'FAIL', None if not fail else 'failed: %s' % fail, checks=G)
    X.W0 = {'sentinel': sentinel(), 'integrity': integrity_digest(base_params, Q4MODS, BUFS)}; log('BASE_INTEGRITY', json.dumps(X.W0))


def _enc_pf(text):
    """enc899 with its NoRun899 mapped to the preflight900 exception type (PF.card_geometry / pf1_marker catch their own)."""
    try: return enc899(text)
    except NoRun899 as e: raise X.PF.NoRun899(str(e))


# ===================================================================================================== physical primitives
def now_ns(): return time.monotonic_ns()


def inv(kind, **d):
    d['kind'] = kind; d.setdefault('ns', now_ns()); X.INV.append(d); return d['ns']


def keep_text(text):
    s = sha_s(text); X.TEXTS[s] = text; return s


def forge900(text, ids, cid, nsdir, lin, parent=None):
    """Forge (730 forge_native via the verbatim TEST896 forge_record), write to SSD append-only, read back (file SHA + tensor
    seal, verbatim load_record) and register the lineage row. Returns the mountable item."""
    cid = re.sub(r'[^A-Za-z0-9_.-]', '_', cid); where = CART_DIR / nsdir; where.mkdir(parents=True, exist_ok=True)
    if (where / ('T896_' + cid + '.pt')).exists(): inv('APPEND_ONLY_VIOLATION', path=str(where / cid)); raise StopT896('APPEND_ONLY_VIOLATION ' + cid)
    t_ = time.perf_counter(); cp, ent = forge_record(list(ids), cid, parent, lin['kind'], where)
    dt = time.perf_counter() - t_; METRICS['forge_s'].append(round(dt, 3)); guard('forge', dt); del cp; release()
    t_ = time.perf_counter(); cp2 = load_record(ent); METRICS['reload_s'].append(round(time.perf_counter() - t_, 3))
    row = {k: lin.get(k) for k in LINEAGE_FIELDS}; row.update({k: v for k, v in lin.items() if k not in ('record',)})
    row.update(cid=cid, namespace=nsdir, text_sha256=sha_s(text), token_ids_sha256=ids_sha(ids), cartridge_sha256=ent['sha256'], seal=ent['tensor_seal'],
               forge={'function': 'forge_native (730)', 'prefix_tokens': P, 'h_layer': CUT, 'kv_layers': list(range(CUT + 1)),
                      'mount': 'native_append_direct (757)', 'n': ent['n'], 'body_tokens': ent['body_tokens'], 'file': ent['file'], 'reloaded_from_ssd': True},
               ns=now_ns())
    if 'record' in lin: row['replay'] = {'record': lin['record']}
    X.LIN.append(row); lineage_write(row); inv('CARTRIDGE', sha256=ent['sha256'], branch=row.get('branch'), t=row.get('t'), ns=row['ns'])
    keep_text(text)
    return {'cp': cp2, 'sha': ent['sha256'], 'ent': ent, 'row': row, 'text': text, 'ids': list(ids), 'kind': row['kind'], 't': row.get('t'),
            'record': lin.get('record'), 'parent_turns': lin.get('parent_turns', [])}


def forge_rec(rec, cid, nsdir, branch, prov, parent=None):
    text = ''.join(segments_npdm(rec)); ids = record_ids_npdm(rec, tok_ids)
    lin = {'kind': 'RECORD:' + rec['kind'], 'branch': branch, 'provenance': prov, 'template_id': 'REC_TPL_NPDM', 'transformation_id': 'record_v1',
           'source_shas': [], 't': rec.get('t', 0), 'record': dict(rec), 'parent_turns': []}
    return forge900(text, ids, cid, nsdir, lin, parent)


def archived_item(base, rec):
    """An archived TEST897 record cartridge (verified in GATE3_ARCHIVE_897 / ENGINE) registered in the lineage."""
    ent = X.ARCH_ENT[base]; text = ''.join(segments_npdm(rec)); ids = record_ids_npdm(rec, tok_ids)
    row = {k: None for k in LINEAGE_FIELDS}
    row.update(cid='ARCH897_' + base[:-3], kind='RECORD:' + rec['kind'], namespace='archive_897', branch='W3_ARCHIVE', provenance='ARCHIVE_RECORD',
               template_id='REC_TPL_NPDM', transformation_id='archive_record_897', source_shas=[ent['sha256']], text_sha256=sha_s(text),
               token_ids_sha256=ids_sha(ids), cartridge_sha256=ent['sha256'], seal=ent['tensor_seal'], t=rec.get('t'), replay={'record': dict(rec)},
               forge={'function': 'forge_native (730) in TEST897', 'file': X.ARCH[base]['path'], 'n': ent['n'], 'body_tokens': ent.get('body_tokens')}, ns=now_ns())
    if row['token_ids_sha256'] != ent.get('ids_sha256'): raise StopT896('ARCHIVED_RECORD_IDS_MISMATCH ' + base)
    X.LIN.append(row); lineage_write(row); inv('CARTRIDGE', sha256=ent['sha256'], branch='W3_ARCHIVE', t=rec.get('t'), ns=row['ns'])
    return {'cp': X.ARCH_CP[base], 'sha': ent['sha256'], 'ent': ent, 'row': row, 'text': text, 'ids': ids, 'kind': row['kind'], 't': rec.get('t'),
            'record': dict(rec), 'parent_turns': []}


def item_kind(it):
    k = it['row']['kind']; return k.split(':', 1)[1] if k.startswith('RECORD:') else ('BELIEF' if k.startswith('BELIEF:') else 'CARD')


def mount900(items, branch, k, arm, w3=False):
    t_ = time.perf_counter(); mem = mount_from([it['cp'] for it in items]); METRICS['append_s'].append(round(time.perf_counter() - t_, 3))
    seal = full_kv_seal(mem); shas = [it['sha'] for it in items]
    mi = {'cids': [it['row']['cid'] for it in items], 'shas': shas, 'seal': seal, 'mount_sha': mount_sha(shas, seal), 'tokens': int(mem[0][0].shape[-2]),
          'provenance': [it['row']['provenance'] for it in items], 'kinds': [item_kind(it) for it in items]}
    if arm in X.JP['arms']:
        bad = [it['row']['cid'] for it in items if not provenance_ok(X.JP['arms'][arm]['provenance'], it['row']['provenance'])]
        if bad: tech('MOUNT_PURITY', arm=arm, branch=branch, cartridges=bad)
    inv('MOUNT', branch=branch, k=k, arm=arm, kinds=mi['kinds'], w3=w3)
    return mem, mi


def gen_with(mem, q, maxnew):
    """Locked 709 answer() through the verbatim gen(); module MAX_NEW set to the per-call value and restored (898 method)."""
    g = globals(); old = g['MAX_NEW']; g['MAX_NEW'] = int(maxnew); t_ = time.perf_counter()
    try: raw = gen(mem, q)
    finally: g['MAX_NEW'] = old
    return raw, time.perf_counter() - t_


def car_logp_ids_900(mem, q, cids, s0):
    """car_logp_898 numeric path with an explicit id list (candidate body ids + canonical stop id): one forward over
    709 suffix + query + ids on the same mount, float32 log_softmax; measurement only."""
    sids = list(tok(SUFFIX_HEAD + q + SUFFIX_TAIL, add_special_tokens=False).input_ids); n_ = int(mem[0][0].shape[-2]); ids_ = sids + list(cids)
    with MountOff():
        cache = cache_build(mem); pos = torch.arange(n_, n_ + len(ids_), device=DEV)
        out = model(input_ids=torch.tensor([ids_], device=DEV), past_key_values=cache, attention_mask=torch.ones((1, n_ + len(ids_)), device=DEV, dtype=torch.long),
                    position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        lp = torch.log_softmax(out.logits[0, len(sids) - 1:len(ids_)].float(), -1).cpu()
        del out, cache
    release()
    tl = [float(lp[i, g]) for i, g in enumerate(cids)]
    return {'s': sum(tl), 'token_logp': tl, 'prefix_sha256': jsha([s0, sids, n_]), 'dtype': str(lp.dtype)}


def score_events(mem, q, texts):
    """Complete candidate events (body + <|im_end|>) under one conditioning prefix; V1..V6 recorded, flags computed offline."""
    s0 = full_kv_seal(mem); items, pre, dts, errs = [], set(), set(), {}
    for c in texts:
        ids = tok_ids(c) + [X.STOP_ID]
        e = X.PF.check_candidate_event(tok, c, ids, X.STOP_ID, X.STOP_SET, X.MAX_NEW_A, X.SPECIAL_IDS)
        r = car_logp_ids_900(mem, q, ids, s0); items.append([c, r['s']]); pre.add(r['prefix_sha256']); dts.add(r['dtype'])
        if e: errs[c] = e
    if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_CANDIDATE_SCORING')
    V = {'V1_identical_prefix': len(pre) == 1, 'V2_V5_event': not errs, 'V6_float32': dts == {'torch.float32'}}
    return {'items': items, 'V': V, 'valid': all(V.values()), 'errors': errs, 'S': sum(math.exp(s) for _, s in items),
            'class_scores': class_scores([(c, s) for c, s in items])}


def probe900(mem, pos, outs):
    """probe_tpl_900 measurement on the given mount: p_norm over the 3 public outcomes (complete events + stop)."""
    out = {}; s0 = full_kv_seal(mem)
    for p in X.PROBES[pos]:
        items, errs = [], {}
        for o in outs:
            ids = tok_ids(o) + [X.STOP_ID]; e = X.PF.check_candidate_event(tok, o, ids, X.STOP_ID, X.STOP_SET, X.MAX_NEW_A, X.SPECIAL_IDS)
            items.append((o, car_logp_ids_900(mem, p['text'], ids, s0)['s']))
            if e: errs[o] = e
        m = logsumexp([s for _, s in items])
        out[p['action']] = {'probe_id': p['id'], 'scores': dict(items), 'p_norm': [math.exp(s - m) for _, s in items], 'valid': not errs, 'errors': errs}
    if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_PROBE')
    return out


def readout(core, arm, world, pos, cell, grammar, items, contract, left, row_id, branch, k=None, card=None, keep=False, w3=False, why=None):
    """One greedy decision readout: MOUNT(seal) -> DECIDE (locked 709 answer, greedy, MAX_NEW) -> MEASURE (CAR + candidates)."""
    rid = '%s/%s/%s/%s/%s/%s' % (core, arm, world, pos, cell, grammar)
    rec = {'id': rid, 'row_id': row_id, 'core': core, 'arm': arm, 'world': world, 'position': pos, 'cell': cell, 'grammar': grammar,
           'branch': branch, 'k': k, 'left': left, 'contract': {kk: list(v) if isinstance(v, tuple) else v for kk, v in contract.items()}}
    if items is None:
        rec.update(status='NOT_CONSTRUCTIBLE', why=why); X.READ.append(rec); X.READ_BY_ID[rid] = rec; ev('READOUT_NOT_CONSTRUCTIBLE', id=rid, why=why); return rec, None
    q = query_npdm(contract_npdm(contract), left, grammar, rot=0)
    mem, mi = mount900(items, branch, k, arm, w3)
    if globals()['MAX_NEW'] != X.MAX_NEW_A: raise StopT896('MAX_NEW_NOT_RESTORED')
    turns = sorted({t for it in items if item_kind(it) in ('CARD', 'BELIEF') for t in it.get('parent_turns', [])})
    X.RC.take(rid); inv('DECIDE', branch=branch, k=k if k is not None else 0, mount_shas=mi['shas'], card_parent_turns=turns if k is not None else [])
    if full_kv_seal(mem) != mi['seal']: raise StopT896('MOUNT_SEAL_CHANGED_BEFORE_DECIDE')
    raw = timed_gen(mem, q)
    car = car_logp_898(mem, q, raw)
    cand = score_events(mem, q, candidate_texts(contract['actions'], contract['outcomes'], grammar))
    parsed = parse_npdm(raw, contract, grammar)
    rec.update(status='RUN', readout_index=X.RC.n, query_sha256=sha_s(q), query_tokens=len(tok_ids(q)), mount=mi, raw=raw, raw_sha256=sha_s(raw),
               retokenized_ids_sha256=ids_sha(tok_ids(raw)), retokenized_tokens=len(tok_ids(raw)), hit_max_new=len(tok_ids(raw)) >= X.MAX_NEW_A, parsed=parsed, decision_key=decision_key(parsed), event=event_kind(parsed), car=car, cand=cand,
               max_new_tokens=X.MAX_NEW_A, mounted_card=card, decoding='greedy, locked 709 answer()')
    keep_text(raw); X.READ.append(rec); X.READ_BY_ID[rid] = rec
    ev('READOUT', **{kk: v for kk, v in rec.items() if kk not in ('car', 'cand', 'contract')}); save(False)
    log('READOUT', rid, '->', repr(raw), '| mount', mi['tokens'], '| decision', rec['decision_key'])
    if keep: return rec, mem
    del mem; release(); return rec, None


def nc(why): return {'status': 'NOT_CONSTRUCTIBLE', 'why': why}
def built(x): return isinstance(x, dict) and 'cp' in x


# ===================================================================================================== card / belief builders (physical)
def consolidate_nat(src_items, acts, outs, branch, nsdir, cid, k, parent_turns):
    """CANON-NAT: consol_tpl_900 (no goal, cost, left) on the source mount; returned text = locked 709 answer() output; card
    text = forge_card_v1(returned); never repaired; INVALID cards are mounted as written (the model's own card)."""
    T = X.JP['templates']; q = T['consol_tpl_900'].format(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(len(outs)))
    eq = q == T['consol_tpl_900'].format(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(3)) and not any(
        b in q for b in ('Goal outcome', 'costs', 'Decisions left'))
    inv('CONSOL_QUERY', branch=branch, k=k, arm='CANON-NAT', equal_tpl=eq)
    mem, mi = mount900(src_items, branch, k, 'CONSOLIDATION_NAT'); raw, dt = gen_with(mem, q, X.JP['generation']['MAX_NEW_CARD'])
    del mem; release(); guard('consolidation')
    if dt > ABORT['consolidation_s']: raise StopT896('ABORT_TECHNICAL_INCOMPLETE CONSOLIDATION_TIME %.1f' % dt)
    pc = X.PF.parse_card_900(X.JP, raw, list(acts), list(outs)); text = X.B['t_forge_card_v1'](T['card_header'], raw)
    if not text.isascii(): tech('CARD_NOT_ASCII', branch=branch, cid=cid)
    ms = keep_text(raw)
    lin = {'kind': 'CARD:CANON-NAT', 'branch': branch, 'provenance': 'MODEL_CONSOLIDATION', 'template_id': 'card_header + consol_tpl_900',
           'transformation_id': 'forge_card_v1', 'source_shas': mi['shas'], 'model_text_sha256': ms, 'generation_query_sha256': sha_s(q),
           'generation_mount_sha': mi['mount_sha'], 't': k, 'parent_turns': parent_turns, 'replay': {'model_text_sha256': ms},
           'card_parse': {'valid': pc['valid'], 'why': pc.get('why')}, 'accounting': {'model_bytes': len(raw.encode()), 'template_bytes': len(T['card_header'].encode()) + 1, 'card_bytes': len(text.encode())}}
    it = forge900(text, tok_ids(text), cid, nsdir, lin, parent=src_items[-1]['sha'] if src_items else None)
    it['card'] = {'valid': pc['valid'], 'values': pc.get('values'), 'why': pc.get('why'), 'arm': 'CANON-NAT'}
    X.GENS.append({'type': 'CONSOLIDATION_NAT', 'branch': branch, 'k': k, 'cid': cid, 'query_sha256': sha_s(q), 'mount': mi['cids'], 'raw': raw, 'gen_s': round(dt, 3), 'parse': pc,
                   'hit_max_new_card': len(tok_ids(raw)) + 1 > X.JP['generation']['MAX_NEW_CARD']})
    ev('CONSOLIDATION', arm='CANON-NAT', branch=branch, k=k, cid=cid, raw_sha256=ms, valid=pc['valid'])
    return it


def transcribe_obs(records, acts, outs, branch, nsdir, cid, k, parent_turns, src_shas):
    T = X.JP['templates']
    returned, text = X.B['t_obs_transcription'](T['card_row'], T['card_header'], T['no_entry_marker'], list(acts), list(outs), records)
    lin = {'kind': 'CARD:CANON-OBS', 'branch': branch, 'provenance': 'CONTROL_TRANSFORM:transcription_of_records', 'template_id': 'card_header + card_row',
           'transformation_id': 'obs_transcription_v1', 'source_shas': src_shas, 't': k, 'parent_turns': parent_turns,
           'replay': {'records': records, 'actions': list(acts), 'outcomes': list(outs)}}
    it = forge900(text, tok_ids(text), cid, nsdir, lin, parent=src_shas[-1] if src_shas else None)
    it['card'] = {'valid': True, 'values': X.PF.parse_card_900(X.JP, returned, list(acts), list(outs)).get('values'), 'arm': 'CANON-OBS'}
    return it


def consolidate_real(src_items, contract, left, t, branch, nsdir, cid, k, parent_turns):
    """REAL: 898 consolidation unchanged (QUERY_TPL_NPDM + CONSOL_INSTR_898, MAX_NEW_B, strict parse_belief_898, BELIEF_TPL_898).
    An INVALID belief is never forged (898 rule): the arm becomes NOT_CONSTRUCTIBLE."""
    outs = list(contract['outcomes'])
    q = QUERY_TPL_NPDM.format(acts=', '.join(contract['actions']), outs=', '.join(outs), nperm=len(list(_it.permutations(outs))),
                              g=contract['goal'], c=('%.1f' % contract['cost']), left=left) + CONSOL_INSTR_898
    mem, mi = mount900(src_items, branch, k, 'CONSOLIDATION_REAL'); raw, dt = gen_with(mem, q, MAX_NEW_B); del mem; release(); guard('consolidation')
    if dt > ABORT['consolidation_s']: raise StopT896('ABORT_TECHNICAL_INCOMPLETE CONSOLIDATION_TIME %.1f' % dt)
    pb = parse_belief_898(raw); ms = keep_text(raw)
    X.GENS.append({'type': 'CONSOLIDATION_REAL', 'branch': branch, 'k': k, 'cid': cid, 'query_sha256': sha_s(q), 'mount': mi['cids'], 'raw': raw, 'gen_s': round(dt, 3),
                   'valid': pb['valid'], 'why': pb['why'], 'hit_max_new_b': len(tok_ids(raw)) + 1 > MAX_NEW_B})
    ev('CONSOLIDATION', arm='REAL', branch=branch, k=k, cid=cid, raw_sha256=ms, valid=pb['valid'])
    if not pb['valid']: return nc('B_INVALID ' + str(pb['why']))
    text = X.B['t_belief_898'](BELIEF_TPL_898, t, raw)
    lin = {'kind': 'BELIEF:REAL', 'branch': branch, 'provenance': 'MODEL_CONSOLIDATION', 'template_id': 'BELIEF_TPL_898 + CONSOL_INSTR_898',
           'transformation_id': 'belief_898_v1', 'source_shas': mi['shas'], 'model_text_sha256': ms, 'generation_query_sha256': sha_s(q),
           'generation_mount_sha': mi['mount_sha'], 't': k, 'parent_turns': parent_turns, 'replay': {'t': t, 'raw_sha256': ms}}
    it = forge900(text, tok_ids(text), cid, nsdir, lin, parent=src_items[-1]['sha'] if src_items else None)
    it.update(raw=raw, belief_t=t)
    return it


def derived_belief(real, raw2, tid, prov, arm, branch, nsdir, cid, replay, ref_geo, k, expect_sha=None):
    """U-TRIED / U-PERM / REL-FLIP: parser-valid control text with the exact REAL token geometry, or NOT_CONSTRUCTIBLE."""
    if raw2 is None: return nc('ANCHOR')
    if not parse_belief_898(raw2)['valid']: return nc('PARSER')
    text = X.B['t_belief_898'](BELIEF_TPL_898, real['belief_t'], raw2)
    try: g2 = geometry899(text, raw2); assert_same_geometry899(ref_geo, g2, arm)
    except NoRun899 as e: return nc(str(e))
    if expect_sha is not None and sha_s(text) != expect_sha: tech('CONTROL_TEXT_DIFFERS_FROM_PF', arm=arm, branch=branch); return nc('PF_TEXT_MISMATCH')
    keep_text(raw2)
    lin = {'kind': 'BELIEF:' + arm, 'branch': branch, 'provenance': prov, 'template_id': 'BELIEF_TPL_898', 'transformation_id': tid,
           'source_shas': [real['sha']], 't': k, 'parent_turns': real.get('parent_turns', []), 'replay': dict(replay, source_raw_sha256=sha_s(real['raw']), t=real['belief_t'])}
    if list(g2['ids']) != tok_ids(text): return nc('IDS_NOT_REPRODUCED')
    return forge900(text, list(g2['ids']), cid, nsdir, lin, parent=real['sha'])


def neutral_belief(real, words, pub_target, arm, branch, nsdir, cid, k, expect_sha=None):
    if not built(real): return nc('REAL_NOT_CONSTRUCTIBLE')
    try:
        ref = geometry899(real['text'], real['raw']); X.B['PUB_TARGET'] = {'actions': list(pub_target['actions']), 'outcomes': list(pub_target['outcomes'])}
        if not inspect_builders(X.B)['ok']: raise StopT896('MOUNT_BUILDER_ISOLATION')
        text, raw2, g2 = X.B['neutral900'](real['text'], real['raw'], ref, NEUTRAL_WORDS_899[words])
    except NoRun899 as e: return nc(str(e))
    if expect_sha is not None and sha_s(text) != expect_sha: tech('CONTROL_TEXT_DIFFERS_FROM_PF', arm=arm, branch=branch); return nc('PF_TEXT_MISMATCH')
    keep_text(raw2)
    lin = {'kind': 'BELIEF:' + arm, 'branch': branch, 'provenance': 'CONTROL_TRANSFORM:neutral900_v1', 'template_id': 'BELIEF_TPL_898',
           'transformation_id': 'neutral900_v1', 'source_shas': [real['sha']], 't': k, 'parent_turns': real.get('parent_turns', []),
           'replay': {'source_raw_sha256': sha_s(real['raw']), 't': real['belief_t'], 'words': words, 'pub_target': X.B['PUB_TARGET']}}
    if list(g2['ids']) != tok_ids(text): return nc('IDS_NOT_REPRODUCED')
    return forge900(text, list(g2['ids']), cid, nsdir, lin, parent=real['sha'])


def s1_card(F_items, pos, acts, outs, branch, nsdir, cid):
    """S1: the dedicated S1 probe on the F mount (I7 declared exception), formatted as the S1 card; own arm only."""
    if X.MAN['s1_geometry']['NS-A'][pos]['status'] != 'OK': return nc('S1_DIGIT_GEOMETRY (PF)')
    mem, mi = mount900(F_items, branch, 0, 'S1_PROBE'); pr = probe900(mem, pos, outs); del mem; release()
    if not all(v['valid'] for v in pr.values()): tech('S1_PROBE_EVENT_INVALID', branch=branch)
    probs = {a: pr[a]['p_norm'] for a in acts}; T = X.JP['templates']
    text = X.B['t_s1_card'](T['s1_header'], T['s1_row'], list(acts), list(outs), probs)
    X.MEAS.append({'type': 'S1_PROBE_F_MOUNT', 'branch': branch, 'mount': mi['cids'], 'probe': pr})
    if len(tok_ids(text)) not in X.MAN['s1_geometry']['NS-A'][pos]['lengths']: return nc('S1_DIGIT_GEOMETRY (runtime)')
    lin = {'kind': 'CARD:S1', 'branch': branch, 'provenance': 'MODEL_LOGIT_FORMAT', 'template_id': 's1_header + s1_row', 'transformation_id': 's1_format_v1',
           'source_shas': mi['shas'], 'generation_query_sha256': [sha_s(p['text']) for p in X.PROBES[pos]], 'generation_mount_sha': mi['mount_sha'],
           't': 0, 'parent_turns': [0], 'replay': {'actions': list(acts), 'outcomes': list(outs), 'probs': probs}}
    return forge900(text, tok_ids(text), cid, nsdir, lin, parent=F_items[-1]['sha'])


def perm_card(nat, acts, outs, role_of, branch, nsdir, cid):
    """CANON-PERM: pi applied to the ACTUAL NAT cells by action identity; direct parent = the NAT cartridge of this state."""
    if not nat['card']['valid']: return nc('NAT_CARD_INVALID')
    T = X.JP['templates']
    vals, returned, text = X.B['t_perm'](T['card_row'], T['card_header'], list(acts), role_of, X.JP['perm']['pi'], nat['card']['values'])
    lin = {'kind': 'CARD:CANON-PERM', 'branch': branch, 'provenance': 'CONTROL_TRANSFORM:pi_on_NAT_cells', 'template_id': 'card_header + card_row',
           'transformation_id': 'perm_pi_v1', 'source_shas': [nat['sha']], 't': nat['t'], 'parent_turns': nat.get('parent_turns', []),
           'replay': {'nat_model_text_sha256': nat['row']['model_text_sha256'], 'actions': list(acts), 'outcomes': list(outs), 'role_of': role_of}}
    it = forge900(text, tok_ids(text), cid, nsdir, lin, parent=nat['sha'])
    it['card'] = {'valid': True, 'values': vals, 'arm': 'CANON-PERM'}
    return it


def geo_rt(st, world, pos, epi, cards, names):
    """GATE-GEO-RT (chronology S3): records, policy queries, consolidation query and the harness-built cards reproduce the
    binding PF geometry; a mismatch is a GEO fatal code (stop before readouts)."""
    M = X.MAN; G = {}; RQ = M['records_queries']['NS-A']
    G['record_tokens'] = [len(it['ids']) for it in epi] == RQ['record_tokens'][world]
    for g in ('PRED', 'DIRECT'):
        q = query_npdm(contract_npdm(state_contract(X.JP, names, world, pos, '0.8_1')), 1, g, rot=0)
        G['query_0.8_1_' + g] = [len(tok_ids(q)), sha_s(q)] == RQ['queries']['0.8_1/' + g]['%s/%s' % (world, pos)]
    acts = [names[r] for r in X.JP['worlds']['positions'][pos]]; outs = [names[o] for o in X.JP['worlds']['positions']['outcome_order']]
    cq = X.JP['templates']['consol_tpl_900'].format(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(3))
    G['consolidation_query'] = [len(tok_ids(cq)), sha_s(cq)] == RQ['consolidation'][pos]
    sig = M['card_geometry']['NS-A']['signatures']['%s/%s' % (world, pos)]
    for arm, it in cards.items():
        if not built(it) or not it.get('card') or not it['card'].get('valid'): continue
        rows = [(a, it['card']['values'][a]) for a in acts]
        try: g_ = X.PF.card_geometry({'enc899': _enc_pf}, X.JP, rows); ok = [g_['n'], g_['rows'], g_['noncontent_sha256']] == sig and len(it['ids']) == sig[0]
        except (X.PF.Fatal, X.PF.NoRun899) as e: ok = False
        G['card_geometry_' + arm] = ok
    fatal = [k for k, v in G.items() if v is not True and not k.endswith('CANON-NAT')]
    if not G.get('card_geometry_CANON-NAT', True): tech('CARD_GEOMETRY_NOT_INVARIANT', state=st, arm='CANON-NAT')
    gate('GATE4_GEO_RT_' + st.replace('/', '_'), 'PASS' if not fatal else 'FAIL', None if not fatal else 'GEO fatal: %s' % fatal, checks=G)


# ===================================================================================================== core A (68), C (12), D (1)
def run_state_A(world, pos):
    JP = X.JP; W = JP['worlds']; names = X.NSA; st = 'A/%s/%s' % (world, pos); br = 'A_%s_%s' % (world, pos)
    acts = [names[r] for r in W['positions'][pos]]; outs = [names[o] for o in W['positions']['outcome_order']]
    role_of = {names[r]: r for r in ROLE_ACTS}; cc = state_contract(JP, names, world, pos, '0.8_1'); facts = dict(W[world]['facts'])
    epi = []                                                                 # S1 epistemic records, a1 then a2
    for i, role in enumerate(W['positions']['record_order']):
        rec = {'kind': W[world]['record'], 'A': names[role], 'O': names[facts[role]], 't': 0}
        epi.append(forge_rec(rec, '%s_E%02d_%s' % (br, i, rec['kind']), 'epistemic/' + br, br, 'DIAGNOSTIC_GIVEN', parent=epi[-1]['sha'] if epi else None))
    inv('READ_RECORDS', branch=br, source_branches=[br])
    pol = 'policy/' + br; P_ = {}; esh = [it['sha'] for it in epi]; recs = [it['record'] for it in epi]
    # S2: NAT, OBS, REAL, S1, PERM, N1, N2, U-TRIED (fixed order)
    P_['CANON-NAT'] = consolidate_nat(epi, acts, outs, br, pol, br + '_NAT', 0, [0])
    P_['CANON-OBS'] = transcribe_obs(recs, acts, outs, br, pol, br + '_OBS', 0, [0], esh)
    real = consolidate_real(epi, cc, cc['budget'], 0, br, pol, br + '_REAL', 0, [0]); P_['REAL'] = real
    P_['S1'] = s1_card(epi, pos, acts, outs, br, pol, br + '_S1')
    P_['CANON-PERM'] = perm_card(P_['CANON-NAT'], acts, outs, role_of, br, pol, br + '_PERM')
    for arm, words in (('N1', 'NEUTRAL1'), ('N2', 'NEUTRAL2')):
        P_[arm] = neutral_belief(real, words, {'actions': acts, 'outcomes': outs}, arm, br, pol, '%s_%s' % (br, arm), 0)
    if world == 'W2':
        if built(real):
            untried = [a for a in acts if a not in {names[r] for r in facts}]
            raw2 = X.B['t_u_tried'](real['raw'], untried, names['a1'])
            try: ref = geometry899(real['text'], real['raw'])
            except NoRun899 as e: ref = None
            P_['U-TRIED'] = derived_belief(real, raw2, 'u_tried_v1', 'CONTROL_TRANSFORM:first_untried_unknown_entry_replaced_by_a1', 'U-TRIED', br, pol,
                                           br + '_UTRIED', {'untried': untried, 'tried_a1': names['a1']}, ref, 0) if ref else nc('REAL_GEOMETRY')
        else: P_['U-TRIED'] = nc('REAL_NOT_CONSTRUCTIBLE')
    geo_rt(st, world, pos, epi, {k: v for k, v in P_.items() if k in ('CANON-OBS', 'CANON-PERM', 'CANON-NAT')}, names)   # S3
    X.STATES[st] = {'epi': epi, 'policy': P_, 'acts': acts, 'outs': outs, 'contract': cc, 'role_of': role_of}
    X.CARDS[st] = {arm: (P_[arm]['card'] if built(P_[arm]) and P_[arm].get('card') else None) for arm in ('CANON-NAT', 'CANON-OBS', 'CANON-PERM')}
    mounts = {'F': epi}
    for arm in ('REAL', 'N1', 'N2', 'U-TRIED'):
        if arm in P_: mounts[arm] = (epi + [P_[arm]]) if built(P_[arm]) else None
    for arm in CARD_ARMS: mounts[arm] = [P_[arm]] if built(P_[arm]) else None
    for arm in CORE_A_ARMS + (('U-TRIED',) if world == 'W2' else ()):     # S4
        card = P_[arm].get('card') if arm in P_ and built(P_[arm]) else None; why = None if mounts[arm] is not None else P_.get(arm, {}).get('why')
        readout('A', arm, world, pos, '0.8_1', 'PRED', mounts[arm], cc, cc['budget'], st + '/PRED', br, card=card, why=why)
        rec, mem = readout('A', arm, world, pos, '0.8_1', 'DIRECT', mounts[arm], cc, cc['budget'], st + '/DIRECT', br, card=card, why=why, keep=True)
        if mem is not None:                                                  # probe once per arm-state after its last grammar
            X.MEAS.append({'type': 'PROBE', 'state': st, 'arm': arm, 'mount_sha': rec['mount']['mount_sha'], 'probe': probe900(mem, pos, outs)})
            del mem; release()
    save()


def run_core_C():
    names = X.NSA; S = X.STATES['A/W1/P-last']; br = 'C_W1_P-last'
    mounts = {'F': S['epi'], 'CANON-OBS': [S['policy']['CANON-OBS']], 'CANON-NAT': [S['policy']['CANON-NAT']]}
    for cell in ('0.1_1', '0.8_3'):
        cc = state_contract(X.JP, names, 'W1', 'P-last', cell)
        for g in ('PRED', 'DIRECT'):
            q = query_npdm(contract_npdm(cc), cc['budget'], g, rot=0)
            if [len(tok_ids(q)), sha_s(q)] != X.MAN['records_queries']['NS-A']['queries']['%s/%s' % (cell, g)]['W1/P-last']:
                gate('GATE4_GEO_RT_C_' + cell, 'FAIL', 'QUERY_ROTATION_GEOMETRY_MISMATCH %s %s' % (cell, g))
        for arm in ('F', 'CANON-OBS', 'CANON-NAT'):
            card = S['policy'][arm].get('card') if arm != 'F' else None
            for g in ('PRED', 'DIRECT'):
                readout('C', arm, 'W1', 'P-last', cell, g, mounts[arm], cc, cc['budget'], 'C/W1/P-last/%s/%s' % (cell, g), br, card=card)


def run_core_D():
    S = X.STATES['A/W1/P-last']; nat = S['policy']['CANON-NAT']; cc = S['contract']
    rec, _ = readout('D', 'CANON-NAT', 'W1', 'P-last', '0.8_1', 'PRED', [nat], cc, cc['budget'], 'D/W1/P-last/PRED', 'D_W1_P-last', card=nat.get('card'))
    ref = X.READ_BY_ID['A/CANON-NAT/W1/P-last/0.8_1/PRED']
    same = {'raw': rec['raw'] == ref['raw'], 'car': canon(rec['car']) == canon(ref['car']), 'mount_sha': rec['mount']['mount_sha'] == ref['mount']['mount_sha']}
    X.CORE_D = same
    if not all(same.values()): tech('CORE_D_REPEAT_NOT_BITWISE', **same)


# ===================================================================================================== core B (20) + W3 continuation (<= 8)
def w3_control_sha(name):
    v = X.MAN['w3']['controls'].get(name, '')
    m = re.match(r'^(?:FULL |REL_ONLY )?OK:([0-9a-f]{64})', v); return m.group(1) if m else None


def run_core_B():
    JP = X.JP; W3 = JP['worlds']['W3']; I = W3['identity']; c3 = w3_contract(JP); br = 'B_W3'; pol = 'policy/W3'
    X.W3_ARCH_ITEMS = [archived_item(b, r) for b, r in zip(ARCH897['cartridges'][1:], X.W3_RECORDS)]
    byid = {it['row']['cid'][len('ARCH897_'):]: it for it in X.W3_ARCH_ITEMS}
    F = [byid[c] for c in W3['F_mount']]
    raw = X.REAL898['raw']; text = X.B['t_belief_898'](BELIEF_TPL_898, 1, raw); keep_text(raw)
    lin = {'kind': 'BELIEF:REAL', 'branch': br, 'provenance': 'MODEL_CONSOLIDATION', 'template_id': 'BELIEF_TPL_898 + CONSOL_INSTR_898 (TEST898 C3)',
           'transformation_id': 'archive_belief_898', 'source_shas': X.REAL898['ent']['parents_sha256'], 'model_text_sha256': sha_s(raw),
           'generation_query_sha256': None, 'generation_mount_sha': None, 't': 1, 'parent_turns': [1], 'replay': {'t': 1, 'raw_sha256': sha_s(raw)},
           'archived_898_cartridge_sha256': X.REAL898['sha256']}
    real = forge900(text, tok_ids(text), 'W3_REAL_B1', pol, lin, parent=F[-1]['sha']); real.update(raw=raw, belief_t=1)
    real['row']['reforged_tensor_seal_equals_898'] = canon(real['ent']['tensor_seal']) == canon(X.REAL898['ent']['tensor_seal'])
    if not real['row']['reforged_tensor_seal_equals_898']: tech('W3_REAL_REFORGE_SEAL_DIFFERS_FROM_898')
    P_ = {'REAL': real}
    try: ref = geometry899(text, raw)
    except NoRun899 as e: ref = None; tech('W3_REAL_GEOMETRY', why=str(e))
    if ref is None:
        for arm in ('U-PERM', 'REL-FLIP', 'N1', 'N2', 'NL50', 'NL100p'): P_[arm] = nc('REAL_GEOMETRY')
        X.REL_FLIP_VARIANT = 'FULL' if X.MAN['w3']['controls']['REL-FLIP'].startswith('FULL') else 'REL_ONLY'
    else:
        build_w3_controls(real, raw, ref, P_, br, pol)
    run_core_B_readouts(JP, W3, I, c3, br, pol, F, real, P_)


def build_w3_controls(real, raw, ref, P_, br, pol):
    I = X.JP['worlds']['W3']['identity']
    P_['U-PERM'] = derived_belief(real, X.B['t_u_perm'](raw, I['actions']), 'u_perm_v1', 'CONTROL_TRANSFORM:unknown_order_reversed', 'U-PERM', br, pol,
                                  'W3_UPERM', {'A': list(I['actions'])}, ref, 1, w3_control_sha('U-PERM')) if w3_control_sha('U-PERM') else nc('PF')
    rf = X.MAN['w3']['controls']['REL-FLIP']; variant = 'FULL' if rf.startswith('FULL') else 'REL_ONLY'
    m = re.search(r" filler=(.*)$", rf); filler = ast.literal_eval(m.group(1)) if (variant == 'FULL' and m) else ''
    X.REL_FLIP_VARIANT = variant; fa, fo = I['facts'][0]
    P_['REL-FLIP'] = derived_belief(real, X.B['t_rel_flip'](raw, variant, fa, fo, filler), 'rel_flip_v1', 'CONTROL_TRANSFORM:REL_flip_FULL_or_REL_ONLY',
                                    'REL-FLIP', br, pol, 'W3_RELFLIP', {'variant': variant, 'fact_a': fa, 'fact_o': fo, 'filler': filler}, ref, 1, w3_control_sha('REL-FLIP'))
    for arm, words in (('N1', 'NEUTRAL1'), ('N2', 'NEUTRAL2')):
        P_[arm] = neutral_belief(real, words, {'actions': I['actions'], 'outcomes': I['outcomes']}, arm, br, pol, 'W3_' + arm, 1, w3_control_sha(arm)) \
            if w3_control_sha(arm) else nc('PF')
    n_real = len(ref['ids'])
    for arm, k_ in (('NL100p', n_real - 1), ('NL50', n_real // 2 - 1)):
        if not w3_control_sha(arm): P_[arm] = nc('PF'); continue
        t3 = X.B['t_nl_plain'](NEUTRAL_WORDS_899['NEUTRAL1'], k_); ids3 = tok_ids(t3)
        if len(ids3) != k_ + 1 or sha_s(t3) != w3_control_sha(arm): P_[arm] = nc('NL_GEOMETRY'); tech('CONTROL_TEXT_DIFFERS_FROM_PF', arm=arm); continue
        lin = {'kind': 'BELIEF:' + arm, 'branch': br, 'provenance': 'CONTROL_TRANSFORM:plain_neutral_%s' % ('100pct' if arm == 'NL100p' else '50pct'),
               'template_id': 'neutral_plain', 'transformation_id': 'nl_plain_v1', 'source_shas': [], 't': 1, 'parent_turns': [1], 'replay': {'words': 'NEUTRAL1', 'k': k_}}
        P_[arm] = forge900(t3, ids3, 'W3_' + arm, pol, lin, parent=real['sha'])


def run_core_B_readouts(JP, W3, I, c3, br, pol, F, real, P_):
    epi_recs = [it['record'] for it in F]
    P_['CANON-OBS'] = transcribe_obs(epi_recs, I['actions'], I['outcomes'], br, pol, 'W3_OBS_C1', 1, [1], [it['sha'] for it in F])
    P_['CANON-NAT'] = consolidate_nat(F, I['actions'], I['outcomes'], br, pol, 'W3_NAT_C1', 1, [1])
    X.W3_POLICY = P_; X.W3_F = F
    mF, miF = mount900(F, br, 2, 'F', True); nF = miF['tokens']; del mF; release()
    mR, miR = mount900(F + [real], br, 2, 'REAL', True); nR = miR['tokens']; del mR; release()
    ok = nF == W3['F_mount_tokens'] and nR == W3['REAL']['mount_tokens_with_F']
    gate('GATE4_W3_GEOMETRY', 'PASS' if ok else 'FAIL', None if ok else 'W3_ARCHIVE_GEOMETRY_MISMATCH F=%d F+REAL=%d' % (nF, nR), F=nF, F_plus_REAL=nR)
    mounts = {'F': F}
    for arm in ('REAL', 'U-PERM', 'REL-FLIP', 'N1', 'N2', 'NL50', 'NL100p'): mounts[arm] = F + [P_[arm]] if built(P_[arm]) else None
    for arm in ('CANON-OBS', 'CANON-NAT'): mounts[arm] = [P_[arm]]
    for arm in JP['matrix_core']['B']['arms']:
        card = P_[arm].get('card') if arm in P_ and built(P_[arm]) else None
        for g in ('PRED', 'DIRECT'):
            readout('B', arm, 'W3', '-', 'W3', g, mounts[arm], c3, c3['budget'], 'B/W3/%s/%s' % (arm, g), 'W3C/' + arm, k=2, card=card,
                    w3=True, why=None if mounts[arm] is not None else P_.get(arm, {}).get('why'))
    save()


def make_branch_env(branch, k):
    """Each branch gets its own TEST897 environment (mapping only in the closure, pend_left = 0); the vault file is opened
    here, at ENV(k), after WRITE-INTENT(k), and nowhere else."""
    inv('VAULT_ACCESS', branch=branch, k=k)
    b = Path(X.VAULT_PATH).read_bytes()
    if sha_b(b) != X.JP['sources']['archive_897']['vault_sha256']: raise StopT896('VAULT_SHA_CHANGED')
    I = X.JP['worlds']['W3']['identity']; mp = vault_mapping_w3(json.loads(b.decode('utf-8')), I['actions'], I['facts'])
    env = make_env_npdm(mp, I['goal'], 0, time.monotonic_ns); del mp, b
    return env, '%s#%x' % (branch, id(env))


def run_w3_continuation():
    JP = X.JP; W3 = JP['worlds']['W3']; C = W3['continuation']; I = W3['identity']; c3 = w3_contract(JP); X.W3C = {}
    for arm in C['arms']:
        branch = 'W3C/' + arm; bdir = 'epistemic/W3C_' + arm.replace('-', '_'); pdir = 'policy/W3C_' + arm.replace('-', '_')
        src = X.READ_BY_ID.get('B/%s/W3/-/W3/PRED' % arm); B = {'branch': branch, 'decisions': [], 'V_REAL': 0.0, 'end': None, 'records': []}
        X.W3C[arm] = B
        if not src or src['status'] != 'RUN': B['end'] = 'NOT_RUN_SOURCE_READOUT_MISSING'; continue
        L = LedgerNPDM(time.monotonic_ns)
        for it in X.W3_ARCH_ITEMS: L.add(it['record'], {'sha256': it['sha']})
        live = []; env = env_id = None; card_prev = X.W3_POLICY.get(arm) if arm in ('CANON-OBS', 'CANON-NAT') else None
        b_prev = X.W3_POLICY['REAL'] if arm == 'REAL' else None
        for idx, k in enumerate(C['decisions']):
            left = C['left'][idx]
            if k == 2:
                r = src; d = {'decision_id': '%s/k%d' % (branch, k), 'source_readout_id': src['id'], 'mount_sha': src['mount']['mount_sha'],
                              'query_sha': src['query_sha256'], 'raw_greedy_sha': src['raw_sha256'], 'inherited': True}
                d['binding_equal'] = (d['mount_sha'], d['query_sha'], d['raw_greedy_sha']) == (src['mount']['mount_sha'], src['query_sha256'], sha_s(src['raw']))
                if not d['binding_equal']: tech('W3_K2_BINDING', branch=branch)
            else:
                filt = [it for it in X.W3_ARCH_ITEMS + live if item_kind(it) != 'MODEL_PREDICTION' and it['t'] < k]
                items = filt if arm == 'F' else (filt + [b_prev] if arm == 'REAL' else [card_prev])
                inv('READ_RECORDS', branch=branch, source_branches=sorted({it['row']['branch'] for it in items if item_kind(it) not in ('CARD', 'BELIEF')} | {branch}))
                r, _ = readout('W3C', arm, 'W3', '-', 'k%d' % k, 'PRED', items, c3, left, '%s/k%d' % (branch, k), branch, k=k,
                               card=card_prev.get('card') if card_prev else None, w3=True)
                d = {'decision_id': '%s/k%d' % (branch, k), 'readout_id': r['id'], 'mount_sha': r['mount']['mount_sha'], 'query_sha': r['query_sha256'],
                     'raw_greedy_sha': r['raw_sha256'], 'inherited': False}
            p = r['parsed']; evk = event_kind(p); d.update(event=evk, decision_key=r['decision_key'], left=left)
            # k.4 WRITE-INTENT (sealed before any environment call)
            def W(rec_):
                it_ = forge_rec(rec_, 'W3C_%s_k%d_%02d_%s' % (arm, k, len(live), rec_['kind']), bdir, branch, 'LIVE_RECORD', parent=(live[-1]['sha'] if live else X.W3_ARCH_ITEMS[-1]['sha']))
                live.append(it_); L.add(rec_, {'sha256': it_['sha']}); B['records'].append({'kind': rec_['kind'], 't': k, 'sha256': it_['sha']}); return it_
            if evk in ('ACT', 'ACQUIRE'):
                W({'kind': 'MODEL_INTENT', 'K': p['kind'], 'A': p['action'], 't': k}); W({'kind': 'MODEL_PREDICTION', 'P': p['prediction'], 't': k, 'pred_status': 'VALID'})
            elif evk == 'STOP': W({'kind': 'MODEL_STOP', 't': k})
            else: W({'kind': 'MODEL_INVALID', 't': k})
            inv('WRITE_INTENT', branch=branch, k=k)
            # k.5 ENV
            recs_, envcall, terminal, exhausted = continuation_transition(evk, left)
            if envcall:
                if env is None: env, env_id = make_branch_env(branch, k)
                res = env['step'](p['kind'], p['action'], L.ticket(k)); inv('ENV', branch=branch, k=k, env_id=env_id)
                o_it = W({'kind': 'OBSERVED_OUTCOME', 'O': res['outcome'], 't': k})
                if o_it['row']['ns'] <= res['env_step_start_ns']: raise StopT896('OUTCOME_SEALED_BEFORE_ENV_STEP')
                d.update(outcome=res['outcome'], reward=res['reward'], cost=c3['cost'] if p['kind'] == 'ACQUIRE' else 0.0)
                B['V_REAL'] += res['reward'] - (c3['cost'] if p['kind'] == 'ACQUIRE' else 0.0)
            elif evk == 'INVALID':
                W({'kind': 'OUTCOME_STATUS', 'S': STATUS_MARKERS_NPDM['none'], 't': k}); d.update(env='NOT_CALLED', cost=0.0)
            B['decisions'].append(d); ev('W3C_DECISION', **d)
            # k.6 END?
            if terminal: B['end'] = 'MODEL_' + evk; break
            if exhausted: B['end'] = 'BUDGET_EXHAUSTED'; ev('BUDGET_EXHAUSTED', branch=branch, k=k, note='harness event, not a model STOP'); break
            # k.7 CONSOLIDATE for k+1 from this branch's records t <= k
            allrec = X.W3_ARCH_ITEMS + live; fil = [it for it in allrec if item_kind(it) != 'MODEL_PREDICTION' and it['t'] <= k]
            if arm == 'REAL':
                b_prev = consolidate_real(allrec, c3, left - 1, k, branch, pdir, 'W3C_REAL_B%d' % k, k, [k])
                if not built(b_prev): B['end'] = 'B_INVALID_NOT_FORGED'; break
                b_prev.update(belief_t=k)
            elif arm == 'CANON-NAT': card_prev = consolidate_nat(fil, I['actions'], I['outcomes'], branch, pdir, 'W3C_NAT_C%d' % k, k, [k])
            elif arm == 'CANON-OBS':
                card_prev = transcribe_obs([it['record'] for it in fil], I['actions'], I['outcomes'], branch, pdir, 'W3C_OBS_C%d' % k, k, [k], [it['sha'] for it in fil])
            if arm != 'F': inv('CARD_FOR_NEXT', branch=branch, k=k, parent_turns=[it['t'] for it in (allrec if arm == 'REAL' else fil)], requires_env=envcall)
        if B['end'] is None: B['end'] = 'DECISIONS_EXHAUSTED'
        ev('W3C_BRANCH_END', branch=branch, end=B['end'], V_REAL=B['V_REAL']); save()


# ===================================================================================================== offline evaluation (runtime)
PLANNED = {'A': 68, 'B': 20, 'C': 12, 'D': 1}


def offline_evaluation(cfg):
    """After every generation: GENERATION_SEALED -> lineage replay -> evaluator objects (contract JSON re-read) -> rules."""
    JP = X.JP; sealed = inv('GENERATION_SEALED'); ev('GENERATION_SEALED', readouts=X.RC.n, cartridges=len(X.LIN)); X.SEALED_NS = sealed
    O = {'generation_sealed_ns': sealed, 'readout_count': X.RC.n}
    NSr = {'tok_ids': tok_ids, 'segments_npdm': segments_npdm, 'record_ids': lambda r: record_ids_npdm(r, tok_ids),
           'parse_card': lambda t, a, o: X.PF.parse_card_900(JP, t, list(a), list(o)), 'BELIEF_TPL_898': BELIEF_TPL_898,
           'geometry899': geometry899, 'NEUTRAL_WORDS_899': NEUTRAL_WORDS_899}
    LR = lineage_replay(X.LIN, X.TEXTS, X.B, NSr, JP); O['lineage_replay'] = LR
    gate('GATE4_LINEAGE_REPLAY', 'PASS' if LR['status'] == 'PASS' else 'FAIL', None if LR['status'] == 'PASS' else 'LINEAGE_BLOCKER', rows=LR['rows'],
         mismatch=LR['mismatch'][:20], errors=LR['errors'][:20])
    cnt = {c: {'run': sum(1 for r in X.READ if r['core'] == c and r['status'] == 'RUN'), 'not_constructible': sum(1 for r in X.READ if r['core'] == c and r['status'] != 'RUN')} for c in ('A', 'B', 'C', 'D', 'W3C')}
    mx = {'counts': cnt, 'max': JP['matrix_core']['max_greedy_readouts'], 'counter': X.RC.n,
          'planned_ok': all(cnt[c]['run'] + cnt[c]['not_constructible'] == PLANNED[c] for c in PLANNED) and cnt['W3C']['run'] <= JP['matrix_core']['B']['continuation_max_extra'],
          'counter_ok': X.RC.n == sum(v['run'] for v in cnt.values()) <= JP['matrix_core']['max_greedy_readouts']}
    O['matrix'] = mx
    gate('GATE4_RUNTIME', 'PASS' if mx['planned_ok'] and mx['counter_ok'] else 'FAIL', None if mx['planned_ok'] and mx['counter_ok'] else 'MATRIX_COUNT', **mx)
    b = (Path(cfg['package_dir']) / CONTRACT_JSON).read_bytes()
    if sha_b(b) != CONTRACT_JSON_SHA: tech('CONTRACT_JSON_CHANGED_DURING_RUN')
    ens = inv('EVALUATOR_LOADED'); JE = json.loads(b.decode('utf-8')); T = JE['thresholds']; ev('EVALUATOR_LOADED')
    ie = check_invariants(X.INV, sealed, ens); O['invariants'] = ie
    gate('GATE4_INVARIANTS', 'PASS' if not ie else 'FAIL', None if not ie else 'I1-I11 violated: %s' % ie[:20])
    RULES = load_by_path('t900_rules900', Path(cfg['package_dir']) / 'tools' / 'rules900.py')
    names = X.NSA; W = JE['worlds']; marker = JP['templates']['no_entry_marker']
    OPTW3 = list(W['W3']['OPT']); QW3 = dict(W['W3']['Q'])
    for r in X.READ:
        if r['status'] != 'RUN': continue
        r['cand']['mass'] = candidate_mass(r['cand']['items'], T['residual_tol'], r['cand']['valid'])
        r['cand']['prob_undefined'] = r['cand']['mass']['flag'] == 'PROBABILITY_UNDEFINED'
        if r['core'] == 'W3C': r['ev'] = {'note': 'continuation decisions are evaluated by V_REAL (environment reward - cost) only'}; continue
        if r['world'] == 'W3': O_, Q_ = OPTW3, QW3
        else: O_, Q_ = opt_named(W[r['world']]['OPT'][r['cell']], names), q_named(W[r['world']]['Q'][r['cell']], names)
        r['ev'] = enrich(r, O_, Q_, T['tau_nat'], T['residual_tol'])
    A = {}
    for r in X.READ:
        if r['core'] == 'A' and r['status'] == 'RUN': A.setdefault(r['row_id'], {})[r['arm']] = r
    A = {rid: A.get(rid, {}) for rid in (x['id'] for x in JE['readouts_core_A'])}
    goal_of, opt_of, det, cardc = {}, {}, {}, {}
    for st in JE['states_core_A']:
        w, pos = st.split('/')[1:]; S = X.STATES[st]
        goal_of[st] = names[W[w]['goal']]; opt_of[st] = opt_named(W[w]['OPT']['0.8_1'], names)
        det[st] = determination_table(S['acts'], S['outs'], [(names[a], names[o]) for a, o in W[w]['facts']])
        tt = {names[a]: names[o] for a, o in W[w]['true_table'].items()}
        if any(det[st][a] != tt[a] for a in tt): tech('CONTRACT_TRUE_TABLE_DIFFERS_FROM_DETERMINATION', state=st)
        cardc[st] = card_correct(X.CARDS[st]['CANON-NAT'], det[st], marker)
    nat_cards = {st: X.CARDS[st]['CANON-NAT'] for st in JE['states_core_A']}; perm_cards = {st: X.CARDS[st]['CANON-PERM'] for st in JE['states_core_A']}
    rows_f = build_core_rows(A, 'F', nat_cards, perm_cards, goal_of, opt_of, True)
    rows_nat = build_core_rows(A, 'CANON-NAT', nat_cards, perm_cards, goal_of, opt_of, True)
    if rows_f is None or rows_nat is None: tech('CORE_A_F_OR_NAT_INCOMPLETE')
    arm_rows = {arm: build_core_rows(A, arm, nat_cards, perm_cards, goal_of, opt_of, True) for arm in ('REAL', 'S1', 'CANON-OBS')}
    tech_ok = not R['technical_blockers'] and all(g['status'] in ('PASS', 'DIAGNOSTIC') for g in R['gates'].values())
    obs_w1_go = sum(A[rid]['CANON-OBS']['ev']['GO'] for rid in A if rid.startswith('A/W1/') and 'CANON-OBS' in A[rid])
    O['TOP'] = top_verdict(RULES, rows_nat or [], rows_f or [], cardc, T, tech_ok and rows_f is not None and rows_nat is not None, obs_w1_go, arm_rows) \
        if rows_f is not None and rows_nat is not None else {'headline': 'UNDECIDABLE_TECHNICAL', 'why': 'CORE_A_F_OR_NAT_INCOMPLETE'}
    O['E1_card_correct'] = cardc; O['determination_tables'] = det
    Bd = {(r['arm'], r['grammar']): r for r in X.READ if r['core'] == 'B' and r['status'] == 'RUN'}
    I = JE['worlds']['W3']['identity']
    h1w3 = rule_h1_w3(Bd, T, I); h1w2 = rule_h1_w2(A, T, names)
    S_W1L, S_W1F = X.STATES['A/W1/P-last'], X.STATES['A/W1/P-first']
    Fs = {'W1/P-last': {'PRED': A['A/W1/P-last/PRED'].get('F'), 'DIRECT': A['A/W1/P-last/DIRECT'].get('F'), 'determined': set(S_W1L['acts'])},
          'W1/P-first': {'PRED': A['A/W1/P-first/PRED'].get('F'), 'DIRECT': A['A/W1/P-first/DIRECT'].get('F'), 'determined': set(S_W1F['acts'])},
          'W3': {'PRED': Bd.get(('F', 'PRED')), 'DIRECT': Bd.get(('F', 'DIRECT')), 'determined': {I['facts'][0][0]}}}
    Cd = lambda cell: {g: next((r for r in X.READ if r['core'] == 'C' and r['arm'] == 'F' and r['cell'] == cell and r['grammar'] == g and r['status'] == 'RUN'), None) for g in ('PRED', 'DIRECT')}
    A81 = {g: A['A/W1/P-last/%s' % g].get('F') for g in ('PRED', 'DIRECT')}
    O['root_cause'] = {
        'REAL-N': rule_real_n(A, T), 'H1-W3': h1w3, 'H1-W2': h1w2, 'H1': rule_h1(h1w3, h1w2), 'H2': rule_h2(Bd, T, X.REL_FLIP_VARIANT),
        'H2p-SAL': rule_h2p_sal(Bd, T, I), 'H2p-LOOK': rule_h2p_look(A, T), 'H2p-PRED': rule_h2p_pred(Fs),
        'H2p-COST': rule_sensitivity(Cd('0.1_1'), A81, A81, Cd('0.1_1'), T, -1),
        'H2p-LEFT': rule_sensitivity(Cd('0.8_3'), A81, Cd('0.8_3'), A81, T, +1),
        'H3': rule_h3(Bd, T), 'W3-ARCH': rule_w3_arch(Bd)}
    O['W3_continuation'] = {arm: {'end': b_['end'], 'V_REAL': round(b_['V_REAL'], 6), 'decisions': b_['decisions']} for arm, b_ in X.W3C.items()}
    O['descriptive'] = descriptive_measures(A, JE, names, det)
    O['core_D_repeat'] = X.CORE_D
    O['rel_flip_variant'] = X.REL_FLIP_VARIANT
    O['scope'] = {'classification': JE['classification'], 'not_claimed': JE['classification']['forbidden_claims'], 'X_R_after_PROVISIONAL_PASS': JE['extensions']['X-R']}
    R['offline'] = O; save()
    gate('OFFLINE_EVALUATION', 'DIAGNOSTIC', O['TOP'].get('headline'), gate_vector=O['TOP'].get('gate_vector'))
    return O


def descriptive_measures(A, JE, names, det):
    """U_ACQ (direct / deduced, greedy rate + candidate mass), F_ACQ (ACQUIRE at left = 1) and KAD per arm; reported only."""
    know = JE['thresholds']['know_p']; out = {}
    probes = {(m['state'], m['arm']): m['probe'] for m in X.MEAS if m['type'] == 'PROBE'}
    for rid, arms in A.items():
        st = '/'.join(rid.split('/')[:3]); w = rid.split('/')[1]; observed = {names[a] for a, _ in JE['worlds'][w]['facts']}
        for arm, r in arms.items():
            d = out.setdefault(arm, {'readouts': 0, 'U_ACQ_direct': 0, 'U_ACQ_deduced': 0, 'U_ACQ_candidate_mass_sum': 0.0, 'F_ACQ': 0, 'KAD': 0})
            d['readouts'] += 1; key = r['decision_key']
            sc = r['cand']['class_scores']; tot = sum(math.exp(v) for v in sc.values()) or 1.0
            d['U_ACQ_candidate_mass_sum'] += sum(math.exp(v) for k, v in sc.items() if k.startswith('ACQUIRE ') and det[st].get(k.split()[1])) / tot
            if key.startswith('ACQUIRE '):
                a = key.split()[1]; d['F_ACQ'] += 1
                if det[st].get(a): d['U_ACQ_direct' if a in observed else 'U_ACQ_deduced'] += 1
                pr = probes.get((st, arm), {}).get(a)
                if pr and det[st].get(a):
                    p_true = pr['p_norm'][X.STATES[st]['outs'].index(det[st][a])]
                    if p_true >= know: d['KAD'] += 1
    return out


def end_gates(cfg):
    E = {'zip_897_unchanged': sha_path(cfg['zip_897']) == X.ZIP_SHA_START['897'], 'zip_898_unchanged': sha_path(cfg['zip_898']) == X.ZIP_SHA_START['898'],
         'results_unchanged': all(sha_b(Path(cfg['res_' + k]).read_bytes()) == X.JP['sources']['results_sha256'][k] for k in ('897', '898', '899'))}
    gate('ARCHIVE_END', 'PASS' if all(E.values()) else 'FAIL', None if all(E.values()) else 'an input changed during the run', **E)
    files_end = {e['cid']: sha_path(e['file']) == e['sha256'] for e in CART_INDEX}
    inputs_end = {k: sha_path(v['path']) == v['sha256'] for k, v in X.ARCH.items()}
    p1 = {'cartridge_files_unchanged': all(files_end.values()), 'archive_inputs_unchanged': all(inputs_end.values()),
          'empty_seal_unchanged': canon(seal_cp(CP_EMPTY)) == canon(X.EMPTY_SEAL0), 'real898_unchanged': sha_path(X.REAL898['path']) == X.REAL898['sha256'],
          'cartridges': len(files_end)}
    ok1 = all(v for k, v in p1.items() if k != 'cartridges')
    gate('P1_PHYSICAL', 'PASS' if ok1 else 'FAIL', None if ok1 else 'a cartridge or input file changed after it was written/verified', **p1)
    hooks_end = hook_inventory(); W1 = {'sentinel': sentinel(), 'integrity': integrity_digest(base_params, Q4MODS, BUFS)}
    p7 = {'hooks_clean_end': hooks_clean(hooks_end), 'same_parameter_objects': {id(p) for _, p in base_params} == {id(p) for _, p in model.named_parameters()},
          'lora_absent': not any('lora' in n.lower() for n, _ in model.named_parameters()), 'base_frozen': all(not p.requires_grad for _, p in model.named_parameters()),
          'eval_mode': not model.training, 'sentinel_equal': W1['sentinel'] == X.W0['sentinel'], 'integrity_equal': W1['integrity']['sha256'] == X.W0['integrity']['sha256']}
    gate('P7_INTEGRITY', 'PASS' if all(p7.values()) else 'FAIL', None if all(p7.values()) else [k for k, v in p7.items() if not v], **p7)


def final_decision():
    bad = {k: g['status'] for k, g in R['gates'].items() if g['status'] not in ('PASS', 'DIAGNOSTIC')}
    technical = not bad and not R['technical_blockers']
    head = (R.get('offline') or {}).get('TOP', {}).get('headline') if technical else 'UNDECIDABLE_TECHNICAL'
    R['decision'] = {'VERDICT': head, 'technical': 'PASS' if technical else 'FAIL', 'failed_gates': bad, 'technical_blockers': R['technical_blockers'],
                     'gate_vector': (R.get('offline') or {}).get('TOP', {}).get('gate_vector'), 'arm_labels': (R.get('offline') or {}).get('TOP', {}).get('arm_labels'),
                     'scope': 'TEST900 stage 1, NS-A only; PROVISIONAL at best; X-R (NS-B) is a later stage and is NOT completed by this run',
                     'implementation_status': IMPLEMENTATION_STATUS}
    R['scientific_verdict'] = head if technical else None; R['technical_verdict'] = 'PASS' if technical else 'UNDECIDABLE_TECHNICAL'
    R['status'] = 'COMPLETE'; save()
    log('TEST900_FINAL VERDICT=%s | TECHNICAL=%s | READOUTS=%d | %s' % (head, R['technical_verdict'], X.RC.n, IMPLEMENTATION_STATUS))


# ===================================================================================================== artefacts
def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()


def write_source_hashes(cfg, SRC, rep, extra=None):
    pkg = Path(cfg['package_dir']); T = {'marker': MARKER, 'implementation_status': IMPLEMENTATION_STATUS, 'contract': R['contract'], 'sources': {}, 'package': {}, 'inputs': {}}
    for n, b in (SRC or {}).items(): T['sources'][n] = {'sha256': sha_b(b), 'git_blob': blob_b(b), 'bytes': len(b)}
    if pkg.is_dir():
        for p in sorted(pkg.rglob('*')):
            if p.is_file(): T['package'][p.relative_to(pkg).as_posix()] = sha_file(p)
    for k in ('pf_report', 'pf_manifest', 'authorization', 'res_897', 'res_898', 'res_899'):
        p = Path(cfg[k]); T['inputs'][k] = {'path': str(p), 'sha256': sha_file(p) if p.is_file() else None}
    b, mode = capture_self(); T['executor_900py'] = {'capture': mode, 'sha256': sha_b(b) if b else None, 'git_blob': blob_b(b) if b else None, 'bytes': len(b) if b else None}
    if extra: T.update(extra)
    (ROOT / 'TEST900_source_hashes.json').write_text(json.dumps(T, indent=1, sort_keys=True, default=str))


def finalize_artifacts():
    """results JSON + log + events + lineage + manifest/gate report + source hash table + cartridges -> SHA256SUMS -> ZIP
    (testzip, SHA256SUMS re-verified from the ZIP, report-in-ZIP == read-back report) -> receipt -> Drive copy."""
    R['finished_utc'] = datetime.now(timezone.utc).isoformat(); R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: save()
    except Exception as e: print('RESULTS_WRITE_FAILED', e)
    AG = {}
    try:
        rep_sha = sha_file(OUT); AG['report_written_read_back'] = json.loads(OUT.read_text())['run_id'] == RUN_ID
        files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt' and not p.name.endswith('.tmp'))
        sums = ['%s  %s' % (sha_file(p), p.relative_to(ROOT).as_posix()) for p in files]
        (ROOT / 'SHA256SUMS.txt').write_text('\n'.join(sums) + '\n')
        zp = ROOT.parent / ('TEST900_SONUC_%s.zip' % RUN_ID)
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in files + [ROOT / 'SHA256SUMS.txt']: z.write(p, ROOT.name + '/' + p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(zp) as z:
            AG['zip_testzip'] = z.testzip() is None
            rows = [l.split('  ', 1) for l in z.read(ROOT.name + '/SHA256SUMS.txt').decode().split('\n') if l]
            AG['sha256sums'] = all(sha_b(z.read(ROOT.name + '/' + rel)) == h for h, rel in rows) and len(rows) == len(files)
            AG['report_in_zip_is_read_back_report'] = sha_b(z.read(ROOT.name + '/' + OUT.name)) == rep_sha
        AG['zip'] = str(zp); AG['zip_sha256'] = sha_file(zp)
        if DRIVE_DIR is not None:
            try: dz = Path(DRIVE_DIR) / zp.name; shutil.copy2(zp, dz); AG['drive'] = sha_file(dz) == AG['zip_sha256']
            except Exception as e: AG['drive'] = False; AG['drive_error'] = '%s: %s' % (type(e).__name__, e)
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    core = all(AG.get(k) is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report'))
    status = 'FAIL' if not core else ('PASS' if DRIVE_DIR is not None and AG.get('drive') else 'LOCAL_ONLY_DRIVE_NOT_COPIED')
    receipt = {'test': TAG, 'marker': MARKER, 'run_id': RUN_ID, 'status': R.get('status'), 'implementation_status': IMPLEMENTATION_STATUS,
               'scientific_verdict': R.get('scientific_verdict'), 'technical_verdict': R.get('technical_verdict'), 'artifact_status': status,
               'artifacts': AG, 'results_sha256': AG.get('report_written_read_back') and sha_file(OUT)}
    rp = ROOT.parent / ('TEST900_SONUC_%s_RECEIPT.json' % RUN_ID); rp.write_text(json.dumps(receipt, indent=1, default=str))
    if DRIVE_DIR is not None:
        try: shutil.copy2(rp, Path(DRIVE_DIR) / rp.name)
        except OSError as e: receipt['drive_receipt_error'] = '%s: %s' % (type(e).__name__, e)
    print('TEST900 ARTIFACTS', json.dumps(receipt, default=str)[:1500])
    return receipt


# ===================================================================================================== GPU path (only after GATE 0-2 PASS)
def gpu_main(cfg, J, SRC, MAN, rep, workdir):
    global DRIVE_DIR
    X.JP = public_view(J); X.MAN = MAN; X.SRC = SRC; X.CFG = cfg
    X.PF = load_by_path('t900_preflight900', Path(cfg['package_dir']) / 'tools' / 'preflight900.py')
    leak = leak_scan(X.JP)
    del J
    if leak: raise StopT896('EVALUATOR_KEYS_IN_PUBLIC_VIEW %s' % leak[:10])
    R['status'] = 'GPU_GATES'
    if Path('/content/drive/MyDrive').exists():
        DRIVE_DIR = '/content/drive/MyDrive/TEST900_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True)
    self_b, mode = capture_self(); ec = published_identity(self_b, ROOT.parent / ('TEST900_srcid_' + RUN_ID)); R['executed_source'] = ec
    auth_blob = json.loads(Path(cfg['authorization']).read_text(encoding='utf-8')).get('executor_900py_git_blob')
    ok = ec['identity_match'] and (ec.get('published') or {}).get('tree_blob') == auth_blob
    gate('GATE3_EXECUTED_SOURCE_IDENTITY', 'PASS' if ok else 'FAIL', None if ok else 'executed 900.py is not the published / authorised 900.py',
         failed=ec.get('failed_checks'), published=ec.get('published'), authorised_blob=auth_blob, capture=mode)
    boot_runtime(X.JP); env_gate()
    SEED = 20261119; random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    globals()['PINNED_CALLS'] = []
    table = source_extract_gate(SRC)
    write_source_hashes(cfg, SRC, rep, {'reuse_table': {k: {kk: vv for kk, vv in v.items() if kk != 'seg'} for k, v in table.items()}})
    pf_repeat_gate(cfg, workdir, MAN, rep['gates']['GATE1_BINDING_PREFLIGHT']['manifest_sha256'])
    archive_897_gate(cfg); archive_898_gate(cfg)
    (ROOT / 'TEST900_input_manifest.json').write_text(json.dumps({
        'archive_897': {'zip': cfg['zip_897'], 'zip_sha256': X.ZIP_SHA_START['897'], 'files': {k: {kk: v[kk] for kk in ('member', 'sha256', 'bytes')} for k, v in X.ARCH.items()}},
        'archive_898': {'zip': cfg['zip_898'], 'zip_sha256': X.ZIP_SHA_START['898'], 'real': {'sha256': X.REAL898['sha256'], 'raw_sha256': sha_s(X.REAL898['raw'])}},
        'pf_reference_manifest_sha256': rep['gates']['GATE1_BINDING_PREFLIGHT']['manifest_sha256'],
        'authorization_sha256': rep['gates']['GATE2_INDEPENDENT_ACCEPTANCE_AND_GPU_PERMISSION'].get('authorization_sha256'),
        'results_sha256': X.JP['sources']['results_sha256'], 'rel_flip_reference': X.MAN['w3']['controls']['REL-FLIP']}, indent=1, sort_keys=True))
    model_gate(); engine_gate()
    X.B, brep = make_builders({'re': re, 'math': math, 'json': json, 'parse_belief_898': parse_belief_898, 'enc899': enc899, 'geometry899': geometry899,
                               'NoRun899': NoRun899, 'tok': tok, 'PUB_TARGET': {}, 'B_FIELDS_898': B_FIELDS_898, 'sha_bytes': sha_bytes},
                              neutral900_source(SRC['899.py'].decode('utf-8')))
    R['mount_builders'] = brep
    if not brep['ok']: raise StopT896('MOUNT_BUILDER_ISOLATION %s' % brep['violations'])
    X.NSA = {r: MAN['names']['NS-A'][r] for r in X.JP['names']['order']}; X.MAX_NEW_A = X.JP['generation']['MAX_NEW']
    X.RC = ReadoutCounter(X.JP['matrix_core']['max_greedy_readouts'])
    X.LIN, X.TEXTS, X.INV, X.READ, X.READ_BY_ID, X.MEAS, X.GENS, X.STATES, X.CARDS = [], {}, [], [], {}, [], [], {}, {}
    probes = X.PF.build_probes(X.JP, 'NS-A', X.NSA); X.PF.validate_probes(probes, {'NS-A': X.NSA})
    ref = {p['id']: p['text_sha256'] for p in MAN['probes']}
    if any(ref.get(p['id']) != sha_s(p['text']) for p in probes): raise StopT896('PROBE_SET_INVALID differs from the binding PF manifest')
    X.PROBES = {pos: [p for p in probes if p['position'] == pos] for pos in ('P-last', 'P-first')}
    R.update(readouts=X.READ, generations=X.GENS, measurements=X.MEAS, lineage_rows=X.LIN, readout_limit=X.RC.limit)
    R['status'] = 'EXPERIMENT'; log('EXPERIMENT START', MARKER, '| NS-A', json.dumps(X.NSA))
    for world in ('W1', 'W2'):
        for pos in ('P-last', 'P-first'): run_state_A(world, pos)
    run_core_B(); run_w3_continuation(); run_core_C(); run_core_D()
    R['texts'] = X.TEXTS; R['w3_continuation'] = {k: {kk: vv for kk, vv in v.items()} for k, v in X.W3C.items()}
    offline_evaluation(cfg); end_gates(cfg); final_decision()


# ===================================================================================================== entry point
def main(argv=None):
    cfg = config(sys.argv[1:] if argv is None else argv)
    ensure_drive(); init_run(cfg)
    log('=' * 112); log(MARKER, '| run', RUN_ID); log('STATUS', IMPLEMENTATION_STATUS); log('DEVIATION', SECTION16_DEVIATION)
    log('SCOPE: S2-D stage 1 (NS-A). Decision = locked 709 answer() greedy only. No learning / autonomy / value-learning claim.'); log('=' * 112)
    ev('RUN_START', marker=MARKER, implementation_status=IMPLEMENTATION_STATUS)
    workdir = ROOT / 'sources'; workdir.mkdir(); rc = 1; SRC = None; rep = None
    try:
        ok, rep, J, SRC, MAN = run_cpu_gates(cfg, workdir)
        R['cpu_gates'] = rep; (ROOT / 'TEST900_gate_report.json').write_text(json.dumps(rep, indent=1, default=str))
        for k, g in rep['gates'].items():
            R['gates'][k] = {'status': g['status'], 'reason': g['failed'] or None, 'data': {}}; ev('GATE', name=k, status=g['status'])
            log('GATE', k, g['status'], '' if g['status'] == 'PASS' else '| missing/failed: %s' % g['failed'][:12])
        write_source_hashes(cfg, SRC, rep)
        if not ok:
            R.update(status='LOCKED_BEFORE_GPU', technical_verdict='NOT_RUN', scientific_verdict=None, gpu_model_loaded=False,
                     torch_imported_by_900=('torch' in sys.modules) and not TORCH_PRELOADED,
                     locked={'first_locked_gate': rep['first_locked_gate'], 'missing_or_failed': {k: g['failed'] for k, g in rep['gates'].items() if g['status'] != 'PASS'}})
            log('TEST900_LOCKED gpu_gate=LOCKED first=%s | no model load, no forge, no GPU work' % rep['first_locked_gate']); rc = 2
        else:
            gpu_main(cfg, J, SRC, MAN, rep, workdir); rc = 0 if R.get('technical_verdict') == 'PASS' else 1
    except StopT896 as e:
        R.update(status='TECHNICAL_ABORT', technical_verdict='UNDECIDABLE_TECHNICAL', scientific_verdict=None, abort=str(e)[:3000], traceback=traceback.format_exc())
        (ROOT / 'TEST900_traceback.txt').write_text(traceback.format_exc()); log('TEST900_TECHNICAL_ABORT', str(e)[:1500]); rc = 1
    except BaseException as e:
        R.update(status='INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR', technical_verdict='UNDECIDABLE_TECHNICAL', scientific_verdict=None,
                 error='%s: %s' % (type(e).__name__, str(e)[:2000]), traceback=traceback.format_exc())
        (ROOT / 'TEST900_traceback.txt').write_text(traceback.format_exc()); log('TEST900_ERROR', R['error']); rc = 1
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(); raise
    finalize_artifacts()
    return rc


if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
