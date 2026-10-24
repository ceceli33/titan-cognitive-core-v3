# ==================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST758D — CUT3 NUMERICAL PARITY DIAGNOSIS
# FROZEN QWEN2.5-72B / NF4 / BF16 / CUT3 / PHYSICAL NUMERICAL FUSION
# Single Colab cell; no Gradio; no text-mediated synthesis in fusion.
# Locked functions imported verbatim from TEST709 / TEST730 / TEST757.
# TEST745 official AIN preliminary-source resolver imported verbatim.
# This script has been statically checked, NOT executed on an A100 by its author.
# ==================================================================================================
import os, sys, subprocess, importlib.util, urllib.request, urllib.parse
import hashlib, json, time, gc, traceback, ast, types, html, re, datetime
from pathlib import Path
from datetime import timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

for module, package in [('torch','torch'), ('transformers','transformers>=5.18,<6'),
                        ('accelerate','accelerate>=1.15'), ('bitsandbytes','bitsandbytes>=0.50'),
                        ('pymupdf','pymupdf'), ('bs4','beautifulsoup4'), ('psutil','psutil')]:
    if importlib.util.find_spec(module) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', package])
import torch, transformers, bitsandbytes, pymupdf
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers.cache_utils import DynamicCache

if not torch.cuda.is_available(): raise RuntimeError('CUDA_REQUIRED')
if torch.cuda.device_count() != 1: raise RuntimeError('EXACTLY_ONE_GPU_REQUIRED')
GPU_INFO = torch.cuda.get_device_properties(0)  # Never name this variable `gpu`: TEST730 has gpu()!
if 'A100' not in GPU_INFO.name or GPU_INFO.total_memory < 70 * 2**30:
    raise RuntimeError(f'A100_80GB_REQUIRED: {GPU_INFO.name}, {GPU_INFO.total_memory/2**30:.2f} GiB')

RUN_ID = datetime.datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
ROOT = Path('/content' if Path('/content').exists() else '/tmp') / ('AKBASCORE_TEST758D_' + RUN_ID)
ROOT.mkdir(parents=True, exist_ok=False)
CART_DIR = ROOT / 'physical_cartridges'
EVIDENCE_DIR = ROOT / 'sealed_sources'
CART_DIR.mkdir(); EVIDENCE_DIR.mkdir()
LOG = ROOT / 'TEST758D.log'; LOG.write_text('', encoding='utf-8')
OUT = ROOT / 'TEST758D_results.json'
MANIFEST = ROOT / 'TEST758D_manifest.json'
TEST = '758D'
MODEL_ID = 'Qwen/Qwen2.5-72B-Instruct'
CUT = 3; EXPECTED = (80,8192,64,8,128)
DTYPE = torch.bfloat16; DEV = torch.device('cuda:0')
CHUNK = 128; GPU_RESERVE_GIB = 9.0
MAX_NEW = 192; MAX_FUSED_TOKENS = 11000
NL, H, QH, KVH, HD = EXPECTED
REPO = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCKS = {
    '709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125',
    '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
    '745.py': 'de9e137e981fd57812d9a5e40d3c72dc278d2133',
    '757.py': '3d88bf8638390995858f23391f1e043faa586835',
}
R = {'test':TEST, 'status':'STARTED', 'run_id':RUN_ID, 'checks':[], 'trials':[],
     'locks':LOCKS, 'method':'TEST757 native append -> S01 SSD reload -> 80-layer numerical discrepancy diagnosis',
     'limitations':['Static validation only; GPU run pending',
                    'Native append is not proof of independent semantic synthesis',
                    'C01 and C02 are segments of the SAME AIN preliminary report',
                    'No final-report outcome is admitted',
                    'Exact parity and scientific correctness are separate questions',
                    'Diagnostics quantify BF16 divergence without weakening exact SHA parity']}
entries = {}

def log(*items):
    s = ' '.join(map(str, items)); print(s, flush=True)
    with LOG.open('a', encoding='utf-8') as f: f.write(s+'\n')

def save():
    temp = Path(str(OUT)+'.tmp')
    temp.write_text(json.dumps(R, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    temp.replace(OUT)

def check(name, ok, detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail})
    save(); log('PASS' if ok else 'FAIL',name,'' if detail is None else detail)
    if not ok: raise RuntimeError('CHECK_FAILED:'+name)

def sha(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h = hashlib.sha256()
    with open(p,'rb') as f:
        for part in iter(lambda:f.read(4*1024*1024),b''): h.update(part)
    return h.hexdigest()

def gitblob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def fetch_locked(name):
    with urllib.request.urlopen(urllib.request.Request(REPO+name, headers={'User-Agent':'AKBASCORE-TEST758D'}),timeout=180) as f:
        b=f.read(600001)
    check('SOURCE_SIZE_'+name,len(b)<=600000,len(b))
    check('GIT_BLOB_LOCK_'+name,gitblob(b)==LOCKS[name],gitblob(b))
    return b

def extract_exact(source, names, label):
    tree=ast.parse(source.decode('utf-8'),filename=label)
    found={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name in names}
    check('LOCKED_SYMBOLS_'+label,set(found)==set(names),sorted(set(names)-set(found)))
    module=ast.Module(body=[found[n] for n in names],type_ignores=[])
    exec(compile(ast.fix_missing_locations(module),label,'exec'),globals())

def persist_manifest():
    tmp=Path(str(MANIFEST)+'.tmp')
    tmp.write_text(json.dumps({'test':TEST,'locks':LOCKS,'cartridges':entries,
                               'panel_sha256':R['panel_sha256']},ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    tmp.replace(MANIFEST)

def record_cp(cid,cp,role,parents,extra=None):
    check('CPU_CARTRIDGE_'+cid,cp['h'].device.type=='cpu' and all(k.device.type=='cpu' and v.device.type=='cpu' for k,v in cp['lower']))
    path=CART_DIR/(cid+'.pt')
    check('FRESH_CARTRIDGE_'+cid,not path.exists())
    temp=Path(str(path)+'.tmp');torch.save(cp,temp);temp.replace(path)
    meta={'id':cid,'role':role,'parents':[{'id':p,'sha256':entries[p]['sha256']} for p in parents],
          'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp),
          'body_tokens':int(cp['body_tokens']),'n':int(cp['n']),'p':int(cp['p'])}
    if extra: meta.update(extra)
    entries[cid]=meta;persist_manifest()
    check('PHYSICAL_SHA_'+cid,sha_file(path)==meta['sha256'])
    log('PHYSICAL_COMMIT',cid,meta['sha256'],'PARENTS',parents)
    return meta

# Fixed evaluation panel; sealed BEFORE downloading the official source.
QUESTIONS=[
 {'id':'Q01','question':'Identify the aircraft and occurrence described by the available investigative evidence. Distinguish observations from uncertainty.'},
 {'id':'Q02','question':'Which observations are documented? Identify the relevant evidence and what remains unverified.'},
 {'id':'Q03','question':'Develop two rival preliminary explanations and explain what observations could disconfirm each. Do not assume the final cause is known.'},
 {'id':'Q04','question':'What missing evidence would best distinguish the rival explanations, and why?'},
 {'id':'Q05','question':'Produce a preliminary evidence-limited assessment separating facts, inferences, and unresolved questions.'},
]
PANEL_BYTES=json.dumps(QUESTIONS,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
PANEL_SHA=sha(PANEL_BYTES)
(ROOT/'SEALED_QUESTIONS.json').write_bytes(PANEL_BYTES)
R['panel_sha256']=PANEL_SHA;save()

# The following imports are *function/class AST copies*, not rewritten motors.
# Importing definitions does not execute TEST730/745/757 experimental top-level code.
raw709=fetch_locked('709.py')
raw730=fetch_locked('730.py')
raw745=fetch_locked('745.py')
raw757=fetch_locked('757.py')
extract_exact(raw709, ['pairs','cache_build','replace','half','rope','rephase','sentinel',
                       'free_gpu','ensure_room','kv_digest','full_kv_seal','answer','mem'], '709.py')
extract_exact(raw730, ['DirectCut3','forge_native','initialize_native','to_gpu','seal_cp',
                       'memory_seals','compare_seals','safe_load','release'], '730.py')
extract_exact(raw757, ['native_append_direct','load_verified','build_fusion'], '757.py')
extract_exact(raw745, ['pdf_text','resolve_ain_reports','partition_preliminary'], '745.py')

# Preflight critical cross-file function dependencies before loading 72B weights.
# AST extraction deliberately omits source-level helper definitions unless requested.
ENGINE_DEPENDENCIES = {
    'forge_native': ('release', 'ensure_room', 'pairs', 'check', 'DirectCut3'),
    'initialize_native': ('release', 'ensure_room', 'DirectCut3', 'pairs'),
    'native_append_direct': ('release', 'ensure_room', 'rephase', 'cache_build', 'full_kv_seal'),
    'build_fusion': ('release', 'load_verified', 'native_append_direct', 'initialize_native'),
    'load_verified': ('safe_load', 'to_gpu'),
    'safe_load': ('seal_cp', 'sha_file', 'check'),
    'pdf_text': ('pymupdf',),
}
for _owner, _dependencies in ENGINE_DEPENDENCIES.items():
    check('DEPENDENCIES_'+_owner,
          callable(globals().get(_owner)) and all(
              callable(globals().get(_dependency)) or _dependency == 'pymupdf'
              for _dependency in _dependencies),
          [name for name in _dependencies if name not in globals()])

# Official case URL is taken from the LOCKED TEST745 AST, not a guessed PDF path.
def locked_case_url():
    tree=ast.parse(raw745.decode('utf-8'))
    for n in tree.body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASE_URL' for t in n.targets):
            return ast.literal_eval(n.value)
    raise RuntimeError('LOCKED_TEST745_CASE_URL_NOT_FOUND')
CASE_URL=locked_case_url()

# Source acquisition: only AIN preliminary PDF. The case HTML is used for link discovery,
# not as model evidence. The final PDF URL is never fetched.
def http_get(url,limit):
    request=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST758D'})
    with urllib.request.urlopen(request,timeout=180) as response:
        final_url=response.geturl();data=response.read(limit+1)
    check('HTTP_LIMIT',len(data)<=limit,len(data))
    host=urllib.parse.urlparse(final_url).hostname
    check('AIN_HOST',host in ('ain.hr','www.ain.hr'),host)
    return data,final_url

def retrieve_preliminary():
    page,_=http_get(CASE_URL,5_000_000)
    links=resolve_ain_reports(page)
    preliminary=[x for x in links['preliminary'] if x[0]=='preliminary report'] or links['preliminary']
    check('AIN_PRELIMINARY_LINK_FOUND',len(preliminary)>0)
    check('AIN_PRELIMINARY_LINK_UNAMBIGUOUS',len(set(u for _,u in preliminary))==1,preliminary)
    preliminary_url=preliminary[0][1]
    check('NO_FINAL_PDF_BEFORE_TEST',not (EVIDENCE_DIR/'AIN_FINAL.pdf').exists())
    raw,resolved=http_get(preliminary_url,40_000_000)
    check('PRELIMINARY_PDF_SIGNATURE',raw.startswith(b'%PDF-'))
    (EVIDENCE_DIR/'AIN_PRELIMINARY.pdf').write_bytes(raw)
    text,npages=pdf_text(raw)
    check('PRELIMINARY_TEXT_EXTRACTED',len(text)>=1400,{'pages':npages,'characters':len(text)})
    (EVIDENCE_DIR/'AIN_PRELIMINARY.txt').write_text(text,encoding='utf-8')
    R['source']={'case_url':CASE_URL,'preliminary_url':resolved,'pdf_sha256':sha(raw),
                 'extracted_sha256':sha(text.encode()),'pages':npages,
                 'case_page_sha256_quarantined':sha(page)}
    save()
    return text

@torch.no_grad()
def model_setup():
    global tok,PREFIX,PIDS,P,model,NL,H,QH,KVH,HD
    tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    # Identical to the verified TEST757 canonical prefix.
    PREFIX=('<|im_start|>system\nUse only the available document memory for document-specific questions. '
            'If evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n')
    PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',
                             bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,
              dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,
              trust_remote_code=False,attn_implementation='sdpa').eval()
    for param in model.parameters():param.requires_grad_(False)
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size)
    QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads)
    HD=int(getattr(cfg,'head_dim',None) or H//QH)
    check('MODEL_ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    check('FROZEN',all(not param.requires_grad for param in model.parameters()))
    check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))

# Compare tensors in bounded token chunks, not by copying entire 80-layer caches.
# The first 4 layers are expected to be exactly equal; upper-layer divergence
# is measured separately on old-prefix and appended-body positions.
@torch.no_grad()
def tensor_region_metrics(x, y, start, end, chunk=128):
    if tuple(x.shape) != tuple(y.shape):
        return {'shape_match':False,'shape_native':list(x.shape),'shape_reload':list(y.shape)}
    if not (0 <= start <= end <= x.shape[-2]):
        raise RuntimeError('INVALID_REGION_BOUNDS')
    n=0;sum_abs=0.;sum_sq=0.;sum_ref_sq=0.;max_abs=0.;equal=0
    dot=0.;norm_x=0.;norm_y=0.
    for a in range(start,end,chunk):
        b=min(a+chunk,end)
        xx=x[:,:,a:b,:].float()
        yy=y[:,:,a:b,:].float()
        delta=xx-yy
        count=delta.numel()
        n+=count
        sum_abs+=float(delta.abs().sum().item())
        sum_sq+=float(delta.square().sum().item())
        sum_ref_sq+=float(xx.square().sum().item())
        max_abs=max(max_abs,float(delta.abs().max().item()))
        equal+=int((xx==yy).sum().item())
        dot+=float((xx*yy).sum().item())
        norm_x+=float(xx.square().sum().item())
        norm_y+=float(yy.square().sum().item())
        del xx,yy,delta
    import math
    return {'shape_match':True,'tokens':end-start,'elements':n,
            'exact_fraction':equal/n if n else None,
            'max_abs':max_abs,'mean_abs':sum_abs/n if n else None,
            'rmse':math.sqrt(sum_sq/n) if n else None,
            'relative_l2':math.sqrt(sum_sq/max(sum_ref_sq,1e-30)) if n else None,
            'cosine':dot/max(math.sqrt(norm_x*norm_y),1e-30) if n else None}

@torch.no_grad()
def fuse_to_physical(parent_ids,fused_id):
    check('TWO_PARENTS',len(parent_ids)==2 and len(set(parent_ids))==2)
    expected_n=P+sum(entries[p]['body_tokens'] for p in parent_ids)
    first_n=P+entries[parent_ids[0]]['body_tokens']
    check('FUSION_TOKEN_BUDGET',expected_n<=MAX_FUSED_TOKENS,expected_n)
    memory=None;reloaded=None;gpu_cp=None
    try:
        memory,active,steps,seconds=build_fusion(parent_ids,'NATIVE_'+fused_id,strict_sha=True)
        check('ALL_PARENTS_ACTIVE',active==parent_ids,active)
        check('FUSED_LENGTH',int(memory[0][0].shape[-2])==expected_n,expected_n)
        original_seals=memory_seals(memory)
        h_parts=[]
        for idx,cid in enumerate(parent_ids):
            cp=safe_load(entries[cid]);check('PREFIX_MATCH_'+cid,cp['p']==P)
            h_parts.append(cp['h'].detach().cpu().contiguous() if idx==0 else
                           cp['h'][:,P:,:].detach().cpu().contiguous())
            del cp
        h=torch.cat(h_parts,dim=1).contiguous()
        check('FUSED_H3_SHAPE',tuple(h.shape)==(1,expected_n,H),tuple(h.shape))
        lower=tuple((memory[i][0].detach().cpu().contiguous(),
                     memory[i][1].detach().cpu().contiguous()) for i in range(CUT+1))
        cp={'h':h,'lower':lower,'n':expected_n,'p':P,
            'body_tokens':expected_n-P,'book_id':fused_id}
        record_cp(fused_id,cp,'DIRECT_NATIVE_NUMERICAL_FUSION',parent_ids)
        del cp,h,lower,h_parts
        release()
        disk_cp=safe_load(entries[fused_id]);gpu_cp=to_gpu(disk_cp);del disk_cp
        reloaded=list(initialize_native(gpu_cp))
        check('RELOADED_LAYER_COUNT',len(reloaded)==NL,len(reloaded))
        reloaded_seals=memory_seals(reloaded)
        parity=compare_seals(original_seals,reloaded_seals)
        layer_parity=[a==b for a,b in zip(original_seals,reloaded_seals)]
        R['fusion']={'id':fused_id,'parents':parent_ids,'active':active,'steps':steps,
                     'native_append_seconds':seconds,'tokens':expected_n,
                     'file_sha256':entries[fused_id]['sha256'],
                     'exact_80_layer_parity':bool(parity),
                     'layer_parity':layer_parity,
                     'first_parent_end':first_n,
                     'regions':{'old_parent':[0,first_n], 'appended_parent':[first_n,expected_n]}}
        save()
        log('EXACT_80_LAYER_PARITY','PASS' if parity else 'FAIL',
            'LAYERS',sum(layer_parity),'/',NL)
        # IMPORTANT: parity failure is the subject of this diagnostic, not a
        # reason to abort before measuring divergence. Never mark it PASS.
        diagnostics=[]
        for layer in range(NL):
            row={'layer':layer,'exact_sha':layer_parity[layer]}
            if layer_parity[layer]:
                row['status']='EXACT_SHA'
            else:
                row['status']='NUMERIC_DIVERGENCE'
                for kind,idx in (('K',0),('V',1)):
                    x=memory[layer][idx];y=reloaded[layer][idx]
                    row[kind]={
                        'old_parent':tensor_region_metrics(x,y,0,first_n),
                        'appended_parent':tensor_region_metrics(x,y,first_n,expected_n),
                    }
            diagnostics.append(row)
            if not layer_parity[layer]:
                log('DIVERGENCE_LAYER',layer,
                    'K_OLD_MAX',row['K']['old_parent'].get('max_abs'),
                    'K_NEW_MAX',row['K']['appended_parent'].get('max_abs'),
                    'V_OLD_MAX',row['V']['old_parent'].get('max_abs'),
                    'V_NEW_MAX',row['V']['appended_parent'].get('max_abs'))
            R['layer_diagnostics']=diagnostics
            save()
        # Answer equivalence is independent of bitwise cache parity.
        # Keep both 80-layer caches alive only during this small 5-question panel.
        paired=[]
        for q in QUESTIONS:
            native_raw=answer(memory,q['question'])
            reload_raw=answer(reloaded,q['question'])
            native_ids=tok(native_raw,add_special_tokens=False).input_ids
            reload_ids=tok(reload_raw,add_special_tokens=False).input_ids
            prefix=0
            for aa,bb in zip(native_ids,reload_ids):
                if aa!=bb:break
                prefix+=1
            paired.append({'id':q['id'],'native':native_raw,'reload':reload_raw,
                           'exact_text':native_raw==reload_raw,
                           'native_tokens':len(native_ids),'reload_tokens':len(reload_ids),
                           'common_prefix_tokens':prefix})
            log('NATIVE_VS_RELOAD',q['id'],'EXACT_TEXT',native_raw==reload_raw,
                'COMMON_PREFIX_TOKENS',prefix)
            R['paired_answers']=paired;save()
        check('PHYSICAL_S01_STILL_VERIFIED',
              sha_file(CART_DIR/(fused_id+'.pt'))==entries[fused_id]['sha256'])
        return bool(parity)
    finally:
        del memory,reloaded,gpu_cp
        release()

@torch.no_grad()
def physical_answer(cid,question):
    cpu=safe_load(entries[cid]);gpu_cp=to_gpu(cpu);del cpu
    memory=None
    try:
        memory=list(initialize_native(gpu_cp))
        before=memory_seals(memory)
        response=answer(memory,question)
        check('READ_ONLY_'+cid,compare_seals(before,memory_seals(memory)))
        return response
    finally:
        del memory,gpu_cp
        release()

def run_arm(cid):
    answers=[]
    for q in QUESTIONS:
        start=time.perf_counter()
        raw=physical_answer(cid,q['question'])
        row={'id':q['id'],'question':q['question'],'raw':raw,
             'answer_sha256':sha(raw.encode()),'seconds':round(time.perf_counter()-start,3)}
        answers.append(row)
        log('QA',cid,q['id'],repr(raw))
    R['trials'].append({'arm':cid,'answers':answers,'semantic_grade':'PENDING_INDEPENDENT_REVIEW'})
    save()

try:
    log('='*108)
    log('AKBASCORE SILICON HIPPOCAMPUS — TEST758D / NUMERICAL PARITY DIAGNOSIS')
    log('='*108)
    log('GPU',GPU_INFO.name,'GiB',round(GPU_INFO.total_memory/2**30,2))
    log('TORCH',torch.__version__,'TRANSFORMERS',transformers.__version__)
    log('LOCKS',LOCKS)
    log('RUN_ROOT',ROOT,'PANEL_SHA256',PANEL_SHA)
    check('PANEL_PRESEALED',sha((ROOT/'SEALED_QUESTIONS.json').read_bytes())==PANEL_SHA)
    # Fetch only the preliminary PDF, never the final report.
    extracted=retrieve_preliminary()
    model_setup()
    weights_before=sentinel()
    parts=partition_preliminary(extracted)
    # TEST745's partition_preliminary returns decoded text; re-tokenize each
    # segment exactly as TEST745 did when forging, without truncation.
    for cid in ('C01','C02'):
        body=parts[cid]
        ids=tok(body,add_special_tokens=False).input_ids
        check('SOURCE_NONEMPTY_'+cid,len(ids)>=30,len(ids))
        check('SOURCE_WITHIN_BUDGET_'+cid,len(ids)+P<=MAX_FUSED_TOKENS,len(ids))
        cp,seconds=forge_native(ids,cid)
        record_cp(cid,cp,'AIN_PRELIMINARY_SEGMENT',[],{'forge_seconds':seconds,
                 'body_sha256':sha(body.encode())})
        del cp;release()
    parity=fuse_to_physical(['C01','C02'],'S01')
    for cid in ('C01','C02','S01'):run_arm(cid)
    for cid in ('C01','C02','S01'):
        cp=safe_load(entries[cid]);del cp
    check('MODEL_WEIGHTS_UNCHANGED',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    check('PANEL_UNCHANGED',sha((ROOT/'SEALED_QUESTIONS.json').read_bytes())==PANEL_SHA)
    R['status']='COMPLETE_PARITY_PASS_PENDING_SEMANTICS' if parity else 'COMPLETE_DIAGNOSTIC_NONPARITY'
    R['summary']={'physical_sources':2,'physical_fused_cartridges':1,
                  'fusion':'TEST757 native numerical append / persistent compact CUT3',
                  'text_mediated_fusion':False,'exact_80_layer_parity':R['fusion']['exact_80_layer_parity'],
                  'semantic_grade':'PENDING_INDEPENDENT_REVIEW','autonomous_research':'NOT_TESTED'}
    R['summary']['parity_failure_is_recorded']=not parity
    R['summary']['diagnostic_layers']=len(R.get('layer_diagnostics',[]))
    R['summary']['paired_answer_questions']=len(R.get('paired_answers',[]))
    save();log('TEST758D_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()
    save();log('TEST758D_FAILED',repr(e));log(R['traceback']);raise
finally:
    save()
