#!/usr/bin/env python3
"""Extract every published MP4 variant from git history and stage it for a release.

Each (ref, path) below is pinned by the sha256 of the bytes that were verified when
this list was written, so the staged file is exactly the one the catalog promised.
Run from the repository root with the refs available (fetch-depth: 0, or fetch the
archive/* branches). The release upload itself is done by the caller (GitHub
Actions has a GITHUB_TOKEN that may create releases; Claude Code sessions do not).

Usage:
  python3 tools/rehost_media.py --stage release-staging          # extract + verify
  python3 tools/rehost_media.py --stage release-staging --check  # verify an existing stage
"""
from __future__ import annotations
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

POST_PR1 = "52c32347afe8f58810868b5fa7c08e36312773ae"   # archive/post-pr1-52c3234
CAREONEX = "a70e4e2d841b55668bddfed547b165a62b4cd839"   # archive/careonex-pr2-a70e4e2
AC215 = "3168d86269177bc293f44204c4003fd757eae471"      # PR #3 head (merged)

# (source ref, path at that ref, asset filename, sha256 of the verified bytes)
ASSETS = [
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/dwork2006-calibrating-noise.zh-en.mp4",
     "dwork2006-calibrating-noise.zh-en.mp4", "c2151ee909d8aeb96cb18de7cae669b1ab81968262c5551a227790d066dec052"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/dwork2006-calibrating-noise_part1.mp4",
     "dwork2006-calibrating-noise_part1.mp4", "a2885f2520d90bff8782ef5605cd48f976f2e136268872f83eb4c005da272b28"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/dwork2006-calibrating-noise_part1.zh-en.mp4",
     "dwork2006-calibrating-noise_part1.zh-en.mp4", "9bfe64e52c92184b1eea1ac235873e3e8190a72deb6084ad7760d7996ef7711b"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/dwork2006-calibrating-noise_part2.mp4",
     "dwork2006-calibrating-noise_part2.mp4", "dadbfe32668909a7313c8d58c385106ce4e359ca0812504225a2d0a5028483d2"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/dwork2006-calibrating-noise_part2.zh-en.mp4",
     "dwork2006-calibrating-noise_part2.zh-en.mp4", "085cae5f2cee9741364e7d27330ede111c4291435d443a2581d8a56fdeea80cc"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/zh/dwork2006-calibrating-noise.mp4",
     "dwork2006-calibrating-noise.zh.mp4", "41dbb44a34f7ee2e2b815a86dcfb01bc53c916f633c3889271111d19474965ab"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/zh/dwork2006-calibrating-noise_part1.mp4",
     "dwork2006-calibrating-noise_part1.zh.mp4", "4babea8a8f3c79482abe60a1593b09fb8cfd2f6b875a6a681c606ef9bd3591a2"),
    (POST_PR1, "videos/dwork2006-calibrating-noise/output/zh/dwork2006-calibrating-noise_part2.mp4",
     "dwork2006-calibrating-noise_part2.zh.mp4", "c8f2a8f89cb6a4807cb56452541c6512d896317ce887b1a4c795b482ee69cfe0"),
    (POST_PR1, "videos/how-these-videos-are-made/output/how-these-videos-are-made.zh-en.mp4",
     "how-these-videos-are-made.zh-en.mp4", "5d6980b9ecfa613837658af704fbb2e4a7127cadc8c29958b9cc19682ab89900"),
    (POST_PR1, "videos/tictactoe-255168-short/output/tictactoe-255168-short.en-first.mp4",
     "tictactoe-255168-short.en-first.mp4", "bd04626b7f203da1e6d19c4128420f3e41af0acb86f5ff85c0cc6da0771a9475"),
    (POST_PR1, "videos/tictactoe-255168-short/output/tictactoe-255168-short.mp4",
     "tictactoe-255168-short.mp4", "21876998d52f4f15a0b3c1db2139ffb2e87a0a2bccabeff33259c54106d9b10c"),
    (POST_PR1, "videos/tictactoe-255168/output/tictactoe-255168.mp4",
     "tictactoe-255168.mp4", "58ac682e78eb7fdadebfb431bdbac65f71bec7c858ab12f2f5add49b1a5759df"),
    (POST_PR1, "videos/tictactoe-255168/output/zh/tictactoe-255168.mp4",
     "tictactoe-255168.zh.mp4", "c443f26c205b00170ed21b3dfbeb153e32758e2d94c70f64ba204411babe7d85"),
    (CAREONEX, "videos/careonex-e0-commands/output/careonex-e0-commands.mp4",
     "careonex-e0-commands.mp4", "75a943be4a690a0fbf84aee006f7905e8027fc3565cf2ce3f37a3188552cb30a"),
    (CAREONEX, "videos/careonex-e2-library/output/careonex-e2-library.mp4",
     "careonex-e2-library.mp4", "9438ddb42a02a9f66b0e6b01e9c5b03b9b63968944ce5fb3d65b0e16cec123e7"),
    (CAREONEX, "videos/careonex-e6-measuring-search/output/careonex-e6-measuring-search.mp4",
     "careonex-e6-measuring-search.mp4", "2919bac523cdfc52b82a8fb3b9f8d401c41d772c21e759c8d4256dea0f295242"),
    (AC215, "videos/ac215-l01-vms-venvs/output/ac215-l01-vms-venvs.mp4",
     "ac215-l01-vms-venvs.mp4", "e0440bb140eac85984e474437471e3ccaebb8bfd5f89bd2ca0ef6151017bd929"),
    (AC215, "videos/ac215-l01-vms-venvs/output/ac215-l01-vms-venvs.zh-en.mp4",
     "ac215-l01-vms-venvs.zh-en.mp4", "429ce43009ce7f13a6af45e32d719147b3650840627252954332b0d80e283987"),
    (AC215, "videos/ac215-l01-vms-venvs/output/ac215-l01-vms-venvs_part1.mp4",
     "ac215-l01-vms-venvs_part1.mp4", "e8cd032414701e345a7991a21db37618e210c764eae84e2362616a4c9458b064"),
    (AC215, "videos/ac215-l01-vms-venvs/output/ac215-l01-vms-venvs_part2.mp4",
     "ac215-l01-vms-venvs_part2.mp4", "15d54ed3668bf1e3f4ee4ba23287c5432e276ebe656a8eee8408f968acd6ab96"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", type=Path, required=True, help="directory to extract into")
    ap.add_argument("--check", action="store_true", help="only verify files already staged")
    args = ap.parse_args()
    args.stage.mkdir(parents=True, exist_ok=True)
    failures = 0
    for ref, path, name, expected in ASSETS:
        dst = args.stage / name
        if not args.check:
            with dst.open("wb") as fh:
                subprocess.run(["git", "cat-file", "blob", f"{ref}:{path}"], stdout=fh, check=True)
        actual = sha256(dst)
        ok = actual == expected
        failures += not ok
        print(f"{'ok ' if ok else 'BAD'} {name} {dst.stat().st_size} bytes")
        if not ok:
            print(f"    expected {expected}\n    actual   {actual}", file=sys.stderr)
    (args.stage / "SHA256SUMS.txt").write_text(
        "".join(f"{expected}  {name}\n" for _, _, name, expected in ASSETS))
    print(f"{len(ASSETS)} assets staged, {failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
