"""S05 · Back in the container: the agent needs an index (README "Prerequisites", "Run Container",
"Agents" step 1, and lecture 5's "Load"). Lecture: none (no lecture tag).

Beats (script.md "## S05", one voiceover block each):
0. TRACKER Prereq 1. The tracker, then (at "today we run it") the terminal (full width, 8 rows,
   title laptop, prompt student@laptop:~/AC215$). A GREY caption "fresh start only · README.md ·
   line 48 links the repo". It types `git clone https://github.com/dlops-io/llm-rag.git` ->
   laptop/01 line 2; then `mkdir secrets; ls` (extra tag) -> laptop/02 line 2; a GOLD key chip
   "llm-service-account.json -> secrets/ · beside llm-rag, never inside · lecture 5 · README.md ·
   lines 62–69"; "secrets" and the key flash.
1. TRACKER Run 1: `cd llm-rag`, the prompt becomes ~/AC215/llm-rag$. TRACKER Run 2: the terminal
   shrinks to the 3-row strip; above it PANEL(laptop/05: 10–11, "docker-shell.sh · line 7 · your
   edit"), line 10 RED, line 11 GREEN; `your-project-id` underlined YELLOW with the YELLOW tag "your
   own project ID" under it. ▶ on a static GREY card (fresh start: git clone, mkdir secrets with the
   key inside; then cd llm-rag, set GCP_PROJECT in docker-shell.sh). Hold 2 s.
2. TRACKER Run 3. The terminal grows to 13 rows: `sh docker-shell.sh` -> laptop/06 lines 2–5 (Compose
   rows, times as GREY tags; Chroma's rows flash), 6 and 7–9 joined (wrapped) RED, then GREY with the
   tag "harmless · wording depends on Docker setup"; 10–11 (11 + "at the time of recording"), "…",
   32–34.
3. "40.5s" flashes; lines 35–40; 3.12.15 and 0.13.1 underlined GREY, "at the time of recording" on
   line 38. Line 41's prompt alone (cut before `exit`): the frame turns TEAL, title "container ·
   llm-rag-cli"; abcf218747d0 underlined, GREY tag "container ID · your numbers will differ";
   ▶ your turn beside it. Hold 2 s.
4. TRACKER Run 3 · extra. The container terminal shrinks to the 3-row strip; a second terminal slides
   in above it (title "laptop · second terminal", prompt ~/AC215/llm-rag$): `docker ps --format
   'table {{.Names}}\\t{{.Image}}\\t{{.Ports}}'` (extra; folds onto two rows) -> laptop/07 lines 2–4,
   shown as the NAMES and PORTS columns (GREY tag "IMAGE not shown": the full rows are 86
   characters, the house terminal holds 65); 0.0.0.0:8000->8000/tcp turns PINK in a PINK box, PINK
   tag "port 8000 · remember for part 2" under it. The second terminal slides away.
5. TRACKER Agents 1. The TEAL terminal grows back (13 rows): `python cli.py --agent --chunk_type
   char-split` -> cli-container/10 lines 2–3, 9–10, "…", 25 (wrap), GREY tag "real run · fresh
   clone"; line 25 RED. The terminal shrinks to a strip (lines 9 and 25); above it CODE(cli.py:
   427–429), line 429 RED.
6. The code panel leaves; "char-split-collection" flashes in the strip. Two GREY cards above the
   strip, one per path (stacked: the README commands need the full width): "kept lecture 5's
   database?" docker-volumes/chromadb · skip ahead, GREY note "chunked before September 22, 2026?
   git pull, then chunk → embed → load / the book changed (explained soon)"; "no database?" (GREY
   README.md · lines 103, 129 + expected) with the chunk and embed commands (embed: "needs your
   key") and "then the load step".
7. The first card leaves, the second rises; a GOLD key lands on the embed row; PANEL(laptop/08: 2–3,
   header "outputs/embeddings-char-split-*" over "copied from commit 68e0bde") slides in under it
   with a GREY arrow up to the key, tag "recorded · the staff's vectors".
8. TRACKER Load 1. The terminal grows (12 rows, leaving a band under the tracker for the README chip
   "README.md · line 152: recursive-split too · the agent uses char-split" + expected):
   `python cli.py --load --chunk_type char-split` -> cli-container/20 lines 2–8, then "…", 142,
   152–153 (wrap; two prints), the prompt returns. GREY tag "8,248 chunks in 11 books · 24 from the
   instructor's story" on the "…" row; 11, 24 and Tolminc flash. TRACKER Load 1 · extra: `python
   cli.py --get --chunk_type char-split` (extra) -> cli-container/21 line 6 cut after
   '1021665fac86c5a5-0', + "…". The chip leaves, the terminal shrinks to the strip; ▶ on a static
   GREY card (load, or keep yours; get). Hold 2 s. Fade to an empty frame.
"""

from common import (
    COST,
    DATA,
    ERR,
    INK,
    KEY_FILE,
    LOOKUP,
    NARRATION,
    P_CTR,
    P_REPO,
    P_WS,
    STRIP_TOP,
    TURN,
    bare_prompt,
    beside,
    capture,
    caption_extra,
    cd_prompt,
    col_box,
    enter_container,
    expected_tag,
    extra_tag,
    grey_tag,
    key_glyph,
    log_panel,
    note,
    pin,
    print_build,
    recording_tag,
    resize,
    second_terminal,
    split_prompt,
    src_panel,
    switch_section,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    VGroup,
    there_and_back,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    box,
    label,
    mono,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real captures and sources
CLONE = capture("01", "laptop")
assert CLONE.cmd == "git clone https://github.com/dlops-io/llm-rag.git", CLONE.cmd
MKDIR = capture("02", "laptop")
assert MKDIR.cmd == "mkdir secrets; ls" and MKDIR.line(2) == "llm-rag  secrets", MKDIR.lines
CD = capture("03", "laptop")
assert CD.cmd == "cd llm-rag", CD.cmd
DIFF = capture("05", "laptop")
assert DIFF.line(10).startswith('-export GCP_PROJECT="ac215-project"'), DIFF.line(10)
assert DIFF.line(11).startswith('+export GCP_PROJECT="your-project-id"'), DIFF.line(11)

RUN = capture("06", "laptop")
assert RUN.cmd == "sh docker-shell.sh", RUN.cmd
assert "chromadb/chroma:latest Pulled" in RUN.line(3) and "llm-rag-chromadb" in RUN.line(5)
assert RUN.line(6) == "Image llm-rag-cli Pulling", RUN.line(6)
PULL_MSG = RUN.join(7, 8, 9)
assert "repository does not exist or may require" in PULL_MSG, PULL_MSG
assert "Building 40.5s" in RUN.line(11) and RUN.line(32) == "Image llm-rag-cli Built"
assert "3.12.15" in RUN.line(38) and "0.13.1" in RUN.line(39), (RUN.line(38), RUN.line(39))
assert split_prompt(RUN.line(41)) == (P_CTR, "exit"), RUN.line(41)
CID = "abcf218747d0"
assert CID in P_CTR

PS = capture("07", "laptop")
assert PS.cmd == "docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Ports}}'", PS.cmd
PORT = "0.0.0.0:8000->8000/tcp"
assert PORT in PS.line(4) and PS.line(4).startswith("llm-rag-chromadb"), PS.line(4)

AGENT = capture("10", "cli-container")
assert AGENT.cmd == "python cli.py --agent --chunk_type char-split", AGENT.cmd
assert AGENT.line(9) == '  File "/app/cli.py", line 429, in agent', AGENT.line(9)
assert AGENT.line(25).endswith("Collection [char-split-collection] does not exist"), AGENT.line(25)

COPY = capture("08", "laptop")
assert COPY.line(2) == "11" and COPY.line(3).startswith("31M") and COPY.line(3).endswith("total")

LOAD = capture("20", "cli-container")
assert LOAD.cmd == "python cli.py --load --chunk_type char-split", LOAD.cmd
assert LOAD.line(8) == "Number of files to process: 11", LOAD.line(8)
assert LOAD.line(142).endswith("Tolminc Cheese.jsonl") and LOAD.line(143) == "Shape: (24, 3)"
assert LOAD.line(153).startswith("Finished inserting 24 items"), LOAD.line(153)
AUTHORS = capture("34", "cli-container")
assert AUTHORS.line(15) == "chunks in char-split-collection: 8248", AUTHORS.line(15)

GET = capture("21", "cli-container")
assert GET.cmd == "python cli.py --get --chunk_type char-split", GET.cmd
GET_ROW = GET.cut(6, "'1021665fac86c5a5-0',") + " …"

README_CHUNK = "python cli.py --chunk --chunk_type char-split"     # README.md:103
README_EMBED = "python cli.py --embed --chunk_type char-split"     # README.md:129
README_152 = "python cli.py --load --chunk_type recursive-split"  # README.md:152 (the chip's excerpt)

# ------------------------------------------------------------------ layout
TOP_Y = 2.78                  # nothing above this but the tracker band
LOAD_ROWS = 12                # the load step's terminal: 12 rows leave a band for the README chip
GAP_Y = STRIP_TOP + 0.14      # the lowest y a picture above the 3-row strip may use


# ------------------------------------------------------------------ small helpers
def attach(scene, row, *mobs):
    """Make mobs (already on screen) part of terminal row `row`: they scroll and fade with it."""
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def detach(scene, row, *mobs):
    """Take mobs out of terminal row `row` (they stay on screen as themselves)."""
    for m in mobs:
        if m in row.submobjects:
            row.remove(m)
        scene.add(m)


def rows_with(rows, sub: str):
    """The printed rows (mono_lines) whose text contains `sub`."""
    hits = [r for r in rows if sub in getattr(r, "text", "")]
    assert hits, (sub, [getattr(r, "text", "") for r in rows])
    return hits


def ps_columns(cap, keep=("NAMES", "PORTS")) -> list[str]:
    """`docker ps --format 'table …'` rows (file lines 2–4) cut down to the named columns, each kept
    column at its own width and offset. The full rows are 86 characters, the house terminal 65."""
    head = cap.line(2)
    names = head.split()
    starts = [head.index(n) for n in names]
    spans = dict(zip(names, zip(starts, starts[1:] + [None])))
    out = []
    for n in (2, 3, 4):
        s = cap.line(n)
        parts = []
        for name in keep:
            a, b = spans[name]
            parts.append(s[a:b] if b is not None else s[a:])
        row = "".join(parts).rstrip()
        out.append(row)
    assert all(len(r) <= 65 for r in out), out
    return out


def key_chip() -> VGroup:
    """The GOLD key chip: the service-account key goes into secrets/, beside llm-rag."""
    k = key_glyph(0.3)
    top = VGroup(k, mono(KEY_FILE, CAPTION, INK), label("→", CAPTION, INK),
                 mono("secrets/", CAPTION, INK)).arrange(RIGHT, buff=0.16)
    sub = note("beside llm-rag, never inside · lecture 5 · README.md · lines 62–69")
    rows = VGroup(top, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(rows.width + 0.5, rows.height + 0.36, COST, fill=S.BG, fill_opacity=0.92, radius=0.14)
    fr.move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.rows, g.key = fr, rows, k
    return g


def path_card(title, rows, width: float = 12.6, right=None) -> VGroup:
    """A GREY card for one path of the fork: a title row (with optional `right` GREY header bits at
    its right end), then `rows` (mobjects) left-aligned. .frame .title .rows"""
    t = label(title, CAPTION + 2, INK)
    body = VGroup(t, *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    fr = box(width, body.height + 0.42, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, body)
    if right is not None:
        right.move_to(t).align_to(fr, RIGHT).shift(LEFT * 0.25)
        g.add(right)
    g.frame, g.title, g.rows, g.right = fr, t, list(rows), right
    return g


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def flash(text, border, color: str = TURN, k: float = 1.06) -> list:
    """Indicate for a filled chip or tag: its text and border take `color`, the fill stays."""
    w = border.get_stroke_width()
    return [Indicate(text, color=color, scale_factor=k),
            border.animate(rate_func=there_and_back).set_stroke(color, w + 1.5)]


def staff_panel() -> VGroup:
    """PANEL(laptop/08: 2–3): the staff's committed embeddings (11 files, 31M total). The header
    "outputs/embeddings-char-split-* · copied from commit 68e0bde" sits on two lines above the
    frame, so the panel stays narrow. .frame .rows .header .sub"""
    p = log_panel([COPY.line(2), COPY.line(3)], "outputs/embeddings-char-split-*", width=3.2)
    sub = note("copied from commit 68e0bde")
    sub.next_to(p.frame, UP, buff=0.1).align_to(p.header, LEFT)
    p.header.next_to(sub, UP, buff=0.08).align_to(sub, LEFT)
    p.add(sub)
    p.sub = sub
    return p


class BackInTheContainer(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · fresh start: clone, secrets/
        tr = tracker("Prereq", 1)
        t = term(P_WS, rows=8, title="laptop")
        cap0 = note("fresh start only · README.md · line 48 links the repo")
        place(cap0, left=-6.25, bottom=t.box.get_top()[1] + 0.18)
        kc = key_chip()
        place(kc, left=-6.3, bottom=cap0.get_top()[1] + 0.3)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), run_time=0.6)
            vo.wait_until("today we run it")
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
            bare_prompt(self, t)
            vo.wait_until("Starting fresh?")
            self.play(FadeIn(cap0, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Clone L-L-M rag")
            type_cmd(self, t, CLONE.cmd, 1.2)
            t.print(self, [CLONE.line(2)], run_time=0.4)
            vo.wait_until("and put the service account key")
            mk = type_cmd(self, t, MKDIR.cmd, 0.6)
            ex0 = beside(extra_tag(), t, mk)
            pin(self, mk, ex0, run_time=0.3)
            ls_out = t.print(self, [MKDIR.line(2)], run_time=0.4)[0]
            vo.wait_until("in a secrets folder")
            self.play(FadeIn(kc, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(substring(ls_out, "secrets"), color=TURN, scale_factor=1.15),
                      Indicate(kc.key, color=TURN, scale_factor=1.2), run_time=0.8)
            vo.wait_until("otherwise, go to your folder")
            self.play(Indicate(cap0, color=TURN, scale_factor=1.05), run_time=0.8)

        # ========================================================== 1 · cd, set GCP_PROJECT, ▶
        diff = log_panel([(DIFF.line(10), ERR), (DIFF.line(11), DATA), ""],
                         "docker-shell.sh · line 7 · your edit")
        place(diff, cx=0, top=TOP_Y)
        r11 = diff.rows[1]
        pid = substring(r11, "your-project-id")
        u_pid = under(pid, TURN, stroke=4)
        own = tag("your own project ID", TURN)
        own.move_to(diff.rows[2].strut).set_x(pid.get_center()[0])
        card1 = turn_card([(CLONE.cmd, "fresh start"),
                           ("mkdir secrets", "fresh start · your key inside"),
                           ("cd llm-rag", "then: set GCP_PROJECT in docker-shell.sh")], header=None)
        place(card1, cx=0, bottom=GAP_Y)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(cap0, kc)), run_time=0.4)
            tr = switch_section(self, tr, "Run", 1, run_time=0.6)
            vo.wait_until("cd L-L-M rag")
            type_cmd(self, t, CD.cmd, 0.5)
            cd_prompt(self, t, P_REPO)
            vo.wait_until("Step 2:")
            self.play(tr.goto(2))
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(diff, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("and set GCP project")
            self.play(Indicate(diff.rows[0], color=ERR, scale_factor=1.02), run_time=0.6)
            self.play(Indicate(r11, color=DATA, scale_factor=1.02), run_time=0.6)
            self.play(Create(u_pid), pid.animate.set_color(TURN), FadeIn(own, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("we used a placeholder")
            self.play(*flash(own.text, own.box), run_time=0.8)
            vo.wait_until("Pause, and do both")
            self.play(FadeIn(card1, shift=UP * 0.15), run_time=0.6)
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 2 · sh docker-shell.sh
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(card1, diff, u_pid, own)), tr.goto(3), run_time=0.5)
            resize(self, t, 13, run_time=0.7)
            vo.wait_until("sh docker-shell.sh")
            type_cmd(self, t, RUN.cmd, 0.8)
            vo.wait_until("Compose starts Chroma first")
            t.print(self, [RUN.line(2)], run_time=0.3)
            comp = print_build(self, t, [RUN.line(3), RUN.line(4), RUN.line(5)], run_time=0.6)
            l3, l5 = comp[0], comp[2]
            self.play(Indicate(substring(l3, "chromadb/chroma:latest"), color=TURN, scale_factor=1.08),
                      Indicate(substring(l5, "llm-rag-chromadb"), color=TURN, scale_factor=1.08),
                      run_time=0.9)
            vo.wait_until("The pull message")
            l6 = t.print(self, [(RUN.line(6), ERR)], run_time=0.3)[0]
            err = t.print(self, [(PULL_MSG, ERR)], wrap=True, run_time=0.5)
            vo.wait_until("but is harmless")
            # 5.8 wide: it ends left of the "2.0s" time tag on the row above (the full SHOW wording,
            # "its wording depends on your Docker setup", is 6.8 wide and touches it)
            hm = tag("harmless · wording depends on Docker setup", S.GREY, size=CAPTION)
            beside(hm, t, l6, buff=0.3)
            self.play(*[r.animate.set_color(S.GREY) for r in (l6, *err)], run_time=0.6)
            pin(self, l6, hm, run_time=0.4)
            vo.wait_until("there's no such image online")
            dne = rows_with(err, "does not exist")[0]
            self.play(Indicate(substring(dne, "does not exist"), color=TURN, scale_factor=1.1),
                      Indicate(substring(l6, "llm-rag-cli"), color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("so Compose builds it")
            b = t.print(self, [RUN.line(10), RUN.line(11)], run_time=0.4)
            l11 = b[1]
            rec11 = beside(recording_tag(), t, l11, buff=0.4)
            pin(self, l11, rec11, run_time=0.4)
            t.print(self, ["…", RUN.line(32), RUN.line(33), RUN.line(34)], run_time=0.5)

        # ========================================================== 3 · the banner, the container's prompt, ▶
        with self.voiceover(SAY[3]) as vo:
            s40 = substring(l11, "40.5s")
            u40 = under(s40, S.GREY, stroke=3)
            self.play(Create(u40), Indicate(s40, color=TURN, scale_factor=1.15), run_time=0.7)
            attach(self, l11, u40)
            vo.wait_until("the banner")
            ban = t.print(self, RUN.at((35, 40)), run_time=0.7)
            l38, l39 = ban[3], ban[4]
            t.set_prompt(P_CTR)
            pr = bare_prompt(self, t)
            self.play(*enter_container(t), run_time=0.6)
            vo.wait_until("Python 3.12.15")
            v38, v39 = substring(l38, "3.12.15"), substring(l39, "0.13.1")
            u38, u39 = under(v38, S.GREY, stroke=3), under(v39, S.GREY, stroke=3)
            self.play(Create(u38), Indicate(v38, color=TURN, scale_factor=1.1), run_time=0.6)
            self.play(Create(u39), Indicate(v39, color=TURN, scale_factor=1.1), run_time=0.6)
            attach(self, l38, u38)
            attach(self, l39, u39)
            vo.wait_until("at the time of recording")
            rec38 = beside(recording_tag(), t, l38, buff=0.5)
            pin(self, l38, rec38, run_time=0.4)
            vo.wait_until("After the at sign")
            cid = substring(pr, CID)
            uid = under(cid, S.GREY, stroke=3)
            self.play(Create(uid), Indicate(cid, color=TURN, scale_factor=1.12), run_time=0.7)
            attach(self, pr, uid)
            vo.wait_until("new every run")
            idt = beside(grey_tag("container ID · your numbers will differ"), t, pr, buff=0.25)
            pin(self, pr, idt, run_time=0.4)
            vo.wait_until("pause, and get to this prompt")
            yt3 = your_turn().next_to(idt, RIGHT, buff=0.18)     # ends inside the frame
            pin(self, pr, yt3, run_time=0.5, anim=FadeIn(yt3, scale=1.2))
        self.wait(2)                                    # ▶ beat: hold the frame

        # ========================================================== 4 · docker ps from a second terminal
        ps_rows = ps_columns(PS)
        with self.voiceover(SAY[4]) as vo:
            detach(self, pr, idt, yt3, uid)
            self.play(FadeOut(VGroup(idt, yt3, uid)), caption_extra(tr, True), run_time=0.5)
            resize(self, t, 3, run_time=0.6)            # a second panel goes above the strip
            t2 = second_terminal(self, P_REPO, rows=6)
            vo.wait_until("docker ps")
            cmd2 = type_cmd(self, t2, PS.cmd, 1.4)
            row2 = cmd2.rows[0] if hasattr(cmd2, "rows") else cmd2     # the prompt row has room
            ex2 = beside(extra_tag(), t2, row2, buff=0.4)
            pin(self, row2, ex2, run_time=0.3)
            out2 = t2.print(self, ps_rows, run_time=0.6)
            hd, row_ch = out2[0], out2[2]
            img = beside(grey_tag("IMAGE not shown"), t2, hd, buff=0.4)
            pin(self, hd, img, run_time=0.3)
            p2 = bare_prompt(self, t2)
            vo.wait_until("Chroma publishes port 8000")
            port = substring(row_ch, PORT)
            a = row_ch.text.index(PORT)
            pbox = col_box(row_ch, a, a + len(PORT), LOOKUP)
            self.play(Indicate(substring(row_ch, "llm-rag-chromadb"), color=TURN, scale_factor=1.08),
                      run_time=0.6)
            self.play(port.animate.set_color(LOOKUP), Create(pbox), run_time=0.6)
            attach(self, row_ch, pbox)
            vo.wait_until("remember that port")
            ptag = tag("port 8000 · remember for part 2", LOOKUP)
            ptag.move_to(p2.strut).align_to(pbox, RIGHT)
            pin(self, p2, ptag, run_time=0.5)
            self.play(*flash(ptag.text, ptag.box, LOOKUP), run_time=0.8)
            self.wait(0.4)
            self.play(FadeOut(t2, shift=DOWN * 0.3), caption_extra(tr, False), run_time=0.6)

        # ========================================================== 5 · --agent on a fresh clone fails
        with self.voiceover(SAY[5]) as vo:
            tr = switch_section(self, tr, "Agents", 1, run_time=0.6)
            resize(self, t, 13, run_time=0.6)
            vo.wait_until("python cli.py, dash dash agent")
            cmd5 = type_cmd(self, t, AGENT.cmd, 1.2)
            vo.wait_until("On a fresh clone")
            out5 = t.print(self, [AGENT.line(2), AGENT.line(3), AGENT.line(9), AGENT.line(10), "…",
                                  (AGENT.line(25), ERR)], wrap=True, run_time=0.8)
            rr = cmd5.rows[0] if hasattr(cmd5, "rows") else cmd5
            fresh = beside(grey_tag("real run · fresh clone"), t, rr, buff=0.4)
            pin(self, rr, fresh, run_time=0.4)
            vo.wait_until("the collection does not exist")
            r25 = rows_with(out5, "NotFoundError")[0]
            r25b = out5[-1]
            self.play(Indicate(substring(r25b, "does not exist"), color=ERR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("That's line 429")
            r9 = rows_with(out5, "line 429")[0]
            resize(self, t, 3, keep=[r9, r25, r25b], run_time=0.6)
            code = src_panel("cli.py", 427, 429)
            place(code, cx=0, cy=(TOP_Y + GAP_Y) / 2)
            bar = code.bar(429, ERR, 0.25)
            self.play(FadeIn(code, shift=UP * 0.15), Indicate(substring(r9, "line 429"), color=TURN),
                      run_time=0.7)
            self.play(FadeIn(bar), run_time=0.5)
            vo.wait_until("before any call to Gemini")
            self.play(Indicate(code.span(429, "client.get_collection(name=collection_name)"), color=ERR,
                               scale_factor=1.04), run_time=0.8)

        # ========================================================== 6 · two ways to the index
        dvol = VGroup(mono("docker-volumes/chromadb", CAPTION, INK), label("· skip ahead", CAPTION, INK))
        dvol.arrange(RIGHT, buff=0.14)
        dnote = VGroup(note("chunked before September 22, 2026? git pull, then chunk → embed → load"),
                       note("the book changed (explained soon)")).arrange(DOWN, aligned_edge=LEFT,
                                                                         buff=0.1)
        card_a = path_card("kept lecture 5's database?", [dvol, dnote])
        c_chunk = mono(README_CHUNK, CAPTION, INK)
        e_cmd = mono(README_EMBED, CAPTION, INK)
        e_note = note("needs your key")
        e_row = VGroup(e_cmd, e_note).arrange(RIGHT, buff=0.4)
        c_load = label("then the load step", CAPTION, INK)
        bhead = VGroup(note("README.md · lines 103, 129"), expected_tag()).arrange(RIGHT, buff=0.15)
        card_b = path_card("no database?", [c_chunk, e_row, c_load], right=bhead)
        place(card_a, cx=0, top=TOP_Y)
        place(card_b, cx=0, bottom=GAP_Y)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(code, bar)), run_time=0.4)
            self.play(Indicate(substring(r25, "char-split-collection"), color=TURN, scale_factor=1.08),
                      run_time=0.9)
            vo.wait_until("Kept that database?")
            self.play(FadeIn(card_a.frame), FadeIn(card_a.title, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("It's in the docker volumes folder")
            self.play(FadeIn(dvol, shift=RIGHT * 0.1), run_time=0.5)
            self.play(Indicate(dvol[0], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("if you chunked before September 22")
            self.play(FadeIn(dnote, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("Otherwise, chunk, embed and load again")
            self.play(FadeIn(card_b.frame), FadeIn(card_b.title, shift=RIGHT * 0.1), FadeIn(bhead),
                      run_time=0.5)
            self.play(FadeIn(c_chunk, shift=RIGHT * 0.1), run_time=0.4)
            self.play(FadeIn(e_cmd, shift=RIGHT * 0.1), FadeIn(e_note), run_time=0.4)
            self.play(FadeIn(c_load, shift=RIGHT * 0.1), run_time=0.4)

        # ========================================================== 7 · the staff's embeddings stand in
        kg = key_glyph(0.3)
        staff = staff_panel()
        rec7 = grey_tag("recorded · the staff's vectors")
        with self.voiceover(SAY[7]) as vo:
            dy = TOP_Y - card_b.get_top()[1]
            self.play(FadeOut(card_a), card_b.animate.shift(UP * dy), run_time=0.7)
            kg.next_to(e_cmd, RIGHT, buff=0.25)
            self.play(e_note.animate.next_to(kg, RIGHT, buff=0.25), FadeIn(kg, scale=1.3), run_time=0.5)
            self.play(Indicate(kg, color=TURN, scale_factor=1.3), run_time=0.5)
            vo.wait_until("the staff's committed embeddings")
            place(staff, left=-6.15, top=card_b.get_bottom()[1] - 0.3)
            rec7.next_to(staff.frame, RIGHT, buff=0.35).align_to(staff.frame, DOWN)
            arr = Arrow(staff.frame.get_right() + RIGHT * 0.08,
                        kg.get_bottom() + DOWN * 0.04, color=S.GREY, stroke_width=3, buff=0.04,
                        max_tip_length_to_length_ratio=0.08)
            self.play(FadeIn(staff, shift=LEFT * 0.6), run_time=0.6)
            self.play(GrowArrow(arr), FadeIn(rec7, shift=LEFT * 0.1), run_time=0.6)

        # ========================================================== 8 · load, get, ▶
        chip8 = load_chip()
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(card_b, kg, staff, rec7, arr)), run_time=0.5)
            tr = switch_section(self, tr, "Load", 1, run_time=0.6)
            resize(self, t, LOAD_ROWS, run_time=0.6)
            place(chip8, left=-6.3, cy=(t.box.get_top()[1] + tr.get_bottom()[1]) / 2)   # under the tracker
            self.play(FadeIn(chip8, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("python cli.py, dash dash load")
            type_cmd(self, t, LOAD.cmd, 1.2)
            # two prints: Terminal.print makes room for one batch only up to the terminal's height
            out8 = t.print(self, LOAD.at((2, 8)), wrap=True, run_time=0.6)
            out8 = VGroup(*out8, *t.print(self, LOAD.at("…", 142, 152, 153), wrap=True, run_time=0.5))
            bare_prompt(self, t)                         # the command is done: the prompt returns
            vo.wait_until("11 books")
            r8 = rows_with(out8, "Number of files to process")[0]
            self.play(Indicate(substring(r8, "11"), color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("8,248 chunks")
            dots = [r for r in out8 if getattr(r, "text", "") == "…"][0]
            cnt = beside(tag("8,248 chunks in 11 books · 24 from the instructor's story", S.GREY,
                             size=CAPTION), t, dots, buff=0.4)
            pin(self, dots, cnt, run_time=0.5)
            vo.wait_until("the instructor's story is just 24")
            r153 = rows_with(out8, "Finished inserting 24")[0]
            r142 = rows_with(out8, "Tolminc")[0]
            self.play(Indicate(substring(r153, "24"), color=TURN, scale_factor=1.3),
                      Indicate(substring(r142, "Tolminc"), color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("An extra get command")
            self.play(caption_extra(tr, True), run_time=0.4)
            g8 = type_cmd(self, t, GET.cmd, 1.0)
            gr = g8.rows[-1] if hasattr(g8, "rows") else g8
            ex8 = beside(extra_tag(), t, gr)
            pin(self, gr, ex8, run_time=0.3)
            t.print(self, [GET_ROW], run_time=0.5)
            vo.wait_until("pause, and load yours")
            card8 = turn_card([(LOAD.cmd, "or keep yours"), (GET.cmd, "extra")], header=None)
            self.play(FadeOut(chip8), run_time=0.3)
            resize(self, t, 3, run_time=0.6)
            place(card8, cx=0, cy=(TOP_Y + GAP_Y) / 2)
            self.play(FadeIn(card8, shift=UP * 0.15), run_time=0.6)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, t, card8)), run_time=0.8)
        self.wait(0.3)


def load_chip() -> VGroup:
    """The one-line README chip of the load step's second line (README.md:152): it loads
    recursive-split too, which the agent does not use."""
    where = note("README.md · line 152:")
    ex = mono("recursive-split", CAPTION, INK)
    gl = note("too · the agent uses char-split")
    row = VGroup(where, ex, gl).arrange(RIGHT, buff=0.16)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    tg = expected_tag().next_to(fr, RIGHT, buff=0.15)
    assert README_152.endswith("recursive-split")
    return VGroup(fr, row, tg)
