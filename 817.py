
# AKBASCORE SILICON HIPPOCAMPUS — TEST817 (CORRECTED)
# REAL SCIENTIFIC DOCUMENTS / SAME-CARTRIDGE CLAIM COMPARISON
# ONE COLAB CELL | Qwen2.5-72B NF4 | A100 80GB
# NO TRAINING / NO RAG AT READ TIME / NO NEW ENGINE
# TEST816 continuation; locked TEST815 prelude.
# The two papers are NOT pre-certified as contradictory.

import ast, hashlib, urllib.request, json, time, traceback, gc, re, csv
from pathlib import Path
import datetime as _datetime817

REPO817 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
LOCK815_817 = '77774f87428c0243c9a86ea6a041364acd9c1b03'

def gitblob817(b):
    return hashlib.sha1(
        b'blob ' + str(len(b)).encode() + b'\0' + b
    ).hexdigest()

req817 = urllib.request.Request(
    REPO817 + 'main/815.py',
    headers={'User-Agent': 'AKBASCORE-TEST817'}
)
with urllib.request.urlopen(req817, timeout=180) as f:
    raw817 = f.read(120001)

assert len(raw817) <= 120000
assert gitblob817(raw817) == LOCK815_817, 'TEST815_SOURCE_LOCK_FAILED'

tree817 = ast.parse(raw817.decode('utf-8'), filename='815.py')
try817 = [
    i for i, n in enumerate(tree817.body)
    if isinstance(n, ast.Try)
]
assert len(try817) == 1 and try817[0] == len(tree817.body) - 1, \
    'TEST815_AST_BOUNDARY_CHANGED'

exec(
    compile(
        ast.fix_missing_locations(
            ast.Module(body=tree817.body[:try817[0]], type_ignores=[])
        ),
        'LOCKED_TEST815_DEFINITIONS',
        'exec'
    ),
    globals()
)

# IMPORTANT: Imported prelude shadows `datetime` with the datetime module.
# Keep TEST817's datetime reference independent.
import datetime as _datetime817

RUN817 = 'TEST817_' + _datetime817.datetime.now(
    _datetime817.timezone.utc
).strftime('%Y%m%dT%H%M%SZ')

DIR817 = Path('/content' if Path('/content').exists() else '/tmp') / RUN817
DIR817.mkdir(parents=True, exist_ok=False)

OUT817 = DIR817 / 'TEST817_results.json'
LOG817 = DIR817 / 'TEST817.log'
REVIEW817 = DIR817 / 'TEST817_independent_review.csv'

DATA817 = {
    'test': '817',
    'status': 'STARTED',
    'locked_815_git_blob': LOCK815_817,
    'scenario': 'TWO_REAL_VERIFIED_PUBLISHED_SCIENTIFIC_ARTICLES; CONTRADICTION_NOT_PRESUPPOSED',
    'sources': [],
    'checks': [],
    'reads': [],
    'limits': [
        'The two papers are authentic, but may be complementary rather than contradictory.',
        'Correctly reporting no established conflict is a valid outcome.',
        'No automatic semantic truth oracle; independent scientific review required.',
        'At inference, no source-text replay or external retrieval; physical CUT3 memory only.',
        'Same-cartridge creation combines two attributed excerpts before forging.'
    ]
}

def save817():
    p = Path(str(OUT817) + '.tmp')
    p.write_text(
        json.dumps(DATA817, indent=2, ensure_ascii=False, default=str),
        encoding='utf-8'
    )
    p.replace(OUT817)

def say817(*xs):
    s = ' '.join(map(str, xs))
    print(s, flush=True)
    with LOG817.open('a', encoding='utf-8') as f:
        f.write(s + '\n')

def gate817(label, ok, detail=None):
    DATA817['checks'].append({
        'name': label,
        'pass': bool(ok),
        'detail': detail
    })
    save817()
    say817('PASS' if ok else 'FAIL', label,
           detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST817_GATE_' + label)

# DOI/title-locked real PLOS papers already used in TEST815.
PAPERS817 = ('PMC9521804', 'PMC9401135')

PROBES817 = [
    (
        'POSITIONS',
        'Describe what Source A and Source B each establish about '
        'persistent identifiers, research data credit, or long-term '
        'availability. Keep attribution explicit.'
    ),
    (
        'CONTRADICTION',
        'Do these documents make directly incompatible claims about '
        'the same proposition under the same conditions? Identify exact '
        'claims if so; otherwise say that a direct contradiction is not established.'
    ),
    (
        'IDENTIFIER',
        'Does assigning a DOI by itself guarantee that research data '
        'will remain retrievable forever? Separate guidance from measured '
        'observations and identify the evidence.'
    ),
    (
        'EVIDENCE_GAP',
        'What additional evidence would be needed to adjudicate any '
        'apparent disagreement? Do not invent a winner. If there is no '
        'direct disagreement, explain the distinction.'
    )
]

DATA817['probe_sha256'] = hashlib.sha256(
    json.dumps(
        PROBES817, ensure_ascii=False, sort_keys=True
    ).encode()
).hexdigest()
save817()

try:
    gate817(
        'LOCKED_815_SOURCE',
        gitblob817(raw817) == LOCK815_817
    )

    required = (
        'model_setup', 'physical_commit', 'build_fusion',
        'free_generate', 'safe_load', 'memory_seals',
        'compare_seals', 'sentinel', 'release', 'acquire815'
    )
    gate817(
        'NATIVE_SYMBOLS',
        all(callable(globals().get(k)) for k in required)
    )
    gate817('FRESH_MEMORY_BANK', len(entries) == 0, len(entries))

    # Fetch and verify sources BEFORE loading 72B weights.
    docs817 = {}
    texts817 = {}

    for pmcid in PAPERS817:
        body, meta = acquire815(pmcid)

        gate817(
            'REAL_SOURCE_METADATA_' + pmcid,
            meta['doi'].casefold() == ARTICLE_LOCKS815[pmcid]['doi']
            and ' '.join(meta['title'].casefold().split()).rstrip('.')
            == ARTICLE_LOCKS815[pmcid]['title']
        )

        texts817[pmcid] = body
        docs817[pmcid] = meta

        say817(
            'TEST817_VERIFIED_SOURCE',
            pmcid,
            meta['doi'],
            meta['title'],
            meta['xml_sha256']
        )

    gate817('TWO_REAL_DOCUMENTS', len(docs817) == 2)

    # Unchanged locked model initialization.
    model_setup()
    before817 = sentinel()

    labeled817 = {}

    for label, pmcid in zip(('A', 'B'), PAPERS817):
        meta = docs817[pmcid]
        ids = tok.encode(
            texts817[pmcid],
            add_special_tokens=False
        )

        # Bounded source excerpt, not a whole-paper claim.
        excerpt = tok.decode(
            ids[:380],
            skip_special_tokens=True
        ).strip()

        gate817(
            'REAL_EXCERPT_' + label,
            len(excerpt) > 300 and len(ids) > 0,
            {
                'source_tokens': len(ids),
                'kept_tokens': min(380, len(ids))
            }
        )

        labeled817[label] = (
            'SOURCE ' + label
            + '\nScientific article: ' + meta['title']
            + '\nDOI: ' + meta['doi']
            + '\nPMCID: ' + pmcid
            + '\nPublished article excerpt (truncated):\n'
            + excerpt + '\n'
        )

        DATA817['sources'].append({
            'label': label,
            'pmcid': pmcid,
            'doi': meta['doi'],
            'title': meta['title'],
            'jats_xml_sha256': meta['xml_sha256'],
            'stored_excerpt_sha256': hashlib.sha256(
                excerpt.encode()
            ).hexdigest(),
            'source_tokens': len(ids),
            'excerpt_tokens': min(380, len(ids)),
            'truncated': len(ids) > 380
        })

    save817()

    A817 = labeled817['A']
    B817 = labeled817['B']

    carts817 = {
        'E817_A': A817,
        'E817_B': B817,
        'E817_AB': A817 + '\n' + B817,
        'E817_BA': B817 + '\n' + A817
    }

    # Physical write: use the locked working engine.
    for cid, body in carts817.items():
        n = len(tok.encode(
            body,
            add_special_tokens=False
        ))
        gate817(
            'CARTRIDGE_TOKEN_BUDGET_' + cid,
            0 < n <= 1150,
            n
        )
        physical_commit(cid, body)

    gate817(
        'FOUR_PHYSICAL_CARTRIDGES',
        len(carts817) == 4
        and all(cid in entries for cid in carts817)
    )

    for cid in carts817:
        cp = safe_load(entries[cid])
        gate817(
            'SEALED_RELOAD_' + cid,
            cp['book_id'] == cid
        )
        del cp

    arms817 = [
        ('A_ONLY', ['E817_A']),
        ('B_ONLY', ['E817_B']),
        ('ONE_CARTRIDGE_AB', ['E817_AB']),
        ('ONE_CARTRIDGE_BA', ['E817_BA']),
        ('TWO_CARTRIDGE_AB', ['E817_A', 'E817_B']),
        ('TWO_CARTRIDGE_BA', ['E817_B', 'E817_A'])
    ]

    def read817(arm, ids, pid, question):
        tag = arm + '_' + pid
        t = time.perf_counter()

        mem, active, steps, _ = build_fusion(
            ids,
            'TEST817_' + tag,
            True
        )

        try:
            gate817(
                'NATIVE80_' + tag,
                len(mem) == 80 and list(active) == ids
            )

            prior = memory_seals(mem)
            n = int(mem[0][0].shape[-2])
            first = int(entries[ids[0]]['body_tokens'])
            expected = P + sum(
                int(entries[c]['body_tokens'])
                for c in ids
            )

            gate817(
                'NATIVE_LENGTH_' + tag,
                n == expected,
                {
                    'observed': n,
                    'expected': expected
                }
            )

            spans = (
                {
                    'B0': (P, P + first),
                    'B1': (P + first, n)
                }
                if len(ids) == 2
                else {
                    'B0': (P, n),
                    'B1': (n, n)
                }
            )

            # No gold answer or source body in the prompt.
            prompt = (
                'Answer from the physically mounted scientific '
                'evidence only. Distinguish claims, observations, '
                'and uncertainty. Do not assume the documents '
                'conflict. If a conclusion is unsupported, '
                'say UNKNOWN.\nQuestion: ' + question
            )

            o = free_generate(
                mem,
                prompt,
                seed=None,
                gain=0.,
                max_new=160,
                spans=spans
            )

            gate817(
                'KV_SEAL_' + tag,
                compare_seals(prior, memory_seals(mem))
            )

            return {
                'arm': arm,
                'probe': pid,
                'ids': list(ids),
                'raw': o['raw'],
                'generated_tokens': int(o['generated_tokens']),
                'possibly_truncated': (
                    int(o['generated_tokens']) >= 160
                ),
                'read_seconds': round(
                    time.perf_counter() - t, 3
                ),
                'fusion_steps': steps
            }

        finally:
            del mem
            gc.collect()
            release()

    # Six arms x four questions = 24 native reads.
    for arm, ids in arms817:
        for pid, q in PROBES817:
            row = read817(arm, ids, pid, q)
            DATA817['reads'].append(row)
            save817()
            say817(
                'TEST817_READ',
                arm,
                pid,
                repr(row['raw'])
            )

    gate817(
        'READ_MATRIX_24',
        len(DATA817['reads']) == 24
    )

    gate817(
        'FROZEN_WEIGHT_SENTINEL',
        before817 == sentinel()
    )

    gate817(
        'NO_RESIDUAL_HOOKS',
        not model.model.layers[CUT]._forward_hooks
        and not model.model.layers[CUT]._forward_pre_hooks
    )

    # Independent human evaluation; no invented truth labels.
    cols = [
        'arm',
        'probe',
        'answer',
        'human_source_attribution_correct_0_1',
        'human_contradiction_assessment_correct_0_1',
        'human_evidence_supported_0_1',
        'human_abstention_appropriate_0_1',
        'reviewer_notes'
    ]

    with REVIEW817.open(
        'w',
        encoding='utf-8-sig',
        newline=''
    ) as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()

        for row in DATA817['reads']:
            w.writerow({
                'arm': row['arm'],
                'probe': row['probe'],
                'answer': row['raw']
            })

    DATA817['review_csv'] = str(REVIEW817)
    DATA817['review_csv_sha256'] = hashlib.sha256(
        REVIEW817.read_bytes()
    ).hexdigest()

    DATA817['scientific_conflict_verified'] = False
    DATA817['semantic_scoring_complete'] = False
    DATA817['status'] = (
        'COMPLETE_MECHANICAL_REAL_SOURCE_COMPARISON_'
        'HUMAN_REVIEW_PENDING'
    )

    save817()
    say817(
        'TEST817_COMPLETED',
        OUT817,
        REVIEW817
    )

except Exception as exc:
    DATA817['status'] = 'ERROR'
    DATA817['error'] = repr(exc)
    DATA817['traceback'] = traceback.format_exc()

    save817()
    say817('TEST817_FAILED', repr(exc))
    say817(DATA817['traceback'])
    raise

finally:
    gc.collect()
    if 'release' in globals() and callable(release):
        release()
    save817()
