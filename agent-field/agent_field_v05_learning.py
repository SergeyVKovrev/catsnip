#!/usr/bin/env python3
"""Agent Field 0.5: authorized cross-process knowledge persistence experiment.

This agent learns a synthetic 4D binary classification task via online logistic SGD.
Each independently launched process scans only its own file-backed mmap,
recovers trained weights from authenticated encrypted records, learns on unseen
synthetic samples, and publishes another private local record. No LLM weights,
ChatGPT memory, real RAM dumps, or other users' state are touched.

Requires local agent_field_v04.py and cryptography; Python 3.10+.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import mmap
import os
from pathlib import Path
import random
import secrets
from agent_field_v04 import (
    initialize, get_head, full_scan, pack, commit_head, SLOT, MAGIC, enc,
)

TEACHER=(1.35, -0.85, 1.05, -0.65)
MEMO='agent-field-v05-learning-linear-classifier-not-an-llm'
LR=0.05

def example(index: int):
    rng=random.Random(1000003*index+217)
    x=[rng.gauss(0,1) for _ in range(4)]
    latent=sum(t*v for t,v in zip(TEACHER,x))+0.2*rng.gauss(0,1)
    return x,int(latent>0)

def fit_one(w, index):
    x,y=example(index)
    logits=sum(a*b for a,b in zip(w,x))
    prob=1.0/(1.0+math.exp(-max(-30.0,min(30.0,logits))))
    return [a+LR*(y-prob)*b for a,b in zip(w,x)]

def accuracy(w):
    correct=0
    for i in range(100000,101000):
        x,y=example(i)
        correct += (sum(a*b for a,b in zip(w,x))>=0)==bool(y)
    return correct/1000

def new_state():
    # q stores learned classifier weights. v is reserved for future optimizer data.
    # The state is simple learned parameters, NOT a hidden neural network state.
    return {'seq':0,'iteration':0,'q':[0.0]*4,'v':[0.0]*4,
            'origin_fingerprint':secrets.token_hex(16),
            'provenance_chain':hashlib.sha256(b'agent-field-v05-learn-origin').hexdigest(),
            'memo':MEMO}

def read_private(root):
    key,path=initialize(root)
    head=get_head(root,key)
    with path.open('r+b') as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_WRITE) as mm:
        state,stats=full_scan(mm,key,head)
    if state is not None and state.get('memo')!=MEMO:
        raise ValueError('Wrong state type: not a learning-agent checkpoint')
    return state,stats

def learn(root: Path, samples: int):
    if not 1 <= samples <= 5000: raise ValueError('samples must be 1..5000')
    key,path=initialize(root)
    head=get_head(root,key)
    with path.open('r+b') as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_WRITE) as mm:
        previous,stats=full_scan(mm,key,head)
        if previous is not None and previous.get('memo')!=MEMO:
            raise ValueError('Wrong state type')
        state=previous if previous is not None else new_state()
        start=state['iteration']
        weights=state['q'][:]
        fresh=[0.0]*4
        for index in range(start,start+samples):
            weights=fit_one(weights,index)
            fresh=fit_one(fresh,index)
        state['q']=weights
        state['iteration']+=samples
        state['seq']+=1
        state['provenance_chain']=hashlib.sha256(enc([
            state['provenance_chain'],state['origin_fingerprint'],state['seq'],
            state['iteration']])).hexdigest()
        record,sha=pack(state,key)
        vacant=[s for s in range(len(mm)//SLOT)
                if mm.find(MAGIC,s*SLOT,(s+1)*SLOT)<0]
        if len(vacant)<2: raise RuntimeError('No two empty private memory slots')
        slots=[vacant.pop(secrets.randbelow(len(vacant))),
               vacant.pop(secrets.randbelow(len(vacant)))]
        for slot in slots:
            offset=slot*SLOT+64+secrets.randbelow(SLOT-len(record)-128)
            mm[offset:offset+len(record)]=record
        mm.flush();os.fsync(f.fileno())
        commit_head(root,{'seq':state['seq'],'sha':sha},key)
    return {'sequence':state['seq'],'samples_before':start,
            'samples_after':state['iteration'],'recovered':previous is not None,
            'origin_fingerprint':state['origin_fingerprint'],
            'heldout_accuracy_recovered':accuracy(weights),
            'heldout_accuracy_fresh_same_new_samples':accuracy(fresh),
            'heldout_items':1000,'records_seen_before':stats['candidates'],
            'private_memory_bytes':stats['mapped_bytes']}

def inspect(root:Path):
    state,stats=read_private(root)
    return {'found':state is not None,'state_type':state.get('memo') if state else None,
            'trained_samples':state['iteration'] if state else 0,
            'heldout_accuracy':accuracy(state['q']) if state else None,
            'origin_fingerprint':state['origin_fingerprint'] if state else None,
            'candidates':stats['candidates']}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['learn','inspect'])
    ap.add_argument('--dir',type=Path,required=True)
    ap.add_argument('--samples',type=int,default=40)
    args=ap.parse_args()
    print(json.dumps(learn(args.dir,args.samples) if args.action=='learn'
                     else inspect(args.dir),ensure_ascii=False,indent=2))
