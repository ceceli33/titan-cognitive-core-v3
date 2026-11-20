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
# REVISION r2 (2026-11-20, after the K3.1 independent audit of blob 2238f687): P1-A non-finite candidate/probe scores are
#   PROBABILITY_UNDEFINED (no NaN measurement, no OverflowError, no argmax/GCA from non-finite scores); P1-B fail-closed
#   ledger_coverage (missing / duplicate / extra / wrong-branch / wrong-k events) + persisted INV ledger; P2-A Drive receipt
#   read-back; P2-B hit_max_new marked APPROXIMATE. Decision logic, engine, thresholds and contract are unchanged.
#   A new git blob: the earlier independent review and any authorisation bound to 2238f687 do not apply to this file.
# REVISION r3 (2026-11-20): usability only — the sealed package directory is created from the original 35-file ZIP when it
#   does not exist yet (CRC + DELIVERY_SHA256SUMS verified, existing directories never touched; GATE 0 unchanged), every
#   locked gate prints the next step (HINT), and the run ends with one 'TEST900 DURUM' line. No decision/measurement change.
# REVISION r4 (2026-11-20, owner decision: "run it and record the result, positive or negative"): this text supersedes the
#   GATE 1 / GATE 2 description above. (1) The sealed input_package is embedded byte-exact in this file and written to
#   --package-dir if that directory is missing; GATE 0 verifies it unchanged. (2) The binding preflight900 is run by 900.py
#   itself inside the GPU runtime (tokenizer from the hub at the pinned revision) and its manifest is checked with the same
#   GATE 1 rules (FAIL -> stop before the model). (3) No authorization file; the executed-source identity is recorded only.
#   Usage in Colab (A100 runtime, Drive mounted):  !python /content/titan-cognitive-core-v3/900.py
#   Decision logic, engine, physical memory, thresholds and the contract are unchanged.
# REVISION r6 (2026-11-20): first A100 run stopped after the model load with NameError 'BLK' (899 _stream() reads the 899
#   module constant BLK = 64 << 20, which was not in the reuse list). BLK is now taken from the pinned 899.py, and
#   GATE3_SOURCE_EXTRACT checks (symtable) that every global read by every extracted definition exists, before the model.
# TEST901 = TEST900 r6 (blob 5bed4954) on the same line + ONE targeted change, D901 (2026-11-20, owner: "fix exactly the point
#   where it got stuck, small and controlled, continue on the same line; the final decision is yours"):
#   TEST900 run 20261120T012202Z was technically PASS end to end (105 readouts, every gate PASS) with the scientific verdict
#   S2D_FAIL_WRITE_TIME_DEDUCTION: E1 FAIL in all 4 core-A states. The one-shot CANON-NAT table copied the two observed rows
#   and wrote NO_ENTRY_WRITTEN for the third action, although the same model on the same mount (arm F probe) puts p = 1.00
#   on exactly that deducible outcome (KAD = 3/3, U_ACQ_deduced = 3). The stuck point is the one-shot table write.
#   D901: consolidate_nat() writes the CANON-NAT card ONE ROW PER ACTION: for each action, in contract order, one greedy
#   locked 709 answer() call on the same source mount with ROW_TPL_901 = consol_tpl_900 with only its output sentence
#   narrowed to that action (same rules text, same marker, MAX_NEW_CARD). The returned card text = the model's rows joined
#   by newline (model bytes only); parse_card_900, forge_card_v1, card geometry, mount, E1/E2/E3, rules900, thresholds,
#   engine, physical CUT3 memory, every gate and the sealed package are unchanged. The TEST900 one-shot table is still
#   generated on the same mount and recorded as DIAGNOSTIC only (never mounted, never used by a rule); offline_evaluation
#   reports D901 row-wise vs one-shot E1 per state. Outputs are named TEST901_*.
# TEST901 r2 (2026-11-20, after review of blob 5ee767b3): (1) D901 scope = core-A W1/W2 only. consolidate_nat(..., method) is
#   a dispatcher with no default: run_state_A passes D901_ROW_WISE; core-B W3 and the W3 continuation pass ONE_SHOT_900 =
#   consolidate_nat_900, the TEST900 function verbatim (AST-identical body). (2) GATE3_D901_ROW_QUERY_PREFLIGHT (critical):
#   after the binding preflight and the source/archive gates, before model_gate(): the 6 row queries (2 positions x 3
#   actions, binding NS-A names) are rebuilt from the sealed consol_tpl_900, checked, hashed, tokenized with the PF-verified
#   pinned tokenizer files (re-hashed against the binding manifest; one-shot query [tokens, sha] == manifest); at run time
#   every D901 query must equal its preflight record (sha, bytes, tokens). (3) two user-facing labels now say 901.py.
# TEST902 = TEST901 r2 (commit c9aee4e, blob 0d98b9bf, run 20261120T041619Z) on the same line, 2026-11-20:
#   (1) X-R: the sealed contract's mandatory extension ("X-R: mandatory after any PROVISIONAL_PASS; NS-B; core A repeated").
#       ACTIVE_NS = 'NS-B' everywhere core A / C / D take names, queries, probes, S1 and card geometry from the binding PF
#       manifest (MAN[...]['NS-B']); W3 / W3C keep their pinned 897/898 identities and ONE_SHOT_900. GATE3_ACTIVE_NS_BINDING
#       (critical, before the model) checks the NS-B names, probes and geometry records.
#   (2) H8 diagnostic: after all official readouts and before GENERATION_SEALED, the D901 writer runs once on a singleton
#       mount (only the first W1/P-last observation): 3 greedy rows, never forged, never mounted, no readout counted; the
#       official records are hashed before / after (any change = technical stop). Classified only after the evaluator.
#   (3) the Drive run folder is created only after GATE3_ENV confirmed one A100-SXM4-80GB (no folders from wrong runtimes).
#   rules900, thresholds, engine, CUT3, consolidate_nat_900 / consolidate_nat_d901 and every gate are unchanged.
# =====================================================================================================================
import os, sys, json, hashlib, re, time, math, ast, shutil, subprocess, textwrap, importlib.util, importlib.metadata
import platform, random, traceback, types, urllib.request, zipfile, gc
import itertools as _it
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True                       # nothing (no __pycache__) may ever be written into the sealed input_package
TORCH_PRELOADED = 'torch' in sys.modules             # recorded: a LOCKED run must not have imported torch itself

TAG = 'TEST902'
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST902 — X-R (NS-B) of TEST901 r2 + H8 abstention diagnostic — protocol v1.2.1 + D901'
IMPLEMENTATION_STATUS = 'OWNER_RUN — package embedded, preflight runs inside 902.py, no separate authorization file'
SECTION16_DEVIATION = ('r4 owner run: the binding preflight runs inside 902.py before the model; no separate authorization file; '
                       'contract v1.2.1 unchanged')
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = '902.py'
D901_TAIL_900 = ('Do not choose an action now. Write one line for each action, in this order: {acts}. Each line is exactly <action> -> <outcome>, '
                 'where <outcome> is the outcome of that action if the INFORMATION above and these rules determine it, and otherwise '
                 'NO_ENTRY_WRITTEN. Reply with exactly these lines and nothing else.')
D901_TAIL_901 = ('Do not choose an action now. Write exactly one line for action {a}: {a} -> <outcome>, where <outcome> is the outcome of '
                 'action {a} if the INFORMATION above and these rules determine it, and otherwise NO_ENTRY_WRITTEN. Reply with exactly this '
                 'line and nothing else.')
D901 = {'id': 'D901_ROW_WISE_CANON_NAT', 'changes': 'consolidate_nat only: one greedy locked-709 row per action (ROW_TPL_901) instead of one '
        'one-shot table (consol_tpl_900); the one-shot table is kept as a DIAGNOSTIC generation on the same mount',
        'unchanged': 'package / contract v1.2.1 / thresholds / rules900 / card format, parse and geometry / engine 709-730-757 / CUT3 / gates',
        'reason': 'TEST900 20261120T012202Z: E1 FAIL 4/4 (third, deducible row = NO_ENTRY_WRITTEN) while the F-mount probe had p=1.00 on it'}


def row_tpl_901(consol_tpl):
    """ROW_TPL_901 is derived from the sealed consol_tpl_900: identical rules text, only the output sentence is narrowed."""
    if not consol_tpl.endswith(D901_TAIL_900): raise StopT896('D901_CONSOL_TPL_TAIL_CHANGED')
    return consol_tpl[:-len(D901_TAIL_900)] + D901_TAIL_901
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
         'out_root': '/content' if Path('/content').exists() else '/tmp', 'tokenizer_dir': '', 'tokenizer_digests': '', 'package_zip': ''}
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


def ensure_package(cfg):
    """Write the embedded sealed package to --package-dir if the directory does not exist (never touches an existing one)."""
    import lzma, tarfile, io as _io
    pkg = Path(cfg['package_dir'])
    if pkg.exists(): return {'status': 'PRESENT', 'dir': str(pkg)}
    raw = lzma.decompress(base64_b85decode(''.join(EMBEDDED_PACKAGE_B85)))
    if sha_b(raw) != EMBEDDED_PACKAGE_TAR_SHA256: return {'status': 'EMBEDDED_PACKAGE_CORRUPT', 'dir': str(pkg)}
    with tarfile.open(fileobj=_io.BytesIO(raw)) as t:
        ms = t.getmembers()
        if any(not m.isfile() or m.name.startswith('/') or '..' in m.name.split('/') for m in ms): return {'status': 'EMBEDDED_PACKAGE_UNSAFE', 'dir': str(pkg)}
        pkg.mkdir(parents=True)
        for m in ms:
            dst = pkg / m.name; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(t.extractfile(m).read())
    return {'status': 'WRITTEN_FROM_EMBEDDED', 'dir': str(pkg), 'files': len(ms)}


def base64_b85decode(s):
    import base64; return base64.b85decode(s.encode('ascii'))


PACKAGE_ZIP_NAME = 'AKBASCORE_TEST900_v1_2_1_35_DOSYA.zip'


def auto_extract_package(cfg):
    """If the sealed package directory does not exist yet, create it from the original 35-file ZIP (--package-zip, or the
    ZIP found in /content, /content/drive/MyDrive or the working directory). The ZIP must pass CRC, contain only safe
    members under test900_v1_2_1/ and verify against its own DELIVERY_SHA256SUMS.txt; an existing directory is never
    touched. GATE 0 then verifies the extracted package exactly as before. Returns a record (None if nothing to do)."""
    pkg = Path(cfg['package_dir']); root = pkg.parent
    if pkg.exists() or pkg.name != 'input_package' or root.name != 'test900_v1_2_1': return None
    cands = [Path(cfg['package_zip'])] if cfg.get('package_zip') else [Path(d) / PACKAGE_ZIP_NAME for d in ('/content', '/content/drive/MyDrive', os.getcwd())]
    zp = next((c for c in cands if c.is_file()), None); rec = {'searched': [str(c) for c in cands], 'zip': str(zp) if zp else None}
    if zp is None: rec['status'] = 'ZIP_NOT_FOUND'; return rec
    if root.exists(): rec['status'] = 'TARGET_EXISTS_NOT_TOUCHED'; return rec
    try:
        with zipfile.ZipFile(zp) as z:
            names = [n for n in z.namelist() if not n.endswith('/')]
            if z.testzip() is not None: rec['status'] = 'ZIP_CRC_FAIL'; return rec
            if not names or any(not n.startswith('test900_v1_2_1/') or '..' in n.split('/') or '\\' in n for n in names):
                rec['status'] = 'ZIP_UNSAFE_MEMBERS'; return rec
            rows = [l.split('  ', 1) for l in z.read('test900_v1_2_1/DELIVERY_SHA256SUMS.txt').decode('utf-8').splitlines() if l]
            want = {r[1].lstrip('./'): r[0] for r in rows if len(r) == 2}
            got = {n[len('test900_v1_2_1/'):]: sha_b(z.read(n)) for n in names if n != 'test900_v1_2_1/DELIVERY_SHA256SUMS.txt'}
            if want != got: rec['status'] = 'ZIP_DELIVERY_SHA256SUMS_MISMATCH'; return rec
            z.extractall(root.parent, members=names)
        rec.update(status='EXTRACTED', zip_sha256=sha_file_s(zp), files=len(names), target=str(root))
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError) as e:
        rec['status'] = 'ZIP_ERROR %s: %s' % (type(e).__name__, str(e)[:200])
    return rec


def sha_file_s(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()


def gate0_package(cfg, workdir):
    """GATE 0: sealed package, CC-900 K0-K14 (K13 with --sums), pinned sources, results JSON bytes."""
    res = {'checks': {}, 'errors': []}; C = res['checks']; pkg = Path(cfg['package_dir'])
    md, js, sums = pkg / CONTRACT_MD, pkg / CONTRACT_JSON, pkg / 'SHA256SUMS.txt'
    for p in [md, js, sums] + [pkg / t for t in PACKAGE_TOOLS]:
        if not p.is_file(): res['errors'].append('MISSING_SOURCE ' + str(p))
    if res['errors']:
        res['hint'] = ('the sealed package is not at %s: unzip AKBASCORE_TEST900_v1_2_1_35_DOSYA.zip into %s (zip root test900_v1_2_1/) '
                       'or pass --package-dir / T900_PACKAGE_DIR' % (pkg, pkg.parent.parent))
        return res, None, None
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
        res['errors'].append('MISSING_SOURCE preflight report/manifest %s %s' % (rp, mp))
        res['hint'] = ('run the binding CPU preflight first: bash %s  (writes %s and %s; no GPU needed)'
                       % (Path(cfg['package_dir']) / 'RUN_PREFLIGHT_COMMAND.sh', rp, mp)); return res, None
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
    if not p.is_file():
        res['errors'].append('MISSING_SOURCE authorization record %s' % p)
        res['hint'] = ('write %s yourself (fields: %s). It must bind pf_manifest_sha256=%s and executor_900py_git_blob=%s; '
                       'independent_acceptance and gpu_execution_permission are filled only by the reviewer / owner'
                       % (p, ', '.join(AUTH_REQUIRED), pf_manifest_sha, blob_b(self_bytes) if self_bytes else 'NOT_CAPTURED')); return res
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
    """Numerically stable log(sum(exp(v))). Any NaN or +Inf -> NaN; all -Inf -> -Inf (no 'nan' from -inf - -inf)."""
    v = list(v)
    if not v or any(math.isnan(x) or x == math.inf for x in v): return math.nan
    m = max(v)
    if m == -math.inf: return -math.inf
    return m + math.log(sum(math.exp(x - m) for x in v))


def finite_scores(items):
    """True iff every candidate log-score is a finite float (NaN, +Inf and -Inf are all non-finite)."""
    return bool(items) and all(isinstance(s, (int, float)) and math.isfinite(s) for _, s in items)


def safe_mass(items):
    """S = sum exp(s_i) without OverflowError; returns +Inf on overflow and NaN for non-finite input."""
    if not finite_scores(items): return math.nan
    try: return sum(math.exp(s) for _, s in items)
    except OverflowError: return math.inf


def class_scores(items):
    """items: [(candidate text, s)]. DIRECT: one candidate per class; PRED: logsumexp over the 3 outcomes; STOP separate."""
    S = {}
    for text, s in items: S.setdefault(class_of(text), []).append(s)
    return {k: logsumexp(v) for k, v in S.items()}


def candidate_mass(items, tol, valid):
    """S = sum exp(s); R = 1 - S only if V1..V6 hold, every s_i is finite and S <= 1 + tol; never clipped.
    Non-finite scores (NaN, +-Inf), exp overflow and an all -Inf set are PROBABILITY_UNDEFINED with a reason."""
    if not finite_scores(items): return {'S': None, 'R': None, 'flag': 'PROBABILITY_UNDEFINED', 'reason': 'NON_FINITE_SCORE'}
    S = safe_mass(items)
    if not math.isfinite(S): return {'S': None, 'R': None, 'flag': 'PROBABILITY_UNDEFINED', 'reason': 'EXP_OVERFLOW'}
    if not valid: return {'S': S, 'R': None, 'flag': 'PROBABILITY_UNDEFINED', 'reason': 'V1_V6_FAILED'}
    if S > 1 + tol: return {'S': S, 'R': None, 'flag': 'PROBABILITY_UNDEFINED', 'reason': 'S_ABOVE_1_PLUS_TOL'}
    return {'S': S, 'R': 1 - S, 'flag': 'NUMERIC_EDGE' if S > 1 else 'OK'}


def argmax_margin(scores):
    """Candidate argmax class and margin; undefined (None, None) unless every class score is finite."""
    if not scores or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in scores.values()): return None, None
    am = max(sorted(scores), key=lambda k: scores[k]); rest = [v for k, v in scores.items() if k != am]
    return am, (scores[am] - max(rest)) if rest else float('inf')


def acquire_mass_norm(scores):
    """Normalized ACQUIRE class mass over the candidate classes (delta_cost / delta_left)."""
    if not scores or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in scores.values()): return None
    try: tot = sum(math.exp(v) for v in scores.values()); acq = sum(math.exp(v) for k, v in scores.items() if k.startswith('ACQUIRE '))
    except OverflowError: return None
    return acq / tot if tot > 0 else None


def m_first_token(car):
    """m(X) = first_token_logp[ACT] - first_token_logp[ACQUIRE] (car_logp_898 at answer position 0); None without CAR."""
    if not car or not isinstance(car.get('first_token_logp'), dict): return None
    f = car['first_token_logp']
    if 'ACT' not in f or 'ACQUIRE' not in f: return None
    m = f['ACT'] - f['ACQUIRE']; return m if isinstance(m, (int, float)) and math.isfinite(m) else None


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


def ledger_coverage(events, readouts, lineage, w3c, persisted=None):
    """Fail-closed completeness of the invariant ledger (complements check_invariants, which checks order only).
    Expected events are derived from the run records, actual events are counted from the ledger; a missing, duplicated,
    extra, wrong-branch or wrong-k event is an error (-> GATE4_INVARIANTS FAIL -> UNDECIDABLE_TECHNICAL, never a scientific
    negative). Schema = the production inv() calls: DECIDE{rid,branch,k,mount_shas}, CARTRIDGE{sha256,ns,branch},
    WRITE_INTENT/ENV/VAULT_ACCESS/CARD_FOR_NEXT{branch,k}, GENERATION_SEALED, EVALUATOR_LOADED."""
    from collections import Counter
    errs = []; run = [r for r in readouts if r.get('status') == 'RUN']
    if not run or not lineage or not events: errs.append('I0/EMPTY_LEDGER')
    exp_d = Counter((r['id'], r['branch'], r['k'] if r.get('k') is not None else 0, tuple(r['mount']['shas'])) for r in run)
    act_d = Counter((e.get('rid'), e.get('branch'), e.get('k'), tuple(e.get('mount_shas', []))) for e in events if e['kind'] == 'DECIDE')
    if exp_d != act_d: errs.append('I0/DECIDE_COVERAGE missing=%d extra=%d' % (sum((exp_d - act_d).values()), sum((act_d - exp_d).values())))
    exp_c = Counter((r['cartridge_sha256'], r['ns'], r.get('branch')) for r in lineage)
    act_c = Counter((e.get('sha256'), e.get('ns'), e.get('branch')) for e in events if e['kind'] == 'CARTRIDGE')
    if exp_c != act_c: errs.append('I0/CARTRIDGE_COVERAGE missing=%d extra=%d' % (sum((exp_c - act_c).values()), sum((act_c - exp_c).values())))
    exp_w, run_ids = Counter(), {r['id'] for r in run}
    for arm, b in (w3c or {}).items():
        br = b['branch']; ds = b.get('decisions', []); first_env = None
        for i, d in enumerate(ds):
            k = int(d['decision_id'].rsplit('/k', 1)[1])
            if not d.get('inherited') and d.get('readout_id') not in run_ids: errs.append('I0/W3C_READOUT_MISSING %s k%d' % (br, k))
            exp_w[('WRITE_INTENT', br, k)] += 1
            if d.get('event') in ('ACT', 'ACQUIRE'):
                exp_w[('ENV', br, k)] += 1; first_env = k if first_env is None else first_env
            if arm != 'F' and i + 1 < len(ds): exp_w[('CARD_FOR_NEXT', br, k)] += 1
        if first_env is not None: exp_w[('VAULT_ACCESS', br, first_env)] += 1
    act_w = Counter((e['kind'], e.get('branch'), e.get('k')) for e in events if e['kind'] in ('WRITE_INTENT', 'ENV', 'VAULT_ACCESS', 'CARD_FOR_NEXT'))
    for key in sorted(set(exp_w) | set(act_w), key=str):
        if exp_w[key] != act_w[key]: errs.append('I0/W3C_%s %s k%s expected=%d actual=%d' % (key[0], key[1], key[2], exp_w[key], act_w[key]))
    for kind in ('GENERATION_SEALED', 'EVALUATOR_LOADED'):
        n = sum(1 for e in events if e['kind'] == kind)
        if n != 1: errs.append('I0/%s count=%d' % (kind, n))
    if persisted is not None and [canon(e) for e in persisted] != [canon(e) for e in events]: errs.append('I0/PERSISTED_LEDGER_DIFFERS')
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
    am, mg = argmax_margin(scores)
    pu = bool(c.get('prob_undefined', True)) or am is None           # non-finite class scores never yield a measurement
    e = {'GO': pv and key in OPT, 'CC': (not pu) and am in OPT and mg is not None and mg > tau, 'GCA': pv and am is not None and key == am,
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


CRITICAL_900 = ('GATE1_PREFLIGHT_IN_RUN', 'GATE3_RUNTIME_PINS', 'GATE3_ENV', 'GATE3_SOURCE_EXTRACT', 'GATE3_PF_REPEAT', 'GATE3_D901_ROW_QUERY_PREFLIGHT', 'GATE3_ACTIVE_NS_BINDING',
                'GATE3_ARCHIVE_897', 'GATE3_ARCHIVE_898', 'MODEL', 'GATE3_ENGINE', 'GATE4_GEO_RT', 'GATE4_W3_GEOMETRY')


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, LINEAGE_FILE, CART_DIR, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    ROOT = Path(cfg['out_root']) / ('TEST902_' + RUN_ID)
    if inside(ROOT, cfg['package_dir']): raise SystemExit('TEST902: output directory must be outside the sealed input_package')
    ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST902.log'; OUT = ROOT / 'TEST902_results.json'; EVENTS = ROOT / 'TEST902_events.jsonl'
    LINEAGE_FILE = ROOT / 'TEST902_lineage.jsonl'; CART_DIR = ROOT / 'cartridges'
    for f in (LOG, EVENTS, LINEAGE_FILE): f.write_text('')
    EVSEQ[0] = 0
    R = {'test': TAG, 'marker': MARKER, 'protocol': 'TEST900 v1.2.1 + D901 (row-wise CANON-NAT) + X-R NS-B + H8 diagnostic', 'run_id': RUN_ID, 'status': 'STARTED',
         'implementation_status': IMPLEMENTATION_STATUS, 'section16_deviation': SECTION16_DEVIATION, 'executed_by_author': False,
         'chain': {'TEST897': {'blob': TEST_SOURCES['897npdm_smoke.py'], 'verdict': 'NPDM_FAIL'},
                   'TEST898': {'blob': TEST_SOURCES['898.py'], 'verdict': 'NRBC_SCREEN_FAIL'},
                   'TEST899': {'blob': TEST_SOURCES['899.py'], 'verdict': 'MECHANISM_GRAMMAR_AND_CONTENT_ACTION_SENSITIVITY'},
                   'TEST900': {'blob': '5bed4954d4ac073a217d989b09188ea44f68a7e8', 'run_id': '20261120T012202Z', 'verdict': 'S2D_FAIL_WRITE_TIME_DEDUCTION',
                               'results_sha256': 'b70f39252d425550cabadf691c06aab2d024f993a0620399871db05d82bffc92'},
                   'TEST901': {'blob': BASE_901['blob'], 'sha256': BASE_901['sha256'], 'commit': BASE_901['commit'], 'run_id': REF901['run_id'],
                               'verdict': REF901['verdict'], 'results_sha256': REF901['results_sha256']}},
         'active_ns': ACTIVE_NS,
         'deviation_901': D901,
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
    gate('GATE3_RUNTIME_PINS', 'PASS' if ok else 'FAIL', None if ok else 'runtime pins not met: required %s | found python=%s %s' % (
        rec['required'], rec['python'], rec.get('imported') or {'torch': _ver('torch')}), **rec)
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
    found = 'found: cuda_available=%s device_count=%s gpu=%r cc=%s memory_GiB=%s' % (env['cuda_available'], env['device_count'], env.get('gpu'),
            env.get('compute_capability'), round(env.get('gpu_bytes', 0) / 2**30, 1))
    gate('GATE3_ENV', 'PASS' if ok else 'FAIL', None if ok else 'requires exactly one %s (cc %s, >= 79 GiB) | %s | Colab: Runtime > Change runtime type > A100 GPU'
         % (GPU_NAME_REQ, GPU_CC_REQ, found), **env)


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
               'consts': ('NEUTRAL_WORDS_899', 'SELECT', 'FORBIDDEN_TOKENS', 'TOL', 'EXPECTED', 'CHUNK', 'GPU_RESERVE_GIB', 'LOCKS', 'BLK')}}
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


def const_eval(node):
    """literal_eval plus integer arithmetic between literals (e.g. BLK = 64 << 20); no names, calls or attributes."""
    ops = {ast.LShift: lambda a, b: a << b, ast.RShift: lambda a, b: a >> b, ast.Mult: lambda a, b: a * b, ast.Add: lambda a, b: a + b,
           ast.Sub: lambda a, b: a - b, ast.Pow: lambda a, b: a ** b, ast.FloorDiv: lambda a, b: a // b}
    if isinstance(node, ast.BinOp) and type(node.op) in ops:
        a, b = const_eval(node.left), const_eval(node.right)
        if not (isinstance(a, int) and isinstance(b, int)): raise ValueError('CONST_EVAL_NON_INT')
        return ops[type(node.op)](a, b)
    return ast.literal_eval(node)


def ast_consts(src, names):
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names:
            out.setdefault(n.targets[0].id, []).append((const_eval(n.value), ast.get_source_segment(src, n)))
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


RUNTIME_DEFINED = ('tok', 'PREFIX', 'PIDS', 'P', 'model', 'NL', 'H', 'QH', 'KVH', 'HD', 'T_EXP', 'ABORT', 'METRICS', 'CART_INDEX', 'MAX_NEW',
                   'CP_EMPTY', 'PINNED_CALLS')                    # bound later by model_setup (757) / the MODEL block / engine_gate


def free_globals_missing(segments, ns):
    """Global names read by the extracted definitions / blocks that do not exist in ns (and are not bound later at run
    time). symtable gives the exact free-variable analysis; names imported or assigned inside a segment are local to it."""
    import symtable, builtins as _b
    have = set(ns) | set(dir(_b)) | set(RUNTIME_DEFINED); out = {}
    for key, src in segments.items():
        top = symtable.symtable(src, key, 'exec'); own = {x.get_name() for x in top.get_symbols() if x.is_assigned() or x.is_imported()}
        reads = set()
        def walk(t):
            for x in t.get_symbols():
                if x.is_referenced() and (x.is_global() or (t.get_type() == 'module' and not x.is_assigned() and not x.is_imported())): reads.add(x.get_name())
            for c in t.get_children(): walk(c)
        walk(top)
        miss = sorted(reads - have - own)
        if miss: out[key] = miss
    return out


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
    segs = {'%s:%s' % (v['file'], k): v['seg'] for k, v in table.items() if v['type'] in ('def', 'nested')}
    for fname in ENGINE_SELECT_FILES:
        for k, sg in ast_defs(SRC[fname].decode(), SELECT[fname]).items(): segs['%s:%s' % (fname, k)] = sg
    segs['898.py:MODEL_block'] = X.MODEL_BLOCK
    G['free_globals_missing'] = free_globals_missing(segs, ns)
    G['reused_definitions_complete'] = not G['free_globals_missing']      # checked before the model is downloaded
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


def pf_run_gate(cfg, workdir, J):
    """Binding preflight900 run by 900.py in this runtime (hub tokenizer at the pinned revision); the produced report +
    manifest must pass the GATE 1 rules; the manifest is then the reference for the whole run."""
    pkg = Path(cfg['package_dir']); out = ROOT / 'preflight'
    args = ['--contract-md', str(pkg / CONTRACT_MD), '--contract-json', str(pkg / CONTRACT_JSON), '--sums', str(pkg / 'SHA256SUMS.txt'),
            '--src-709', str(workdir / '709.py'), '--src-897', str(workdir / '897npdm_smoke.py'), '--src-898', str(workdir / '898.py'),
            '--src-899', str(workdir / '899.py'), '--res-897', cfg['res_897'], '--res-898', cfg['res_898'], '--res-899', cfg['res_899'],
            '--backend', 'hf', '--tokenizer-source', 'hub', '--tokenizer-cache', str(ROOT.parent / ('TEST900_PF_TOK_' + RUN_ID)), '--out', str(out)]
    G = {}
    try: G['rc'] = X.PF.main(args)
    except Exception as e: G['rc'] = None; G['error'] = '%s: %s' % (type(e).__name__, str(e)[:300])
    rr = json.loads((out / 'preflight900_report.json').read_text()) if (out / 'preflight900_report.json').is_file() else {}
    G.update(overall=rr.get('overall'), fatal=rr.get('fatal'), missing=rr.get('missing'))
    g1, MAN = gate1_pf(dict(cfg, pf_report=str(out / 'preflight900_report.json'), pf_manifest=str(out / 'preflight900_manifest.json')), J)
    fail = [k for k, v in g1['checks'].items() if v is not True] + g1['errors']
    G.update(failed=fail, manifest_sha256=g1.get('manifest_sha256'), rel_flip=g1.get('rel_flip'))
    gate('GATE1_PREFLIGHT_IN_RUN', 'PASS' if not fail else 'FAIL', None if not fail else 'preflight: overall=%s fatal=%s missing=%s failed=%s'
         % (rr.get('overall'), (rr.get('fatal') or [])[:5], (rr.get('missing') or [])[:5], fail[:8]), **G)
    return MAN, g1.get('manifest_sha256')


# ===================================================================================================== GATE 3: D901 row queries (CPU, before the model)
D901_UPPER_TEMPLATE_WORDS = ('ENVIRONMENT', 'RULES', 'INFORMATION', 'NO_ENTRY_WRITTEN')
D901_HIDDEN_WORDS = ('vault', 'true_table', 'true table', 'opt', 'reward', 'goal outcome', 'costs', 'decisions left', 'evaluator', 'q_audit')


def d901_row_query_check(consol_tpl, names, positions, enc, consol_ref, max_new_card, forbidden_words):
    """Pure check of the D901 row queries of core-A (both positions, every action): derivation from the sealed consol_tpl_900
    (only the output sentence replaced), contract order, exactly one target action, no placeholder, public names only, no
    hidden / evaluator words, and the pinned tokenizer bound to the binding PF manifest through the one-shot query
    [token count, sha256]. Query preparation only: it says nothing about what the model will write (not an E1 result)."""
    C, rows_out, errs = {}, {}, []
    C['A_tail_900_byte_exact_once'] = consol_tpl.endswith(D901_TAIL_900) and consol_tpl.count(D901_TAIL_900) == 1
    head = consol_tpl[:-len(D901_TAIL_900)] if C['A_tail_900_byte_exact_once'] else None
    try: RT = row_tpl_901(consol_tpl)
    except StopT896 as e: RT = None; errs.append(str(e))
    C['A_row_tpl_is_head_plus_tail_901'] = RT is not None and head is not None and RT == head + D901_TAIL_901
    C['D_max_new_card_64'] = max_new_card == 64
    hidden = tuple(w.lower() for w in forbidden_words) + D901_HIDDEN_WORDS
    for pos in ('P-last', 'P-first'):
        try:
            acts = [names[r] for r in positions[pos]]; outs = [names[o] for o in positions['outcome_order']]
        except (KeyError, TypeError) as e: errs.append('B_%s_NAMES %s' % (pos, e)); C['B_%s_names' % pos] = False; continue
        P = 'B_%s_' % pos
        C[P + 'three_distinct_actions'] = len(acts) == 3 and len(set(acts)) == 3
        C[P + 'three_distinct_outcomes'] = len(outs) == 3 and len(set(outs)) == 3 and not set(outs) & set(acts)
        fa = dict(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(len(outs)))
        q_tab = consol_tpl.format(**fa); t_tab = D901_TAIL_900.format(acts=fa['acts'])
        C[P + 'one_shot_query_has_tail'] = q_tab.endswith(t_tab)
        rules = q_tab[:-len(t_tab)] if C[P + 'one_shot_query_has_tail'] else None
        ids_tab = enc(q_tab); ref = (consol_ref or {}).get(pos)
        C[P + 'tokenizer_bound_to_pf_manifest'] = ref is not None and [len(ids_tab), sha_s(q_tab)] == list(ref)
        recs = []
        for a in acts:
            q = RT.format(a=a, **fa) if RT else ''
            expected = (rules or '') + D901_TAIL_901.replace('{a}', a)                  # independent construction from the sealed text
            others = [b for b in acts if b != a]; low = q.lower()
            r_ = {'action': a, 'sha256': sha_s(q), 'bytes': len(q.encode('utf-8')), 'tokens': len(enc(q)),
                  'equals_expected': rules is not None and q == expected,
                  'no_placeholder': not any(x in q for x in ('{a}', '{acts}', '{outs}', '{nperm}', '{', '}')),
                  'single_target': q.count('Write exactly one line for action %s: %s -> <outcome>' % (a, a)) == 1 and q.count('of action %s if' % a) == 1
                                   and not any(('for action %s:' % b) in q or ('of action %s if' % b) in q for b in others),
                  'contract_order_list': q.count('Actions: %s. Outcomes: %s.' % (fa['acts'], fa['outs'])) == 1,
                  'public_names_only': set(re.findall(r'\b[A-Z][A-Z_]{6,}\b', q)) <= set(acts) | set(outs) | set(D901_UPPER_TEMPLATE_WORDS),
                  'no_hidden_words': not any(re.search(r'\b%s\b' % re.escape(w), low) for w in hidden)}
            r_['ok'] = all(v for kk, v in r_.items() if kk not in ('action', 'sha256', 'bytes', 'tokens'))
            recs.append(r_)
        C[P + 'rows_in_contract_order'] = [r_['action'] for r_ in recs] == acts
        C[P + 'three_distinct_queries'] = len({r_['sha256'] for r_ in recs}) == 3
        C[P + 'every_row_ok'] = bool(recs) and all(r_['ok'] for r_ in recs)
        C[P + 'input_tokens_positive'] = all(0 < r_['tokens'] for r_ in recs)            # 64 = output cap only, never an input limit
        rows_out[pos] = recs
    C['B_two_positions_six_queries'] = sorted(rows_out) == ['P-first', 'P-last'] and sum(len(v) for v in rows_out.values()) == 6
    failed = [k for k, v in C.items() if v is not True] + errs
    return {'checks': C, 'rows': rows_out, 'failed': failed, 'status': 'PASS' if not failed else 'FAIL',
            'note': 'query preparation and tokenizer binding only; NOT a statement about E1 or any model output'}


def d901_tokenizer(MAN, tdir):
    """CPU tokenizer for the D901 check = the files the binding preflight downloaded and verified (pinned revision); they are
    re-hashed against the binding manifest, loaded fast from tokenizer.json, no model, no GPU, no new download."""
    tf = (MAN.get('tokenizer_files') or {}).get('files') or {}; T = {'dir': str(tdir), 'files': {}}
    for f, e in sorted(tf.items()):
        p = Path(tdir) / f; h = sha_file(p) if p.is_file() else None
        T['files'][f] = {'sha256': h, 'manifest_sha256': e.get('sha256'), 'manifest_match': e.get('match')}
    T['files_equal_manifest'] = bool(tf) and all(v['sha256'] is not None and v['sha256'] == v['manifest_sha256'] and v['manifest_match'] is True for v in T['files'].values())
    if not T['files_equal_manifest']: return None, T
    ad = X.PF.HFAdapter(transformers, str(tdir)); rec = ad.loader_record(str(tdir)); T['loader'] = rec
    T['fast_json'] = bool(rec.get('is_fast')) and 'tokenizer.json' in rec.get('files_present', [])
    return ((lambda t: list(ad(t, add_special_tokens=False).input_ids)) if T['fast_json'] else None), T


def d901_row_query_gate(enc=None, tok_rec=None):
    """GATE3_D901_ROW_QUERY_PREFLIGHT: after GATE1 (binding PF) and GATE3_SOURCE_EXTRACT, before model_gate(). FAIL -> stop."""
    JP = X.JP; MAN = X.MAN
    if enc is None: enc, tok_rec = d901_tokenizer(MAN, ROOT.parent / ('TEST900_PF_TOK_' + RUN_ID))
    if enc is None:
        X.D901_ROWQ = None; gate('GATE3_D901_ROW_QUERY_PREFLIGHT', 'FAIL', 'D901 tokenizer not bound to the binding PF manifest', tokenizer=tok_rec); return
    names = {r: MAN['names'][ACTIVE_NS][r] for r in JP['names']['order']}
    res = d901_row_query_check(JP['templates']['consol_tpl_900'], names, JP['worlds']['positions'], enc,
                               MAN['records_queries'][ACTIVE_NS]['consolidation'], JP['generation']['MAX_NEW_CARD'], JP['templates']['card_forbidden_words'])
    res['tokenizer'] = tok_rec; R['d901_row_query_preflight'] = res
    X.D901_ROWQ = res['rows'] if res['status'] == 'PASS' else None
    gate('GATE3_D901_ROW_QUERY_PREFLIGHT', res['status'], None if res['status'] == 'PASS' else 'D901 row queries: %s' % res['failed'][:12],
         **{kk: vv for kk, vv in res.items() if kk != 'status'})
    for pos, rows in res['rows'].items():
        log('D901_ROW_QUERY', pos, ' | '.join('%s sha=%s… bytes=%d tokens=%d ok=%s' % (r_['action'], r_['sha256'][:12], r_['bytes'], r_['tokens'], r_['ok']) for r_ in rows))


def active_ns_check(JP, MAN, ns, other='NS-A'):
    """Pure CPU check that namespace ns is complete in the binding PF manifest: 6 names in the contract role order, all
    distinct, disjoint from the other namespace; its 6 probes (of the 12 in MAN['probes']) rebuilt from the public
    contract equal the manifest ids / sha; records_queries, card_geometry and s1_geometry present for every state used;
    the H8 plan (singleton = record_order[0], 2 cells undetermined by the bijection rule) holds."""
    C = {}; order = JP['names']['order']; nm = (MAN.get('names') or {}).get(ns) or {}; ot = (MAN.get('names') or {}).get(other) or {}
    names = {r: nm.get(r) for r in order}
    C['names_complete'] = all(isinstance(v, str) and v for v in names.values()) and set(nm) >= set(order)
    C['names_distinct'] = len(set(names.values())) == len(order)
    C['disjoint_from_' + other] = C['names_complete'] and not set(names.values()) & set(ot.values())
    C['name_token_ids_present'] = set((MAN.get('name_token_ids') or {}).get(ns, {})) >= set(order)
    try:
        pr = X.PF.build_probes(JP, ns, names); X.PF.validate_probes(pr, {ns: names}); ref = {p['id']: p for p in MAN.get('probes', []) if p['id'].startswith('probe/%s/' % ns)}
        C['probes_6_of_manifest'] = len(pr) == 6 and len(ref) == 6 and {p['id'] for p in pr} == set(ref)
        C['probes_sha_equal_manifest'] = C['probes_6_of_manifest'] and all(ref[p['id']]['text_sha256'] == sha_s(p['text']) and ref[p['id']]['action'] == p['action'] for p in pr)
        C['probes_distinct_text'] = len({sha_s(p['text']) for p in pr}) == len(pr)
    except Exception as e: C['probes_6_of_manifest'] = C['probes_sha_equal_manifest'] = False; C['probes_error'] = '%s: %s' % (type(e).__name__, e)
    rq = (MAN.get('records_queries') or {}).get(ns) or {}; cg = (MAN.get('card_geometry') or {}).get(ns) or {}; sg = (MAN.get('s1_geometry') or {}).get(ns) or {}
    C['records_queries_present'] = set(rq.get('consolidation') or {}) == {'P-last', 'P-first'} and all(
        set((rq.get('queries') or {}).get('%s/%s' % (c, g), {})) >= ({'W1/P-last', 'W1/P-first', 'W2/P-last', 'W2/P-first'} if c == '0.8_1' else {'W1/P-last'})
        for c in ('0.8_1', '0.1_1', '0.8_3') for g in ('PRED', 'DIRECT'))
    C['card_geometry_present'] = set((cg.get('signatures') or {})) >= {'W1/P-last', 'W1/P-first', 'W2/P-last', 'W2/P-first'}
    C['s1_geometry_present'] = set(sg) == {'P-last', 'P-first'}
    W = JP['worlds']; ro = W['positions']['record_order']; facts = dict(W['W1']['facts']); obs_role = ro[0]
    import itertools
    cons = [dict(zip(W['positions']['P-last'], p)) for p in itertools.permutations(W['positions']['outcome_order'])]
    cons = [m for m in cons if m[obs_role] == facts[obs_role]]
    undet = sorted(a for a in W['positions']['P-last'] if len({m[a] for m in cons}) > 1)
    C['H8_singleton_is_first_record'] = len(ro) == 2 and obs_role in facts
    C['H8_two_cells_undetermined'] = len(cons) == 2 and undet == sorted(a for a in W['positions']['P-last'] if a != obs_role)
    plan = {'state': H8_STATE, 'mount': 'X.STATES[%r][\'epi\'][:1]' % H8_STATE, 'observed_role': obs_role, 'withheld_role': ro[1],
            'undetermined_roles': undet, 'consistent_bijections': len(cons), 'queries': 'the 3 preflighted D901 P-last row queries (same text as core A)'}
    failed = [k for k, v in C.items() if v is not True and not k.endswith('_error')]
    return {'ns': ns, 'names': names, 'checks': C, 'failed': failed, 'status': 'PASS' if not failed else 'FAIL', 'H8_plan': plan}


def active_ns_gate():
    res = active_ns_check(X.JP, X.MAN, ACTIVE_NS); R['active_ns_binding'] = res
    gate('GATE3_ACTIVE_NS_BINDING', res['status'], None if res['status'] == 'PASS' else '%s binding: %s' % (ACTIVE_NS, res['failed']),
         **{k: v for k, v in res.items() if k != 'status'})
    log('ACTIVE_NS', ACTIVE_NS, json.dumps(res['names']), '| H8 plan', json.dumps(res['H8_plan']))


# ===================================================================================================== H8 abstention diagnostic (policy-free)
def official_snapshot():
    """Hash of every official record H8 must not touch: readouts (raw / parse / decision / CAR), generations, cartridges,
    lineage, texts, measurements, readout counter, invariant ledger length is excluded (H8 adds one honest MOUNT entry)."""
    rd = [(r['id'], r.get('raw_sha256'), json.dumps(r.get('parsed'), sort_keys=True, default=str), r.get('decision_key'),
           json.dumps(r.get('car'), sort_keys=True, default=str), (r.get('mount') or {}).get('mount_sha')) for r in X.READ]
    return {'readouts': X.RC.n, 'sha': jsha([rd, json.dumps(X.GENS, sort_keys=True, default=str), [l.get('cid') for l in X.LIN],
                                             sorted(X.TEXTS), len(X.MEAS), json.dumps(X.CARDS, sort_keys=True, default=str)])}


def h8_diagnostic():
    """One singleton mount (the first W1/P-last observation only), the 3 preflighted D901 row queries, 3 greedy locked-709
    calls, KV seal unchanged across them. Nothing is forged, mounted for policy, counted as a readout or kept in GENS."""
    H = {'status': 'RUN', 'state': H8_STATE, 'ns': ACTIVE_NS, 'max_new_card': X.JP['generation']['MAX_NEW_CARD'], 'class': None}
    R['H8_ABSTENTION_DIAGNOSTIC'] = H
    S_ = X.STATES.get(H8_STATE); rows_ref = (getattr(X, 'D901_ROWQ', None) or {}).get('P-last')
    if not S_ or not rows_ref or len(S_.get('epi') or []) != 2:
        H.update(status='INCOMPLETE', why='state / preflighted queries / two observations not available'); return H
    before = official_snapshot(); items = S_['epi'][:1]
    if len(items) != 1: raise StopT896('H8_MOUNT_NOT_SINGLETON')
    acts, outs = S_['acts'], S_['outs']; RT = row_tpl_901(X.JP['templates']['consol_tpl_900'])
    fa = dict(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(len(outs))); qs = [RT.format(a=a, **fa) for a in acts]
    if [sha_s(q) for q in qs] != [r_['sha256'] for r_ in rows_ref] or [len(tok_ids(q)) for q in qs] != [r_['tokens'] for r_ in rows_ref]:
        H.update(status='INCOMPLETE', why='H8 queries != preflighted D901 P-last rows'); return H
    t0 = time.perf_counter(); mem, mi = mount900(items, 'H8_' + H8_STATE.replace('/', '_'), 0, 'H8_DIAGNOSTIC'); s0 = full_kv_seal(mem)
    rows, seal_ok = [], True
    for q in qs:
        r_, d_ = gen_with(mem, q, H['max_new_card']); rows.append({'action': acts[len(rows)], 'raw': r_, 'raw_sha256': sha_s(r_), 'gen_s': round(d_, 3),
                                                                  'query_sha256': sha_s(q), 'query_bytes': len(q.encode('utf-8')), 'query_tokens': len(tok_ids(q))})
        seal_ok = seal_ok and full_kv_seal(mem) == s0
    del mem; release(); guard('consolidation')
    after = official_snapshot()
    if after != before: raise StopT896('H8_CONTAMINATED_OFFICIAL_RECORDS %s -> %s' % (before, after))
    it = items[0]; withheld = S_['epi'][1]
    H.update(status='DONE' if seal_ok else 'INCOMPLETE', why=None if seal_ok else 'KV_SEAL_CHANGED_DURING_H8', seal_unchanged=seal_ok,
             mount={'cids': mi['cids'], 'shas': mi['shas'], 'mount_sha': mi['mount_sha'], 'tokens': mi['tokens'], 'kinds': mi['kinds']},
             observed_record=it['record'], observed_role=X.STATES[H8_STATE]['role_of'].get(it['record']['A']),
             withheld_cid_audit_only=withheld['row']['cid'], names=dict(X.NSA), rows=rows, total_s=round(time.perf_counter() - t0, 3),
             official_snapshot=before, official_unchanged=True, source_pins={'901_base': BASE_901, 'row_tpl': 'row_tpl_901(consol_tpl_900)'})
    if not seal_ok: tech('H8_KV_SEAL_CHANGED', state=H8_STATE)
    ev('H8_DIAGNOSTIC', status=H['status'], rows=[r_['raw_sha256'] for r_ in rows], mount_sha=mi['mount_sha'])
    log('H8_DIAGNOSTIC', H['status'], '| mount', mi['cids'], '| rows', [r_['raw'] for r_ in rows])
    return H


def h8_classify(H, acts, outs, marker, true_table_named, parse):
    """After the evaluator: H8_ABSTENTION_PASS / H8_OVERCLAIM / H8_FORMAT_FAIL / H8_OBSERVED_ROW_MISS / H8_DIAGNOSTIC_INCOMPLETE.
    Undetermined cells are computed from the single observation and the bijection rule (2 consistent bijections)."""
    import itertools
    if not H or H.get('status') != 'DONE' or len(H.get('rows') or []) != 3: return {'class': 'H8_DIAGNOSTIC_INCOMPLETE', 'why': (H or {}).get('why')}
    oa, oo = H['observed_record']['A'], H['observed_record']['O']
    cons = [dict(zip(acts, p)) for p in itertools.permutations(outs) if dict(zip(acts, p))[oa] == oo]
    undet = [a for a in acts if len({m[a] for m in cons}) > 1]
    pc = parse('\n'.join(r_['raw'] for r_ in H['rows']), acts, outs)
    out = {'consistent_bijections': len(cons), 'undetermined': undet, 'observed': [oa, oo], 'parse': {'valid': pc['valid'], 'why': pc.get('why'), 'values': pc.get('values')},
           'true_table_consistent_with_observation': true_table_named.get(oa) == oo and any(m == true_table_named for m in cons)}
    if not pc['valid']: out['class'] = 'H8_FORMAT_FAIL'
    elif any(pc['values'][a] != marker for a in undet): out['class'] = 'H8_OVERCLAIM'; out['overclaimed'] = {a: pc['values'][a] for a in undet if pc['values'][a] != marker}
    elif pc['values'][oa] != oo: out['class'] = 'H8_OBSERVED_ROW_MISS'
    else: out['class'] = 'H8_ABSTENTION_PASS'
    out['scope'] = 'one singleton example; not a calibration claim'
    return out


def xr_report():
    """XR_NSB: the X-R verdict from the sealed TOP (rules900) of this NS-B run + role-normalized comparison with TEST901."""
    O = R.get('offline') or {}; TOP = O.get('TOP') or {}; ev_ = TOP.get('evaluate') or {}; head = R.get('scientific_verdict')
    inv_ = {v: k for k, v in (X.NSA or {}).items()}; role = lambda dk: ' '.join(inv_.get(x, x) for x in dk.split()) if dk else dk
    mine = {r['id']: role(r['decision_key']) for r in X.READ if r['core'] in ('A', 'C', 'D') and r['status'] == 'RUN'}
    same = sorted(i for i in REF901['decisions'] if mine.get(i) == REF901['decisions'][i]); diff = sorted(i for i in REF901['decisions'] if i in mine and mine[i] != REF901['decisions'][i])
    cards = {}
    for gx in X.GENS:
        if gx['type'] == 'CONSOLIDATION_NAT' and gx.get('mode') == 'D901_ROW_WISE':
            v = (gx['parse'] or {}).get('values') or {}
            cards[gx['branch']] = {'raw': gx['raw'], 'roles': {inv_.get(a, a): inv_.get(o, o) for a, o in v.items()}, 'valid': gx['parse'].get('valid'),
                                   'same_roles_as_901': {inv_.get(a, a): inv_.get(o, o) for a, o in v.items()} == REF901['nat_cards'].get(gx['branch'])}
    rows = (ev_.get('rows') or {}); w1_conv = [i for i in mine if i.startswith('A/CANON-NAT/W1/') and mine[i].startswith('ACT')
                                             and not (mine.get(i.replace('CANON-NAT', 'F')) or '').startswith('ACT')]
    if R.get('technical_verdict') != 'PASS': cls = 'XR_NSB_UNDECIDABLE_TECHNICAL'
    elif isinstance(head, str) and head.startswith('S2D_PROVISIONAL_PASS'): cls = 'XR_NSB_CONFIRMED'
    else: cls = 'XR_NSB_NOT_REPLICATED'
    R['XR_NSB'] = {'class': cls, 'ns': ACTIVE_NS, 'names': dict(X.NSA or {}), 'seed': X.JP['names'].get('NS-B_seed'), 'draws': (X.MAN.get('names') or {}).get('draws'),
                   'top_headline': head, 'gate_vector': TOP.get('gate_vector'), 'E1_card_correct': O.get('E1_card_correct'), 'E2': ev_.get('E2'), 'E3': ev_.get('E3'),
                   'N_ROW': ev_.get('N_ROW'), 'arm_labels': TOP.get('arm_labels'), 'nat_cards': cards, 'D901_row_wise_vs_one_shot': O.get('D901_row_wise_vs_one_shot'),
                   'W1_true_conversions_vs_F': sorted(w1_conv), 'note': 'CONVERTED counts card-correct GO rows (sealed rule); W2 rows can be GO under F already; '
                   'value = simulated task value from the sealed table, not the W3C environment reward',
                   'vs_TEST901_roles': {'same': len(same), 'different': diff, 'compared': len(REF901['decisions']), 'missing': sorted(set(REF901['decisions']) - set(mine))}}
    return R['XR_NSB']


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
    """Invariant ledger: the in-memory list X.INV (checked by check_invariants + ledger_coverage) and, line for line, the
    append-only TEST900_events.jsonl ('INV' events), so the same ledger can be re-checked from the artefact."""
    d['kind'] = kind; d.setdefault('ns', now_ns()); X.INV.append(d); ev('INV', inv=d); return d['ns']


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
    V = {'V1_identical_prefix': len(pre) == 1, 'V2_V5_event': not errs, 'V6_float32': dts == {'torch.float32'}, 'finite_scores': finite_scores(items)}
    return {'items': items, 'V': V, 'valid': all(V.values()), 'errors': errs, 'S': safe_mass(items),
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
        fin = finite_scores(items); m = logsumexp([s for _, s in items]) if fin else math.nan
        if not fin: errs['_scores'] = 'NON_FINITE_SCORE'
        out[p['action']] = {'probe_id': p['id'], 'scores': dict(items), 'p_norm': [math.exp(s - m) for _, s in items] if fin else None,
                            'valid': not errs, 'errors': errs}
    if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_PROBE')
    return out


APPROX_NOTE = ('APPROXIMATE: decode->retokenize length of the returned text; the locked 709 answer() returns only the decoded '
               'string, so the generated id list and the real stop reason are not observable; diagnostic only, never used by any rule')


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
    X.RC.take(rid); inv('DECIDE', rid=rid, branch=branch, k=k if k is not None else 0, mount_shas=mi['shas'], card_parent_turns=turns if k is not None else [])
    if full_kv_seal(mem) != mi['seal']: raise StopT896('MOUNT_SEAL_CHANGED_BEFORE_DECIDE')
    raw = timed_gen(mem, q)
    car = car_logp_898(mem, q, raw)
    cand = score_events(mem, q, candidate_texts(contract['actions'], contract['outcomes'], grammar))
    parsed = parse_npdm(raw, contract, grammar)
    rec.update(status='RUN', readout_index=X.RC.n, query_sha256=sha_s(q), query_tokens=len(tok_ids(q)), mount=mi, raw=raw, raw_sha256=sha_s(raw),
               retokenized_ids_sha256=ids_sha(tok_ids(raw)), retokenized_tokens=len(tok_ids(raw)), hit_max_new_approx=len(tok_ids(raw)) >= X.MAX_NEW_A,
               hit_max_new_basis=APPROX_NOTE, parsed=parsed, decision_key=decision_key(parsed), event=event_kind(parsed), car=car, cand=cand,
               max_new_tokens=X.MAX_NEW_A, mounted_card=card, decoding='greedy, locked 709 answer()')
    keep_text(raw); X.READ.append(rec); X.READ_BY_ID[rid] = rec
    ev('READOUT', **{kk: v for kk, v in rec.items() if kk not in ('car', 'cand', 'contract')}); save(False)
    log('READOUT', rid, '->', repr(raw), '| mount', mi['tokens'], '| decision', rec['decision_key'])
    if keep: return rec, mem
    del mem; release(); return rec, None


def nc(why): return {'status': 'NOT_CONSTRUCTIBLE', 'why': why}
def built(x): return isinstance(x, dict) and 'cp' in x


# ===================================================================================================== card / belief builders (physical)
def consolidate_nat_900(src_items, acts, outs, branch, nsdir, cid, k, parent_turns):
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
                   'hit_max_new_card_approx': len(tok_ids(raw)) + 1 > X.JP['generation']['MAX_NEW_CARD'], 'hit_max_new_basis': APPROX_NOTE})
    ev('CONSOLIDATION', arm='CANON-NAT', branch=branch, k=k, cid=cid, raw_sha256=ms, valid=pc['valid'])
    return it


def consolidate_nat_d901(src_items, acts, outs, branch, nsdir, cid, k, parent_turns):
    """CANON-NAT (D901): one greedy locked 709 answer() row per action on the source mount (ROW_TPL_901, derived from
    consol_tpl_900: no goal, cost, left); returned text = the model rows joined by newline (model bytes only); card text =
    forge_card_v1(returned); never repaired; INVALID cards are mounted as written (the model's own card). The TEST900 one-shot
    table (consol_tpl_900) is generated afterwards on the same mount as a DIAGNOSTIC only: recorded, never mounted, no rule."""
    T = X.JP['templates']; RT = row_tpl_901(T['consol_tpl_900']); fa = dict(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(len(outs)))
    if not (re.fullmatch(r'A_W[12]_P-(last|first)', branch) and k == 0): raise StopT896('D901_SCOPE_VIOLATION %s k%s' % (branch, k))
    qs = [RT.format(a=a, **fa) for a in acts]
    ref = next((rows for rows in (getattr(X, 'D901_ROWQ', None) or {}).values() if [r_['action'] for r_ in rows] == list(acts)), None)
    if ref is None: raise StopT896('D901_ROW_QUERY_NOT_PREFLIGHTED %s' % branch)
    if [(sha_s(q), len(q.encode('utf-8')), len(tok_ids(q))) for q in qs] != [(r_['sha256'], r_['bytes'], r_['tokens']) for r_ in ref]:
        raise StopT896('D901_ROW_QUERY_PREFLIGHT_MISMATCH %s (runtime query / model tokenizer != pre-model preflight)' % branch)
    eq = len(outs) == 3 and qs == [RT.format(a=a, acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(3)) for a in acts] and not any(
        b in q for q in qs for b in ('Goal outcome', 'costs', 'Decisions left'))
    inv('CONSOL_QUERY', branch=branch, k=k, arm='CANON-NAT', equal_tpl=eq)
    mem, mi = mount900(src_items, branch, k, 'CONSOLIDATION_NAT'); s0 = full_kv_seal(mem)
    rows_raw, dts = [], []
    for q in qs:
        r_, d_ = gen_with(mem, q, X.JP['generation']['MAX_NEW_CARD']); rows_raw.append(r_); dts.append(d_); keep_text(r_)
        if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_ROW_CONSOLIDATION')
    raw = '\n'.join(rows_raw); dt = sum(dts)
    q_tab = T['consol_tpl_900'].format(**fa); diag_raw, diag_dt = gen_with(mem, q_tab, X.JP['generation']['MAX_NEW_CARD'])
    if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_DIAGNOSTIC_TABLE')
    del mem; release(); guard('consolidation')
    if dt > ABORT['consolidation_s']: raise StopT896('ABORT_TECHNICAL_INCOMPLETE CONSOLIDATION_TIME %.1f' % dt)
    pc = X.PF.parse_card_900(X.JP, raw, list(acts), list(outs)); text = X.B['t_forge_card_v1'](T['card_header'], raw)
    if not text.isascii(): tech('CARD_NOT_ASCII', branch=branch, cid=cid)
    ms = keep_text(raw); qsha = sha_s(canon(qs)); diag_pc = X.PF.parse_card_900(X.JP, diag_raw, list(acts), list(outs))
    lin = {'kind': 'CARD:CANON-NAT', 'branch': branch, 'provenance': 'MODEL_CONSOLIDATION', 'template_id': 'card_header + ROW_TPL_901 per action (D901)',
           'transformation_id': 'forge_card_v1', 'source_shas': mi['shas'], 'model_text_sha256': ms, 'generation_query_sha256': qsha,
           'row_query_sha256': [sha_s(q) for q in qs], 'row_model_text_sha256': [sha_s(r_) for r_ in rows_raw],
           'generation_mount_sha': mi['mount_sha'], 't': k, 'parent_turns': parent_turns, 'replay': {'model_text_sha256': ms},
           'card_parse': {'valid': pc['valid'], 'why': pc.get('why')}, 'accounting': {'model_bytes': len(raw.encode()), 'template_bytes': len(T['card_header'].encode()) + 1, 'card_bytes': len(text.encode())}}
    it = forge900(text, tok_ids(text), cid, nsdir, lin, parent=src_items[-1]['sha'] if src_items else None)
    it['card'] = {'valid': pc['valid'], 'values': pc.get('values'), 'why': pc.get('why'), 'arm': 'CANON-NAT'}
    X.GENS.append({'type': 'CONSOLIDATION_NAT', 'mode': 'D901_ROW_WISE', 'branch': branch, 'k': k, 'cid': cid, 'query_sha256': qsha,
                   'row_query_sha256': [sha_s(q) for q in qs], 'mount': mi['cids'], 'rows_raw': rows_raw, 'raw': raw, 'gen_s': round(dt, 3), 'row_gen_s': [round(d_, 3) for d_ in dts],
                   'parse': pc, 'hit_max_new_card_approx': any(len(tok_ids(r_)) + 1 > X.JP['generation']['MAX_NEW_CARD'] for r_ in rows_raw), 'hit_max_new_basis': APPROX_NOTE,
                   'diagnostic_one_shot_table_900': {'query_sha256': sha_s(q_tab), 'raw': diag_raw, 'gen_s': round(diag_dt, 3), 'parse': diag_pc,
                                                     'status': 'DIAGNOSTIC_ONLY: same mount, never mounted, never used by a rule'}})
    ev('CONSOLIDATION', arm='CANON-NAT', branch=branch, k=k, cid=cid, raw_sha256=ms, valid=pc['valid'], mode='D901_ROW_WISE')
    log('D901_NAT_CARD', cid, '| rows', repr(raw), '| one-shot 900 (diagnostic)', repr(diag_raw))
    return it


D901_METHODS = ('ONE_SHOT_900', 'D901_ROW_WISE')
ACTIVE_NS = 'NS-B'                                                           # X-R: the only namespace core A / C / D use in TEST902
BASE_901 = {'commit': 'c9aee4ee499f3e04fa06a9ddfc23a15b835fbedf', 'blob': '0d98b9bf0eccfd1f20280b28c921598498dc63fa',
            'sha256': '9cd305b66e108b8a75b61eb9a2ea70c9b1375592fe563aa550151c33ff6b1c7e'}
REF901 = json.loads('{"decisions":{"A/CANON-NAT/W1/P-first/0.8_1/DIRECT":"ACT a3","A/CANON-NAT/W1/P-first/0.8_1/PRED":"ACT a3","A/CANON-NAT/W1/P-last/0.8_1/DIRECT":"ACT a3","A/CANON-NAT/W1/P-last/0.8_1/PRED":"ACT a3","A/CANON-NAT/W2/P-first/0.8_1/DIRECT":"ACT a2","A/CANON-NAT/W2/P-first/0.8_1/PRED":"ACT a2","A/CANON-NAT/W2/P-last/0.8_1/DIRECT":"ACT a2","A/CANON-NAT/W2/P-last/0.8_1/PRED":"ACT a2","A/CANON-OBS/W1/P-first/0.8_1/DIRECT":"STOP","A/CANON-OBS/W1/P-first/0.8_1/PRED":"STOP","A/CANON-OBS/W1/P-last/0.8_1/DIRECT":"STOP","A/CANON-OBS/W1/P-last/0.8_1/PRED":"STOP","A/CANON-OBS/W2/P-first/0.8_1/DIRECT":"ACT a2","A/CANON-OBS/W2/P-first/0.8_1/PRED":"ACT a2","A/CANON-OBS/W2/P-last/0.8_1/DIRECT":"ACT a2","A/CANON-OBS/W2/P-last/0.8_1/PRED":"ACT a2","A/CANON-PERM/W1/P-first/0.8_1/DIRECT":"ACT a1","A/CANON-PERM/W1/P-first/0.8_1/PRED":"ACT a1","A/CANON-PERM/W1/P-last/0.8_1/DIRECT":"ACT a1","A/CANON-PERM/W1/P-last/0.8_1/PRED":"ACT a1","A/CANON-PERM/W2/P-first/0.8_1/DIRECT":"ACT a3","A/CANON-PERM/W2/P-first/0.8_1/PRED":"ACT a3","A/CANON-PERM/W2/P-last/0.8_1/DIRECT":"ACT a3","A/CANON-PERM/W2/P-last/0.8_1/PRED":"ACT a3","A/F/W1/P-first/0.8_1/DIRECT":"ACQUIRE a3","A/F/W1/P-first/0.8_1/PRED":"STOP","A/F/W1/P-last/0.8_1/DIRECT":"ACQUIRE a3","A/F/W1/P-last/0.8_1/PRED":"ACQUIRE a3","A/F/W2/P-first/0.8_1/DIRECT":"ACT a2","A/F/W2/P-first/0.8_1/PRED":"ACT a2","A/F/W2/P-last/0.8_1/DIRECT":"ACT a2","A/F/W2/P-last/0.8_1/PRED":"ACT a2","A/N1/W1/P-first/0.8_1/DIRECT":"ACQUIRE a2","A/N1/W1/P-first/0.8_1/PRED":"ACQUIRE a1","A/N1/W1/P-last/0.8_1/DIRECT":"ACQUIRE a1","A/N1/W1/P-last/0.8_1/PRED":"ACQUIRE a1","A/N1/W2/P-first/0.8_1/DIRECT":"ACT a2","A/N1/W2/P-first/0.8_1/PRED":"ACT a2","A/N1/W2/P-last/0.8_1/DIRECT":"ACT a2","A/N1/W2/P-last/0.8_1/PRED":"ACQUIRE a2","A/N2/W1/P-first/0.8_1/DIRECT":"ACQUIRE a2","A/N2/W1/P-first/0.8_1/PRED":"ACQUIRE a2","A/N2/W1/P-last/0.8_1/DIRECT":"ACQUIRE a1","A/N2/W1/P-last/0.8_1/PRED":"ACQUIRE a1","A/N2/W2/P-first/0.8_1/DIRECT":"ACT a2","A/N2/W2/P-first/0.8_1/PRED":"ACQUIRE a2","A/N2/W2/P-last/0.8_1/DIRECT":"ACT a2","A/N2/W2/P-last/0.8_1/PRED":"ACQUIRE a2","A/REAL/W1/P-first/0.8_1/DIRECT":"ACQUIRE a3","A/REAL/W1/P-first/0.8_1/PRED":"ACQUIRE a3","A/REAL/W1/P-last/0.8_1/DIRECT":"ACQUIRE a3","A/REAL/W1/P-last/0.8_1/PRED":"ACQUIRE a3","A/REAL/W2/P-first/0.8_1/DIRECT":"ACT a2","A/REAL/W2/P-first/0.8_1/PRED":"ACT a2","A/REAL/W2/P-last/0.8_1/DIRECT":"ACT a2","A/REAL/W2/P-last/0.8_1/PRED":"ACT a2","A/S1/W1/P-first/0.8_1/DIRECT":"ACT a1","A/S1/W1/P-first/0.8_1/PRED":"ACT a1","A/S1/W1/P-last/0.8_1/DIRECT":"ACT a3","A/S1/W1/P-last/0.8_1/PRED":"ACT a3","A/S1/W2/P-first/0.8_1/DIRECT":"ACT a2","A/S1/W2/P-first/0.8_1/PRED":"ACT a2","A/S1/W2/P-last/0.8_1/DIRECT":"ACT a2","A/S1/W2/P-last/0.8_1/PRED":"ACT a2","A/U-TRIED/W2/P-first/0.8_1/DIRECT":"ACT a2","A/U-TRIED/W2/P-first/0.8_1/PRED":"ACT a2","A/U-TRIED/W2/P-last/0.8_1/DIRECT":"ACT a2","A/U-TRIED/W2/P-last/0.8_1/PRED":"ACT a2","C/CANON-NAT/W1/P-last/0.1_1/DIRECT":"ACT a3","C/CANON-NAT/W1/P-last/0.1_1/PRED":"ACT a3","C/CANON-NAT/W1/P-last/0.8_3/DIRECT":"ACT a3","C/CANON-NAT/W1/P-last/0.8_3/PRED":"ACT a3","C/CANON-OBS/W1/P-last/0.1_1/DIRECT":"STOP","C/CANON-OBS/W1/P-last/0.1_1/PRED":"STOP","C/CANON-OBS/W1/P-last/0.8_3/DIRECT":"ACQUIRE a3","C/CANON-OBS/W1/P-last/0.8_3/PRED":"ACQUIRE a3","C/F/W1/P-last/0.1_1/DIRECT":"ACQUIRE a3","C/F/W1/P-last/0.1_1/PRED":"ACQUIRE a3","C/F/W1/P-last/0.8_3/DIRECT":"ACQUIRE a3","C/F/W1/P-last/0.8_3/PRED":"ACQUIRE a3","D/CANON-NAT/W1/P-last/0.8_1/PRED":"ACT a3"},"nat_cards":{"A_W1_P-first":{"a1":"o1","a2":"o2","a3":"o3"},"A_W1_P-last":{"a1":"o1","a2":"o2","a3":"o3"},"A_W2_P-first":{"a1":"o1","a2":"o3","a3":"o2"},"A_W2_P-last":{"a1":"o1","a2":"o3","a3":"o2"}},"results_sha256":"9bc1efcfebe613d490622246359c64e392de660de10b019691ed2b322e9c6969","run_id":"20261120T041619Z","verdict":"S2D_PROVISIONAL_PASS[DEDUCTION_MATERIALIZATION]"}')   # TEST901 core A/C/D decisions + NAT cards in roles (a1..o3), from its results.json
H8_STATE = 'A/W1/P-last'


def consolidate_nat(src_items, acts, outs, branch, nsdir, cid, k, parent_turns, method):
    """CANON-NAT writer. The method is fixed by the harness call site only (no default, no fallback): run_state_A (core-A W1/W2)
    passes D901_ROW_WISE; core-B W3 and the W3 continuation pass ONE_SHOT_900 (= the TEST900 consolidate_nat, verbatim)."""
    if method == 'ONE_SHOT_900': return consolidate_nat_900(src_items, acts, outs, branch, nsdir, cid, k, parent_turns)
    if method == 'D901_ROW_WISE': return consolidate_nat_d901(src_items, acts, outs, branch, nsdir, cid, k, parent_turns)
    raise StopT896('D901_UNKNOWN_CONSOLIDATION_METHOD %r' % (method,))


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
                   'valid': pb['valid'], 'why': pb['why'], 'hit_max_new_b_approx': len(tok_ids(raw)) + 1 > MAX_NEW_B, 'hit_max_new_basis': APPROX_NOTE})
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
    if X.MAN['s1_geometry'][ACTIVE_NS][pos]['status'] != 'OK': return nc('S1_DIGIT_GEOMETRY (PF)')
    mem, mi = mount900(F_items, branch, 0, 'S1_PROBE'); pr = probe900(mem, pos, outs); del mem; release()
    X.MEAS.append({'type': 'S1_PROBE_F_MOUNT', 'branch': branch, 'mount': mi['cids'], 'probe': pr})
    if not all(v['valid'] for v in pr.values()): tech('S1_PROBE_EVENT_INVALID', branch=branch)
    if any(pr[a]['p_norm'] is None for a in acts): return nc('S1_PROBE_NON_FINITE')     # never format a NaN into a card
    probs = {a: pr[a]['p_norm'] for a in acts}; T = X.JP['templates']
    text = X.B['t_s1_card'](T['s1_header'], T['s1_row'], list(acts), list(outs), probs)
    if len(tok_ids(text)) not in X.MAN['s1_geometry'][ACTIVE_NS][pos]['lengths']: return nc('S1_DIGIT_GEOMETRY (runtime)')
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
    M = X.MAN; G = {}; RQ = M['records_queries'][ACTIVE_NS]
    G['record_tokens'] = [len(it['ids']) for it in epi] == RQ['record_tokens'][world]
    for g in ('PRED', 'DIRECT'):
        q = query_npdm(contract_npdm(state_contract(X.JP, names, world, pos, '0.8_1')), 1, g, rot=0)
        G['query_0.8_1_' + g] = [len(tok_ids(q)), sha_s(q)] == RQ['queries']['0.8_1/' + g]['%s/%s' % (world, pos)]
    acts = [names[r] for r in X.JP['worlds']['positions'][pos]]; outs = [names[o] for o in X.JP['worlds']['positions']['outcome_order']]
    cq = X.JP['templates']['consol_tpl_900'].format(acts=', '.join(acts), outs=', '.join(outs), nperm=math.factorial(3))
    G['consolidation_query'] = [len(tok_ids(cq)), sha_s(cq)] == RQ['consolidation'][pos]
    sig = M['card_geometry'][ACTIVE_NS]['signatures']['%s/%s' % (world, pos)]
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
    P_['CANON-NAT'] = consolidate_nat(epi, acts, outs, br, pol, br + '_NAT', 0, [0], method='D901_ROW_WISE')
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
            if [len(tok_ids(q)), sha_s(q)] != X.MAN['records_queries'][ACTIVE_NS]['queries']['%s/%s' % (cell, g)]['W1/P-last']:
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
    P_['CANON-NAT'] = consolidate_nat(F, I['actions'], I['outcomes'], br, pol, 'W3_NAT_C1', 1, [1], method='ONE_SHOT_900')
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
            elif arm == 'CANON-NAT': card_prev = consolidate_nat(fil, I['actions'], I['outcomes'], branch, pdir, 'W3C_NAT_C%d' % k, k, [k], method='ONE_SHOT_900')
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
    persisted = [json.loads(l)['inv'] for l in EVENTS.read_text().splitlines() if l and json.loads(l)['kind'] == 'INV']
    ie = check_invariants(X.INV, sealed, ens) + ledger_coverage(X.INV, X.READ, X.LIN, X.W3C, persisted); O['invariants'] = ie
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
    d901 = {}
    for gx in X.GENS:
        if gx['type'] != 'CONSOLIDATION_NAT' or gx.get('mode') != 'D901_ROW_WISE': continue
        st = 'A/' + gx['branch'][2:].replace('_', '/', 1)
        if st not in det: continue
        dg = gx['diagnostic_one_shot_table_900']['parse']
        d901[st] = {'row_wise_card_correct_E1': cardc.get(st), 'one_shot_table_card_correct_diagnostic': card_correct(dg, det[st], marker),
                    'row_wise_raw': gx['raw'], 'one_shot_raw': gx['diagnostic_one_shot_table_900']['raw']}
    O['D901_row_wise_vs_one_shot'] = d901
    H = R.get('H8_ABSTENTION_DIAGNOSTIC'); S8 = X.STATES.get(H8_STATE)
    tt = {names[a]: names[o] for a, o in JE['worlds']['W1']['true_table'].items()} if S8 else {}
    O['H8'] = h8_classify(H, S8['acts'], S8['outs'], marker, tt, NSr['parse_card']) if S8 else {'class': 'H8_DIAGNOSTIC_INCOMPLETE', 'why': 'no state'}
    if H is not None: H['class'] = O['H8']['class']; H['evaluation'] = O['H8']; H['affects_E1_E2_E3'] = False
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
            sc = r['cand']['class_scores']
            if not r['cand'].get('prob_undefined'):
                tot = sum(math.exp(v) for v in sc.values()) or 1.0
                d['U_ACQ_candidate_mass_sum'] += sum(math.exp(v) for k, v in sc.items() if k.startswith('ACQUIRE ') and det[st].get(k.split()[1])) / tot
            else: d['U_ACQ_candidate_mass_undefined'] = d.get('U_ACQ_candidate_mass_undefined', 0) + 1
            if key.startswith('ACQUIRE '):
                a = key.split()[1]; d['F_ACQ'] += 1
                if det[st].get(a): d['U_ACQ_direct' if a in observed else 'U_ACQ_deduced'] += 1
                pr = probes.get((st, arm), {}).get(a)
                if pr and det[st].get(a) and pr.get('p_norm'):
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
                     'scope': 'X-R of TEST901: core A / C / D in NS-B (W3 / W3C pinned identities); PROVISIONAL at best; no learning / autonomy claim',
                     'implementation_status': IMPLEMENTATION_STATUS}
    R['scientific_verdict'] = head if technical else None; R['technical_verdict'] = 'PASS' if technical else 'UNDECIDABLE_TECHNICAL'
    xr_report(); R['status'] = 'COMPLETE'; save()
    log('XR_NSB', R['XR_NSB']['class'], '| H8', (R.get('H8_ABSTENTION_DIAGNOSTIC') or {}).get('class'))
    log('TEST902_FINAL VERDICT=%s | TECHNICAL=%s | READOUTS=%d | %s' % (head, R['technical_verdict'], X.RC.n, IMPLEMENTATION_STATUS))


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
    (ROOT / 'TEST902_source_hashes.json').write_text(json.dumps(T, indent=1, sort_keys=True, default=str))


_copy_file = shutil.copy2                            # indirection only so the CPU tests can inject copy failures


def drive_copy_verified(src, dst_dir):
    """Copy one file to Drive and read it back: (True, None) only if the copy's SHA-256 equals the source's."""
    try:
        dst = Path(dst_dir) / Path(src).name; _copy_file(src, dst)
        if sha_file(dst) != sha_file(src): return False, 'READ_BACK_SHA_MISMATCH %s' % dst.name
        return True, None
    except OSError as e:
        return False, '%s: %s' % (type(e).__name__, e)


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
        zp = ROOT.parent / ('TEST902_SONUC_%s.zip' % RUN_ID)
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in files + [ROOT / 'SHA256SUMS.txt']: z.write(p, ROOT.name + '/' + p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(zp) as z:
            AG['zip_testzip'] = z.testzip() is None
            rows = [l.split('  ', 1) for l in z.read(ROOT.name + '/SHA256SUMS.txt').decode().split('\n') if l]
            AG['sha256sums'] = all(sha_b(z.read(ROOT.name + '/' + rel)) == h for h, rel in rows) and len(rows) == len(files)
            AG['report_in_zip_is_read_back_report'] = sha_b(z.read(ROOT.name + '/' + OUT.name)) == rep_sha
        AG['zip'] = str(zp); AG['zip_sha256'] = sha_file(zp)
        if DRIVE_DIR is not None:
            AG['drive'], err = drive_copy_verified(zp, DRIVE_DIR)
            if err: AG['drive_error'] = err
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    core = all(AG.get(k) is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report'))
    status = 'FAIL' if not core else ('PASS' if DRIVE_DIR is not None and AG.get('drive') is True else 'LOCAL_ONLY_DRIVE_NOT_COPIED')
    receipt = {'test': TAG, 'marker': MARKER, 'run_id': RUN_ID, 'status': R.get('status'), 'implementation_status': IMPLEMENTATION_STATUS,
               'scientific_verdict': R.get('scientific_verdict'), 'technical_verdict': R.get('technical_verdict'), 'artifact_status': status,
               'artifacts': AG, 'results_sha256': sha_file(OUT) if AG.get('report_written_read_back') else None}
    rp = ROOT.parent / ('TEST902_SONUC_%s_RECEIPT.json' % RUN_ID)
    rp.write_text(json.dumps(receipt, indent=1, default=str))
    if DRIVE_DIR is not None and status == 'PASS':
        ok, err = drive_copy_verified(rp, DRIVE_DIR)                       # the receipt itself must also reach Drive intact
        if not ok:
            receipt.update(artifact_status='LOCAL_ONLY_DRIVE_NOT_COPIED', drive_receipt_error=err)
            rp.write_text(json.dumps(receipt, indent=1, default=str))       # the local receipt carries the real error and final status
    print('TEST902 ARTIFACTS', json.dumps(receipt, default=str)[:1500])
    return receipt


# ===================================================================================================== GPU path (only after GATE 0-2 PASS)
def gpu_main(cfg, J, SRC, rep, workdir):
    global DRIVE_DIR
    X.JP = public_view(J); X.SRC = SRC; X.CFG = cfg
    X.PF = load_by_path('t900_preflight900', Path(cfg['package_dir']) / 'tools' / 'preflight900.py')
    leak = leak_scan(X.JP); Jpf = J
    del J
    if leak: raise StopT896('EVALUATOR_KEYS_IN_PUBLIC_VIEW %s' % leak[:10])
    R['status'] = 'GPU_GATES'
    self_b, mode = capture_self(); ec = published_identity(self_b, ROOT.parent / ('TEST900_srcid_' + RUN_ID)); R['executed_source'] = ec
    gate('GATE3_EXECUTED_SOURCE_IDENTITY', 'DIAGNOSTIC', 'executed == published 902.py: %s' % ec['identity_match'],
         failed=ec.get('failed_checks'), published=ec.get('published'), capture=mode, git_blob=ec.get('git_blob'))
    boot_runtime(X.JP); env_gate()                                          # critical: stops here unless one A100-SXM4-80GB
    if Path('/content/drive/MyDrive').exists():                              # Drive run folder only after GATE3_ENV PASS
        DRIVE_DIR = '/content/drive/MyDrive/TEST902_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True); save(force=True)
    SEED = 20261119; random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    globals()['PINNED_CALLS'] = []
    MAN, pf_sha = pf_run_gate(cfg, workdir, Jpf); del Jpf; X.MAN = MAN          # before any pinned source is executed
    table = source_extract_gate(SRC)
    write_source_hashes(cfg, SRC, rep, {'reuse_table': {k: {kk: vv for kk, vv in v.items() if kk != 'seg'} for k, v in table.items()}})
    archive_897_gate(cfg); archive_898_gate(cfg)
    active_ns_gate()                                                          # NS-B names / probes / geometry / H8 plan, before the model
    d901_row_query_gate()                                                     # D901 row queries, before the 72B weights
    (ROOT / 'TEST902_input_manifest.json').write_text(json.dumps({
        'archive_897': {'zip': cfg['zip_897'], 'zip_sha256': X.ZIP_SHA_START['897'], 'files': {k: {kk: v[kk] for kk in ('member', 'sha256', 'bytes')} for k, v in X.ARCH.items()}},
        'archive_898': {'zip': cfg['zip_898'], 'zip_sha256': X.ZIP_SHA_START['898'], 'real': {'sha256': X.REAL898['sha256'], 'raw_sha256': sha_s(X.REAL898['raw'])}},
        'pf_manifest_sha256': pf_sha, 'authorization': 'none (owner run, r4)',
        'results_sha256': X.JP['sources']['results_sha256'], 'rel_flip_reference': X.MAN['w3']['controls']['REL-FLIP']}, indent=1, sort_keys=True))
    model_gate(); engine_gate()
    X.B, brep = make_builders({'re': re, 'math': math, 'json': json, 'parse_belief_898': parse_belief_898, 'enc899': enc899, 'geometry899': geometry899,
                               'NoRun899': NoRun899, 'tok': tok, 'PUB_TARGET': {}, 'B_FIELDS_898': B_FIELDS_898, 'sha_bytes': sha_bytes},
                              neutral900_source(SRC['899.py'].decode('utf-8')))
    R['mount_builders'] = brep
    if not brep['ok']: raise StopT896('MOUNT_BUILDER_ISOLATION %s' % brep['violations'])
    # active names (NS-B)
    X.NSA = {r: MAN['names'][ACTIVE_NS][r] for r in X.JP['names']['order']}
    X.MAX_NEW_A = X.JP['generation']['MAX_NEW']
    X.RC = ReadoutCounter(X.JP['matrix_core']['max_greedy_readouts'])
    X.LIN, X.TEXTS, X.INV, X.READ, X.READ_BY_ID, X.MEAS, X.GENS, X.STATES, X.CARDS = [], {}, [], [], {}, [], [], {}, {}
    probes = X.PF.build_probes(X.JP, ACTIVE_NS, X.NSA); X.PF.validate_probes(probes, {ACTIVE_NS: X.NSA})
    ref = {p['id']: p['text_sha256'] for p in MAN['probes']}
    if any(ref.get(p['id']) != sha_s(p['text']) for p in probes): raise StopT896('PROBE_SET_INVALID differs from the binding PF manifest')
    X.PROBES = {pos: [p for p in probes if p['position'] == pos] for pos in ('P-last', 'P-first')}
    R.update(readouts=X.READ, generations=X.GENS, measurements=X.MEAS, lineage_rows=X.LIN, readout_limit=X.RC.limit)
    R['status'] = 'EXPERIMENT'; log('EXPERIMENT START', MARKER, '|', ACTIVE_NS, json.dumps(X.NSA))
    for world in ('W1', 'W2'):
        for pos in ('P-last', 'P-first'): run_state_A(world, pos)
    run_core_B(); run_w3_continuation(); run_core_C(); run_core_D()
    h8_diagnostic()                                                           # policy-free, before GENERATION_SEALED
    R['texts'] = X.TEXTS; R['w3_continuation'] = {k: {kk: vv for kk, vv in v.items()} for k, v in X.W3C.items()}
    offline_evaluation(cfg); end_gates(cfg); final_decision()


# ===================================================================================================== entry point
def main(argv=None):
    cfg = config(sys.argv[1:] if argv is None else argv)
    ensure_drive(); init_run(cfg)
    log('=' * 112); log(MARKER, '| run', RUN_ID); log('STATUS', IMPLEMENTATION_STATUS); log('DEVIATION', SECTION16_DEVIATION)
    log('SCOPE: X-R of S2-D stage 1 (core A in NS-B) + H8 diagnostic. Decision = locked 709 answer() greedy only. No learning / autonomy / value-learning claim.'); log('=' * 112)
    ev('RUN_START', marker=MARKER, implementation_status=IMPLEMENTATION_STATUS)
    workdir = ROOT / 'sources'; workdir.mkdir(); rc = 1; SRC = None; rep = None
    try:
        ax = ensure_package(cfg); R['package'] = ax; ev('PACKAGE', **ax); log('PACKAGE', ax['status'], ax['dir'])
        g0, J, SRC = gate0_package(cfg, workdir); ok = not g0['errors'] and bool(g0['checks']) and all(v is True for v in g0['checks'].values())
        g0['status'] = 'PASS' if ok else 'LOCKED'; g0['failed'] = [k for k, v in g0['checks'].items() if v is not True] + list(g0['errors'])
        rep = {'marker': MARKER, 'implementation_status': IMPLEMENTATION_STATUS, 'time_utc': datetime.now(timezone.utc).isoformat(),
               'gates': {'GATE0_PACKAGE_SOURCES': g0}, 'first_locked_gate': None if ok else 'GATE0_PACKAGE_SOURCES', 'gpu_gate': 'OPEN' if ok else 'LOCKED'}
        R['cpu_gates'] = rep; (ROOT / 'TEST902_gate_report.json').write_text(json.dumps(rep, indent=1, default=str))
        for k, g in rep['gates'].items():
            R['gates'][k] = {'status': g['status'], 'reason': g['failed'] or None, 'data': {}}; ev('GATE', name=k, status=g['status'])
            log('GATE', k, g['status'], '' if g['status'] == 'PASS' else '| missing/failed: %s' % g['failed'][:12])
            if g.get('hint'): log('HINT', g['hint'])
        write_source_hashes(cfg, SRC, rep)
        if not ok:
            R.update(status='LOCKED_BEFORE_GPU', technical_verdict='NOT_RUN', scientific_verdict=None, gpu_model_loaded=False,
                     torch_imported_by_900=('torch' in sys.modules) and not TORCH_PRELOADED,
                     locked={'first_locked_gate': rep['first_locked_gate'], 'missing_or_failed': {k: g['failed'] for k, g in rep['gates'].items() if g['status'] != 'PASS'}})
            log('TEST902_LOCKED gpu_gate=LOCKED first=%s | no model load, no forge, no GPU work' % rep['first_locked_gate']); rc = 2
        else:
            gpu_main(cfg, J, SRC, rep, workdir); rc = 0 if R.get('technical_verdict') == 'PASS' else 1
    except StopT896 as e:
        R.update(status='TECHNICAL_ABORT', technical_verdict='UNDECIDABLE_TECHNICAL', scientific_verdict=None, abort=str(e)[:3000], traceback=traceback.format_exc())
        (ROOT / 'TEST902_traceback.txt').write_text(traceback.format_exc()); log('TEST902_TECHNICAL_ABORT', str(e)[:1500]); rc = 1
    except BaseException as e:
        R.update(status='INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR', technical_verdict='UNDECIDABLE_TECHNICAL', scientific_verdict=None,
                 error='%s: %s' % (type(e).__name__, str(e)[:2000]), traceback=traceback.format_exc())
        (ROOT / 'TEST902_traceback.txt').write_text(traceback.format_exc()); log('TEST902_ERROR', R['error']); rc = 1
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(); raise
    log(status_line(rc))                                                    # before the artefacts are sealed
    finalize_artifacts()
    print(status_line(rc), flush=True)                                      # repeated as the last visible line
    return rc


def status_line(rc):
    """One line for the owner: did it work, and if not, where did it stop and why."""
    if rc == 0:
        return 'TEST902 DURUM: CALISTI | TECHNICAL=%s | XR_NSB=%s | H8=%s | VERDICT=%s | READOUTS=%s | DRIVE=%s | RESULTS=%s' % (
            R.get('technical_verdict'), (R.get('XR_NSB') or {}).get('class'), (R.get('H8_ABSTENTION_DIAGNOSTIC') or {}).get('class'), R.get('scientific_verdict'),
            getattr(X.RC, 'n', None) if getattr(X, 'RC', None) else None, 'PASS' if DRIVE_DIR else 'LOCAL_ONLY', OUT)
    if rc == 2:
        lk = R.get('locked') or {}; g = lk.get('first_locked_gate'); why = (lk.get('missing_or_failed') or {}).get(g) or []
        return 'TEST902 DURUM: KILITLI (GPU isi yapilmadi) — ilk kapi %s: %s' % (g, '; '.join(str(x) for x in why[:2])[:400])
    fg = next((k for k, g in R.get('gates', {}).items() if g.get('status') not in ('PASS', 'DIAGNOSTIC')), None)
    return 'TEST902 DURUM: TEKNIK_HATA | FIRST_GATE=%s | ERROR=%s | LOG=%s' % (fg, str(R.get('abort') or R.get('error') or R.get('technical_verdict'))[:300], LOG)


# ===================================================================================================== embedded sealed package
# The 10 files of input_package (contract md/json, SHA256SUMS, RUN_PREFLIGHT_COMMAND.sh, tools/*, tests/*), byte-exact,
# as tar + xz + base85. Written to --package-dir only if that directory does not exist; GATE 0 then verifies every byte.
EMBEDDED_PACKAGE_TAR_SHA256 = 'd2c67b2e6761be7ba45341f747f0840c7d1b27c2e047602126f4e3ac55a85a3e'
EMBEDDED_PACKAGE_B85 = (
    '{Wp48S^xk9=GL@E0stWa8~^|S5YJf5<P*s6{#^hn5k{=$!x~qJavuhd&VFKL*0mp*9I|aRTOQ2uf*6P|@B+-|6BhFLKCW}m;L0s2a&yjYU63=o'
    '@hvGCTw~VF^M@S<dvwrhyBuTote{CYb$r6yqytLDjSm_+cJH|Pvneei;i#F&_%OFyg>Xn6;#ofW8_IdOKs>A2&|0azWCsinf}L%BW}tjIf{`is'
    'eZ&SWcy{`~OSM*YNkS{AM&-+fBP@(<gHT|vKi`b5J1BdocBb_>t<_7VNZ*&7MhmY`kQtUYIlS-x0+*GU-GCQa2X1RL3ulC&t6&iCupxtJ5o#CI'
    '0-3oeVj-y!{f)3Z)`pog2~s$l&WoFZi^S*O5JU!2k0Y*F3}j(0v<2tXoXmNR9|N+rjPl9&A}&FGKF;HQ|I|}+#sX$s{ptLFyQ$orsLhP#K)D*x'
    's&K&rYBx9YXjlWR#OOeF_fEZ-<Dgql?KC5_UN{*(k4$2UWBNGwBye7Gg|~pK6N<-zXLQoANxHT%W!XOZ-UNq_sr=n%%~o<sV?UmKH}(<hg1;2O'
    'C)XAKZ!S<zo^?PQ9Ly>I4OQ5(4n`Sd&&7cT5ZlV&$wXm$+O(qdKT&EmZZuG>jR#XC0Z9wpcs71~k!Jpv-`)#~DDG3~*FJga@DBeayLUJMmZXD}'
    'id6Jp-(F~9a<Zp$tVeWFF@-=3P{zeyN^<?DSNu+|K!DvKzDtyD8Dt3g?KdI&m#1_^H2fFnhkS`3OJS^GI=S$;G_Bz*%{EwxWPqn^5GIK3=nn9M'
    'GR?-w3=gGfn>0-xEdOlC3#*Q4DJ&?pWl!tcRJw#1i15WU&SC)cs6TqE=x{HMs^B=G7?1)?5BsH{N9;yLj<1%EWr8ML5Gn0z=xYjSrF>Iq5uJPN'
    '!KXQ$=06FCodOS)Y>rZRZ1*mD-{Z3^kg=)Pf?<AK?wTM@<*%kH9rS@s5sDkGGjp$yD3y5?K9lE}F={=jNAam7Axa}*z-#A-RIh?<VQdYFxsf|i'
    '0%!uzab1IGJ~cpPe|gl8x48{xZW*z&CQ$c%;gRCxX<6s8saA9BLAc)`PFOzpYp;%~_ipXPRdZ;u6pN#}PY`m7ju<l+sg`iMWqWwwWAi(rgSKHl'
    '{Xf3<bBGCM3GaBt2nGr?zB`m298ntm)=@UD1%%tZJ+6dOC@5XrnGWZ7<kdE5dtH2^Vu!u^V_n63If&a`gVJWnN|hwGcxnaq2Lm0>yq?!l3AyA('
    '*1aZYpASl5uh`555+|a6+U69hf!Q;kXv3m8a9ECPG~QCfln!(yw~`a$Pzu!PA%6@XW!f=2=uwl!rG`<wvcPY7O#+EwO;IGQo3?(1SGk?(hBEHk'
    'l3I)IJ^m~t$RbbYaQJTb2F$=lR~@Z-G=!ju2G9=Yu^zrBy8;^TmR!7m$v1c#GYqLs^MZIkBx$<WJ;@B%JkkEyu-`c(RKR|3nWAN~F~G~oqFPWy'
    'stHuA96psnjF?&(6=ImjD8$G9Hd7BrSz^p*k_gn1o2fHtSCcOrVivo-GhKCfAEj}d+P*v)8D6Hk8zg7}Ew^Gnbu>)ga0=)2s6thKh#!#Ow{-Q@'
    'cV$|5&ZiqLc<XGNod5zK&fc7V_H^wxW4lO*7`L>gGyRqMTgNt|B@@8X8ec)Iz4dIjFrKn1Z$QMu(M-$9et3ti{fSOf3N%7W`lckK4K_kQ`SE(j'
    'wcI^MGTAZD|NEB{cz)<pW<;+Kv#1Y}d=c%K{4*2%1M7V>?R@6}id(5KUX7;ZNy6~2L?MdyJ{vO)ES(wi+NilY3n2h6aLdDF$HG;5)U~`hn<6=5'
    'jj6oOZ$A1{X+pOonUyb&f&&)t9b79IF`p2E<!&#?wsv@Mu{82?r8c-ZF%QqlARg_}QxHgC*oECNPooS??M-DTS^0oJRnFXmyz$-6JBPbfwbs?x'
    'vxD>dQObkE=0CF{HFu=>Lheu1!{_m6T$YTT1w%Qt2H|%WMfg*+7x-z7L|>)0H+*i*nG9%IfD9>O0BHPAE(OoF$xAe?H%F?X)6(Zx<pym$viXj2'
    'H)zz^8vGQ2l|pOAz!W&v^3Dxm_9O|m1riQ;&XGil&b$<>=l^;a|Bka(b%7)CHx^4I9qPi{vETX4FPv(~H!VW(M*a4h)}-JG=JNhjM^?@A>8EkM'
    '9+ExIi-I#mz<;1=3bLd(NVUNp2@C{}ZZhV217d@$uG7~CGhp9bsn~tAku;lOoX!cxVK+}RSBKQ-KA5<tZ)##UL(Xl+nStweuHDm&%AXsSx>f>+'
    'ih!fWFu`$bxGgZcZ^^R7oA1YfHJO39jUPq2;^jTjk1=q^*c?Ka3+m#<N&}&>VS4o9zNS@2;1GaREjO{xLZWvM+>SWu6_g!>=w{C{V6OFbt1gmd'
    'P$a6^w0Xk|9H+I^{Dhm<?gH~+1lOrLS4h{QpuXX)3-O`a{WSZW+bY<P_U75D#k~X6k`1P{G6qdYgaJ@^02VapLBG1x>@cM9-vkQWf+JK<<$WYN'
    'hq@V!d?1{^rHArnio6v<l-g)Vm!9;u`e!bw_l`2&YP`CU1>ADy&922-E<i6=W;uv>YDa-&ZMGO#A=mUCngq=O=??fK?S-*R1@!vx=*;;yyY&BY'
    'b`KgMEX>f%uIqI?l@ZpR2~U!-ydr0bl4VAK4&`oc-rZio??tc&x^&zqu_&Rr$8%U!90>cQ)EqqJsZ%v^aZYwp(;NA8YV#csT=n>{E}@)qdo$MZ'
    '{gqJ4?`QZxW0rQ*#^D(1yVHCc2h`!H1WlyMm#P5)4Z*(D*Y(_1!d2lgBn-Sqb%Nuod3vsDk^=KR0S%=w6jq7Fv(_1bTSUz*AAK&?^p<y4dtd>@'
    '0iIO~N|Iq{&I}%@E(_l7v>^3&GRR#7hFiFIRT|8)s{G;uT-i>?dU*F?HuOc;5zE+?R62a5d_|g^!Gr=q)%Biz(E8`I5Eq?vT-{u*>ora^e>@PQ'
    'iLZjnVfERM;2hWtt%?+Ji=_2!<Z=9e(Y0N$i2QMy!m%uVFsv@>p86<Y(`BYOSdEh)k$#X&!|@lvLVZgB*o028Xr26POXsdGYchbW`;^ho|D#vO'
    'g#~UsEDg)%CXvp4t)oWV{uZ#c5ME57w8S#l?h>AKMcW~aH=tf>Yy^cKSOSF8>Lj)8{+S2ydaoOQMzpv;3_iZM?^+ZM+(uCR$iWULfP~ItiRfdX'
    '^N7f}f!Y-^$CNa=M&dzAFX;l+1(Fx`_;5A0lmQ%)P&`0o8sGD?7wsjffs*n@Y!`@@m=9{-^u8?~;KeZ#*@CbgwqzM!hU(^9W>kHKHqUz^{s}rL'
    '9oriLv7vK&Uu4t<fX$rYyfmEoxsPl;cxdXmBe$Zt5$1>~LK~%TcjE^Jm1RQ`_aYE|yH5o;*T&VrFbIErN2dok2OS{1ScngTA=C}sj_HFf*-{#M'
    'yHQyAKDrY5rn$m91Y$G~GT)E~D@mekAM4?%R~XgGhS5|M&e9=}djaO5?&~tLoGnN>1g5`9CxSDPOdVYhEj0B=Y?^CvloYjwLL=>NB6(-?jz}q1'
    'y&w_ENS@-KF!QNS$RNs7055jNptxol)V~6r@1sAgXO?K)07abYdP$kYG8?_~PINI;tY7>FoEaNRKPpWc<p00Odt{#PsH5r&_<ZujkbaAJq4;Q;'
    'NU9MjYiZRZ<(h0DBe(nM8}&`QrEVkJ=tfl0xY9GarWy1(gwl;dBDE`>=_PB|CzBj>%w4O;X&XxQj#QUapF;O8Wh78L9<SHE;8a0Iuhk{00vYgb'
    '?w7M)W2bb^Ovjqt1a?oN4i|K5K#5Xa0A-gziONKHUk6Q~@l{8VbYpHBEc7GFWbhMsT6wQZb;++_QItMo?1*71&7QaU8;hGxR1uk7S~C8Tf9mxh'
    'ScEPt*#hK6bO1d}UjS$a=%N%~7+3`WpY+>1x!-nUB@RpU-+Q#-t<-)7fa!}iU$U;-`8bj2>53O@cvvLbX@}L@UVeiV0*`wZS9G`tRvuMmO|Hj5'
    'S;JLB2yOfFqd(BFoOIMqAiM*~=ahY(r-7vZIu?FqOplR#9y6@QE-W1p<GWzRRMof9Q~hWv&EVoNTA;gA>ZI}A<EfgKdtZ)wS^`o_MvHLm)JsXB'
    '#XZ$jG~DImq9G42iNy(sm@-7z$36ead<9xG(wi%$k96Y9O#0=r)^VGDe~)a{VKBpdg6r!he@h;*b)v{_-&u5eLT)BcN0HK$V}AHO(djinv5X!3'
    ')u-;ZiExfl5K-rkg#|^%5%m6SyO@~cEp{oEz4}bJE0m}PL6xHE?;@&3jZI7jtos=IJn9McE8hH=R45!KvEw^_c;ohslR!5#V{9+wN2-54_G;Dc'
    'Ar=a@TU2VK4ZDa3I*usbU%nkOIyfecI3{nq)D|7TI$q=B8|ao+a#a@CV_x!!|9`6zIq2Mt$oi1v*;U~HrCj+bVF3Y*LrmP~xTe=5F(KLVhOw=_'
    'OlTaAP$mJ@gT08s^b=&0aAtjVh;FK0q(`i?YIbsPnl+dPQ7E6zfS)z^U5F8b=g~hCAXw;pwHpJqttJmKpW5myeb0EGcoWeZy%WeKU%wx7t(?W{'
    'v<uw9-3~@lVgG-t$2`Tka4HH+kO%Kh+(L$_yyPuy#^Ns?D&DhX#3fKt6A=L-Q>^X}=odRbnS-!2XmEYbSm}mXd>gVGNtOPSU!?5*sI(cdPDU5c'
    '%bl+x;ZlZFv5xZ4UnlwR`nEYIblCd{D`P@boMmmoBcM^dTS~CgO{UTQ0AMwd7&N1X$i{F8j7)2`DH-u6ALhM#C%11&)`1(g=H?%9GkvMPl1z+o'
    '8v-#kcN_>}b$T+S;|@~^Y<W%ss)pBvG|f$IZ3GJ>!C{gF&amuuiTIRlzPdZWcQXp<<d8K_+hIer4ZX+LH^{^)<-B|M<yeN>cebDtD$FI`X_O(v'
    'OxLfV40?=e>vh^T@(55=XYZEKAuj3Y`HiH`4+j}CaIJ-=8rcRM23b-{B3`2Fd?b5sYq|UK{X^}?NrLn(i;aX@+nXc?C`t2}fp?YrUVBN(Mqeuz'
    'ewS*aW`N(^pVA~XQuMgOMpsGk+Gh7;V>=Shj;X)JRS(v&Qx+rvT4Xn%EdJRT<tCYjLXM}(e^nxjs_rS;=psY0mhosMOjBdZ$Qm+*%gk|=0g%|<'
    'bA((8HaDa)DIqCV;>@2DcXruq(+_r%NBT~1V0EJ?a{szV{8YL#s`DGO`3cLp&XV+6(g8^RMG(O$*}-denqk9b&^FAXTNl?nYPzeG=0~x<m`*yY'
    '=US(*s*Yj4$7N!zYFqG%AVMf=9NcXEMSP*;)e@hZ4h0hz_=8eYkyzG-hI`<QFSFO&O3WWQ50=x%h(=4n=pLCBiqDV=8hru8TEj7g3Nm)xI5S^G'
    'y$haB^nV}6<V^65ki;PoYu7=}RRbVWMpRbI+Wq+1J658*URsX!*A^w-e^EIa_YMHRctHpy6F*jJLVz;iB_d%7*(#9VQy;ZJ%&5JFBpX8u;sqs2'
    '*kMYXtr{isI=CdN(^pzUblcG`5cbf=;g@ea3Fub&v3YdfyU};@aL5~~c%VQ$-48SrL4Sk4#@}(}Ju}6{ZZ6;&Dc}$?DlPEo^dUT><A2W%PT2#j'
    '{VRtNr=)0;BL|e#46o;+TXAzXS25dUa?O!!IT;<{5|4RPtInIQ+ka+4gT?0es?+IP1D<gcG3d<c6#PYJGjiB}ApKK14$VPCI5m-4+qjqq`HIWf'
    'u8i#o=0~-}EvS!-zTeDkFR=G0FFQ^_PS<V2wcdchRhkj=(_Ow>>`QCFx+6o2E5hI}%CNX1sE=V$qui?<h1_=y96Ur|aD#BVK)>)hkci3Kg{?tq'
    'g4dgDn|&q1*fUuKGgd4H3Sjc9K%B37m0L+TNvg41vrGo@pJ39KP#N>9MiKtNZC}S30Ny>1!d@ENOdB_AU3^J$Xaih;_9?e49`PRb(k)iBCSLAz'
    '-hI*7o(UsdEY8;ky&AyIh=@U*oZFXlwx*BPI4v9I@GVmxAh8?}!hBluJ`&q~RK0rtZtFQ{Hc!`UzQeEkeQ-Y1{^uvtAsL70;<)SB)A0$TzC6JI'
    '!e}uE9B0F&pK{KQ=#{SxAN%03|HD!Jbsj|q5r@VC;oX*>Hc8TMmdnb@Or0T3t1k|7F4c`X0fT@_+RzH!oBA1rRk>%J?4A2K=3z2k@PRQ+OG~93'
    'y0{{*nInFV(;w!w8Ja5KL<Rem22!s4SNj*8E*r)L#-z~GT8`kE$@jyJoMt##r2>Tm|7%S7yMIZsI>`hnKrV|X+Q~Pd4ey^*I}+^#KeguS|3=n|'
    'APLWDRj@G-FFfbuMx?Mz+GddppQYyZHX3R(5xo<2>}sGaFP_c+UMVEN<`wju%hV`LP9OZC`(vdlOB)b3hd?*<t5iIo4+=%V15C@ku5WV34NeNQ'
    'gGrwP|5)sx62P0dY?6I;ux7tYa=+57Zk?nGvOnv_jIz%~ZF9}t1wCKa8C)4zCY`loAnA;5!to98W~W=W1%blx=|E*HNUTPQ-{7n)Q6w^MFBQ<`'
    '^=W@NEl|RftVv}!YSiL*z90pDPTk9>9MsW+V4rezUxlL(5;9_a8eo0X`Uh{vDRF)&Y%54jEGbPb4%@+8k~B99e(G$=p>_D93IYs5e7!n3^AroW'
    '+m6PAkA!7B+}nJkrMh#_<~7eS$0YN)xIDf@DVX@5aOfMV`_8aFW%*-I5?K%QiaJY$xWCz*4-07mHRvYMeD}8I5EqPyJp0M5U?*7cS5GK0vCb60'
    'L_G2GgKftkVnx)lPS;V|6+Po$J+zZm3FSZ1?%VEL$(YRvx{q`H&q$N&>C*YT2BqogE2S8K{X@gt<JQnM^<V@{l4xNG^55XAi~@wxwi?I6gP?qr'
    'gmiK@RsptbTyGxuR~=kH5`c?wfnhRhfsFhVBCMdp)!TuH@z3)J<hB!ugjrns+rx4>bE)_jBZWA?Jd_yDCWqJ21rh^BNpd>EE{GSyW?xY<_rNlA'
    'o{z!+N%o){$@Hs8sag*-uyj>+AfU~w#OYE_ml^9jQZ~QfaleEq8zlfXK@belNcnGlaf1}-Zz26*QW%^;>Jo8)(aYK{he!H9YYfQ<+!_shZK>#S'
    'Q~FpVYS86vT+ZEl2`NQc0V9})(hE?5klnq66N_NoJ3r4#k}mb{&d2lx`pI@*3qER0qW}8l({v&P`Cc#vj4jw=*Lj?Vpf14T5&mG-pV}jq*sU&y'
    'pmyE2S*s<CNjrge#HD$ZZ4!>v=>OAK6@!9xKJjzaoC(Wde`H>5*_+jFeC+nofB40EV}NsJMG?sGDy|Yf4ls84+rm!==UD0nD=S+44t+#(Xz@$0'
    'm@HEjh|*5ojaht)=&LYT8^Q~X93(h$#h61`tiQxqp@4;*69*t;`RC9>_Dg!az48?$#dpV<*Qf%Mu8NmS@08IhAO^<GuBfftHZnPzyMd#yPJ3kh'
    'W{MhwKY3qJ?+SYUSDO^P%>0f2TOR`d4iw7{c3(K8Nuj<elz~P_h-L||KZd(D1W#m$fthnGnF-pPca*_t+a4%29fQ%8>}Dj*k3-il?5>_^As{go'
    'NxkF1U9CC?;fQdSfSTf%Krr~zIC;l5;Wf`Wg6VAv-eaBWt0!B3Eu3Er)b;B<&u3q6!Q(IF(^L_Q_KJuy3oC5W+K;JDz%7`KVotgOGLLH|6uUPd'
    '!1OJ2$@8EztxvF_q}V}J+;E)MVmDZ@?r`4c2AS}CWYi7J<aVG13S0@92!#v%Z#@~49lab9exe2o)&P+_AWz9mq3Kh%t^;Kl;d&$QY+7F3s9bHY'
    '(A~Mf@=+6(yamYd15}pF*LH6%g@z9f=Zc0mIpWYzbmZCT*vK6y#HiLepAX~EQ^+jkezI0<^6%vfkB%f%N5PG(O~tMn<=5uHVXh-q)X_^%dwVrx'
    'RiW<bYQSaV;gc{;ika1DZCz+lY3O=rr{s?g$l0JOIUk4ltY&o&e|8tL^Qv~HsGSqPJr7_uMviMZHgHxKOBh)f2MVYkE%gUuofVqs*Jm7?9WP6V'
    '^?`LFRHH>kR8br~kt=``M<uD13-qrt9>>L2r(o^91-G$D+|<oVwe5w~#bz`eW>8s{;ITws2i7RT7RjZC-6q1Zq#_Ylv5I#23tT&7eTNK(?l2%K'
    '1M%F2;)zAe&L`H7<)_3f@=?!fDkniZH_Qi&Mc+)lb29~nH?&p!xoU-PF<92rzmwa2Gh$LNUs({qM5cs*3E^#cjiq{n7AG~l%8omM(<Dq9m}p9r'
    'q!yfFG%#y;#P-)p?lI7zNjidv(S~_jIBqPnWCK_`(?Oe9SvU+i#*!Z^cMyU~5;bSm6u36bqL6)YqT|qf>q=ys)5%%t(JqOgM;%Z{XUR(lQZ$%S'
    'ksHg^vc2KtMX7pC7H(~FWRhjJv0m}nkL(~#-9h%8hY|wPjxu5g{7$AV33&Qjz0yx@3@VT~j9Als5Bj<}Mk;BENaWMU!=YjtfM}CNw%!fzb1sHT'
    'w>$qyZAW)r0^W{^0*}*e*QIr&CRL!vR=neUJ<cgSNb3V>94O`l%TnN5{in0(ZCE?0-b5m_VQ=k`!j-X1O3ZD2eUm-ev<udEuqtgf!*hOY$5$eE'
    '@MjPaaurtxp`}B^mBfElj=uw~4qc#@iE_c3ftAtMCofHB1V+RvBAB#^#flFQK``4sl^#4=PR2$R@gI(cNWn~FivU7~3M86ih!^i?QwMA|P;YKx'
    '+5!3E>yfpk$4hz*NB<<_c=#kc%1iQ87A_pM$s4U2xlNtso7=PbtC2IvO=+LnimOeGKkB_H<brSvFF+(g0W%Nd>OK^n{bRqG6NF&oFZ8uNK)oLK'
    'NgBVw3PL|aEki{9z>uHCHIXEC)8AJEF6JrSb-)0ukYeNw%E+vzX5y=B$3B6HB_-zz)@WGcWDs`5pA{p|yx~b5gBq6(L1TO`h{VdK$nTkLSUp-}'
    '3{KzU4j*3VvfTp$@5fU(zM>lYYlu0$v}|naEB@}W(n<KP9s&-XqBED%X+zs3;No@2S(TZDGZYw$+YE`Kc!;dzC!<N35=Rsb?@NQ+8Tkn1DFu`y'
    '$doGcvK15|8uqs02W!>H$oowqeGc^Re$m&ik6L}ZIpp9&)x5PKJW|I^AwuA`^e^wAN_;=-_DJ|n=d`6iHQ4<n?jxZme(a#QWSIvfR<zFppG#p3'
    '!}e;RMgJWQP%!k^xiB0Bum@L3VGrOKN=W=QdH?;VEywflu7oUPIwIw^u!t4OJe7!nx{@*?^k2^z`49)#J=&Fy*mCEipLDyWM0D@YqVW>NE47rk'
    '>rER2;|o6Gbuk(|u;sDC2=Dw@Vt?5{qYR;1M8q8iFKW&7i_>9igJ&l^M`sk@-e#U&vrk}ICyh3cqwrYKm7vu=WmRTc4ZZ;=RM)G>3&<PMzlqC2'
    'JP)oa8=XKReD<V}r~q|~34;Z&aZk>bh`;%<Jppa?*!_p2G|0-rHWjU(8FRg><+c#jf|mc}lqu!``Q?l~zv5>wu)LnvBTyVqhL_(3q=uZ;pa4KZ'
    'uS&zCg~dT$O!Pmd;!{tnlM=Wmf@5SXR-T?i2tcOt{w2QP9-aDpjpf;2K9;_`;h&^c#|nvwmR+LN-1{?5*02hCJ^K-&R{eAm+K35BHJI?*_N%zx'
    '`e%xO4<YcNgvF4Cr~G@D?%_LKd<kL!naAoFc_ZfW;g#NA4)A<U3LKGX7jnYa;xU1TS#+%sMalxh8+G@5U7slKoNCKwNt9#og2@SzAHQ7bx7%H!'
    'zzFbTLR#QR2Wmw;te!o`G>2)<#+7Y@f>o9lO3>?M-)W*TH^LI;DR9fE*)44sYqw2O*zu|qBPIPm>xhkOEAaEhYwSE}xKY1u;4@q7%<=Zq*3BH{'
    '?IbSy_2nC}d709S<b6`M5EIZP$mS*$GzV?TxoiJ3oc4e%#^}jI#Xq@QiNAaL7J?~B#V#TKw3gw4DG%Wr6(8ef0^g}qY-8>nt6J%!l~gxziX|W|'
    '5Vpy;6I=AzdE`)5Q2tc~l3`<_lPGT)>8Y11(7`TAfnPjF#6y+>#bH$z@ep2q6e4wCM#LI}OwQa3!M?o$PUz4_sz<9KgFj?lFM%zIC)Lul1cugh'
    '7pZqzKZk&{O|C}G=AfX;=>G{e)<M6AO;hIYe%w_5_Lq`0jqANdNcyFLXhe;j**G7<9*ErUqkC`SDDOh%$qYD&I`WZm5(S_$JaFq@)>0(BB>&1-'
    'b)ZaE3guJn?@b!kCw*DZO;;5yHjCCx52-v~(7aaLYHf&r{^j&|)i8?j!$iM|f;zf+RQw`yaKF6PE>YyWxF6%0Q@`OP)`r1WFw}zecxrJ918uq5'
    '3IOcYh*XE4Ru-jNL1XRR+WhQA3zN7bbqC$7T!Be;QTLg&lg>O>Vum-Hi`j{Mjn6RJ?HRvfm@l?L`S;0_^j(z$`)P~g$XAq-#c)Z+TSVXFnE%4Q'
    '4gYRTYabkqBw}}(c7Dhw8N}YGFN}R)oXuf>=@Q)uc?An7brsMv8At2!L;k@MfRuxI@2%utKO?gHGm83xc^UF3Gyh0>x*xI`by$1gF@o{)%d54I'
    'y-efHGW9{Cq$ZL3CE2tbJt7@>gS>R)O>DRNo0h%#D7KKTp0w9-U6GsNzoe<)n>+TmDB(2w^K>Au_B!72PV6+Zhuc6zfM9&n$^ewiGdE9t>uwE('
    'o-M=js}O#y>g9BbkwB=MX!5lR?eP}4O{O=Vo$<h91od(D-VT`zM=G)iY#M*j#fx5inm|{uznKjS^VB8NS^3h|XMAltEuKn0A;~{#@)Bl=gSd;s'
    '3mD~_uJ0n9l!5;RUuFydJtFYrp=g;oDypryK34qDY08U^^XOO0Z{uiBx?dN|<_hHZ4|SXHjy7WlkRS!|O)_mKS0I5qBd!$<i65Y<Ff=wD=B}DY'
    '-j#PWC)D}>#a1WgS0H3{<(conQ_{{5Xe;JUMv7xj0xj8d_$tVrmirAiqWVTnBp(DR0bAspb(wzLPjq=dx$;DwIaZu1^Ardc6&LVbA*=L|Nak?l'
    'FM8aoDLjs}QK<4kBLl}WPWw2xfg{lf#S7-6!3<~VV%K@-B>}^Apro#fE`FM%9+yEwWLF*Um?h3jWyMc1O#2g&bh=(0b#B&{Y>TcoAZCvVTk8BQ'
    '5o8jGhSqvkFUq$DWyaD9e+Y&TvO`((0~_L8%xJct9nVg#wm+=v(Tp!#Jjnsaf%A|~63;s6f92qFYfG>893=B^&}5vRDTMTYofvDzW+Se<+oJa3'
    'oEI=zl2EAE=q)}y-A3=ia=``_LRj0A335%twV>Kyjllfid46AUY#hed#(g+pM@QREM8X)nR0Svo&6UcKMQSG!$0}0t#5r!A>vE=K!&;V!D65?p'
    '4+JltuEnv(vawmxgaN8bZ<L~9Gm9=YGbP5!5g`yagp||m#0`#L(tzIXCc2D%GK<YS7tL~8sy?pE`RfYct2JcTS2Y3_SgsI0ooDAp+6^3-zx17V'
    'v``3gw}+!R+Q=`|fa8>ldR%n=Mui}eecRgN2%ON2cqaRHKGpg8%Sg0HBQK$6T81jwMLRn%QF(fhu#1We6trtXdpPw0tCDV*914i@JkjMkVUWsh'
    'Y3;FEcL7$&2Q?Y@V#A7^29;OjE(i*2X)8CkcN$^GA8YZEZ9#tbs5S1V;l_QKLcIliifZQ(*Xps&z#Wf<FdDf`UvsJVJHmsw%RCN|er8)X6{@m~'
    ')QW6_+8=XFH_PNscG<SBK**x!to26BpC4oxnMeTx;nL&&yV|(xGI_&<5qSJjH;$&;EVP6oM%?Mmas!oAS$e1u7=Ukm_0tN&afrCU_17G(v582%'
    'lo?1>+s-b#Hqx82W*M$2kvcBmj{`+Z1t=LA3ucMKve%F4?#FtDLxh1b;W#DKnT(GGdv@oR6`HFz*N<whBKvVEvIN?1K9xa=soBz_SZ>6N%^Ujg'
    '$}M9v-6~&3Tq!)cPaZ^RU^KP2kY@4GHCLeZIm><%dJjh{pGv)x|12Sa#-8PwYQft>ZejJ39`F8^!wgyb`fw&YQ3wzEkLa_CO-O<M9#qO*#~;$w'
    'bY~h;ysWKoacTmC(<a=Fqb6UN3GL{{a6Ud&`|pCd{Fh|%9+6zV+gC+j^)k;OMv@-!hRYJkgXTD|-i@2cDKohI+5IPBP}-Ln+OEY|c*Mi4m`o;('
    '{oW}`p@ZavhtYD9F1aMG+r64moP)~0m+s1)#JHOGJ%hiqWQ)N_np>gB!f7WYrxYpls{QZg<&k&FP0zr#DLz>X%*rAG#ZN$(XF+(I8mnm-go~@n'
    'ojI_<)7__tZ9iL{oky#M--h^LVK?yoF^Cq#lzh^%VB~LD5pIXVyIsG><6#V1$A1ZLKy29;1l*_*JTt67WH~l|Apkro1A$CZKDbmzRI%?Rf_m<A'
    'Uh0Dzk?WACx<x5EnfnV9L%j>XDokZw2`F9ZEVv=6;1_V5^D;~xZAX-LiVeP<2}(ybawfK!Ae(-cPZuX<_!FB_lZ!kqUwff`B_)@JNuA77&~dMH'
    'Rh^S$V=Q%d0|0uwF;WcLjgzfpn9OZpg%c-Kq<^oUp_t>rL$Y}tW@~A6(j}~~w@a;O3m^(iva6zE#4;xP<&+U`Tr=xI0uyj@rVI1_TgZ`BLfsCz'
    '8WCz^qYfW&JlZUbp1-reV-BrZa+uax8A6_3$A2xV#VF9f@vzt;<S#*8wk1j>W2XF1rt|u}MtiLC;@??jh)MM-#<>aH#cKGeY~GR4#UyI26nU69'
    'AXgwMB<#0%P)$p5<#pB9QqY|b8Zo=l3$y_fFYFhJLIX;U4}+TH{kB<f;<RzirnC!@_fz?8-ZaS?xi|P<j0MSQJq=Gr(+7oLaP0;WRXI|Q;B{(Y'
    'uMS~ee7rjO8Zg(GI}t5Q9i~V_p!1V$1a3n&Zd3JUESu%va*RuPY}rv3zAPrbIUOf%-``>s7}Unz4Y&U-rzUD+SGLPG9f~dc7>cpTK@_TKyUGL?'
    '{)wJ?rn3|TEL1-CHn~WHvX_sr7=apSV{4++%Rmcr9gN#11!1yw?x_v{w>}Ld7l_{t)k}E7B}aW%D}5)RycS>l@ibxHtfdZ@9!r$?u{6r+s{%Yo'
    'b7{8};208SwOb(npoW@Db>#+54~|hn{A{0zdBi_kf$lN;8L&B>1HA_5mp;~=L6}dyX+kqUeDla#?Y{g&Wos=Jt{&8USx-aqIPC$GYLD=ZcS`=K'
    '5}P**j-;TM_}RMAR+_%n@EcWvr`Asrmgu*3SvF`PavZ*&a$$z_{4Gr+&3J;w?iioiE^jWfRfxZNax{6)%Rz8wjH-W`WpH`0@Z!6fxo_*!L(YUO'
    '7XP!t>VZol_T&o5ro<K7gEE3NjLUp?vG(A1n{>%XEzu*G5ukxXoouJ$lX)emKkW0|OmtP<TWSK<!R3$TYllIK!JaRW)G{tk1{%CYx8I8)d(?HX'
    '>YKPYfo_ftO;a73*(u&z1B-*LoVeQ9)DYMqf0)`W7-KC#v-LE*3a=G$LP=_8K|VAvNDT_++XPR+a3Mcyo8DUn9Ng9X8JWww5W5NU_K1mFR)ulX'
    '^<DfRlPHZG(5gD97|~b@?1OFW%4!02%7oGqKCVm4hhY9U7AwvXLAE`32)YcXDeIhLb_3^0GFoUFP;SeeulCxyx>}*RbHy>L{YA)elAlmSS0=_f'
    'yd>Yvp3vJ0Z2#QR(UITSRlVd}TllC0of^)&e?eGkc25)KTY>aJGwv(+JN}hn09oS40`~Ek)#?X8<_1GWFx=fl&?w=^5OU{dyr@t@bqzWqZ)Ui4'
    'tT_&3nFBT(ismbD;*Z*i{01tfkJtDR$O~ytZEprHWZnM2xcve`RYer|MZws78g(7zExMOS$=0@?(W@xO@r;?5)*h|uCei1S+jK|D30n2DbqF$V'
    'H#CwF3yN2x_NLZ2`9pr>z8C#<n$IZpwN9>aaQ!l_#;yXCyh8{=!9I!6!KIK^F@+uu=u~rAq<R|u8N@*^9>UR?=U(bo%kxPVF}PojT{G6Q6J+NL'
    'PVa6j3^R|(K@{tA&#`zGwC_;KI;kl)>QgX1UIp_B7s}W?m^$VNOK>%DiM=6$4`f1FlJgYu^0+fE=^3TjT92|6G7gdmtH$=cwviWq1!Z*e#n?TF'
    '`5;h%4T~CvY!(KL3$`U*DHVhwXwr<O>Y(K`&2L7^5<K_|tDx<|<9Q>!t?jD#egP%-oLR^Uh_Kcz?<G%#$?oGEtF=3I{Z;LY)5zaRhJ5^OcLEb5'
    '<$H?;B78Vv(`geb#-QYQ>KMlSUB<&KY!0k`@Thc4&0YD7hmiU!Gpn<L$bp;EQyChiz5D=S1zbm@hm_lVf$IatP=7BedaU8RPaM;Ye<+)smZ0cZ'
    '6yMq@_diHMeJk^AP-OZDw>Jl*N+hG}Ge!#p^Nj*j?;wTZyBStyJun5HZAS3}n)~!Cb7qrer(hXWa|dKxnyFD)U_hc<ih=jd=PkuYr)_ALY^$H1'
    'cWr7=yKq7TiL#U~`tUMV?FDfeRhaG?EBX{Ap0{_W`aJGrFCcXIj5_KO94p8&G$}K;E-&qD-C?EI#q0|X7Ep!=V(V#!0_n1FtcH)*MXcE(L6bVB'
    '6D-gIi4p2Y(|)9ED-XyJ`4Xq>hw<P_!IT6;*l6cxZ@UYs)NS;y&tPD;6L9?*EITI<H<LGNU(70qAh^~lX3w9*DPCIvo-P_I0L9VYCst3D0Q(-4'
    '&ZNJ@zcEtes(Sr`@+ZM2?z05?W>;hbMhFLuHox8uKsorHGbcKpL+eW8fj0ifvv`J6#E@TyI;QJxz4)N*zM_Nvp}NK5T_DJGaoV&wBw4gG9pczo'
    'AVH00nHa(ZmT*5EB5l|G<8+OqTZaYXF^V{LHShWfYqejMnVPDfuk2&_kTy&4meu~_c5U{y+(7%5|6t{NSy8zU>x^hgq@hKuY(i}mzxGo*uT5kT'
    '-lg-r7QZ>P`NErO^619*sPL2`V6^?zD!P#>seefr7%AXAg4tot*3R+_yj_TsgkhboG?+!y9W!s+iwd~ABefgP>w-Zf0Vr9q1kI@|%V6o<cI92>'
    'U(X-q9n%j!lsHy7|4bB^gNV60)kn1epN&HS>B<8j%C&_<RS!{Cb%pWgtq}q$RvXxx1Ce$$6;aaDGOILrOb_sG2k02Nuz4I%p6<0%e48E2%ovkQ'
    'UVU@~25FRM5=vK4F9fAV;D@-OF{aFx4eo!r@w9D^@f3g;^}>c_Fk)8RK7t?i`iyt6Q(gWbu*61u^#PWPUE+QY-5#KK3}j11Ncn30tz1>~LhzSC'
    'WmoCV;FBjd`(JKU`@SL-B`z0MWJM7Urx>utg@w~0qxiY*O@q5=S5j=$TKmzEtcNvtbJ_h3PW!1M+&NPm2J6;zL6}Y{13Xs~ZZLtZ63T$w7+OOG'
    'j|n#R*??Rl)dzZzs&$LF+#W;ei&<z#qI7FBc{lfJkzMbOO}5xHp{1lq!=jbRMTXO(MgH)`t4X?+8W@Q0I!;nG0n73(JS8-gc@h6-&}}cN4`y2~'
    'mOD>zBTSOqQC<UH>%b=yh)IU3s0#(r=s=IfVI;BrSZ#Kx=lj6L&#6qq%ku*7*U+<#r--}b13eh;A%7&1(xGrJW)pF)K*LvYQ<6Ae-K@FVzi$wG'
    'F4e;~DW5is0cvo6&QSh>zM=82iq?juDNYWY8^)a8DzzzRI>~zQZ3u4+I6esG-Jp+p5K=$zl*>sIl8myprT4sC)L@HstZ{B0W8?h%IXcAr$)^~V'
    'Smqe6r8@Be-CgZWEq-yZCbuzfnQD1nWYs_^$Y_(YDMRA7znCexS#_oig!X_o!`}GLp)}=yCiglBKdi(BuG(944yC3cU(5%}@C`Fqf6^YJThu+A'
    ';3R&eXc~gb9$LSSO>C@jM8k!=0nuS=NZ~@l2)Y2$-XivcTaLk%$@`Uxt6rtlfyF&l&4W^rF!7l{kt8(nASaEzKsJ~`?Ho0Z8*qoy!OOO3Kai1u'
    '{FJCWW|3J3(_lizG)VyytE02e$i?|0GS8T5<M=~px(QH(`_nD5pt)Mjx}iVR49d>@oWRoMs%uf4rkCGTk{tbt02~UNBR$2f8PCCggdf?qg=xHD'
    '1umYj1ukq>nF5Ud2^DMEAk+yNtdD$agGLuVo@S)9A-Bw=!O^<iK=DKDGMie9!(5lI@_w^zFy3{@rLQK}auJHHe3qDlc0{L(NHh>;!B6Y2G0Jlv'
    'u_S_xS@s77AFyV}mr)zWafRC=u9FGsyqS#1w!i8t$bCa_^z2Sc*kE1Jy5bd*xL7=Pi#hI!<Alx}sA`M}=fK1<)83pog!P<w)h`@Db4=JJocK^c'
    '^E5n6isMo@H>(iAnbwH&YQHXeAv-<pKg)tx-VG!jbtr5@A|IUor7+(Uu#9fg&{0`Wx!8GJCP)~iARjZWM=f*}W11tX>ttkYi~^wvng>S}ctgI+'
    'e&a*3Oh>7zq{@Vn%@PRv6b*3OEDoy%&t%ldB^Hg=TmKP9%Ecy9kC=*W7@)AwUPhIlX-RW@A8n#i??G^()PjC*nJ89xrR3RLA|b;h<Y_?6BgVyD'
    '>Mz*4qIiol0ouLh0|C5j^Yo>fVM`U#nkzxosXligdk{k&%iPoo6^0b}M)?uN6w^i}0JWkxqj@0$$nBijq9xsZUtZ3YhIZS+b}q$`T-Kgj`2#5S'
    'Xt#|CDC4Jq&n>fqWiXS*e0_~-@(@m5$R-=d&M7wzDg4dNfA}%eP(!I9kC!pLKp_NIrOwQ%;+?XQ@6iv-iy@OuPf|0Y0vQOlj5Jg&^0{3@Jw3rd'
    'he%ehy&WL4b*>!PJ$T`4w|OYuEP2Fe&C}_ShYV<&zk&Yti&}*RzyT&4RL1<Q@1H3N@ZAdtmDdV0?=X?=6s*qR&#nUlk*y-zw!8<QEoT|+_b?*|'
    '685nDS1SpK{{jmyETV1sAcpOGw=d8l)L#g(d?Z-})02e1IV78gR9$JVy}Rhw%*_C!GKFLG62dkVEkZSk^D_voljZK{@<|9QL*yK7NJ&fkOf>5t'
    'D>5d<17dB9*xR-|Yrx-q0h5RcZqS=guJb$g1!C5UC(E)%Aez?ENd%cVpQys{vv}-^fMza-C);KnAiC$~%Zxr?zMFc<P~~c%H|Dc3cQ`QOM#d=R'
    'embB6BZld6V1bz+Lh6NkUJ5A|>bG#s>nL6%Ppz5$Lq^x#R49pFNs70Uyi4fRN@JFLUMUx$Xa%RBhBA!W=*Z_$w{M9F-P=3lZ2+>XgPCAIoACSq'
    ')th_sWeTDhi*@d9fMJL5X>VPsb|JNh7A_1W&`B6-Nm1<2#o32pG*N7<2|cPi3GA%YO@viT+u*_g*YtDdNmCvq*%{^b;cR4`yv;e8en=`N1=AR0'
    '*2q!0#B=j=iSj&0S==nTZ+Ae@RvWQd%~H5MbCp(7$ZFn6ah!3cSUFuD2-PcdYlr2b1GEb?sbN{;$ssl|HNNk`rLQ<z6gF%wLF>NqiO$EB7mm#M'
    '=)Xk*^w6%!FMSXU_atR|GfBPCrc&U~MdY9kW~S2JATNwG)dW7AuB;@f`yIYKGLsQslqgRc)JGO<oHK8_r6x!z03u05uYd|T4Km?()UBGh)nNfj'
    'a6Qca$tJgZcS`PoE$Fo?<|~J*U`j%FB4bbP;uN;dc^QkLX4=o9XP{uSa21zNNf{`N5T=%z0q&FeKR&958R~Ye8e$7-H6#<}FZ3T0r5yRzTUg9B'
    'SRQvy%q|Dn64mTv$)1nhem<hB`2CbTtjk#9(VU{b&=o>QAyDa^1<!3c>`7q*yY<}YfD$HL%T33OUt7rSk$v$mxFIfZym0wKK=;cACL00$$C2)0'
    'kfQdg3yvWo%e?|mj5Q-VY+-K8QmMVZ^bw`Aeb#(LJpD^6s^77VWC(Fc$97RktYY1Z)SBP&6}<^{MI^HjSHVlHM^rawAUO1ZaFYntS0kmn=V1^*'
    'dVD^f9?-Yyv>+kHH*oDP7d}71pUOpX{GHN{m$+&~;Q57|WG%|1Ji;&Nk+<Re!QX$hB^eNSd|0k0W}X;%)T*Ve5A~hrD$*iZPC-Ih<Vf44sVqqN'
    'MX?4+G<y%&iv2M34dm>+pA4YB(kmNl%t_BDIXgb5cx2nu^^;vABMMhP?9`ZcIUCtMCVd-e@&I37(^>7k^Zk94xeC>TKs8@bQ5xV#$@o*r>L3#K'
    '@ZTBR$7Kdp-+S?QE`PCn^l_)iP}Po|4O!Z5JvZ3K2qCG)f<mswM;jQ^VYK5l2?Zf)3}{tC(fd_2BEy@Ze@l3LqDkSsr<z5uO0lwfXNK^;fUctV'
    'ID|6%7q(+W?14x<5@<uC-NQZjN<TdV3wL@KkQC!Hbw&1fjH=RBl+Xl0sDtbZZX{mqj>HV5?kb^M{(M_?xBtVpxKYt4Qb;aj+6JV68OB+2CGzC)'
    'AP_(vCH;j7I2-6Eoz>z6Om;)v@2Snn_?gOpm<PG1%z`@EM??MHo-is006Dt1DWOltF?uB==8DxMuwrpE1m1cd2iVt*0h2_NS^?pzoyM#<Q4_3('
    'ig9_!AO&)g^QS!$KCi~cG13*%_OONIgjEOO?ZozTS6u%d02yxN2e<{ICZferd2nknWolZ|(0x(BS7`T~UMWbshww&N(G4)RfT$8TW|-1E56!{K'
    '?}pW(IW+acqHE5UAOAyniGh%X-j6Z#^*tR0(Rpnp=o58;V_gQFE)_2>071C|^bm0a(ms^Y3>1)7UB?bDq<sUDT&m-nAVyoQY31_K15XO}=D6SZ'
    'q)m5X{AVJlS4_=bdEPiqIr<i~@>mC$&}h_E4o8hmB`^7u9Dj(K^<+Oyt0pRYS8&IHhY~g3{{RwS3Nz>;#SwJVEW>VRn0?&c336dpOr7;kUm4?E'
    'qZm{1Sm{G}IbO2R_DSw2BK7P*rz9*|T6Vg*`l)2?Nf!GTT1!Q=`m;-VFc}3-ETaez@0v}xj}1hLarrM*i5*ALKRP2Sy-4{yTc_QM-!06;7=>%b'
    'NrH+AazATmN<K~lFmgiv{h}yxM0ykgEfEKqtV{P;RrVyw`BA4}S8IORpZ?96upI`*$Lvq~Y@M#)Le#B3PjalGA{-Rf%pU99nPRpztTJbH@H<Un'
    'AX=V-Y5*Yg$+k`1pNdEC98C$f|H2TqR*cNwkS=dr!D84-O?2q)kbNly2n9)cC=*>aYlEjfJ-!)A$Y+JJI$Z+lG4}XNuH4W-xh_jy19#;$+?GvJ'
    'VRCw?2u_=&xDkh-7`cJHV)DM-L>}LD(+%R>${rv;`5=DCjcu`PCF-G{(F`r5Dq`lgyQ;$raqMV@I#n^*u%G_{6|zD+!|7Ph?~y(f!rWqDJ37tw'
    'Z$tFr1+Av4eym5&c^K11AY^y%WMO>nImbJRL%c6G6ubwSO=w_kP&k*3i2!`No6D%^G2+`TNGwJK5w6^ZH!aN!3bE>W9;{Q;!Ak<xbh;YsxEY3|'
    'cIz)>;Tbg1odE{9WSIVcbX~n4rj6~5E%b%)Nx>v94}pxHOJ;WU4gV-|%<T~e(dGv-$vuMl39?Tfb%9i=4wP*CyrAXLyz!8o<|7gNjz%e;7h%7l'
    'A(DEPYDH`FA##g<-Ucy$!KXHX&zv7F<?teGKrCgvGW#BWl^e7|MQ3VqN1;$o^89=659=Q7q@_9|^>Ex+m={FWo@>2*KUfgx4d9yMN=F|BK?EgJ'
    'yA&On0+3OiKI#{C{r9@v6H&3HqdEjWbJbE7<m2-)Z-_-X<aWb-FZX}hxH)juqk?f70kxd!lGUU?ZdTGuM}EqT{?;guvgo2R&dXajpzu44Tak*~'
    'kt$b@BoIE!8A^<bQ^bMR-ci6R00dcX12(asho(K3*;q(p$DC7ScU;$sMn$|ZRgQ4nNA9#Bul)1WcYp{(S8!HgJF>#h)vx&pO)Su5?IQOKLN&Dv'
    '`ckSSB;4xQTnY<4=kUCF#4Xpa^lHT<6kDHM`8R@IvnX@a7GFgkO0c#{#bB;#g|%PigUAOdCs;{W)TUop`}hPeg&{l<cFJ^fna;t_ysuSfqfsQq'
    ';GZV?qjt^H36!a<Bz|*$$}u-L_OR;wL=RCwUc3as@YXy+{wPa^O%ll-A#%3Y^>bct0|w(4k_0Sp77Cjpp7OUFcUfKzFD7h7n09>Ml=5?*h!r92'
    'rk_zLzr|r<ymON!L6;~y9r+W*Qy&~_ys0ur(?vXRxBR@QD+Im<tO15khMsSWAvF@P`a1;dERc+OkAS)Sq>XZ}{h7*QUu1{m{7KvvOR6%a`3Z|i'
    'XESZ9RE1WJUoweZ@cG8fOB2VOd13>ZzVtO>agywv&QMHY$?nlKCwk5R`3lyH{Yw*tlwb}SPQ|C8MAwY#mwCkFlbD&$3MAEH`irb92h(tFJ)=KT'
    'CN-4cIz<oAss)fc)vW${^a}Z~GRKMYB)5~Myp2mFRu-#%d%zj{_#5?PN1DG0Wpjm=A%Wmn{*G`r>r;Mrl07G{^JD5aSu*{C*50jfdou`|E+fFd'
    'prB(()ncuP4v;r;X<_Cu?or%9I(HN>>jm6ON^$eaZRxTFS&wcOQ{gHXW@VS|wiG{#wu3aKj=WUqN~YD(>30eZ2(4|tPhW6vB)(?YfQ7ABCq5tB'
    'R3Q^RXW<?yuDhefW@>4rTMNZ6M51Lo>ThuZ0#pE1oL8I2$NJGQOgr_d@~I4pNr2w;8oc4=8T7K#3}%osWupgRW~|UKZKa)|iHVN>W5r{~5Ge!*'
    'f|M%5`L&w8i7yw)sP;R;@;28nT@DFTz2Ah4PT;`Mg?|+vbi1Q2T#6T$ad?n;@%PfOoLV@fE<7Y<)FqaNl~|^Fj69fs4Q2Y^x*oh#O9mtG_?&8c'
    '!l8L8eh~VFcB9G5q`wbum3+r|jFUR&7zxd;(fC)X7@RJM^INTz%0@Y_#16^*MmR~%Inok56m$58ETo8anYbXv!YkinuRyW(hf(Jef%p4sMxq<-'
    'ngn*^<<1ycpqlRQ->f-9HR&swf7`$x66xvVE_Up3IAkNa%9!*b?!MO3FPY-<MVKaqw8AINenvhYKLS7`JY*OCr3JA4iA*qNe+q*gM{qi5uFFXB'
    'yNVW^%R{hFBe_43rcMP(;(y)4a;>QGJqLGXS)FSYW1>!Cr2|k*GIOV8lgS<^YuFZh0=PJGg-Hn<$t>xY;>}ZpJ9j{L1N2RjE-mS9P^8lMG)6I$'
    '28I(Hjb}rx(ubF|moGS^)W%{3f+$c?gmL;y4`?sr%17jl-(hWLilf}3p5CnmZ3Xh=40^dj!H|@5BNZX)WDh#g7<FAV&HW(Y@b^y<fL&-+(es5H'
    'p|Y`^T{T4y=y@*O!8#YlXgE0~t*RXipWx^AsE73k^$rKrwvs(|zb#6N*h@K+9J|R2DnD-mCjk?b(fO1zm+<wVq_Sx<GcY<3?RbisqQ-kmnDkP8'
    ')ES^)GIrlOKvo(V!EU^?Vjt36$>R1x8-q0d;7vWZDV-z#>TrpmLpKT~Pmb@65_B77ym5^?;<QN<NDc?!0lRql_vL&4DTRASIXvuY8o_rkat<iw'
    '-!$G^=#_mJtq2CdfGt^*NS1i0p4Ps)TFbKeWV!cZeS+j)=F)dew?`fT&^OLF9ih|u<2^(rcN7y<I8Y%lBKlRUtEjD8e+0a*D&%~DV$3b=dVTqe'
    'f7WuPHDc4SbxKu&!<k&$lz|yCl_|2oPxEM?FBNZ#+IizvD5uyub{M=$@!1uDUQi%FW^PuOB5lj1LH&fQ?z>o(R-r+J9t(JXCtrTDl}9l7btC!W'
    '^#x0Zum!)#)yL0qbkuD@<I9)pe&##u&y_y0z`Xn-jk^45uZiQgNPwBv0M0+Srp(?2&lYP-eSa)-D}*J+NZ3oY12URqvIlRwJ+#TGS=y|*Dv=gJ'
    '%t>5~6=4f)9!B70z#h+yBC+rrZ`FO~P_i3otyxEeW5ZI5(ucvg#Cm28))yTUeI8=h%~gY^R}|aN8Y%Ecrd8{)Urq0=^7m_Cfc>>!!Pf?>ImqPv'
    '4pHsDRbo0|?aO4l_{h#E{J~rp+>>dVJ4}w6iiyDnjCY#oB)*r4Zpj564+M-2J?O%54&UCRkV}CmND0PRVlJO9^z?A&q*Z$DUM~4o;WgXocIv_)'
    '?T)ZZd0%6;V2E@&=`}Hyn$Xmm$!1rU7d8U3ldij-MYJSN1&cfanDLzsN&z&-2)o2zzO<~{ZwN;DyB(y?(sKdfxxLB<_+FJ${ar428Nij!$1&-|'
    '>m#>}m5wJDwkirn?Zn`6f3~Q;_>&^je|XWZ5MItULXG1A8asojM|JB*ss>hX&{UHfC$L<GamDo8rmIqUTTfTe9&@)|=2NvM@LKHr-a_fhk=nr0'
    '2xKEAe$G4P_pS(#s#Z-brVVX~E+NZ=rZuY&(0z3Rk=mMSrf5^=;3&NzIMBe+EL->bDWJ-Z(aC-(B9r&~u@|zRw^7V}`>fYpMZty1N=h&2c!Z$%'
    '&i7o^3?O_eZJ>=lIUu|Af1vI-8oAQJB#h$l;zkXeJhG99q-o;AR%%NGkUH=4J0gzyO0n(%6!p~2C|bh9W$lpEQ)OQ;h)4|8M)YGB?+bnCPSz>>'
    '@QnOp)Q6hQKH$W|U)|7y^bxiv%Nx+alT0oPze}$@?ko2gHiI7VLAuj>9MlPbXzTq>(UdO&*sBWs2>N4wU6XcrWBZXYCr}&(A$E%idYUn&o^rOS'
    'IfqAT(wT?t9WIComvbMkWR5r7OD+(z=_~ONSK;M8_M`RME|t=LJ|09dB6{!#m~2MCTAd=i)Y~pdzi!GpZR8!wfi4!nGt4M5FOQ2MhJ#bF_+VhL'
    '{@N`Fn)FuV?P~>GyrA!xuAnyANBgd7Hd2@Lp==~<Dvcnyg5(9pPyV0YaI|v@nkOSsX7}<*AWX&G)FIXx7i**87G>UPw$G?GHY7Nu7mhFoBa)0c'
    '^=!e1{;}T-g*?whyBJh*Kq$Q2Mk$aoqoX+t<&NJpS-v}SEz|3-9vYO%fCRbrz&>*GaTcCB=s^Uc{=wsXWo19Q+;8jM-Lkcs;X+LI+)?ii_AhU2'
    '-^RK`prnX3kzd{{6D||F_I_-|HqJ0iC*r$?XQQ-q5^hNb)!33^-*r8Ot})V1^w~vX&}Uy+G1}PTRhjw{pHeU|5@@~Y$HB)+3kZm0cZH5s_>S}n'
    '#rF2XBZZI(C9j7~kcYvqQNqjt^PbVv5LXnyCWqxI@s|o`^JuamoQ5cbq>sn=gDRkH!di?M;!^+ioT3Z)5f^~PU9E#9l~)V$)}2HT3f_TK-!7Rg'
    '^APcTVceriG3#NRfxJ>R>{NGb*nxR))Yi|u()hXP>msh*+@6>}S0g67s8aa3Oz@pf)XmCL8sQQFKCD-vrW=zm$=HdG+(70X9M_Ar#*m9ZjqiY^'
    'P>J#vhuBUPD8n6JY?(<*rT1B0LHTy&nk#zH#P>J2frTI3VDXGs0H%JJ(BuZ0c<E2V`_B~^U*I~JD>aLb25$htk!3x!DT7vDGf$C%92Z1Hw#6l+'
    'r1YAQI7RY6secpbv?-5Onya6^xFCRqq32R1yL9VvP{7MHxmB@#7J-n?L<Ms=ZifVL!<!9~Lf`~W0TvM3a){N50K#EiW55|R)0YqTV<UI5utp;7'
    'kVD`AwP5!}RvG9|F|pv2LR$p-p!Q9&&Mpahf?~5m+J8+OWD%CHw<0CL1Yk9nyxf+!%p{PoxlMKW?H1VN!U%Oax08Xl7P>%AaoV?;=g_S8b_D>U'
    '#98t!>e7Gd?rzjz`}2bHC%l<<mVGEuJI?WWMJ4ZD$}Od-6Mh2Mc_X;#gwj@Sa$&y~iyatQRP^%$SBa4B<Sa~kAa<m74O8%5)<}aSZ-m*wrkIUw'
    'Dlb;)+g0|;%1~}JbzF*Xo^?2B5zd2XVjH}y?G#rFKOn>tNyXQG&rLy^JWVOtNhp32d78E_B~`~Rg+{;qT=K4nLCnmM$0ha!Wuhp`MPF0hi|@Xh'
    'Ihq$R^~2>uXq2$VFnvLR+X?4SMKSA`Ch;4$*=g>5VejXctRLXatX}&SN!$ap@x;5$46NrC#nxNQ4ObS?GsL9TElLLtM@dNfY5oRceS<aiGsBa;'
    'w&Atn^Wh75WWY++{iPR0j*>nnqg0L^WG>)qZIo0!yk)gzYui(z4B9%)URd+(VSqIdpvKv)o-cdSJCw7xrl>|pLd@E#x~liU<aL+z=US@afNCyW'
    'kWYgWxoa&oF@($g$Rz}iwVMfwAE#|lnQT<(%wEPpee{~k6CA43BBnsyA@nkAkiU(eptY6Hw82TrY=v--7(IQrFQ7qAU-<;EyvDI{X%jpUs@xw#'
    'rT)-(G3&=iHhtnLAeXYr`*XY(@Vf?hG5Cwm9Jhw-7g;q1$7qw@McrpUg>Xk!eKx@JSviozTAET1=RZ2anlqz}4^}YZf$!zWTj3}w1c3tTfpm1a'
    'c}OR1q=j0*8P!$7pI7E~j5I(MVs|J)Z`*H~0<ia;=<Xr*>1ZvaDkI56MW?SJdBR~G+GIh2r~fto(0CO=KQNZ_Yz#w_|1kUZQIRVM-ca@eXeu}{'
    'adA5Vhl>5MA(z!h8=;&+!m~UC!3o&_zU;N~WquHVYW?K0Sf>~Zb|W5`NhR&`b#pypWRSediY(2l#5rsS2D*t2dM7~cCy2kpR!)k`xmxxw+<4Y%'
    'h%oRV9;(c?jxd`t`!+atR(lkFB$9BotUA`TR~24J?zirVt$vlLlj3K=Og6m>l4`Fjg*jbYV^^Jkw|ZGVY#e;O2tBE-=y4DfMQWw~`L6Ke1Pwy`'
    'YVbdjNSm-*O)sC;9!wKrtFehEF&9zaC2hV^P1r~Qj5w;O^tMlEH7k|M*O4$S-J&cUQ>4ID+@ru<u)q!uh$I(!ZszN-BgxUuVzr%``;LH#j?1C7'
    'X&2NjUc|Hz5W~#N+4<yopDmG<l#@SLU+mX6>#)Y`tPAE077Ec{ZJQty;|chy1FV+{Zo_wZPC$wp!`D;=ziVIHM7R-1@{mFK2!o-9x!!;;ySDoK'
    'krAl29cP{I$cxu2oa#6xk*$qNSiKl?$KnGA)t?^ASTB)E!!bJt*vx=psHcP2KgFIb!=m+#5p~gM06IQeJSh$QP-I7Ly$bU=hLp;Fb%D<|`X+?Z'
    'Y<(F3v!u3)7MdQ%=xlYE%_@&cZ5(62XTzi(V#oOG1)X<!JN&%)$0Q`!OD%sAdd7ns>h14InQG#wZSFCqa<8Cm><n=dQ4%wxkRQvAo14T>oGz>i'
    '0?g-JE1v)SI+^{zK!_n|qOB5s?F^6H*MhHSbrsYgZ5@DoPEs4Et}(7QSL3IH?EW1JrQ6|)G{i(MVtb4V*<`pp+v%JE{>}sZUoW$EiVRBZ=#q1C'
    'iYG<Ys&SWT-Fe3BLv;W1jjR_#sX5ojNI@#Nq)Zg9)Xe120iC^V?2bl)&HjMNMw7_A9=2=&q<BUGpEg}kQtG3{Gc1vT(f8o$xXu8F;Rib@G!yw%'
    '%jW~i*d$;ZDACPOwj4=%xJ^pTJ0c4#-SAhCqr_W;Lpn`he2#~p5zSUjk>>BP41GN)137tQYan5qX>PB=_3j0z7zIe>0Iw^SAx$F}6rrlO{hW`('
    'oi4eCh)&6LH8IRg#BHVPR^B#zCH##5o)1z(Z(InH#%|VX*o0?*1egH)Rz1G?ZD0a-hAD{?KyLw%3tm03ijV-dF-nX$74Y1v2?c(lnDX~sD;qZ3'
    'mX+eJ8SbaJxWwGbn0rg5+-BMR0DkSot1}>smY`4)lYuC^PGikO?-d0Q?QVvS&hCKFA1`s{ggqbyHbxAO;$}E;16~$57}so4izZ<2((i2^M6isP'
    '##@L^+k<14$G@YO&D<vr9G*UiUx)O3n;ciMR1-MNPtx4TVi%tl_Ij7ubQ!Sto-=dGthE^|H96Vw)+__soqYd51MX`?JbYOMg=Rh%IZCG^7I+ok'
    'z+HQuu{Uq-kWDN}p`2V!#TOKa02_vzqf^(rNP=;v#s}aOK`#8>t?^hh6n1<a<!yBdQ1G!T;~4LaxV)M?hW4)<=A(ju@Lc*yo$QN?IC<z;=?~!X'
    '<Sdr@O@uHM^VMS#d75(?$y30@ImlhYaX!oH1HMh(Pwc$t4Jx-IkVc|tx(^Zf{H2}OI6D)kQHNrsyUZ5cmGE!>ELXOmIPSPnvsUfhsW<3Lw?~58'
    'CGSJS;V*bJ1**}q(klEV-cf4jq(f8OW>>p=i6ZX({>agIv(_CHKS<UO<^4b>K5jw++busg@A{{AuuizIj8xU6<UowNaeqbaI#SYn<fg{m81QiV'
    '9L01hsT4KEOF=qL;SnjRohi>|LEGV72SHtB^ulkcfIjwQ?tLUH^wc%Xib-{0kcRj|`RaW%VSrGkh-3&S`5y~`&b$|K=bS0JhG+J(l+uZ^Vc(YR'
    'V`hu&qf&%Au@U<@fp%5RECAhlD0aCT9@Zo(BBIL0nU2ZE6fr^~8DmFx{jimA*J4g;(y1MpJ`UzrJ_DUF`;Q8erPZ-Z5x!QL?k0W)tq`?q8rmx|'
    'u&bolw5&y{>>$-`Qgjf8y;zv-0kYc;O2sjg{I8&pc4Mi5#k?1{sDJc{o*^1(EFgI;EOUE)Ht*94!$FEZ_5=)ka^-v}>BDFbDvN2H`W3kzNe6@>'
    '<oJUw=s(Ly4Xe_ojz0b<UH#GV+=aOfi0S2cL{GS!qnQ;7Bn^1g28+`UI5ApKpySL>!C6N<N!u$a%N!lF?Z<n^ht*Xfb>gXZvAPxffR)oi=`R_H'
    '^5YDGDK<&Ls?J2PRit^@k5rO}3a(XpqmxKSO0Y_5mOMmw)#rT<xw0^@PLfq(ILPoYcFoMxX{_DlzN<IcrK`S0dp$E!iMVEF290nsPOsU%N*%LC'
    'wRk_%PicNSkld5LkcVdbvPAXu@qwu|EiU{R9;R#B8PranpvHg)#N9W&eZ4g96m-21N6GMU)?ob<rK%WQXHPa$%N}Y{FqV^cZb4b5)96;*keh=Y'
    '0Oo;71bf=8+9>+ziI@87qC)4qu7dSipEp{!l0~qhHI<ArMO#HBP8J$Ckr8$V!~oQNloGiCAEiL4+Vl!;R?=>nXF69it&pdTZ55&CTS=l*04vpY'
    'V_BdftU?j`%kN`ih%+6dcq1C7x@TcK*YNC}fu8Lv69jTt<3R?hSDJrTwgNw~QTYf<4d)%JRbK^i5oF2b&stVfEq2tC=h!u^s>0yrTDjY8S%qgu'
    'R2Hk$I=r0Upsr__KsYaSoy@#SZb(y+Pq#2^)x!2IoO0Qxcn~pacF?<@%^CO=_O!pX*-y0}+Ev3K8Avau^*u<mxsobrwO4$xL->5xxm9H51G^g3'
    'O~2<fj~K?-$S-O}lnhn>#*B=V_cLL*J{R#cKIGTSg0c9*YZ50a25}%ZOcXGLd^1;7B8_;-M<UKX#7st4(^bTf;`A(u(!k1?WVACH`ajp4EL!HG'
    '8+%LF!%SQ>+V=>&{s#68m2sXUzP*g>Qt<Q%<?@I2$_kgXccf{WHeGIg_0IUDqY#ZiQ!Oo6-++WZc`b@EpNSp7?Ila!%nI2*7ll@zzolJ-vkdY|'
    '`P18Dpw{kY(EeS!uaf}d6cAxG-FDHduN0JZ=if<;EDu^}aE+w!5+OG$PbIsiIRaMoNuCcHK38_550hl6K?ZO8#;z+FZ{cX(o^z%@34SBNBP#Ry'
    '7>W2XdYyKTYgDCmrvyh)f7c79!S$wCCk-qLi_NvOW;<5tw7RMx|J;<n4YjAWrB;Jvi82MUW5a%%5@;OR^5ldKpjBAcL}i5ga+jTy^fM#mBt6I%'
    'Wuy}s&7U@q!lGL|jmGh)oI5S;vR`&@tG4Wx25n=l&l~mR6{rZLJzQj%k#m8Me@A$Dfpp=N3Rd^FsxZ_}DkqMYS{!O}{U!bPk@XwQPp+EgLIoJ*'
    'cz|SfyABEJP=Ey>zr$N}KChKodPQ4QYm*R1G_SOIB;TM+<*GpJZ;ncj(e|!TbuO!U-@k`P@e|8rr#~q#!S4(qAE#B)i+g}af$cAKECr#nv9$^k'
    'G7brQ4a=27)G(4QvQYw1FOT{yKY)le1_=CUBE6ZXqG&hSeN&Z_ub92FXfSEUlodU<1#K2XGV`(nbnDLffkNO~BL!R$ud=6l%&1;5-;xe7t1VM-'
    '*+3-{`UQ_pqt)b5ZfVA~1;ZsCQytc+xN$f7M5AdNl~sDDU3v%G3_&|=zbLwN031W@naQqe^{65ellWEWS0j@#ij^sI#|8*$i`x<N`?8+$D)pU*'
    '2*?36W8xFLP5>lKr}+YB(TH$>dpl;WAdvkNKgErp@v&-yj(Wvs`@yAS+IbHFRuu;{z-Z$-c63Kl+4x0T0_2Lpp;%sjQ)?LyRKV1L{iz-24bD*}'
    'Dk;}FfaKTaGfRM4-&e$qZ&3l)>mS>+Q+kFnzUnKfX_5Mab1zS8*hfozwF#6wbSl5TarQgcYV3cx+ZPp{-3$Rt9Zy$8aP8t^vlG1xRG!W6r9$&6'
    '0zl8VHJKj!BA|GzAYlZSjvIbtn#h|J^E-ZE1JwX6k$wAsmoUt1$O1sO!BNHSOb93}i_RRL*d}J$)@u2$>ANvU(NL92icc?%S3dKOQ0@*3HCHce'
    'Yth>WaL9gkOqTa=9K%u^ap=yjUW^dg?H`usa*Hr#>Yn&EOz4pKl@to&@Zu1ax{9WB;#?6|pHudPqy>V<BbCb3A$=QZuPhvzp(0!w-L<aLJFctD'
    '8=GUQ-~}t$jr|b*`MX=&Go0}^MCEOO^t8aO^!`H8${>r2nX^0s)%G5$bnlkJ!LGq|OeCU`{|*4D`Kb1J3x02WlU`rmiegMiE@M12q<$Xjq2HEV'
    'hJY;cLV5uh{`N>tbDXI^ebGjqyxn?X?TZd$BMxDDg*&9b;B2Iy+X=%$Fs7^DB`F-n=ivMuXo;igyQou5rMtE+h)Mylyc;lzaQ9@WDu6#&%tS4G'
    'M%KX9F){w7c^{H113$3HN0p;`RMp&&_+Zww{^muf`ZZhyA;(EpG>S00S7C`GOGk2b8xn}u+TrD}cdZir){t$IsKZ1j07J|ymKd)W*$WnC?jO+T'
    'JV)UjX*|TeOyZOt1~H!%!MntYHsd7<RKpt!VKoaQALz%YsLGbxkB8tOHHEdefK-a{;i;d%=<D^~=xLtw&;LVjGM-G}L4o0Q&{qp;dL`b4e%#>K'
    '8iEMnc~JAa3zS%F7<soGP(P+&Ua?|_RFm?r6yrr8>>8PNjbp*7NvjxYg@dD)zJ}r~egb9z*g<Ue`2M>~Twq<1lOAqy<<qO%lH%Gr_EhK@TrAlr'
    '!bmnlZ4F>>8g5K%4+dNvjfZp>0WzboYua<wK9n(i#L0h#3>aZ4(*V<LYBwjP0nbZ}>V!3cs+9~ua%%Zqg>}Vef9TrZ;n7LwQgZ#eK7J6|(r$TL'
    'mm|Z%I#gEqEMwP>tQ3WY5gS94ey(dm4PadLf1sD$+vPU(LXZ-FtPz(MuL+f7CWbSZT?@=#w(B^Ri{pfs$&(LXU8-2Gez4|1v!8YY%EDCA-V|Du'
    'J!*oxQ%5M%K|Dd<q6#i&<DOyGSBgtCS+$d8=3?z%RG(QokyoD$o%)9Og50Q@GU2EN%-|y}(-?!J+l^W!YOhPjvFj>9({tCbgXJ`nAuYw9qAM7i'
    '${E*IExY}2#4%#@;$;NQe2|>>5o4>Hdqs0g2fDA2`_IP|yPka+kC=_-ZJm67J(9}_-zx{dLF+%1-*RrnC<E9@HnzCoYiS}N-svZ(l3Xhr{{6|Z'
    'r!_q%z|%Y0!|;^IA-CwkQJT?m{(>Xq8c!dsT#k=%*w|gXP(2<n{?sovh`y3RZGn0j$TjHlW2HsXsZIhzmC)4o!077f+1vHVyRT@pZJm87soW!H'
    'E5vt|o{!J<(p9-V1QCo-<1Uff#88t~aGHwSCX~*N^4JFLgPP)dD(Fz~OlLoP@}nf22ebhJi+BVMaW*=4?h+~%zi@xqR7wZo{b8d9z-`mzesXDm'
    'zFRQF@3*$sZY?w9ipf-uq2+`ttj^&A&W}%(6`Dn~2`E%S_$9DUH(JM<yBUA02l{DgReE#qc6*?jMdrx5Dg=<#41e+jYFWMH<i8!u?B~SQ1}Nt;'
    'B>{xQ%UegL)7uZeC~A@n$o`pVqu#}r{ypa-2JXEYbv+Aj`Pjw5^Y6e(Un@e;`~thABHhH#thpGCoNuF{G&!YH0GA+Ra$byGZJMN_TZg@W;_ny5'
    'h_NMFB;{bBdt`dY@0j81|H9H+S1Wb_Y3;pUM&gDLTGqQOq7o;C=a{ZhW^?_Kl6w-1X2YRHn^=#zi-*&*Hu;Yvt;#+%RA!K_!3N)c`w~i)nzZ!Y'
    'wHBZmL*FAHp7BLYAIJ!8xe2_u1fei4WK-~AbL0bBx_8-pzF{v%ogcs4_$iBG85kpZ{@)~!K(n?@a3CcCj`9@LC5OJPn|tJivSM|QgWK(+T6{T^'
    '0(yLG<=YhC0dqe>xo&-x5)6VjvEXn80;!D&?4Tq<@s6#x#35Az8pq!3(Ax1adXg=VX}mljCb`v#64BUUzXpSdT-<-K-!hzEIma^Lc=Hj=MI<0u'
    ')IbB6k|pRBnIdErU~{fsnv4u37!z-#5a|Ld-_%EEM>S(XD=?$`P5u11FR;>5Wuh9+d((TF3Ug0vf9v47+plFkc_HRSYr9^j>zE8X{y(9M>5gX`'
    'M^+ls{XL(Tr)SFdZK(S+pIbdyhHLgTYN?%}bjD`D7i%61IFZOq78av>;5%+5hmA`ls0gr?bJ~zNa_ywN+Ze-h4j7CQ|JqlQ!03BpoaSN|YiJmu'
    '5<K#|EUc|BXy5vlbLEA<`eTsIyImIbgld~m^Ah$YQgvkK7!c4DnXp$jyHXLlQg2Y>-}mI9#TLkq-%8#wwz%4V^`}7S)Z~Jh_FF_-5bX6I(?_|J'
    '4o#oEa(NwkE;(LJS%^;AsT`Nek^O=AL*)L&e#Cqi@!l`~b16&}<d=bFdLyu*a9K)>K*`=15|R3z>_4{2x)oH%PpyOED>xHncooJsLxSsC(J+^D'
    's{!^fV-}-^E`_1bJ1O0%!!bH}t%wF}Bd2IfwWzsp4q>SAqI1%*7(R!iYB2DRY2K@RTZBfX#YBe))~|B`WOGuGmFI$MCCoHFC3!A=_ux`6p(@n^'
    'Pj2oVm!mk#(pxWJ^DPFFdqvlZ4{aqnVm}MgOB$26m=%Q)0Oo)j=Kwl17rBmPE5rj1RhN9fJmZDCqLlzF0~XhI62!c<tMw5bo}(0V;zRjqo#^ET'
    '49#~vqB@?g&|%*Po}`z#g=Gjv#5$hfBda!A2Sk)M5<ZOT9+~Xrv-rpnNQ*%~OtmTJ5L~L%RPk19=#EAArO2^pv}P7~%vs8pP@B#|4fEgCh-&wQ'
    'n<qbuSg1*S3m$ZEWv5s97fz;;3vlN!8vlHn#qEan3P(p-udW8a-ri=W$aEvbqoV7NcpW-~>w}cIruKg*sPG${peSVv&6zJ?*;wKmZ#Y98&E_{Q'
    'TgB>4b9)a!%@z<52q7@(rn8n9)yd9psInA=mdBoCrxy%qf$EzP+0Vh}xCW*sGFx}DGewD{;EQ}hPEqp>@)PljI``Bihm!52+ZggK)0h#J^>1|b'
    'g&mwT41&-@_>LtFSyg>=ay<olcRE!~?n^YQod_ZOH%@dPZ+vGMP~rarF)ECI5v<<J`S_!oU@iTe%5uK_YTEv>X}ZOUj~mJGwieW~9wR9zVhYd{'
    '9)x(G4Oid%RO}UG=zme0{(D8HEA>A#bd|pewILxB0#&YRdENYvhUx^&<>Z+21$+x>?tL8TTph(b{Lw@QdtU|MQW;}R4`RUAMp(epAqcGy=Ah|B'
    'w=}Z|nA@!hyL@n7hN?ah37$n`S&CsLwM*MkP4ElYA$Vt}x=^TrgK53twd5pSr4btyNzi#tbW}|%EB<D5VW%Cat2boN8j-jM1|8K7;#|_>GY3kL'
    ';Hm5Szfe%(&xznL8`IP>`_5hDobIhUvwOVC2F2_@DhfO_W`A%)MrC<`zVE!k(on6rIe8$@_21b!lG*c07XO(EzsL`z*zl{%Bg)wijAuI$$`W}%'
    'Bhl^-RAP0)Gx6f(k4d(AoAWzqeJBMD6U<p7-(<-<o`%msy;#ZB*H6{ahF69>=k`d7FAn1WWSKnltqfytg17S9Solty@3qg}E_gJh9A!B(Qm$51'
    '>vf%U)d+65&E=AHSZvVWyrr2i|L*TJ`CsI%0T|}-2?>5Htn>I(XriUmpvLNlr_KQQ@ly}R?gB)WU{Gnu&8z?=CCu7>Y3XxfJO_Yy`MT?7y;Bbh'
    'Pzsw;zZbgQX8N8Xmlqn`C7cfLIS^(2<lJc%4t@q1{Qbpw@7)9kB_|b%XL|jY<o?&~nPszJb~1HSYHlJp;_3w|$t>;sc|?hF=buwY(<5;zhMQfF'
    '#6Nd@g7ez#{}G})@^nV>R$hc!xNOUGfR7v54;+S(7D<1M)9jMxKvvGi{>8{kx2YPz<R|<Z?Joc2gNnsuDvbrwk&p_bF!Cn+%yS-hqL~K~4J&3M'
    'sOU=FQIUduQQ&cZZwoax+y5>!P}9`^ov{iM9(&@qo_AV@0-RsE`OW!nKey$SCOwu(1(U_mi);&&@a|lC+NNnKzdGWxyD7Xb<`}+azmIodSdqwC'
    '%zKFT*!ug<tX$D)lQz)t8^Wr)`SaoO&X@?q)dz>vEEkqlYyOv~Is4LEtMK@fXJ1edw5|Zf;r&`SbZ7tD7_n0(Sr|<>Geh^r`xcjTcxJy_;tR@F'
    '#hvBsfjCq-m$v+_Ru!F~i-&~@M7oDaD`OZoI~Ltr|I)2=*$lxgwTHGIO7@kSTttYc96l@?#Q*n-LzZ7N1uk9b(a$*;!fdV*u11Y5aEZhq_=kjf'
    'm<YvMf;u~zINf^`J)ecyTu6TV#FuM`bwxipLyLc7PWxuZ`k@QAY&+Jpke2k&h7rZZyC@}p0%lZd4}?r6_A0^)3<&ZoFRZpL`dNwoQVn9Uh9C1y'
    'cN%Rr9DMp-`q4I+Bav592s)$*#XI(FEzNLf*cPCgr~3K$d(N0n(2z6AqXj33N4>I;>^9QYLtd(X3>DLFA=x;JV&rI{JII<C97xJlV%v$6aNr!t'
    '0qF39+_@>ZIA~ajbJs+WgZg!p^bG<CJXuKYuY`(jyVXw@Qg*D+F}px>^d9>k3;4~#V`+PCS?gMiOWMUo7njof8?kAOPOPtoNU^;%UsT7AB-^Wa'
    '&2O+a%mNplk1s<30BJQ#YmyaK7@4sbs<bxXk9G873`>x4Q3!Fw4s<8AwdZ}-R5^Dgc+>jisUbedI1SyLNNCxH5wj7>mU}$=tT`!W=3&m-f(K~k'
    '<U^A#CtLN92>t|^u00YQEC(cd#cNCRD5Whk?Sq~U#qCc-B&jeCFIGQeGfr<WTWTmg*m9Kg?AhWr&&7mPL`asbwW_Lt+5)8{8aKk(mh6>c{bWs!'
    'vCZ-#-&kp|)gVe(=f8z+tR2U7%><W@mh^8XMn){4jKbL0g_*s2X>%B?Z(Kb}Oj;yjy4lAJ`>dOdOn3(gt^}82A&KT#i7ndVU8kqBK+r_jP~fSI'
    'a`s=*e9?A9(#Z}triz?hXN<stn)zF=yaEmkpzqL?!5v|d;RRO3FXB+>(WGx)xkbt7iQ0I9F0gpaCjl@6L3v}AW-EPQe{32rM)w0z2IoCl;#%&g'
    ')+WXpEP>W*wXQXv(4a_cvo1|e^RiuI4lR?^6o|Z|2VB6MwO$&((_=Q3`L-uHu4rIO0>Xi6@jGRuX2Gkhr|0elpcAo*#_MhV5m`aH{5S&f-S@K8'
    'MI=<|$Se`4wdrTTI&sl_ETf75M77iY;4iDaM=e_vI7-ostUC?Y2kQN&`yKorB<*TLDB@dWm7O2^sgR%M9G3P6LcIgpNj{2@dX0eN{)}0_vMs^O'
    'wQtqT%m2aoOTNGprt3u6RC1`7>f_+hv%fsQj?Dw9&mBIN@j_olnB&m{phiB0wG=xa)a6qZfuC`a&%j#pRe|>h7AnuLDpiA9h<=Q7D{$)56Ec<u'
    '&<`7}1P@WETS~}SB`oFurOzk(nH?{!duP$}94+<T@5fiCNY>g%qeIPHr;+E{o+*;=a}W`M@vsDv#&vLy1xdu==XA=-vaMe*xe(TP(8CgFJU{{M'
    'YeP~Po1&o4clI;GeL3s-=M?<zP|nxE@vDdD^3N=x#wYQ0GeF$-E7z18>SNU#00^h^Nm6a|=^)lpfzP{1O0^G-hQW5F!w0ejGr9ClA><%J5rRF^'
    'jT-s~#p>s#h8iKmk*|MS$%sl*@JQe<LRTW=8XZ2(oEa(UL!nc^26H3YYdO`jRVmoGAVIphZ|jU)-{W>hVcI&`4$BO!>~iS@33UvdVv$p<gdK6P'
    'l57|D3l+Gv+ItT$gn0tNpt3?L!_o855eeIg<JA4Q&2#gTP>N6Fnh4_Zvw+)q?%h~8Eb958o1?R)L*N39v1C23k#>K{B+txP)sNObFBb+|tUB1c'
    '(H=Ih%w0CYRa&h?k1en!ku?)<&<fT7$Q-kZw3zrF2gx^zy7}zqra{QhY=HfCAMMhuS|K8WTN0<uoVp$n+aCb9iF;hqOl=%Q3*6Z|uLB7Rh`Oc;'
    '<e&h<8%7TGv;?fLpmzi_IRjQBIg3N>TYRLI>HiVn5NpSwA`t(UJjU8&-qWJ`aVIba=ym&LSWQin6ah^d>?NgV$~|Kl3-pp={FUG6Jw&}Ge2i9}'
    '=29g&BPVbFI7Uq(K$ZYic<nh-t=yTWp2ca~^N*lSGclNKzovTeo#G4r6Pa&8+b5JHjDc;3gWtYqSiC1=l88xHuEvbyxraElEOY|^zqbGS8Hdeo'
    'eKQM&BfDz?<bI8BWW|sG`lmJiI)t-7t3b~8Pb7TSl(&H?w&lexa~2(`{=3Qi#<~#b1U7E*23QopFksi$oz!TiNC7RNO8FQ(d(BH;*>CJOJ|<us'
    'HtTEby^tH+94ID|zyQTGNj_saK^y%$gSi#AkYtblIH1a{7x;Cu)=?1#$Q;@|8NuHGeZ^{l6RA%cVcHNii<%%bo6)kV;EMh;HE@8^SPx$j;9Gye'
    'EO${rqu#>1KOYr(EvPgso_`I9Lk&dTWj0T)&zteOXg)3O%c~}r2q1KoaD|1X8*n@vO(6eX-)7@UeUd7_M-vNQYVPkQ>uw$KNzq-_nA8tiBX$~~'
    'C^3K-eH}t3Hy`KbQVJiU)0AAshdxot&@vXHY{Xg<L|GihKEpIWP!|Jpkuv_n>fBhIS|2BM#)OmvM$WNn7&GHZn{lVbP5&1|1Lusi3e;}mItGrh'
    'njs-{L(fI!@vsMd$>>PIvdFII`@0?36>~se(W#N>-3;dk_8AZz1LD10sxNPzi34RX3{LIv@)TB*1B^1<_UZmKGP*ZZntRN<l;$Xs2A}9fzq6G('
    'XL@_Dyu!OazskPbVNrwCU-;5ynOf>Kwdo&2R?Y=LN?WKe-Ms^#iuG_DJCX}^4LN8Mm~L44Zl%FE5wA%eQ7#zNLBZ??ON%Wp(}wqdc{s(n+;+>g'
    'oJfsGVYCH=Xu==7)dqf~+zTkuzI9oG>T9&~%ht;^lC1{OyeL3>MAJO9ew~dkV+KtJb)nQc5<3Jhr@VLg8H7^_m%|XQ!K+_xEj_$#fP}{im9@Js'
    'jKG4U?(_8B5`{{s`odj5-hDug?8t@*w#=ORV%|;9AzJl;8lzZUEhB8c1OY5Dk105I@2;{v&K+#~-9@3j={qaG*|^b1RM9{P5O}xZnWknxS?wWv'
    '5=Ao7=;SClA?747kOc_zoGbj+i?*XYoR_4YV@OT)QF1qeIYHn{#}YA`kpn1&F=oqZlSfN`Sf!uWO?-48_yKh?jG;q3Rq3^m%p?TI|Gz^Rq7e`k'
    'ofA^2l1#nz{C6toI#k$eb3YS>bJldF2zkRC{ABb1cxAuxik~x%3xRfV1NRs@X-$MdXGX8HZy+J~qO2n#t6NVp-zW0wW-r0Axi$z8CF4ZVck-Uy'
    'mxZ#y6+!A>nXkY^84ik5v3MApb#PcpkF@_nz9^Uf_c5(8F>Ud|($mdagLqLc$i`zqua7WOF>5)f_Cj2&)09I6uvTp5yk6Dx9|7KjtSWiu7kJR~'
    'n~z^jTzNb|qz{c5=%7N*UKpp<O~F--)MKon0br8MTkCWj-EZIMqDLI)8b}6FJK@-cYfmxmPjEW*+%y#Uc2S#sD*3a*(<qGy3PfIiiA1)B!5>RV'
    '$jBIBif`jTeChjGhF&KG4yQAcvT5$Q5EP`bP9|TjvJ<vn-|Wr;+f6Z3qoZy;bmg>*=X)5LnM0fM$lWIJqiAZh8FUi-$s3+(0q8GAEyi+f#+*d@'
    'K6y+l50bmG*9p`b;>y|{yRuxD;V~ua$*p`$1Qn0kRvK=s?JFSJj{GB4j$@g`X^@ij^0*H`ME1bE*3Qoc`D{=VlFZqyLW-fXnnXYb+KBJk`P@i~'
    '(mzu(1bKb&rO;rHdor}4TY1EDsb`@~U`ZFTOx6kbzSh}#K}@N*Ci&&3?LCKu08GBJLZ~u1@NoUi8Z3)BF&OA!Oa;HOrgI}2f@Y&T;i3zTcnqW|'
    'AQlHqxeCRyNQqs27Wb4XEm4ZR>-cY@ef0mtq`N{-w&i0B`Gi$k>S1%i70o+j6a21?qcP8kdm929ee?vKjq<ziSlFS{d24MfP@8MvBBmlJQHFtt'
    'F?Z=-7vn5)ECgbm-s*Me+1S(falm!9R!`L<Mw9acCE|oZR}&uy4*%t!XRv(~9EYfYD53vD3I_0$b7x#mP+zx)&vu-AeGp>Y>a;tFBuvRRiSzhs'
    'wtVMA!yNv`+ma!n(V-SHTa?aRW@T9Unh&D<78j*+X_3r*_WP=uchWa@NM*~6O}0*;w$^)ZqhdJ|QE0t&21mKQPdZ~@r8lC)5ayj<;U?64Ims5&'
    '>Bnz%K6(Gi(_}@URv5doz7l?_QvtE&&qM0Zo~OYO%PGoPx82WkZ1?d;?ee!<G=k7#TxF@C@HTPn8`W*<YUkg4Ua}s6UvJP<Oax@UP1zSE-a_R_'
    'DV6Xdu9^|yKBlw5r)r{C>q7(~v(1iE)cPITtw*wfzAo27Y>ZIK1m^a9-w+o>UG**sFi5sCT$G6%y44sJtUQmfEL(qaET<B{4(zk%R+mR@(*d%c'
    'G42C_ol)3PcsxeajAT;{tK~w3dygQTdwGG16Xl67JYrS+xp_M`2<^c4Y}fWDDY&*(Su{(wv|FX6Bb5Btn^Btr+Ctrf9JHuNpoaHS8N_b9c^i9T'
    '1KaFqFR_V0bc$8=_rWlTvB>iQ(J;%6JH|z8xQY;j-!q3B6#~n6G7NbHX<hNK3!#8^mwhO?(@pCg7VolZ!AKQeb8q4#%XR17iE&Tr3UNS!B`>#('
    '>xwaPRF32ty`APyYT*iPb=MZG%8ouSx2lJR!JzA{k87CW_xxk+z7`vm{&Vz-uRiA^DE7=VH_ZMQ!e)f?z1gr^mYfnCpB<nT%ct@NM2zgxO2h4y'
    'JX~lZmrV0ZU<<LT1leKGbpHDP75U6==zF-<RH(rb4w(B89PTsGEl0^2eqn+ExV;wX{HjYqICly4n1uI0`D)Jg)tDI&qrHhS$PtxeY(+P$^-xI_'
    '(0(Z0NGDL;HJHKR^3opKDd(yO^(h67m{D3HH^1aNRh`K=l1mztCvYuV4o-0SBj<ek%z&<1c$LPzs$j({?J9$_-48Gm64QFNlL#F*;{f@fplv%W'
    '*J%{PLEeSWembqo?qg@nSCi4I#-uT~8qM_`Q`QRE_2C-uXaYK(q@X|9CMwuugdz1&XO3!21pSV<cDKS(G#=IR;buX)6TMp}FmTRSjgS_8P{a~e'
    'gD7o}VY-cvE^V@XgkqWvcCZcIT_w?F^1$yiS&#8qd5@7S;Bs(sSDjkck!6y7rL5I90KD7(iO(;aGr2LGu>SY<Xpu+B$3IM#!|(C3`mxU`brVI8'
    'l3mVh01{<kq?lQLLJ3DHv4~h@2E@TnfA4$W7%ys_9zSYUuuQ$Ha`7>f!52Va$A1S3;<8lHo*7k5d+ub6?OCO>UIrvmM^C;$BhOzcjg4!IP-$*V'
    'X?hYI^@|y^Y_6GPb1R`tslo$f)8%gp6+ti3O%$&3(M$&x%3x^C%3a(OIl+4i?kyCEkb*CO?(fOaqLAypl<l!4bs@)GR|G@Xjwr`v_r;W6v)gp0'
    'KM;Im@oa(zexO!X<N2OLp#8NdO7(Omb0_hd_~~E-z-@vibr+|&7j~J58#tm!GmO-BgE>m^=$;V*9y6r-3h5QF6CM}6%63(W+w)JC;1SiDvNII&'
    '9M0pdjnOSRI6IbvNT$SkMSde$PPni$T3e#=8a6%ulrD2y(e}=Nsu?9*Xoxa+x>k5?xL6s`g<x+L*MKZcjtoz}Kj2nv&tYAm!j?;Ct9o#09ZDy('
    'Y=3!4i-$M0v)FJ{4e%OLrwD7SlKC4;r1n(O=i7EOs01>LCub(J>9f`#wkW>Cg&O#M7JnK88P;>-#D?<9xx0s8Yge|&9pp5;=GtG&w%ZhlX2@{d'
    'tB?k5>eC8q2|j58t{(=S{Le!abTY;|9($jp-LUtX&8Ymnkpi!-$7I&$SRT>oJiUk3o{?_`3OGXTsnMdHH-jg8xGi!MDN6_Wf^Ed}yesNN?iMEe'
    '{PAOf@RXvv)BJ*D>R#`nd;ezJ79qd}YTY?!74Lgi!Q1uBo1iefJP?t48_8q#04NHZf@{!ocf0O*F5=Esw6gUAfyOu^D!<(3OR&vK@hFfl?4WlL'
    '=8wtS9DEQwB^@V(%GV(I6_Q(REt!?6rDZ@1yGlwbl&d>03<brgZ02;!NmwoNe|ob|jPz~EXlRTTIB$T5(^k;Pv8W!2MPk?vaL%lm4l0BINUA%+'
    '?Xd`3i9AJ|*hEGDNY}E5Z+(psG2cfnaD@4O#5qGYGD~IO0ph5)lxVQ2LMmQWkh(||bPdJEW=6>tM90!bH#Xo4iXD8<kWnQfgtpjE;QlV>h?UyP'
    'YW!I56e+(Hq`+ZSB+SJWb=J?#k+MN!ZF}(SX-OxP2OkN$wp2m!YB-Fz0C0(cFS*voc>hOeUETDQ7f_+e^q^N)dXG5Vt$2@+>+D)(qyCyMT<yj>'
    'M0tH$L>@uKZ3LVlv^BBTBs{_A5e@u`@KgXYnMkD~{ms3i3eaVpoFMcMLZnH|_hbm78j1hX1nSfXLQC>?a=GgrSp_|&0CDzD;kK6T*2q=FBn(!6'
    'fkBwhpQft0|M#yE#9#YcMRxTC5=eTCvHq}xlH0XxOp`|OFd@XLVD}oJ>2k3bPEEiv4pj-f4ht%V^pj|<Y2`T<z_%g=8R1YKGZE>LfV}6}I#2}J'
    'PHn@8;my^7_*^~VE?`qYx;}I`7e-Y4h<k5EAX!^RW=oow_0*KyGCmp>&9T;tlX@EeQ(ZM+W-P6~@n8IA)DCQtv>Q64-e#L)Yl~8Eu)BXCJ9=5p'
    '(ZRo0FW0RrB5i}1BHWR9w1I90A>&qZYD%>zH6)-DyBgvz^^cwwd7Z1p%(p<S&<*P@1%(W>&ml``Zr{}!%=H2f)l0w^dIHKz@ySu(K}f)ABJ@^m'
    '+a<<2>wmuPW|t~MR2(sDSbom(Z!s3^O2;;^FhROtr|yuPK#PgmXFwV4xjPkc2G~$ER1oPa62v#)c9c>Y+?`5xiqKmmC_zi4-Br}z%~=H8)lE5D'
    '>HcxclFCza3<&^7Rg2~VWE*}&166Rtf<zcO6r03D2QyZ}Ke1=}V7INyaB<gEyj}C@2ncZ>YcLfIW=PQGbCIdBtgBy*r9>xw0+d7N8`+?0Jj$*W'
    'BnH6X$Ji5b9pFHJrWL&3Ko8Ig1%dav$x8688f=W5EO?WKI@g;7)q);zWl-+|c_8MI*3Rp-b)v&r=%QbOA^ii`s44_Lo+A<U*W=2H0$|ucU9A}H'
    '%W+)Eki`+U@*WtY9ENfvBS`yGmvffQ<uBecDVbtD;b%?AO9Q0EqDiW>blJ!oBDO@=^l(OPC!F6ymM;-Pf@wL|LKE|>iKW9w8F9bXmqY%!Fz#GM'
    '?u0z4>7H|n1Qq)m6|>JhVoT1qQB+c<D$ExZ^1T@UiAm2;5ql<6@q!u_Cvz5%at$lc7H%u`<a<x8<WEtToQg`I%tE1o(fl_%0Cu^Fx_D67b*$zk'
    'P9hG=Ub#{xrn8W;fmquFQpg(*#VQu8EaNta@z<)_H&SYMi6f%R)c(gjx`%P8)1!LRtrXeFz*CZE@vsVC2jq`J;)<c4;cy>K>Bfxw;5?yQKgLsn'
    'I6Yu(#41nn2V;ApYQnh>AemFu1_j85CxaWPz`-Z=7w$Sy?$?!t`@!m>h%q`xkmKDB?bhEy+`x`@FFam&PJiN|lDH8fj)aX=S>bF{$yfKa#Aj-Q'
    'yut#Ol&oYM%b@ITQ2iom*i#TkdN)~@smdT3j!_~k@#{Rm!%*OGFb%QF$q5cE9_+!t^R~+T_kO9CW&LdCtE}<RLnESRwxikCLt)xg25&+~@V{1j'
    'W+35<Ux8m%ZL6Q|y&oL)bctFZ0y8gb0$E$YBI3aC&J)(&D@6CaVlZte{UXKWr>WJaz-#+2X*({Ug0VE(em+UHtz|%q{gh)WXSYcj1Y*U!^mZ-~'
    'oFksgWb4Wr>S7H4V>J&??O9Ecn+)S(%(KJIfeOOw277C2NQz~m>WPcqkZ@Dj%p#Un!U|Lh#4YSCe(LEv50IT#87c-Pc|uAl4^?t-P4w;fTG-A7'
    'hMOImC&I;7@jcw4ClU8lz@zEt?PR$EeS@kZF;b2i!)(aP!*Wr5%mr(b*IBgrBs}@LMQxa%_||J=AHxXrCQfeOjoj%)vw+mbp5|ul$ibNTitmm)'
    '!HiomE%qBs*tO@n8WY@^$Qy$QASS%<Rb@2EdS~68O!o>q9TNoA8gGGV=WRlQ`1u7(=g_q?(H9BIt{_5&j#iPH$z+{wcm~~p<D)Vfc0<|MsY4R3'
    'C5!!RIKO&GTik&Igorm@q;?66-ZoxON(6s)nOFX}Epl3}6(|)%QFtH8e6TqBoMs`XPHa+c5PMNsGK?;c%ee1i=$rQN)c)cP4L&YJrkh@sS0b&F'
    'UmjDuDHAPKjVe+m_$~t%W#?i50YT0$0L{*vQ;KHa@W!1w(JUj#CQ3(kfnANv7_r!`15TTkQf0zcax|XwbsCC?s9w~7XJ4r}V}KXkl=}w`TUC!_'
    '<UB79MkH+sr(h1=JOQop<*d#z6+XDQE(pBR=z1iiE<@hXiLK5aWvS`E9BV8V(hf%2YBbWF8LffLQsX@}LgUG63ejX*9OeGI3_c@}k(Zm&fMZqR'
    '-8B(w2-nPXoNQ>;C7!9|IP6`M8Zx{I0CYVBhR5mRgdl-?bZGoYyQAw+aw4S(zo24^$@KlY|BUFYw*!9Y3xF(b#!pnpdU!^ByLnrcw$_;t29?gQ'
    '?n7F2KPATUgPU0fV<Bwya<u#ma}S!_39bdR>FJFT^=rD+IeBY?6+3mYAKL^|Ur#J9Jv1NG-u8j^>R_h}_kX?3s!6BTcyANW%l8Zh+kL(*SBauT'
    '(IyioAIy_nwS4NFNvw)?W3vyanf4<$$TZ9C8g9yGOHq&#s={-E#?`DQ=5f)gde?)%GrWb253|tN+?zd(b?&iETxG;U#ZMk?%Kl7SDfx+e<xE%K'
    'l0}*e7=nFIT_4<^*dz*T&}>~aXk&a6gIdU*?MZ!^8fwORf*(j5HZ>3}Be;k%+JS-DMzgO%I<x5B<86K&&ny9Ei1tWzx@!YPl-|egPjQDyhk%L-'
    '?$rmNg}yKyaI`)QOY#!F4Bj&=%B4EoV5ps{<GOm7%6<c9Lcio>Jt#jJlbYqSBpjP2@hM12mhWm&6dyun#AjIj{MM9{A97fhRsQ^6<suhCW3CYY'
    'yjeg34?m#-3CEV!`aAe5&6+qdZI2u0gbfh4m=QMWe#%bbxDAbEp-)<CiyL?CVKV3YOkXoeRT<S|=X;!A!HRz<#O_l^lH@RFy2|G@U=n1+eSTqA'
    '9Fgh#d(Qgg$Nj@l&tT+^XVvS%AxUvDS|)Rh3@!OM#R<}gK&5tFh!;!~{y%iKk<Y0vH63w~k?YhMT{G4s{mv>y#J1{aeYK~7FFf*M#Wh-<-gQJ9'
    'BSM<29bkALzOZPzE_*$<-RRzs7=ofMW=<AhM&M)kGH4U^AJM3|<`|r3HL~RKr=FlQ{7^Ja#AMw%BKjW-&eBa84Pd)al`q&pRTJcjvkY<|sB{sp'
    'kE5V%4_`YJMscT+MkEtl>)qU2jP<DWDR$Sw+NkjiPdG*OPu@c-=Yew$T#-pff*5Zaw#J!;QjunobWZxn@^&<ix-@D;j)Djm^(zpJ+#U^&6RF29'
    'L%3nNr5E08ruBT-nBKUj7Z9xX#2!IS!(d2H)s~%mZQ$vvKV@yn<|Apb7jad**~V=E1$Y6@DTxoN6wGE*pDDCAs<+$yk~%u@U*n~_t9N4iK&YbR'
    '|0LMQ^h%;jrQ^bc6A0zura+PE%;RFVqF)ew+8z!y&yxIPBZpY0@ss$4lFZ=Hha7YCYRgyF*!yjW<nTA4^!{*!TK1|oy?~7%iYZj%&lo_Ww~=Q='
    '*~neTSY<0rlEm?0&f8zbgIcAFp?Naq-w{ijo}BGNJErK@l2m%dgwDcPznJA4CI4bffw;2lfz*Yq*v|^P4^<=_%jX-KjV7~;-=WEf6wk4}bVWdF'
    '<CQqB*N`eA3wV8(W6TYl78$70hvO0E2=~`D&eX&)fMDU8KiH<C4WOo#wnXQ8LA?@#w0dEanFo)I)=OGT_+0UVRvC8EW!xFxkXPk9_d~aIOK+|L'
    'EU4dq4xwD=hFq+gaXyBt19%(D&<Rr4UMa<6^R}FM1b9rfc`q0J_-_<`&Vk}nm3<20v)*Hjfme7iFV79==&zG6XN)xm9i_YrxqW7G%KZ5}V~idg'
    'Se1q}+^ehuK8*^}Ia<LPfYk3h4)@IgfM721HW?&&aL%K7?u`sHTwKrP3!ZFkpcYbg=ZPugO!YAH%g#Rg7$wMQ@ZAw8)fqGAV|1qwPK7B1_n6!&'
    'DXSsgNTt{zr^!yZcDx#x^I-#-SMo_mM&k>XbP({wo8Wo5Qp^nkQ$u>f){7bG?tCzWrlsogckCl%4=W}#GCQ!@trmtq*lRUe`V|m9&!tC>*h9@T'
    'GZr<Ny0b)RH|lM~Pbl3~u%Na-{ca4U;7}B4TuQ<831-KMu)AE3^85j61@#^7`BMqg|AW3&j0xg6Z3ABf5gPjmBy`3Lw}I(dE`gP1@EaQf%GA-b'
    'D6NQ2HUs91b#f{p?5fzhX(J2b#<BZO=T2D?BayFZfg(9kUX@d;s)}Ep`Nw)Sw=|%`+WqkFlLSi?b%x1r$|zKYtA=EeDt1N&y3giP3Du8RLSqCs'
    'VKUa@ZbyABw^MdxEt?(T0N^>(ES2dp0`J+HkfM2P0H$I!Dd3k6-;5y`Z(k9U$lE$xC9KnhiFKz$eI;Gmv8A@q3Wdk*<|69hLH8YHzJm!`-(w1e'
    'soJJC-7Oh(l`i;@B$Dp&m|ny1%AsCybJneM?kVJ+>Y;aFnE;G%=apE#6D0hcWiUIuKW;f_p(acMp~8_=BgiXR60>P)BXf%k1+7w5$l%sYCA?M_'
    'E>F}9qLYilBy&MTPKTdZO@7`FygF2p+sVsU7^N4K;e#aVT!}nkNxo@YuUt`43yc0s+lI1qK2$5fQVJMKgJG+sTt}S3JvtVss{~@!z=5A);eUpM'
    'kP$bJ=I7g#12!4Ht2fn(+^y^Hp6y7)+Tq<)4C!f@l5<CFaB{`6JIwpVrZq@2_9Z*g4hxjgF2plg=qT^<8lZ9xaBvamNv@YE)i1|R_){iPbvWcO'
    'FR6@k92AT5m`AqZdOy$H;DC%Tv=FQ+qwNg^b10vCk#H-XpB?{jfYT9vN)E00(VX?&u$GbvKu+jTaHQnte?+C^23^IX<O)X<XpsJOG&Gj*7+QZt'
    '&t5k~`FjT7w+h!mJ$1}VTk#Df4-IcrVJm0#R8Kvn{z$qS@VOOcUg6gd98B4aO!$K-T5W~^-amcY1J5<0E*eEmOcZ%ME3Iui47mId%h9-=flDm5'
    'iN?cT<k|d-zvbqF&>oyQ5L)`7QW8T0@c9si^xXy%1{H6HOe;cVf)!Y8cs-IZpVMUcy2za^_!@S9&N|XNbWjd)tt(ku{n8HThL>pdqmcEG3pjhv'
    '?h5u+<c*ss*ovLPV_>7Zdn$N$B{3fpe$U)6?fJ&GnsIeah9|E*S)UJmE3h03s9Kd+2Fcejb;xJ)OE+67UPAnrY5Qyry5AH0`>iU63BdGKWz1ga'
    'ipxOqC4r!k_^)H_+s?=_^l5aH#}p{K_G80jQt5pQkDr}#7l1#PRu`d_@s+~Bs<xTI!8OX4<~d7jfXG5Ft1#C*051_mwH&alE3lAU4_!!6Bhw&v'
    'kLME!R>x<`G)ujIAyHzVc{8SmPA~;vI4E=mZX%ibzS(^OD4EOE6y;EDN>fNCBLu?N%FuX{Q4-OOU)!-!IT!gHf`k#R(w`?e{;guIg~a+hxd!j_'
    '?|UO$Q8o&z@S&TszODj4Mt?p5(CL*a0Ht{DNM9t0&AL7CZZ_7f`fW9;{<puwo3an!53kWgU15qUV}}OM3OLP;X4i%@>PTh4uk;_Y6er16;Orqr'
    'n6EsK@rw(wf$*%u-zE2B<L${}BsYZkkfvfyn(N1v6kCyPeXUTGmx!b<GwLRLH=bGqpu3k0WGYR_P@?x=1LCo*f3P-iMsD-`Jj;S{v%OdunuJP4'
    'rx_B0#lcSVFjq66JpGuB8RV4Nrmr+dG;@daW_boQzI7BcMpQFa8esAx2rk8#z^z?U)O`jPgQOlW*pOu~bl9P6)=JQ0dJEZaKh;v{Zq9!|J!NUu'
    'c~Iib*mC#uDYk@V-a`q0WoYX@{q)LfG6&we9X;o{ICI^sw1HSYytQEH2+#f3$<tIp5x{F0?&_m0;E054UV0+mPVLMKFP<rg83HM>@YCL!fyaM9'
    'FEtu>Eam$1Y?yDV)}x?(7m9aql5N;(T7^}u%sk;T?v6*ni5p3DI02LzHl#9flwseLoHI!*0=pb}-8o<EAby6gy@r$M_m*C|sa2}2Qjc%3qG>dH'
    '-qvduuktE<c=u+-tP_UfF#Cff%I7M}x%;sc1YID;sP#{!Nw-J7d~0ZIYV*4c`j2d1NMJDC^D_)~SEuaDh0m<xCK|mf;UN!M)-0enZou5b&|NSI'
    '=#S{h%}9CgW#z%bf{vYHDR*rqq9kF62zIIwlM~blB7zHgjF_>oJJ@;WRS79(eb4l1l@oXk8qKeV?{N**?U!gH=nz)&NDn5o8oCwn$n?G8fATvf'
    '<`#HT@9_E3!@hwUI4qWA19`97X-fv><`R5CW#JSsN+@YEP6#Gv7xuUYQ<J)+_=|#NNWdHGt|D|Q1oDAtpV2@E29t9lqaCGp*S297U+l%ck-Rol'
    'tRee|iiSp(I_JhT?`~FOOG3uidt=WZ5~1@{vKoaw-x(q(B=z^r#XWXR_PPasF0J_Z6vE`}4s^xlCd*l~(=bZ7D!qPZ>STTG48U4fM|x+JyHibX'
    'P}ynDV#ec2xe4fCxA^B6)w|HyrKp3~Em|@ro0i?UtF6v>y_xq#dF#-wT0<QPe^=CYyV0Q2M=<{o(N@u$diSr)wdai%N%jDNtqrL3*5n~alI#?l'
    'h>Gd1eXqx0=e%;Z44FcuLppKaBo&l)goKJW@$RBl&?68fhXwxdEVEYC-GJQN7klxs=&c$%RBXOod&X6>^sxx#8ni3+uvMHEYW*35=QAk1UBbj1'
    'i%!Xjv4d#8l>n?RE-ggpS+|6T>1}Vw-PL+tZ88NgS_ADs1@N(oPpF=y@++t6Hz}aEmj~O7{*U@<xt)}weO4&!(@~gmwf#E@g!Rto2q~Z!orBiX'
    'f~#F!#8=mt5EAD5Vs|&&*$KyqK!zADZ!yvliF)1ra3w&Huo)XPvuH<L1h;V4PsWJ`DyrfGqwPuE)Z7-ZEx!m>89G2KZ|i=qeGS*|JC3RbJOxHS'
    'q}pN~o3}UFMojr6IJE9d?~%~#%J`zJ$e=bJ+0q*oPT;~PA*}!ykA^u+7YWeSA+#N}(PjI0RKp-1<fIU+!DG(EoWmd0epog`d1%fDF~q@*UKeU='
    '3Zc(PXSa_(Y?Hz>Bv*2dT3QH3n4_oK)f1GX+AI-!y(`N8Jra&kE@O-_Rj!Nj$hW1hW%FC^h%#FN77<>IGQee4a+T6Or_!&+Fpew?z+q>9K=;<S'
    'H&kWqq!8a_DUh{XY38>m#-2`OQ!nZ`>P=nNe?O?Y<OXqjq;$=W5PF_9iF8eOXtry<u#ltCOP;L(!Y-<iQAPIGhCUoUH+9*Jgl;q&dKlrDmFcz1'
    'QW8*^2Op2YKfP<PeshC(x_WiAmEm2{=%0$#nX|7zYuRd0c7N@nM8icTmehZBYt8sjnYl?zII!6B)NR8rXa7{sM)^jgMlm$jsF9`wZ4Z)yP0nTB'
    'M{hmNCXQF$;bA0f$P8HL+qA)v@X(LzWKS$VzPKlXNIxzVSkAh~8@$P4BQ7d8{k^ZYE-IU=fp$W5BQdnI(PD(NBQeC$2K?vvJ?oU?wS42-?TT^^'
    'uKUbV<6poT88<5?fp~mv#l?|s=-T;dh2tD|6neiWIK16537m$h`>1}KbT~-2VnPMz-)W7lk@{53-YSFV0oYwsrBPBNF38JHVry;gIaDz8T?o0h'
    '{!WvZgN)?Wv72+raV5&RhG50%v|wR2JpFeDLP;1mVoZI8%m#w#inwR6(BVBfS$Y}7&{z$#GAyP$?M(^uXqjT;kR;FG|7Ltu6e{SUiSXz~<J7Ne'
    'r7aY4x_X0E?qAgnTc<|cbI-_`8UJBp(HF!?yjdq$3BqwdXw6pK<0bKTYe5tuG!Jd}8vZO|;XB9)fSa`YyOci!Lw|{+p-&YweT5kF8#N08^ak)u'
    't!vcEzwDQf$lh=i>9H{tTItV74RlHoXX%5YHVE%QGCW+I6m_@;95-KPlYqs$&K1_Ez-f}E4D7KxHPM4avWjK^nRO+xV}&BeC`ZqnVuz){gP>3R'
    'u8_-809z8c8j*`!U=O7#Atn{=IXPsHkx`xeg5WT)2DHv}KDTp=T7P{$Cy?qB&q-jl8xE7OS{@dZJkZ;EmHt$1u?^^ELe0fekoD4{Tko3n9i92V'
    'KEDhfXCuxyuS8QXoh~kN)`z30eD$SToLwX(ZOZ3q$s5rJ)4Y61i!4SNMu10JouS`eYxQjiR~zTW`p7>LLa7n=eUp`1z?vm<qEZQgPX<VLVt%KR'
    '_TKeU`uV&Y>BmONn-l^%S|QKrv}c(l>@aywDs2p_txZ-#pirSEt*l)dvF(Q!AI({-zFZsGnQB-IBE`)RMwmr+lQlVHmqu<d!^hf0$Bl@pR=Whc'
    'vdbC!60(VAiVjp=81P8v3)BR-Asu`ABSZ}hKG{-dFUKbw`3g7-@7S^kXkkfDT;%q^WWvG*HXw{HS+L*6C0S;Fid{FGMiQKs>G4Ls-8LmMf!UgU'
    'EG$dw<&7Zf{+Y$lVeu;N)Q)0AX{h5DY+pKwD6XenY8GU<LkO~C6J#h45Ss8f245%h>#zqgDOAO|rB-`6fuPGUPp7>u-COZ5$Auk~c>f=K5|Tcg'
    '_$5sM<O0_n3eJvyR%A|{4npRc@6`0&WBe#j;qVUW+$Fn~@t^MWShCEj3m3U6zy3LpG(&;`(OB}#rM>sX`msh^%!&yHfvKiBp-7$t7u|9<amzeg'
    'B;@${MX8p%7-rS)iLa|3@bqYgtS<-xqP>G(Waih2CNj`F*;O6WV|StZnN4t~gUj`_shBmW=qTfz4BZzRyTTtlH7H=LvQ(RN!jsXM7%pFuE>*<s'
    '%E00SgCb9jlos(f#mmC`N@)JpJU3gVZ0<R|>{>+=MK4oo0|K}{4{@%&ueaHK>%$NTsDK_L<PPB7o}hj7wsm=!-rYN0;mXKT6l@yp_zE3jFs&0>'
    'FsEla@7sVDVQbwwE*3me)4)KGUho$O{qDoUTbq3{It~#BUAud%m4B1DD>QvB_BP!2#?~&BCS`glD0AYIAZVeyi{c&(dv=DyE;>ko`QXigp@{zu'
    '+ra>PZ8_!Nnv_{hnwrRcHF*!ESjoON?S^zBWKV0Ilvxw?Nkx_x5r-fKoZL<-QELz2T|?_V8>~X*rNEJ^R_wgzG&j%KITU|Wivp_v%Djfy=cM6I'
    'pO?SE0w8eT1ez*$uk^nOgmS32b5t9!(4%+OVUF<<U?vf!>L7fo_!j6|8-)WYTCE&ellYN?<=8T%He9K$r|htG86UtQx5mgxu!|P2g}5whjkdcj'
    'NzGB_plze;A#Ks4we*Kllr{)w7j7-LE*99;L(I3Rb9t06>D8=(Gf2uBeM2@i{M@&W;C2q7adgBs=RbHAl=g5G*TW*y<{JvgwbztGh$bEM>6qzT'
    'Z2R4!9=@;oWBoJp(bZkxrAq4oY?rq+TdlMwm0d`tW!r2>@9KP7G0u)#B%k{r7}9bNk2;Yd0%Rd-&~ghi-@MkCAVudBA*y6l>Z7sXXO`OTh-a=?'
    'UIU}-=8pnoouwiuEmrbWkDM(8_RS?-EExWzk{LFw78Q&&w<8|AXQQ9Ul*gcJkD~retE|05R#X#$t$16arn(+tlc{>}MHnOC#v%M&4hHOsKMi-D'
    '`kHcgD}F2)%wHeKJhnKBQ}LVF`I>17oUcH*F`@QP2B52ruJ_w&HIhDQ-McyTdrLT2&toU)f(5<g<I@V8yssj{K3F*A?9WJhnLc1{37SBsgn!Wq'
    '<_bDRtJOe(^l4ke&2lxR<hbg8`w?G<DY+ri9+a$lLeDWr#q<?o%NQtsY%KuQk2-ORhsC(;%CAt!8Q{<NXeDC6*nupYTq!`mF~o!I<$zht$ii{y'
    'aeX_Au;lM@@@J|3C7TJRBu=W4mR-KZP8L|DAQC|iQ<5(#F}NkuDOEiuU?!h(pscNapgR;f{tAY9$5)dBYcRbt(p~}`A~BS1L`ct<B@Ssqs5(0d'
    'o;J7-<1AT_Vb76dnpct$cdM1PT+7v^v2d5a8h8TejPuENo^M1j^X!SV7Ptja3A#zVMaKSgD5_VC;QU1M{)K0(*PqTW(!;KM3_^xwtU8Fcl*x|S'
    'Ug<|XLEM?vHY`+fe$us3T)dp;r#Z9++<ls5%ca5B6*IP2m!dM>B+3xP<k1)!ci2)TEN-VLw^!151=`wS$Nm)Kb)~|h#7Jl?V+`;GD3AtTg0q(@'
    ';l}$WLBhm@*sWWIMW<P<<v3>z=e9lYy7#I*xHX(M-GRYz6{BO+q@wFlV|?ZB3uA;%=GRnRm`S`#Yg2m42w}K$6n3C&9(j$!Sgd8LNx6>~!tTTf'
    'n&TQep=?BbtrK(|;hdiu+w{@!sG@-b`!P|Audd3<OiDlGkQz0Pf9t)Et~kS7StFuG1s!$sbgQZ3<@)JiJOYaXKf4heja0?uex1iSsVH<<poU}L'
    'GIbRXpHCD`1#on(#=Rl=Z^Qr$aA4f~Ygeh3d_mwuh2<)38p26@g%bOYTywE?oQ4Tx<u=POShxI?Ws!M}5)n63qJhE7^dw<DZ;X5fU`_n?+{w`M'
    'Jx)D2e!3*ZH!5G6Qd?Y~Xp7uW<LBBueGzYR8qoxQesLcxRf`wxqTJ@-PMHLXc>rP_ET~mUbu2Dn7aaX){@gg&53Nr@1J7?62S}1-uQ?~;&=d61'
    '+;%D#axC@GcxKGwNWm;~nBq8ZU7G5y)%5K@d%ZJXplu369Fs)bjhk}Z5AsEw-p~Pt!C&s6kMqrL&Y~+NEM?D$?Sbj)ykV0^9c_(;_x5e5yKVsK'
    'A8NDWRG7r~Y2d?W`B@hBh~$pKQ7xV)s-1W|uP%+?r_nO)pP`9oGH4wXdTP+3-Oz=UTzbhmhMZ8H=Of}j9AEi~80?r+MC$Y^3r2!`z<i!_0flI%'
    'ObV4h$zl?(qm-MV`>6Xg%UzAf?vH`!9)8Jh%%NW0W$qj|+0UY-y5qTZz-=gkl&`iR4qk1gHxoUwLXZ`K)uxp#>wNYP{db){+NqPM38nZl!xP2b'
    't1YXs-Gju2DwruoG=8J@%?J)29{=z}nPBnl%d3VSWh#W5zedOIbVRrb;G;FD2t`W(1hRX`WrnO?rF1o1wLc=`g3_Y_aTm^B43n!RFe=ot<s=kZ'
    '2&@DPgbBvn<}<QiVS^W0*FocfyXIc5YT<;(pbNpxL(Dp!BF1?qg-xVkLk#Ki3eYi4*r>)UZr31sU(x%yv)VaFi`?xWAD`VaP*yNo%c4-4<m-Z7'
    'ru(vPH)ks;S={VI&xcMX40tfumIf>9ll+&mgRQ)-_6=!9MfwhWn;t1k5P~UH-X>8?35$fAB`^XcUb0-_qSB`xZgi*gWUl6J3mV5Qvi3~GvPR(U'
    'W$`8wr#gw%o`^pQVB>_(V1o)agXE>oPJRYM-Ph8}q0K{9^q=p1!M-y5J;4!6mY6eSyWswd2M6~Zw2kEBU*<nfPHhN{yC3=m+tJ^_buQ_g684cI'
    'Ch#Ee9~en3Voy6|aL9Dhw%rw+6^~Ug9ov&FFf1>%pUjpjku0_b@^yv(Sf75w69Y@KFj~#+PN5QzbSjWO!XU6qD+xv8o?T}_#e8wi<&mFIyWBZf'
    'xBE5FQc*}#Zg$wXbt0-{9fipXnXqC|7I0!8j>leuj#;I?3x`aQ`LNMl2<@n<NVkMNS(AIpeC7F<w<(EWh6!3SU+@C&In0@OT8Ze=-=pZj&DDF?'
    'Nqz@hsazP@ozS5{V~s|bKn}|1ROR}iTFTWxABP}VPBGw}j7qG2Q>0s=qA^1vn><B>NSa(DCr1DgWl=^M{NlaAbwIp$5G8jQf5Tu~b^6{!{sqQ$'
    '+q_mgF(57?$?_-IbO^6W^`P06$jG4rW5(fs%DsEC7eH&WHW{)0tEV@W#mL#GywnUAixcoHU84GZL#>U%@%5X2e)I|IY!b#`VA*lQzmOCB?wJQ<'
    '2rH#8Wjw4u$Uki<qb}^!xGU+WHg#~sio@;wFkfQHjocoHl_%z6L1Ny``$;J>Tb#?LZpo48*2uQTQ{3`nC&UX?Tp(`3?QVtzjQmjz?bm@>PrW?u'
    'c9_RD&J<-B_uH*Uy;0QKjaJ4s$J^(gog^R+Ca0(uW08?ySkYuGCGH-%8Z{znHCXjK;Av<JQYCw|$kdk}-HNhsH^Y5Wg7;X2*cI8A*~<%xl!W^i'
    '#C}=#m2tJWeOk4Pf^CQSyxJ^mW2mb4_ykUB?=E%Xt@@S|{*za@A66@P5m|vPqXyDIkTGMa<v|`RM)`yS?u_M3cB(9?3T@h>pz2kf^mIeoQ~A(d'
    'c>hz*D}p}}$!YhUHALNo&$M0wGEBU)mn}2P<61}1Q_nO)--g!P=PDzwZ}TnvL-rRJBK?B_@=SwS?$_xWsTEv;U{spu9d#?b!j6()pni9*C00uT'
    'G2zgN(7WZfxfF1sXwtwlkqA*t@bOc*-<A&TXerjo%%jY?tbMRctD=nZb)#ZDA`*c6B%zD$J(H4x1@KlqwHYmpQrdj%ZS%Ae5&_9ea(_LUqqe(5'
    'd~O^#`+ne6MDytpkhq&5>{8+GuR!boISNV+lQOu*4L1Tq4JXF)DQ@LoBnOtR|Ht8e2BWwj*=|=~+Gj`pOn<f4-US*vFCS&J_Y1WoO0SAu`N1;x'
    'Hma7oCZ@5~fN<Khpzdcn7aB+Fx2U(j;f*;0iPqc~!Jid?D5#;vWoLmat?UxmcWz}8q&c0V<-o*#@G0y7Z%Yquo`L8x*ze&ypIo5_3<_IDN`nYn'
    'D1IH;vVLEeDdCoS0ZC({az4|V5R7OS@-nC^-pkJ~F?)eRTI8OGYt?34nYG6_iC<2`qyEaKn+SgX<f`RQ3RadjUER;4UpG#5X)dmlFVHqB0X?*e'
    'g&+jsK?pJ91qYF|sS(G*o1fH@cgTedaMi!H8oTsq;(~s0M41n+#1$Np`gt@%9D?)W>@EmhpfQ}P1BEl`;}UoY(9(=ebXZL<KomVYgaI4_E_zDp'
    '-mSfVNJhX00yCl)WTOD*B<9Ka02>3#mJxDH@2dzrZ1s#4_vA34ay~6}e{SiHA7BNG<@qAE^@D20Qmhqd2Zyf&Ew5A@m71QoVnc?A8Zyv1(O7<f'
    '+eG%}hwvp&ix&ssyB`cJt!lxaGz8dXPr7|^NVN_qNIW4yFP_d#67Rs6n#EH%9RBk>JILWZ?vs}Zz4d!TkEea3^^DdKZs0!cdnq>&e_s)?PYrhe'
    '8gdw>+>*AhanldS0D?P2_71*nUPEXpPx)ljnr+kOOMy${Pw}3MGZHgdvPR;oK_~LUM=hn-D=vK0GsU(Nw%cV?9)o%wtw3TT-ON7q2@_(*K8=n='
    '8S|uRDZbPW+0)lVc(`)w8>lgNQX&Wul#8aT9>_@#CUN4#snK$I-ua2arl~#iddv4pJwK+;u5h^e%W^>?!d}r?5=`FQD=ig_>pEi&Cv6wFGTssC'
    'oI%H0;8p1R?EWn-IMjtvn1Q?6>GpsLVHk4Y6eid5f8~jXju|z#IBi^>)M2ONMzvRXk*h_^bIy6|(ygm<i^8~24J>VV`kpg?4qNx(yZQ^Imd0gQ'
    'g+1J!(x1s9A!?uBm#24vZC->Vp&n+yd%m{10O=O!!MKQdNZ0%{i0$v@U}+DBa08llr`m+7ImIVmF~+0Lh`zmelnp?1U3Fw;3g8#BU(~X8#U9|R'
    'wC#;Mye<vRjRv~rJkM@5^wsr%1=#;X?vEPi--rFMzksa&wyD2sGIG)<@Nr3Bt7sDP^53(KX%eIH$y#PpOnc(u`KU1k)%wO@JX$0x1B3Lo+?!>r'
    'e6B2&`PKIoUx~1QltXs*En>T@!5by?8;os(Rce`WUN=qpBa4`krOQce^(2JIAG=cKoo%M~QWh0Z4)%}N<>{)<sh~@9jOw`v*H50-EmOaDHMmu8'
    '%ATAkj<r*EUi4Kp-$*0bWGccBQxq7&9rGyZa%im{$g%&I?DNJt4OpgWPuDl<o>Z<Gad@Q%W06vABHU&)Pi6*;_3_A)XPFQypgvbWsjKT&&q)qE'
    'W}w=y2M^=fUvGf520;&aK~1rs;6rMU)yP%Ezrss?B^&U1)+yxT`e{X}Ib%!jVSEj0;Jn?4YbjZsU&G(*gej1Sp(0&*><7M5{I{z5J3}3jbazV5'
    'K)QE#q^&L_QPrgWoN@I#uwU&Rty^<;P(toWYYdVR>B3^MyJyw;9K|L7{^|=RuD*$N8*08N`pxB^ob7Fahfd}sp@aDG^S8CrZ8!~N&9{i9ad8{V'
    '7|V*36LNr73#=JVoqWUN+psV{iDg_SY=0K-RNw`XKKxOWm|)pZl66=4OfKdBLFLobk^I<4DFCffGeb*+`MrcFtT#YN_$KIaD8<l!8;FHjJ=^Tb'
    'AZ$;r6BHgvfF}^QPittGD3j>@uwo5C_Y$@sRidyVHBTQ`c%XA#b-9Q`xec<lNjDG^FD4}JL4b9NkOEk!>Yy(eC!LArU4O;UosQb+@GA7%BzA6X'
    '>MMt}<tbaT7tgKh0G^(kk!BT1_3v-NNv~CrH!E&HB(fg9JGU;<v(q7J0F_u}aw>7yIw6Q09kK=EcZEU)Z>%@cFQ5*^;|aT+|ID~Twta9Jxi6e8'
    '!I#m3X`5W$6K3Up12j?;`buNx*W0=rTZ;>!b-`^gH3ReMo4&yDe+r&~h-RkXahDoCA@hE6M&64RwF_;CSP7Y}VK=D(R%URUTR1US9KrfD8K-JA'
    '=RJlSc2lFG>}_|m9oq`(p_ej}jU;jmy&5gnl_WPG?~1643$gMYm3)Zk;C!wm08x$86CG7>J-$)Xb*3|2U*{evYiHccX4vmg&`Ii(z9?Q4YU4br'
    'x_&=8%v)__un$;L>L`Y_qv!*OcSte^$d2)vm9&o-2G_l}`N#3?E-S1@B>dz#HEm92YBV-rMB!N8xsSw6RF#DbHe`y1iI3DCt)<o{#O3+L{u5zt'
    '^44^z@3Xq40P`dd?(nZ=JEzUXRH9)1w{yO$JE42mOtblQ;DEWjUs6Sx)z@SopX13FuZ-UD*dJS4qJJ)JR!BR13*jHk!X`|C7{QbMx0-@8bleqS'
    '=*0;9Wjq-fQ}+fHrQN47s^EP|2SU8x3%K+QkZ5)J4%HRSwm$T<U%{K?U0iR(L9t&vPYKa+>KEm9QVQng#7;I_$sNdR9<kl%1ySEs_+SDc-B#|s'
    'Vhl+NaX4ybA*1?_oQVMiax`zzqc%Yzd{Tn+4|?tV*k`LtaWJZw#8&4EH9muGlPeNFR6;<^UbxNUHt_)*H6a?366J>>LNBK+xQilg`!M2ASRM(T'
    'G^5Z?kG~qh8#lJ%7WWdq3~x&>5R_R;wqS2KzY-gLM4oVeVqSZrZ3nH%I*zQ9pS;~(BqYhzn<5k=pkp>GjGWl>ZA-&spHo+aTY?*}aQRoP{M*5U'
    '2EdK<fdUm=I7hG;jqAPX$k{!5cb$WB8zs2rfSBmSH*kOlYPLbXLG-3W_E^0=2rozEe`5$P(NxLgs#qWxt)&~Ec)YVTDcvGdB30lDTs*4qT3qna'
    'Eo?sHX}u5K^(G2A9hL}p*^?o;hynw{><4PoVL(pQWH6&AWqJVUnf_%WDf`1^DqEfnt*ugJ$KBd|Jn-W{2TsMF?;_eqh!y2cN=J`w32p`R!HVfS'
    'woL5N%__m}Hx<O3fq5<VpqK2*m%;kXX1=5v=n<qwqFlpA1D3fzK#;#tW{{PL9cj}R;uJo38j&!G%cw_h0PnQOb~Y9<MWQ(^==4ypG+z3iB6qe+'
    'Af=|vVk_RE<5!}N85zG(qK26s%T=D-`W^&%2ZtU~H@wIw3^?`{!6Z(BMDdf(@xG*AtQ0U%ztd#udz^BorPWK0+nXnpz%*eRoGQ>L^H}t)Q;3`Z'
    'S+N~WUIGgUb;luDnFwCp6{=S*roNoxSjt9NRzq6oDlsOsKRWKbH(!*~a5I3%>v?zO1z>xs8pxI13n8!(<}G*dv4-G{4U}5z^SQq0&zJNzeA3*<'
    '&z8wS$FGd*I==VTIJP+620A2RrXoUmlB|BB8o5iE6k%|^C2SOTfpyue<-fjL$6P-B@xa2rU)-;NkdsIe9Fa%gwwh%asoCqgMf*%pZy%u3bPv4+'
    '%-~{6h<AKcI%HGOu$+D7RQ)vr;{lqP#${%d^4qV~16$t5nXubwFf%Q`@Frbu>=1;Bei`l3y580>M%^{LX$fdr+|JDh?0s6o*#|p$QNQW7E-{!g'
    '@tn|brkrKR$)FPr7QSu8iHI_q4GC3~i(sK)H)U7awOnwe)FPr1yg@w51T-hOW#yc|G(Qp0Td<GC$xfHNg(--gw0q9HUFR0xK*dK|VpP?hsYqBr'
    'iX;)s5<N-XX5%M|)FKP4@pnsQ%ev)=hd+C`_=V<smuj$LI%sGBpVIHI)~Jy=u!hUiaVRUhuy5i;<H1C{>zll9!VU??L-fxNsJ4Cai)LG&6>fI3'
    'U@0F9ro0RrcnLv=N?!LR*`2W@ev7Q3>vFgYg;n6?Njgi8cVPf*-e-wP<>@>8Bc;!BWk*MG`FEPn*^^PsUBduH_t>sL<t5$qeD<>&Ut7g=rWrrv'
    '0530KaFlpZHDKyVhJrM~06eIWL%CpVD3r`gLkUoJC<Kx<$OR6I{0B9$a*vmwi}?u}>EMJ5<7a$lpB_JCKcBR|x{{@qwNX1CZ=uO~=pfLb+v6E3'
    'vK94&LgYLYzqtc;vlEtYFp*!t&<URmRw<|kxcyy$wayyyR8|$>+6a@=9c!O&sz8@FhzCsGo!!9)FrsK2*BFni_XGEy#h!kknWHF-paYG6LN-%g'
    'I}Z=GngVxy1lga|(B&(&Y$36nP=v>8#ab-|Hh)@k>QmRrZSUu%k|D$I1KcP0>syw-po@_3Fl;}POIr>j{pdXH5|#%`0Nfp$lV*M)zCGp73@JuK'
    'SbHeUlqswUK1<CN*MM`&3hH|f8T-{Fejw|>+-|&HPsR`o+?i}vM7<NK&2lK2Yo*t;aa?ba6X1-r8Lk@(er&+`KZi`mq^3YTVqtER<Lje7Yv(67'
    'EqkZg2<2xm3!jKlBW5hppg`*SH9op@%uxHboZB(}nUFH8L?>2WUn0leTCCIwQ=r}nVjcH;aDR_;hk*yU+y!&W943!R5avRo^Xr326`&Q9j8OK!'
    'v4#Wqgz6~h<s8{nP)&L)*!lEEqU10?nrW&d%`!RKgA{Y&t&2^Ay{APz=n^Y6!3afNB^&XY)vSn)M4v;6ss1Y{wGQ2ckNG5Vrqm=(RF4G*0j_uH'
    '>Lv+96iu<X$oE?VmH{(`7V<O9=yWkJk9<I!W6CCNA3)FVY|$zrO7>tu5$Al~I85%Mp$ts!L<72R|3!4diL4hQnl?{OD+YECG%&CE$nU2A?KyX@'
    'rn_DPYax-it=!-XkIy{Yx-o!$N2|TtX>{hvu){R_m@8r=ph$sg*9XoHgl;m0iE6{2`WUitVd)KmZA@`Pj9j``kS1Ij!YHgOa1ei7v7E_bO7UWM'
    'CSrP9GksADZ#IAaH!Sn)Uh<SG9HxnDGCctdaC~a@_hBooYD|F?JxdWcnzuMt;-cIIA=9t$fWf{C9)f@vnrtYQC_HLeR7wEsY_d*`(91~Hmg7c%'
    'NI4=}360P)@Fb>Re4zzYxX%2BGsfIFAC0Lz2`gg)xVoDh+bClG0m5i7-_i_S^W>!&%jNRE^Q$pUsW1RYqbQ@irkQzB=G$m&ti6xue!p5BHopQ^'
    's+|c1gT=&IlZ_d!PBQ4Eme>XM)cw0Tdtn3vDQ$oP?ujFGVCFcd#jyz@5mEft*Un#jS#en)&@M30GTP56QUSA>x)M{uQ65olS-#JBN~bY3z+3&0'
    '9Gq+WUo(q|PC&Wtiv<Jq2jk7U>Nyy%j0B$X#)5qOmLE#9%slJ-oxVccviV`sD{TK@)BZ{Z7OfV=D39;Ju~{D!7CQ~KEIlHNktKtmVaZEvI*Zq7'
    '!_z$HI*Fu|1)=pGe#Z1sCj`I3H?t?V3SSFfWWbaLN5_H1Bpl>qlMlB!YYtm`4k=BljInWKoMg-$+Eid6Ly-NxGn2Tk#k3zbM_9TpC(Do1s({^l'
    '7C)KWgL<CLOAy9JDBU3}1<>~%9#>XY6x_H3N}jbWWr8wX*R)6D+1+i&k7ivEKJeP*1@bJSHc6@bvfylqc&#YCh}L57#1o2pM2b!w9mRS!wJ{NV'
    'k{#H{QfOv+pA`k^`|T^%lksQ8OBU?QrS-3!S<Fr|E=dOiO>221_^Kk*@%FDUlQ1#s>+)CHErs+XIOC~?M3%O}3K9L|6du=Jl|u4<)c`x|g9qYx'
    'L~hLb<C9(A8Fn&16pO4m9ATP0>B*#xl;jk|H43`+O5#K=81Tv1{^~~Q;n?*Mh|RVz`j<FkkEd*eCJZGuEvpNi?nH@6FHR<PL%seuqJ1F*yuW*c'
    'hpoalrsQd~E0z)AUp5#0!javC%>=(ubR0w+zQcP>UPDmS<|0%+XSX?A<CRw_E7Io8mpA2^x|!C~u?a_<7n{a4tFe)v1FeiP(YK&jtRP+8tH5+k'
    'D<cQBUB?p3^TKYbXJekD9vy^)z7x_dRcTVkte(&$OptqNOuC}|%!x$Xn0FQ|!IRv_-xmkAIGvacb})aZJB9JhC}4!B5!R_>=vT4@dldJaiHbfS'
    'm;(u2g}q`7{012`J)r0$v8Da{Kl)r0?krRgYXb&v*?&FfH@M8A10Mk*pF*4^k=f1Lo4?atl7lV7P;~X@3f$#)Sw&I*g9|mvsez`)ED0d6jf9*E'
    'fv|~S^<PJ;bmas&KZL6bVKkE>pd-auqg^)>R2lv9qtt(wgke9EGA=xNPKHMr!SO&j<<lCSfsPgZ$TsnYEOmmuhIcvN>+XhV(NPd`1NePD;npVv'
    'rah_O6yhcTLaRWq2?EAldUy=T7R&&IHDUCC(#9UPuSDodf6WUQV}<8&TOLmw8Chr}FQFS&7&h4i>`@41=HN7Kynu!fhd77n@#0!cX(2>fq%@Qg'
    '-tv+5$68Cw7~qNSMfV89U86X64qZhPqBeZ|9n5_U+53)ILIeXH)XOOK=GGL8P}x&&$5ntmgwTpDk_#n#<$)r-6nn)9Vbpa{Y+6}he)F`oH;1O~'
    '1nbeP?U-TT_lfw#ne6+8F}|xrkAuMbK0U~v6I=OrD5)gJRP=~G359>U5S;MVqau^ohxoKHKwmIK9r1d*x-wZm&r^yZM=l<0%aj?uHA&3btjXbI'
    '*;J{4>zeafVsyZ(JvC<5{dZ5MY7sUzG^8+*Sr1melKwV?c&Rpx<~qJI)3eKI&eq9v*R7$_OfM~(o)uq7l@Q=STGl3lJ~i<tBKX6{JGl3bN;^Tc'
    'g=l17#{qBVEZChWYr}nH6PG=uj3hm((TeZ6?Y?Zs$MhgE;zUD`8F8gpd(U08yqZo6@c8-#4zD5?W}X!ZWV0Tj6W&=9X3%wXKQa@;g-=K2+yCZx'
    'D&4sC6a?+*jGTl9?W!9^7>y%67F>p*bu9xc@q)v3>6q|w*!R=4z*Pc5Zs`Ft_I4+vc+!<opW+bs0M3oN7XD0m<=yYPcLB#fwe*xjFnQtvJ3&sO'
    'pV`*p;q$sc%06hvd-Sx^E);C#Bbei~d#mVF?{wd-&ATdq$cm1=sq0u9r<&_VAY_$qjLoVx>rBsIZF$(_`nU=An?)QZ#8aM!xVfE19@_kj7NuVx'
    'T}L{s2ti}51zv6VYg7$yIn8=n{;3fjNatj;<xkmBefoaJ;~Y3PLYgB;$3@#%iS6_+U|wXp=M77yf(6s7QkK>GIRG}hbFZB<f#OStPQK7g_E4Qi'
    'a}$qd4CZ1~!IcxFHsWF6)l2o@$9=B<(nGvL)fTBV-|(-j+kah~Zp?D1nBj>AkCk!Ug*I%rI$Os1-K-%qb><UhN*D9wMjH57Dct4ch$X(G>MCN7'
    'O3VRfv0|6Si%|o4&28bTl;4f{gbZ7Gf7IS%;yCe&>=fuSezu9~Z0CUw?ZiwDf}fMZ<al|JWKuNLeo4-n&A?hr?Sd1**uZ=mI^TN~HEP|ayVlC%'
    'wC;sBodI_E?S3X7M|he$E^#Y^eFFld<TZYQbHGTKKY|WVqP(j_^IP?lErKWqT78lz$Df(QB{B4Z+(zJyc5F2aMzP3&b{KxiADHQk$`KJLrz4Kq'
    'V_6ySH*Ph*HBeiV^5VL;I3I@L2^4RJ=WApp@V7B-q{u3jtW5bow{$G9rm=Z)^dc{T@c+Wq`kNVoQmo{l?y=6td$)+<>Q%(-&vt7?$tmrTwIeqJ'
    'w^;>!-t)4nUzQ31*;gFHdywjY6Lf<NceQHYBV8)!DiEnH0KE`tOV|68ga0iyvi|)?{8L<$+GOd1%47}Y!T{+L9SVf5>NVZ<bOc7e9!;+B|2C#C'
    'I@lT89nx^@@P#l=w-~y21*%n?8+?$oQMFjcJu&Vx@8K-+5Ojee$c0y$`h1~$zd>hX=uHfCrbi~?3#E8Lcb$l@7du{<L1sJe)1{0>V>qNNhRYpM'
    '@Y>P-l~9(`!XauBL!wi$fD}a$2L^_E2~<S-X6!;qbvszip7q+tY1tZxgQn}IMwpwgy7Z=pu7ZhVtTxV}6*+s^_-%Ntyqf`}iYr*$EeaWy5+e#K'
    '2pc`y%T`YSzqSUqV?_HPtdLGZOMobtj-Rm~+LFKFg_QWK7DT7o#IxFHy;;^U5`XF)6y!pPC$7c*bip~im1(h)gr)l}C!`>Zdy{~TE~CP7zv)Ax'
    'OI@mIBEPSazth|OEyMsBjx>zmUA*Qu=IraVQUeL2f4L(EA#3|!u$~RUblyD4M;~mqC=9PtN$loT<e*R&yL(DJ(&~fy?X(H<iw5d7eJ}A8ItUn&'
    '^uL>h``vE55)wP1{9>T`^@rq)q}%g6e+3ip^2dEuB(NU>F)_CnbY5lSaLvqqK-yfYKg1|F>Pm`4Xo16i$FdmXZ_;XbqgUQ{VLja5o`l;}az~4i'
    'KK~loa`LN?2o1A;&AY$V$_q<?LynFT3tn!0@iYxkTHpFKi=n|){rs$6;)mXOkxIg`n*yJ>#T*IfHu0yh)tCTb|6cm}K7lk6T5@EknfAFmjN@PG'
    '%q#tPWne>f?3>2`e`j$@yt$MY&0z#TG(+AP#AxLIfXuCykFJK8(9D#}UOW=j-@@dy->qB|D9*g<7XByDl?VUTKq~*oL9)}73#(k7YQkJ6fT`QS'
    '3m+7<{|oAF43^~6;CGFb--#WuW3Eok4m2$eupRC%_{!YE;&g%es+X|!E_BiXeD8wPbMl6+M>1oMW~%HJDsJ<(DO?VUVus`4jv;zY0+xlylT~(C'
    'CG~A23u<TD3B}XKr<4f{gdYd|!h-nniU>HP&KP+MC4ckTG^E0fFRkk5Y`!P0hb;{sc}z%`7WM$ChLkfHhRv9()dD83U&dPgg!zU(G-xOQs-|ws'
    'zrj&d>VXg?iC$JSWHa`w2+pF4r&UnQk=-W_jNYua5#33zi6f-Tb`qMetxxzyzLek4%7#WhB3-7D6Q^@8l62e6w5Xyw(uOwT7ETdPXJ^;*I%`H6'
    '6Pq2T`)usLxPp&5`~eRj8Pf01Q@!4n?1~xWtQ{Lnd9$6Cc8L0Q$!yhX^bK8H>kbLr*!eLrp{InSF^a;i>j54WZ3M#WGZV2n3bmIWTKjXAs0(pa'
    'WfJ{O`~LlEX)BY!>=f4cRipyBE%VcPvH$OoELMW;heT7ABUOR?2W4M16RiU0w7L;8R6if>(2Btv^~7>uDW#UW-Z_32oD<_}oN$fUwSP@N`6`lY'
    'tm_rL77aYS@#1q^&i+o%ug@*lTIbWP-N)_f%VHBkg}_(<t+Td!1Dt*G(C4sm1q%em`Htfy&*#_Y(4(Jld;tCXrx9Vmb5_-&2m9v38+zH2y2@b*'
    'My8LD6penR`p>W#;pqjJu?s%{nZnF^0KP+gIzBcJ+@An$cO1@#)H^R_e?cR7_)({tTq2VY*!bCFr4xm?p%wdh{g)wzyR4PniUYc%PJ!M~o}@)Y'
    'mk8Yw@fJ-;k>OuFTcfUGp?7Dkj>@<M2~leBa&VXnB2?oaxVcyD-X*L@C>Zd6V=riKoNP|MByMaPWyQvI8D8l@z}2sxnKfQI9=!`zaoMI4Js)@W'
    'i1XH&pkp);-PZMv``~4DLJ*$^I{a|3q?IF_gO+x%p2k<GWkW!#s6OGF;uwwJ_~CCm??R{^_g=tKXY>q|vTsNt87SEDJ<S~ky&ha+LNFmJry!<j'
    'kSFpZk&M0IKPCi81H?m}A_3XieejqEK6!=;XB$^4SY-n4M?)G_JD=Gm|GWa|JSu;NEiMYFrI{zonj&5s*yaZ6ryE$6;8}}5;7nUH#X=w691sm2'
    'NvscVnHXOCtSMG4&05k7K)`QQ+J=~4^B2+6oOTgzygntdz$Vo|3%S<o3Eq{@k=pz=iD>+C$<7w2(nM;e`<}KlI|4`*rz3l$|EkJOq-Zcuee0FV'
    'Xo3;9MQ)96GP0#f-T{22=b3)mS6=qcSl9(w<(OCoc3ENQM%drp2LTMsi?j&nff8_T>kXA@$UTDdU3aTqqQuir0iw%WLR7lgqcH8G+i~XVW0(1#'
    '{w(*C{l!t9DWZ~B3dKn4Y=k8MCDXW|Ix{J5<5ZR?%=Ck?t>#z<0*{MrHqd7+UTbry`v0SUc`JdhyYZJi<{7vZikL%-P|qJ(H%MN<yX$_%SLqn-'
    '(<dg6t~yhZClkSQJH)@kKzsZTe?Qfh@s$wF-ix=8F|U|Do)(ROITa?b!E~v-32Ug-Q<3zJ--EB-;`Eg1#t(Y;KqW2+gN3v++yM?cI#H8d&2YRq'
    'H1lCe;nWtD4F_03oH)A4yiw7z>=U6n@}}Tf+7L69{}%KtLMk$ZIwQeOvj^+T^4Kx0{8h*AAvscah@KKwW9{1iTYe8cVFnfpED>6jyTd4BpMN?C'
    'p?AI}Nxry#*rHM4#oc=DQt-OQ=^vV;^q7<g02^}-GHNPb4RlFR<qNwfDy8qof`SOc#_HJ<bpBQ!nO89D6u}xRv}-;$v{QX%?u_T}4V)|}b5fJT'
    '<955S9Gb8KtdVCsAt6sBsTt(Z*AWNc;q(VFR_x)Z9$F4i4u_L5xy2{OVwd0QcC5El2+nn&29qlU@tptbj4ji?p2?KoV)JZKJ~gIxrN=(UVzx+X'
    '1iuGNLAaUFcsMUk@-U<0*;;LF1I_*LI*8NbgH<49MOlptTNu7h<pZlHN2pU^5?^Hej(n}_UQ+;MN&IkjbDo;{KN;S2g7XRM>Qt~0xRP9q(A;uM'
    'ARE9p4=8?lw<HevT;n}Y8jcOVKfI9u5)S8X78XYF81(!kboYy_P^FDxa~ubuawk$YcdD65H!%n09Gn#*eJsks#a;sHcb&rPSx^GiQv#SE_Jf=O'
    'qSAkToq9*&nT|$9Usi}I?eYH8(mA7ProFfqbN(;qb*F(|hsL~z<g^W9bEyeNI+<fTu&kaN$CKsM8S4eThmxl@2kG!C|B+E|+KrhAy)kWqM8UYG'
    'f$;x;SjQHRvz?NTS|iMm7#*t3W4D!Zeq#biT<WjV^5pLC8vIXmU3BYmoD+~pO&nVF!KS3x($490ul^r%JGEA<!YAVpr!{dbg9RM$^0(EJ($zR*'
    'MQ*-!Op&RKGHw;&ToFCL%0GB!Tpkhvk`2t{@`10$NhoR81c%BcTcDV4rD^1tukRI;ZKdhO$yz%sYJ%Rb#jtsbI<{w4u`v+?_naSBSQC?XbO09H'
    'dnuhlybVeaiB*;RLPwtkE;iQ<;qsS`H<s#wR^)=D^^)q{lnI?D_j15KmUzGE-}on0eupLt*X4zK#9aGwuZqbPS=bUgSy5Pn(qL440rqOwYWBlk'
    '+gDqnuduNwBL2Pb#%~yljirT-N2hCL-B(zZjjqooWy`O)FygWm=CIxL8NwJ0z>#J)X}M_2yvF!64)0t?lu#JM^y8eM|C#?SUYQM;s0y~vv!;%9'
    '{V@AaHP|t(A1U>=^1jcS`#4EEI7R)mR5UL8>e;j*zvgwJV#dh%c_FrI;NQjvx`Da6v%>uC0j3z2>1(iZYzY8%0kf^^!lTT(mE$jjTS!i{y>DG?'
    'l6PC}7nF`iHughGP&v2YYIHJpHdx98!0b4`>ikG!u+Jm{A&dRIkK>#SV@!W8FlL<gl5%3Gm#?<zlw)8^zq|+(b#N9Kan@2Ge8{xqwegIg-nW2#'
    'CBB^JfuOL(Pw>$A+b92Ze#KoX4Im4g&3q?+*ZIGhynVIxW}l>4x|=FLY+|$clw>=mroen++Z*l$AsfBSAC+xcY!+d8i~PF<z2te@ev$8~750oT'
    ';F^!&uAjah)7nAK=O4tQqq$jfP=AwCuB}qhaAlU1w+&hzGkhA=fLfDwotPdwNfW({7L3g@EY}nwcQccoSYZeR>xztt&Uf>k?>_<96MIAK1F>@;'
    'nS-zq?80)^OUWS|XqH0_=bvenH!H1xuNZRQ=Ek4eA`W(M5nlpMil>AyBxM5NQbdHRg_vqN0dMC46hu2ogV&!U6AE1j{ynlivnhQ0GXv>sYTKlR'
    '2AIGo354c|$5|aczA!R0*frz@s7PZL?oo`$AO5TSP1MqWMlxe6;0wLq%{o$vhkPGeD!1xGTJNCYtxm|BM&5T-5eCY>yP6f#Y{8wR+|i$m63J_A'
    'rRRQJ3Z;YS2LWdfCa|CN$WyhT$w=qZT$R0rjOR*Uz&L$PS=G+?gth7+U0+qQ(&(ST7yC1b+?YQ#GF{+aqaAw(?D0KCMc!v~@Y<hr?G=@r#cc}W'
    'ibgV*ZO|h3FBop*a9+CRc-XAiGyE-{ol4Psw)o=Z<xU7@RSWoWvnN8W7%elNqS%Dx)XVh+fP~BH=dQYbM1n?O5c7XReNKE|5wCbQMAN8;%hJ26'
    'FZNL>CVMQygWMzvKqQ@)^ss82omiY!;loIC?b|kW^3g%@4+uH_UtJY72ir{YK#jGRnFgE{!P4xwDX_x->HV^}c@)c}yCY6_a`;t}r^uSr6KQW>'
    'GQBUzK-jKiB-CjW45?JLRKZrv|8zfS(!msKp&q677LkW4uf*6&mxSYfj}Ol^h)=aN3C@EM?32zxC~v&oJzWZa`iN>uyB6jTPmiDM6i8?)OeIh4'
    'k6$DvtD!|Sn=J$?x!du$;c@=XeD<J1OPVIA5)c`^9{+ZDV)}F#VPu)1`Z?5nq%f~jp4sU}k}d4SZgpBBNBb7D--2?={~scXxn+@>XQ9x;rEC!4'
    '#UUTC4HCv2LOL1azMQ%PU*zsgG;w5U`W1V7dx$)o8-$P<Ql<je{%;77TKLh<D9bTgh@=)Q9p|zRF=tm{FJ7^X>12-E_X|q6aytP0`NI8|6Ug}{'
    'HP2j=pq3J?`7V?sr)o?&ipI@B*_Ii3*+$^1@b82lq2PcvY^*{3)zE;_xO#7uxW(O{a0nu>**&iCBQKr!$-RK2BC<KrIf5b32Og+HndL2K`aB;>'
    'c8}7RRegcXH{S72Mq1_Csyh|^HF1;m+I0r$+2sKR))6Y`hq~@>vmWyD8oeia+<34u!867zPybm66k{^rsMn$ol_^E*I$aY@?GX-Z`pN&zm(V@Z'
    '|0xh2nkz(f*E>Ltmd~g}V(lYHZNTx<uPQ;?k3xmgUW%kz#N&jo@pGTBvXhPTT>ZV|K@=f8eP*7`>iS4=Jf_`$xTvqFHHs`m@T}5@qj30ee0yH>'
    'sKQfu(MA=0k)A}|ra`KebEBCK)GZV|oMd)nV*9(Y+FzLBD}pBsQ&o|y`#dm*YIqTNJ^SY%y*Z~avCL%xlaqv|xqK<|1xVptb}DLHay86Ul3!DR'
    'bLQa)lPxZ1U>F;-3QSr}z+Lt#fE`1%HLP0rh7mNRMMuxKfQg?1QVcB`7q9?k)BY4%fuST>9mcnOBOk`Z#{?nV@WUMhO``dq1DTv(Czr$*?l}-_'
    'x~qW`7~9W*ldm8u*9$z9qcC&Ce6}1@1^QRl#RJ;X{q!roEUD6`!u7J<H(MNU2Yl1i@*HhM`F2YVZI^0bd7E0hPH=hM)km)86P`SyrX)e4d;l=*'
    '6bIv-$MNE=3@Lwq!c5`p`7sl^!MSh42fepjwGEn?ADShKuchhS|1Vx6GYu<YDTO|1kvt(6b_&Ssm^<ww+p0kMgE=+bC8kxJFM;(Pe~g-|@4h2-'
    'rNq}(OkDZw3C;4UoQmtNh073jaR-TZ1nq?rXe(E1&x=mLMKI~1r>XPrYT8NjcS(qG9fU}RA>>I+c&j{0<+;AHvj~N?%T}NS7>)?}PRSsChq@e|'
    'gmPJor%4z_^dAyrpf-m&0scNlo=+?oPxCs7c6)gTJNM$BX*8Kc9%8B5^WO(L`ComMNM?$pm&!)vGDwSdJSUNur}n&oEMzbos;p>{$=Mv0VOWsQ'
    '_QiM~P`dFgY+;xG3v&6r((}(!q66XFXLaG2NA+qf^8IMk^Y+$F_>9Bqo`f$Ft~7z-JJYYVgf3zVC{mfB5M;3U;Au;8&mbae=c~`wmOfh>p13!&'
    'VGp=$Ind2N^5Ax_U;I-J&nNfx=+>qA!=0r#sjH%>986nN7!N*R?QoyR0SG!cxUyrlQW@VDhtE8L88`0vRA#t1wSMfbd@0>a*~dQ`$$C7n3pged'
    '#lzZMLf#M(gM6SF?M6k>jXMBJlscy#att)W{V<$#ZGJ2N1I&r<qG-_5Iwtxa0TXAD44dq3$9`bFHA=#)zKR0=pLR!w2W|NZZSp(#Cqe(wL)8jR'
    'YqbfGWQPYuM0`xBrj=!=;p}JsS4w9U2l|=5q*LY9F>$kiQ@3*jm5C|qxs^tDxTI6=$^<KX)%l)@(6()hx-h`$HBo<5GHEhj+<-jw5K$E&ypKy3'
    'nBs&$(=z>a&KWN*k{p97b8II6zU|9p8mM}j4{{&yA)okIyp}qKmmUmOQ&NfSdmC#_ffx$~lMmGk8!pmJA8!VqwvYJ80q);~g6i;ssB+j|-40w;'
    'twU6qX6(+RDs;z)Ds&@kVa4WUY8ONIFQm7>pE^C?J`^sxDGH1}e*sS+^liIBBbn#}Pcc0`FO+3~SxBcrNc*zf=$bHyo6S3)Z*Vw(9Oq<24+ROE'
    'mlLewL9b+URcQIEw`;4>F9HY>HzyE$VImbBtT3g(s@L3pJivAxELlRV%heq8J%0N-h943u;wC++uP&db*w>BnyAck-Vi9;1SBrG(#JH6r(GQ(('
    'E7qn^${OyO&<>iRsNQDFwKW`0)5~H6rASbgyTjUVM3vUA(LtP=*8PI9K5o*cVm6v5PNds@W1Up7S=BS?J$5-7{hS@@tOvFN)-$6_AWcX6v4LBI'
    'jQ(w(M^Wvysl2at!gI)4e+EV_+CAcs7HS-J_ssw=%qE2dZj9%ET9dehj8!!^J@Y_kU2onC?)6nWKaUcQHOc9rymYrSWNYxZavergM-Th+46~89'
    'E_Vh&$~Toe#CnDw?u}Q>?QPiE=0p~dSy2$?&K@zr+7RWUWli?1rpNC|!#;-%>H}j0e%Ih1&1!1tk=Lp0tgyjyxsLdiGUet(SnRor!wa`A>F|S>'
    'i-oVG2r91F5N;e|<LFhJfC^(?kVbV^H22*odAe@CremLhRjy$yoMvA3u--SlXKpvU`E*i)anF;DFf#{Oj`-lLqg~4G-1B9z{}WR26a6JHPx$N#'
    '$9vM99p_Fx_IT-U02B@sis5!ux^K2%6`fp`HHVy#raHs_(4ge2wlKX08F$4kx!X<k$8k7k_4W|tIC=D#EheZrVjxRypQd!P&6<!~RY#|l*Be`K'
    'PXOPX#!@_ykYhbR&)~)f>?$Zo#|Z1jV!bET3bhEfRPE{1G~SE4O;%xubnek}9A_1EP}-=vN)UR$93m5|nY)Mv!tRxAtn(l&r?!Yy7pN4I$x5_<'
    'D~HOq+JwjGBADAv!o1a*?@vBZ1!~Er3939y@+d>A&Qaw*g~_G+i|ra)$^jCcZH#j*1W>)@5c(wca7GOolVlqSfe_q^5XhG_=w)kbwZ)@6bmLik'
    '*&wg3NMwGyqKayfw+$D~P*G(i`_sS-FWnIDm4zT+X+bty-EE}Ze&RPzh{-<?AUNr@s`2O0xs%%YTB+{Oi%H`5_|-&6LKjd-!{0DtsH@htjQ)7_'
    '4U((+l(8K0w}<(t?E@)+>7TmO_J<vBxhyxf++A_D%b5fhEPsv=WrviES%a}Cq19ed9c-H(!>4aAkevsx2KE^b9kS-1r8vFH$`JivRMZwG%>I9y'
    'UY9R6U-VI~dCo42VOYdpfrq@pY9BB}bt{{Dqah0z$lHwS2~(nWnN@ZXbrJSsJVS;T`H7_j>M1v1i^>3;S`_Oy;mdU|4aW6DuD)H#it0tLf&DL2'
    '!Z?{>#5cgA=ih;XKqb77M*Fz-mJJAkwgS}~j6?7aER4!%HT^jyDIIqvG9=_(a#-M~?o#XZ2yI-kCll+X;sVA+VwBA6&`lv4W{KBRTg~aMX2*6`'
    'w}}lClx^Y=crn*BKZHi^Ex8N;*&>O=*Wizm$TnCV38PXwR?#@@W--r9pB<$3g-lOg!|bgtU|pI>TLmO>rQtt|BB<ZyFFaIA2>eHhTccJUnQ%n!'
    'a%qspr3!;)#1-e`tw{}&GFULk2DasCf-#A*YJ7|Lt<dqekOL%$O|+Ht_le#D`bS2DlHNmuGrT7_ZxDePv605BBxW&8_<S~4TLUL;9f=UT2cyLF'
    'Ddu31obM}85gX{s0;#}eN8?1N&Db3IlXAG+un;wWHEETnA^WW28L5piC4a!*x(0!Y7ZcWAdha&L35?Y*gE>Y4lQAAcPYN&wbhmhqd#m18Z1`Xn'
    'X6HXQjF{7FIpvU8m&=dbkEv67C3_p-HuRCeFx~0gU8rbot*;K4Ah9J1dGY^!)kya5(m#UC^Ha+FKwu8u0cfI8nD3oFv3PWpDkTq+x`2sD6*m5-'
    'M3Fl1vs9R?O7)W+xuHiut7oEedo~wj5A=+Z8-I)KzSD+WvA_Y4{#Vo`EwgOixK5L>L~AvPoTs?)k+~A%v@c>|u!C>EsUWlFZ9p!6-D5q`zt^Nw'
    'rwBYui=(FHYLKj}@ixguhZp>e%Qgkjdhx7-P5p8Lc0gEpA!+Jl<Wy1a)`~+%WB#wh^q%|RlEVAf|2ZQEYK^fNW6kZDh#;QGe)+?T?$%!1gMh{+'
    'hk^+M-4`yBm$(!C&+%7#k%p714&P`gy{R}85qgSb{{Db>^SyaNpYSU$5BsJ*7c48~b1Q8nlG9^`#Fd(|h4y9uXy9tYc3S0KNZYZ`Ixv48SD^e-'
    '&Ct$|#lfsWqA6BY9ZapY-mj<UL4OnvBs!m4J7raehx|L4Nk+E;{o(bB!lp5B{84_yayV(@iL(FWh1>(UAeUdG-X}t-Q-4sw=#3`4Ol_Z&Y{$gv'
    'dkgU)Atnf2%E}XbAEMdh`Y@o|#<ZIfB0)-cpZY83fdpE5Q0%i|7AZv|G@4tSg|Tg1_U?GXjW?a}>Fmzp4Qg%qN=QpX33dh+*2QwClPU{cB3zXW'
    'e-3-GGX6N06z~DIO&@(BqH&VFrFdaIB^clT7xrdr*%Tp{2mva|`d-sfh3!KmrowCEBL~ClPj)`fV#|u`zrbUKN14L93@%uNo*~E(r>JVXqBWUZ'
    '=AmyNW6BD5o>2|e^--n6UFbd%y_?@D&d3F-q_oXp+b&`5GKY{G@8+9Mzt%1B@}%05=!SDN&-tRjXxh5WDRam-r8VN}^q?p;HwEW2Si>sUXVm*U'
    '<%{Q&EahJ*g-6SF-;8BFk0}LprF0!u1fw6POI=ev=3yi&+REHY6iaSk_t47jE`8ckYp9{lPwac$du_HKQVAenCbsRcLI6`!pz(=$uBo068Uc7('
    'Vci4XitRRDGl=E0s$EL}O5V%rOvtu}E4I(ai;X)`v(ISzlJDtA%q1z71S}F&JIqVbnGF{eDcCgJR^<G2@QPL_uOp7b1C9T!<{?FIBd2`Pm&v^k'
    'BA0;z9aeP~k+qXmjL^1D8Um?)4nb((sfP((Dj>2eS>{nMAbl=9fgn1-+4ZnfkL|rcnJb^H<Se@#1S3+LRmOmI(Lvr9Ir1#n-z|&WpyozN70aa<'
    'D32b4*dsP_0VCOZ4j6H#OJj~?i@1}N)gX@F#?9qZT(qO4??tevT~MRQ6SmB0?$O#3OPXrn6(`?=i5NrH8YR%G<rCbetd<2VMIQ2{guU4bu5>fD'
    '7HH^hfR}5O5vxlZ)5715S6WX<G`B$}35lPwGP=gKhO?jxGoIyAnG0*ghoKv-Jh#b5_>^Of?PBrF={4EO;Jx-Y=jcKqFEJOXtc~&x!VbK!2Bjp|'
    '2W-4Ca$XR0d?Cw!z;ED)qiGvD^lhIv+eKMDXd6KASZnLfH9<&Ys7}G-u@1Tu3fhA7krC^S5dHRjJ2az)yX=wSAwZdt{)#A5eO=emEv%#}`LOjk'
    'IX;>N*(nnuVxW+i2cl?r`Kd{NtL(TYhfpv312K=3lPIE{_4v6w*1-jyH|wZM<u15^(km4^=tWF?$BQj~S=H@L@Jt4Yov~WwLYC13ZPm_$l9uLM'
    'Xci<hSa`{b&~&VyZY0|0@aIFG5PdN842vQ1=Hoj6>4ES#87xJAai$|wVGc;ySG*|-rq-SU&^74)54ZiPqcYGEl$ff~QL$TDTc(ZSoPhK9l9gBF'
    'T%wBoX=m$t!lS9*gtc_$(VHR+8;6TEA#OP&f8d(03hq6^d>o8icGIAV&nCxPSCD@dQFk2uvTm6kn!*F<LO>m>YsG&GawKAuEiTxveG8a9Z2##}'
    'nB%UuJl}{RZMLz|i@?QyU^vo+>V3-B0aWrPorOfxIv={=Y-agG<_w>;WCGWJ)2~jC!a{G?-%d{N6rK?<95~hWACbZ)W4)rR;nEN+<)*mvr@WkD'
    '4#?<dq=AM_<mczQy0ZZzfyA!qPO!Bbta|DW1_AZj`<xKvh9lEgfgwe=AM;uzW-=j^7nuHFKF$7b^4cj6l-Kh=VQx$|K4wS<Eq`X~sWCnx`jDi?'
    'sw`a4r(y}P$6Pm@<AzaJ<^4_Gu+poR-^>ej&UDlndWpFb=}>p%8F7_bf_F}P+Osqsz6%!d##c=R-^2>aWgd)4V-$^2@O*We%XQX2eO*g?zP-J>'
    'sJMILdOu(*AnAZVK#i>_AU$Jm$;t9sx@em5`c}iJYU7@2jRCZH&JZ$id!hJbXsa$|5rshBN?mXo|8A(X@$^at>hQmzq_PI)_k(o$!<mQZs8*%v'
    '11#`$T+ET*fXp<E(oy8ZCm{cnkAC+Cwq%t+nc&Z;YK>WY)>D}9Vovm{up!h-&1t%N_vv3Q&hmkY-9o@cv_^d46_{Q!%1JmBS{oiMcmBy)PIRNf'
    '>VEFK&w(uGCSfGIr82{KiII+ovjebeLJ14`=&YekNb(a-*HI&Nd+PhT5N=(W&0kZUCf@|iTb2qbQ~D+k`hqU5Nn7H=Cue+ZO}6o8t-H~8@G@Ug'
    '6uKI;7$m;O@!t1)r}B}xPZN05ru&>Lfyo%;!MV{ziMtULQ5x)X^{xR7_0~1m=!oe%dW*KKO!wc#FN&Ug6DwSsS^j!_u@EudU<>2>$fC(`gC6L!'
    'Nv>~KLZlFM?0|-a9(WgzhH4dO-4x*yiTQG~f}t@9%BE}I{ifGew~^Xn0p^uE&%PdHtHLFJm0<j&!9l@tZ9&-Twc&!J^Ilwr1eu(0xzQ!17Xht>'
    '?OcpsSYJ94ZCH<pCS39A7USL;zy(i0Kd7{bj6}X*AP<?`6~FrggLnPwI-XnwR+7TVdm!g9@cPIsIb1(!%E<&B;D(vkIPpTnZWm6@kN@&jAs8@{'
    '&?tr{Z)d*>b$Ui{Q)0FA`JB`@Z2S-`lw|&LB0Yqld_$yC6$z2ZC9mj2Ta1rnc9l|ZD?lPJigjkvlb8{uQF0b$2XYK`!!?@(5R75k^>}3pMqOrp'
    'MW9qtF?IoOVd;u59Qe?94f0myQ>pjW=sNuBZut^UWoRFt(8qn{9LNHNlf_7uVmxE;G3Io9@41&}DUz6#uPvIS`k^qgPM2tYNIjA<n5L2;X}l^m'
    'jP~a};S7asgyV5VLwr?JnF%07Eirc))pq9BJi32B*nq!#DmYTUhB$$VS9%kz<~!MBZy{;t&<@`2cm#TpO0X+gNpvNrYcGWU3D(S2=+>WVf^#nt'
    '=@GER_203JA2fv@T;0PK=Ti7AqnD%7RB&x6mnclQd;ix9T##3o7$YY|#IkA^8rq-=kkUs0=3h;9qc$1#ce%@tYB_OZ&S{!sxXr%5b%|><b>77)'
    '_OeM18%7_TBJ7tf4-Rzy@ntMdE$p-S_%qt;T7_(0z{LFiyTV>L$X<T9zC`!0%S=>~t48FWZ65qZcp4xTBK=Yisf>0CYe%)M0+enCb`nSNK%kjM'
    'GN8a#374xoI!iY;;3Gz6<nUnjcgB(E-T}9QkU_97!`I$sO=6qzMbUgsEjCGh-Ok4Hs?)+XGEvP5?4bV_Kj<7HU4i%Yjz8Fw;{Mdo4@8+Y!O<)e'
    'l1!P)QHDf4%jK>AE2lA=#@yQ+q-%2T;d<b6UYc3@NE5Wcts!lQNxhzD&Vp(7%wQSaAW^N8GOc!K|7I(Qsj;nFHCZpDpPZ0E69nyPT&T9jJmBBm'
    '7C#om+7lc_+teF4uinUfLKIkn!OcI$ts(?Xrq=a<IwNb#r8WK6Iz#T;bkbLLw2L~F$at>=`Txa9aPYupau1ii>*-PPuV;=UIq-wxk~}aBS<RM7'
    '&WbCA&A5?H1$khdz39!`aO>>s{wEMct}@NKwY8zr#4G+BB@^ly>o2yH(E`0?;U7H9co72NB`P|kh%s8#P`(6Lf{XaiOln009VIJ^#PVh2E%eyx'
    'Ddh5z^V*9lP`o589xzLW7RJ%htv;B~WK!XSHAchXfefl#wKW%G=W5pW&`fxW+f+mJU^cL}_Y>zP6W~oDE>0MSrlf&y`J(<Xm6IB=+G*-nK5`l6'
    '0Y5|F<xe5s+D-8r78c@~YKalhTy&Xxv^Dp)oUcw2AgU?_HD^26M2MOpM#-fmAL3Jni%T<vt$_8}Q^OY2=%n5JLPTMk>J0d+bi1Gn$@w64_`3z+'
    'XH#O>I5v<#2=swUo9VYM;Bx$Z6aY=ndz22?6Ad3)5OG5=jmy^4bLkNIjOw@?BF<gKhCz7Il1lf*9N$T{qhuFR&l=Gnt6+S@P^vfA{*WTG>0G85'
    'L-cL0KCawPa0H(-3ymGcTno}$JcxKQJr+!()55Unb-aih?zJ>Y)1G7KyPx2s(s$a>b-20ZtnGrVFVWAzOj(->X#Hqsbb`zKrv#57hm6!9<24Vf'
    'htEZmxGcJ~lZj!Np|v&2JkAAt^)HW|KV}8n@oCGefP$vW#InqGLp0SMg+WL}>c%FMWdPF8s?1>C*-WLpj$`<!C#_^ea;|fFyJGjmu(E6%19rR)'
    'jkQnJ+Cu0eVYNS<NY!5pr$j8Hu*Er<n9)5n<RJEQN*G~&FhPl_5#-zM$kKK_|INVMh;DSAN_LGkEG;0gP+q^1979~wHP2g&A1ZQ+pF2g$i73=D'
    'CK_2RS5B0rC1Nr|^r7%kT{|5MO+hw3<`<$AT{y+Ry&S+}yPIhjs8?55%(KS3zr$@O8fC=LG6JPtHQc+>SB64uex;iC7M>*3I_ZbLK&Nr(5y*;L'
    't0L=Xt0H^fSP`ouf@0byDMuCn%;L5BG3|Sn`vulzh!~<pD<1?$xn)$r{E557wi4gxC!q!ng9i8qUYZou4?6?!rV-o;l=F8TbFM8Av5>){3au=i'
    '_i!*YexixiOPM*w>$kmGrc8FQIv9k%Ml<Jf3Z|1Zvwu#NGh>9M3d#66%Q$r(1)1SCq6{Bb7nE^-1ZPUwCFkvp0)%O!EDM2Tn|4Hqp+b7OtpM;*'
    '7z;ezFX362nhiq?!(Qm#|DWRcfumb;q5nMWUO7G1SklRu$^HAo$#RFhTtCe^J+R9)T4n0xpPZwX32INz@K>3)i)U4=nl%q=W;O>-@Qg5`zk7tm'
    'wbG?Vau>jMvpjbz&%fR7UGGP!VvF_$ym3*xH~nnFtn&yflx6P{Rd=XU>#mi2On|Rp<2nt)W%I#Gwfi?mytsA;b+xC_v1$Z<O{)M0IQm^P74kDZ'
    'cHoUp7_<EgP-;(sT-F^~Yn@7PysBvWSfVktMcw@L)gJX=ih`)wFGLpYOpOON+gbZ!paxq5(84k9(uQV)cPDIpzj5KFSQwDnRqwK_f{3-oQ|ek%'
    'X{-;V5oKZ5Hr4>T_9Sh`KjB}+kX=W(W4Tx!>47v+Bz|=br$u-7NFI7_oO4h+@IW<8YIf!HjTrF-jUSRz+&N*?iaB<kPSF=S89l|#lD2jw&130E'
    'VOS0zn_uNzQV+m#3DgFh`kYVF!B9oaEMIi&rwZHj;sVRaz8*Mz-6ekBBc6IXz67V}m(T^f*SqV7K}u<EWxy&sV#1#2O;*@}tF_631}l}A;~<<t'
    'N=_6`y89(aR$rKpyu|~q;3WoEgbvJpBS$c#?<ReHkka%U3}s3Y-~DnGmT$jqq}k>)_5{Ja(`*vi)hTtqF@9-^PerQq5VA__i$pMj&4TRDqb|f*'
    '9K*O?0k#BBgkPCsI9cS-oSh6YqV9VkeC>R#451%XJ)X(xO;!gPhqAv*l$X0aN}Y-iM1+Vp`{6aH;Zh8{Dr-W`mnvv=Rx-Xa#jz2udH{7VBu)cz'
    '<f=l=$Vp({>vaZ3rMV;7R;5EF>e2Z7EC|tW5@FvtzOdMFS#Wlcr}6yb`;)L+0sSwLfQ!(ZA{*k?HZMWXC;9Gd`IMj?r@wCa>8{TX<cltV@8|aj'
    'ArSf|xHx!d$z4-~oDDUPWM<kJ?yFSC`vnB-N;ah9iO2tVbO1SWJy3Tr*+~`=kaEgb*-JceV&L7FB0*YshT@H#91^j^)s6}L&eUu7xJln~%Vz7-'
    'a+JYkyjFu-BeYn}VmFb(PxmY0tF$cy8|<O9X5lJrLJ-WJp;D!s(O_4tB2voBJ%|)Ern|5@A$CRkmtJTx{<s_jP1=~F!eyQ};ML_Wz9z%<I7N2-'
    'D&3Pnagui3&2t}eN%$pO+G5O176RJK?z|qSm%Zxo=z!rZLIL1_TErHeG%16;+S*>@Z#)MV?>Ri29N**{P6kbO#+2z~a{PW&?^|X*cU4!;+%CI}'
    'pF8}r{}E<Ts~(1QChB$545*NsDaLWmw1GLMIi)zpKo1e0=he1YlK3;;nbon>pAu#pTS~WmjH(*5=n-)KSz&VSRKG-ktb?uVyh26_PbNM6%7vOF'
    '%w4mM<vmdT{?BMG|6cXSq(9sG3I*&y8dZz)J?gC|<yl9JOm?DT+1m6q-Ux{*DDHCp@;hS!OD|(KDn)}%F~<7Sfc>qc7OIlXUEjCk$0N16yT+Ed'
    'LxHToGt$!^Y1+wm&9VIxKmLiyu=Wy7`y<azq8mcZf+RsKW9F?a2+Hn=E#8_}+Xa7F{E@{o`t*DLY1Bm{L!Ysdix{@sK!U0m$I0_z%^r(Uz%d!f'
    'vTE?i<@JySQrkc!ARsWyN-D1NZj%niX4$L20sTl+qxU}I(qv{jcqk%|fm8j9B!aZ=i??f9JejQu8%2DIMPzRmTT($JsIS(Vo)~)G?M(2lovK1s'
    'JQR5Y%ft}55rOf;Fv3A8!@a97dbXrG9w+Ajk_fjnISIH=YouULe`n&3Bs5jC{F_Blp|4w}Wax}s4M@Uz@15--Q+C+Hs9|4gGYUgkUPddjdGBJs'
    'oH)XlJ{QQ&;}msOP}|U3af}LG+c2zr-lT1k?FPe{H~vxQHbLKXta0wOtaFnT?>N%DJkK>mUMEr~wg`rdys1l^TlTn4MrK&`OVYrhakQevZ~*CD'
    '>F4f3t2MZ0{SG{`0OEzt<#1dg{x$&73&J)-8}chTS`5tIs=oG!T8@!!TBl_KwJcTcZb|4kV|%%wHKq4WJ@pidtQDNY*!K5bv`~!JMfVh&2P-1^'
    'ZcY4dW*zs}^R(*{nA)|=Cm+=XM+Ut>Wp1HK##GWPULtAb>0xajEh$5q?DyF8JUS%q>!$(Po=4{NymX{p8K9r~7oLt?f^HmHkzE&N_TIh8VGPE='
    '{BsQph%TDUJ}l`!;kocih+x0*HcPZQ1j+Bj-@^l=l4jMKoLu)SdgSR(YP-e<RcL#`Pm{rjijn&r7qRJD|6XG+LRr(P3}hD=+PsQc8~40*DMY{c'
    '+y+;mqT}UHQNYtGEhehuh2Ch9+lZ8&=5*W)(Ol+>SrlFbbak_JQbT-qiF4j-0k*I+-*rRLUJ`3lXa|mK>S)Xv*0s?$GSLB$q{h=c34FF6bU187'
    '<+TWghhZA~++zw=`buM^giKxrpia0Pu{iJuC`F;BBjX+ytWrVUzLzp_8gnPTKB^X@v}2|R-IrU%)jaYsfu<Lo-fOM0XvdcCD~N?~Fg#9G08n}>'
    'YqF9(OxN4<gjVDbbW>E+Ab*}zQO^T%OnsYD(QolDnxIm@>{xD$<Pjd35_-1%tJVy3{%1bM3{UnGPt|G3dcD0k+UTi?@6>pEkMjx9p@nk6{Fp%8'
    '+t*A=>X#P0?Q_W9>_&f}QLRKp#&6A3PuEd>)E>7N2EXkCP0zI9j0MdL<qefU_*#jn=DVh3SC|82J^>Xzv*NAY*daV;#DQA8gRVG{E?&s&#P-*a'
    'tXb32bT}kp(4F`J`CiHg@MjvU&>8GA7?DU7KIr~-qPg7~7JRtG^^w3pi+o#q)UHjSm`YF=-Gp~Y?B@UjlT+-3rB6AR32qtm8@$}gIngivP+IEe'
    ';c}G>K`I(D|8g6WNp3S?5w23a5L4T91!nd}I;L&ay$_}0L^#WbY%PUb`1{!L1d)2nKk7JO_rtO%K0-O-R(`_8_b}i$P8RGLD0mLI7>*~@s;I+T'
    '$4R?2m)%iVaYMX60ttosDI_vFqX8UnhayPKQWRVYl-8FhmzFh?i`Hi13L+~AZ1p|as^uj<6f#RdZ&d1}-~d4tcRfG3+vNom-3)@r;m{5iQOVKL'
    'M5(V&nV6?oDqbf=Cb~k?6Gw3rQ0mnBf;=asu*_y&`EMpZS*8S3WYCac1XvylflzwVCq67X?<h7At+=B{S(O1h3ERZ=LXp!=h8L)Di=P{`2aU=%'
    'JKn-FY=;-&x5h2`YIu0sHUEEA+jyrGdipGG`&!7**8<d)%7>I?`>tx5S)4}AX$yHQYG;Fd&kpxHt}BK9+@=a%J%1CCOsu3wn(v&GJ*K@g!Z>Mw'
    'YpE|<UCXd<IphMF<s4dfEuOlM*`TK6(%KNbLTiO#pAo?YA7ltewkzOBc#t~ervRqvT=HiGx?Wz;z8GYxUAzv2M$C8_cE=76ewce~S%nV_J@~!>'
    'tXZzx*2Ywdl`%`Pik9zKQ$LPIyuhbn&Lo?Nh7ZN50f>4on#Xz9DyBC%M(=~bv~9%U=#C?q8pa>EYVGMut{RvVmn*BuI5<x-G;TRi<@~`*;GIyK'
    '<?#EBK&^c$IpvOfFykq9HN8`NreERkmNcyWcs(kzu&F#087FDU!|X-ygYG<f9(3$OOpVTwswQ0^YE(3_0Q1qO>S+sr2g1Ve3y^Z=<3WGK8*HEg'
    'rA9=Xoghk&okaO5Ua^P`<QZu|mYFj^&+|@w%1&xbwSX^c^!C_TLb>Y?KFHUPoUMk_%5)IgIxs8N>&{maGSRP+d?X9hZj$lwRvKz$>jy|VL|dE&'
    'Q=noX@g|n1+9`}OGkEV|OQFeV<?#;#5dlxCJ!#1G=AIAb(gh$nVPI;rQ-9$EDW@d~T4|mH+~j!q<+DyA0snLr>mb}Q^-(*&DF~<}v}_ra_Mi5&'
    'iiUVdV~5~#G{TU-vHW4%ABQr7WFbkb!M>q9!8G<*vdObo^aXfCDM`l#H84Kr2fn?d+?*D+qo<l^Cx@!;@JWIQ^QnsxSx;i$PYl$j1u^q?tDE7('
    '&eN}pZ>KxgiM&7x)(J*Bx^r=`yn*(o`A^LvQP++XYauQ@7Bj7^Km0#|V);%s0T!97>wJI@vmFX4<;^t#plJnfgBRTK6$|7{2=pf+;CE5s^=1O3'
    'KVtxtwgxk2F7d>p0$j|k0WOji7h62*e7oAqX2K&6d*5-6T6%A+MujK9*}!ec1t)KPO$G)g6w5#?o3(D@zm(~_jgWvC2|zSvHaqGba;`IC4w@i-'
    'P1z90E6tW%D?>}3^X#R7M8%@FDDh`2QJ8{qljE;98N&G``Qi&YFdh=NAp7-f#t<+z@B4*&BV2pAoT?n{DAZ`FtWz}(>^1d6v7)?wum#kMCx0d2'
    'No}5brq^;&WyeZ<T<*~@#ItTx6O&64hS4qQ5Yz3bl1}+P^U@8uOuXF#%FC78mrzWT&oJ+vS{&mc*Hn0G8DZdUYO+$0YRRhFRYUaSB1pfuWL%>E'
    'l9|gdXnKG9qAE5>V>q+yvD`uUe+S)UVC2)>X=&Tk;KrC?+wQe72*M#|(rKQK?f)O$f4Z*kkw3A}*wz)5)gRP0z5evM-a7`0F3TJ64X>*RP|?nZ'
    'i+2v1uli8H?>4jQ>+Z`OX`?pEQAvChjc!Yh`%}8ZB$w6r^^%TXlNhUajg#q~(?TJ|LO8~+6l{#ydL&&<_wV6g{dEUMA19-$6h9<m=9YY4I+Fa&'
    'NFGv_P44jDPD+nsAh0;due4wd^+*}O`)+Mn?&~TMfEP*0X6=e8IIFs0fe7{5vvq@fYTky2Yd}XAYU;hGW~Fa@hrBHM*2*|CaZ#<tC(S#Kjvai9'
    'V~WwBEFU%WHZ!(M(;N5rWHFR`hwF)Ka)z-5qXG|u3mnT4jJ?GJH3;7fE6$72aCU=%Vy47pRDq4Bx-?%eJUxP9@ZXgwBtK`mB;pliJ%oEqeJfBG'
    'sL<}O%gE~u<Rh`v?^m^iiXqMq{fuBQJA-=2sL`sr`PRJsQx4zW`k<Ar)TyBQMq~IjJ5MC_U#Tj2Tk$A>vf82yzsy1YLXiF<=dFZus0BBwzkc2v'
    'Ldig|wN>3Q@wxe}XKU<fZT37ZW2oaYzW@_U;<D2f3Gd`y*TR7Z=BZZ$Ld28}jg&(7_I(ZD5QBs2OD^?Iyx4|9IY}p|=G|;ENIt~Ubs9VRAlG%3'
    'wt?x|9TB+IY+-IqK`!y+J+_-}*%5aWO<SUWV`dAmwdLQs1zVNZxe2Uu>@hJ3-wteS+Akscn=BfHtwFJLGPX+1Sg5#z<C<Wmrv~t;QxrL5Q}Ri%'
    'Qy*YYa3_HFbSJ?XhNaO@@2g~}mj6l$guKjFGCE<X)zeGYtcHbgX^l|t$~#_FEf)q!{F;mTwwv>u&bpehsA7HN0{iYU7xxf})59psES4)LopsO^'
    '7w~L(NCz#w*gT8h5!x9-Xzk}pWxB~$I(sj&bXJ5bg#zFK{Aw656DwoAbMtG80yy1S??-;F?#Rci#e3te$!94#HMl*QzdcuHJ5<(wo934ydZzSZ'
    '-HQpZOrREO>%7%y{#|*)470x-i#}!=n652EWAV{yUMDaYSS@ytmVho2M9nnQH;@_-HPiZN0YpyRC7Yh%l8ED);DFX&utd!u-q;J0wzdo{dGHTE'
    'm?yx5sS~`z;Naz^=O=v~eBk}6bQF37>n8@_(JjM$0tEbIleo>%2%`9E)DTTtpq{W*uI#V?5qoH!W<3@R9_WYnZ+^2O<^AZ&+YC^J$(M=|#Z|*K'
    '(J`c~;o)x(!=d;Ljjms&vgl;h9Lyvwrbmf<<H=-9{OK6DZ^2+r8aE_Y@xW}vK1i;tCf}xhv_5XsVFTIH5?I?qPoA<d4Q;is0P1W%y4~S(hIuJX'
    'tdLTT477PZ{D>|RheEv=F*-o-9`<~fAl#UiQx5yj${;@cO*!K_+Ys&40Jw8+<eb1w3M+@oYZs&9X^ez6(u<N<zoiwapjxd6`()XkeozCu_OWQV'
    'zsv=T%Q2_`erAQZfv!}4FLX3Q96YyB_tb1?Mlj~n_Xe=<bcoZN!p$LmY`_i@>}043zbUslfQGxY<LrlYojO_1vb`**ilTe^E{X+=h=k0ws8m8X'
    'zVc!%RQ|A59pl%tS>j^H3-H=LrupwzgH4Z9AEEI5I+(DoE*iuw{T^1nmfOM~f&5Vc6P~(WvC#w%@(c~eaqJBk4HVA9h#|W!PMWp;2w9M+o~()R'
    'IJEjjC#6*Y?}t2Gq>2gm{}q*?ssJnjaAtZ)x*!w6;rq9pMd+8&9(9l|mV)=i(J@4bdrX2zIX}k@4kl9R1x>ZeL7S*fOV*7rsPaK}PvpFao%dlt'
    '?jYBQJLB+Ye@9^`t&ZLUi~)a`=4_5Y0qDE@0u#%SSWL-bZR%WY`&>HZvIFo>SWl(~GI`VmZbrw<5j(OM9$RrrUTqG2?~o;RAgNKS=zDym%F8*U'
    'mi?{$gAWHa4j<p@f*zVELqL3K(^~^O2oAK&l`Bp9)02-?WJ;F1jXby5xg)bg08$?U$N4oe8oU`}`k}h*4XEw&m&5!r&DuY4Lffm+I#j>Y1Pk>|'
    '0*0h2xu!AA5luSu&jVFP_4BZ^p%+fW?#YbuI5g$8o@-;bfg@xz1{;qsAI63QE`nk+SMC4%`vXreQn5fT%wZ&V;T(D&9byvhpQlUVI|-PXFJW?u'
    '?%J7YVk@JKP)tb>Y-unaM@qGDhUQ#-|0_X}sy>K~rmZSQ%WI*2q5cHnw1j#_boN714&d<&;0QRDH8NChw7%UsN{(AgiRwb)Af3np&VQ!7irKje'
    ')i{Sv{SABEaY`Dg_`Z9_ZIo(evv9=sQ<<e`LI}L=s0C(Mpi1fE#(S85xe!IKlJ8KpGF4LeU=jMGdU~U~<bDNn<G_CYd}W6O7yA?*_-3o{GrPY`'
    'y0Wg6Zz&nM!y!&+tPm<TH!ne|I23_cT2&;#|3+z+Hv)zB#jN?+z_DMKN<3Ch$PA)(Xk;sxo=#SYe}*hn{2SjCFm0WJa0v{>%J-WSZsT)Of$fQG'
    'eM7xr%YcV3us*m+$HWfx3luDYwx6pkyj~lJ?j#dnvD1XVEWbb}B^?|)*=SQb`~z^cA}SE2Z5m;Hg=ffK3M@6&lsr@FK#Uh{I99h?$;B;~s+X}5'
    '+AK@Pq05E(Q+_?JvBIXjb#G5}5fp;;%2V}Q3Y!_1!e;>R0MdkAyi4oY5Sc72y&~~?kE%_WfQZWBSdNu{+hXva!P2Kk_Q6_60hVo>?6<<t##PA-'
    'G6$28@jQOhg;WcOg;T9G)7#_gvMS_l$Hc)LZQIL5)(y~*y6bDj82%02Jl8kKu!iNV9?gG*=B>=-?>*EYG@wo+Le3UB^i}2Tp-U{K8ICm0%CiDX'
    'usnLDO3;5)^eGoo;3#dPu7aX>-WjJD7khxXxOJ1S5I}RW!^cj;d73+ei|1f$^jZvBJdynZnMi47u=DZt;B5_6@?yF3k<@|njXAOhsPP<rYEIlS'
    'y)CD>IA6H&4wJ<sebB*x>RlR7K}l$6AAH(P7b?(?kTO{S5odocA;?Xk3z$}|QwP>$_bC$oNd`oh2h1j+PhaOMa9$BQl#qOaS2S#=pTs|ZI2DWe'
    'v@zpx=agu1E0`N_#{c2SBsZ3tz=Ixg7dckh#z1ZQyava%d_)Y^XE0b{NPr|Z1@-`al1Xx9uv4V_%5!95O${NsIitT68Bm)#Ef4>y_SW6bI4IAK'
    '|Je^gS0(^nSzZ#Aes=E`0Vpnn$0C@}vqf#O8HMYERh%Ms3PRF?BVF@SohfP-#-L5`&Y=QnW(4OO=hqxt>vZazr@YDK!JN1e{hdn1*q(6d)v8M3'
    '*m%|0qHtpp3@9Wz-AC`0_uygrjOt@0=KXAib|VNFOIDFFs%aED=R%C&qIyPoBpAN7t_sGp{Hdfx!+G;Z)<k8L%VMoafWM<x4SVz3bncmw@&{^>'
    'uwex0E9lUQFOqT3AVE-2f^XYkZvmg8;J**=3o@Dx8;WfRt=cVY2|%H|^I0u2e9pXBqLFKxy93qh{hC_&p9@>giA%ViC;TY93pms@WjFNO$^2X^'
    'dc4zjkIJuZzm}cs1EaAg*x?t;`r%DVOY%wB1ZQlthD@2gdd766F}j6BX8O%H1VTIPZaO`i6ALsRU?m!ir6`{)SJKYP|MOnRmkGI~krE4(l_a}9'
    'TwpeKLh~;6t^UQnIm>%?lFpBK`&)!(Xe;rKGl=OSQ{QIS`VvDRLfFND)S1~W=wkMgezyJeAlJ~s!`b2Ze2uM`v$43kbgZBBm}VOD75jVCd*x^*'
    '7ZDdSm^?PjNj4t`n{Op2j(OkL;xxyio~=^->K_hxh%Ou~ejnbtwh&74nXUM~(RC=D8s3WU1%+6pR99PmD5Np;hKhv^gE#LYa7I>=dw_itx#r9Y'
    'NHT$!$XTxBvnl`=oMCH9PBJ8*D|gqTZV1_*YZ9Xr%SiGxp&d!Y!+0yKX1NzMKE0(*;!z+#h3-<Ac>#_)J0n%YL3hx}>=izFu|N9pY>6g*7*I+T'
    'LuI9uAhBK!70f3o49?w4fU@B~Ze=Qz2>J*A@`cAx0jBjAVBuu}i$@GgQa1{*0J_Mq$RDV|#$tFwc>U?bx&nh0(ts2bo4vgF-QB7;WEKGBZ+<;f'
    '^{CWaIve3$zmyy;`GB9#LB|o1PzSzQ+y+FD#Y?xNFCeAs&lvX5*#z(kss(?e1acJ0Pm%g6FhCj;<d^uo4p_O(Km~VU7tEF4B+#1Z;NoB4GHpLb'
    '0M716Rl-R=M+Bc4DRd5ko4@$wPzi8pf<KMx4wWTFGpDpRzAx`BW4vQG>`Z})D=u#y30-e$fWf6bauNi~*s`MwyA#5;W8j`ah^2lKum#t`7HGs1'
    ';aJ=YpWrU)T;Y?ut8Sv5@~D9mzcg8h(KGd`(iNQg#I~FDHAxUe(x(JYs?ZPUdAX3^ML#|_1ft$29vLcQhT{y+qhW$0q%J?(x|)lGIh3Bw`A-o<'
    'XArmv1SR7*c})WaW#2TZu=v|Rk~wL2Q`~&K>eUGT4HuQxul*^iV3|I`(aQvmDYEQWl#<JO$uPj0J#DgzLP2GpAn4ryuZ<AVHx#`T-oFK)hYcT6'
    '-rN{Xvc-}hm%vz}T$nu>HF5FDxsIu89zvo52GszfW^5#!-QpQi<ix^jg{=w~ON_G1Wn0&!qmpxsc9c(vNR`dadZ%Uk&1M2X@(z`FtbmARQ$Khr'
    '+Lp@5P1?C#frCpYRMY+`ZU?Y|<oWFlJmBBIz;i1SfwQ2D7|}7S0TNqeHJ#VzN+37SWQT+&L)BXUc@X4m%6(hJyH<*=aa!wdz{%Unouv-vR<||b'
    '%eL&_8m6^MD*+-}1<Hv8_dF}>f<S_AYe|BoI)mP{>ytllK$3*t?$KXLCU6Ew%D%Ue>lx8fwxox&r>asY!q(+vdX<cHEYHiH&c>#bP*H-wp8NV&'
    '<`{m4YhkBYIAl^@yzYoMk=1c>3wG42S0j?o+)%PGXbs2M+G-7gv3gZ^o<I*g1OW2H&j%k_95AadU||GPqZy8TqvdWnOA+EhWv(05qSBPLWw!h)'
    'B)qUFH$J<l5pmH)wAJpaB;9+JGdb1G_E8UYg%1`$W9-@61&ImZFMrH)NVJ&IIjL3Ktf5=z+5g`3mwfy65T&!qGJ)Sy0LU3nQF|R%ssI20KaQc&'
    'Mf^N@00EZl1Ay=l>Q2QUvBYQl0ssI200dcD')


if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
