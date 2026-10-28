# AKBASCORE SILICON HIPPOCAMPUS — TEST807
# SOURCE-BLIND H3 NUMERICAL ROUTING / CAUSAL EVIDENCE / CONCISE ANSWERS / PHYSICAL CUT3 CARTRIDGES
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB (40GB NOT SUPPORTED)
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# TEST807: H3 routing and paraphrase stability measured blind; no gold answer in inference; no claim of general reasoning.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

# Fail fast BEFORE downloading locked source trees or 72B model weights.
# Do not weaken the TEST779 hardware contract.
def preflight_gpu807():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('TEST807_REQUIRES_TORCH_AND_A100_80GB_RUNTIME') from exc
    if not torch.cuda.is_available():
        raise RuntimeError('TEST807_NO_CUDA_GPU: Select a Colab A100 80GB runtime.')
    count=torch.cuda.device_count()
    if count!=1:
        raise RuntimeError(f'TEST807_EXPECTS_ONE_GPU: detected={count}')
    info=torch.cuda.get_device_properties(0)
    name=info.name; gib=info.total_memory/(1024**3)
    print('TEST807_GPU_PREFLIGHT',{'name':name,'vram_gib':round(gib,2),'gpu_count':count},flush=True)
    if 'A100' not in name or info.total_memory < 70*2**30:
        raise RuntimeError(
            f'TEST807_A100_80GB_REQUIRED: detected {name}, {gib:.2f} GiB. '
            'Colab assigned A100 40GB. This 72B locked engine needs A100 80GB; '
            'restart the runtime and execute this cell again. '
            'The locked TEST779 safety gate is intentionally unchanged.')
    free,total=torch.cuda.mem_get_info(0)
    print('TEST807_GPU_FREE_GIB',round(free/2**30,2),flush=True)
    if free < 40*2**30:
        raise RuntimeError(
            f'TEST807_INSUFFICIENT_FREE_VRAM: {free/2**30:.2f} GiB free; '
            'restart the runtime to clear old models.')
preflight_gpu807()

SOURCE807='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB807='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob807(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE807,headers={'User-Agent':'AKBASCORE-TEST807'}),timeout=180) as response:
    raw807=response.read()
assert len(raw807)<100000 and gitblob807(raw807)==BLOB807,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob807(raw807))
tree807=ast.parse(raw807.decode('utf-8'),filename='790.py')
cut807=next((i for i,n in enumerate(tree807.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut807 is not None and cut807==len(tree807.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree807.body[:cut807],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
assert torch.cuda.is_available() and torch.cuda.device_count()==1
assert 'A100' in torch.cuda.get_device_properties(0).name
# TEST807 — TWO VERIFIED RESEARCH ARTICLES / NATIVE CUT3
# Selection: two specific PLOS articles with publisher CC0 declarations.
# PMCID field in JATS is OPTIONAL; DOI+title are REQUIRED and independently locked.
# Rights review is completed outside this experiment. No runtime license gate.
# This is a bounded H3-routing and evidence-controller experiment, not the final demo.
import re,os,datetime,xml.etree.ElementTree as ET
from urllib.parse import urlparse

TEST='807';OUT=ROOT/'TEST807_results.json';LOG=ROOT/'TEST807.log';MANIFEST=ROOT/'TEST807_manifest.json'
LOG.write_text('',encoding='utf-8')
CANDIDATES=('PMC9521804','PMC9401135')
# Expected bibliographic identifiers; independent source review required before release.
# XML DOI and article title MUST match these locks even if XML omits its PMCID.
ARTICLE_LOCKS807={
 'PMC9521804':{'doi':'10.1371/journal.pcbi.1010476','title':'ten simple rules for getting and giving credit for data'},
 'PMC9401135':{'doi':'10.1371/journal.pone.0272845','title':'long-term availability of data associated with articles in plos one'},
}
API='https://www.ebi.ac.uk/europepmc/webservices/rest/'
ALLOWED_LICENSES={
 'https://creativecommons.org/licenses/by/4.0/':'CC-BY-4.0',
 'https://creativecommons.org/publicdomain/zero/1.0/':'CC0-1.0'}
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,
   'locks':LOCKS,'source790_git_blob':BLOB807,'checks':[],'rows':[],
   'candidates':list(CANDIDATES),'scope':'TEST807: source-blind native H3 routing, physical evidence controls and concise response audit',
   'limitations':['Source rights and attribution are reviewed separately from the runtime experiment.',
                  'No automatic scientific truth score; evidence-grounding audit is not a truth oracle.',
                  'Native H3 numerical ranking is evaluated on two physical source cartridges only; it is not general autonomous retrieval.',
                  'Agreement does not imply factual correctness or self-correction.',
                  'No training, no source text replay at question time, frozen model.']}
def save807():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate807(name,ok,detail=None):
    R['checks'].append({'name':name,'ok':bool(ok),'detail':detail});save807()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST807_GATE_'+name)
def get807(url,limit=5_000_000):
    gate807('API_HOST',urlparse(url).scheme=='https' and urlparse(url).hostname=='www.ebi.ac.uk')
    req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-Silicon-Hippocampus-TEST807/1.0 (nonbulk academic research)'})
    with urllib.request.urlopen(req,timeout=150) as f:
        gate807('API_FINAL_HOST',urlparse(f.geturl()).hostname=='www.ebi.ac.uk',f.geturl())
        raw=f.read(limit+1)
    gate807('API_SIZE',500<len(raw)<=limit,len(raw))
    return raw

def normlicense807(href):
    href=href.strip().lower().replace('http://','https://').split('#')[0].split('?')[0]
    if href and not href.endswith('/'):href+='/'
    return ALLOWED_LICENSES.get(href)
def localname807(el):return el.tag.rsplit('}',1)[-1]
def first_text807(root,name):
    for el in root.iter():
        if localname807(el)==name:
            val=' '.join(' '.join(el.itertext()).split())
            if val:return val
    return ''
def license807(root):
    # Explicit article-level license element; reject all other variants.
    found=[]
    for el in root.iter():
        if localname807(el)!='license':continue
        urls=[]
        for x in el.iter():
            for k,v in x.attrib.items():
                if k.rsplit('}',1)[-1] in ('href','license-type') and 'creativecommons.org' in v.lower():urls.append(v)
            if x.text:
                urls+=re.findall(r'https?://creativecommons\.org/(?:licenses|publicdomain)/[^\s<>"\']+',x.text,re.I)
        approved=[(u,normlicense807(u)) for u in urls if normlicense807(u)]
        found.append({'urls':urls,'approved':approved,'text':' '.join(' '.join(el.itertext()).split())[:450]})
    # Fail closed if no explicit approved license OR ambiguous multiple license declarations.
    if len(found)!=1 or len(found[0]['approved'])<1:return None,found
    if any('creativecommons.org' in u and normlicense807(u) is None for u in found[0]['urls']):return None,found
    if len(set(v for _,v in found[0]['approved']))!=1:return None,found
    return found[0]['approved'][0][1],found

def text_from807(root):
    # Text only: exclude figure/table captions, references, embedded third-party material,
    # bibliographies and supplementary material. Keep abstract + first few body sections.
    skip={'fig','table-wrap','graphic','inline-graphic','supplementary-material',
          'ref-list','ack','permissions','funding-group','fn-group','media','ext-link','xref'}
    def walk(el):
        if localname807(el) in skip:return ''
        chunks=[el.text or '']
        for c in el:
            chunks.append(walk(c));chunks.append(c.tail or '')
        return ' '.join(' '.join(chunks).split())
    pieces=[]
    for kind in ('abstract','body'):
        element=next((x for x in root.iter() if localname807(x)==kind),None)
        if element is not None:pieces.append(walk(element))
    text='\n'.join(x for x in pieces if x).strip()
    return text

def acquire807(pmcid):
    url=API+pmcid+'/fullTextXML'
    raw=get807(url)
    root=ET.fromstring(raw)
    gate807('JATS_ARTICLE_'+pmcid,localname807(root)=='article')
    # Europe PMC fullTextXML JATS sometimes omits <article-id pub-id-type="pmc">.
    # Missing metadata is NOT a mismatch. If supplied, it MUST match.
    article_meta=next((x for x in root.iter() if localname807(x)=='article-meta'),None)
    gate807('ARTICLE_META_'+pmcid,article_meta is not None)
    ids={}
    for el in article_meta.iter():
        if localname807(el)=='article-id':
            k=el.attrib.get('pub-id-type','').lower()
            v=(el.text or '').strip()
            if k and v:ids.setdefault(k,[]).append(v)
    xmlid=['PMC'+v.upper().removeprefix('PMC') for k,vs in ids.items()
           if k in ('pmc','pmcid') for v in vs]
    gate807('PMCID_IF_PRESENT_'+pmcid,not xmlid or all(x==pmcid for x in xmlid),xmlid)
    # The DOI and title locks are independent of the XML's optional PMCID field.
    doi_values=ids.get('doi',[])
    doi=doi_values[0] if len(doi_values)==1 else ''
    expected=ARTICLE_LOCKS807[pmcid]
    gate807('EXACT_DOI_LOCK_'+pmcid,doi.lower()==expected['doi'],{'xml_doi':doi,'expected':expected['doi']})
    title=first_text807(article_meta,'article-title')
    normalized_title=' '.join(title.casefold().split()).rstrip('.')
    gate807('EXACT_TITLE_LOCK_'+pmcid,normalized_title==expected['title'],
            {'xml_title':title,'expected':expected['title']})
    # Article usage rights were reviewed prior to the experiment; no runtime licensing decision.
    approved='PRE_REVIEWED_OUTSIDE_RUNTIME';license_details=[]
    full=text_from807(root)
    gate807('SCIENTIFIC_BODY_'+pmcid,len(full)>1600,len(full))
    (ROOT/('TEST807_'+pmcid+'.xml')).write_bytes(raw)
    # A bounded exact contiguous scientific excerpt, no paraphrase or fabricated statements.
    # Truncation is explicitly recorded. Final token length checked after tokenizer loads.
    excerpt=full[:6500].rsplit(' ',1)[0]
    gate807('EXCERPT_'+pmcid,len(excerpt)>1000)
    (ROOT/('TEST807_'+pmcid+'.txt')).write_text(excerpt,encoding='utf-8')
    return excerpt,{'pmcid':pmcid,'doi':doi,'title':title,'license':approved,
      'license_evidence':license_details,'xml_identifiers':ids,'xml_url':url,
      'xml_sha256':hashlib.sha256(raw).hexdigest(),
      'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),
      'full_extracted_chars':len(full),'excerpt_chars':len(excerpt),
      'excerpt_truncated':len(excerpt)<len(full),'exclusions':'figures, tables, references, supplements, links'}

STOP=set('a an the and or to of in for on with is are what how does do which this that from under about research article articles study studies paper papers according compare describe evidence findings results'.split())
def words807(s):return set(x for x in re.findall('[a-z]{3,}',s.lower()) if x not in STOP)

def build_real_bank807():
    # Same proven TEST757 H3 representation and TEST721/757 numeric ranking.
    # No title, DOI, PMCID, correct-source label, or answer is supplied to the selector.
    bank={}
    for cid in CANDIDATES:
        cp=safe_load(entries[cid])  # verified physical SSD reload
        try:
            x=cp['h'][0,P:,:].float().cpu().numpy()
            gate807('NONEMPTY_H3_'+cid,x.ndim==2 and x.shape[0]>8 and x.shape[1]==8192,x.shape)
            ix=np.linspace(0,len(x)-1,min(96,len(x)),dtype=np.int64)
            bank[cid]=normalized(x[ix]).T.copy()
        finally:
            del cp
    return bank

def route807(question,bank):
    # Native CUT3 question capture (TEST757), then native H3 numerical rank.
    # This path does NOT inspect article titles or ground truth.
    ordered,raw_scores=numeric_rank(question,bank)
    gate807('H3_RANK_TWO',len(ordered)==2 and set(ordered)==set(CANDIDATES))
    return ordered,[(float(raw_scores[cid]),cid) for cid in ordered]

def clean807(x):return ' '.join(x.split()).strip()
def similarity807(a,b):
    x=words807(a);y=words807(b)
    return len(x&y)/max(1,len(x|y)) if x and y else 0.

def native807(ids,q,tag,max_new=128):
    # The locked TEST779 free_generate is used unchanged. 128-token budget is
    # an upper bound, not a guarantee of EOS or a complete sentence.
    t0=time.perf_counter()
    mem,active,_,_=build_fusion(ids,'TEST807_'+tag,True)
    try:
        gate807('NATIVE80_'+tag,len(mem)==80 and list(active)==ids)
        n=int(mem[0][0].shape[-2]);expected=P+sum(int(entries[x]['body_tokens']) for x in ids)
        gate807('NATIVE_LENGTH_'+tag,n==expected,{'n':n,'expected':expected})
        spans=({'B0':(P,P+int(entries[ids[0]]['body_tokens'])),'B1':(P+int(entries[ids[0]]['body_tokens']),n)}
               if len(ids)==2 else {'B0':(P,n),'B1':(n,n)})
        before=memory_seals(mem)
        out=free_generate(mem,('Answer the question using only the physical scientific document memory. Give at most two concise factual sentences (maximum 45 words). If unsupported, answer UNKNOWN.\nQuestion: '+q),seed=None,gain=0.,max_new=max_new,spans=spans)
        gate807('KV_SEAL_'+tag,compare_seals(before,memory_seals(mem)))
        raw=clean807(out['raw'])
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

def decide807(case_id,q,bank):
    ranking,scores=route807(q,bank)
    chosen=ranking[:2]
    assert len(chosen)==2 and len(set(chosen))==2
    steps=[]
    def read(name,ids):
        r=native807(ids,q,case_id+'_'+name)
        steps.append({'operation':name,**r});return r
    # Physical causal controls: H3-ranked pair, H3 top-1 single, reverse pair.
    pair=read('PAIR',chosen)
    single=read('SINGLE',[chosen[0]])
    reverse=read('REVERSE_PAIR',list(reversed(chosen)))
    sim1=similarity807(pair['raw'],single['raw'])
    sim2=similarity807(pair['raw'],reverse['raw'])
    # Conditional retry uses observable disagreement, not expected answers.
    retry=any(x['possible_truncation'] or not x['raw'] for x in (pair,single,reverse)) or min(sim1,sim2)<.20
    alternate=None
    if retry:alternate=read('ALTERNATE_SINGLE',[chosen[1]])
    complete=all(x['raw'] and not x['possible_truncation'] for x in (pair,single,reverse))
    # Sentence-end is an additional heuristic; not a semantic truth criterion.
    stable=bool(complete and pair['sentence_end'] and min(sim1,sim2)>=.20 and not pair['raw'].upper().startswith('UNKNOWN'))
    return {'action':'ANSWER' if stable else 'ABSTAIN',
            'answer':pair['raw'] if stable else 'UNKNOWN',
            'selected':chosen,'route_method':'NATIVE_CUT3_H3_NUMERICAL_RANK_TEST757_TWO_SOURCES',
            'scores':[{'id':cid,'score':round(score,5)} for score,cid in scores],
            'steps':steps,'retry':retry,'complete_under_budget':complete,'pair_sentence_end':pair['sentence_end'],
            'all_sentence_end':all(x['sentence_end'] for x in (pair,single,reverse)),
            'lexical_agreement':{'pair_single':sim1,'pair_reverse':sim2,
                                 'pair_alternate':similarity807(pair['raw'],alternate['raw']) if alternate else None},
            'warning':'Lexical agreement and sentence ending do not prove scientific accuracy.'}

try:
    log('='*110);log('TEST807 — REAL ARTICLES / COMPLETION AUDIT / NATIVE CUT3')
    gate807('TEST790_EXACT_BLOB',gitblob807(raw807)==BLOB807)
    gate807('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate807('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate807('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    persist_manifest()
    gate807('PROVEN_NATIVE_SYMBOLS',all(callable(globals().get(k)) for k in
         ('model_setup','build_fusion','free_generate','physical_commit','memory_seals','compare_seals')))
    docs={};rawtexts={}
    for pmcid in CANDIDATES:
        rawtexts[pmcid],docs[pmcid]=acquire807(pmcid)
        log('TEST807_SOURCE_LOADED',pmcid,docs[pmcid]['doi'],docs[pmcid]['title'])
    gate807('TWO_LOCKED_ARTICLES',len(docs)==2 and set(docs)==set(ARTICLE_LOCKS807) and len(set(CANDIDATES))==2)
    R['documents']=docs;save807()
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
    # Offline routing evaluation only. NEVER passed to route807 or free_generate.
    expected_sources={'Q1':['PMC9521804'],'Q2':['PMC9401135'],
      'Q3':['PMC9521804','PMC9401135'],'Q4':['PMC9401135','PMC9521804'],
      'Q5':['PMC9401135'],'Q6':['PMC9401135'],
      'Q7':['PMC9521804'],'Q8':['PMC9401135']}
    gate807('QUESTION_NO_BODY_REPLAY',all(len(q)<320 and not any(cid in q for cid in CANDIDATES) and not any(d['title'].lower() in q.lower() for d in ARTICLE_LOCKS807.values()) for _,q in questions))
    R['question_panel_sha256']=hashlib.sha256(json.dumps(questions,ensure_ascii=False).encode()).hexdigest()
    R['question_panel']=questions;save807()
    model_setup();before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate807('BASE_20_CARTRIDGES',len(entries)==20,len(entries))
    # Tokenizer-aware excerpt trimming; physical_text_sha256 records actual physical text.
    # The original excerpt SHA remains unchanged as the extraction audit record.
    for pmcid in CANDIDATES:
        title=docs[pmcid]['title'];text=rawtexts[pmcid]
        ids=tok.encode(text,add_special_tokens=False)
        if len(ids)>950:
            text=tok.decode(ids[:950],skip_special_tokens=True).strip()
        gate807('TRIMMED_TEXT_NONEMPTY_'+pmcid,len(text)>300)
        body='Scientific article: '+title+'\n'+text
        docs[pmcid]['physical_text_sha256']=hashlib.sha256(body.encode()).hexdigest()
        docs[pmcid]['physical_text_tokens']=len(tok.encode(body,add_special_tokens=False))
        docs[pmcid]['physical_text_truncated']=len(ids)>950
        gate807('TOKEN_BUDGET_'+pmcid,docs[pmcid]['physical_text_tokens']<=1150,docs[pmcid]['physical_text_tokens'])
        physical_commit(pmcid,body)
    gate807('PHYSICAL_22_CARTRIDGES',len(entries)==22,len(entries))
    gate807('BOTH_REAL_ARTICLES_COMMITTED',all(x in entries for x in CANDIDATES))
    R['documents']=docs;save807()
    bank807=build_real_bank807()
    gate807('NUMERICAL_H3_BANK',len(bank807)==2 and all(x.shape[0]==8192 for x in bank807.values()))
    # TEST807 NEW: sealed question-paraphrase routing controls. These are NOT
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
    gate807('PARAPHRASE_PANEL_LOCK',set(paraphrases)==set(x[0] for x in questions))
    R['paraphrase_panel_sha256']=hashlib.sha256(json.dumps(paraphrases,sort_keys=True).encode()).hexdigest()
    R['routing_robustness']=[];save807()
    for qid,q in questions:
        # Both rankings are obtained with the exact locked TEST757 CUT3/H3 scorer.
        original_order,original_scores=route807(q,bank807)
        paraphrase_order,paraphrase_scores=route807(paraphrases[qid],bank807)
        relevant=expected_sources[qid]  # offline evaluation only
        rr={'case_id':qid,'original_top1':original_order[0],
            'paraphrase_top1':paraphrase_order[0],
            'same_top1':original_order[0]==paraphrase_order[0],
            'original_top1_relevant':original_order[0] in relevant,
            'paraphrase_top1_relevant':paraphrase_order[0] in relevant,
            'original_scores':{cid:round(float(v),6) for v,cid in original_scores},
            'paraphrase_scores':{cid:round(float(v),6) for v,cid in paraphrase_scores}}
        R['routing_robustness'].append(rr);save807()
        log('TEST807_ROUTE_PARAPHRASE',json.dumps(rr,ensure_ascii=False))
    gate807('PARAPHRASE_EIGHT',len(R['routing_robustness'])==8)
    for qid,q in questions:
        decision=decide807(qid,q,bank807)
        offline=expected_sources[qid]
        row={'case_id':qid,'question':q,'controller':decision,
             'offline_routing_eval':{'relevant_sources':offline,
               'top1_relevant':decision['selected'][0] in offline,
               'top2_recall':len(set(decision['selected'])&set(offline))/len(offline)}}
        R['rows'].append(row);save807();log('TEST807_ROW',json.dumps(row,ensure_ascii=False))
    gate807('EIGHT_CASES',len(R['rows'])==8)
    gate807('BOUNDED_STEPS',all(3<=len(x['controller']['steps'])<=4 for x in R['rows']))
    gate807('RETRY_CONDITIONAL',all((len(x['controller']['steps'])==4)==x['controller']['retry'] for x in R['rows']))
    gate807('FROZEN_WEIGHTS',sentinel()==before)
    gate807('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==22)
    gate807('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'cases':8,'source_count':2,'native_reads':sum(len(x['controller']['steps']) for x in R['rows']),
      'answers':sum(x['controller']['action']=='ANSWER' for x in R['rows']),
      'abstentions':sum(x['controller']['action']=='ABSTAIN' for x in R['rows']),
      'retries':sum(x['controller']['retry'] for x in R['rows']),
      'possible_truncated_pair_answers':sum(x['controller']['steps'][0]['possible_truncation'] for x in R['rows']),
      'complete_under_budget':sum(x['controller']['complete_under_budget'] for x in R['rows']),
      'pair_sentence_end':sum(x['controller']['steps'][0]['sentence_end'] for x in R['rows']),
      'routing_top1_relevant':sum(x['offline_routing_eval']['top1_relevant'] for x in R['rows']),
      'routing_top1_total':len(R['rows']),
      'paraphrase_top1_agreement':sum(x['same_top1'] for x in R['routing_robustness']),
      'paraphrase_top1_relevant':sum(x['paraphrase_top1_relevant'] for x in R['routing_robustness']),
      'routing_top2_recall_mean':round(sum(x['offline_routing_eval']['top2_recall'] for x in R['rows'])/len(R['rows']),4),
      'scientific_accuracy':'UNSCORED_REQUIRES_INDEPENDENT_REVIEW',
      'autonomous_recursive_reasoning_proven':False}
    R['status']='COMPLETE_UNGRADED';save807()
    log('TEST807_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as exc:
    R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save807()
    log('TEST807_FAILED',repr(exc));log(R['traceback']);raise
finally:
    gc.collect()
    if 'release' in globals() and callable(release):release()
    save807()
