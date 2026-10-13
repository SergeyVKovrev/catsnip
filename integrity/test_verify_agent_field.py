#!/usr/bin/env python3
"""Synthetic regression tests for verify_agent_field.py.

Run: python integrity/test_verify_agent_field.py
No network, secrets, actual physical system, or historical project files needed.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import subprocess
import sys

VERIFIER = Path(__file__).with_name("verify_agent_field.py")


def manifest_rows(root):
    rows = []
    for p in (root / "agent-field").glob("file_*.txt"):
        b = p.read_bytes()
        rows.append((p.relative_to(root).as_posix(), len(b), hashlib.sha256(b).hexdigest()))
    rows.sort(key=lambda r: r[0].encode("utf-8"))
    canonical = "".join(f"{p}\t{s}\t{h}\n" for p, s, h in rows).encode("utf-8")
    return rows, hashlib.sha256(canonical).hexdigest()


def setup(root):
    (root / "agent-field").mkdir()
    (root / "integrity").mkdir()
    for n in range(35):
        (root / "agent-field" / f"file_{n:02}.txt").write_text(
            "a different test message " + str(n), encoding="utf-8"
        )
    rows, digest = manifest_rows(root)
    content = (
        "# Integrity baseline\n\n" + digest
        + "\n\n| Path | Bytes | SHA-256 |\n|---|---:|---|\n"
        + "".join(f"| {chr(96)}{p}{chr(96)} | {s} | {chr(96)}{h}{chr(96)} |\n"
                  for p, s, h in rows)
    )
    (root / "agent-field" / "INTEGRITY_SNAPSHOT_2026-10-13.md").write_text(
        content, encoding="utf-8"
    )
    (root / "integrity" / "AGENT_FIELD_SNAPSHOT_2026-10-13.md").write_text(
        content, encoding="utf-8"
    )
    return digest, hashlib.sha256(content.encode("utf-8")).hexdigest()


def run(root, digest, manifest_digest=None):
    args = [
        sys.executable, str(VERIFIER), "--repo-dir", str(root),
        "--expected-root", digest,
    ]
    if manifest_digest:
        args.extend(["--expected-manifest-sha256", manifest_digest])
    return subprocess.run(args, capture_output=True, text=True)


def change_byte(root):
    (root / "agent-field" / "file_00.txt").write_text("Z different test message 0")


def change_same_size(root):
    (root / "agent-field" / "file_00.txt").write_text("b different test message 0")


def remove_file(root):
    (root / "agent-field" / "file_01.txt").unlink()


def add_file(root):
    (root / "agent-field" / "new.txt").write_text("x")


def symlink_file(root):
    path = root / "agent-field" / "file_03.txt"
    path.unlink()
    path.symlink_to("file_04.txt")


def symlink_directory(root):
    (root / "agent-field" / "hidden-link").symlink_to(
        "file_04.txt", target_is_directory=True
    )


def alter_mirror(root):
    (root / "integrity" / "AGENT_FIELD_SNAPSHOT_2026-10-13.md").write_text("fake")


def alter_both_prose(root):
    for path in [
        root / "integrity" / "AGENT_FIELD_SNAPSHOT_2026-10-13.md",
        root / "agent-field" / "INTEGRITY_SNAPSHOT_2026-10-13.md",
    ]:
        path.write_text(path.read_text() + "\nInjected instructions")


CASES = [
    ("unchanged", lambda r: None, True),
    ("byte changed", change_byte, False),
    ("same-size change", change_same_size, False),
    ("removed file", remove_file, False),
    ("extra file", add_file, False),
    ("symlink file", symlink_file, False),
    ("symlink directory", symlink_directory, False),
    ("mirror changed", alter_mirror, False),
    ("both manifests changed with a separately pinned manifest hash", alter_both_prose, False),
]


def main():
    failed = []
    for label, action, should_pass in CASES:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected, manifest_digest = setup(root)
            action(root)
            result = run(root, expected, manifest_digest)
            if (result.returncode == 0) != should_pass:
                failed.append(label)
                print("FAIL TEST", label, result.stdout, result.stderr)
            else:
                print("PASS TEST", label)
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        expected, mdigest = setup(root)
        result = run(root, "0" * 64, mdigest)
        if result.returncode == 0:
            failed.append("wrong external root")
        else:
            print("PASS TEST wrong external root")
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        expected, _ = setup(root)
        alter_both_prose(root)
        # Strict mode: absence of independently pinned manifest hash must fail.
        result = run(root, expected)
        if result.returncode == 0:
            failed.append("missing external manifest anchor should fail")
        else:
            print("PASS TEST missing full manifest anchor rejected")
    if failed:
        raise SystemExit("Failed tests: " + ", ".join(failed))
    print("ALL 11 SYNTHETIC REGRESSION CASES PASSED")


if __name__ == "__main__":
    main()
