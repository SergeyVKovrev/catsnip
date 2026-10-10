#!/usr/bin/env python3
"""Agent Field 0.4 -- file-backed mapped-memory 'crumbs' proof of concept.

The program scans ONLY its own allocated, private file-backed memory mapping.
It does not access other processes, crash dumps, raw sectors, or OS memory.
Each command is a fresh program process. Crumbs are authenticated/encrypted.

Python 3.10+ and cryptography package required.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import mmap
import os
from pathlib import Path
import secrets
import struct
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b'AGENT-FIELD-OWN-MAPPED-MEMORY-04\x00'
SCHEMA = 'agent-field-v0.4-lab'
SLOT = 32 * 1024
DEFAULT_SLOTS = 64
TARGET = [0.5, -0.75, 0.25, 1.0]
CURV = [0.75, 1.2, 2.0, 3.5]
INITIAL = [3.0, -2.5, 2.1, -1.0]


def enc(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'), sort_keys=True,
                      allow_nan=False).encode('utf-8')


def private_write_once(path, data):
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def key_for(root):
    keyfile = root / 'lab-secret.key'
    if not keyfile.exists():
        try:
            private_write_once(keyfile, secrets.token_bytes(32))
        except FileExistsError:
            pass
    key = keyfile.read_bytes()
    if len(key) != 32:
        raise ValueError('Damaged lab key')
    return key


def state_initial():
    return {
        'seq': 0,
        'iteration': 0,
        'q': INITIAL[:],
        'v': [0.0] * 4,
        'origin_fingerprint': secrets.token_hex(16),
        'provenance_chain': hashlib.sha256(b'agent-field-origin').hexdigest(),
        'memo': 'Дальше продолжать вычисление, а не начинать его заново.'
    }


def iterate(state, n):
    for _ in range(n):
        state['v'] = [0.88 * state['v'][i] + 0.035 * CURV[i] *
                      (state['q'][i] - TARGET[i]) for i in range(4)]
        state['q'] = [state['q'][i] - state['v'][i] for i in range(4)]
    state['iteration'] += n
    state['seq'] += 1
    state['provenance_chain'] = hashlib.sha256(enc([
        state['provenance_chain'], state['origin_fingerprint'],
        state['seq'], state['iteration']
    ])).hexdigest()


def loss(state):
    return 0.5 * sum(CURV[i] * (state['q'][i] - TARGET[i])**2 for i in range(4))


def head_tag(d, key):
    return hmac.new(key, enc(d), hashlib.sha256).hexdigest()


def get_head(root, key):
    path = root / 'last-commit.json'
    if not path.exists():
        return None
    d = json.loads(path.read_text())
    signature = d.pop('hmac', None)
    if not signature or not hmac.compare_digest(head_tag(d, key), signature):
        raise ValueError('Bad last-commit authentication')
    return d


def commit_head(root, head, key):
    d = dict(head)
    d['hmac'] = head_tag(head, key)
    temp = root / ('head-tmp-' + secrets.token_hex(4))
    private_write_once(temp, enc(d))
    os.replace(temp, root / 'last-commit.json')


def pack(state, key):
    meta = {'schema': SCHEMA, 'seq': state['seq'],
            'scope': 'own-file-backed-mmap', 'codec': 'numeric-state-v1'}
    nonce = secrets.token_bytes(12)
    cipher = AESGCM(key).encrypt(nonce, enc(state), enc(meta))
    envelope = enc({'meta': meta, 'nonce': base64.b64encode(nonce).decode(),
                    'ciphertext': base64.b64encode(cipher).decode()})
    record = MAGIC + struct.pack('>I', len(envelope)) + envelope
    if len(record) > SLOT - 1024:
        raise ValueError('Too long for safe image slot')
    return record, hashlib.sha256(envelope).hexdigest()


def unpack(payload, key):
    packet = json.loads(payload)
    meta = packet['meta']
    if meta.get('schema') != SCHEMA or meta.get('scope') != 'own-file-backed-mmap' \
       or meta.get('codec') != 'numeric-state-v1':
        raise ValueError('Wrong authorized record context')
    nonce = base64.b64decode(packet['nonce'], validate=True)
    ct = base64.b64decode(packet['ciphertext'], validate=True)
    state = json.loads(AESGCM(key).decrypt(nonce, ct, enc(meta)))
    if (not isinstance(state.get('seq'), int) or meta.get('seq') != state['seq']
        or not isinstance(state.get('iteration'), int) or state['iteration'] < 0
        or len(state['q']) != 4 or len(state['v']) != 4):
        raise ValueError('Corrupt or unsupported state')
    return state


def initialize(root):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    key = key_for(root)
    path = root / 'field-owned.mmap'
    if not path.exists():
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        with os.fdopen(fd, 'r+b') as f:
            f.truncate(DEFAULT_SLOTS * SLOT)
            for _ in range(DEFAULT_SLOTS):
                f.write(secrets.token_bytes(SLOT))
            f.flush(); os.fsync(f.fileno())
    return key, path


def full_scan(field, key, head):
    """Scan whole allocated mapping for recognizable encrypted crumbs."""
    found, invalid, matches = 0, 0, []
    pos = 0
    while True:
        p = field.find(MAGIC, pos)
        if p < 0:
            break
        pos = p + 1
        after = p + len(MAGIC)
        if after + 4 > len(field):
            invalid += 1; continue
        count = struct.unpack('>I', field[after:after+4])[0]
        if not 0 < count < SLOT-1024 or after + 4 + count > len(field):
            invalid += 1; continue
        found += 1
        raw = field[after + 4:after + 4 + count]
        try:
            st = unpack(raw, key)
            sha = hashlib.sha256(raw).hexdigest()
            if head is not None and st['seq'] == head['seq'] and sha == head['sha']:
                matches.append(st)
        except Exception:
            invalid += 1
    if head is not None and not matches:
        raise RuntimeError('Missing latest committed crumb: refuse silent reset/rollback')
    if head is None and found:
        raise RuntimeError('Detected uncommitted breadcrumbs without a valid head')
    return (matches[0] if matches else None), {'candidates': found,
                 'invalid': invalid, 'matching_copies': len(matches),
                 'mapped_bytes': len(field)}


def inspect(root):
    key, path = initialize(root)
    head = get_head(root, key)
    with path.open('r+b') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE) as mm:
        state, stats = full_scan(mm, key, head)
    return {'restored': state is not None, 'head_sequence': (head or {}).get('seq'),
            'state': state, 'scan': stats, 'loss': loss(state) if state else None}


def step(root, n):
    if not 1 <= n <= 10000:
        raise ValueError('steps should be 1..10000')
    key, path = initialize(root)
    head = get_head(root, key)
    with path.open('r+b') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE) as mm:
        previous, stats = full_scan(mm, key, head)
        state = previous if previous is not None else state_initial()
        was_restored = previous is not None
        before = state['iteration']
        iterate(state, n)
        record, sha = pack(state, key)
        vacant = []
        for slot in range(len(mm) // SLOT):
            if mm.find(MAGIC, slot * SLOT, (slot + 1) * SLOT) < 0:
                vacant.append(slot)
        if len(vacant) < 2:
            raise RuntimeError('Not enough free slots: run grow')
        slots = [vacant.pop(secrets.randbelow(len(vacant))),
                 vacant.pop(secrets.randbelow(len(vacant)))]
        for slot in slots:
            offset = slot * SLOT + secrets.randbelow(SLOT - len(record) - 128) + 64
            mm[offset:offset+len(record)] = record
        mm.flush()
        os.fsync(f.fileno())
        commit_head(root, {'seq': state['seq'], 'sha': sha}, key)
        return {'restored_previous_generation': was_restored,
                'steps_before': before, 'steps_after': state['iteration'],
                'sequence': state['seq'], 'loss': loss(state),
                'origin_fingerprint': state['origin_fingerprint'],
                'provenance_chain': state['provenance_chain'],
                'memo_found': state['memo'] if was_restored else None,
                'previous_scan': stats, 'new_record_replicas': 2}


def grow(root, mib):
    key, path = initialize(root)
    head = get_head(root, key)
    with path.open('r+b') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE) as mm:
            before, stats1 = full_scan(mm, key, head)
            old_size = len(mm)
        size = mib * 1024 * 1024
        if size <= old_size or size % SLOT:
            raise ValueError('Expansion must be larger and aligned to 32KiB')
        f.seek(old_size)
        for _ in range((size - old_size) // SLOT):
            f.write(secrets.token_bytes(SLOT))
        f.flush(); os.fsync(f.fileno())
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE) as mm:
            after, stats2 = full_scan(mm, key, head)
    if before != after:
        raise AssertionError('Expanded field did not preserve prior state')
    return {'previous_bytes': old_size, 'expanded_bytes': size,
            'same_state_after_growth': True, 'restored_origin':
            after['origin_fingerprint'] if after else None,
            'scan_before': stats1, 'scan_after': stats2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['step', 'inspect', 'grow'])
    ap.add_argument('--dir', required=True, type=Path)
    ap.add_argument('--steps', type=int, default=10)
    ap.add_argument('--to-mib', type=int, default=4)
    args = ap.parse_args()
    if args.command == 'step':
        result = step(args.dir, args.steps)
    elif args.command == 'grow':
        result = grow(args.dir, args.to_mib)
    else:
        result = inspect(args.dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
