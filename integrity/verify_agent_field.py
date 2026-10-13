#!/usr/bin/env python3
"""Verify Agent Field snapshot with an EXTERNALLY pinned SHA-256 root.

Run from repository root:
    python integrity/verify_agent_field.py --expected-root <64-hex-external-root>

Only read local repository files. Never auto-fix/overwrite or execute project code.
This baseline intentionally excludes its own two snapshot metadata copies and
the integrity/ verifier from the historical 35-file scope.
"""
import argparse
import hashlib
import pathlib
import re
import sys

EXCLUDED = {"agent-field/INTEGRITY_SNAPSHOT_2026-10-13.md"}
SNAPSHOT = "agent-field/INTEGRITY_SNAPSHOT_2026-10-13.md"
MIRROR = "integrity/AGENT_FIELD_SNAPSHOT_2026-10-13.md"
ROW = re.compile(r"^\| `(agent-field/[^\x60]+)` \| (\d+) \| `([0-9a-f]{64})` \|$")
ROOT = re.compile(r"(?m)^([0-9a-f]{64})$")


def fail(message):
    print("FAIL:", message, file=sys.stderr)
    raise SystemExit(1)


def load(rootdir, path):
    target = rootdir / path
    if target.is_symlink() or not target.is_file():
        fail("Missing or symlinked manifest: " + path)
    return target.read_bytes()


def verify(rootdir, trusted_root):
    primary = load(rootdir, SNAPSHOT)
    mirror = load(rootdir, MIRROR)
    if primary != mirror:
        fail("Manifest copies disagree. Stop; do not automatically choose one.")
    text = primary.decode("utf-8")
    root_matches = ROOT.findall(text)
    if len(root_matches) != 1:
        fail("Missing or ambiguous aggregate hash")
    asserted_root = root_matches[0]
    expected = {}
    for line in text.splitlines():
        m = ROW.fullmatch(line)
        if m:
            path, size, digest = m.groups()
            if path in expected:
                fail("Duplicate entry " + path)
            expected[path] = (int(size), digest)
    if len(expected) != 35 or any(x in expected for x in EXCLUDED):
        fail("Unexpected baseline entry count/scope")
    canonical = "".join(
        f"{path}\t{expected[path][0]}\t{expected[path][1]}\n"
        for path in sorted(expected, key=lambda p: p.encode("utf-8"))
    ).encode("utf-8")
    computed_root = hashlib.sha256(canonical).hexdigest()
    if computed_root != asserted_root or computed_root != trusted_root.lower():
        fail("Aggregate does not match manifest and independently pinned root")
    folder = rootdir / "agent-field"
    actual = set()
    for f in folder.rglob("*"):
        if f.is_dir():
            continue
        rel = f.relative_to(rootdir).as_posix()
        if rel in EXCLUDED:
            continue
        actual.add(rel)
        if f.is_symlink() or not f.is_file():
            fail("Unexpected special entry: " + rel)
    missing = set(expected) - actual
    added = actual - set(expected)
    differences = []
    for path in sorted(actual & set(expected)):
        payload = (rootdir / path).read_bytes()
        got = (len(payload), hashlib.sha256(payload).hexdigest())
        if got != expected[path]:
            differences.append(path)
    if missing or added or differences:
        print("MISSING:", sorted(missing))
        print("UNEXPECTED:", sorted(added))
        print("SIZE_OR_SHA256_DIFFERENCE:", differences)
        fail("Snapshot differs: this can be an authorized update, accident, or attack")
    print(f"PASS: {len(expected)} files verified against externally pinned {computed_root}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-root", required=True, help="An independently stored 64-hex SHA-256 fingerprint")
    parser.add_argument("--repo-dir", default=".", help="Local checkout root")
    options = parser.parse_args()
    if not re.fullmatch(r"[0-9a-fA-F]{64}", options.expected_root):
        fail("Invalid external root argument")
    verify(pathlib.Path(options.repo_dir).resolve(), options.expected_root)


if __name__ == "__main__":
    main()
