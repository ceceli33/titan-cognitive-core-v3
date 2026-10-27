# AKBASCORE SILICON HIPPOCAMPUS — TEST805
# RESPONSE COMPLETENESS / EVIDENCE-DEPENDENCE AUDIT / PHYSICAL CUT3 CARTRIDGES
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB (40GB NOT SUPPORTED)
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# TEST805: no answer oracle; no claims of general autonomous reasoning.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

# Fail fast BEFORE downloading locked source trees or 72B model weights.
# Do not weaken the TEST779 hardware contract.
def preflight_gpu805():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('TEST805_REQUIRES_TORCH_AND_A100_80GB_RUNTIME') from exc
    if not torch.cuda.is_available():
        raise RuntimeError('TEST805_NO_CUDA_GPU: Select a Colab A100 80GB runtime.')
    count=torch.cuda.device_count()
    if count!=1:
        raise RuntimeError(f'TEST805_EXPECTS_ONE_GPU: detected={count}')
    info=torch.cuda.get_device_properties(0)
    name=info.name; gib=info.total_memory/(1024**3)
    print('TEST805_GPU_PREFLIGHT',{'name':name,'vram_gib':round(gib,2),'gpu_count':count},flush=True)
    if 'A100' not in name or info.total_memory < 70*2**30:
        raise RuntimeError(
            f'TEST805_A100_80GB_REQUIRED: detected {name}, {gib:.2f} GiB. '
            'Colab assigned A100 40GB. This 72B locked engine needs A100 80GB; '
            'restart the runtime and execute this cell again. '
            'The locked TEST779 safety gate is intentionally unchanged.')
    free,total=torch.cuda.mem_get_info(0)
    print('TEST805_GPU_FREE_GIB',round(free/2**30,2),flush=True)
    if free < 40*2**30:
        raise RuntimeError(
            f'TEST805_INSUFFICIENT_FREE_VRAM: {free/2**30:.2f} GiB free; '
            'restart the runtime to clear old models.')
preflight_gpu805()

SOURCE805='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB805='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob805(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE805,headers={'User-Agent':'AKBASCORE-TEST805'}),timeout=180) as response:
    raw805=response.read()
assert len(raw805)<100000 and gitblob805(raw805)==BLOB805,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob805(raw805))
tree805=ast.parse(raw805.decode('utf-8'),filename='790.py')
cut805=next((i for i,n in enumerate(tree805.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut805 is not None and cut805==len(tree805.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree805.body[:cut805],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
assert torch.cuda.is_available() and torch.cuda.device_count()==1
assert 'A100' in torch.cuda.get_device_properties(0).name
# TEST805 — TWO VERIFIED CC0 RESEARCH ARTICLES / NATIVE CUT3
# Selection: two specific PLOS articles with publisher CC0 declarations.
# PMCID field in JATS is OPTIONAL; DOI+title are REQUIRED and independently locked.
# Rights review is completed outside this experiment. No runtime license gate.
# This is a bounded evidence-controller experiment, not the final demo.
import re,os,datetime,xml.etree.ElementTree as ET
from urllib.parse import urlparse

TEST='805';OUT=ROOT/'TEST805_results.json';LOG=ROOT/'TEST805.log';MANIFEST=ROOT/'TEST805_manifest.json'
LOG.write_text('',encoding='utf-8')
CANDIDATES=('PMC9521804','PMC9401135')
# Expected bibliographic identifiers; independent source review required before release.
# XML DOI and article title MUST match these locks even if XML omits its PMCID.
ARTICLE_LOCKS805={
 'PMC9521804':{'doi':'10.1371/journal.pcbi.1010476','title':'ten simple rules for getting and giving credit for data'},
 'PMC9401135':{'doi':'10.1371/journal.pone.0272845','title':'long-term availability of data associated with articles in plos one'},
}
API='https://www.ebi.ac.uk/europepmc/webservices/rest/'
ALLOWED_LICENSES={
 'https://creativecommons.org/licenses/by/4.0/':'CC-BY-4.0',
 'https://creativecommons.org/publicdomain/zero/1.0/':'CC0-1.0'}
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,
   'locks':LOCKS,'source790_git_blob':BLOB805,'checks':[],'rows':[],
   'candidates':list(CANDIDATES),'scope':'TEST805: physical CUT3 response completeness and independent source-visibility audit',
   'limitations':['Source rights and attribution are reviewed separately from the runtime experiment.',
                  'No automatic scientific truth score; evidence-grounding audit is not a truth oracle.',
                  'Routing is article-title lexical baseline, NOT autonomous semantic retrieval.',
                  'Agreement does not imply factual correctness or self-correction.',
                  'No training, no source text replay at question time, frozen model.']}
def save805():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate805(name,ok,detail=None):
    R['checks'].append({'name':name,'ok':bool(ok),'detail':detail});save805()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST805_GATE_'+name)
def get805(url,limit=5_000_000):
    gate805('API_HOST',urlparse(url).scheme=='https' and urlparse(url).hostname=='www.ebi.ac.uk')
    req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-Silicon-Hippocampus-TEST805/1.0 (nonbulk academic research)'})
    with urllib.request.urlopen(req,timeout=150) as f:
        gate805('API_FINAL_HOST',urlparse(f.geturl()).hostname=='www.ebi.ac.uk',f.geturl())
        raw=f.read(limit+1)
    gate805('API_SIZE',500<len(raw)<=limit,len(raw))
    return raw

def normlicense805(href):
    href=href.strip().lower().replace('http://','https://').split('#')[0].split('?')[0]
    if href and not href.endswith('/'):href+='/'
    return ALLOWED_LICENSES.get(href)
def localname805(el):return el.tag.rsplit('}',1)[-1]
def first_text805(root,name):
    for el in root.iter():
        if localname805(el)==name:
            val=' '.join(' '.join(el.itertext()).split())
            if val:return val
    return ''
def license805(root):
    # Explicit article-level license element; reject all other variants.
    found=[]
    for el in root.iter():
        if localname805(el)!='license':continue
        urls=[]
        for x in el.iter():
            for k,v in x.attrib.items():
                if k.rsplit('}',1)[-1] in ('href','license-type') and 'creativecommons.org' in v.lower():urls.append(v)
            if x.text:
                urls+=re.findall(r'https?://creativecommons\.org/(?:licenses|publicdomain)/[^\s<>"\']+',x.text,re.I)
        approved=[(u,normlicense805(u)) for u in urls if normlicense805(u)]
        found.append({'urls':urls,'approved':approved,'text':' '.join(' '.join(el.itertext()).split())[:450]})
    # Fail closed if no explicit approved license OR ambiguous multiple license declarations.
    if len(found)!=1 or len(found[0]['approved'])<1:return None,found
    if any('creativecommons.org' in u and normlicense805(u) is None for u in found[0]['urls']):return None,found
    if len(set(v for _,v in found[0]['approved']))!=1:return None,found
    return found[0]['approved'][0][1],found

def text_from805(root):
    # Text only: exclude figure/table captions, references, embedded third-party material,
    # bibliographies and supplementary material. Keep abstract + first few body sections.
    skip={'fig','table-wrap','graphic','inline-graphic','supplementary-material',
          'ref-list','ack','permissions','funding-group','fn-group','media','ext-link','xref'}
    def walk(el):
        if localname805(el) in skip:return ''
        chunks=[el.text or '']
        for c in el:
            chunks.append(walk(c));chunks.append(c.tail or '')
        return ' '.join(' '.join(chunks).split())
    pieces=[]
    for kind in ('abstract','body'):
        element=next((x for x in root.iter() if localname805(x)==kind),None)
        if element is not None:pieces.append(walk(element))
    text='\n'.join(x for x in pieces if x).strip()
    return text

def acquire805(pmcid):
    url=API+pmcid+'/fullTextXML'
    raw=get805(url)
    root=ET.fromstring(raw)
    gate805('JATS_ARTICLE_'+pmcid,localname805(root)=='article')
    # Europe PMC fullTextXML JATS sometimes omits <article-id pub-id-type="pmc">.
    # Missing metadata is NOT a mismatch. If supplied, it MUST match.
    article_meta=next((x for x in root.iter() if localname805(x)=='article-meta'),None)
    gate805('ARTICLE_META_'+pmcid,article_meta is not None)
    ids={}
    for el in article_meta.iter():
        if localname805(el)=='article-id':
            k=el.attrib.get('pub-id-type','').lower()
            v=(el.text or '').strip()
            if k and v:ids.setdefault(k,[]).append(v)
    xmlid=['PMC'+v.upper().removeprefix('PMC') for k,vs in ids.items()
           if k in ('pmc','pmcid') for v in vs]
    gate805('PMCID_IF_PRESENT_'+pmcid,not xmlid or all(x==pmcid for x in xmlid),xmlid)
    # The DOI and title locks are independent of the XML's optional PMCID field.
    doi_values=ids.get('doi',[])
    doi=doi_values[0] if len(doi_values)==1 else ''
    expected=ARTICLE_LOCKS805[pmcid]
    gate805('EXACT_DOI_LOCK_'+pmcid,doi.lower()==expected['doi'],{'xml_doi':doi,'expected':expected['doi']})
    title=first_text805(article_meta,'article-title')
    normalized_title=' '.join(title.casefold().split()).rstrip('.')
    gate805('EXACT_TITLE_LOCK_'+pmcid,normalized_title==expected['title'],
            {'xml_title':title,'expected':expected['title']})
    # Article usage rights were reviewed prior to the experiment; no runtime licensing decision.
    approved='PRE_REVIEWED_OUTSIDE_RUNTIME';license_details=[]
    full=text_from805(root)
    gate805('SCIENTIFIC_BODY_'+pmcid,len(full)>1600,len(full))
    (ROOT/('TEST805_'+pmcid+'.xml')).write_bytes(raw)
    # A bounded exact contiguous scientific excerpt, no paraphrase or fabricated statements.
    # Truncation is explicitly recorded. Final token length checked after tokenizer loads.
    excerpt=full[:6500].rsplit(' ',1)[0]
    gate805('EXCERPT_'+pmcid,len(excerpt)>1000)
    (ROOT/('TEST805_'+pmcid+'.txt')).write_text(excerpt,encoding='utf-8')
    return excerpt,{'pmcid':pmcid,'doi':doi,'title':title,'license':approved,
      'license_evidence':license_details,'xml_identifiers':ids,'xml_url':url,
      'xml_sha256':hashlib.sha256(raw).hexdigest(),
      'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),
      'full_extracted_chars':len(full),'excerpt_chars':len(excerpt),
      'excerpt_truncated':len(excerpt)<len(full),'exclusions':'figures, tables, references, supplements, links'}

STOP=set('a an the and or to of in for on with is are what how does do which this that from under about research article articles study studies paper papers according compare describe evidence findings results'.split())
def words805(s):return set(x for x in re.findall('[a-z]{3,}',s.lower()) if x not in STOP)
def route805(question,docs):
    q=words805(question)
    scores=[]
    for cid,m in docs.items():
        title=words805(m['title'])
        score=len(q&title)/max(1,len(title)**.5)
        scores.append((float(score),cid))
    scores.sort(key=lambda x:(-x[0],x[1]))
    return [cid for _,cid in scores],scores

def clean805(x):return ' '.join(x.split()).strip()
def similarity805(a,b):
    x=words805(a);y=words805(b)
    return len(x&y)/max(1,len(x|y)) if x and y else 0.

def native805(ids,q,tag,max_new=160):
    # The locked TEST779 free_generate is used unchanged. 160-token budget is
    # an upper bound, not a guarantee of EOS or a complete sentence.
    t0=time.perf_counter()
    mem,active,_,_=build_fusion(ids,'TEST805_'+tag,True)
    try:
        gate805('NATIVE80_'+tag,len(mem)==80 and list(active)==ids)
        n=int(mem[0][0].shape[-2]);expected=P+sum(int(entries[x]['body_tokens']) for x in ids)
        gate805('NATIVE_LENGTH_'+tag,n==expected,{'n':n,'expected':expected})
        spans=({'B0':(P,P+int(entries[ids[0]]['body_tokens'])),'B1':(P+int(entries[ids[0]]['body_tokens']),n)}
               if len(ids)==2 else {'B0':(P,n),'B1':(n,n)})
        before=memory_seals(mem)
        out=free_generate(mem,q,seed=None,gain=0.,max_new=max_new,spans=spans)
        gate805('KV_SEAL_'+tag,compare_seals(before,memory_seals(mem)))
        raw=clean805(out['raw'])
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

def decide805(case_id,q,docs):
    ranking,scores=route805(q,docs)
    chosen=ranking[:2]
    assert len(chosen)==2 and len(set(chosen))==2
    steps=[]
    def read(name,ids):
        r=native805(ids,q,case_id+'_'+name)
        steps.append({'operation':name,**r});return r
    # Physical causal controls: pair, relevant single, reverse pair.
    pair=read('PAIR',chosen)
    single=read('SINGLE',[chosen[0]])
    reverse=read('REVERSE_PAIR',list(reversed(chosen)))
    sim1=similarity805(pair['raw'],single['raw'])
    sim2=similarity805(pair['raw'],reverse['raw'])
    # The retry is triggered by a bounded observable discrepancy, not gold.
    retry=any(x['possible_truncation'] or not x['raw'] for x in (pair,single,reverse)) or min(sim1,sim2)<.30
    alternate=None
    if retry:alternate=read('ALTERNATE_SINGLE',[chosen[1]])
    complete=all(x['raw'] and not x['possible_truncation'] for x in (pair,single,reverse))
    # Sentence-end is an additional heuristic; not a semantic truth criterion.
    stable=bool(complete and pair['sentence_end'] and min(sim1,sim2)>=.30)
    return {'action':'ANSWER' if stable else 'ABSTAIN',
            'answer':pair['raw'] if stable else 'UNKNOWN',
            'selected':chosen,'route_method':'TITLE_LEXICAL_BASELINE_NOT_AUTONOMOUS',
            'scores':[{'id':cid,'score':round(score,5)} for score,cid in scores],
            'steps':steps,'retry':retry,'complete_under_budget':complete,'pair_sentence_end':pair['sentence_end'],
            'all_sentence_end':all(x['sentence_end'] for x in (pair,single,reverse)),
            'lexical_agreement':{'pair_single':sim1,'pair_reverse':sim2,
                                 'pair_alternate':similarity805(pair['raw'],alternate['raw']) if alternate else None},
            'warning':'Lexical agreement and sentence ending do not prove scientific accuracy.'}

try:
    log('='*110);log('TEST805 — REAL ARTICLES / COMPLETION AUDIT / NATIVE CUT3')
    gate805('TEST790_EXACT_BLOB',gitblob805(raw805)==BLOB805)
    gate805('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate805('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate805('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    persist_manifest()
    gate805('PROVEN_NATIVE_SYMBOLS',all(callable(globals().get(k)) for k in
         ('model_setup','build_fusion','free_generate','physical_commit','memory_seals','compare_seals')))
    docs={};rawtexts={}
    for pmcid in CANDIDATES:
        rawtexts[pmcid],docs[pmcid]=acquire805(pmcid)
        log('TEST805_SOURCE_LOADED',pmcid,docs[pmcid]['doi'],docs[pmcid]['title'])
    gate805('TWO_LOCKED_ARTICLES',len(docs)==2 and set(docs)==set(ARTICLE_LOCKS805) and len(set(CANDIDATES))==2)
    R['documents']=docs;save805()
    # Questions frozen before model load; use title words only, not abstracts/bodies.
    questions=[
      ('Q1','According to the article Ten simple rules for getting and giving credit for data, what role do persistent identifiers play in crediting scientific data?'),
      ('Q2','According to the article Long-term availability of data associated with articles in PLOS ONE, how did DOI-linked and URL-linked resources compare in availability?'),
      ('Q3','Compare the two articles on the role of DOIs in making research data discoverable and accessible. Distinguish recommendations from measured results.'),
      ('Q4','What can and cannot be concluded from these two papers about whether a DOI guarantees permanent access to research data?'),
      ('Q5','Compare the evidence and limitations of the two articles regarding long-term data availability.'),
      ('Q6','If a data link is still valid but its content changed, what risk is discussed in the empirical paper and how does that relate to FAIR data practices?')]
    gate805('QUESTION_NO_BODY_REPLAY',all(len(q)<320 for _,q in questions))
    R['question_panel_sha256']=hashlib.sha256(json.dumps(questions,ensure_ascii=False).encode()).hexdigest()
    R['question_panel']=questions;save805()
    model_setup();before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate805('BASE_20_CARTRIDGES',len(entries)==20,len(entries))
    # Tokenizer-aware excerpt trimming; physical_text_sha256 records actual physical text.
    # The original excerpt SHA remains unchanged as the extraction audit record.
    for pmcid in CANDIDATES:
        title=docs[pmcid]['title'];text=rawtexts[pmcid]
        ids=tok.encode(text,add_special_tokens=False)
        if len(ids)>950:
            text=tok.decode(ids[:950],skip_special_tokens=True).strip()
        gate805('TRIMMED_TEXT_NONEMPTY_'+pmcid,len(text)>300)
        body='Scientific article: '+title+'\n'+text
        docs[pmcid]['physical_text_sha256']=hashlib.sha256(body.encode()).hexdigest()
        docs[pmcid]['physical_text_tokens']=len(tok.encode(body,add_special_tokens=False))
        docs[pmcid]['physical_text_truncated']=len(ids)>950
        gate805('TOKEN_BUDGET_'+pmcid,docs[pmcid]['physical_text_tokens']<=1150,docs[pmcid]['physical_text_tokens'])
        physical_commit(pmcid,body)
    gate805('PHYSICAL_22_CARTRIDGES',len(entries)==22,len(entries))
    gate805('BOTH_REAL_ARTICLES_COMMITTED',all(x in entries for x in CANDIDATES))
    R['documents']=docs;save805()
    for qid,q in questions:
        decision=decide805(qid,q,docs)
        row={'case_id':qid,'question':q,'controller':decision}
        R['rows'].append(row);save805();log('TEST805_ROW',json.dumps(row,ensure_ascii=False))
    gate805('SIX_CASES',len(R['rows'])==6)
    gate805('BOUNDED_STEPS',all(3<=len(x['controller']['steps'])<=4 for x in R['rows']))
    gate805('RETRY_CONDITIONAL',all((len(x['controller']['steps'])==4)==x['controller']['retry'] for x in R['rows']))
    gate805('FROZEN_WEIGHTS',sentinel()==before)
    gate805('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==22)
    gate805('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'cases':6,'source_count':2,'native_reads':sum(len(x['controller']['steps']) for x in R['rows']),
      'answers':sum(x['controller']['action']=='ANSWER' for x in R['rows']),
      'abstentions':sum(x['controller']['action']=='ABSTAIN' for x in R['rows']),
      'retries':sum(x['controller']['retry'] for x in R['rows']),
      'possible_truncated_pair_answers':sum(x['controller']['steps'][0]['possible_truncation'] for x in R['rows']),
      'complete_under_budget':sum(x['controller']['complete_under_budget'] for x in R['rows']),
      'pair_sentence_end':sum(x['controller']['steps'][0]['sentence_end'] for x in R['rows']),
      'scientific_accuracy':'UNSCORED_REQUIRES_INDEPENDENT_REVIEW',
      'autonomous_recursive_reasoning_proven':False}
    R['status']='COMPLETE_UNGRADED';save805()
    log('TEST805_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as exc:
    R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save805()
    log('TEST805_FAILED',repr(exc));log(R['traceback']);raise
finally:
    gc.collect()
    if 'release' in globals() and callable(release):release()
    save805()
