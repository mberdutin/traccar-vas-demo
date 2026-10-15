#!/usr/bin/env python3
"""Promote the exact successful managed CI SHA without repeating its checks."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

REPO = "mberdutin/traccar-vas-demo"


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--image", required=True)
    parser.add_argument("--evidence-url", required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text())
    assert report["status"] == "PASS"
    assert report["ci_image"] == args.image and "@sha256:" in args.image
    sha = report["source_sha"]
    assert re.fullmatch("[0-9a-f]{40}", sha)
    assert command("git", "rev-parse", "HEAD") == sha
    assert command("git", "rev-parse", "HEAD^{tree}") == report["source_tree"]
    assert not command("git", "status", "--porcelain")
    assert (
        command("git", "remote", "get-url", "origin").rstrip("/").removesuffix(".git")
        == f"https://github.com/{REPO}"
    )
    for name, digest in report["build_files"].items():
        assert (
            hashlib.sha256((Path("build") / name).read_bytes()).hexdigest() == digest
        ), name
    subprocess.run(["git", "fetch", "origin", "main:refs/remotes/origin/main"], check=True)
    assert command("git", "rev-parse", "origin/main") == report["base_main_sha"], (
        "Main advanced since CI: run again on the new base"
    )
    status = {
        "state": "success",
        "context": "vas/kubernetes-ci",
        "description": "Managed sandbox: unit, lint, build, desktop/mobile and real API PASS",
        "target_url": args.evidence_url,
    }
    subprocess.run(
        [
            "gh",
            "api",
            "--method",
            "POST",
            f"repos/{REPO}/statuses/{sha}",
            "--input",
            "-",
            "--silent",
        ],
        input=json.dumps(status),
        text=True,
        check=True,
    )
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", "origin/main", sha], check=True
    )
    # Normal push is fast-forward checked by GitHub. A concurrent main update fails.
    subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            "credential.helper=!gh auth git-credential",
            "push",
            "origin",
            f"{sha}:refs/heads/main",
        ],
        check=True,
    )
    print("PROMOTED", sha)


if __name__ == "__main__":
    main()
