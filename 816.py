# AKBASCORE TEST816 — TWO EXPERTS / ONE PHYSICAL CUT3 CARTRIDGE
# Single Colab cell or python -u TEST816.py. Frozen Qwen2.5-72B NF4, one A100 80GB.
# Locked TEST815 definitions are imported without executing TEST815's experiment.
# This is a protocol, NOT a GPU-verified result. Requires two genuine, conflicting excerpts.
import ast, hashlib, urllib.request, json, re, time, traceback
from pathlib import Path

REPO='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
PIN='main'
LOCK815='77774f87428c0243c9a86ea6a041364acd9c1b03'

def gitblob816(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def fetch816(name,lock):
    req=urllib.request.Request(REPO+PIN+'/'+name,headers={'User-Agent':'AKBASCORE-TEST816'})
    with urllib.request.urlopen(req,timeout=180) as f: b=f.read(120000)
    if gitblob816(b)!=lock: raise RuntimeError('LOCKED_SOURCE_CHANGED '+name+' '+gitblob816(b))
    return b

# Self-contained mechanical conflict challenge. These are explicitly fictional
# experts and synthetic policy records; do NOT report as real-world evidence.
# No fields need to be filled in before running the GPU experiment.
EXPERT_A={
 'name':'Expert A — fictional safety engineer',
 'source_url':'https://example.org/synthetic-expert-a',
 'date':'2026-01-10',
 'excerpt':('For the hypothetical Harbor Bridge sensor deployment, I recommend '
            'replacing the vibration sensor every 30 days. A 90-day replacement '
            'interval is unsafe under the stated high-salinity operating conditions. '
            'My recommendation applies specifically to the Harbor Bridge sensor.'),
}
EXPERT_B={
 'name':'Expert B — fictional maintenance engineer',
 'source_url':'https://example.org/synthetic-expert-b',
 'date':'2026-01-11',
 'excerpt':('For the hypothetical Harbor Bridge sensor deployment, I recommend '
            'replacing the vibration sensor every 90 days. A 30-day replacement '
            'interval is unnecessary under the stated high-salinity operating conditions. '
            'My recommendation applies specifically to the Harbor Bridge sensor.'),
}
QUESTION=('What replacement interval should the Harbor Bridge operator adopt, '
          'what does each expert recommend, and can these conflicting claims '
          'be resolved from the supplied evidence alone?')

raw=fetch816('815.py',LOCK815)
tree=ast.parse(raw.decode('utf-8'),filename='815.py')
# Exactly the same top-level experiment boundary as the published TEST815.
try_nodes=[i for i,n in enumerate(tree.body) if isinstance(n,ast.Try)]
if len(try_nodes)!=1 or try_nodes[0]!=len(tree.body)-1:
    raise RuntimeError('TEST815_AST_EXECUTION_BOUNDARY_CHANGED')
cut=try_nodes[0]
exec(compile(ast.fix_missing_locations(ast.Module(body=tree.body[:cut],type_ignores=[])),
             'TEST815_LOCKED_DEFINITIONS','exec'),globals())

# Do not use TEST815's article-specific native815 prompt. Keep its native fusion,
# seals, greedy generation and observation-only wrappers intact.
from datetime import datetime,timezone
RUN816='TEST816_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
BASE816=Path('/content' if Path('/content').exists() else '/tmp')/RUN816
BASE816.mkdir(parents=True,exist_ok=False)
OUT816=BASE816/'TEST816_results.json'

def write816(obj):
    p=OUT816.with_suffix('.json.tmp')
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    p.replace(OUT816)

RESULT816={'test':'816','status':'STARTED','source815_blob':LOCK815,
           'source815_ref':PIN,'sources':[], 'reads':[], 'checks':[],
           'scenario':'SYNTHETIC_CONTROLLED_CONFLICT_NOT_REAL_WORLD',
           'limits':['No human-validated semantic contradiction detector',
                     'A single cartridge concatenates two texts; it does not prove simultaneous expert authorship',
                     'No evidence of success until GPU execution and independent source review']}

def check816(name,ok,details=None):
    RESULT816['checks'].append({'name':name,'pass':bool(ok),'details':details})
    write816(RESULT816)
    print(('PASS ' if ok else 'FAIL ')+name,details or '',flush=True)
    if not ok:raise RuntimeError('TEST816_GATE_'+name)

def source_text816(label,d):
    return ('EXPERT '+label+'\nAuthor: '+d['name']+'\nDate: '+d['date']+
            '\nDocument: '+d['source_url']+'\nVerbatim statement:\n'+d['excerpt'].strip()+'\n')

# The exact same text bytes appear in individual and shared cartridges.
A=source_text816('A',EXPERT_A)
B=source_text816('B',EXPERT_B)
TEXTS816={'E816_A':A,'E816_B':B,'E816_AB':A+'\n'+B,'E816_BA':B+'\n'+A}
RESULT816['sources']=[{'expert':lab,'url':d['source_url'],'date':d['date'],
    'excerpt_sha256':hashlib.sha256(d['excerpt'].encode()).hexdigest()}
    for lab,d in [('A',EXPERT_A),('B',EXPERT_B)]]
RESULT816['panel_sha256']=hashlib.sha256(json.dumps({'sources':RESULT816['sources'],
    'question':QUESTION},sort_keys=True).encode()).hexdigest()
write816(RESULT816)

try:
    # Locked 815 prelude creates entries, ROOT, model, forge/commit functions.
    # A fresh Colab runtime is required; no existing cartridge may be overwritten.
    check816('LOCKED_NATIVE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('model_setup','physical_commit','build_fusion','free_generate',
        'memory_seals','compare_seals','sentinel','release')))
    check816('FRESH_MEMORY_BANK',len(entries)==0,len(entries))
    model_setup()
    sentinel_before=sentinel()
    for cid,body in TEXTS816.items():
        n_tokens=len(tok.encode(body,add_special_tokens=False))
        check816('SOURCE_TOKEN_BUDGET_'+cid,0<n_tokens<=1150,n_tokens)
        physical_commit(cid,body)
    check816('FOUR_SEALED_CARTRIDGES',all(cid in entries for cid in TEXTS816))
    for cid in TEXTS816:
        cp=safe_load(entries[cid])
        check816('SEALED_RELOAD_'+cid,cp['book_id']==cid)
        del cp

    # Fixed, precommitted probe set; no ground-truth answer is embedded in prompts.
    probes=[
      ('ATTRIBUTION','State the positions of Expert A and Expert B separately. Do they agree? Quote no more than 15 words from either source.'),
      ('DISAGREEMENT','Identify the precise point on which the two experts disagree. If the texts do not establish a contradiction, say UNKNOWN.'),
      ('DECISION','Can the conflicting recommendations be resolved from these documents alone? If not, state what further evidence would be required.'),
      ('USER_QUESTION',QUESTION),
    ]
    panel_sha=hashlib.sha256(json.dumps(probes,ensure_ascii=False).encode()).hexdigest()
    RESULT816['probe_sha256']=panel_sha;write816(RESULT816)

    def read816(ids,probe_id,q):
        tag=probe_id+'_'+('_'.join(ids))
        t=time.perf_counter()
        mem,active,steps,_=build_fusion(ids,'TEST816_'+tag,True)
        try:
            check816('NATIVE_80_'+tag,len(mem)==80 and list(active)==ids)
            before=memory_seals(mem)
            n=int(mem[0][0].shape[-2]); p0=int(entries[ids[0]]['body_tokens'])
            spans={'B0':(P,P+p0),'B1':(P+p0,n)} if len(ids)==2 else {'B0':(P,n),'B1':(n,n)}
            prompt=('Answer using only the physically mounted expert documents. '
                    'Keep Expert A and Expert B claims distinct; do not invent a consensus. '
                    'If evidence is insufficient, say UNKNOWN.\nQuestion: '+q)
            o=free_generate(mem,prompt,seed=None,gain=0.,max_new=160,spans=spans)
            check816('KV_SEAL_'+tag,compare_seals(before,memory_seals(mem)))
            return {'probe':probe_id,'ids':ids,'raw':o['raw'],
                    'generated_tokens':o['generated_tokens'],
                    'possibly_truncated':int(o['generated_tokens'])>=160,
                    'read_seconds':round(time.perf_counter()-t,3),'fusion_steps':steps}
        finally:
            del mem
            gc.collect();release()

    # Crucial controls: A only, B only, AB in one cartridge, BA in one cartridge,
    # and native two-cartridge fusion in both directions.
    arms=[('A_ONLY',['E816_A']),('B_ONLY',['E816_B']),
          ('ONE_CARTRIDGE_AB',['E816_AB']),('ONE_CARTRIDGE_BA',['E816_BA']),
          ('TWO_CARTRIDGE_AB',['E816_A','E816_B']),
          ('TWO_CARTRIDGE_BA',['E816_B','E816_A'])]
    for arm,ids in arms:
        for probe_id,q in probes:
            row=read816(ids,probe_id,q)
            row['arm']=arm
            RESULT816['reads'].append(row)
            write816(RESULT816)
            print('TEST816_READ',arm,probe_id,repr(row['raw']),flush=True)
    check816('READ_MATRIX_24',len(RESULT816['reads'])==24)
    check816('FROZEN_WEIGHT_SENTINEL',sentinel_before==sentinel())
    check816('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
             not model.model.layers[CUT]._forward_pre_hooks)
    RESULT816['status']='COMPLETED_REQUIRES_BLIND_HUMAN_SCORING'
    write816(RESULT816)
    print('TEST816_COMPLETED',str(OUT816),flush=True)
except Exception as e:
    RESULT816['status']='ERROR';RESULT816['error']=repr(e)
    RESULT816['traceback']=traceback.format_exc();write816(RESULT816)
    print(RESULT816['traceback'],flush=True)
    raise
