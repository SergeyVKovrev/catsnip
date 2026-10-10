#!/usr/bin/env python3
"""Agent Field v0.6-RC1: audit candidate step-5 JSON from trusted step-3.
Usage: python verify_v06_submission.py START_CHECKPOINT.json CANDIDATE_STEP5.json
Python standard library; reads only explicitly passed user-authorized files.
"""
import json
import math
import sys
from pathlib import Path
from agent_field_v06_executor import sha, update, loss, example

TOL = 1e-12

def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def compare_recursive(a, b, path, differences):
    if isinstance(a, bool) or isinstance(b, bool):
        if a != b: differences.append(path + ': boolean mismatch')
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if not (math.isfinite(float(a)) and math.isfinite(float(b))):
            differences.append(path + ': nonfinite value')
        elif abs(a-b) > TOL:
            differences.append(path + ': numerical mismatch')
    elif isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b): differences.append(path + ': key sets differ')
        for k in sorted(set(a)&set(b)):
            compare_recursive(a[k], b[k], path+'.'+str(k), differences)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): differences.append(path + ': lengths differ')
        for i, (x,y) in enumerate(zip(a,b)):
            compare_recursive(x,y,path+'['+str(i)+']',differences)
    elif a != b:
        differences.append(path + ': value mismatch')

def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: verify_v06_submission.py START_CHECKPOINT.json CANDIDATE_STEP5.json')
    source, candidate = load(sys.argv[1]), load(sys.argv[2])
    step3 = source['state']
    if sha(step3) != source['state_sha256']:
        raise SystemExit('FAIL: incoming checkpoint digest mismatch')
    if step3['schema_version']!='agent-field/0.6-rc1' or step3['step']!=3:
        raise SystemExit('FAIL: unexpected input schema/step')
    if 'envelope' not in candidate and 'state' in candidate:
        candidate = {'envelope': candidate}
    if 'envelope' not in candidate or 'state' not in candidate['envelope']:
        raise SystemExit('FAIL: expected an envelope containing state')
    got = candidate['envelope']['state']
    errors = []
    if sha(got) != candidate['envelope'].get('state_sha256'):
        errors.append('candidate SHA256 inconsistent with state')
    step4 = update(step3)
    if got.get('parent_state_sha256') != sha(step4):
        errors.append('parent_state_sha256 must equal SHA256 of step-4 state')
    if got.get('step') != 5 or got.get('state_id') != step3['run_id']+'/step-5':
        errors.append('step/state_id mismatch')
    expected = update(step4)
    compare_recursive(expected, got, 'state', errors)
    if 'last_training_loss' in candidate:
        compare_recursive(expected['history'][-1], candidate['last_training_loss'], 'last_training_loss', errors)
    if 'holdout_loss' in candidate:
        compare_recursive(loss(expected,[example(i) for i in range(500,550)]),
                          candidate['holdout_loss'],'holdout_loss',errors)
    print(json.dumps({'ok':not errors, 'errors':errors[:30],
                      'total_errors':len(errors)},indent=2,ensure_ascii=False))
    raise SystemExit(1 if errors else 0)

if __name__ == '__main__':
    main()
