#!/usr/bin/env python3
"""Additional fail-closed regression cases for Agent Field historical snapshot.

Run: python integrity/test_verify_agent_field_extended.py
These are synthetic tests, not a historical 35-file independent audit.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from test_verify_agent_field import setup, manifest_rows

CHECKER = Path(__file__).with_name("verify_agent_field.py")
FAILED = []


def run(root, expected_root, manifest_hash):
    return subprocess.run(
        [sys.executable, str(CHECKER), "--repo-dir", str(root),
         "--expected-root", expected_root,
         "--expected-manifest-sha256", manifest_hash],
        capture_output=True, text=True,
    )


def rewrite_both(root, transform):
    first = root / "agent-field" / "INTEGRITY_SNAPSHOT_2026-10-13.md"
    second = root / "integrity" / "AGENT_FIELD_SNAPSHOT_2026-10-13.md"
    payload = transform(first.read_bytes())
    first.write_bytes(payload)
    second.write_bytes(payload)
    return hashlib.sha256(payload).hexdigest()


def check(name, mutation, expected_diagnostic):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        original_root, original_manifest_hash = setup(root)
        pinned_root, pinned_manifest_hash = mutation(
            root, original_root, original_manifest_hash
        )
        result = run(root, pinned_root, pinned_manifest_hash)
        good = result.returncode != 0 and expected_diagnostic in result.stderr
        print(("PASS" if good else "FAIL"), name, "exit=", result.returncode,
              "reason=", (result.stderr or result.stdout).strip()[:180])
        if not good:
            FAILED.append(name)


def compromised_file_and_updated_manifests(root, old_root, old_manifest_hash):
    target = root / "agent-field" / "file_00.txt"
    target.write_text("CHANGED" + target.read_text())
    rows, new_root = manifest_rows(root)
    old_text = (
        root / "agent-field" / "INTEGRITY_SNAPSHOT_2026-10-13.md"
    ).read_text()
    new_rows = "".join(
        f"| `{p}` | {size} | `{digest}` |\n"
        for p, size, digest in rows
    )
    altered = old_text.replace(old_root, new_root)
    altered = re.sub(
        r"(?m)^\| `agent-field/file_\d\d\.txt` \| \d+ \| `[a-f0-9]{64}` \|$",
        "", altered
    )
    altered = altered.replace("|---|---:|---|\n", "|---|---:|---|\n" + new_rows)
    reanchored_markdown = rewrite_both(root, lambda _: altered.encode("utf-8"))
    # Root stays externally pinned to OLD value despite coherent updated files/manifests.
    return old_root, reanchored_markdown


def mutate_markdown(root, old_root, old_hash, operation):
    return old_root, rewrite_both(root, operation)


def duplicate(root, r, m):
    return mutate_markdown(
        root, r, m,
        lambda data: data +
        b"| `agent-field/file_00.txt` | 26 | `" + b"0" * 64 + b"` |\n"
    )


def traversal(root, r, m):
    return mutate_markdown(
        root, r, m,
        lambda data: data.replace(
            b"agent-field/file_00.txt", b"agent-field/../evil.txt"
        )
    )


def missing_row(root, r, m):
    return mutate_markdown(
        root, r, m,
        lambda data: re.sub(
            rb"(?m)^\| `agent-field/file_00\.txt`[^\n]*\n", b"", data
        )
    )


def bom(root, r, m):
    return mutate_markdown(root, r, m, lambda data: b"\xef\xbb\xbf" + data)


def crlf(root, r, m):
    return mutate_markdown(root, r, m,
                           lambda data: data.replace(b"\n", b"\r\n"))


def invalid_utf8(root, r, m):
    return mutate_markdown(root, r, m, lambda data: data + b"\xff")


def hardlinked_data(root, r, m):
    os.link(root / "agent-field" / "file_00.txt", root / "external_hardlink.txt")
    return r, m


def hardlinked_manifest(root, r, m):
    os.link(
        root / "agent-field" / "INTEGRITY_SNAPSHOT_2026-10-13.md",
        root / "outside_manifest_hardlink.md",
    )
    return r, m


def symlinked_integrity(root, r, m):
    (root / "integrity").rename(root / "real_integrity")
    (root / "integrity").symlink_to(
        "real_integrity", target_is_directory=True
    )
    return r, m


SCENARIOS = [
    ("modified-file-and-updated-manifest-stale-external-root",
     compromised_file_and_updated_manifests, "Aggregate does not match"),
    ("duplicate-row", duplicate, "Duplicate manifest path"),
    ("path-traversal", traversal, "Disallowed path"),
    ("missing-row", missing_row, "Expected 35 historical file rows"),
    ("UTF8-BOM", bom, "without BOM"),
    ("CRLF", crlf, "without BOM"),
    ("invalid-UTF8", invalid_utf8, "not valid UTF-8"),
    ("hardlink-data", hardlinked_data, "Hardlinked files are disallowed"),
    ("hardlink-manifest", hardlinked_manifest, "Manifest must not be a hardlink"),
    ("symlinked-integrity-dir", symlinked_integrity,
     "Missing or symlinked repository directory"),
]


def main():
    for name, mutator, reason in SCENARIOS:
        check(name, mutator, reason)
    if FAILED:
        raise SystemExit("FAILED: " + ", ".join(FAILED))
    print("ALL 10 EXTENDED SYNTHETIC REGRESSION CASES PASSED")


if __name__ == "__main__":
    main()
