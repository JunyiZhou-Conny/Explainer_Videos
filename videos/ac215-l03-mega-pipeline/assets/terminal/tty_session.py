#!/usr/bin/env python3
"""Run one command in a pseudo-terminal (80x40 by default, TTY_COLS/TTY_ROWS) the way a person would: wait
for each shell prompt ("... $ "), type the next line from <typed_lines_file> (none if the file is empty),
and save what the terminal finally shows: scrollback plus screen, rendered with the `pyte` terminal
emulator when it is installed (needed for docker build's live progress display, which redraws in place),
otherwise with ANSI sequences removed and carriage-return overwrites resolved.
Usage: tty_session.py <out_file> <typed_lines_file> <command> [args...]
The first line of the file is "$ " + $SHOW_CMD (default: the command itself); the last is "[exit N]",
like run_steps.sh's step files."""
import fcntl, os, pty, re, select, struct, sys, termios, time

out_path, typed_path, cmd = sys.argv[1], sys.argv[2], sys.argv[3:]
COLS, ROWS = int(os.environ.get('TTY_COLS', 80)), int(os.environ.get('TTY_ROWS', 40))
typed = [l for l in open(typed_path).read().splitlines() if l.strip()]
ANSI = re.compile(rb'\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[()][A-Za-z0-9]|\x1b[=>78]')

pid, fd = pty.fork()
if pid == 0:
    fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', ROWS, COLS, 0, 0))
    os.environ['TERM'] = 'xterm-256color'
    os.execvp(cmd[0], cmd)

buf = b''


def pump(until_prompt, timeout):
    global buf
    end = time.time() + timeout
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if not r:
            continue
        try:
            data = os.read(fd, 65536)
        except OSError:
            return False
        if not data:
            return False
        buf += data
        if until_prompt and re.search(rb'\$ $', ANSI.sub(b'', buf[-400:])):
            r2, _, _ = select.select([fd], [], [], 0.5)   # nothing else still arriving
            if not r2:
                return True
    return False


for line in typed:
    if not pump(True, 600):
        break
    time.sleep(0.2)
    os.write(fd, line.encode() + b'\r')
pump(False, 1800)
_, status = os.waitpid(pid, 0)
code = os.waitstatus_to_exitcode(status)

try:
    import pyte
    screen = pyte.HistoryScreen(COLS, ROWS, history=100000, ratio=0.001)
    screen.set_mode(pyte.modes.LNM)          # the pty already turned \n into \r\n
    stream = pyte.ByteStream(screen)
    stream.feed(buf)
    rows = [''.join(r[x].data for x in range(COLS)) for r in screen.history.top]
    rows += screen.display
    lines = [r.rstrip() for r in rows]
except ImportError:
    text = ANSI.sub(b'', buf).decode('utf-8', 'replace').replace('\r\n', '\n')
    lines = []
    for ln in text.split('\n'):
        if '\r' in ln.rstrip('\r'):
            ln = ln.rstrip('\r').split('\r')[-1]
        lines.append(ln.rstrip('\r').rstrip())
while lines and not lines[-1]:
    lines.pop()
with open(out_path, 'w') as f:
    f.write('$ ' + (os.environ.get('SHOW_CMD') or ' '.join(cmd)) + '\n')
    f.write('\n'.join(lines) + '\n')
    f.write('[exit %d]\n' % code)
