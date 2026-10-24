#!/usr/bin/env python3
"""Run a command in a pseudo-terminal, type into it like a person would, and print what the
terminal finally shows. Used by run_steps.sh for the README's interactive steps
(`docker run --rm -ti ...`, then commands typed at the container's prompt).

Usage: ptyrun.py [--cols 80] [--rows 24] [--timeout 300] [--expect REGEX --send TEXT]... -- CMD...
Each --expect waits (on the screen text written since the previous send) for REGEX, then types
TEXT and Enter. After the last pair it waits for CMD to exit and prints the final screen +
scrollback: a minimal terminal emulator applies carriage returns, cursor-up/erase-line (Docker's
pull progress) and drops colours and title sequences. Exit status = CMD's exit status.
"""
import argparse
import fcntl
import os
import pty
import re
import select
import struct
import sys
import termios
import time

CSI = re.compile(r"\x1b\[([0-?]*)([ -/]*)([@-~])")
OSC = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
ESC2 = re.compile(r"\x1b[()][A-Za-z0-9]|\x1b[=>78DEMc]")


def render(text, raw=False):
    """Apply the cursor movements a terminal would, return the visible lines
    (raw=True: keep trailing blanks, for prompt matching)."""
    lines, row, col = [[]], 0, 0
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "\x1b":
            m = OSC.match(text, i)
            if m:
                i = m.end(); continue
            m = CSI.match(text, i)
            if m:
                args, final = m.group(1), m.group(3)
                nums = [int(a) if a.isdigit() else 0 for a in args.lstrip("?").split(";")] if args else []
                k = (nums[0] if nums and nums[0] else 1)
                if final == "A":
                    row = max(0, row - k)
                elif final == "B":
                    row += k
                elif final == "C":
                    col += k
                elif final == "D":
                    col = max(0, col - k)
                elif final == "G":
                    col = max(0, k - 1)
                elif final == "K":
                    while len(lines) <= row:
                        lines.append([])
                    mode = nums[0] if nums else 0
                    if mode == 0:
                        del lines[row][col:]
                    elif mode == 1:
                        lines[row][:col] = [" "] * min(col, len(lines[row]))
                    else:
                        lines[row] = []
                i = m.end(); continue
            m = ESC2.match(text, i)
            i = m.end() if m else i + 1
            continue
        while len(lines) <= row:
            lines.append([])
        if ch == "\r":
            col = 0
        elif ch == "\n":
            row += 1
            col = 0
        elif ch == "\b":
            col = max(0, col - 1)
        elif ch == "\x07":
            pass
        elif ch == "\t":
            col = (col // 8 + 1) * 8   # next tab stop, like a terminal
        elif ch >= " ":
            line = lines[row]
            if len(line) < col:
                line.extend([" "] * (col - len(line)))
            if col < len(line):
                line[col] = ch
            else:
                line.append(ch)
            col += 1
        i += 1
    if raw:
        return "\n".join("".join(l) for l in lines)
    out = ["".join(l).rstrip() for l in lines]
    while out and not out[-1]:
        out.pop()
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cols", type=int, default=80)
    ap.add_argument("--rows", type=int, default=24)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--expect", action="append", default=[])
    ap.add_argument("--send", action="append", default=[])
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    pairs = list(zip(a.expect, a.send))

    pid, fd = pty.fork()
    if pid == 0:
        fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack("HHHH", a.rows, a.cols, 0, 0))
        os.execvp(cmd[0], cmd)

    buf = b""
    mark = 0          # screen text length at the last send
    status = None
    deadline = time.time() + a.timeout

    def pump(wait):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], wait)
        if r:
            try:
                data = os.read(fd, 65536)
            except OSError:
                return False
            if not data:
                return False
            buf += data
        return True

    alive = True
    for rx, text in pairs:
        pat = re.compile(rx)
        while alive:
            screen = render(buf.decode("utf-8", "replace"), raw=True)
            if pat.search(screen, mark):
                break
            if time.time() > deadline:
                buf += f"\n[ptyrun: timed out waiting for /{rx}/]\n".encode()
                alive = False
                os.kill(pid, 9)
                break
            alive = pump(0.2)
        if not alive:
            break
        time.sleep(0.4)
        while pump(0.05) and select.select([fd], [], [], 0)[0]:
            pass  # drain what is already there, so the next search starts after it
        mark = len(render(buf.decode("utf-8", "replace"), raw=True))
        os.write(fd, text.encode() + b"\r")
    while alive and time.time() < deadline:
        alive = pump(0.2)
    try:
        _, st = os.waitpid(pid, 0)
        status = os.waitstatus_to_exitcode(st)
    except ChildProcessError:
        status = 1
    sys.stdout.write(render(buf.decode("utf-8", "replace")) + "\n")
    sys.stdout.flush()
    sys.exit(status if status >= 0 else 128 - status)


if __name__ == "__main__":
    main()
