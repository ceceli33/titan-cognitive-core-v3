# AKBASCORE SILICON HIPPOCAMPUS — TEST778
# Locked GPU-proven TEST767 backbone; same sealed 20-card panel; frozen 72B native CUT3.
# ONE Colab cell. Existing engine definitions are imported VERBATIM by locked Git blobs.
# No training, no source text in QA prompts, no forward hooks, no Gradio.
# TEST778 compares forward and reverse native B0/B1 append order, isolated source rebuilds and 80-layer parity.
# Research probe only: no learned controller, no proof of autonomous retrieval, synthesis or stopping.
# TEST777 predecessor completed on A100; TEST778 modification is NOT GPU executed by author.
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
TEST='777';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
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
ROOT=Path('/content' if Path('/content').exists() else '/tmp')/('AKBASCORE_TEST778_'+RUN_ID)
ROOT.mkdir(parents=True,exist_ok=False);CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir()
LOG=ROOT/'TEST778.log';LOG.write_text('',encoding='utf-8');OUT=ROOT/'TEST778_results.json';MANIFEST=ROOT/'TEST778_manifest.json'
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'locks':LOCKS,'checks':[], 'trials':[],
   'scope':'Forward and reverse B0/B1 physical append order; causal prefix invariance, RoPE rephase and isolated rebuild comparisons',
   'limits':['Pair selection is an oracle diagnostic; NOT autonomous routing',
             'Gold answers are used only after inference for scoring',
             'Unknown and code syntax are not proof of semantic truth',
             'Synthetic labels; results do not establish real-world generalization',
             'No trained neural self-correction is claimed',
             'Wall-clock includes CPU overhead; CUDA events measure GPU stream elapsed time only',
             'Reuses TEST766 synthetic panel; NOT a held-out generalization test',
             'Source ablation uses controlled known pairs, not autonomous retrieval; no gold answer used for intervention choice']}
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
    req=urllib.request.Request(REPO+name,headers={'User-Agent':'AKBASCORE-TEST778'})
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
    record_cp(cid,cp,'TEST778_TEMPORAL_RELATION',[],{'forge_seconds':seconds,'body_sha256':sha(body.encode())})
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

# TEST778: SAME SEALED B0/B1 PAIR, SAME FUSION ORDER, only query cue changes.
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

# TEST778 — attention mass and causal Q/K routing, bounded state feedback.
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
 'attention':'Readout instrumentation is observational; physical KV removal is performed on all 80 layers',
 'intervention':'All 80-layer KV cache slices remove B0, B1, or both; original cache is not mutated',
 'routing':'Selected-layer QK attention mass is a BASELINE only, never fed back as self-evidence',
 'feedback':'No feedback loop: independent full-cache source removal and physical rebuild comparisons',
 'limits':['Oracle pair is supplied for causal isolation; NOT autonomous cartridge discovery',
           'No learned gate or trained autonomous controller','KV span deletion is a controlled causal probe, not autonomous routing',
           'RoPE rephasing assumes static rotary frequencies and Qwen rotate-half convention; tensor parity measured, never assumed',
           'Gold candidate scoring is offline teacher-forced, never used to choose the axis sign']}
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
def score_candidate(mem,question,candidate,spans,seed=None,gain=0.,bias_span=None,bias=0.,selected_layers=(4,20,40,79)):
    # Exact candidate sequence probability; never use gold during generation or selection.
    # Teacher forcing is solely an offline diagnostic and cannot claim autonomous correctness.
    qids=prompt_ids(question);aids=tok(candidate,add_special_tokens=False).input_ids
    if not aids:raise RuntimeError('EMPTY_CANDIDATE')
    n=mem[0][0].shape[-2];ids=qids+aids[:-1]
    cache=cache_build(mem)
    positions=torch.arange(n,n+len(ids),device=DEV)
    with Cut3Diagnostic(seed=seed,gain=gain) as diag, AttentionIntervention(spans,selected_layers=selected_layers,bias_span=bias_span,bias=bias) as probe:
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

def compare(mem,q,old,new,spans,seed=None,gain=0.,bias_span=None,bias=0.,selected_layers=(4,20,40,79)):
    # Both labels evaluated under exactly the same condition. Higher margin favors new.
    lp_old,old_state,d_old,att_old,calls_old=score_candidate(mem,q,old,spans,seed,gain,bias_span,bias,selected_layers)
    lp_new,new_state,d_new,att_new,calls_new=score_candidate(mem,q,new,spans,seed,gain,bias_span,bias,selected_layers)
    if not att_old or not att_new or calls_old<len(selected_layers) or calls_new<len(selected_layers):raise RuntimeError("ATTENTION_INSTRUMENTATION_NOT_ACTIVE")
    return {'old_logp':round(lp_old,5),'new_logp':round(lp_new,5),
            'new_minus_old':round(lp_new-lp_old,5),
            'old_state':old_state,'new_state':new_state,
            'cut3_delta_l2':round(max(d_old,d_new),5),
            'attention_old':att_old,'attention_new':att_new,'sdpa_calls':calls_old+calls_new}

def clean_score(d):return {k:v for k,v in d.items() if k not in ('old_state','new_state')}


# TEST778 — DRA-inspired bidirectional activation probe, built on TEST772 verified GPU skeleton.
# The DRA compass is NOT a truth oracle. The first pass only measures activation
# separation. The second pass tests small, norm-relative +/- interventions.
# Gold answers are used only in offline evaluation, NEVER in steering construction.
# We deliberately avoid a self-reinforcing attention feedback loop.
ROUTE_LAYERS=(20,40,79)
DRA_GAINS=(0.0,0.01,0.03)
MAX_DELTA_REL=0.05

def observe_state(mem,question,spans):
    qids=prompt_ids(question);n=int(mem[0][0].shape[-2]);cache=cache_build(mem)
    pos=torch.arange(n,n+len(qids),device=DEV)
    with Cut3Diagnostic() as diag,AttentionIntervention(spans) as probe:
        out=model(input_ids=torch.tensor([qids],device=DEV),past_key_values=cache,
            attention_mask=torch.ones((1,n+len(qids)),device=DEV,dtype=torch.long),
            position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        if diag.last is None or probe.calls<4:raise RuntimeError('STATE_PROBE_NOT_ACTIVE')
        state=diag.last.float().detach().reshape(-1).contiguous().clone()
        if state.numel()!=H or state.ndim!=1:
            raise RuntimeError(f'CUT3_STATE_SHAPE_INVALID: {tuple(state.shape)}, expected ({H},)')
        if not torch.isfinite(state).all():
            raise RuntimeError('CUT3_STATE_NONFINITE')
        att=aggregate_attention(probe.records)
    del out,cache
    return state,att

def source_signal(a,spans):
    density={}
    for src in ('B0','B1'):
        length=spans[src][1]-spans[src][0]
        density[src]=float(np.mean([float(a[str(i)][src+'_mass'])/length for i in ROUTE_LAYERS]))
    chosen='B1' if density['B1']>density['B0'] else 'B0'
    conf=abs(density['B1']-density['B0'])/max(sum(density.values()),1e-12)
    return chosen,conf,density

def build_source_cache(cid,fid):
    # Exactly the same locked native physical fusion engine, one source at a time.
    pack=build_fusion([cid],'ISOLATED_'+fid+'_'+cid,True)
    mem,active,steps,seconds=pack
    check('ISOLATED_SOURCE_'+cid,list(active)==[cid],list(active))
    return mem

@torch.no_grad()
def free_generate(mem,question,seed=None,gain=0.,max_new=20,spans=None,bias_span=None,bias=0.,selected_layers=(4,20,40,79)):
    # Greedy output under the SAME causal ablation used by candidate scoring.
    qids=prompt_ids(question)
    n=int(mem[0][0].shape[-2]);cache=cache_build(mem)
    generated=[]
    try:
        with Cut3Diagnostic(seed=seed,gain=gain) as diag, AttentionIntervention(
            spans if spans is not None else {'B0':(0,0),'B1':(0,0)},
            selected_layers=selected_layers,bias_span=bias_span,bias=bias) as probe:
            for t in range(max_new):
                if t==0:
                    ids=torch.tensor([qids],device=DEV)
                    pos=torch.arange(n,n+len(qids),device=DEV)
                else:
                    ids=torch.tensor([[generated[-1]]],device=DEV)
                    pos=torch.tensor([n+len(qids)+t-1],device=DEV)
                out=model(input_ids=ids,past_key_values=cache,
                          attention_mask=torch.ones((1,n+len(qids)+t),device=DEV,dtype=torch.long),
                          position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
                next_id=int(out.logits[0,-1].argmax().item());generated.append(next_id)
                del out
                if next_id==tok.eos_token_id:break
            if probe.calls < len(selected_layers):raise RuntimeError('GENERATION_ATTENTION_INTERVENTION_NOT_ACTIVE')
        raw=tok.decode(generated,skip_special_tokens=True).strip()
        return {'raw':raw,'prediction':read_exact(raw,'TEAM'),'generated_tokens':len(generated),'sdpa_calls':probe.calls}
    finally:
        del cache

# TEST778: full 80-layer physical KV source removal, never attention-only masking.
# Rebuilt single-source cartridges are independent causal controls.
# IMPORTANT: Removing B0 changes the physical position of B1. The B1-only
# rebuild has a different positional history; equality is NOT presumed.
# A failed equivalence comparison is a diagnostic, not a GPU execution failure.
ARMS=('PAIR','REBUILD_B0','REBUILD_B1','DELETE_B0','REPHASE_DELETE_B0',
      'DELETE_B1','REVERSE_PAIR','REVERSE_DELETE_B0')

def verify_mem_shape(mem,label):
    check('KV_LAYER_COUNT_'+label,len(mem)==NL,len(mem))
    length=None
    for li,layer in enumerate(mem):
        if len(layer)!=2:raise RuntimeError(f'KV_PAIR_EXPECTED {label} {li}')
        k,v=layer
        if k.shape!=v.shape or k.ndim!=4 or k.shape[1]!=KVH or k.shape[-1]!=HD:
            raise RuntimeError(f'KV_SHAPE_INVALID {label} L{li} {tuple(k.shape)} {tuple(v.shape)}')
        if length is None:length=int(k.shape[-2])
        if k.shape[-2]!=length:raise RuntimeError(f'KV_LENGTH_MISMATCH {label} L{li}')
    return length

def physical_transform(mem,spans,arm):
    # Slicing K and V at every layer. No SDPA monkeypatch, no forward hooks.
    if arm not in ('DELETE_B0','DELETE_B1','DELETE_BOTH','ZERO_B0','ZERO_B1'):
        raise ValueError(arm)
    n=verify_mem_shape(mem,'INPUT_'+arm)
    b0a,b0b=spans['B0'];b1a,b1b=spans['B1']
    if not (0<=b0a<b0b==b1a<b1b==n):raise RuntimeError('INVALID_SOURCE_SPANS')
    result=[]
    for k,v in mem:
        if arm=='DELETE_B0':
            nk=torch.cat((k[...,:b0a,:],k[...,b1a:,:]),dim=-2).contiguous()
            nv=torch.cat((v[...,:b0a,:],v[...,b1a:,:]),dim=-2).contiguous()
        elif arm=='DELETE_B1':
            nk=k[...,:b1a,:].contiguous();nv=v[...,:b1a,:].contiguous()
        elif arm=='DELETE_BOTH':
            nk=k[...,:b0a,:].contiguous();nv=v[...,:b0a,:].contiguous()
        else:
            a,b=spans['B0' if arm=='ZERO_B0' else 'B1']
            nk=k.clone();nv=v.clone();nk[...,a:b,:]=0;nv[...,a:b,:]=0
        result.append((nk,nv))
    check('KV_TRANSFORM_LAYER_COUNT_'+arm,len(result)==NL,len(result))
    expected=n-((b0b-b0a) if arm=='DELETE_B0' else (b1b-b1a) if arm=='DELETE_B1' else
                (b1b-b0a) if arm=='DELETE_BOTH' else 0)
    check('KV_TRANSFORM_LENGTH_'+arm,verify_mem_shape(result,'OUTPUT_'+arm)==expected,
          {'actual':result[0][0].shape[-2],'expected':expected})
    # Exact elementwise retention, across every layer. This verifies the
    # removal operation independently of subsequent answer behavior.
    with torch.no_grad():
        for i,((k,v),(nk,nv)) in enumerate(zip(mem,result)):
            if arm=='DELETE_B0':
                expected_k=torch.cat((k[...,:b0a,:],k[...,b1a:,:]),dim=-2)
                expected_v=torch.cat((v[...,:b0a,:],v[...,b1a:,:]),dim=-2)
            elif arm=='DELETE_B1':expected_k,expected_v=k[...,:b1a,:],v[...,:b1a,:]
            elif arm=='DELETE_BOTH':expected_k,expected_v=k[...,:b0a,:],v[...,:b0a,:]
            else:
                a,b=spans['B0' if arm=='ZERO_B0' else 'B1']
                if torch.count_nonzero(nk[...,a:b,:]).item() or torch.count_nonzero(nv[...,a:b,:]).item():
                    raise RuntimeError(f'ZERO_NOT_EFFECTIVE {arm} L{i}')
                if not (torch.equal(nk[...,:a,:],k[...,:a,:]) and torch.equal(nv[...,:a,:],v[...,:a,:]) and
                        torch.equal(nk[...,b:,:],k[...,b:,:]) and torch.equal(nv[...,b:,:],v[...,b:,:])):
                    raise RuntimeError(f'ZERO_CHANGED_OTHER_SPANS {arm} L{i}')
                continue
            if not torch.equal(nk,expected_k) or not torch.equal(nv,expected_v):
                raise RuntimeError(f'DELETION_INTEGRITY_FAILURE {arm} L{i}')
    log('PASS PHYSICAL_80_LAYER_TRANSFORM',arm,'original',n,'result',expected)
    return result

# TEST778: exact inverse RoPE rotation on retained B1 keys after deleting B0.
# The source-only reference is a separate locked physical rebuild, not a copied cache.
# We do not assume RoPE correction alone makes independently fused K/V equal.
def rotary_inv_freq():
    rope=model.model.rotary_emb
    inv=getattr(rope,'inv_freq',None)
    if inv is None or inv.numel()!=HD//2:
        raise RuntimeError('ROPE_INV_FREQ_UNAVAILABLE_OR_WRONG_SHAPE')
    return inv.detach().float().to(DEV)

def rotate_half_qwen(x):
    return torch.cat((-x[...,HD//2:],x[...,:HD//2]),dim=-1)

def rephase_delete_b0(mem,spans,shift_override=None):
    b0a,b0b=spans['B0'];b1a,b1b=spans['B1']
    shift=-(b0b-b0a) if shift_override is None else int(shift_override)
    inv=rotary_inv_freq()
    angles=(inv*float(shift))
    c=torch.cat((angles.cos(),angles.cos())).reshape(1,1,1,HD)
    si=torch.cat((angles.sin(),angles.sin())).reshape(1,1,1,HD)
    result=[];max_zero_err=0.0
    for li,(k,v) in enumerate(mem):
        # No change to prefix; the retained B1 key span alone receives inverse RoPE.
        pre_k=k[...,:b0a,:].contiguous()
        src_k=k[...,b1a:b1b,:].contiguous()
        pre_v=v[...,:b0a,:].contiguous()
        src_v=v[...,b1a:b1b,:].contiguous()
        rotated=(src_k.float()*c+rotate_half_qwen(src_k.float())*si).to(k.dtype)
        if shift==0:
            max_zero_err=max(max_zero_err,float((rotated-src_k).float().abs().max().item()))
        result.append((torch.cat((pre_k,rotated),dim=-2).contiguous(),
                       torch.cat((pre_v,src_v),dim=-2).contiguous()))
    verify_mem_shape(result,'REPHASE_DELETE_B0')
    check('REPHASED_80_LAYERS',len(result)==NL,len(result))
    if shift==0:check('ROPE_ZERO_SHIFT_IDENTITY',max_zero_err==0.0,max_zero_err)
    return result

def tensor_parity(a,b,label):
    # Absolute and relative BF16 differences on all 80 layers, separately K and V.
    na=verify_mem_shape(a,'PARITY_A_'+label)
    nb=verify_mem_shape(b,'PARITY_B_'+label)
    check('PARITY_LENGTH_'+label,na==nb,{'a':na,'b':nb})
    metrics={'k_max_abs':0.,'v_max_abs':0.,'k_rel_l2_sq_num':0.,
             'v_rel_l2_sq_num':0.,'k_rel_l2_sq_den':0.,'v_rel_l2_sq_den':0.,
             'k_exact_layers':0,'v_exact_layers':0}
    for (ak,av),(bk,bv) in zip(a,b):
        for key,x,y in [('k',ak,bk),('v',av,bv)]:
            if x.shape!=y.shape:raise RuntimeError('PARITY_SHAPE_MISMATCH_'+label)
            diff=(x.float()-y.float())
            metrics[key+'_max_abs']=max(metrics[key+'_max_abs'],float(diff.abs().max().item()))
            metrics[key+'_rel_l2_sq_num']+=float(diff.square().sum().item())
            metrics[key+'_rel_l2_sq_den']+=float(y.float().square().sum().item())
            metrics[key+'_exact_layers']+=int(torch.equal(x,y))
            del diff
    result={key+'_max_abs':round(metrics[key+'_max_abs'],7) for key in ('k','v')}
    for key in ('k','v'):
        result[key+'_rel_l2']=round((metrics[key+'_rel_l2_sq_num']/max(metrics[key+'_rel_l2_sq_den'],1e-30))**.5,8)
        result[key+'_exact_layers']=metrics[key+'_exact_layers']
    R.setdefault('tensor_parity',[]).append({'family':label,**result})
    log('TENSOR_PARITY',label,json.dumps(result));save()
    return result

def quick_read(mem,question,old,new):
    # Reuse proven TEST778 scoring and greedy generation, without an
    # intervention. All 80 layers still run natively.
    dummy={'B0':(0,0),'B1':(0,0)}
    score=compare(mem,question,old,new,dummy,selected_layers=(4,20,40,79))
    generated=free_generate(mem,question,spans=dummy,max_new=20,
                            selected_layers=(4,20,40,79))
    return {'margin_new_minus_old':score['new_minus_old'],
            'old_logp':score['old_logp'],'new_logp':score['new_logp'],
            'generated':generated['prediction'],'generated_raw':generated['raw'],
            'generated_tokens':generated['generated_tokens']}

def run_family(fam):
    fid=fam['id'];pair=[fid+'_B0',fid+'_B1']
    work=next(c['work'] for c in CASES if c['family']==fid)
    old=fam['old_team'];new=fam['new_team']
    physical_before={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
    rebuilt={};ref_mem={};mem=None;reverse_mem=None;edits={}
    try:
        for src,cid in [('B0',pair[0]),('B1',pair[1])]:
            single=build_source_cache(cid,fid)
            verify_mem_shape(single,'REBUILD_'+fid+'_'+src)
            ref_mem[src]=single
            rebuilt[src]={view:quick_read(single,CUE[view].format(work=work),old,new)
                          for view in VIEWS}
        mem,active,steps,build_s=build_fusion(pair,'FORWARD_'+fid,True)
        check('ACTIVE_PAIR_'+fid,list(active)==pair,list(active))
        verify_mem_shape(mem,'PAIR_'+fid)
        seals=memory_seals(mem);spans=source_spans(fid,mem)
        edits['DELETE_B0']=physical_transform(mem,spans,'DELETE_B0')
        edits['DELETE_B1']=physical_transform(mem,spans,'DELETE_B1')
        edits['REPHASE_DELETE_B0']=rephase_delete_b0(mem,spans)
        # The same locked native engine, with only the physical append order reversed.
        # B1 is now the prefix, so removing the later B0 does not alter B1 positions.
        reverse_mem,reverse_active,reverse_steps,reverse_time=build_fusion(
            [pair[1],pair[0]],'REVERSE_'+fid,True)
        check('REVERSE_ACTIVE_PAIR_'+fid,list(reverse_active)==[pair[1],pair[0]],list(reverse_active))
        reverse_len=verify_mem_shape(reverse_mem,'REVERSE_PAIR_'+fid)
        prefix_len=verify_mem_shape(ref_mem['B1'],'ISOLATED_B1_'+fid)
        check('REVERSE_LENGTH_'+fid,reverse_len==prefix_len+len(tok.encode(CARD_TEXT[pair[0]],add_special_tokens=False)),
              {'reverse':reverse_len,'prefix':prefix_len})
        reverse_deleted=[]
        for k,v in reverse_mem:
            reverse_deleted.append((k[...,:prefix_len,:].contiguous(),v[...,:prefix_len,:].contiguous()))
        edits['REVERSE_DELETE_B0']=reverse_deleted
        # The exact parity of the early B1 prefix is a control of append-only causality.
        par_rev=tensor_parity(reverse_deleted,ref_mem['B1'],fid+'_REVERSE_DELETE_B0_VS_REBUILD_B1')
        check('REVERSE_PREFIX_TENSOR_EXACT_'+fid,
              par_rev['k_exact_layers']==NL and par_rev['v_exact_layers']==NL,par_rev)
        par_delete=tensor_parity(edits['DELETE_B1'],ref_mem['B0'],fid+'_FORWARD_DELETE_B1_VS_REBUILD_B0')
        check('FORWARD_PREFIX_TENSOR_EXACT_'+fid,
              par_delete['k_exact_layers']==NL and par_delete['v_exact_layers']==NL,par_delete)
        tensor_parity(edits['DELETE_B0'],ref_mem['B1'],fid+'_FORWARD_DELETE_B0_VS_REBUILD_B1')
        tensor_parity(edits['REPHASE_DELETE_B0'],ref_mem['B1'],fid+'_REPHASE_VS_REBUILD_B1')
        # Compare the first (B1) part of reverse fusion and the second (B1) part
        # of forward fusion with the isolated B1, on identical sequence lengths.
        # The forward B1 span has different positional history; report only,
        # never assume that simple tensor alignment establishes parity.
        forward_b1=[];b0a,b0b=spans['B0'];b1a,b1b=spans['B1']
        for k,v in mem:
            forward_b1.append((torch.cat((k[...,:b0a,:],k[...,b1a:b1b,:]),dim=-2).contiguous(),
                               torch.cat((v[...,:b0a,:],v[...,b1a:b1b,:]),dim=-2).contiguous()))
        tensor_parity(forward_b1,ref_mem['B1'],fid+'_FORWARD_B1_SPAN_VS_REBUILD_B1')
        del forward_b1
        for view in VIEWS:
            q=CUE[view].format(work=work)
            rows={'PAIR':quick_read(mem,q,old,new),
                  'REBUILD_B0':rebuilt['B0'][view],
                  'REBUILD_B1':rebuilt['B1'][view],
                  'REVERSE_PAIR':quick_read(reverse_mem,q,old,new)}
            for arm in edits:rows[arm]=quick_read(edits[arm],q,old,new)
            correct=new if view=='CURRENT' else old
            baseline=rows['PAIR']['generated']
            for arm in ARMS:
                d=rows[arm]
                row={'family':fid,'view':view,'arm':arm,
                     'answer_expected':correct,'prediction':d['generated'],
                     'generated_correct':d['generated']==correct,
                     'generated_changed_from_pair':d['generated']!=baseline,
                     'margin_new_minus_old':d['margin_new_minus_old'],
                     'delta_margin_from_pair':round(d['margin_new_minus_old']-rows['PAIR']['margin_new_minus_old'],5),
                     'old_logp':d['old_logp'],'new_logp':d['new_logp'],
                     'generated_raw':d['generated_raw'],'generated_tokens':d['generated_tokens']}
                R['observations'].append(row);save()
                log('OBS',fid,view,arm,'PRED',row['prediction'],
                    'CORRECT',row['generated_correct'],'CHANGED',row['generated_changed_from_pair'],
                    'MARGIN',row['margin_new_minus_old'])
            for label,a,b in [('FORWARD_DELETE_B1_VS_REBUILD_B0','DELETE_B1','REBUILD_B0'),
                              ('FORWARD_DELETE_B0_VS_REBUILD_B1','DELETE_B0','REBUILD_B1'),
                              ('REPHASE_VS_REBUILD_B1','REPHASE_DELETE_B0','REBUILD_B1'),
                              ('REVERSE_DELETE_B0_VS_REBUILD_B1','REVERSE_DELETE_B0','REBUILD_B1'),
                              ('REVERSE_PAIR_VS_FORWARD_PAIR','REVERSE_PAIR','PAIR')]:
                same_answer=rows[a]['generated']==rows[b]['generated']
                delta=round(rows[a]['margin_new_minus_old']-rows[b]['margin_new_minus_old'],5)
                log('EQUIVALENCE_DIAGNOSTIC',fid,view,label,'same_prediction',same_answer,'delta_margin',delta)
                R.setdefault('equivalence',[]).append({'family':fid,'view':view,
                    'comparison':label,'same_prediction':same_answer,'delta_margin':delta})
                save()
        check('RESIDENT_MEMORY_UNCHANGED_'+fid,compare_seals(seals,memory_seals(mem)))
    finally:
        edits.clear();ref_mem.clear()
        if mem is not None:del mem
        if reverse_mem is not None:del reverse_mem
        release()
    for cid in pair:
        check('PAIR_SHA_UNCHANGED_'+fid+'_'+cid,
              sha_file(CART_DIR/(cid+'.pt'))==physical_before[cid]==entries[cid]['sha256'])

def summarize():
    score={}
    for arm in ARMS:
        rows=[r for r in R['observations'] if r['arm']==arm]
        score[arm]={'n':len(rows),'generated_correct':sum(r['generated_correct'] for r in rows),
            'generated_changed':sum(r['generated_changed_from_pair'] for r in rows),
            'median_abs_delta_margin':round(float(np.median([abs(r['delta_margin_from_pair']) for r in rows])),5)}
    return score

try:
    log('='*108)
    log('AKBASCORE TEST778 / ORDER-DEPENDENT KV FUSION / REVERSE APPEND / TENSOR PARITY')
    log('='*108)
    check('PANEL_SEALED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('FRESH_GPU',free>=40*2**30,'Restart Colab runtime if 72B already loaded')
    model_setup();weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('ALL_20_PHYSICAL_CARTRIDGES',len(entries)==20,len(entries))
    for fam in FAMILIES:run_family(fam)
    check('OBSERVATION_MATRIX',len(R['observations'])==NUM_CHAINS*len(VIEWS)*len(ARMS),len(R['observations']))
    check('MODEL_WEIGHTS_UNCHANGED',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    check('PANEL_UNCHANGED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    R['score']=summarize();R['status']='COMPLETE_RESULTS_RECORDED'
    R['summary']={'model':'frozen Qwen2.5-72B NF4','cards':len(entries),
      'pairs':NUM_CHAINS,'observations':len(R['observations']),'score':R['score'],
      'physical_KV_layers_deleted':80,'rope_rephase_tested':True,'reverse_append_tested':True,'greedy_generation_measured':True,
      'autonomous_routing_proven':False,'model_internal_closed_loop_proven':False,
      'interpretation':'Physical forward/reverse source append order, exact prefix invariance, and B1 tensor dependence on preceding B0. RoPE-only correction and rebuilt source controls measured separately. No autonomous routing or closed-loop correction proven.'}
    save();log('TEST778_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save()
    log('TEST778_FAILED',repr(e));log(R['traceback']);raise
finally:save()
