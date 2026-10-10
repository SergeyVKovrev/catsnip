"""Independent-process synthetic learning persistence verification."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT=Path(__file__).with_name('agent_field_v05_learning.py')

def cmd(action,root,*args):
    return subprocess.run([sys.executable,str(SCRIPT),action,'--dir',str(root),*args],
                          capture_output=True,text=True,check=True)

def main():
    with tempfile.TemporaryDirectory(prefix='af-v05-check-') as root:
        results=[]
        for i in range(6):
            results.append(json.loads(cmd('learn',root,'--samples','40').stdout))
        verify=json.loads(cmd('inspect',root).stdout)
        assert results[0]['recovered'] is False
        assert all(v['recovered'] for v in results[1:])
        assert all(v['origin_fingerprint']==results[0]['origin_fingerprint'] for v in results)
        assert verify['trained_samples']==240 and verify['candidates']==12
        assert verify['heldout_accuracy']==results[-1]['heldout_accuracy_recovered']
        assert results[-1]['heldout_accuracy_recovered']>results[-1]['heldout_accuracy_fresh_same_new_samples']
        fresh=json.loads(cmd('learn',str(Path(root)/'independent'),'--samples','40').stdout)
        assert fresh['origin_fingerprint'] != verify['origin_fingerprint']
        print(json.dumps({'six_distinct_processes':True,'same_origin_across_restarts':True,
                          'no_prior_state_in_independent_workspace':True,
                          'last_accuracy_recovered':verify['heldout_accuracy'],
                          'last_accuracy_cold':results[-1]['heldout_accuracy_fresh_same_new_samples'],
                          'total_records':verify['candidates']},indent=2))

if __name__=='__main__':
    main()
