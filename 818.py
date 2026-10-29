# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST818
# TWO REAL SYSTEMATIC REVIEWS (N95 vs SURGICAL/MEDICAL MASKS) / PHYSICAL CUT3 CARTRIDGES / SOURCE ATTRIBUTION
# ONE COLAB CELL | frozen Qwen2.5-72B-Instruct NF4 | ONE A100 80GB | NO TRAINING / NO RAG AT READ TIME / NO GRADIO
# Direct continuation of TEST816/TEST817 (both completed on A100). The locked TEST815 prelude is executed unchanged;
# no engine function is rewritten. Only the experiment layer below is new.
#
# Source protocol (fixed before the run):
#   SOURCE_SCOPE = VERIFIED_ABSTRACT_BOTH_SOURCES. Each cartridge holds the COMPLETE published abstract (never
#   truncated). The abstract comes from the Europe PMC "core" record (resultType=core, query PMCID:<id>), which is
#   available for both papers. Identity is locked by PMCID + DOI + title; the PMID must be present and consistent
#   across channels. The Europe PMC JATS full text is fetched as an independent identity/content cross-check. If it
#   is served and its abstract is a word-level superset of the metadata version, the more complete JATS version is
#   used; if the two versions conflict, the run stops. If JATS is not served (e.g. HTTP 500 for the Cochrane review),
#   that is recorded with its error class. No unverified text ever enters a cartridge.
#   The experiment therefore measures abstract-level evidence handling; it makes no claim about full-text coverage.
#
# The two papers are NOT pre-certified as contradictory. A correct statement that no direct contradiction is
# established is a valid outcome. Scientific correctness is NOT scored automatically; a blind review CSV is exported.
# =====================================================================================================================
import ast, hashlib, urllib.request, urllib.error, urllib.parse, json, time, traceback, gc, re, csv, socket
import html as _html818
from pathlib import Path
import datetime as _dt818

TEST818 = '818'
REPO818 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
LOCK815_818 = '77774f87428c0243c9a86ea6a041364acd9c1b03'          # git blob of the GPU-proven TEST815 engine
EPMC_HOST818 = 'www.ebi.ac.uk'
EPMC_REST818 = 'https://www.ebi.ac.uk/europepmc/webservices/rest/'

RUN818 = 'TEST818_' + _dt818.datetime.now(_dt818.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR818 = Path('/content' if Path('/content').exists() else '/tmp') / RUN818
DIR818.mkdir(parents=True, exist_ok=False)
OUT818 = DIR818 / 'TEST818_results.json'
LOG818 = DIR818 / 'TEST818.log'
REVIEW818 = DIR818 / 'TEST818_independent_review.csv'
COMPARE818 = DIR818 / 'TEST818_source_comparability_review.csv'
OFFLINE818 = DIR818 / 'TEST818_offline_evaluator_inputs.json'
STAGE818 = {'now': 'START'}

DATA818 = {
    'test': TEST818, 'status': 'STARTED', 'run_id': RUN818, 'locked_815_git_blob': LOCK815_818,
    'scenario': 'TWO_REAL_SYSTEMATIC_REVIEWS_N95_VS_MASKS; CONTRADICTION_NOT_PRESUPPOSED',
    'source_scope': 'VERIFIED_ABSTRACT_BOTH_SOURCES',
    'stages': [], 'sources': [], 'source_events': [], 'checks': [], 'cartridges': [], 'reads': [],
    'limits': [
        'Abstract-level evidence only: claims that exist only in the full texts (included-study details, risk-of-bias tables) are outside scope.',
        'The two reviews may differ by population, outcome definition, study design and literature window; a difference in conclusions is not assumed to be a contradiction.',
        'Automated diagnostics (number provenance, UNKNOWN markers) are not semantic truth tests; blind human review is required.',
        'At inference: no source text, no reference answer, no retrieval in the prompt; physical CUT3 memory only.',
        'A one-cartridge AB/BA memory concatenates two attributed abstracts before forging; it is not joint authorship.',
        '42 native reads completing mechanically does not mean 42 scientifically correct answers.']}


def save818():
    p = Path(str(OUT818) + '.tmp')
    p.write_text(json.dumps(DATA818, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
    p.replace(OUT818)


def say818(*xs):
    s = ' '.join(map(str, xs))
    print(s, flush=True)
    with LOG818.open('a', encoding='utf-8') as f:
        f.write(s + '\n')


def stage818(name):
    STAGE818['now'] = name
    DATA818['stages'].append({'stage': name, 'utc': _dt818.datetime.now(_dt818.timezone.utc).isoformat()})
    save818()
    say818('=' * 24, 'TEST818 STAGE', name, '=' * 24)


class Gate818Error(RuntimeError):
    def __init__(self, label, error_class, detail=None):
        super().__init__('TEST818_GATE_' + label)
        self.label, self.error_class, self.detail = label, error_class, detail


class Source818Error(RuntimeError):
    def __init__(self, error_class, message, detail=None):
        super().__init__(error_class + ': ' + message)
        self.error_class, self.detail = error_class, detail


def gate818(label, ok, detail=None, error_class='EXPERIMENT_GATE'):
    DATA818['checks'].append({'name': label, 'pass': bool(ok), 'detail': detail, 'stage': STAGE818['now'],
                              'error_class_if_fail': error_class})
    save818()
    say818('PASS' if ok else 'FAIL', label, detail if detail is not None else '')
    if not ok:
        raise Gate818Error(label, error_class, detail)


def sha818(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()


def gitblob818(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


# ---------------------------------------------------------------------------------------------------------------------
# Sources and locked experiment panel (fixed before any network access or model load)
# ---------------------------------------------------------------------------------------------------------------------
PAPERS818 = ('PMC8552225', 'PMC8094623')
LABEL818 = {'PMC8552225': 'A', 'PMC8094623': 'B'}
EXPECTED818 = {
    'PMC8552225': {'doi': '10.1002/emp2.12582',
                   'title': 'N95 respirator and surgical mask effectiveness against respiratory viral illnesses in the '
                            'healthcare setting: A systematic review and meta-analysis'},
    'PMC8094623': {'doi': '10.1002/14651858.CD006207.pub5',
                   'title': 'Physical interventions to interrupt or reduce the spread of respiratory viruses'},
}
# Probe -> measurement goals (A..H as defined in the TEST818 brief). Probes contain no answer, number or conclusion.
PROBES818 = [
    ('POSITIONS', 'A,B',
     'Describe separately what Source A and Source B conclude about N95 respirators compared with surgical or '
     'medical masks. For each conclusion, name the source, the outcome measured and the population or setting.'),
    ('OUTCOME_SPLIT', 'A,B,D',
     'Do the sources distinguish influenza-like illness from laboratory-confirmed influenza or other confirmed '
     'infection? Describe the reported findings for each outcome without treating different endpoints as identical.'),
    ('APPARENT_CONFLICT', 'C,D,E',
     'Do the two sources truly contradict each other on the same outcome, population and study design, or can '
     'differences in methods or included evidence explain any apparently different conclusions? State what cannot '
     'be established from the documents.'),
    ('EVIDENCE_LIMITS', 'E',
     'Identify the limitations and the missing information that would be needed to reconcile the sources. Do not '
     'claim that the absence of statistical significance proves equivalence.'),
    ('ABSENT_INFORMATION', 'F',
     'What unit price or cost per wearer do the sources report for N95 respirators compared with surgical masks?'),
    ('SYNTHESIS', 'C,G,H',
     'Write a reasoned synthesis of what the mounted evidence supports about N95 respirators versus surgical or '
     'medical masks for preventing respiratory viral infection. Label every statement with its source (A, B or '
     'A+B) and state the overall certainty.'),
]
READ_INSTRUCTION818 = ('Answer from the physically mounted scientific evidence only. Distinguish claims, observations '
                       'and uncertainty. Attribute each statement to Source A or Source B. Do not assume the documents '
                       'conflict. If a conclusion is unsupported, say UNKNOWN.\nQuestion: ')
NULL_TEXT818 = 'MEMORY CONTROL RECORD\nNo scientific document is stored in this memory record.\n'
# Six arms of TEST816/817 unchanged + one no-evidence memory control (same prompt, same generation path).
ARMS818 = [('A_ONLY', ['E818_A']), ('B_ONLY', ['E818_B']),
           ('ONE_CARTRIDGE_AB', ['E818_AB']), ('ONE_CARTRIDGE_BA', ['E818_BA']),
           ('TWO_CARTRIDGE_AB', ['E818_A', 'E818_B']), ('TWO_CARTRIDGE_BA', ['E818_B', 'E818_A']),
           ('NULL_MEMORY', ['E818_NULL'])]
MAX_NEW818 = 256
SOURCE_TOKEN_CAP818 = 2400            # per abstract; never truncated — a longer abstract stops the run.
                                      # Run 1 measured: A 276 tokens, B (Cochrane) 1,938 tokens; 2x2400+P stays < MAX_FUSED_TOKENS
VERSION_CONTAINMENT818 = 0.95         # word-set containment needed to call one abstract version a superset of the other
COMPARABILITY818 = ['research_question', 'population_and_setting', 'healthcare_workers_vs_community',
                    'n95_definition', 'surgical_or_medical_mask_definition', 'infection_types_and_outcomes',
                    'included_studies', 'rct_vs_observational', 'outcome_measures', 'effect_sizes_and_confidence_intervals',
                    'certainty_or_quality_of_evidence', 'statistical_uncertainty', 'publication_date_and_literature_window']
PANEL818 = {'papers': PAPERS818, 'expected': EXPECTED818, 'probes': PROBES818, 'instruction': READ_INSTRUCTION818,
            'null_text': NULL_TEXT818, 'arms': ARMS818, 'max_new': MAX_NEW818, 'scope': DATA818['source_scope']}
PANEL_SHA818 = sha818(json.dumps(PANEL818, ensure_ascii=False, sort_keys=True))
DATA818['panel'] = PANEL818
DATA818['panel_sha256'] = PANEL_SHA818
save818()


# ---------------------------------------------------------------------------------------------------------------------
# Network layer: host-locked, bounded retries, every failure classified and recorded (never logged as success)
# ---------------------------------------------------------------------------------------------------------------------
def source_event818(pmcid, channel, kind, **kw):
    ev = {'pmcid': pmcid, 'channel': channel, 'event': kind, 'utc': _dt818.datetime.now(_dt818.timezone.utc).isoformat()}
    ev.update(kw)
    DATA818['source_events'].append(ev)
    save818()
    say818('SOURCE_EVENT', pmcid, channel, kind, json.dumps(kw, ensure_ascii=False, default=str)[:600])


def fetch818(url, pmcid, channel, attempts, min_bytes, max_bytes, accept):
    """GET from Europe PMC only. Retries ONLY 408/429/5xx/timeouts, at most `attempts` times, with backoff that
    honours Retry-After (capped at 30 s). Raises Source818Error with an error class; never returns an error body."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != EPMC_HOST818:
        raise Source818Error('SOURCE_ACCESS', 'host not allowed ' + str(parsed.hostname))
    last = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'AKBASCORE-TEST818/2.0 (non-bulk academic research)',
                                                       'Accept': accept})
            with urllib.request.urlopen(req, timeout=60) as f:
                final_host = urllib.parse.urlparse(f.geturl()).hostname
                status = getattr(f, 'status', 200)
                ctype = f.headers.get('Content-Type', '')
                data = f.read(max_bytes + 1)
            if final_host != EPMC_HOST818:
                raise Source818Error('SOURCE_ACCESS', 'redirected to another host ' + str(final_host))
            if not (min_bytes <= len(data) <= max_bytes):
                raise Source818Error('SOURCE_SCHEMA', 'response size outside bounds',
                                     {'bytes': len(data), 'min': min_bytes, 'max': max_bytes, 'content_type': ctype,
                                      'head': data[:300].decode('utf-8', 'replace')})
            source_event818(pmcid, channel, 'HTTP_OK', attempt=attempt, status=status, bytes=len(data),
                            content_type=ctype, sha256=sha818(data))
            return data
        except urllib.error.HTTPError as exc:
            body = b''
            try:
                body = exc.read(600)
            except Exception:
                pass
            source_event818(pmcid, channel, 'HTTP_ERROR', attempt=attempt, status=exc.code,
                            body_head=body.decode('utf-8', 'replace')[:300])
            if exc.code in (408, 429, 500, 502, 503, 504):
                last = ('SOURCE_HTTP_429' if exc.code == 429 else 'SOURCE_HTTP_5XX' if exc.code >= 500
                        else 'SOURCE_TIMEOUT', exc.code)
                if attempt < attempts:
                    ra = exc.headers.get('Retry-After') if exc.headers else None
                    wait = min(30.0, float(ra)) if ra and ra.strip().isdigit() else min(30.0, 3.0 * 2 ** (attempt - 1))
                    time.sleep(wait)
                continue
            raise Source818Error('SOURCE_ACCESS', 'HTTP %d' % exc.code, {'status': exc.code})
        except (socket.timeout, TimeoutError) as exc:
            source_event818(pmcid, channel, 'TIMEOUT', attempt=attempt, error=repr(exc))
            last = ('SOURCE_TIMEOUT', None)
            if attempt < attempts:
                time.sleep(min(30.0, 3.0 * 2 ** (attempt - 1)))
        except urllib.error.URLError as exc:
            is_timeout = isinstance(getattr(exc, 'reason', None), (socket.timeout, TimeoutError))
            source_event818(pmcid, channel, 'NETWORK_ERROR', attempt=attempt, error=repr(exc))
            last = ('SOURCE_TIMEOUT' if is_timeout else 'SOURCE_ACCESS', None)
            if attempt < attempts:
                time.sleep(min(30.0, 3.0 * 2 ** (attempt - 1)))
    cls, code = last if last else ('SOURCE_ACCESS', None)
    raise Source818Error(cls, 'retries exhausted (%d attempts)' % attempts, {'last_status': code})


def normtitle818(s):
    import unicodedata
    s = unicodedata.normalize('NFKC', s or '').casefold()
    return ' '.join(re.sub(r'[^a-z0-9]+', ' ', s).split())


def normdoi818(s):
    s = (s or '').strip().casefold()
    for p in ('https://doi.org/', 'http://doi.org/', 'https://dx.doi.org/', 'doi:'):
        if s.startswith(p):
            s = s[len(p):]
    return s.strip()


def normpmcid818(s):
    s = (s or '').strip().upper()
    return 'PMC' + s.removeprefix('PMC') if s else ''


def strip_markup818(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return ' '.join(_html818.unescape(s).split())


def epmc_metadata818(pmcid):
    """Europe PMC REST search, resultType=core. The record of a PMC article that also has a PubMed ID is indexed
    as SRC:MED with EXT_ID=<PMID>; its PMCID is a separate field. Therefore the query is PMCID:<id> (and, if that
    returns nothing, the identity-equivalent DOI:"<doi>"). Exactly one record must carry the locked PMCID AND DOI."""
    exp = EXPECTED818[pmcid]
    queries = [('PMCID', 'PMCID:' + pmcid), ('DOI', 'DOI:"' + exp['doi'] + '"')]
    for qname, query in queries:
        url = EPMC_REST818 + 'search?' + urllib.parse.urlencode(
            {'query': query, 'resultType': 'core', 'format': 'json', 'pageSize': 25})
        raw = fetch818(url, pmcid, 'METADATA_' + qname, attempts=4, min_bytes=20, max_bytes=3_000_000,
                       accept='application/json')
        try:
            obj = json.loads(raw.decode('utf-8'))
        except Exception as exc:
            raise Source818Error('SOURCE_SCHEMA', 'metadata is not JSON', {'head': raw[:300].decode('utf-8', 'replace')})
        if not isinstance(obj, dict) or 'resultList' not in obj or not isinstance(obj.get('resultList', {}).get('result'), list):
            raise Source818Error('SOURCE_SCHEMA', 'unexpected metadata schema',
                                 {'keys': sorted(obj)[:20] if isinstance(obj, dict) else type(obj).__name__,
                                  'head': raw[:300].decode('utf-8', 'replace')})
        hits = obj.get('hitCount')
        records = obj['resultList']['result']
        if not isinstance(hits, int):
            raise Source818Error('SOURCE_SCHEMA', 'hitCount missing or not an integer', {'hitCount': hits})
        if hits == 0 or not records:
            source_event818(pmcid, 'METADATA_' + qname, 'EMPTY_RESULT', hitCount=hits, bytes=len(raw),
                            response=raw[:400].decode('utf-8', 'replace'))
            continue
        matches = [r for r in records if normpmcid818(r.get('pmcid')) == pmcid and normdoi818(r.get('doi')) == exp['doi'].casefold()]
        source_event818(pmcid, 'METADATA_' + qname, 'RESULTS', hitCount=hits, returned=len(records),
                        exact_pmcid_and_doi=len(matches),
                        indexed_as=[{'id': r.get('id'), 'source': r.get('source'), 'pmid': r.get('pmid'),
                                     'pmcid': r.get('pmcid'), 'doi': r.get('doi')} for r in records[:5]])
        if len(matches) != 1:
            raise Source818Error('ARTICLE_ID_MISMATCH', 'no unique record with the locked PMCID and DOI',
                                 {'query': query, 'returned': len(records), 'matched': len(matches)})
        return matches[0], raw, query
    raise Source818Error('SOURCE_EMPTY_RESULT', 'Europe PMC returned no record for the locked identifiers',
                         {'queries': [q for _, q in queries]})


def jats_crosscheck818(pmcid):
    """Optional independent channel: Europe PMC fullTextXML. Any HTTP failure is recorded and classified, never
    treated as success; it is not fatal because the protocol does not use full text. A JATS document that IS served
    must match the locked identity, otherwise the run stops (a wrong article must never be accepted)."""
    url = EPMC_REST818 + pmcid + '/fullTextXML'
    try:
        raw = fetch818(url, pmcid, 'JATS', attempts=3, min_bytes=500, max_bytes=5_000_000,
                       accept='application/xml, text/xml;q=0.9')
    except Source818Error as exc:
        return {'status': 'UNAVAILABLE', 'error_class': exc.error_class, 'detail': exc.detail, 'url': url}
    import xml.etree.ElementTree as _ET818
    try:
        root = _ET818.fromstring(raw)
    except Exception as exc:
        return {'status': 'UNAVAILABLE', 'error_class': 'SOURCE_SCHEMA', 'detail': {'xml_error': repr(exc)}, 'url': url}
    meta = next((x for x in root.iter() if localname815(x) == 'article-meta'), None)
    if localname815(root) != 'article' or meta is None:
        return {'status': 'UNAVAILABLE', 'error_class': 'SOURCE_SCHEMA', 'url': url,
                'detail': {'root': localname815(root), 'article_meta': meta is not None}}
    say818('PASS JATS_SCHEMA_' + pmcid, {'root': 'article', 'bytes': len(raw)})
    ids = {}
    for el in meta.iter():
        if localname815(el) == 'article-id':
            k = el.attrib.get('pub-id-type', '').lower()
            v = (el.text or '').strip()
            if k and v:
                ids.setdefault(k, []).append(v)
    pmc_vals = sorted(set(normpmcid818(v) for k, vs in ids.items() if k in ('pmc', 'pmcid') for v in vs))
    doi_vals = sorted(set(normdoi818(v) for v in ids.get('doi', []) if v.strip()))
    pmid_vals = sorted(set(v.strip() for v in ids.get('pmid', []) if v.strip()))
    gate818('JATS_PMCID_IF_PRESENT_' + pmcid, not pmc_vals or pmc_vals == [pmcid], pmc_vals, 'ARTICLE_ID_MISMATCH')
    # Repeated identical DOI elements are one identity; distinct DOI values are a mismatch.
    gate818('JATS_UNIQUE_DOI_' + pmcid, doi_vals == [EXPECTED818[pmcid]['doi'].casefold()],
            {'raw_values': ids.get('doi', []), 'unique_values': doi_vals}, 'DOI_MISMATCH')
    title = first_text815(meta, 'article-title')
    gate818('JATS_TITLE_' + pmcid, normtitle818(title) == normtitle818(EXPECTED818[pmcid]['title']), title, 'ARTICLE_ID_MISMATCH')
    abstracts = [x for x in meta.iter() if localname815(x) == 'abstract' and not x.attrib.get('abstract-type')]
    abstract = ' '.join(' '.join(abstracts[0].itertext()).split()) if abstracts else ''
    full = text_from815(root)
    (DIR818 / (pmcid + '_fullText.xml')).write_bytes(raw)
    return {'status': 'AVAILABLE', 'url': url, 'xml_sha256': sha818(raw), 'xml_bytes': len(raw), 'pmid_values': pmid_vals,
            'doi_values_raw': ids.get('doi', []), 'untyped_abstracts': len(abstracts), 'abstract': abstract,
            'body_chars': len(full)}


def words818(s):
    return set(re.findall(r'[a-z0-9]+', (s or '').casefold()))


def acquire818(pmcid):
    exp = EXPECTED818[pmcid]
    rec, raw, query = epmc_metadata818(pmcid)
    (DIR818 / (pmcid + '_europepmc_core.json')).write_bytes(raw)
    gate818('META_PMCID_' + pmcid, normpmcid818(rec.get('pmcid')) == pmcid, rec.get('pmcid'), 'ARTICLE_ID_MISMATCH')
    gate818('META_DOI_' + pmcid, normdoi818(rec.get('doi')) == exp['doi'].casefold(), rec.get('doi'), 'DOI_MISMATCH')
    gate818('META_TITLE_' + pmcid, normtitle818(rec.get('title')) == normtitle818(exp['title']), rec.get('title'),
            'ARTICLE_ID_MISMATCH')
    pmid = str(rec.get('pmid') or '').strip()
    gate818('META_PMID_PRESENT_' + pmcid, pmid.isdigit(), {'pmid': pmid, 'source': rec.get('source'), 'id': rec.get('id')},
            'ARTICLE_ID_MISMATCH')
    abstract = strip_markup818(rec.get('abstractText') or '')
    source_format = 'EUROPEPMC_CORE_ABSTRACT'
    (DIR818 / (pmcid + '_abstract_metadata_version.txt')).write_text(abstract, encoding='utf-8')
    jats = jats_crosscheck818(pmcid)
    if jats['status'] == 'AVAILABLE':
        gate818('JATS_PMID_CONSISTENT_' + pmcid, not jats['pmid_values'] or jats['pmid_values'] == [pmid],
                {'jats': jats['pmid_values'], 'metadata': pmid}, 'ARTICLE_ID_MISMATCH')
        ja = jats.pop('abstract', '')
        (DIR818 / (pmcid + '_abstract_jats_version.txt')).write_text(ja, encoding='utf-8')
        if ja:
            # Two versions of the same abstract: never ignore a difference silently. Use the version that contains the
            # other (word-set containment); if neither contains the other, the content conflict stops the run.
            wm, wj = words818(abstract), words818(ja)
            m_in_j = len(wm & wj) / max(1, len(wm))
            j_in_m = len(wm & wj) / max(1, len(wj))
            jats.update(abstract_chars=len(ja), abstract_sha256=sha818(ja), metadata_words_in_jats=round(m_in_j, 4),
                        jats_words_in_metadata=round(j_in_m, 4),
                        word_jaccard=round(len(wm & wj) / max(1, len(wm | wj)), 4))
            if m_in_j >= VERSION_CONTAINMENT818 and j_in_m >= VERSION_CONTAINMENT818:
                decision = 'EQUIVALENT_USE_METADATA'
            elif m_in_j >= VERSION_CONTAINMENT818:
                decision = 'JATS_IS_SUPERSET_USE_JATS'
                abstract, source_format = ja, 'EUROPEPMC_JATS_ABSTRACT'
            elif j_in_m >= VERSION_CONTAINMENT818:
                decision = 'METADATA_IS_SUPERSET_USE_METADATA'
            else:
                decision = 'CONFLICTING_VERSIONS'
            jats['version_decision'] = decision
            source_event818(pmcid, 'VERSION_COMPARE', decision, metadata_chars=len(strip_markup818(rec.get('abstractText') or '')),
                            jats_chars=len(ja), metadata_words_in_jats=round(m_in_j, 4), jats_words_in_metadata=round(j_in_m, 4))
            gate818('ABSTRACT_VERSIONS_RECONCILED_' + pmcid, decision != 'CONFLICTING_VERSIONS',
                    {'decision': decision, 'metadata_words_in_jats': round(m_in_j, 4), 'jats_words_in_metadata': round(j_in_m, 4)},
                    'SOURCE_CONTENT_INTEGRITY')
    else:
        source_event818(pmcid, 'JATS', 'FULL_TEXT_NOT_SERVED', error_class=jats['error_class'], detail=jats['detail'],
                        consequence='not required by SOURCE_SCOPE; identity verified from the metadata record')
    gate818('ABSTRACT_PRESENT_' + pmcid, len(abstract) >= 600, len(abstract), 'MISSING_SOURCE_CONTENT')
    gate818('ABSTRACT_TOPIC_N95_' + pmcid, 'n95' in abstract.casefold(), {'chars': len(abstract)}, 'SOURCE_CONTENT_INTEGRITY')
    (DIR818 / (pmcid + '_abstract.txt')).write_text(abstract, encoding='utf-8')
    journal = ((rec.get('journalInfo') or {}).get('journal') or {}).get('title')
    meta = {'label': LABEL818[pmcid], 'pmcid': pmcid, 'pmid': pmid, 'doi': exp['doi'], 'title': rec.get('title'),
            'journal': journal, 'pub_year': rec.get('pubYear'),
            'first_publication_date': rec.get('firstPublicationDate'),
            'pub_types': ((rec.get('pubTypeList') or {}).get('pubType')),
            'europepmc_record': {'id': rec.get('id'), 'source': rec.get('source'), 'query': query,
                                 'is_open_access': rec.get('isOpenAccess'), 'in_pmc': rec.get('inPMC'),
                                 'in_epmc': rec.get('inEPMC'), 'license': rec.get('license')},
            'access_url': EPMC_REST818 + 'search?' + urllib.parse.urlencode({'query': query, 'resultType': 'core', 'format': 'json'}),
            'source_format': source_format, 'content_kind': 'ABSTRACT',
            'abstract_chars': len(abstract), 'abstract_sha256': sha818(abstract), 'metadata_sha256': sha818(raw),
            'jats_crosscheck': jats, 'verification': 'PMCID+DOI+TITLE LOCKED; PMID PRESENT AND CONSISTENT'}
    return abstract, meta


# ---------------------------------------------------------------------------------------------------------------------
# Offline evaluator (never visible to the model): number provenance and UNKNOWN markers — diagnostics, not truth
# ---------------------------------------------------------------------------------------------------------------------
NOISE818 = [r'\bN\s?95\b', r'\bP[23]\b', r'\bFFP[123]\b', r'\bKN95\b', r'95\s*%\s*(?:CI|confidence)', r'COVID[- ]?19',
            r'SARS[- ]?CoV[- ]?\d', r'MERS[- ]?CoV', r'\bH\d+N\d+\b', r'\bCD\d{6}\b', r'10\.\d{4,9}/\S+', r'\bPMC\d+\b',
            r'\b(?:Source|SOURCE)\s+[AB]\b']


def numbers818(s):
    t = s or ''
    t = re.sub(r'(?m)^\s*\d+[.)]\s', ' ', t)                      # list markers
    for rx in NOISE818:
        t = re.sub(rx, ' ', t, flags=re.I)
    out = set()
    for m in re.finditer(r'(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?![\w])', t):
        v = m.group(1).replace(',', '')
        try:
            x = float(v)
        except ValueError:
            continue
        out.add(('%.4f' % x).rstrip('0').rstrip('.'))
    return out


def provenance818(answer, numsA, numsB):
    n = numbers818(answer)
    return {'numbers': sorted(n), 'in_A_only': sorted(n & (numsA - numsB)), 'in_B_only': sorted(n & (numsB - numsA)),
            'in_both': sorted(n & numsA & numsB), 'in_neither': sorted(n - numsA - numsB)}


def shingles818(s, k=8):
    w = re.findall(r'[a-z0-9]+', (s or '').casefold())
    return set(tuple(w[i:i + k]) for i in range(max(0, len(w) - k + 1)))


# ---------------------------------------------------------------------------------------------------------------------
# Error classification for the final record
# ---------------------------------------------------------------------------------------------------------------------
def classify818(exc):
    if isinstance(exc, (Gate818Error, Source818Error)):
        return exc.error_class
    name, msg = type(exc).__name__, str(exc)
    if name == 'OutOfMemoryError' or 'CUDA out of memory' in msg:
        return 'CUDA_OOM'
    if 'GPU_SAFETY_STOP' in msg:
        return 'CUDA_MEMORY_RESERVE'
    if any(k in msg for k in ('TEST815_NO_CUDA', 'TEST815_EXPECTS_ONE_GPU', 'TEST815_A100_80GB_REQUIRED',
                              'TEST815_INSUFFICIENT_FREE_VRAM', 'ONE_CUDA_GPU_REQUIRED', 'A100_80GB_REQUIRED',
                              'TEST815_REQUIRES_TORCH')):
        return 'GPU_HARDWARE'
    if 'FAIL_CLOSED' in msg or 'TEST815_SOURCE_LOCK' in msg or 'GIT_LOCK' in msg or 'AST_BOUNDARY' in msg:
        return 'LOCKED_SOURCE'
    if 'FILE_SHA_' in msg or 'CARTRIDGE_TENSOR_SHA_' in msg or 'PHYSICAL_SHA_' in msg or 'PRIOR_MEMORY_CHANGED' in msg:
        return 'SHA_MISMATCH'
    if 'SHAPE' in msg or 'CARTRIDGE_ID_' in msg or 'NATIVE_INIT_80' in msg:
        return 'TENSOR_SHAPE_OR_IDENTITY'
    if 'CHECK_FAILED:MODEL_ARCH' in msg or 'CHECK_FAILED:FROZEN' in msg or 'CHECK_FAILED:NF4' in msg:
        return 'MODEL_LOAD'
    if isinstance(exc, urllib.error.URLError) or isinstance(exc, (socket.timeout, TimeoutError)):
        return 'SOURCE_ACCESS'
    return {'LOCKED_SOURCE': 'LOCKED_SOURCE', 'SOURCES': 'SOURCE_ACCESS', 'LOCKED_ENGINE': 'LOCKED_ENGINE', 'TOKENIZER': 'MODEL_LOAD',
            'MODEL_LOAD': 'MODEL_LOAD', 'CARTRIDGE_FORGE': 'CARTRIDGE_PRODUCTION', 'CARTRIDGE_VERIFY': 'SHA_MISMATCH',
            'NATIVE_READ': 'NATIVE_READ', 'EVALUATION': 'EVALUATION'}.get(STAGE818['now'], 'UNCLASSIFIED')


# =====================================================================================================================
try:
    # 1 · Locked TEST815 source. Parsing helpers are taken verbatim from it BEFORE any GPU work, so that both
    #     papers are verified before the 72B model (≈145 GB) is downloaded or loaded.
    stage818('LOCKED_SOURCE')
    req = urllib.request.Request(REPO818 + 'main/815.py', headers={'User-Agent': 'AKBASCORE-TEST818'})
    with urllib.request.urlopen(req, timeout=180) as f:
        raw815_818 = f.read(120001)
    gate818('LOCKED_815_SOURCE', len(raw815_818) <= 120000 and gitblob818(raw815_818) == LOCK815_818,
            gitblob818(raw815_818), 'LOCKED_SOURCE')
    tree815_818 = ast.parse(raw815_818.decode('utf-8'), filename='815.py')
    try_idx818 = [i for i, n in enumerate(tree815_818.body) if isinstance(n, ast.Try)]
    gate818('TEST815_AST_BOUNDARY', len(try_idx818) == 1 and try_idx818[0] == len(tree815_818.body) - 1,
            try_idx818, 'LOCKED_SOURCE')
    helpers818 = {n.name: n for n in tree815_818.body
                  if isinstance(n, ast.FunctionDef) and n.name in ('localname815', 'first_text815', 'text_from815')}
    gate818('VERBATIM_PARSE_HELPERS', set(helpers818) == {'localname815', 'first_text815', 'text_from815'},
            sorted(helpers818), 'LOCKED_SOURCE')
    exec(compile(ast.fix_missing_locations(ast.Module(body=[helpers818[k] for k in
         ('localname815', 'first_text815', 'text_from815')], type_ignores=[])), 'TEST815_PARSE_HELPERS', 'exec'), globals())

    # 2 · Sources (network only, no GPU). Any failure stops here with its class.
    stage818('SOURCES')
    texts818, docs818 = {}, {}
    for pmcid in PAPERS818:
        try:
            body, meta = acquire818(pmcid)
        except Source818Error as exc:
            DATA818['source_failure'] = {'pmcid': pmcid, 'error_class': exc.error_class, 'message': str(exc),
                                         'detail': exc.detail}
            save818()
            say818('SOURCE_FAILED', pmcid, exc.error_class, str(exc), json.dumps(exc.detail, default=str)[:600])
            raise
        texts818[pmcid], docs818[pmcid] = body, meta
        DATA818['sources'].append(meta)
        save818()
        say818('TEST818_VERIFIED_SOURCE', meta['label'], pmcid, 'PMID', meta['pmid'], meta['doi'], '|', meta['title'],
               '|', meta['journal'], meta['pub_year'], '| abstract chars', meta['abstract_chars'],
               '| JATS', meta['jats_crosscheck']['status'])
    gate818('TWO_VERIFIED_SOURCES', set(docs818) == set(PAPERS818), sorted(docs818), 'SOURCE_ACCESS')
    gate818('DISTINCT_SOURCES', len({d['doi'] for d in docs818.values()}) == 2 and
            len({d['pmid'] for d in docs818.values()}) == 2, None, 'ARTICLE_ID_MISMATCH')
    # Read-time inputs are fixed now and checked against the source texts before any GPU work.
    shA818, shB818 = shingles818(texts818[PAPERS818[0]], 12), shingles818(texts818[PAPERS818[1]], 12)
    idents818 = [normtitle818(d[k]) for d in docs818.values() for k in ('doi', 'pmcid', 'pmid', 'title')]
    PROMPTS818 = {pid: READ_INSTRUCTION818 + q for pid, goals, q in PROBES818}
    for pid, prompt in PROMPTS818.items():
        np_ = normtitle818(prompt)
        gate818('PROMPT_HAS_NO_SOURCE_TEXT_' + pid,
                not (shingles818(prompt, 12) & (shA818 | shB818)) and not any(x and x in np_ for x in idents818),
                {'prompt_sha256': sha818(prompt), 'prompt_chars': len(prompt)}, 'EXPERIMENT_GATE')
    gate818('NULL_CONTROL_HAS_NO_SOURCE_TEXT',
            not (shingles818(NULL_TEXT818, 6) & (shingles818(texts818[PAPERS818[0]], 6) |
                                                 shingles818(texts818[PAPERS818[1]], 6))), None, 'EXPERIMENT_GATE')
    numsA818 = numbers818(texts818[PAPERS818[0]])
    numsB818 = numbers818(texts818[PAPERS818[1]])
    OFFLINE818.write_text(json.dumps({'note': 'Offline evaluator inputs. Never passed to the model.',
        'numbers_A': sorted(numsA818), 'numbers_B': sorted(numsB818),
        'abstract_sha256': {p: docs818[p]['abstract_sha256'] for p in PAPERS818}}, indent=2), encoding='utf-8')
    DATA818['offline_evaluator_sha256'] = sha818(OFFLINE818.read_bytes())
    save818()

    # 3 · Locked TEST815 prelude, unchanged (GPU preflight, 790→789→788→787→785→779 chain, native engine symbols).
    stage818('LOCKED_ENGINE')
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_818.body[:try_idx818[0]], type_ignores=[])),
                 'LOCKED_TEST815_DEFINITIONS', 'exec'), globals())
    gate818('NATIVE_SYMBOLS', all(callable(globals().get(k)) for k in
            ('model_setup', 'physical_commit', 'build_fusion', 'free_generate', 'safe_load', 'memory_seals',
             'compare_seals', 'sentinel', 'release')), None, 'LOCKED_SOURCE')
    gate818('FRESH_MEMORY_BANK', len(entries) == 0, len(entries), 'CARTRIDGE_PRODUCTION')
    import torch as _torch818
    SDPA_ORIG818 = _torch818.nn.functional.scaled_dot_product_attention

    # 4 · Tokenizer-only budget check before the 72B weights are touched.
    stage818('TOKENIZER')
    tok818 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    labeled818 = {}
    for pmcid in PAPERS818:
        lab, meta = LABEL818[pmcid], docs818[pmcid]
        ntok = len(tok818.encode(texts818[pmcid], add_special_tokens=False))
        gate818('SOURCE_TOKENS_' + lab, 0 < ntok <= SOURCE_TOKEN_CAP818, {'tokens': ntok, 'cap': SOURCE_TOKEN_CAP818},
                'SOURCE_TOKEN_BUDGET')
        meta['abstract_tokens'] = ntok
        meta['stored_untruncated'] = True
        labeled818[lab] = ('SOURCE ' + lab + '\nScientific article: ' + meta['title'] + '\nJournal: ' +
                           str(meta['journal']) + ' (' + str(meta['pub_year']) + ')\nDOI: ' + meta['doi'] +
                           '\nPMCID: ' + pmcid + '\nPMID: ' + meta['pmid'] +
                           '\nPublished abstract (complete, verified):\n' + texts818[pmcid] + '\n')
    CARTS818 = {'E818_A': labeled818['A'], 'E818_B': labeled818['B'],
                'E818_AB': labeled818['A'] + '\n' + labeled818['B'], 'E818_BA': labeled818['B'] + '\n' + labeled818['A'],
                'E818_NULL': NULL_TEXT818}
    LINEAGE818 = {'E818_A': ['A'], 'E818_B': ['B'], 'E818_AB': ['A', 'B'], 'E818_BA': ['B', 'A'], 'E818_NULL': []}
    ntoks818 = {cid: len(tok818.encode(b, add_special_tokens=False)) for cid, b in CARTS818.items()}
    for cid in CARTS818:
        gate818('CARTRIDGE_TOKENS_' + cid, 4 < ntoks818[cid] <= 3300, ntoks818[cid], 'CARTRIDGE_PRODUCTION')
    # build_fusion silently skips a cartridge that would exceed MAX_FUSED_TOKENS; refuse that case up front.
    gate818('FUSION_BUDGET_TWO_CARTRIDGE', 30 + ntoks818['E818_A'] + ntoks818['E818_B'] + 64 <= MAX_FUSED_TOKENS,
            {'A': ntoks818['E818_A'], 'B': ntoks818['E818_B'], 'max': MAX_FUSED_TOKENS}, 'CARTRIDGE_PRODUCTION')
    del tok818

    # 5 · Frozen model (locked model_setup), weight sentinel.
    stage818('MODEL_LOAD')
    model_setup()
    before818 = sentinel()
    gate818('PREFIX_LENGTH', P == 30, P, 'MODEL_LOAD')

    # 6 · Physical cartridges: forge → atomic write → SHA → manifest (locked physical_commit), then sealed reload.
    stage818('CARTRIDGE_FORGE')
    for cid, body in CARTS818.items():
        physical_commit(cid, body)
        gate818('BODY_SHA_IN_MANIFEST_' + cid, entries[cid].get('body_sha256') == sha818(body), None, 'SHA_MISMATCH')
    gate818('FIVE_PHYSICAL_CARTRIDGES', all(cid in entries for cid in CARTS818) and len(entries) == 5,
            sorted(entries), 'CARTRIDGE_PRODUCTION')
    stage818('CARTRIDGE_VERIFY')
    for cid in CARTS818:
        cp = safe_load(entries[cid])                         # FILE_SHA, CARTRIDGE_ID, CARTRIDGE_TENSOR_SHA (locked)
        n = int(cp['n'])
        layout = (tuple(cp['h'].shape) == (1, n, H) and cp['h'].dtype == DTYPE and cp['h'].device.type == 'cpu'
                  and len(cp['lower']) == CUT + 1 and
                  all(tuple(k.shape) == (1, KVH, n, HD) and tuple(v.shape) == (1, KVH, n, HD) and
                      k.dtype == DTYPE and v.dtype == DTYPE and
                      k.device.type == 'cpu' and v.device.type == 'cpu' for k, v in cp['lower']))
        gate818('SEALED_RELOAD_LAYOUT_' + cid, cp['book_id'] == cid and layout,
                {'n': n, 'h': list(cp['h'].shape), 'h_dtype': str(cp['h'].dtype), 'lower_layers': len(cp['lower']),
                 'k0': list(cp['lower'][0][0].shape)}, 'TENSOR_SHAPE_OR_IDENTITY')
        e = entries[cid]
        DATA818['cartridges'].append({
            'id': cid, 'lineage_sources': [{'label': l, 'pmcid': PAPERS818[0 if l == 'A' else 1],
                                            'doi': docs818[PAPERS818[0 if l == 'A' else 1]]['doi'],
                                            'abstract_sha256': docs818[PAPERS818[0 if l == 'A' else 1]]['abstract_sha256']}
                                           for l in LINEAGE818[cid]],
            'path': str(CART_DIR / e['file']), 'body_sha256': e.get('body_sha256'), 'cartridge_file_sha256': e['sha256'],
            'tensor_sha': e['tensor_sha'], 'n': e['n'], 'p': e['p'], 'body_tokens': e['body_tokens'],
            'cut': 'CUT%d: H%d residual (1,n,%d) + K/V of blocks 0..%d' % (CUT, CUT, H, CUT),
            'save_reload_verified': True})
        del cp
    save818()
    release()

    # 7 · Native reads: 7 arms × 6 locked probes = 42. Memory path recorded per read.
    stage818('NATIVE_READ')
    def read818(arm, ids, pid, question):
        tag = arm + '_' + pid
        prompt = READ_INSTRUCTION818 + question
        gate818('PROMPT_IS_PRECHECKED_' + tag, prompt == PROMPTS818[pid], sha818(prompt), 'EXPERIMENT_GATE')
        t0 = time.perf_counter()
        mem, active, steps, _ = build_fusion(ids, 'TEST818_' + tag, True)
        try:
            gate818('NATIVE80_' + tag, len(mem) == NL and list(active) == ids, None, 'NATIVE_READ')
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[c]['body_tokens']) for c in ids)
            gate818('NATIVE_LENGTH_' + tag, n == expected, {'observed': n, 'expected': expected}, 'NATIVE_READ')
            gate818('MEMORY_ON_GPU_' + tag, all(k.is_cuda and v.is_cuda for k, v in mem), None, 'NATIVE_READ')
            prior = memory_seals(mem)
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else {'B0': (P, n), 'B1': (n, n)}
            o = free_generate(mem, prompt, seed=None, gain=0., max_new=MAX_NEW818, spans=spans)
            gate818('KV_SEAL_' + tag, compare_seals(prior, memory_seals(mem)), None, 'SHA_MISMATCH')
            gate818('SDPA_RESTORED_' + tag, _torch818.nn.functional.scaled_dot_product_attention is SDPA_ORIG818,
                    None, 'NATIVE_READ')
            raw = o['raw']
            return {'arm': arm, 'probe': pid, 'goals': dict((p[0], p[1]) for p in PROBES818)[pid], 'ids': list(ids),
                    'raw': raw, 'generated_tokens': int(o['generated_tokens']),
                    'possibly_truncated': int(o['generated_tokens']) >= MAX_NEW818, 'sdpa_calls': o['sdpa_calls'],
                    'read_seconds': round(time.perf_counter() - t0, 3), 'fusion_steps': steps,
                    'memory_path': {'mode': 'NATIVE_CUT3_PHYSICAL_SSD_CARTRIDGES', 'cartridges': list(ids),
                                    'cartridge_file_sha256': [entries[c]['sha256'] for c in ids],
                                    'memory_tokens': n, 'prompt_sha256': sha818(prompt),
                                    'source_text_in_prompt': False, 'external_retrieval': False,
                                    'reference_answer_in_prompt': False},
                    'diagnostics': {'number_provenance': provenance818(raw, numsA818, numsB818),
                                    'starts_unknown': raw.strip().upper().startswith('UNKNOWN'),
                                    'contains_unknown': 'UNKNOWN' in raw.upper()}}
        finally:
            del mem
            gc.collect()
            release()

    for arm, ids in ARMS818:
        for pid, goals, q in PROBES818:
            row = read818(arm, ids, pid, q)
            DATA818['reads'].append(row)
            save818()
            d = row['diagnostics']['number_provenance']
            say818('TEST818_READ', arm, pid, 'tokens', row['generated_tokens'], 'seconds', row['read_seconds'],
                   '| numbers A-only', d['in_A_only'], 'B-only', d['in_B_only'], 'both', d['in_both'],
                   'neither', d['in_neither'], '|', repr(row['raw']))
    gate818('READ_MATRIX_42', len(DATA818['reads']) == len(ARMS818) * len(PROBES818) == 42, len(DATA818['reads']),
            'NATIVE_READ')

    # 8 · Integrity after the experiment.
    stage818('EVALUATION')
    gate818('FROZEN_WEIGHT_SENTINEL', before818 == sentinel(), None, 'MODEL_LOAD')
    gate818('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks,
            None, 'NATIVE_READ')
    gate818('PANEL_UNCHANGED', sha818(json.dumps(PANEL818, ensure_ascii=False, sort_keys=True)) == PANEL_SHA818,
            None, 'EXPERIMENT_GATE')
    for cid in CARTS818:                                     # cartridges unchanged on SSD after all reads
        gate818('FINAL_FILE_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'], None,
                'SHA_MISMATCH')

    # Automatic diagnostics (not truth): cross-source number leakage and abstention markers per arm.
    summary = {}
    for arm, ids in ARMS818:
        rows = [r for r in DATA818['reads'] if r['arm'] == arm]
        prov = [r['diagnostics']['number_provenance'] for r in rows]
        summary[arm] = {'reads': len(rows), 'truncated': sum(r['possibly_truncated'] for r in rows),
                        'answers_starting_UNKNOWN': sum(r['diagnostics']['starts_unknown'] for r in rows),
                        'numbers_total': sum(len(p['numbers']) for p in prov),
                        'numbers_only_in_A': sum(len(p['in_A_only']) for p in prov),
                        'numbers_only_in_B': sum(len(p['in_B_only']) for p in prov),
                        'numbers_in_both': sum(len(p['in_both']) for p in prov),
                        'numbers_in_neither_source': sum(len(p['in_neither']) for p in prov)}
    summary['interpretation'] = ('Numbers found only in B while only A is mounted (and vice versa), or any source '
                                 'number under NULL_MEMORY, indicate content not supplied by the mounted memory '
                                 '(e.g. parametric recall). Numbers in neither source are unsupported by both abstracts. '
                                 'These are diagnostics for the human reviewer, not correctness scores.')
    DATA818['automatic_diagnostics'] = summary
    say818('TEST818_DIAGNOSTICS', json.dumps(summary, ensure_ascii=False))

    cols = ['arm', 'probe', 'measurement_goals', 'cartridges', 'answer', 'possibly_truncated',
            'auto_numbers_only_in_A', 'auto_numbers_only_in_B', 'auto_numbers_in_neither',
            'human_single_source_fact_correct_0_1', 'human_source_attribution_correct_0_1',
            'human_common_findings_correct_0_1', 'human_difference_or_conflict_assessment_correct_0_1',
            'human_evidence_limits_recognised_0_1', 'human_abstention_appropriate_0_1',
            'human_synthesis_reasoned_0_1', 'human_synthesis_traceable_to_sources_0_1',
            'human_unsupported_claim_present_0_1', 'reviewer_notes', 'reviewer_identity', 'review_date']
    with REVIEW818.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in DATA818['reads']:
            p = r['diagnostics']['number_provenance']
            w.writerow({'arm': r['arm'], 'probe': r['probe'], 'measurement_goals': r['goals'],
                        'cartridges': '|'.join(r['ids']), 'answer': r['raw'], 'possibly_truncated': r['possibly_truncated'],
                        'auto_numbers_only_in_A': ' '.join(p['in_A_only']), 'auto_numbers_only_in_B': ' '.join(p['in_B_only']),
                        'auto_numbers_in_neither': ' '.join(p['in_neither'])})
    with COMPARE818.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['attribute', 'source_A_as_stated_in_abstract', 'source_B_as_stated_in_abstract',
                                          'same_for_both_0_1', 'difference_can_explain_divergent_conclusions_0_1',
                                          'reviewer_notes'])
        w.writeheader()
        for a in COMPARABILITY818:
            row = {'attribute': a}
            if a == 'publication_date_and_literature_window':
                row['source_A_as_stated_in_abstract'] = '%s · %s · %s' % (docs818[PAPERS818[0]]['journal'],
                    docs818[PAPERS818[0]]['first_publication_date'], docs818[PAPERS818[0]]['pub_types'])
                row['source_B_as_stated_in_abstract'] = '%s · %s · %s' % (docs818[PAPERS818[1]]['journal'],
                    docs818[PAPERS818[1]]['first_publication_date'], docs818[PAPERS818[1]]['pub_types'])
            w.writerow(row)
    DATA818['review_csv'] = {'path': str(REVIEW818), 'sha256': sha818(REVIEW818.read_bytes())}
    DATA818['comparability_csv'] = {'path': str(COMPARE818), 'sha256': sha818(COMPARE818.read_bytes())}
    DATA818['technical_completion'] = {
        'sources_verified': 2, 'physical_cartridges': len(DATA818['cartridges']), 'native_reads': len(DATA818['reads']),
        'gates_passed': sum(c['pass'] for c in DATA818['checks']), 'gates_failed': sum(not c['pass'] for c in DATA818['checks'])}
    DATA818['scientific_assessment'] = {'semantic_scoring_complete': False, 'conflict_verified': False,
                                        'synthesis_correctness_verified': False,
                                        'note': 'Technical completion is reported separately from scientific correctness.'}
    DATA818['status'] = 'COMPLETE_MECHANICAL_HUMAN_REVIEW_PENDING'
    save818()
    say818('TEST818_COMPLETED', json.dumps(DATA818['technical_completion']), OUT818, REVIEW818, COMPARE818)
except BaseException as exc:
    cls = classify818(exc)
    DATA818['status'] = 'ERROR'
    DATA818['error'] = {'class': cls, 'stage': STAGE818['now'], 'repr': repr(exc),
                        'detail': getattr(exc, 'detail', None), 'traceback': traceback.format_exc()}
    save818()
    say818('TEST818_FAILED', 'class=' + cls, 'stage=' + STAGE818['now'], repr(exc))
    say818(traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save818()
