"""Run this member's suite in the Flask project root."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

MEMBER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MEMBER_DIR.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parallel", action="store_true", help="use pytest-xdist workers")
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER)
    options = parser.parse_args()
    extra = options.pytest_args
    if extra and extra[0] == "--":
        extra = extra[1:]
    command = [
        sys.executable, "-m", "pytest", "-c", str(MEMBER_DIR / "pytest.ini"),
        str(MEMBER_DIR / "tests"),
    ]
    if options.parallel:
        command.extend(["-n", "auto"])
    command.extend(extra)
    env = os.environ.copy()
    env["APP_ROOT"] = str(PROJECT_ROOT)
    return subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
