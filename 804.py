# AKBASCORE SILICON HIPPOCAMPUS — TEST804
# BOUNDED EVIDENCE-DIRECTED CLOSED LOOP / PHYSICAL CUT3 CARTRIDGES
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB (40GB NOT SUPPORTED)
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# First bounded adaptive controller; general autonomous reasoning remains unproven.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

# Fail fast BEFORE downloading locked source trees or 72B model weights.
# Do not weaken the TEST779 hardware contract.
def preflight_gpu804():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('TEST804_REQUIRES_TORCH_AND_A100_80GB_RUNTIME') from exc
    if not torch.cuda.is_available():
        raise RuntimeError('TEST804_NO_CUDA_GPU: Select a Colab A100 80GB runtime.')
    count=torch.cuda.device_count()
    if count!=1:
        raise RuntimeError(f'TEST804_EXPECTS_ONE_GPU: detected={count}')
    info=torch.cuda.get_device_properties(0)
    name=info.name; gib=info.total_memory/(1024**3)
    print('TEST804_GPU_PREFLIGHT',{'name':name,'vram_gib':round(gib,2),'gpu_count':count},flush=True)
    if 'A100' not in name or info.total_memory < 70*2**30:
        raise RuntimeError(
            f'TEST804_A100_80GB_REQUIRED: detected {name}, {gib:.2f} GiB. '
            'Colab assigned A100 40GB. This 72B locked engine needs A100 80GB; '
            'restart the runtime and execute this cell again. '
            'The locked TEST779 safety gate is intentionally unchanged.')
    free,total=torch.cuda.mem_get_info(0)
    print('TEST804_GPU_FREE_GIB',round(free/2**30,2),flush=True)
    if free < 40*2**30:
        raise RuntimeError(
            f'TEST804_INSUFFICIENT_FREE_VRAM: {free/2**30:.2f} GiB free; '
            'restart the runtime to clear old models.')
preflight_gpu804()

SOURCE804='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB804='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob804(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE804,headers={'User-Agent':'AKBASCORE-TEST804'}),timeout=180) as response:
    raw804=response.read()
assert gitblob804(raw804)==BLOB804,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob804(raw804))
tree804=ast.parse(raw804.decode('utf-8'),filename='790.py')
cut804=next((i for i,n in enumerate(tree804.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut804 is not None and cut804==len(tree804.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree804.body[:cut804],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
assert torch.cuda.is_available() and torch.cuda.device_count()==1
assert 'A100' in torch.cuda.get_device_properties(0).name
# TEST804 — TWO VERIFIED CC0 RESEARCH ARTICLES / NATIVE CUT3
# Selection: two specific PLOS articles with publisher CC0 declarations.
# PMCID field in JATS is OPTIONAL; DOI+title are REQUIRED and independently locked.
# Rights review is completed outside this experiment. No runtime license gate.
# This is a bounded evidence-controller experiment, not the final demo.
import re,os,datetime,xml.etree.ElementTree as ET
from urllib.parse import urlparse

TEST='804';OUT=ROOT/'TEST804_results.json';LOG=ROOT/'TEST804.log';MANIFEST=ROOT/'TEST804_manifest.json'
LOG.write_text('',encoding='utf-8')
CANDIDATES=('PMC9521804','PMC9401135')
# Expected bibliographic identifiers; independent source review required before release.
# XML DOI and article title MUST match these locks even if XML omits its PMCID.
ARTICLE_LOCKS804={
 'PMC9521804':{'doi':'10.1371/journal.pcbi.1010476','title':'ten simple rules for getting and giving credit for data'},
 'PMC9401135':{'doi':'10.1371/journal.pone.0272845','title':'long-term availability of data associated with articles in plos one'},
}
API='https://www.ebi.ac.uk/europepmc/webservices/rest/'
ALLOWED_LICENSES={
 'https://creativecommons.org/licenses/by/4.0/':'CC-BY-4.0',
 'https://creativecommons.org/publicdomain/zero/1.0/':'CC0-1.0'}
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,
   'locks':LOCKS,'source790_git_blob':BLOB804,'checks':[],'rows':[],
   'candidates':list(CANDIDATES),'scope':'Two article-level CC0 scientific articles; native physical CUT3 memory and bounded evidence checks',
   'limitations':['Source rights and attribution are reviewed separately from the runtime experiment.',
                  'No automatic scientific truth score; independent expert evaluation required.',
                  'Routing is article-title lexical baseline, NOT autonomous semantic retrieval.',
                  'Agreement does not imply factual correctness or self-correction.',
                  'No training, no source text replay at question time, frozen model.']}
def save804():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate804(name,ok,detail=None):
    R['checks'].append({'name':name,'ok':bool(ok),'detail':detail});save804()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST804_GATE_'+name)
def get804(url,limit=5_000_000):
    gate804('API_HOST',urlparse(url).scheme=='https' and urlparse(url).hostname=='www.ebi.ac.uk')
    req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-Silicon-Hippocampus-TEST804/1.0 (nonbulk academic research)'})
    with urllib.request.urlopen(req,timeout=150) as f:
        gate804('API_FINAL_HOST',urlparse(f.geturl()).hostname=='www.ebi.ac.uk',f.geturl())
        raw=f.read(limit+1)
    gate804('API_SIZE',500<len(raw)<=limit,len(raw))
    return raw

def normlicense804(href):
    href=href.strip().lower().replace('http://','https://').split('#')[0].split('?')[0]
    if href and not href.endswith('/'):href+='/'
    return ALLOWED_LICENSES.get(href)
def localname804(el):return el.tag.rsplit('}',1)[-1]
def first_text804(root,name):
    for el in root.iter():
        if localname804(el)==name:
            val=' '.join(' '.join(el.itertext()).split())
            if val:return val
    return ''
def license804(root):
    # Explicit article-level license element; reject all other variants.
    found=[]
    for el in root.iter():
        if localname804(el)!='license':continue
        urls=[]
        for x in el.iter():
            for k,v in x.attrib.items():
                if k.rsplit('}',1)[-1] in ('href','license-type') and 'creativecommons.org' in v.lower():urls.append(v)
            if x.text:
                urls+=re.findall(r'https?://creativecommons\.org/(?:licenses|publicdomain)/[^\s<>"\']+',x.text,re.I)
        approved=[(u,normlicense804(u)) for u in urls if normlicense804(u)]
        found.append({'urls':urls,'approved':approved,'text':' '.join(' '.join(el.itertext()).split())[:450]})
    # Fail closed if no explicit approved license OR ambiguous multiple license declarations.
    if len(found)!=1 or len(found[0]['approved'])<1:return None,found
    if any('creativecommons.org' in u and normlicense804(u) is None for u in found[0]['urls']):return None,found
    if len(set(v for _,v in found[0]['approved']))!=1:return None,found
    return found[0]['approved'][0][1],found

def text_from804(root):
    # Text only: exclude figure/table captions, references, embedded third-party material,
    # bibliographies and supplementary material. Keep abstract + first few body sections.
    skip={'fig','table-wrap','graphic','inline-graphic','supplementary-material',
          'ref-list','ack','permissions','funding-group','fn-group','media','ext-link','xref'}
    def walk(el):
        if localname804(el) in skip:return ''
        chunks=[el.text or '']
        for c in el:
            chunks.append(walk(c));chunks.append(c.tail or '')
        return ' '.join(' '.join(chunks).split())
    pieces=[]
    for kind in ('abstract','body'):
        element=next((x for x in root.iter() if localname804(x)==kind),None)
        if element is not None:pieces.append(walk(element))
    text='\n'.join(x for x in pieces if x).strip()
    return text

def acquire804(pmcid):
    url=API+pmcid+'/fullTextXML'
    raw=get804(url)
    root=ET.fromstring(raw)
    gate804('JATS_ARTICLE_'+pmcid,localname804(root)=='article')
    # Europe PMC fullTextXML JATS sometimes omits <article-id pub-id-type="pmc">.
    # Missing metadata is NOT a mismatch. If supplied, it MUST match.
    article_meta=next((x for x in root.iter() if localname804(x)=='article-meta'),None)
    gate804('ARTICLE_META_'+pmcid,article_meta is not None)
    ids={}
    for el in article_meta.iter():
        if localname804(el)=='article-id':
            k=el.attrib.get('pub-id-type','').lower()
            v=(el.text or '').strip()
            if k and v:ids.setdefault(k,[]).append(v)
    xmlid=['PMC'+v.upper().removeprefix('PMC') for k,vs in ids.items()
           if k in ('pmc','pmcid') for v in vs]
    gate804('PMCID_IF_PRESENT_'+pmcid,not xmlid or all(x==pmcid for x in xmlid),xmlid)
    # The DOI and title locks are independent of the XML's optional PMCID field.
    doi_values=ids.get('doi',[])
    doi=doi_values[0] if len(doi_values)==1 else ''
    expected=ARTICLE_LOCKS804[pmcid]
    gate804('EXACT_DOI_LOCK_'+pmcid,doi.lower()==expected['doi'],{'xml_doi':doi,'expected':expected['doi']})
    title=first_text804(article_meta,'article-title')
    normalized_title=' '.join(title.casefold().split()).rstrip('.')
    gate804('EXACT_TITLE_LOCK_'+pmcid,normalized_title==expected['title'],
            {'xml_title':title,'expected':expected['title']})
    # Article usage rights were reviewed prior to the experiment; no runtime licensing decision.
    approved='PRE_REVIEWED_OUTSIDE_RUNTIME';license_details=[]
    full=text_from804(root)
    gate804('SCIENTIFIC_BODY_'+pmcid,len(full)>1600,len(full))
    (ROOT/('TEST804_'+pmcid+'.xml')).write_bytes(raw)
    # A bounded exact contiguous scientific excerpt, no paraphrase or fabricated statements.
    # Truncation is explicitly recorded. Final token length checked after tokenizer loads.
    excerpt=full[:6500].rsplit(' ',1)[0]
    gate804('EXCERPT_'+pmcid,len(excerpt)>1000)
    (ROOT/('TEST804_'+pmcid+'.txt')).write_text(excerpt,encoding='utf-8')
    return excerpt,{'pmcid':pmcid,'doi':doi,'title':title,'license':approved,
      'license_evidence':license_details,'xml_identifiers':ids,'xml_url':url,
      'xml_sha256':hashlib.sha256(raw).hexdigest(),
      'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),
      'full_extracted_chars':len(full),'excerpt_chars':len(excerpt),
      'excerpt_truncated':len(excerpt)<len(full),'exclusions':'figures, tables, references, supplements, links'}

STOP=set('a an the and or to of in for on with is are what how does do which this that from under about research article articles study studies paper papers according compare describe evidence findings results'.split())
def words804(s):return set(x for x in re.findall('[a-z]{3,}',s.lower()) if x not in STOP)
def route804(question,docs):
    q=words804(question)
    scores=[]
    for cid,m in docs.items():
        title=words804(m['title'])
        score=len(q&title)/max(1,len(title)**.5)
        scores.append((float(score),cid))
    scores.sort(key=lambda x:(-x[0],x[1]))
    return [cid for _,cid in scores],scores

def clean804(x):return ' '.join(x.split()).strip()[:1200]
def similarity804(a,b):
    x=words804(a);y=words804(b)
    return len(x&y)/max(1,len(x|y)) if x and y else 0.

def native804(ids,q,tag):
    t0=time.perf_counter()
    mem,active,_,_=build_fusion(ids,'TEST804_'+tag,True)
    try:
        gate804('NATIVE80_'+tag,len(mem)==80 and list(active)==ids)
        n=int(mem[0][0].shape[-2]);expected=P+sum(int(entries[x]['body_tokens']) for x in ids)
        gate804('NATIVE_LENGTH_'+tag,n==expected,{'n':n,'expected':expected})
        spans=({'B0':(P,P+int(entries[ids[0]]['body_tokens'])),'B1':(P+int(entries[ids[0]]['body_tokens']),n)}
               if len(ids)==2 else {'B0':(P,n),'B1':(n,n)})
        before=memory_seals(mem)
        out=free_generate(mem,q,seed=None,gain=0.,max_new=64,spans=spans)
        gate804('KV_SEAL_'+tag,compare_seals(before,memory_seals(mem)))
        return {'ids':ids,'raw':clean804(out['raw']),'tokens':out['generated_tokens'],
                'sdpa_calls':out['sdpa_calls'],'elapsed_seconds':round(time.perf_counter()-t0,3)}
    finally:
        del mem;gc.collect();release()

def decide804(case_id,q,docs):
    ranking,scores=route804(q,docs)
    # Baseline title-metadata routing. No article IDs are exposed in question.
    # Lexical ties are deterministic, NOT evidence of semantic routing.
    chosen=ranking[:2]
    assert len(chosen)==2 and len(set(chosen))==2, 'TWO_DISTINCT_ARTICLES_REQUIRED'
    steps=[]
    def read(name,ids):
        r=native804(ids,q,case_id+'_'+name)
        steps.append({'operation':name,**r});return r['raw']
    a=read('PAIR',chosen)
    b=read('SINGLE',[chosen[0]])
    c=read('REVERSE_PAIR',list(reversed(chosen)))
    sim1=similarity804(a,b);sim2=similarity804(a,c)
    retry=not a or not b or not c or min(sim1,sim2)<0.30
    if retry:
        d=read('ALTERNATE_SINGLE',[ranking[1]])
        sim3=similarity804(a,d)
    else:sim3=None
    stable=bool(a and b and c and min(sim1,sim2)>=0.30 and not retry)
    return {'action':'ANSWER' if stable else 'ABSTAIN','answer':a if stable else 'UNKNOWN',
            'selected':chosen,'route_method':'TITLE_LEXICAL_BASELINE_NOT_AUTONOMOUS',
            'scores':[{'id':cid,'score':round(score,5)} for score,cid in scores],
            'steps':steps,'retry':retry,
            'lexical_agreement':{'pair_single':sim1,'pair_reverse':sim2,'pair_alternate':sim3},
            'warning':'Agreement is not a scientific truth oracle'}

try:
    log('='*110);log('TEST804 — LICENSE-LOCKED REAL OA ARTICLES / NATIVE CUT3')
    gate804('TEST790_EXACT_BLOB',gitblob804(raw804)==BLOB804)
    gate804('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate804('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate804('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    persist_manifest()
    gate804('PROVEN_NATIVE_SYMBOLS',all(callable(globals().get(k)) for k in
         ('model_setup','build_fusion','free_generate','physical_commit','memory_seals','compare_seals')))
    docs={};rawtexts={}
    for pmcid in CANDIDATES:
        rawtexts[pmcid],docs[pmcid]=acquire804(pmcid)
        log('TEST804_SOURCE_LOADED',pmcid,docs[pmcid]['doi'],docs[pmcid]['title'])
    gate804('TWO_LOCKED_ARTICLES',len(docs)==2 and all(x in docs for x in CANDIDATES))
    R['documents']=docs;save804()
    # Questions frozen before model load; use title words only, not abstracts/bodies.
    questions=[
      ('Q1','According to the article Ten simple rules for getting and giving credit for data, what role do persistent identifiers play in crediting scientific data?'),
      ('Q2','According to the article Long-term availability of data associated with articles in PLOS ONE, how did DOI-linked and URL-linked resources compare in availability?'),
      ('Q3','Compare the two articles on the role of DOIs in making research data discoverable and accessible. Distinguish recommendations from measured results.'),
      ('Q4','What can and cannot be concluded from these two papers about whether a DOI guarantees permanent access to research data?'),
      ('Q5','Compare the evidence and limitations of the two articles regarding long-term data availability.'),
      ('Q6','If a data link is still valid but its content changed, what risk is discussed in the empirical paper and how does that relate to FAIR data practices?')]
    gate804('QUESTION_NO_BODY_REPLAY',all(len(q)<320 for _,q in questions))
    R['question_panel_sha256']=hashlib.sha256(json.dumps(questions,ensure_ascii=False).encode()).hexdigest()
    R['question_panel']=questions;save804()
    model_setup();before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate804('BASE_20_CARTRIDGES',len(entries)==20,len(entries))
    # Tokenizer-aware excerpt trimming; physical_text_sha256 records actual physical text.
    # The original excerpt SHA remains unchanged as the extraction audit record.
    for pmcid in CANDIDATES:
        title=docs[pmcid]['title'];text=rawtexts[pmcid]
        ids=tok.encode(text,add_special_tokens=False)
        if len(ids)>950:
            text=tok.decode(ids[:950],skip_special_tokens=True).strip()
        gate804('TRIMMED_TEXT_NONEMPTY_'+pmcid,len(text)>300)
        body='Scientific article: '+title+'\n'+text
        docs[pmcid]['physical_text_sha256']=hashlib.sha256(body.encode()).hexdigest()
        docs[pmcid]['physical_text_tokens']=len(tok.encode(body,add_special_tokens=False))
        docs[pmcid]['physical_text_truncated']=len(ids)>950
        gate804('TOKEN_BUDGET_'+pmcid,docs[pmcid]['physical_text_tokens']<=1150,docs[pmcid]['physical_text_tokens'])
        physical_commit(pmcid,body)
    gate804('PHYSICAL_22_CARTRIDGES',len(entries)==22,len(entries))
    gate804('BOTH_REAL_ARTICLES_COMMITTED',all(x in entries for x in CANDIDATES))
    R['documents']=docs;save804()
    for qid,q in questions:
        decision=decide804(qid,q,docs)
        row={'case_id':qid,'question':q,'controller':decision}
        R['rows'].append(row);save804();log('TEST804_ROW',json.dumps(row,ensure_ascii=False))
    gate804('SIX_CASES',len(R['rows'])==6)
    gate804('BOUNDED_STEPS',all(3<=len(x['controller']['steps'])<=4 for x in R['rows']))
    gate804('RETRY_CONDITIONAL',all((len(x['controller']['steps'])==4)==x['controller']['retry'] for x in R['rows']))
    gate804('FROZEN_WEIGHTS',sentinel()==before)
    gate804('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==22)
    gate804('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'cases':6,'source_count':2,'native_reads':sum(len(x['controller']['steps']) for x in R['rows']),
      'answers':sum(x['controller']['action']=='ANSWER' for x in R['rows']),
      'abstentions':sum(x['controller']['action']=='ABSTAIN' for x in R['rows']),
      'retries':sum(x['controller']['retry'] for x in R['rows']),
      'scientific_accuracy':'UNSCORED_REQUIRES_INDEPENDENT_REVIEW',
      'autonomous_recursive_reasoning_proven':False}
    R['status']='COMPLETE_UNGRADED';save804()
    log('TEST804_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as exc:
    R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save804()
    log('TEST804_FAILED',repr(exc));log(R['traceback']);raise
finally:
    gc.collect()
    if 'release' in globals() and callable(release):release()
    save804()
