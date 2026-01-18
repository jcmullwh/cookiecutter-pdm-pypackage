import argparse
import logging
import os
from pathlib import Path
import subprocess
import sys
import zipfile

logging.basicConfig(level=logging.INFO)

ARTIFACTS_DIRNAME = "_artifacts"
DEFAULT_DIFF_FILENAME = "working-tree.diff"
DEFAULT_SNAPSHOT_FILENAME = "repo-snapshot.zip"


def run_git(command, cwd=None, text=False):
    try:
        return subprocess.check_output(["git", *command], cwd=cwd, text=text)  # noqa: S603
    except FileNotFoundError:
        logging.error("git executable not found. Ensure git is installed and on PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        logging.error("git %s failed with exit code %s.", " ".join(command), exc.returncode)
        sys.exit(exc.returncode)


def repo_root():
    root = run_git(["rev-parse", "--show-toplevel"], text=True).strip()
    if not root:
        logging.error("Unable to determine git repository root.")
        sys.exit(1)
    return Path(root)


def artifacts_dir(root):
    output_dir = root / ARTIFACTS_DIRNAME
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_diff(root, output_dir):
    diff_bytes = run_git(["diff", "--no-color"], cwd=root)
    output_path = output_dir / DEFAULT_DIFF_FILENAME
    output_path.write_bytes(diff_bytes)
    logging.info("Saved diff to %s", output_path)


def write_snapshot(root, output_dir):
    output_path = output_dir / DEFAULT_SNAPSHOT_FILENAME
    file_list = run_git(["ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root)
    paths = [os.fsdecode(path) for path in file_list.split(b"\0") if path]
    paths = sorted(paths)
    if output_path.exists():
        output_path.unlink()
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel_path in paths:
            if rel_path.startswith(f"{ARTIFACTS_DIRNAME}/"):
                continue
            file_path = root / rel_path
            if file_path == output_path:
                continue
            try:
                archive.write(file_path, arcname=rel_path)
            except FileNotFoundError:
                logging.error("Unable to read file for snapshot: %s", rel_path)
                sys.exit(1)
            except OSError as exc:
                logging.error("Unable to read file for snapshot %s: %s", rel_path, exc)
                sys.exit(1)
    logging.info("Saved snapshot to %s", output_path)


def parse_args():
    parser = argparse.ArgumentParser(description="Capture git diffs and repo snapshots.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("diff", help="Write a working tree diff to _artifacts.")
    subparsers.add_parser("snapshot", help="Write a zip snapshot to _artifacts.")
    return parser.parse_args()


def main():
    args = parse_args()
    root = repo_root()
    output_dir = artifacts_dir(root)
    if args.command == "diff":
        write_diff(root, output_dir)
    elif args.command == "snapshot":
        write_snapshot(root, output_dir)


if __name__ == "__main__":
    main()
