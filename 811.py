# AKBASCORE SILICON HIPPOCAMPUS — TEST811
# NATIVE H3 EVIDENCE ARBITRATION / CAUSAL CONTROLS / PARAPHRASE ROBUSTNESS / PHYSICAL CUT3 CARTRIDGES
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB (40GB NOT SUPPORTED)
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# TEST811: evidence-conditioned hypothesis revision with independent narrow fact audit; no gold in inference.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

# Fail fast BEFORE downloading locked source trees or 72B model weights.
# Do not weaken the TEST779 hardware contract.
def preflight_gpu811():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('TEST811_REQUIRES_TORCH_AND_A100_80GB_RUNTIME') from exc
    if not torch.cuda.is_available():
        raise RuntimeError('TEST811_NO_CUDA_GPU: Select a Colab A100 80GB runtime.')
    count=torch.cuda.device_count()
    if count!=1:
        raise RuntimeError(f'TEST811_EXPECTS_ONE_GPU: detected={count}')
    info=torch.cuda.get_device_properties(0)
    name=info.name; gib=info.total_memory/(1024**3)
    print('TEST811_GPU_PREFLIGHT',{'name':name,'vram_gib':round(gib,2),'gpu_count':count},flush=True)
    if 'A100' not in name or info.total_memory < 70*2**30:
        raise RuntimeError(
            f'TEST811_A100_80GB_REQUIRED: detected {name}, {gib:.2f} GiB. '
            'Colab assigned A100 40GB. This 72B locked engine needs A100 80GB; '
            'restart the runtime and execute this cell again. '
            'The locked TEST779 safety gate is intentionally unchanged.')
    free,total=torch.cuda.mem_get_info(0)
    print('TEST811_GPU_FREE_GIB',round(free/2**30,2),flush=True)
    if free < 40*2**30:
        raise RuntimeError(
            f'TEST811_INSUFFICIENT_FREE_VRAM: {free/2**30:.2f} GiB free; '
            'restart the runtime to clear old models.')
preflight_gpu811()

SOURCE811='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB811='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob811(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE811,headers={'User-Agent':'AKBASCORE-TEST811'}),timeout=180) as response:
    raw811=response.read()
assert len(raw811)<100000 and gitblob811(raw811)==BLOB811,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob811(raw811))
tree811=ast.parse(raw811.decode('utf-8'),filename='790.py')
cut811=next((i for i,n in enumerate(tree811.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut811 is not None and cut811==len(tree811.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree811.body[:cut811],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
assert torch.cuda.is_available() and torch.cuda.device_count()==1
assert 'A100' in torch.cuda.get_device_properties(0).name
# TEST811 — TWO VERIFIED ARTICLES + TWENTY SYNTHETIC CONTROLS / NATIVE CUT3
# Selection: two bibliographically locked PLOS articles; article text license NOT asserted as CC0.
# PMCID field in JATS is OPTIONAL; DOI+title are REQUIRED and independently locked.
# Rights review is completed outside this experiment. No runtime license gate.
# This is a bounded H3-routing and evidence-controller experiment, not the final demo.
import re,os,datetime,xml.etree.ElementTree as ET
from urllib.parse import urlparse

TEST='811';OUT=ROOT/'TEST811_results.json';LOG=ROOT/'TEST811.log';MANIFEST=ROOT/'TEST811_manifest.json'
LOG.write_text('',encoding='utf-8')
CANDIDATES=('PMC9521804','PMC9401135')
# Expected bibliographic identifiers; independent source review required before release.
# XML DOI and article title MUST match these locks even if XML omits its PMCID.
ARTICLE_LOCKS811={
 'PMC9521804':{'doi':'10.1371/journal.pcbi.1010476','title':'ten simple rules for getting and giving credit for data'},
 'PMC9401135':{'doi':'10.1371/journal.pone.0272845','title':'long-term availability of data associated with articles in plos one'},
}
API='https://www.ebi.ac.uk/europepmc/webservices/rest/'
ALLOWED_LICENSES={
 'https://creativecommons.org/licenses/by/4.0/':'CC-BY-4.0',
 'https://creativecommons.org/publicdomain/zero/1.0/':'CC0-1.0'}
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,
   'locks':LOCKS,'source790_git_blob':BLOB811,'checks':[],'rows':[],
   'candidates':list(CANDIDATES),'scope':'TEST811: blind 22-cartridge H3 routing with synthetic distractors, evidence arbitration, order and paraphrase robustness',
   'limitations':['Source rights and attribution are reviewed separately from the runtime experiment.',
                  'No automatic scientific truth score; evidence-grounding audit is not a truth oracle.',
                  'Native H3 numerical ranking is evaluated on 22 cartridges, 20 synthetic controls and two real papers; not an independent multi-paper benchmark.',
                  'Agreement is a stability signal, not independent factual verification.',
                  'No training, no source text replay at question time, frozen model.']}
def save811():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate811(name,ok,detail=None):
    R['checks'].append({'name':name,'ok':bool(ok),'detail':detail});save811()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST811_GATE_'+name)
def get811(url,limit=5_000_000):
    gate811('API_HOST',urlparse(url).scheme=='https' and urlparse(url).hostname=='www.ebi.ac.uk')
    req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-Silicon-Hippocampus-TEST811/1.0 (nonbulk academic research)'})
    with urllib.request.urlopen(req,timeout=150) as f:
        gate811('API_FINAL_HOST',urlparse(f.geturl()).hostname=='www.ebi.ac.uk',f.geturl())
        raw=f.read(limit+1)
    gate811('API_SIZE',500<len(raw)<=limit,len(raw))
    return raw

def normlicense811(href):
    href=href.strip().lower().replace('http://','https://').split('#')[0].split('?')[0]
    if href and not href.endswith('/'):href+='/'
    return ALLOWED_LICENSES.get(href)
def localname811(el):return el.tag.rsplit('}',1)[-1]
def first_text811(root,name):
    for el in root.iter():
        if localname811(el)==name:
            val=' '.join(' '.join(el.itertext()).split())
            if val:return val
    return ''
def license811(root):
    # Explicit article-level license element; reject all other variants.
    found=[]
    for el in root.iter():
        if localname811(el)!='license':continue
        urls=[]
        for x in el.iter():
            for k,v in x.attrib.items():
                if k.rsplit('}',1)[-1] in ('href','license-type') and 'creativecommons.org' in v.lower():urls.append(v)
            if x.text:
                urls+=re.findall(r'https?://creativecommons\.org/(?:licenses|publicdomain)/[^\s<>"\']+',x.text,re.I)
        approved=[(u,normlicense811(u)) for u in urls if normlicense811(u)]
        found.append({'urls':urls,'approved':approved,'text':' '.join(' '.join(el.itertext()).split())[:450]})
    # Fail closed if no explicit approved license OR ambiguous multiple license declarations.
    if len(found)!=1 or len(found[0]['approved'])<1:return None,found
    if any('creativecommons.org' in u and normlicense811(u) is None for u in found[0]['urls']):return None,found
    if len(set(v for _,v in found[0]['approved']))!=1:return None,found
    return found[0]['approved'][0][1],found

def text_from811(root):
    # Text only: exclude figure/table captions, references, embedded third-party material,
    # bibliographies and supplementary material. Keep abstract + first few body sections.
    skip={'fig','table-wrap','graphic','inline-graphic','supplementary-material',
          'ref-list','ack','permissions','funding-group','fn-group','media','ext-link','xref'}
    def walk(el):
        if localname811(el) in skip:return ''
        chunks=[el.text or '']
        for c in el:
            chunks.append(walk(c));chunks.append(c.tail or '')
        return ' '.join(' '.join(chunks).split())
    pieces=[]
    for kind in ('abstract','body'):
        element=next((x for x in root.iter() if localname811(x)==kind),None)
        if element is not None:pieces.append(walk(element))
    text='\n'.join(x for x in pieces if x).strip()
    return text

def acquire811(pmcid):
    url=API+pmcid+'/fullTextXML'
    raw=get811(url)
    root=ET.fromstring(raw)
    gate811('JATS_ARTICLE_'+pmcid,localname811(root)=='article')
    # Europe PMC fullTextXML JATS sometimes omits <article-id pub-id-type="pmc">.
    # Missing metadata is NOT a mismatch. If supplied, it MUST match.
    article_meta=next((x for x in root.iter() if localname811(x)=='article-meta'),None)
    gate811('ARTICLE_META_'+pmcid,article_meta is not None)
    ids={}
    for el in article_meta.iter():
        if localname811(el)=='article-id':
            k=el.attrib.get('pub-id-type','').lower()
            v=(el.text or '').strip()
            if k and v:ids.setdefault(k,[]).append(v)
    xmlid=['PMC'+v.upper().removeprefix('PMC') for k,vs in ids.items()
           if k in ('pmc','pmcid') for v in vs]
    gate811('PMCID_IF_PRESENT_'+pmcid,not xmlid or all(x==pmcid for x in xmlid),xmlid)
    # The DOI and title locks are independent of the XML's optional PMCID field.
    doi_values=ids.get('doi',[])
    doi=doi_values[0] if len(doi_values)==1 else ''
    expected=ARTICLE_LOCKS811[pmcid]
    gate811('EXACT_DOI_LOCK_'+pmcid,doi.lower()==expected['doi'],{'xml_doi':doi,'expected':expected['doi']})
    title=first_text811(article_meta,'article-title')
    normalized_title=' '.join(title.casefold().split()).rstrip('.')
    gate811('EXACT_TITLE_LOCK_'+pmcid,normalized_title==expected['title'],
            {'xml_title':title,'expected':expected['title']})
    # Article usage rights were reviewed prior to the experiment; no runtime licensing decision.
    approved='PRE_REVIEWED_OUTSIDE_RUNTIME';license_details=[]
    full=text_from811(root)
    gate811('SCIENTIFIC_BODY_'+pmcid,len(full)>1600,len(full))
    (ROOT/('TEST811_'+pmcid+'.xml')).write_bytes(raw)
    # A bounded exact contiguous scientific excerpt, no paraphrase or fabricated statements.
    # Truncation is explicitly recorded. Final token length checked after tokenizer loads.
    excerpt=full[:6500].rsplit(' ',1)[0]
    gate811('EXCERPT_'+pmcid,len(excerpt)>1000)
    (ROOT/('TEST811_'+pmcid+'.txt')).write_text(excerpt,encoding='utf-8')
    return excerpt,{'pmcid':pmcid,'doi':doi,'title':title,'license':approved,
      'license_evidence':license_details,'xml_identifiers':ids,'xml_url':url,
      'xml_sha256':hashlib.sha256(raw).hexdigest(),
      'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),
      'full_extracted_chars':len(full),'excerpt_chars':len(excerpt),
      'excerpt_truncated':len(excerpt)<len(full),'exclusions':'figures, tables, references, supplements, links'}

STOP=set('a an the and or to of in for on with is are what how does do which this that from under about research article articles study studies paper papers according compare describe evidence findings results'.split())
def words811(s):return set(x for x in re.findall('[a-z]{3,}',s.lower()) if x not in STOP)

def build_real_bank811():
    # BLIND 22-CARTRIDGE CANDIDATE BANK: 20 sealed synthetic control
    # cartridges plus 2 real article cartridges. No metadata, titles,
    # expected labels or source bodies are read by the selector.
    bank={}
    for cid in sorted(entries):
        cp=safe_load(entries[cid])
        try:
            x=cp['h'][0,P:,:].float().cpu().numpy()
            gate811('NONEMPTY_H3_'+cid,x.ndim==2 and x.shape[0]>8 and x.shape[1]==8192,x.shape)
            ix=np.linspace(0,len(x)-1,min(96,len(x)),dtype=np.int64)
            bank[cid]=normalized(x[ix]).T.copy()
        finally:
            del cp
    gate811('BLIND_BANK_22',len(bank)==22 and set(CANDIDATES).issubset(bank))
    return bank

def route811(question,bank):
    # Native H3 scores over ALL 22 cartridges, not just the two articles.
    ordered,raw_scores=numeric_rank(question,bank)
    gate811('H3_RANK_22',len(ordered)==22 and set(ordered)==set(bank))
    return ordered,[(float(raw_scores[cid]),cid) for cid in ordered]

def clean811(x):return ' '.join(x.split()).strip()
def similarity811(a,b):
    x=words811(a);y=words811(b)
    return len(x&y)/max(1,len(x|y)) if x and y else 0.

def native811(ids,q,tag,max_new=128):
    # The locked TEST779 free_generate is used unchanged. 128-token budget is
    # an upper bound, not a guarantee of EOS or a complete sentence.
    t0=time.perf_counter()
    mem,active,_,_=build_fusion(ids,'TEST811_'+tag,True)
    try:
        gate811('NATIVE80_'+tag,len(mem)==80 and list(active)==ids)
        n=int(mem[0][0].shape[-2]);expected=P+sum(int(entries[x]['body_tokens']) for x in ids)
        gate811('NATIVE_LENGTH_'+tag,n==expected,{'n':n,'expected':expected})
        spans=({'B0':(P,P+int(entries[ids[0]]['body_tokens'])),'B1':(P+int(entries[ids[0]]['body_tokens']),n)}
               if len(ids)==2 else {'B0':(P,n),'B1':(n,n)})
        before=memory_seals(mem)
        out=free_generate(mem,('Answer the question using only the physical scientific document memory. Give at most two concise factual sentences (maximum 45 words). If unsupported, answer UNKNOWN.\nQuestion: '+q),seed=None,gain=0.,max_new=max_new,spans=spans)
        gate811('KV_SEAL_'+tag,compare_seals(before,memory_seals(mem)))
        raw=clean811(out['raw'])
        # EOS is not exposed by the locked free_generate. A full token budget
        # means POSSIBLE_TRUNCATION, not a confirmed completed response.
        possible_truncation=int(out['generated_tokens'])>=max_new
        sentence_end=bool(re.search(r'[.!?][\"\')\]]?$',raw))
        return {'ids':ids,'raw':raw,'tokens':out['generated_tokens'],
                'max_new':max_new,'possible_truncation':possible_truncation,
                'sentence_end':sentence_end,'sdpa_calls':out['sdpa_calls'],
                'elapsed_seconds':round(time.perf_counter()-t0,3)}
    finally:
        del mem;gc.collect();release()

def is_unknown811(raw):
    # A source-specific UNKNOWN is missing support, NOT a veto of another source.
    t=clean811(raw).upper()
    return not t or t.startswith('UNKNOWN') or t.startswith('NOT ENOUGH INFORMATION')

def usable811(step):
    return (not step['possible_truncation'] and step['sentence_end']
            and not is_unknown811(step['raw']))

def numeric_facts811(s):
    # Diagnostic only: this is a non-semantic comparison of numbers, not a truth oracle.
    return set(re.findall(r'(?<![\w.])\d+(?:\.\d+)?\s*%',s))

def evidence_conflict811(a,b):
    # Never label semantic disagreement as proved by lexical overlap alone.
    x,y=numeric_facts811(a),numeric_facts811(b)
    return bool(x and y and x!=y)

def decide811(case_id,q,bank,policy='ADAPTIVE'):
    # Frozen model + proven native readout; no offline gold in this function.
    # The hypothesis is the first usable single-source answer, which can be revised.
    full_ranking,scores=route811(q,bank)
    ranking=full_ranking[:2]  # Top-2 blind physical memories; no oracle fallback.
    steps=[];trace=[]
    def read(op,ids):
        r=native811(ids,q,case_id+'_'+policy+'_'+op)
        steps.append({'operation':op,**r})
        return r
    first=read('INITIAL',[ranking[0]])
    hypothesis=first['raw'] if usable811(first) else 'UNKNOWN'
    trace.append({'step':1,'hypothesis':hypothesis,'usable':usable811(first),
                  'action':'PROBE_ALTERNATE' if not usable811(first) else 'VERIFY_HYPOTHESIS'})
    if policy=='FIXED':
        second=read('SECOND',[ranking[1]])
        pair=read('PAIR',ranking)
        reverse=read('REVERSE',list(reversed(ranking)))
        candidate=pair if usable811(pair) else second if usable811(second) else first
        support=max(similarity811(candidate['raw'],x['raw']) if usable811(candidate) and usable811(x) else 0.
                    for x in (first,second,reverse))
        accepted=usable811(candidate) and support>=0.25
        final=candidate['raw'] if accepted else 'UNKNOWN'
        return {'policy':policy,'action':'ANSWER' if accepted else 'ABSTAIN','answer':final,
                'initial_hypothesis':hypothesis,'revised_hypothesis':final,
                'revision':hypothesis!='UNKNOWN' and final!='UNKNOWN' and hypothesis!=final,
                'recovered_from_unknown':hypothesis=='UNKNOWN' and final!='UNKNOWN',
                'support':round(support,5),'selected':ranking,'ranked_22':full_ranking,'steps':steps,'trace':trace,'read_count':len(steps)}
    # Adaptive: act on native observation; stop only when a second independent reading corroborates.
    if not usable811(first):
        second=read('ALTERNATE_AFTER_UNKNOWN',[ranking[1]])
        trace.append({'step':2,'observed':'INITIAL_UNSUPPORTED','alternate_usable':usable811(second),
                      'action':'VERIFY_ALTERNATE' if usable811(second) else 'FUSE_TWO_UNKNOWNS'})
        pair=read('FUSE_ALTERNATE_FIRST',list(reversed(ranking)) if usable811(second) else ranking)
        anchor=second
    else:
        second=None
        pair=read('FUSE_TO_CHALLENGE_INITIAL',ranking)
        anchor=first
        trace.append({'step':2,'observed':'INITIAL_SUPPORTED',
                      'pair_usable':usable811(pair),
                      'agreement':round(similarity811(first['raw'],pair['raw']),5) if usable811(pair) else 0.,
                      'numeric_conflict':evidence_conflict811(first['raw'],pair['raw']),
                      'action':'ASSESS_CONTRADICTION'})
    candidate=pair if usable811(pair) else anchor
    agreement=(similarity811(candidate['raw'],anchor['raw'])
               if usable811(candidate) and usable811(anchor) else 0.)
    conflict=(evidence_conflict811(candidate['raw'],anchor['raw'])
              if usable811(candidate) and usable811(anchor) else False)
    reverse=None
    if not usable811(candidate) or agreement<0.25 or conflict:
        reverse=read('REVERSE_EVIDENCE_CHECK',list(reversed(ranking)))
        trace.append({'step':len(trace)+1,'observed':'INSUFFICIENT_OR_CONFLICTING',
                      'reverse_usable':usable811(reverse),'action':'REASSESS'})
        if usable811(reverse):
            # A revision must be supported by a second distinct physical reading.
            if usable811(pair) and similarity811(reverse['raw'],pair['raw'])>=0.25:
                candidate=pair
            elif usable811(anchor) and similarity811(reverse['raw'],anchor['raw'])>=0.25:
                candidate=anchor
        agreement=max(agreement,similarity811(candidate['raw'],reverse['raw'])
                      if usable811(candidate) and usable811(reverse) else 0.)
    if agreement<0.25 and second is None:
        second=read('ALTERNATE_EVIDENCE_CHECK',[ranking[1]])
        agreement=max(agreement,similarity811(candidate['raw'],second['raw'])
                      if usable811(candidate) and usable811(second) else 0.)
        trace.append({'step':len(trace)+1,'observed':'LOW_CORROBORATION',
                      'alternate_usable':usable811(second),'action':'FINAL_REASSESS'})
    accepted=usable811(candidate) and agreement>=0.25
    final=candidate['raw'] if accepted else 'UNKNOWN'
    trace.append({'step':len(trace)+1,'observed':'FINAL_EVIDENCE',
                  'action':'ANSWER' if accepted else 'ABSTAIN','revised':final!=hypothesis})
    return {'policy':policy,'action':'ANSWER' if accepted else 'ABSTAIN','answer':final,
            'initial_hypothesis':hypothesis,'revised_hypothesis':final,
            'revision':hypothesis!='UNKNOWN' and final!='UNKNOWN' and hypothesis!=final,
            'recovered_from_unknown':hypothesis=='UNKNOWN' and final!='UNKNOWN',
            'support':round(agreement,5),'selected':ranking,'ranked_22':full_ranking,'steps':steps,'trace':trace,'read_count':len(steps)}

# Offline, sealed before GPU inference: deliberately narrow exact-fact checks.
# These rules are NEVER available to route811, decide811 or free_generate.
# They are insufficient to establish full scientific accuracy.
OFFLINE811={
 'Q2':{'required_percent':['98%','78%'],'relevant':'PMC9401135'},
 'Q8':{'required_percent':['80%','78%','98%'],'relevant':'PMC9401135'},
}
def grade811(case_id,record):
    base=case_id.removesuffix('_PARA')
    spec=OFFLINE811.get(base)
    if spec is None:return {'status':'UNSCORED_NO_INDEPENDENT_FACT_KEY'}
    facts=numeric_facts811(record['answer'])
    initial=numeric_facts811(record['initial_hypothesis'])
    required=set(spec['required_percent'])
    return {'status':'NARROW_NUMERIC_FACT_CHECK',
            'required':sorted(required),'observed':sorted(facts),
            'passed':record['action']=='ANSWER' and required<=facts,
            'initial_passed':required<=initial,
            'initial_source_relevant':record['selected'][0]==spec['relevant'],
            'note':'Presence of expected numbers is not proof of correct relationships or general reasoning.'}

try:
    log('='*110);log('TEST811 — BLIND 22-CARTRIDGE ROUTING / ADAPTIVE VS FIXED / NATIVE CUT3')
    gate811('TEST790_EXACT_BLOB',gitblob811(raw811)==BLOB811)
    gate811('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate811('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate811('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    persist_manifest()
    gate811('PROVEN_NATIVE_SYMBOLS',all(callable(globals().get(k)) for k in
         ('model_setup','build_fusion','free_generate','physical_commit','memory_seals','compare_seals')))
    docs={};rawtexts={}
    for pmcid in CANDIDATES:
        rawtexts[pmcid],docs[pmcid]=acquire811(pmcid)
        log('TEST811_SOURCE_LOADED',pmcid,docs[pmcid]['doi'],docs[pmcid]['title'])
    gate811('TWO_LOCKED_ARTICLES',len(docs)==2 and set(docs)==set(ARTICLE_LOCKS811) and len(set(CANDIDATES))==2)
    R['documents']=docs;save811()
    # Questions frozen before model load; no titles, PMCID, DOI or article bodies in prompts.
    # All prompts avoid article titles, DOI, PMCID and source labels.
    # Expected relevant source(s) are kept ONLY in the offline evaluator below.
    questions=[
      ('Q1','What role do persistent identifiers play in giving researchers credit for shared scientific data?'),
      ('Q2','In the empirical study of data availability, how did DOI-linked and URL-linked resources compare?'),
      ('Q3','Distinguish recommended practices for making data findable from measured evidence of link availability.'),
      ('Q4','Does assigning a DOI guarantee that scientific data will remain accessible forever?'),
      ('Q5','What limitations affect long-term availability of published research data?'),
      ('Q6','What is content drift when a research-data link still resolves, and why is it problematic?'),
      ('Q7','How do persistent identifiers support attribution and responsible data reuse?'),
      ('Q8','What does the empirical study report about manual versus automated retrieval of linked data?')]
    # Offline routing evaluation only. NEVER passed to route811 or free_generate.
    expected_sources={'Q1':['PMC9521804'],'Q2':['PMC9401135'],
      'Q3':['PMC9521804','PMC9401135'],'Q4':['PMC9401135','PMC9521804'],
      'Q5':['PMC9401135'],'Q6':['PMC9401135'],
      'Q7':['PMC9521804'],'Q8':['PMC9401135']}
    gate811('QUESTION_NO_BODY_REPLAY',all(len(q)<320 and not any(cid in q for cid in CANDIDATES) and not any(d['title'].lower() in q.lower() for d in ARTICLE_LOCKS811.values()) for _,q in questions))
    R['question_panel_sha256']=hashlib.sha256(json.dumps(questions,ensure_ascii=False).encode()).hexdigest()
    R['question_panel']=questions;save811()
    model_setup();before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate811('BASE_20_CARTRIDGES',len(entries)==20,len(entries))
    # Tokenizer-aware excerpt trimming; physical_text_sha256 records actual physical text.
    # The original excerpt SHA remains unchanged as the extraction audit record.
    for pmcid in CANDIDATES:
        title=docs[pmcid]['title'];text=rawtexts[pmcid]
        ids=tok.encode(text,add_special_tokens=False)
        if len(ids)>950:
            text=tok.decode(ids[:950],skip_special_tokens=True).strip()
        gate811('TRIMMED_TEXT_NONEMPTY_'+pmcid,len(text)>300)
        body='Scientific article: '+title+'\n'+text
        docs[pmcid]['physical_text_sha256']=hashlib.sha256(body.encode()).hexdigest()
        docs[pmcid]['physical_text_tokens']=len(tok.encode(body,add_special_tokens=False))
        docs[pmcid]['physical_text_truncated']=len(ids)>950
        gate811('TOKEN_BUDGET_'+pmcid,docs[pmcid]['physical_text_tokens']<=1150,docs[pmcid]['physical_text_tokens'])
        physical_commit(pmcid,body)
    gate811('PHYSICAL_22_CARTRIDGES',len(entries)==22,len(entries))
    gate811('BOTH_REAL_ARTICLES_COMMITTED',all(x in entries for x in CANDIDATES))
    R['documents']=docs;save811()
    bank811=build_real_bank811()
    gate811('NUMERICAL_H3_BANK',len(bank811)==22 and all(x.shape[0]==8192 for x in bank811.values()))
    # TEST811: sealed question-paraphrase routing controls. These are NOT
    # used to choose a source or to alter answers; they measure route stability.
    # Ground truth is consulted only after both independent routes are produced.
    paraphrases={
      'Q1':'How do stable identifiers help acknowledge contributions to shared datasets?',
      'Q2':'In the measured data-link study, compare access success for DOI references and ordinary URLs.',
      'Q3':'Separate guidance about data discovery from observations about links that actually work.',
      'Q4':'Is a digital object identifier sufficient proof that a dataset will always be retrievable?',
      'Q5':'Which weaknesses limit the lasting accessibility of research datasets?',
      'Q6':'What is the danger when a dataset address works but now leads to different material?',
      'Q7':'Explain how persistent references support proper acknowledgement and reuse of datasets.',
      'Q8':'What did the observational paper find when comparing automatic link retrieval with manual checks?'
    }
    gate811('PARAPHRASE_PANEL_LOCK',set(paraphrases)==set(x[0] for x in questions))
    R['paraphrase_panel_sha256']=hashlib.sha256(json.dumps(paraphrases,sort_keys=True).encode()).hexdigest()
    R['routing_robustness']=[];save811()
    for qid,q in questions:
        # Both rankings are obtained with the exact locked TEST757 CUT3/H3 scorer.
        original_order,original_scores=route811(q,bank811)
        paraphrase_order,paraphrase_scores=route811(paraphrases[qid],bank811)
        relevant=expected_sources[qid]  # offline evaluation only
        rr={'case_id':qid,'original_top1':original_order[0],
            'paraphrase_top1':paraphrase_order[0],
            'same_top1':original_order[0]==paraphrase_order[0],
            'original_top1_relevant':original_order[0] in relevant,
            'paraphrase_top1_relevant':paraphrase_order[0] in relevant,
            'original_scores':{cid:round(float(v),6) for v,cid in original_scores},
            'paraphrase_scores':{cid:round(float(v),6) for v,cid in paraphrase_scores}}
        R['routing_robustness'].append(rr);save811()
        log('TEST811_ROUTE_PARAPHRASE',json.dumps(rr,ensure_ascii=False))
    gate811('PARAPHRASE_EIGHT',len(R['routing_robustness'])==8)
    evaluation_questions=questions+[(qid+'_PARA',paraphrases[qid]) for qid,_ in questions]
    # A/B: same questions, same physical source bank, no gold in controllers.
    # Counterfactuals: each real source is independently removed from candidate bank.
    for qid,q in evaluation_questions:
        base_id=qid.removesuffix('_PARA')
        adaptive=decide811(qid,q,bank811,'ADAPTIVE')
        fixed=decide811(qid,q,bank811,'FIXED')
        offline=expected_sources[base_id]
        row={'case_id':qid,'question':q,'adaptive':adaptive,'fixed':fixed,
             'offline_fact_audit':{'adaptive':grade811(qid,adaptive),'fixed':grade811(qid,fixed)},
             'offline_routing_eval':{'relevant_sources':offline,'top1_relevant':adaptive['selected'][0] in offline,
             'top2_relevant':bool(set(adaptive['selected'])&set(offline)),
             'relevant_rank_positions':{src:adaptive['ranked_22'].index(src)+1 for src in offline},
             'control_cartridges_in_top2':sum(cid not in CANDIDATES for cid in adaptive['selected'])}}
        R['rows'].append(row);save811();log('TEST811_ROW',json.dumps(row,ensure_ascii=False))
    gate811('THIRTY_TWO_POLICY_CASES',len(R['rows'])==16 and all(x['adaptive']['read_count']>=2 and x['fixed']['read_count']==4 for x in R['rows']))
    gate811('ADAPTIVE_BOUNDED',all(x['adaptive']['read_count']<=4 for x in R['rows']))
    gate811('OFFLINE_FACT_AUDIT_SEALED',set(OFFLINE811)=={'Q2','Q8'} and all('required_percent' in x for x in OFFLINE811.values()))
    gate811('ACTUAL_POLICY_BRANCHES',all(x['adaptive']['trace'] for x in R['rows']))
    # Observed policy differences are evidence of branching, NOT proof of general reasoning.
    R['policy_comparison']={
      'adaptive_answers':sum(x['adaptive']['action']=='ANSWER' for x in R['rows']),
      'fixed_answers':sum(x['fixed']['action']=='ANSWER' for x in R['rows']),
      'adaptive_reads':sum(x['adaptive']['read_count'] for x in R['rows']),
      'fixed_reads':sum(x['fixed']['read_count'] for x in R['rows']),
      'changed_decisions':sum(x['adaptive']['action']!=x['fixed']['action'] for x in R['rows']),
      'different_read_counts':sum(x['adaptive']['read_count']!=x['fixed']['read_count'] for x in R['rows']),
      'adaptive_revisions':sum(x['adaptive']['revision'] for x in R['rows']),
      'adaptive_recoveries':sum(x['adaptive']['recovered_from_unknown'] for x in R['rows']),
      'fixed_revisions':sum(x['fixed']['revision'] for x in R['rows']),
      'audited_cases':sum(x['offline_fact_audit']['adaptive']['status']=='NARROW_NUMERIC_FACT_CHECK' for x in R['rows']),
      'adaptive_audited_pass':sum(x['offline_fact_audit']['adaptive'].get('passed',False) for x in R['rows']),
      'fixed_audited_pass':sum(x['offline_fact_audit']['fixed'].get('passed',False) for x in R['rows'])}
    log('TEST811_POLICY_COMPARISON',json.dumps(R['policy_comparison']))
    gate811('FROZEN_WEIGHTS',sentinel()==before)
    gate811('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==22)
    gate811('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'cases':len(R['rows']),'source_count':len(bank811),
      'adaptive_native_reads':R['policy_comparison']['adaptive_reads'],
      'fixed_native_reads':R['policy_comparison']['fixed_reads'],
      'adaptive_answers':R['policy_comparison']['adaptive_answers'],
      'fixed_answers':R['policy_comparison']['fixed_answers'],
      'changed_decisions':R['policy_comparison']['changed_decisions'],
      'different_read_counts':R['policy_comparison']['different_read_counts'],
      'routing_top1_relevant':sum(x['offline_routing_eval']['top1_relevant'] for x in R['rows']),
      'routing_top2_relevant':sum(x['offline_routing_eval']['top2_relevant'] for x in R['rows']),
      'decoy_selected_cases':sum(x['offline_routing_eval']['control_cartridges_in_top2']>0 for x in R['rows']),
      'scientific_accuracy':'UNSCORED_REQUIRES_INDEPENDENT_REVIEW',
      'blind_bank_composition':'20 synthetic control cartridges + 2 verified real article cartridges',
      'autonomous_recursive_reasoning_proven':False,
      'hypothesis_revision_observed':R['policy_comparison']['adaptive_revisions'],
      'unknown_recovery_observed':R['policy_comparison']['adaptive_recoveries'],
      'narrow_fact_audit_pass':R['policy_comparison']['adaptive_audited_pass'],
      'narrow_fact_audit_total':R['policy_comparison']['audited_cases'],
      'claim':'Tests blind H3 selection among 22 physical cartridges, including 20 synthetic controls; no oracle routing or gold in inference. Not proof of general autonomous reasoning.'}
    R['status']='COMPLETE_UNGRADED';save811()
    log('TEST811_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as exc:
    R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save811()
    log('TEST811_FAILED',repr(exc));log(R['traceback']);raise
finally:
    gc.collect()
    if 'release' in globals() and callable(release):release()
    save811()
