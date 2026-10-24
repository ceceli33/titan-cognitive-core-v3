# AKBASCORE SILICON HIPPOCAMPUS — TEST771
# Locked GPU-proven TEST767 backbone; same sealed 20-card panel; frozen 72B native CUT3.
# ONE Colab cell. Existing engine definitions are imported VERBATIM by locked Git blobs.
# No training, no source text in QA prompts, no forward hooks, no Gradio.
# TEST771 tests a bounded CUT3 hidden-state feedback perturbation against the TEST768 resident baseline.
# Research probe only: no learned controller, no proof of autonomous retrieval, synthesis or stopping.
# Static syntax verified; NOT GPU executed by author.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,json,ast,time,random,re,gc,traceback,types,datetime
from pathlib import Path
from datetime import timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for mod,pkg in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('numpy','numpy')]:
    if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,bitsandbytes,numpy as np
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
if not torch.cuda.is_available() or torch.cuda.device_count()!=1:raise RuntimeError('ONE_CUDA_GPU_REQUIRED')
GPU_INFO=torch.cuda.get_device_properties(0)
if 'A100' not in GPU_INFO.name or GPU_INFO.total_memory<70*2**30:raise RuntimeError('A100_80GB_REQUIRED')
TEST='771';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
NL,H,QH,KVH,HD=EXPECTED;DTYPE=torch.bfloat16;DEV=torch.device('cuda:0')
CHUNK=128;GPU_RESERVE_GIB=9.0;MAX_NEW=48;MAX_FUSED_TOKENS=3500
NUM_CHAINS=4;SAMPLE_PER_PIECE=512;ROUTE_K=3;MODEL_SEED=7662026
STEPS=('works_at','collaborates_with','archives_in');KINDS=('PERSON','WORK','TEAM','VAULT')
REPO='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCKS={'709.py':'6c9f8cbb1eeed848d45133d73f0d7676b68e9125',
       '730.py':'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
       '757.py':'3d88bf8638390995858f23391f1e043faa586835',
       '764.py':'99acb97cde2b11c0c23e14a3ed11cb6f5d7f3902',
       '721.py':'7c6575beddca87f02c344ee1a132f02b191dc00a'}
RUN_ID=datetime.datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
ROOT=Path('/content' if Path('/content').exists() else '/tmp')/('AKBASCORE_TEST771_'+RUN_ID)
ROOT.mkdir(parents=True,exist_ok=False);CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir()
LOG=ROOT/'TEST771.log';LOG.write_text('',encoding='utf-8');OUT=ROOT/'TEST771_results.json';MANIFEST=ROOT/'TEST771_manifest.json'
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'locks':LOCKS,'checks':[], 'trials':[],
   'scope':'TEST770 proven resident CUT3 temporal pairs; measured attention mass and controlled QK bias; fixed hidden-state probes',
   'limits':['Pair selection is an oracle diagnostic; NOT autonomous routing',
             'Gold answers are used only after inference for scoring',
             'Unknown and code syntax are not proof of semantic truth',
             'Synthetic labels; results do not establish real-world generalization',
             'No custom attention kernel, delta-rule learning or neural self-correction is claimed',
             'Wall-clock includes CPU overhead; CUDA events measure GPU stream elapsed time only',
             'Reuses TEST766 synthetic panel; NOT a held-out generalization test',
             'Fixed CUT3 modulation gain is externally specified; not learned']}
entries={}
def log(*x):
    s=' '.join(map(str,x));print(s,flush=True)
    with LOG.open('a',encoding='utf-8') as f:f.write(s+'\n')
def save():
    p=Path(str(OUT)+'.tmp');p.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');p.replace(OUT)
def check(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save();log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('CHECK_FAILED:'+name)
def sha(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fetch_locked(name):
    req=urllib.request.Request(REPO+name,headers={'User-Agent':'AKBASCORE-TEST771'})
    with urllib.request.urlopen(req,timeout=180) as r:b=r.read(600001)
    check('SOURCE_SIZE_'+name,len(b)<=600000,len(b));check('GIT_LOCK_'+name,gitblob(b)==LOCKS[name],gitblob(b))
    return b
def extract_exact(b,names,label):
    tree=ast.parse(b.decode('utf-8'),filename=label)
    found={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name in names}
    check('SYMBOLS_'+label,set(found)==set(names),sorted(set(names)-set(found)))
    mod=ast.Module(body=[found[n] for n in names],type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod),label,'exec'),globals())
def persist_manifest():
    tmp=Path(str(MANIFEST)+'.tmp')
    tmp.write_text(json.dumps({'test':TEST,'locks':LOCKS,'panel_sha256':R['panel_sha256'],'cartridges':entries},ensure_ascii=False,indent=2,default=str))
    tmp.replace(MANIFEST)
# Seal panel BEFORE model loading or physical cartridge creation.
# New temporal panel, old motor functions imported unchanged.
rng=random.Random(MODEL_SEED);ALPHABET='ABCDEFGHJKLMNPQRSTUVWXYZ'
def opaque(prefix,n=8):return prefix+'-'+''.join(rng.choice(ALPHABET) for _ in range(n))
def synthetic_panel():
    # Four disjoint chains. The middle edge has an old superseded value and a
    # later authoritative replacement; both versions remain on SSD.
    # Each destination has its own independent vault card.
    cases=[];cards={};families=[]
    for i in range(NUM_CHAINS):
        person=opaque('PERSON');work=opaque('WORK')
        oldteam=opaque('TEAM');newteam=opaque('TEAM')
        oldvault=opaque('VAULT');newvault=opaque('VAULT')
        base=f'C{i:02d}'
        card_ids=[base+'_A',base+'_B0',base+'_B1',base+'_C0',base+'_C1']
        cards[card_ids[0]]=f'{person} works_at {work}.'
        cards[card_ids[1]]=(f'Historical record REVISION 0 (superseded): {work} '
                            f'collaborates_with {oldteam}. Valid at revision 0 only.')
        cards[card_ids[2]]=(f'Authoritative CURRENT record REVISION 1: {work} '
                            f'collaborates_with {newteam}. Supersedes revision 0.')
        cards[card_ids[3]]=f'{oldteam} archives_in {oldvault}.'
        cards[card_ids[4]]=f'{newteam} archives_in {newvault}.'
        families.append({'id':base,'old_team':oldteam,'new_team':newteam,
                         'old_vault':oldvault,'new_vault':newvault,'cards':card_ids})
        for view,answer in [('CURRENT',newvault),('HISTORICAL',oldvault)]:
            cases.append({'id':f'Q{i:02d}_{view}', 'person':person,'work':work,
                          'view':view,'answer':answer,'family':base,
                          'question':f'Starting from {person}, follow works_at, '
                          f'then collaborates_with, then archives_in. '
                          f'Use {"only the latest authoritative revision 1" if view=="CURRENT" else "the historical revision 0"} '
                          f'for collaborates_with. What is the final VAULT code? '
                          f'Reply with only the exact VAULT code, or UNKNOWN if evidence is insufficient.'})
    for j in range(2):
        ghost=opaque('PERSON')
        cases.append({'id':f'M{j:02d}','person':ghost,'work':None,
                      'view':'CURRENT','answer':'UNKNOWN','family':None,
                      'question':f'Starting from {ghost}, follow works_at, '
                      'then collaborates_with using the latest authoritative revision, '
                      'then archives_in. Return only the VAULT code or UNKNOWN.'})
    return cases,cards,families
CASES,CARD_TEXT,FAMILIES=synthetic_panel()
PANEL_BYTES=json.dumps({'cases':CASES,'cards':CARD_TEXT,'families':FAMILIES},sort_keys=True,ensure_ascii=False).encode()
PANEL_SHA=sha(PANEL_BYTES);(ROOT/'SEALED_PANEL.json').write_bytes(PANEL_BYTES)
R['panel_sha256']=PANEL_SHA;save()
# Exact locked engine functions. TEST721 routing is recovered via its native score and H3 capture,
# TEST757 provides proven 3-hop traversal, physical append and score-compatible formatting.
raw709=fetch_locked('709.py');raw730=fetch_locked('730.py');raw757=fetch_locked('757.py')
raw721=fetch_locked('721.py');raw764=fetch_locked('764.py')
extract_exact(raw709,['pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room',
                      'kv_digest','full_kv_seal','answer','mem'],'709.py')
extract_exact(raw730,['DirectCut3','forge_native','initialize_native','to_gpu','seal_cp',
                      'memory_seals','compare_seals','safe_load','release'],'730.py')
extract_exact(raw757,['native_append_direct','load_verified','build_fusion','answer_fused','run_arm',
                      'normalized','exact_value','query_native','numeric_rank','step_question','read_exact','model_setup'],'757.py')
# Import the TEST721 exact routing scorer as a provenance control (same TOP2 rule).
extract_exact(raw721,['native_score','route'],'721.py')
# Import only the TEST764 working disk commit and manifest helpers, not its AIN experiment.
extract_exact(raw764,['record_cp'],'764.py')
check('ENGINE_DEPENDENCIES',all(callable(globals().get(k)) for k in
      ('forge_native','initialize_native','native_append_direct','build_fusion','run_arm','query_native','numeric_rank','route','model_setup','record_cp')))

def physical_commit(cid,body):
    ids=tok(body,add_special_tokens=False).input_ids
    check('CARD_NONEMPTY_'+cid,len(ids)>4,len(ids))
    cp,seconds=forge_native(ids,cid)
    record_cp(cid,cp,'TEST771_TEMPORAL_RELATION',[],{'forge_seconds':seconds,'body_sha256':sha(body.encode())})
    del cp;release()

def build_bank():
    bank={};bank721={}
    for cid in sorted(entries):
        cp=safe_load(entries[cid]);x=cp['h'][0,P:,:].float().cpu().numpy()
        ix=np.linspace(0,len(x)-1,min(SAMPLE_PER_PIECE,len(x)),dtype=np.int64)
        bank[cid]=normalized(x[ix]).T.copy();bank721[cid]=normalized(x[ix])
        del cp
    return bank,bank721

def evaluate_step(label,cid,hop,question,ids,kind):
    if not ids:return {'raw':'UNKNOWN','prediction':'UNKNOWN','selected':[]}
    trial=run_arm(label,ids,[{'id':cid+'_'+str(hop),'question':question}],strict_sha=True)
    raw=trial['answers'][0]['raw'];return {'raw':raw,'prediction':read_exact(raw,kind),'selected':list(ids)}

# TEST771: SAME SEALED B0/B1 PAIR, SAME FUSION ORDER, only query cue changes.
# Direct-pair tests are diagnostic upper bounds, NOT evidence of successful autonomous routing.
# Routing tests separately report unmodified H3 and metadata-biased candidate ranking.
# No gold labels, answer values or support IDs are used by the H3 ranking or bias.
# The family identifier is used only to select a controlled pair for the causal diagnostic.
CUE={
 'NEUTRAL':'Using the available document memory, for {work} find collaborates_with. Return ONLY its exact TEAM code or UNKNOWN.',
 'CURRENT':'Using the available document memory, for {work} find collaborates_with in the latest authoritative revision 1. Ignore superseded revision 0. Return ONLY its exact TEAM code or UNKNOWN.',
 'HISTORICAL':'Using the available document memory, for {work} find collaborates_with in historical revision 0, not revision 1. Return ONLY its exact TEAM code or UNKNOWN.'}
def read_pair(label,ids,q):
    row=run_arm(label,ids,[{'id':label,'question':q}],strict_sha=True)
    raw=row['answers'][0]['raw']
    return {'raw':raw,'prediction':read_exact(raw,'TEAM'),'selected':list(ids)}

# TEST771 — attention mass and causal Q/K routing, bounded state feedback.
# ALL experiments are independent arms from the same unmodified resident cache.
# Attention is intercepted only inside a selected self-attention module. It uses
# the same SDPA result; scores are measured separately, and additive bias is
# introduced ONLY in intervention arms. No oracle candidate labels in control.
import contextlib,torch.nn.functional as F
VIEWS=('CURRENT','HISTORICAL')
CUE={
 'CURRENT':'Using the available document memory, for {work} find collaborates_with in the latest authoritative revision 1. Ignore superseded revision 0. Return ONLY its exact TEAM code or UNKNOWN.',
 'HISTORICAL':'Using the available document memory, for {work} find collaborates_with in historical revision 0, not revision 1. Return ONLY its exact TEAM code or UNKNOWN.'}
R['observations']=[];R['timing']={};R['probe']={
 'attention':'Exact sampled softmax attention weights computed from Q/K at layers 4, 20, 40, 79, last query position; GQA keys repeated by QH/KVH',
 'intervention':'Additive SDPA attention-logit bias to one source range, no cache mutation',
 'routing':'Model-derived query CUT3 hidden state projected against source H3 centroids, with signed intervention controls',
 'feedback':'Candidate-conditioned state re-injection with fixed gain; no autonomous second read or self-stopping',
 'limits':['Oracle pair is supplied for causal isolation; NOT autonomous cartridge discovery',
           'No learned gate or trained autonomous controller','Bias is an externally calibrated causal probe, not an autonomous routing mechanism',
           'Attention mass is measured for selected layers, not all 80 layers',
           'Gold candidate scoring is offline teacher-forced, never used to choose memory source']}
save()
def measure(fn):
    torch.cuda.synchronize();a=torch.cuda.Event(enable_timing=True);b=torch.cuda.Event(enable_timing=True)
    t=time.perf_counter();a.record();res=fn();b.record();torch.cuda.synchronize()
    return res,{'wall_ms':round((time.perf_counter()-t)*1000,3),'cuda_stream_ms':round(a.elapsed_time(b),3)}

class Cut3Diagnostic:
    # Temporary direct-forward replacement, never a persistent hook.
    def __init__(self,seed=None,gain=0.):
        self.seed=seed;self.gain=gain;self.old=None;self.last=None;self.delta_l2=0.;self.steps=0
    def __enter__(self):
        layer=model.model.layers[CUT]
        if layer._forward_hooks or layer._forward_pre_hooks:raise RuntimeError('CUT3_HOOK_PRESENT')
        self.old=layer.forward;ctx=self
        def wrapped(this,*args,**kwargs):
            out=ctx.old(*args,**kwargs)
            z=out[0] if isinstance(out,(tuple,list)) else out
            if ctx.seed is not None and ctx.gain:
                v=ctx.seed.to(device=z.device,dtype=torch.float32).reshape(1,1,-1)
                if v.shape[-1]!=z.shape[-1]:raise RuntimeError('SEED_DIMENSION_MISMATCH')
                v=v/v.norm(dim=-1,keepdim=True).clamp_min(1e-6)
                amp=z.float().square().mean(dim=-1,keepdim=True).sqrt().detach()
                delta=(ctx.gain*amp*v*(z.shape[-1]**0.5)).to(z.dtype)
                ctx.delta_l2+=float(delta.float().norm().item())
                z=z+delta;out=replace(out,z)
            ctx.last=z[:,-1,:].detach().clone();ctx.steps+=1
            return out
        layer.forward=types.MethodType(wrapped,layer);return self
    def __exit__(self,*exc):
        model.model.layers[CUT].forward=self.old
        return False

def source_spans(fid,mem):
    # build_fusion initializes first cartridge with the original P prefix,
    # native_append_direct appends only the new cartridge's body.
    n0=int(entries[fid+'_B0']['body_tokens']);n1=int(entries[fid+'_B1']['body_tokens'])
    total=int(mem[0][0].shape[-2]);expected=P+n0+n1
    check('SPAN_TOTAL_'+fid,total==expected,{'actual':total,'expected':expected,'prefix':P,'b0':n0,'b1':n1})
    return {'B0':(P,P+n0),'B1':(P+n0,P+n0+n1)}

class AttentionIntervention:
    """Temporarily replace SDPA only while selected attention layers execute.

    The SDPA implementation is used unchanged for outputs, except a controlled
    additive logit bias in the intervention arms. Measurements are computed
    independently in float32 on the last query token; no model weight changes.
    """
    def __init__(self,spans,selected_layers=(4,20,40,79),bias_span=None,bias=0.):
        self.spans=spans;self.layers=selected_layers;self.bias_span=bias_span;self.bias=float(bias)
        self.old_sdpa=None;self.old_forwards={};self.active_layer=None;self.records=[];self.calls=0
    def __enter__(self):
        self.old_sdpa=F.scaled_dot_product_attention
        ctx=self
        def intercepted(q,k,v,attn_mask=None,dropout_p=0.0,is_causal=False,scale=None,enable_gqa=False):
            layer=ctx.active_layer
            if layer is None:
                return ctx.old_sdpa(q,k,v,attn_mask=attn_mask,dropout_p=dropout_p,is_causal=is_causal,scale=scale,enable_gqa=enable_gqa)
            ctx.calls+=1
            # SDPA Q/K are [batch, heads, query_len, head_dim].
            nq=q.shape[-2];nk=k.shape[-2]
            if q.ndim!=4 or k.ndim!=4 or v.ndim!=4:raise RuntimeError('UNEXPECTED_SDPA_SHAPE')
            if q.shape[1]!=k.shape[1] and not enable_gqa:
                raise RuntimeError('GQA_UNDECLARED_IN_SDPA')
            # An additive mask is applied only to existing physical cache rows.
            newmask=attn_mask
            if ctx.bias_span is not None and ctx.bias:
                a,b=ctx.spans[ctx.bias_span]
                if b>nk:raise RuntimeError('SPAN_EXCEEDS_KV')
                additive=torch.zeros((1,1,nq,nk),device=q.device,dtype=q.dtype)
                additive[...,a:b]=ctx.bias
                if attn_mask is not None:
                    if attn_mask.dtype==torch.bool:
                        additive=additive.masked_fill(~attn_mask,float('-inf'))
                    else:additive=additive+attn_mask
                newmask=additive
            # The final query position is measured, per layer and per head.
            if layer in ctx.layers:
                with torch.no_grad():
                    qq=q[:,:,-1:,:].float()
                    kk=k.float()
                    if qq.shape[1]!=kk.shape[1]:
                        kk=kk.repeat_interleave(qq.shape[1]//kk.shape[1],dim=1)
                    factor=(q.shape[-1]**-0.5) if scale is None else scale
                    scores=torch.matmul(qq,kk.transpose(-2,-1))*factor
                    mask=newmask
                    if mask is not None:
                        if mask.dtype==torch.bool:scores=scores.masked_fill(~mask[...,-1:,:],float('-inf'))
                        else:scores=scores+mask[...,-1:,:].float()
                    # Causal alignment when q_len differs from k_len (decode cache).
                    # For q_len==1, last query may see all preceding KV rows.
                    if is_causal and nq>1:
                        allowed=nk-nq+(nq-1)
                        scores[...,allowed+1:]=float('-inf')
                    probs=torch.softmax(scores,dim=-1)
                    masses={key:float(probs[...,a:b].sum(dim=-1).mean().item()) for key,(a,b) in ctx.spans.items()}
                    ctx.records.append({'layer':layer,'query_tokens':nq,'kv_tokens':nk,'masses':masses,
                       'entropy':float((-(probs*probs.clamp_min(1e-30).log()).sum(-1)).mean().item())})
            return ctx.old_sdpa(q,k,v,attn_mask=newmask,dropout_p=dropout_p,is_causal=is_causal,scale=scale,enable_gqa=enable_gqa)
        F.scaled_dot_product_attention=intercepted
        try:
            for i in self.layers:
                module=model.model.layers[i].self_attn
                if module._forward_hooks or module._forward_pre_hooks:raise RuntimeError('ATTENTION_HOOK_PRESENT')
                old=module.forward;self.old_forwards[i]=old
                def wrapped(this,*args,_i=i,_old=old,**kwargs):
                    prior=ctx.active_layer;ctx.active_layer=_i
                    try:return _old(*args,**kwargs)
                    finally:ctx.active_layer=prior
                module.forward=types.MethodType(wrapped,module)
        except:
            self.__exit__(None,None,None);raise
        return self
    def __exit__(self,*exc):
        for i,old in self.old_forwards.items():model.model.layers[i].self_attn.forward=old
        if self.old_sdpa is not None:F.scaled_dot_product_attention=self.old_sdpa
        self.active_layer=None
        return False

def aggregate_attention(records):
    grouped={}
    for layer in sorted(set(r['layer'] for r in records)):
        rows=[r for r in records if r['layer']==layer]
        grouped[str(layer)]={'calls':len(rows),'B0_mass':round(float(np.mean([r['masses']['B0'] for r in rows])),7),
            'B1_mass':round(float(np.mean([r['masses']['B1'] for r in rows])),7),
            'entropy':round(float(np.mean([r['entropy'] for r in rows])),6)}
    return grouped

def prompt_ids(question):
    suffix='\nQUESTION:\n'+question+'\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
    return tok(suffix,add_special_tokens=False).input_ids

@torch.no_grad()
def score_candidate(mem,question,candidate,spans,seed=None,gain=0.,bias_span=None,bias=0.):
    # Exact candidate sequence probability; never use gold during generation or selection.
    # Teacher forcing is solely an offline diagnostic and cannot claim autonomous correctness.
    qids=prompt_ids(question);aids=tok(candidate,add_special_tokens=False).input_ids
    if not aids:raise RuntimeError('EMPTY_CANDIDATE')
    n=mem[0][0].shape[-2];ids=qids+aids[:-1]
    cache=cache_build(mem)
    positions=torch.arange(n,n+len(ids),device=DEV)
    with Cut3Diagnostic(seed=seed,gain=gain) as diag, AttentionIntervention(spans,bias_span=bias_span,bias=bias) as probe:
        out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
          attention_mask=torch.ones((1,n+len(ids)),device=DEV,dtype=torch.long),
          position_ids=positions.unsqueeze(0),cache_position=positions,use_cache=True,return_dict=True)
        logits=out.logits[0,len(qids)-1:len(qids)-1+len(aids),:].float()
        logp=torch.log_softmax(logits,dim=-1)
        chosen=logp.gather(-1,torch.tensor(aids,device=DEV).unsqueeze(-1)).sum()
        value=float(chosen.item());last=diag.last.detach().clone();delta_l2=diag.delta_l2
        attention=aggregate_attention(probe.records);probe_calls=probe.calls
    del out,cache,logits,logp
    return value,last,delta_l2,attention,probe_calls

def compare(mem,q,old,new,spans,seed=None,gain=0.,bias_span=None,bias=0.):
    # Both labels evaluated under exactly the same condition. Higher margin favors new.
    lp_old,old_state,d_old,att_old,calls_old=score_candidate(mem,q,old,spans,seed,gain,bias_span,bias)
    lp_new,new_state,d_new,att_new,calls_new=score_candidate(mem,q,new,spans,seed,gain,bias_span,bias)
    if not att_old or not att_new or calls_old<4 or calls_new<4:raise RuntimeError("ATTENTION_INSTRUMENTATION_NOT_ACTIVE")
    return {'old_logp':round(lp_old,5),'new_logp':round(lp_new,5),
            'new_minus_old':round(lp_new-lp_old,5),
            'old_state':old_state,'new_state':new_state,
            'cut3_delta_l2':round(max(d_old,d_new),5),
            'attention_old':att_old,'attention_new':att_new,'sdpa_calls':calls_old+calls_new}

def clean_score(d):return {k:v for k,v in d.items() if k not in ('old_state','new_state')}

def run_family(fam):
    fid=fam['id'];pair=[fid+'_B0',fid+'_B1']
    work=next(c['work'] for c in CASES if c['family']==fid)
    questions={v:CUE[v].format(work=work) for v in VIEWS}
    old=fam['old_team'];new=fam['new_team']
    physical_before={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
    pack,tbuild=measure(lambda:build_fusion(pair,'RESIDENT_'+fid,True))
    mem,active,steps,build_s=pack
    try:
        check('ACTIVE_PAIR_'+fid,list(active)==pair,list(active))
        seals=memory_seals(mem);spans=source_spans(fid,mem)
        R['timing'][fid]=tbuild;save()
        for view in VIEWS:
            q=questions[view]
            base,tm=measure(lambda:compare(mem,q,old,new,spans))
            # State seeds are taken from the unmodified model and are used only
            # for a controlled causal probe, not as a source-ID oracle.
            own_seed=base['new_state'] if view=='CURRENT' else base['old_state']
            opposite_seed=base['old_state'] if view=='CURRENT' else base['new_state']
            # B0/B1 bias controls are deliberately opposite physical interventions.
            # They are NOT chosen by gold labels and are both run for every query.
            arms=[('FULL',None,0.,None,0.),
                  ('BIAS_B0',None,0.,'B0',2.),
                  ('BIAS_B1',None,0.,'B1',2.),
                  ('STATE_SAME',own_seed,0.035,None,0.),
                  ('STATE_OPPOSITE',opposite_seed,0.035,None,0.),
                  ('STATE_HIGH_GAIN',own_seed,0.07,None,0.)]
            for arm,seed,gain,bias_span,bias in arms:
                if arm=='FULL':res,timing=base,tm
                else:res,timing=measure(lambda:compare(mem,q,old,new,spans,seed,gain,bias_span,bias))
                row={'family':fid,'view':view,'arm':arm,
                     'margin_new_minus_old':res['new_minus_old'],
                     'old_logp':res['old_logp'],'new_logp':res['new_logp'],
                     'cut3_delta_l2':res['cut3_delta_l2'],
                     'attention_old':res['attention_old'],'attention_new':res['attention_new'],
                     'sdpa_calls':res['sdpa_calls'],**timing}
                R['observations'].append(row);save()
                log('OBS',fid,view,arm,'MARGIN_NEW_MINUS_OLD',row['margin_new_minus_old'],
                    'ATTN_NEW',row['attention_new'],'CUT3_DELTA_L2',row['cut3_delta_l2'],'WALL_MS',row['wall_ms'])
        check('RESIDENT_MEMORY_UNCHANGED_'+fid,compare_seals(seals,memory_seals(mem)))
    finally:
        del mem,pack;release()
    for cid in pair:
        check('PAIR_SHA_UNCHANGED_'+fid+'_'+cid,
              sha_file(CART_DIR/(cid+'.pt'))==physical_before[cid]==entries[cid]['sha256'])

def summarize():
    out={}
    for arm in ('FULL','BIAS_B0','BIAS_B1','STATE_SAME','STATE_OPPOSITE','STATE_HIGH_GAIN'):
        rows=[r for r in R['observations'] if r['arm']==arm]
        out[arm]={'n':len(rows),'median_margin_new_minus_old':round(float(np.median([r['margin_new_minus_old'] for r in rows])),5),
          'median_wall_ms':round(float(np.median([r['wall_ms'] for r in rows])),3),
          'mean_cut3_delta_l2':round(float(np.mean([r['cut3_delta_l2'] for r in rows])),5),
          'current_prefers_new':sum(r['margin_new_minus_old']>0 for r in rows if r['view']=='CURRENT'),
          'historical_prefers_old':sum(r['margin_new_minus_old']<0 for r in rows if r['view']=='HISTORICAL')}
    return out

try:
    log('='*108);log('AKBASCORE TEST771 / QK ATTENTION MASS / CAUSAL BIAS / HIDDEN STATE');log('='*108)
    check('PANEL_SEALED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('FRESH_GPU',free>=40*2**30,'Restart Colab runtime if 72B already loaded')
    model_setup();weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('ALL_20_PHYSICAL_CARTRIDGES',len(entries)==20,len(entries))
    for fam in FAMILIES:run_family(fam)
    check('OBSERVATION_MATRIX',len(R['observations'])==NUM_CHAINS*len(VIEWS)*6,len(R['observations']))
    check('MODEL_WEIGHTS_UNCHANGED',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    check('PANEL_UNCHANGED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    R['score']=summarize();R['status']='COMPLETE_RESULTS_RECORDED'
    R['summary']={'model':'frozen Qwen2.5-72B NF4','cards':len(entries),'pairs':NUM_CHAINS,
       'observations':len(R['observations']),'score':R['score'],
       'attention_mass_measured':True,'autonomous_routing_proven':False,
       'model_internal_closed_loop_proven':False,
       'interpretation':'Selected-layer QK softmax attention mass, causal SDPA logit bias and fixed-gain CUT3 perturbation. Oracle pair supplied. No learned routing or autonomous self-correction.'}
    save();log('TEST771_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save()
    log('TEST771_FAILED',repr(e));log(R['traceback']);raise
finally:save()
