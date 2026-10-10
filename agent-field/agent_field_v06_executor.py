#!/usr/bin/env python3
"""Agent Field 0.6-RC1 independent checkpoint executor, Python >=3.10 stdlib.
Usage: python agent_field_v06_executor.py START_CHECKPOINT_V06.json
No RAM dumps or other users' memory are read.
"""
import copy, hashlib, json, math, sys
from pathlib import Path
N=8
TEACHER=[0.65,-0.4,0.2,0.7,-0.6,0.1,0.9,-0.3]
def canonical(o):
    return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
def sha(o): return hashlib.sha256(canonical(o)).hexdigest()
def example(i):
    x=[(((i+1)*(j+2)*7+3*j)%29-14)/14.0 for j in range(N)]
    y=sum(TEACHER[j]*x[j] for j in range(N))-0.15
    return x,y
def batch(k): return [example(3*(k-1)+j) for j in range(3)]
def loss(s,items):
    return sum(.5*(sum(w*x for w,x in zip(s['weights'],xs))+s['bias']-y)**2 for xs,y in items)/len(items)
def update(old):
    new=copy.deepcopy(old)
    k=old['step']+1
    g=[0.0]*9
    data=batch(k)
    for xs,y in data:
        err=sum(old['weights'][j]*xs[j] for j in range(N))+old['bias']-y
        for j in range(N): g[j]+=err*xs[j]/len(data)
        g[N]+=err/len(data)
    a,b=.9,.999
    updated=[]
    for j,p in enumerate(old['weights']+[old['bias']]):
        m=a*old['adam_m'][j]+(1-a)*g[j]
        v=b*old['adam_second_moment'][j]+(1-b)*g[j]**2
        new['adam_m'][j]=m
        new['adam_second_moment'][j]=v
        updated.append(p-.045*(m/(1-a**k))/(math.sqrt(v/(1-b**k))+1e-8))
    new['weights']=updated[:N]
    new['bias']=updated[N]
    new['step']=k
    new['state_id']=old['run_id']+'/step-'+str(k)
    new['parent_state_sha256']=sha(old)
    new['history']=(old['history']+[loss(new,data)])[-16:]
    return new
def main():
    source=Path(sys.argv[1] if len(sys.argv)>1 else 'START_CHECKPOINT_V06.json')
    data=json.loads(source.read_text(encoding='utf-8'))
    state=data['state']
    if state['schema_version']!='agent-field/0.6-rc1' or state['run_id']!='AF06-20261011-ADAM8' or state['step']!=3:
        raise ValueError('Unexpected source state')
    if sha(state)!=data['state_sha256'] or sha(state)!='a29e371cc036298bb9dca81e71fe13edaea6452fe75e9d51f5ed125827b9f08c':
        raise ValueError('Incoming checkpoint SHA-256 mismatch')
    assert len(state['weights'])==8 and len(state['adam_m'])==len(state['adam_second_moment'])==9
    new=update(update(state))
    wrapped={'state':new,'state_sha256':sha(new)}
    print(json.dumps({'envelope':wrapped,'last_training_loss':new['history'][-1],
                      'holdout_loss':loss(new,[example(i) for i in range(500,550)])},
                     indent=2,ensure_ascii=False,allow_nan=False))
if __name__=='__main__': main()
