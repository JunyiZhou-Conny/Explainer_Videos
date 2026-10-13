#!/usr/bin/env python3
"""Run one command in a pseudo-terminal (80x40 by default, TTY_COLS/TTY_ROWS) the way a person would, and
save what the terminal finally shows: scrollback plus screen, rendered with the `pyte` terminal emulator
when it is installed (needed for docker build's and docker compose's live progress views, which redraw in
place), otherwise with ANSI sequences removed and carriage-return overwrites resolved.

Usage: tty_session.py <out_file> <script_file> <command> [args...]

Each line of <script_file> is either a line to type or a directive:
  <text>              wait for a shell prompt (PROMPT_RE, default: "$ " or "# " at the end of the output),
                      then type <text> and Enter
  @@wait <regex>      wait until the output (ANSI removed) matches <regex>
  @@touch <path>      create <path> (tells run_steps.sh that this terminal reached a point)
  @@waitfile <path>   wait until <path> exists (run_steps.sh ran the commands of "another terminal")
  @@sleep <seconds>
  @@ctrl-c            press Ctrl+C
The first line of <out_file> is "$ " + $SHOW_CMD (default: the command itself); the last is "[exit N]",
like run_steps.sh's step files. Timings (Ctrl+C -> exit) go to $TIMING_FILE when it is set.
L04 version of the L03 helper (videos/ac215-l03-mega-pipeline/assets/terminal/tty_session.py), plus the
directives above."""
import fcntl, os, pty, re, select, struct, sys, termios, time

out_path, script_path, cmd = sys.argv[1], sys.argv[2], sys.argv[3:]
COLS, ROWS = int(os.environ.get('TTY_COLS', 80)), int(os.environ.get('TTY_ROWS', 40))
PROMPT = re.compile(os.environ.get('PROMPT_RE', r'[$#] $').encode())
script = [l for l in open(script_path).read().splitlines() if l.strip()]
ANSI = re.compile(rb'\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[()][A-Za-z0-9]|\x1b[=>78]')

pid, fd = pty.fork()
if pid == 0:
    fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', ROWS, COLS, 0, 0))
    os.environ['TERM'] = 'xterm-256color'
    os.execvp(cmd[0], cmd)

buf = b''
seen = 0          # bytes of buf already consumed by a successful wait
alive = True
t0 = time.time()
events = []


def read_some(timeout):
    global buf, alive
    r, _, _ = select.select([fd], [], [], timeout)
    if not r:
        return False
    try:
        data = os.read(fd, 65536)
    except OSError:
        alive = False
        return False
    if not data:
        alive = False
        return False
    buf += data
    return True


def wait_prompt(timeout=900):
    end = time.time() + timeout
    while alive and time.time() < end:
        if read_some(0.2) and PROMPT.search(ANSI.sub(b'', buf[-400:])):
            if not read_some(0.5):   # nothing else still arriving
                return True
    return False


def wait_regex(rx, timeout=900):
    global seen
    pat = re.compile(rx.encode())
    end = time.time() + timeout
    while alive and time.time() < end:
        m = pat.search(ANSI.sub(b'', buf[seen:]))
        if m:
            seen = len(buf)
            return True
        read_some(0.2)
    return False


for line in script:
    if line.startswith('@@'):
        op, _, arg = line[2:].partition(' ')
        if op == 'wait':
            wait_regex(arg)
        elif op == 'touch':
            open(arg, 'w').close()
        elif op == 'waitfile':
            while alive and not os.path.exists(arg):
                read_some(0.2)
        elif op == 'sleep':
            end = time.time() + float(arg)
            while alive and time.time() < end:
                read_some(0.1)
        elif op == 'ctrl-c':
            os.write(fd, b'\x03')
            events.append(('ctrl-c', time.time()))
        continue
    if not wait_prompt():
        break
    time.sleep(0.2)
    os.write(fd, line.encode() + b'\r')
end = time.time() + 1800
while alive and time.time() < end:
    read_some(0.5)
_, status = os.waitpid(pid, 0)
code = os.waitstatus_to_exitcode(status)
events.append(('exit', time.time()))

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
if os.environ.get('TIMING_FILE'):
    with open(os.environ['TIMING_FILE'], 'a') as f:
        marks = ' '.join('%s=+%.1fs' % (k, t - t0) for k, t in events)
        f.write('%s\t%s\n' % (os.path.basename(out_path), marks))
