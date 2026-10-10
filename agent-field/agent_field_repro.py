#!/usr/bin/env python3
"""Agent Field v0.2: separate-process agents, synthetic carriers only.
Usage: python agent_field_repro.py experiment 24 25
       python agent_field_repro.py experiment 12 12
Requires numpy, cryptography. Touches no real memory dumps, devices, or sectors.
"""
import base64
import json
from pathlib import Path
import secrets
import struct
import subprocess
import sys
import tempfile
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b'AFIELD-SIMULATED-v1\x00'
DUMP = 32768
SECTORS = 512 * 160


def qbasis():
    j = np.arange(128)[:, None]
    k = np.arange(1, 9)[None, :]
    return np.sqrt(2 / 128) * np.cos(np.pi * (j + 0.5) * k / 128)


def params(seed):
    r = np.random.default_rng(seed)
    target = r.uniform(-.8, .8, 4)
    initial = r.uniform(-3.2, 3.2, 4)
    return initial, target, np.array([.7, 1.6, 2.8, 4.2])


def optimize(q, v, target, curvature, n):
    q, v = q.copy(), v.copy()
    for _ in range(n):
        v = .88 * v + .035 * curvature * (q - target)
        q -= v
    return q, v


def loss(q, target, curvature):
    return float(.5 * np.dot(curvature, (q - target) ** 2))


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def head(seed):
    return dict(schema='agent-field-synthetic-v0.2', sender='algorithmic-agent-A',
                recipient='algorithmic-agent-B', session=f'trial-{seed}',
                sequence=1, codec='dct128-8', state_type='optimizer-q-v')


def image(data, offset, total):
    b = bytearray(secrets.token_bytes(total))
    b[offset:offset + len(MAGIC)] = MAGIC
    at = offset + len(MAGIC)
    b[at:at + 4] = struct.pack('>I', len(data))
    b[at + 4:at + 4 + len(data)] = data
    return bytes(b)


def read_image(b, offset):
    if b[offset:offset + len(MAGIC)] != MAGIC:
        raise ValueError('Laboratory marker missing')
    at = offset + len(MAGIC)
    (size,) = struct.unpack('>I', b[at:at + 4])
    if not 0 < size <= 16384 or at + 4 + size > len(b):
        raise ValueError('Invalid record size')
    return b[at + 4:at + 4 + size]


def agent_a(work, seed, before):
    q, target, curvature = params(seed)
    q, v = optimize(q, np.zeros(4), target, curvature, before)
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    field = (qbasis() @ np.r_[q, v]).tolist()
    metadata = head(seed)
    cipher = AESGCM(key).encrypt(nonce, dump({'field': field}), dump(metadata))
    envelope = dump(dict(header=metadata, nonce=base64.b64encode(nonce).decode(),
                         ciphertext=base64.b64encode(cipher).decode()))
    work.mkdir(parents=True, exist_ok=True)
    (work / 'key.local').write_bytes(key)
    (work / 'position.json').write_bytes(dump({'q': q.tolist()}))
    (work / 'direct.bin').write_bytes(envelope)
    (work / 'synthetic_dump.bin').write_bytes(image(envelope, DUMP, 131072))
    (work / 'synthetic_sectors.img').write_bytes(image(envelope, SECTORS, 262144))
    print(dump({'ok': True}).decode())


def agent_b(work, seed, carrier, check_replay=True):
    _, target, curvature = params(seed)
    if carrier == 'position':
        q = np.array(json.loads((work / 'position.json').read_bytes())['q'])
        v = np.zeros(4)
    else:
        names = {'direct': ('direct.bin', 0), 'dump': ('synthetic_dump.bin', DUMP),
                 'sectors': ('synthetic_sectors.img', SECTORS)}
        name, offset = names[carrier]
        raw = (work / name).read_bytes()
        packet = raw if carrier == 'direct' else read_image(raw, offset)
        env = json.loads(packet)
        if env['header'] != head(seed):
            raise ValueError('Invalid envelope context')
        journal = work / f'journal-{carrier}.txt'
        if check_replay and journal.exists():
            raise ValueError('Replay rejected')
        nonce = base64.b64decode(env['nonce'], validate=True)
        cipher = base64.b64decode(env['ciphertext'], validate=True)
        key = (work / 'key.local').read_bytes()
        field = np.array(json.loads(AESGCM(key).decrypt(nonce, cipher,
                                                         dump(head(seed))))['field'])
        if field.shape != (128,) or not np.isfinite(field).all():
            raise ValueError('Invalid field')
        state = qbasis().T @ field
        q, v = state[:4], state[4:]
        if check_replay:
            journal.write_text('seen')
    q, v = optimize(q, v, target, curvature, 9)
    print(dump({'carrier': carrier, 'loss': loss(q, target, curvature)}).decode())


def child(*args):
    p = subprocess.run([sys.executable, __file__, *map(str, args)],
                       text=True, capture_output=True, check=True)
    return json.loads(p.stdout)


def experiment(n, before):
    scores = {name: [] for name in ('position', 'direct', 'dump', 'sectors')}
    with tempfile.TemporaryDirectory(prefix='agent-field-') as folder:
        for seed in range(1, n + 1):
            work = Path(folder) / str(seed)
            child('send', work, seed, before)
            for carrier in scores:
                scores[carrier].append(child('receive', work, seed, carrier)['loss'])
    print(json.dumps({'trials': n, 'sender_steps': before, 'receiver_steps': 9,
                      'mean_loss': {k: float(np.mean(v)) for k, v in scores.items()},
                      'equal_carriers': all(np.allclose(scores['direct'], scores[x],
                                                        rtol=0, atol=1e-10)
                                            for x in ('dump', 'sectors')),
                      'agent_type': 'separate algorithmic processes, not LLMs',
                      'carriers': 'synthetic files only, never real dumps or raw disk'},
                     indent=2))


if __name__ == '__main__':
    if sys.argv[1] == 'send':
        agent_a(Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif sys.argv[1] == 'receive':
        agent_b(Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif sys.argv[1] == 'experiment':
        experiment(int(sys.argv[2]), int(sys.argv[3]))
    else:
        raise SystemExit('Use: experiment TRIALS SENDER_STEPS')
