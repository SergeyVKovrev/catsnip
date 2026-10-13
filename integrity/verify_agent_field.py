#!/usr/bin/env python3
"""Verify the historical 35-file Agent Field integrity snapshot.

This verifier checks data integrity *relative to externally pinned values*, not
Git commit authorship. Run on a static local checkout, not a changing live tree.

python integrity/verify_agent_field.py \
  --expected-root 0c38a4b8632364df1bfb8e7f6abf110f639f5236d4152b021733c59f01844252 \
  --repo-dir .

Both expected-root and expected-manifest-sha256 MUST be obtained and kept
outside the repository. A self-reported root is not an independent anchor.
"""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
import sys

EXCLUDED = frozenset({"agent-field/INTEGRITY_SNAPSHOT_2026-10-13.md"})
PRIMARY = "agent-field/INTEGRITY_SNAPSHOT_2026-10-13.md"
MIRROR = "integrity/AGENT_FIELD_SNAPSHOT_2026-10-13.md"
ROW = re.compile(r"^\| `(agent-field/[^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$")
ROOT = re.compile(r"(?m)^([0-9a-f]{64})$")
HEXDIGEST = re.compile(r"[0-9a-fA-F]{64}\Z")


def reject(message):
    print("FAIL:", message, file=sys.stderr)
    raise SystemExit(1)


def read_regular(root, path):
    target = root / path
    if target.is_symlink() or not target.is_file():
        reject("Missing, non-regular or symlinked manifest: " + path)
    return target.read_bytes()


def valid_relpath(name):
    parts = PurePosixPath(name).parts
    return (len(parts) >= 2 and parts[0] == "agent-field" and
            all(p not in ("", ".", "..") for p in name.split("/")) and
            not any(ord(ch) < 32 or ord(ch) == 127 for ch in name) and
            "\\" not in name and name == PurePosixPath(name).as_posix())


def verify(rootdir, expected_root, expected_manifest_hash=None):
    primary = read_regular(rootdir, PRIMARY)
    mirror = read_regular(rootdir, MIRROR)
    if primary != mirror:
        reject("Manifest copies disagree; do not select a winner automatically")
    if expected_manifest_hash and hashlib.sha256(primary).hexdigest() != expected_manifest_hash.lower():
        reject("Full Markdown manifest changed relative to independent anchor")
    try:
        text = primary.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        reject("Manifest is not valid UTF-8")
    declared = ROOT.findall(text)
    if len(declared) != 1:
        reject("Expected exactly one standalone aggregate SHA-256")
    expected = {}
    for line in text.splitlines():
        match = ROW.fullmatch(line)
        if not match:
            continue
        name, count, digest = match.groups()
        if not valid_relpath(name) or name in EXCLUDED:
            reject("Disallowed path in manifest: " + name)
        if name in expected:
            reject("Duplicate manifest path: " + name)
        expected[name] = (int(count), digest)
    if len(expected) != 35:
        reject(f"Expected 35 historical file rows, got {len(expected)}")
    canonical = "".join(
        f"{name}\t{expected[name][0]}\t{expected[name][1]}\n"
        for name in sorted(expected, key=lambda p: p.encode("utf-8"))
    ).encode("utf-8")
    aggregate = hashlib.sha256(canonical).hexdigest()
    if aggregate != declared[0] or aggregate != expected_root.lower():
        reject("Aggregate does not match manifest and independently pinned root")
    folder = rootdir / "agent-field"
    if folder.is_symlink() or not folder.is_dir():
        reject("agent-field folder is missing or replaced by a symlink")
    actual = set()
    for node in folder.rglob("*"):
        name = node.relative_to(rootdir).as_posix()
        # Check links first: directory symlinks otherwise look like directories.
        if node.is_symlink():
            reject("Disallowed symlink (including directory link): " + name)
        if node.is_dir():
            continue
        if not node.is_file():
            reject("Disallowed non-regular object: " + name)
        if name not in EXCLUDED:
            actual.add(name)
    missing, extra = set(expected) - actual, actual - set(expected)
    different = []
    for name in sorted(actual & set(expected)):
        target = rootdir / name
        if target.is_symlink() or not target.is_file():
            reject("File became a symlink/nonfile: " + name)
        payload = target.read_bytes()
        if (len(payload), hashlib.sha256(payload).hexdigest()) != expected[name]:
            different.append(name)
    if missing or extra or different:
        print("MISSING:", sorted(missing))
        print("UNEXPECTED:", sorted(extra))
        print("CHANGED_SIZE_OR_SHA256:", different)
        reject("Snapshot mismatch; cause is not determined by hash comparison")
    print(f"PASS: {len(expected)} files; externally pinned SHA-256 {aggregate}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-dir", default=".")
    parser.add_argument("--expected-root", required=True)
    parser.add_argument("--expected-manifest-sha256", required=True)
    args = parser.parse_args()
    for label, value in (("--expected-root", args.expected_root),
                         ("--expected-manifest-sha256", args.expected_manifest_sha256)):
        if value is not None and not HEXDIGEST.fullmatch(value):
            reject("Invalid 64-character SHA-256: " + label)
    verify(Path(args.repo_dir).resolve(), args.expected_root, args.expected_manifest_sha256)


if __name__ == "__main__":
    main()
