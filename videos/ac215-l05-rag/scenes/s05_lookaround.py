"""S05 · Names, mounts, and two traps (README "Run Container" step 3, all extras). Lecture: none.

Beats (script.md "## S05", one voiceover block each):
 0  TRACKER Run 3 · extra. V2 as a glyph-only thumbnail top left ("the picture" S04 built). A
    second terminal (8 rows, `laptop · second terminal`) opens on student@laptop:~$ with the GREY
    caption "new terminal: cd here first", then the prompt ~/AC215/llm-rag$. `docker ps` (extra)
    -> laptop/08 lines 2–4 as the column view (GREY tag "docker ps · PORTS and NAMES"):
    0.0.0.0:8000->8000/tcp PINK (the thumbnail's port route pulses), llm-rag-chromadb and
    llm-rag-llm-rag-cli-run-90678535ddef YELLOW (their boxes flash). Above: the excerpt chip
    docker-compose.yml · line 9 `container_name: llm-rag-cli` (the name struck RED) with the tag
    "erratum · not used by compose run".
 1  `docker inspect …` twice (laptop/15's `$` line, typed one after the other, extra; each folds):
    the name inside the first underlines YELLOW, GREY tag "yours differs · copy it from docker ps"
    on the docker ps row it came from. Lines 2, 3, 5 print; the thumbnail's app, secrets and data
    routes pulse PINK as their lines print.
 2  The container terminal (TEAL, app@92c5bfd26089:/app$, 8 rows): the env check (extra, folds)
    -> cli-container/01 lines 2–6. your-project-id YELLOW (the thumbnail's $ slots flash PINK);
    the path on line 3 becomes a PINK signpost pointing at an empty TEAL /secrets box; a GOLD
    dashed key outline sits where yours would be, tag "yours: the key file".
 3  `getent hosts …; curl …; echo` (extra, folds) -> cli-container/04 lines 2–3: line 2 PINK
    becomes V2's phone-book card on the thumbnail's rail, `llm-rag-chromadb → 172.19.0.2`. Then
    the second terminal: `curl http://localhost:8000/api/v2/heartbeat` (extra) -> laptop/10 line
    2; the thumbnail's 8000:8000 route and street door pulse. Heartbeats: "your numbers will differ".
 4  `ls -la docker-volumes/chromadb` (extra) -> laptop/13 lines 2–5; `root root` YELLOW. Beside
    the thumbnail, its chromadb folder at full size: GREY tag "made by Docker: the mount's source"
    (the data route pulses), then a GREY lock and "root's · Linux: sudo to delete".
 5  Trap 1 in the RED dashed frame `what if · just watch` (GREY "recorded after teardown"); the
    thumbnail stays inside it and its $ slots empty out. A fresh laptop terminal (8 rows) types
    `docker compose run --rm llm-rag-cli` (extra, RED tag "the wrong way") -> gotchas/01 lines
    2–3 joined, 4, … (word-folded); at app@2af936bbf5b9:/app$ it types the chunk command ->
    lines 17–19, …, 55 (55 RED, word-folded): a YELLOW box around the two spaces, tag "an empty
    file name"; the chip cli.py · line 35 `llm_client = genai.Client(` "runs at startup"; the
    slots blink RED, empty. A GREEN chip "always start with: sh docker-shell.sh".
 6  Trap 2 in the same frame: a laptop terminal (student@laptop:~/AC215-zip$, 9 rows) types the
    clone-as-llm-rag-main line (extra) -> gotchas/03 lines 2–4, GREY tag "what a zip download
    unpacks"; above, the GREY ~/AC215-zip folder with llm-rag-main/ and secrets/. The prompt
    becomes ~/AC215-zip/llm-rag-main$ (GREY caption "after cd llm-rag-main"); `sh
    docker-shell.sh` -> gotchas/04 lines 2–7, line 7 RED. The PINK route ../llm-rag → /app reaches
    for a folder that isn't there; a GREY dashed llm-rag folder (root) pops into existence and
    slides over /app, hiding the code. `ls -la ..; ls -la ../llm-rag` (extra) -> gotchas/05 lines
    2, 5–6, 8–10 (root YELLOW). Fix card: "keep the name llm-rag (or mount .:/app)" · "delete the
    stray folder (sudo on Linux)".
 7  The frame leaves; the TEAL container terminal returns as a 3-row strip, GREY caption "back in
    your container". Above: docker-compose.yml · line 19 `image: chromadb/chroma:latest` (latest
    underlined), three version chips "tag 1.5.9" · "chroma 1.4.4" (laptop/11b line 2) · 'API
    "1.0.0"' (laptop/11 line 2), "at the time of recording", GREY "team tip: pin a tag in
    docker-compose.yml · line 19". Then ▶ your turn on a static GREY card in two groups
    (container: the env check; second terminal, in llm-rag: docker ps · curl · ls) with a GOLD
    note "yours: llm-service-account.json listed" (the env check folded at its "; " so the card's rows
    paste back as one valid command). Hold 2 s, empty frame.

Deviations from SHOW (see the scene report): V2 is shown as S04's glyph-only thumbnail (the full
V2 does not fit above an 8-row terminal); the container terminal and the trap-1 terminal have 8
rows (not 9 and 12) so that the thumbnail fits above them, inside the what-if frame too.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    ShowIncreasingSubsets,
    TransformFromCopy,
    VGroup,
    VMobject,
    linear,
)

from common import (
    COST,
    CTR,
    DATA,
    ERR,
    INK,
    KEY_FILE,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_CTR,
    P_G5,
    P_REPO,
    P_ZIP,
    P_ZIP_REPO,
    TURN,
    ComposeView,
    STRIP_TOP,
    Prose,
    _drop_bare,
    bare_prompt,
    beside,
    build_row,
    capture,
    caption_extra,
    cd_prompt,
    col_box,
    column_view,
    differ_tag,
    erratum_tag,
    excerpt,
    excerpt_chip,
    extra_tag,
    file_row,
    fix_chip,
    grey_tag,
    key_outline,
    note,
    padlock,
    pin,
    place_time,
    recording_tag,
    second_terminal,
    signpost,
    strip_top,
    term,
    time_tag,
    tracker,
    turn_card,
    type_cmd,
    under,
    what_if_frame,
)
from explainer import style as S
from explainer.devops import (CAPTION, MONO, OUTPUT, box, chip, folder_glyph, glyph_range, mono,
                              mono_line, substring, tag)
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real captures
PS = capture("08", "laptop")
assert PS.cmd == "docker ps"
CLI_NAME = "llm-rag-llm-rag-cli-run-90678535ddef"
assert CLI_NAME in PS.line(3) and "0.0.0.0:8000->8000/tcp" in PS.line(4), PS.lines
PS_ROWS = column_view([PS.line(n) for n in (2, 3, 4)], ("PORTS", "NAMES"))
assert PS_ROWS[1].endswith(CLI_NAME) and PS_ROWS[2].startswith("0.0.0.0:8000->8000/tcp"), PS_ROWS

MOUNTS = capture("15", "laptop")
INSPECT_CLI, INSPECT_CHROMA = MOUNTS.cmd.split("; ")
assert INSPECT_CLI.startswith(f"docker inspect {CLI_NAME} --format '")
assert INSPECT_CHROMA.startswith("docker inspect llm-rag-chromadb --format '")
assert MOUNTS.line(2).endswith("-> /app") and MOUNTS.line(3).endswith("-> /secrets")
assert MOUNTS.line(4) == "" and MOUNTS.line(5).endswith("-> /data"), MOUNTS.lines

ENV = capture("01", "cli-container")
assert ENV.line(2) == "GCP_PROJECT=your-project-id"
SECRETS_PATH = "/secrets/" + KEY_FILE
assert ENV.line(3) == "GOOGLE_APPLICATION_CREDENTIALS=" + SECRETS_PATH, ENV.line(3)
assert ENV.line(5).endswith(" .") and ENV.line(6).endswith(" .."), ENV.lines   # /secrets is empty here

BYNAME = capture("04", "cli-container")
assert BYNAME.line(2).startswith("172.19.0.2") and "heartbeat" in BYNAME.line(3)
HEART = capture("10", "laptop")
assert HEART.cmd == "curl http://localhost:8000/api/v2/heartbeat" and "heartbeat" in HEART.line(2)
VOLS = capture("13", "laptop")
assert VOLS.cmd == "ls -la docker-volumes/chromadb" and VOLS.line(5).endswith("chroma.sqlite3")
assert all("root root" in VOLS.line(n) for n in (3, 4, 5)), VOLS.lines

G5 = capture("01", "gotchas")
assert G5.cmd == "docker compose run --rm llm-rag-cli" and G5.exit == 1
# lines 2–3: one WARN line the 80-column terminal wrapped at a space (the space itself was lost)
assert len(G5.line(2)) == 79 and G5.line(2).endswith("Defaulting") and G5.line(3) == "to a blank string."
WARN_CREDS = G5.line(2) + " " + G5.line(3)
assert G5.typed(16) == "python cli.py --chunk --chunk_type char-split" and G5.line(16).startswith(P_G5)
assert G5.line(18).strip().startswith('File "/app/cli.py", line 35') and "genai.Client(" in G5.line(19)
NOT_FOUND = G5.line(55)
assert NOT_FOUND.endswith("File  was not found."), NOT_FOUND
CLI35 = excerpt("cli.py", 35, 35)
assert "llm_client = genai.Client(" in CLI35, CLI35

CLONE = capture("03", "gotchas")
assert CLONE.line(3) == "llm-rag-main" and CLONE.line(4) == "secrets"
SHELL = capture("04", "gotchas")
assert SHELL.cmd == "sh docker-shell.sh" and SHELL.exit == 127
assert SHELL.line(7) == "/bin/bash: docker-entrypoint.sh: No such file or directory", SHELL.line(7)
STRAY = capture("05", "gotchas")
assert STRAY.cmd == "ls -la ..; ls -la ../llm-rag" and STRAY.line(5).endswith(" llm-rag")
assert "root    root" in STRAY.line(5) and STRAY.line(8) == "total 8", STRAY.lines

VERSION_API = capture("11", "laptop").line(2)
VERSION_SERVER = capture("11b", "laptop").line(2)
assert VERSION_API == '"1.0.0"' and VERSION_SERVER == "chroma 1.4.4", (VERSION_API, VERSION_SERVER)
HUB_TAG = "1.5.9"        # Docker Hub listed the same digest under latest and 1.5.9 (ASSETS.md)

COMPOSE = "docker-compose.yml"
assert excerpt(COMPOSE, 9, 9).strip() == "container_name: llm-rag-cli"
assert excerpt(COMPOSE, 19, 19).strip() == "image: chromadb/chroma:latest"
assert excerpt(COMPOSE, 12, 12).strip() == "- ../llm-rag:/app"

# ------------------------------------------------------------------ commands folded by hand
# type_cmd's fold of these three breaks where a viewer who retypes the rows gets another command:
# inside the 63-character token GOOGLE_…=$GOOGLE_…; (a hard break) and inside the 68-character
# '{{…}}' literal of docker inspect (a " \" there is literal). Folded here instead: " \" only
# outside quotes (the env check's long token starts its row at column 0, as S07 does for a
# literal), and the literal wraps at a space onto a GREY ↪ row, the code panels' wrap mark (as
# L04 S08 does for its --format string). type_rows asserts that the rows join back into the capture.
ENV_ROWS = [P_CTR + " echo GCP_PROJECT=$GCP_PROJECT; echo \\",
            "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS; \\",
            "    ls -la /secrets"]
FMT_A, FMT_B = "'{{range .Mounts}}{{.Source}} ->", "{{.Destination}}{{println}}{{end}}'"
INSPECT_CLI_ROWS = [P_REPO + " docker inspect \\",
                    f"    {CLI_NAME} --format \\",
                    "    " + FMT_A,
                    "      ↪ " + FMT_B]
INSPECT_CHROMA_ROWS = [P_REPO + " docker inspect llm-rag-chromadb \\",
                       "    --format " + FMT_A,
                       "      ↪ " + FMT_B]

# ------------------------------------------------------------------ layout
T8_TOP = strip_top(8)            # 0.58: top of the 8-row terminals
T9_TOP = strip_top(9)            # 0.98: top of trap 2's 9-row terminal
THUMB_TOP, THUMB_BOTTOM = 2.27, 0.68    # inside the what-if frame (its title reaches down to 2.37)
OVER_X = -2.35                   # the overlay area: x from here to 6.4, right of the thumbnail
TERM_ROWS = 8


# ------------------------------------------------------------------ small helpers
def at_left(m, x: float, y: float):
    """Put m's left edge at x and its centre at height y."""
    return m.shift(np.array([x - m.get_left()[0], y - m.get_center()[1], 0]))


def attach(scene, row, *mobs):
    """Make mobs (on screen) part of terminal row `row`: they scroll and fade with it."""
    for m in mobs:
        if m in scene.mobjects:
            scene.remove(m)
        row.add(m)
    scene.add(row)


def text_sub(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line Text (mono()/label(); Text keeps no glyph for a space)."""
    i = t.text.find(sub)
    if i < 0:
        raise ValueError(f"{sub!r} not in {t.text!r}")
    a, n = len("".join(t.text[:i].split())), len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def word_fold(s: str, n: int) -> list[str]:
    """An output line folded at spaces into rows of at most n characters (the capture's own text,
    every character kept; a double space stays inside its row)."""
    rows, cur = [], None
    for w in s.split(" "):
        if cur is not None and len(cur) + 1 + len(w) > n:
            rows.append(cur)
            cur = w
        else:
            cur = w if cur is None else f"{cur} {w}"
    rows.append(cur)
    assert " ".join(rows) == s and all(len(r) <= n for r in rows), rows
    return rows


def thumbnail() -> ComposeView:
    """V2 as S04 left it, glyph-only (no text: scaled freely), top left inside the safe frame and
    inside the what-if frame: the laptop zone with its folders and key, both containers, the rail,
    the three mounts, the published port, the filled $ slots. Docker Hub, Vertex AI and the phone
    book stay out (the phone book appears in beat 3)."""
    cv = ComposeView()
    for n in ("book", "cloud", "vertex", "key_ride", "hub", "hub_slot", "image", "name"):
        cv.remove(cv.parts[n])
    for s in cv.slot_list:                     # docker-shell.sh's values are in the slots
        s.fill_sq.set_fill(LOOKUP, 0.55)
    th = cv.glyph_only()
    th.scale((THUMB_TOP - THUMB_BOTTOM) / th.height)
    th.shift(np.array([-6.35 - th.get_left()[0], THUMB_TOP - th.get_top()[1], 0]))
    for m in th.get_family():                  # thinner strokes at this size
        if isinstance(m, VMobject) and m.get_stroke_width() > 2.5:
            m.set_stroke(width=m.get_stroke_width() * 0.7)
    return th


def phone_book() -> VGroup:
    """V2's phone book card, `llm-rag-chromadb → 172.19.0.2` (PINK), opaque."""
    bt = mono("llm-rag-chromadb → 172.19.0.2", CAPTION, LOOKUP)
    bf = box(bt.width + 0.4, bt.height + 0.26, LOOKUP, fill=S.BG, fill_opacity=0.95, radius=0.1)
    g = VGroup(bf, bt.move_to(bf))
    g.frame, g.text = bf, bt
    return g


def window(name: str, w: float, h: float) -> VGroup:
    """A TEAL container window (as V2's /app, /secrets) at full size, its name at the top."""
    fr = box(w, h, CTR, fill=S.BG, fill_opacity=0.95, radius=0.1, stroke=3)
    t = mono(name, CAPTION, INK).move_to(fr.get_top() + DOWN * 0.27)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def code_rows(w: float, n: int = 3) -> VGroup:
    """A few GREEN code lines (the image's own /app: the code baked in at build)."""
    rows = VGroup()
    for k, f in enumerate((0.85, 0.6, 0.75, 0.5)[:n]):
        rows.add(Line(LEFT * w / 2, LEFT * w / 2 + RIGHT * w * f, color=DATA, stroke_width=4)
                 .shift(DOWN * k * 0.16))
    return rows


def dashed_folder(h: float = 0.42, color: str = LAPTOP) -> VGroup:
    """A dashed GREY folder glyph (a folder Docker made: empty, owned by root)."""
    f = folder_glyph(h, color)
    return VGroup(*[DashedVMobject(m, num_dashes=14, dashed_ratio=0.55).set_stroke(color, 2.5) for m in f])


def type_rows(scene, t, rows: list[str], cmd: str, type_time: float):
    """Type `cmd` at t's prompt, folded by hand into `rows` (row 0 starts with the prompt). A row
    ending in " \\" continues outside quotes; a row whose text starts with "↪ " continues a '...'
    literal at a space (the ↪ drawn GREY, not typed). Returns a VGroup with .rows, as type_cmd."""
    _drop_bare(scene, t)
    p = t.prompt + " "
    assert rows[0].startswith(p) and all(len(r) <= t.max_chars for r in rows), rows
    segs = [rows[0][len(p):]] + [r.strip().removeprefix("↪ ") for r in rows[1:]]
    assert " ".join(s.removesuffix(" \\") for s in segs) == cmd, segs
    for k in range(1, len(rows)):
        assert rows[k].strip().startswith("↪ ") != rows[k - 1].endswith(" \\"), rows
    t._make_room(scene, len(rows))
    out = []
    for k, s in enumerate(rows):
        t2c = t._prompt_colors(t.prompt) if k == 0 else ({"↪": S.GREY} if "↪" in s else None)
        ln = mono_line(s, t.size, INK, t2c=t2c)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        out.append(ln)
    scene.add(glyph_range(out[0], 0, len(p)))
    typed = VGroup(*glyph_range(out[0], len(p)), *[g for r in out[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in out:
        scene.add(r)
    g = VGroup(*out)
    g.rows, g.text = out, " ".join(r.text.strip() for r in out)
    return g


def print_rows(scene, t, rows: list, run_time: float = 0.6, lag: float = 0.12) -> VGroup:
    """Print capture lines with one scroll: a Compose "✔" row as print_build shows it (its time a
    GREY tag at the row's end), any other row as Terminal.print does. (text, colour) accepted."""
    items = [(r, OUTPUT) if isinstance(r, str) else r for r in rows]
    t._make_room(scene, len(items))
    new = VGroup()
    for s, col in items:
        txt, tm = build_row(s, t.max_chars - 7)
        ln = mono_line(txt if tm else t._cut(s), t.size, col)
        t._place(ln, len(t.lines))
        ln.time_tag = None
        if tm:
            ln.time_tag = place_time(time_tag(tm), t, ln)
            ln.add(ln.time_tag)
        t.lines.add(ln)
        new.add(ln)
    scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag), run_time=run_time)
    return new


def card_text(lines, size: float = CAPTION, color: str = INK):
    return VGroup(*[note(s, color, size) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)


# ------------------------------------------------------------------ the scene
class NamesAndMounts(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S05 has {len(SAY)} SAY lines; this scene times 8"

        # ========================================================== 0 · docker ps: names and the port
        tr = tracker("Run", 3)
        th = thumbnail()
        hdr_tag = grey_tag("docker ps · PORTS and NAMES")
        chip9 = excerpt_chip("container_name: llm-rag-cli", f"{COMPOSE} · line 9",
                             line=excerpt(COMPOSE, 9, 9))
        at_left(chip9, OVER_X + 0.1, 2.35)
        err9 = erratum_tag("not used by compose run")
        at_left(err9, OVER_X + 0.1, 1.35)
        x9 = text_sub(chip9.text, "llm-rag-cli")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(th, shift=DOWN * 0.15), run_time=0.8)
            self.play(caption_extra(tr, True), Indicate(th, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("open a second laptop terminal")
            t2 = second_terminal(self, P_REPO, rows=TERM_ROWS, top=T8_TOP)
            vo.wait_until("The docker ps command shows")
            ps = type_cmd(self, t2, PS.cmd, 0.5)
            pin(self, ps, beside(extra_tag(), t2, ps))
            rows = t2.print(self, PS_ROWS, run_time=0.5)
            ps_head, ps_cli, ps_chroma = rows
            pin(self, ps_head, beside(hdr_tag, t2, ps_head, buff=0.6))
            port = substring(ps_chroma, "0.0.0.0:8000->8000/tcp")
            vo.wait_until("Chroma with port 8000")
            self.play(substring(ps_chroma, "llm-rag-chromadb").animate.set_color(TURN),
                      Indicate(th.parts["chroma"], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("port 8000 published")
            self.play(port.animate.set_color(LOOKUP), th.pulse("port"), Indicate(th.door_glyph, color=LOOKUP),
                      run_time=1.0)
            vo.wait_until("But the CLI container")
            cli_name = substring(ps_cli, CLI_NAME)
            self.play(cli_name.animate.set_color(TURN), Indicate(th.parts["cli"], color=TURN, scale_factor=1.06),
                      run_time=0.8)
            self.play(FadeIn(chip9, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("compose run ignores")
            strike9 = Line(x9.get_left() + LEFT * 0.05, x9.get_right() + RIGHT * 0.05, color=ERR, stroke_width=4)
            self.play(FadeIn(err9, shift=UP * 0.1), Create(strike9), run_time=0.6)
            self.play(Indicate(cli_name, color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 1 · docker inspect: the three mounts
        yours = tag("yours differs · copy it from docker ps", S.GREY, size=CAPTION)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(chip9, err9, strike9)), run_time=0.4)
            c1 = type_rows(self, t2, INSPECT_CLI_ROWS, INSPECT_CLI, 1.5)
            name_row = next(r for r in c1.rows if CLI_NAME in r.text)
            u1 = under(substring(name_row, CLI_NAME), TURN)
            at_left(yours, ps_cli.strut.get_left()[0] + 0.02, ps_cli.strut.get_center()[1])
            self.play(Create(u1), FadeIn(yours, shift=RIGHT * 0.1), Indicate(cli_name, color=TURN, scale_factor=1.05),
                      run_time=0.8)
            attach(self, name_row, u1)
            attach(self, ps_cli, yours)
            pin(self, c1, beside(extra_tag(), t2, c1))
            vo.wait_until("The repo is on slash app")
            o2 = t2.print(self, [MOUNTS.line(2)], run_time=0.3)[0]
            self.play(th.pulse("app"), substring(o2, "/app").animate.set_color(LOOKUP), run_time=0.9)
            vo.wait_until("secrets on slash secrets")
            o3 = t2.print(self, [MOUNTS.line(3)], run_time=0.3)[0]
            self.play(th.pulse("secrets"), substring(o3, "/secrets", 1).animate.set_color(LOOKUP), run_time=0.9)
            c2 = type_rows(self, t2, INSPECT_CHROMA_ROWS, INSPECT_CHROMA, 1.2)
            pin(self, c2, beside(extra_tag(), t2, c2), run_time=0.3)
            o5 = t2.print(self, [MOUNTS.line(5)], run_time=0.3)[0]
            self.play(th.pulse("data"), substring(o5, "/data").animate.set_color(LOOKUP), run_time=0.9)
            vo.wait_until("on Chroma's slash data")
            self.play(th.blink("data"), run_time=0.8)

        # ========================================================== 2 · in the container: the two values
        tc = term(P_CTR, rows=TERM_ROWS, container=True)
        sp = signpost([SECRETS_PATH])
        sec = window("/secrets", 1.9, 1.25)
        at_left(sp, OVER_X + 0.15, 2.05)
        sec.next_to(sp.board, RIGHT, buff=0.4)
        ko = key_outline(0.46).move_to(sec.frame.get_center() + DOWN * 0.2)
        yk = grey_tag("yours: the key file").next_to(sec, DOWN, buff=0.18)
        yk.shift(RIGHT * min(0.0, 6.35 - yk.get_right()[0]))
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t2), run_time=0.3)        # one terminal leaves, then the other comes:
            self.play(FadeIn(tc, shift=UP * 0.2), run_time=0.4)   # never two texts crossfading
            env = type_rows(self, tc, ENV_ROWS, ENV.cmd, 1.2)
            pin(self, env, beside(extra_tag(), tc, env), run_time=0.3)
            out = tc.print(self, ENV.at((2, 6)), run_time=0.5)
            pid, cred = out[0], out[1]
            self.play(substring(pid, "your-project-id").animate.set_color(TURN),
                      *[Indicate(s, color=LOOKUP, scale_factor=1.2) for s in th.slot_list], run_time=0.7)
            path = substring(cred, SECRETS_PATH)
            self.play(path.animate.set_color(LOOKUP), FadeIn(VGroup(sp.board, sp.post, sp.foot), shift=UP * 0.1),
                      run_time=0.4)
            self.play(TransformFromCopy(path, sp.text[0]), run_time=0.7)   # the board first: the text on top
            vo.wait_until("Our secrets folder is empty")
            self.play(FadeIn(sec, shift=LEFT * 0.15), Indicate(VGroup(out[3], out[4]), color=TURN, scale_factor=1.03),
                      run_time=0.7)
            vo.wait_until("yours should list")
            self.play(Create(ko), FadeIn(yk, shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(ko, color=COST, scale_factor=1.15), run_time=0.7)

        # ========================================================== 3 · by name inside, by the door outside
        book = phone_book()
        rail_end = th.rail_line.get_end()
        book.move_to(rail_end + RIGHT * (0.12 + book.width / 2))
        book_link = Line(rail_end, book.frame.get_left(), color=CTR, stroke_width=4)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(sp, sec, ko, yk)), run_time=0.3)
            gc = type_cmd(self, tc, BYNAME.cmd, 1.0)
            pin(self, gc, beside(extra_tag(), tc, gc), run_time=0.3)
            hosts, beat = tc.print(self, BYNAME.at(2, 3), run_time=0.4)
            self.play(hosts.animate.set_color(LOOKUP), Create(book_link), FadeIn(book.frame), run_time=0.4)
            # the phone book's line is the hosts line read the other way round: name -> address
            self.play(TransformFromCopy(substring(hosts, "llm-rag-chromadb"), text_sub(book.text, "llm-rag-chromadb")),
                      TransformFromCopy(substring(hosts, "172.19.0.2"), text_sub(book.text, "172.19.0.2")),
                      FadeIn(text_sub(book.text, "→")),
                      Indicate(th.parts["rail"], color=LOOKUP, scale_factor=1.0), run_time=0.9)
            pin(self, beat, beside(differ_tag(), tc, beat), run_time=0.3)
            vo.wait_until("From your laptop")
            self.play(FadeOut(tc), FadeOut(VGroup(book, book_link)), run_time=0.3)
            self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.4)
            hc = type_cmd(self, t2, HEART.cmd, 0.9)
            pin(self, hc, beside(extra_tag(), t2, hc), run_time=0.3)
            hb = t2.print(self, [HEART.line(2)], run_time=0.3)[0]
            vo.wait_until("localhost port 8000")
            self.play(substring(hc.rows[-1], "localhost:8000").animate.set_color(LOOKUP), th.pulse("port"),
                      run_time=0.9)
            vo.wait_until("the published door")
            self.play(th.pulse("port", run_time=1.2), Indicate(th.door_glyph, color=TURN, scale_factor=1.6),
                      run_time=1.2)
            pin(self, hb, beside(differ_tag(), t2, hb), run_time=0.4)

        # ========================================================== 4 · the data folder: made by Docker, root's
        vol_row = file_row("docker-volumes/chromadb/", INK, LAPTOP)
        at_left(vol_row, OVER_X + 0.15, 1.68)
        lock = padlock(0.32, LAPTOP).next_to(vol_row, RIGHT, buff=0.25)
        made = grey_tag("made by Docker: the mount's source")
        at_left(made, OVER_X + 0.1, 2.25)
        roots = grey_tag("root's · Linux: sudo to delete")
        roots.next_to(lock, DOWN, buff=0.14).align_to(lock, RIGHT)
        with self.voiceover(SAY[4]) as vo:
            type_cmd(self, t2, VOLS.cmd, 0.9)
            lv = t2.print(self, VOLS.at((2, 5)), run_time=0.5)
            ex4 = extra_tag()            # the typed row is full: the tag sits at the end of the row under it
            ex4.move_to(lv[0].strut).align_to(t2.box, RIGHT).shift(LEFT * 0.12)
            pin(self, lv[0], ex4, run_time=0.3)
            self.play(TransformFromCopy(th.rows["chromadb"], vol_row), th.pulse("data"), run_time=0.9)
            self.play(FadeIn(made, shift=UP * 0.1), Indicate(th.rows["chromadb"], color=TURN, scale_factor=1.3),
                      run_time=0.7)
            vo.wait_until("owned by root")
            self.play(*[substring(lv[k], "root root").animate.set_color(TURN) for k in (1, 2, 3)], run_time=0.6)
            self.play(FadeIn(lock, scale=0.6), run_time=0.5)
            vo.wait_until("with the database file")
            self.play(Indicate(substring(lv[3], "chroma.sqlite3"), color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("On Linux")
            self.play(FadeIn(roots, shift=LEFT * 0.1), Indicate(lock, color=TURN, scale_factor=1.2), run_time=0.7)

        # ========================================================== 5 · trap 1: Compose without the script
        wf = what_if_frame(note_="recorded after teardown")
        tw = term(P_REPO, rows=TERM_ROWS, title="laptop")
        wrong = tag("the wrong way", ERR)
        c35 = excerpt_chip("llm_client = genai.Client(", "cli.py · line 35 (excerpt)", line=CLI35)
        at_left(c35, OVER_X + 0.3, 1.78)
        startup = note("runs at startup").next_to(c35.chip, DOWN, buff=0.14).align_to(c35.chip, LEFT)
        always = fix_chip("always start with: sh docker-shell.sh")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t2), FadeOut(VGroup(vol_row, lock, made, roots)), run_time=0.5)
            self.play(Create(wf.frame), FadeIn(wf.title), FadeIn(wf.note), run_time=0.8)
            self.play(*[s.fill_sq.animate.set_fill(LOOKUP, 0.0) for s in th.slot_list], run_time=0.8)
            vo.wait_until("Trap one")
            self.play(FadeIn(tw, shift=UP * 0.2), run_time=0.5)
            cr = type_cmd(self, tw, G5.cmd, 1.0)
            ex = beside(extra_tag(), tw, cr)
            pin(self, cr, ex, run_time=0.3)
            wrong.next_to(ex, RIGHT, buff=0.2)
            pin(self, cr, wrong, run_time=0.4)
            vo.wait_until("Both variables come out blank")
            warn = tw.print(self, word_fold(WARN_CREDS, tw.max_chars) + word_fold(G5.line(4), tw.max_chars) + ["…"],
                            run_time=0.7)
            names = [substring(r, v) for r in warn for v in ('"GOOGLE_APPLICATION_CREDENTIALS"', '"GCP_PROJECT"')
                     if v in r.text]
            blanks = [substring(r, "blank string.") for r in warn if "blank string." in r.text]
            self.play(*[m.animate.set_color(TURN) for m in names], *[m.animate.set_color(ERR) for m in blanks],
                      *th.empty_slots(), run_time=1.2)
            vo.wait_until("and even chunking dies")
            tw.set_prompt(P_G5)
            type_cmd(self, tw, G5.typed(16), 1.0)
            vo.wait_until("where cli.py creates")
            tb = tw.print(self, G5.at(17, 18, 19), run_time=0.5)
            self.play(FadeIn(c35, shift=DOWN * 0.1), Indicate(substring(tb[2], "genai.Client("), color=TURN,
                                                              scale_factor=1.08), run_time=0.7)
            self.play(FadeIn(startup, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("looking for a key file")
            nf = tw.print(self, ["…"] + [(r, ERR) for r in word_fold(NOT_FOUND, tw.max_chars)], run_time=0.5)
            nf_row = next(r for r in nf if "File  was" in r.text)
            i = nf_row.text.index("File  was") + 4
            gap = col_box(nf_row, i, i + 2, TURN)
            empty = tag("an empty file name", TURN, size=CAPTION)
            beside(empty, tw, nf[-1], buff=0.5)
            self.play(Create(gap), run_time=0.4)
            attach(self, nf_row, gap)
            pin(self, nf[-1], empty, run_time=0.4)
            self.play(*th.empty_slots(), run_time=1.2)
            vo.wait_until("Always start through")
            always.next_to(startup, RIGHT, buff=0.6)
            self.play(FadeIn(always, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(always, color=DATA, scale_factor=1.08), run_time=0.7)

        # ========================================================== 6 · trap 2: a clone with another name
        tz = term(P_ZIP, rows=9, title="laptop")
        # the picture: ~/AC215-zip on the laptop, the route ../llm-rag -> /app into the CLI container
        zone = box(5.3, 1.18, LAPTOP, fill_opacity=0.05, radius=0.14).move_to([-3.65, 1.65, 0])
        r_main = file_row("llm-rag-main/", INK, LAPTOP)
        r_sec = file_row("secrets/", INK, LAPTOP)
        zlab = mono("~/AC215-zip/", CAPTION, LAPTOP)
        at_left(r_main, -6.1, 1.97)
        at_left(r_sec, -6.1, 1.6)
        at_left(zlab, -6.1, 1.24)
        y_r = 1.72                                   # the route's height
        ghost_row = VGroup(dashed_folder(0.22, LAPTOP), mono("llm-rag/", CAPTION, S.GREY))
        ghost_row[1].next_to(ghost_row[0], RIGHT, buff=0.12)
        at_left(ghost_row, -3.25, y_r)
        root_t = tag("root · empty", S.GREY, size=CAPTION)
        at_left(root_t, -3.3, 1.3)
        appw = window("/app", 1.7, 1.0).move_to([3.55, 1.56, 0])
        ctl = VGroup(mono("CLI", CAPTION, CTR), mono("container", CAPTION, CTR)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.08)
        ctl.next_to(appw, RIGHT, buff=0.2)
        code = code_rows(1.1).move_to(appw.frame.get_center() + DOWN * 0.18)
        miss = DashedVMobject(RoundedRectangle(width=0.34, height=0.27, corner_radius=0.04),
                              num_dashes=12).set_stroke(LOOKUP, 2.5).move_to(ghost_row[0])
        route = DashedVMobject(Line([ghost_row.get_right()[0] + 0.15, y_r, 0], [appw.frame.get_left()[0] - 0.04, y_r, 0]),
                               num_dashes=36).set_stroke(LOOKUP, 4)
        rlab = mono("../llm-rag → /app", CAPTION, LOOKUP).move_to([(route.get_left()[0] + route.get_right()[0]) / 2,
                                                                  y_r + 0.3, 0])
        fix = VGroup(fix_chip("keep the name llm-rag (or mount .:/app)"),
                     fix_chip("delete the stray folder (sudo on Linux)")).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        unpacks = grey_tag("what a zip download unpacks")
        after_cd = note("after cd llm-rag-main")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(tw, th, c35, startup, always)), run_time=0.4)
            self.play(FadeIn(tz, shift=UP * 0.2), run_time=0.4)
            gl = type_cmd(self, tz, CLONE.cmd, 1.1)
            pin(self, gl, beside(extra_tag(), tz, gl), run_time=0.3)
            co = tz.print(self, CLONE.at((2, 4)), run_time=0.4)
            beside(unpacks, tz, co[1], buff=0.6)
            self.play(FadeIn(unpacks, shift=LEFT * 0.1), Create(zone), FadeIn(zlab),
                      TransformFromCopy(VGroup(*co[1].glyphs), r_main.text), FadeIn(r_main.glyph),
                      TransformFromCopy(VGroup(*co[2].glyphs), r_sec.text), FadeIn(r_sec.glyph), run_time=0.8)
            attach(self, co[1], unpacks)
            bare = cd_prompt(self, tz, P_ZIP_REPO, LAPTOP, run_time=0.5)    # not narrated: no anchor
            beside(after_cd, tz, bare, buff=0.5)
            self.play(FadeIn(after_cd), run_time=0.3)
            vo.wait_until("The compose file mounts")
            ghost_row[1].set_color(LOOKUP)
            self.play(FadeIn(ctl), FadeIn(appw), FadeIn(code), Create(miss), FadeIn(ghost_row[1]), Create(route),
                      FadeIn(rlab), FadeOut(after_cd), run_time=0.8)
            type_cmd(self, tz, SHELL.cmd, 0.5)
            so = print_rows(self, tz, SHELL.at((2, 6)) + [(SHELL.line(7), ERR)], run_time=0.6)
            vo.wait_until("so Docker creates")
            self.play(ReplacementTransform(miss, ghost_row[0]), ghost_row[1].animate.set_color(S.GREY),
                      run_time=0.6)
            st = type_cmd(self, tz, STRAY.cmd, 0.7)
            pin(self, st, beside(extra_tag(), tz, st), run_time=0.3)
            sl = tz.print(self, STRAY.at(2, (5, 6), (8, 10)), run_time=0.4)
            vo.wait_until("owned by root")
            self.play(substring(sl[1], "root    root").animate.set_color(TURN),
                      substring(sl[1], "llm-rag").animate.set_color(TURN),
                      substring(sl[4], "root    root").animate.set_color(TURN),
                      FadeIn(root_t, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("over your code")
            mover = ghost_row[0].copy()
            self.play(mover.animate.scale(2.4).move_to(appw.frame.get_center() + DOWN * 0.2),
                      code.animate.set_opacity(0.0), Indicate(so[-1], color=ERR, scale_factor=1.04), run_time=1.0)
            vo.wait_until("Keep the name")
            at_left(fix, -0.6, 1.65)
            self.play(FadeOut(VGroup(route, rlab, ctl, appw, code, mover)), run_time=0.3)
            self.play(FadeIn(fix[0], shift=UP * 0.1), Indicate(r_main, color=TURN, scale_factor=1.06), run_time=0.5)
            vo.wait_until("and delete the stray folder")
            self.play(FadeIn(fix[1], shift=UP * 0.1), Indicate(ghost_row, color=ERR, scale_factor=1.12),
                      run_time=0.6)

        # ========================================================== 7 · back home: versions, then your turn
        st3 = term(P_CTR, rows=3, container=True)
        back = note("back in your container")
        i19 = excerpt(COMPOSE, 19, 19).strip()
        img = excerpt_chip(i19, f"{COMPOSE} · line 19", line=excerpt(COMPOSE, 19, 19))
        chips = VGroup(*[chip(s, CTR, size=CAPTION, font=MONO) for s in
                         (f"tag {HUB_TAG}", VERSION_SERVER, f"API {VERSION_API}")]).arrange(RIGHT, buff=0.35)
        rec = recording_tag()
        tip = note("team tip: pin a tag in docker-compose.yml · line 19")
        vcard_rows = VGroup(img, chips, VGroup(rec, tip).arrange(RIGHT, buff=0.4)).arrange(DOWN, buff=0.38)
        vcard_rows[1].align_to(vcard_rows[0], LEFT)
        vcard_rows[2].align_to(vcard_rows[0], LEFT)
        vfr = box(vcard_rows.width + 0.7, vcard_rows.height + 0.6, S.GREY, fill_opacity=0.0, radius=0.14)  # no fill:
        # it fades in after the image chip, and nothing lies behind it
        vfr.move_to(vcard_rows)
        vcard = VGroup(vfr, vcard_rows).move_to([0, 0.55, 0])
        latest = text_sub(img.text, "latest")
        u_latest = under(latest, TURN)

        env_rows = "echo GCP_PROJECT=$GCP_PROJECT; \\\necho GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS; \\\nls -la /secrets"
        assert env_rows.replace(" \\\n", " ") == ENV.cmd
        turn = turn_card([(Prose("container"), CTR), env_rows,
                          (Prose(f"yours: {KEY_FILE} listed"), COST),
                          (Prose("second terminal, in llm-rag"), LAPTOP),
                          f"{PS.cmd}\n{HEART.cmd}\n{VOLS.cmd}"], header=None)
        turn.move_to([0, (2.85 + STRIP_TOP) / 2, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(wf, tz, zone, zlab, r_main, r_sec, ghost_row, root_t, fix)), run_time=0.6)
            self.play(FadeIn(st3, shift=UP * 0.2), run_time=0.5)
            bp = bare_prompt(self, st3)
            beside(back, st3, bp, buff=0.5)
            self.play(FadeIn(back, shift=LEFT * 0.1), run_time=0.4)
            self.play(FadeIn(img, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("the image tag called latest")
            self.play(Create(u_latest), latest.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("and three version numbers")
            self.play(FadeIn(vfr), *[FadeIn(c, shift=UP * 0.15) for c in chips], run_time=0.8)
            self.play(*[Indicate(c, color=TURN, scale_factor=1.08) for c in chips], FadeIn(rec), run_time=0.8)
            vo.wait_until("a team should pin a tag")
            self.play(FadeIn(tip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Pause and try these checks")
            self.play(FadeOut(VGroup(vcard, u_latest, chips, rec, tip)), FadeIn(turn, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("your key in slash secrets")
            self.play(Indicate(turn.rows[2], color=COST, scale_factor=1.06), run_time=0.8)
        self.wait(2)                                   # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, st3, back, turn)), run_time=0.8)
        self.wait(0.3)

