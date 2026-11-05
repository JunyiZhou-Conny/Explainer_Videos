"""S06 · v2: four containers, and the cheese books (AC215 L18, part 1). No tracker in beats 0–2; tracker
[SE] "README › Setup Environments · Environment Setup" 4 in beat 3, then [V] "README › Tutorial: Vector
DB for RAG Setup" 1 → 5. Lecture: 18 · 45 (APIs) in beat 4.

Beats (script.md "## S06", one voiceover block each):
0. A README card (README.md · lines 5–10: the table's Container, On your laptop and What it is
   columns; the Folder column and the long descriptions cut with a GREY '…') morphs into V5
   TwoLocalhosts: each container cell becomes its TEAL box, each URL its PINK door, around them the
   GREY laptop and the GREEN cable cheese-app-network. On "Chroma" the vector-db box and door 8000
   light, "a loader" the CLI box, "the API on 9000", "the React frontend on 3000".
1. V5 goes. The prerequisites card (EXPECTED(expected/01-prerequisites.txt: 5–8) drawn as a
   checklist, tag "illustration · README:13–18"): a BLUE cloud + "Google Cloud project + Vertex AI
   API", a GREY key + "ml-workflow.json · Vertex AI User", a GOLD disk chip "about 10 GB"; on "With
   your key" the GOLD cost tag hangs on the BLUE item.
2. The key gets a GREY chip "this recording: a well-formed key for no account". A small diagram
   under the card: a GREY laptop with three TEAL boxes, GREEN-ticked one by one on "Everything that
   does not call Google"; on "the first Google call fails" one PINK arrow out to the BLUE Vertex AI
   cloud with a RED "account not found" at its tip.
3. Tracker [SE] 4. The `laptop` terminal (11 rows, prompt ~/cheese-app-v2) with the GREY chip
   "cd ~/cheese-app-v2" above it. It types b03's sed line (title-bar tag extra, chip "or edit both
   files") and `git diff` → b03:3 (cut), 4, 7, 11–12, 16 (cut), 17, 20, 24–25; on "Ours shows a
   placeholder" `your-gcp-project` GREEN on the + lines.
4. Tracker [SE] → [V] 1, lecture_ref 45 (APIs). The terminal clears and shrinks to a 3-row strip;
   a small GREY card "slide 45 (APIs) · step 1: make sure the vector database is running". It types
   `cd src/vector-db` (b05, no output: the prompt changes); tracker [V] 2, `./docker-shell.sh`;
   ▶ your turn on the bar.
5. Lecture tag and card off; the empty V5 laptop above the strip. "creates the network": b06:2 with
   the bar tag "docker network create · cheese-app-network" while the GREEN cable draws; "builds the
   loader": b06:3 (cut), …, 24 (cut); "Compose starts Chroma": b06:27 (cut, row tag "at the time of
   recording"), 28 (cut, TEAL) while the vector-db and CLI boxes come in and the vector-db box
   lights. "publishing 8000": door 8000 pulses, then V5 gives way to CODE(vector-db/docker-compose.yml:
   19–25) (no room for both side by side) with `8000:8000` PINK; "a folder on your laptop":
   `./docker-volumes/chromadb:/data` GREEN.
6. Tracker [V] 3. The panel goes, the terminal grows to 10 rows: b06:31–34, 36–42 (wrapped); at
   b06:44's prompt it types the --download --load line → b06:50, 52 ("11" YELLOW), 53 (wrap), 65
   (wrap), …, 197 (wrap), 208 (wrap). A YELLOW counter above the terminal sums the eleven "Finished
   inserting" numbers (b06:65 … 208) book by book and lands on 14,356 GREEN. ▶ your turn on the bar.
7. The terminal shrinks to a strip; a `laptop · second tab` (4 rows) comes in at the top while the
   counter slides down between the two; the tab types b09 (title-bar tag extra) → b09:25–27; a GREY
   dashed card "Lecture 5 · chunk → embed" slides in beside the counter, and a dashed arrow from it
   up to the row tag "downloaded, not recomputed" beside `78.8M outputs` (which flashes).
8. Tracker [V] 4. Tab, card and counter go; the terminal grows to 10 rows and types the --chat line
   at b06:209's prompt → b06:211, 212, 219–222 (220 YELLOW: the embedding call), …, 297 (wrap, RED). A
   small inset above: the GREY laptop chip → PINK arrow with the GOLD cost tag → BLUE Vertex AI cloud;
   on "fails here" a RED cross at the arrow's tip; on "With your key" the GREY chip "with your key:
   an answer from the books".
9. The inset goes; the terminal shrinks to a strip (297 stays). CODE(vector-db/cli.py: 370–378,
   line 374 cut), line 377 YELLOW, the GREY chip "fixed question · edit this line" beside it.
10. Tracker [V] 5. The panel goes; at b06:298's prompt it types `exit` → b06:299. V5 (the vector-db
   row with the CLI and the cable) returns above the strip. Tracker [V] 5 · extra: the strip types b07
   → b07:2–3 (wrapped), `0.0.0.0:8000->8000/tcp` PINK while door 8000 pulses; then b10 → b10:2. On
   "the network's phone book" a GREEN card opens on the cable; on "turns its name into an address"
   its first entry writes on: the name, an arrow, then the address 172.19.0.2. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources (checked)
B03 = capture("b03")
B05 = capture("b05")
B06 = capture("b06")
B07 = capture("b07")
B09 = capture("b09")
B10 = capture("b10")
assert B03.cmd_lines[0].startswith("sed -i 's/\"ac215-project\"/\"your-gcp-project\"/'") and B03.cmd_lines[1] == "git diff"
assert B03.line(3).startswith("diff --git a/src/api-service/docker-shell.sh")
assert B03.line(16).startswith("diff --git a/src/vector-db/docker-shell.sh")
assert B03.line(12) == '+export GCP_PROJECT="your-gcp-project" # CHANGE TO YOUR PROJECT ID', B03.line(12)
assert B03.line(25) == B03.line(12)
assert B05.cmd == "cd src/vector-db" and B05.lines == [], B05.lines
assert B06.cmd == "./docker-shell.sh"
assert len(B06.line(2)) == 64 and all(c in "0123456789abcdef" for c in B06.line(2))
assert B06.line(3).startswith("[+] Building 29.2s (11/11) FINISHED")
assert "naming to docker.io/library/cheese-app-vector-db-cli:latest" in B06.line(24)
assert "Image chromadb/chroma:1.5.9    Pulled" in B06.line(27)
assert "Container cheese-app-vector-db Created" in B06.line(28)
assert B06.line(31) == "Container is running!!!" and B06.line(37).strip().startswith("python cli.py --download")
assert at_prompt(B06, 44)[1] == "python cli.py --download --load --chunk_type recursive-split"
assert B06.line(52) == "Number of files to process: 11"
assert at_prompt(B06, 209)[1] == "python cli.py --chat --chunk_type recursive-split"
assert B06.line(220).strip() == "query_embedding = generate_query_embedding(query)"
assert B06.line(297).startswith("google.auth.exceptions.RefreshError: ('invalid_grant: Invalid grant: account not found'")
assert at_prompt(B06, 298)[1] == "exit" and B06.line(299) == "exit"
for _n, _k in zip(BOOK_LINES, BOOK_CHUNKS):
    assert B06.line(_n) == f"Finished inserting {_k} items into collection 'recursive-split-collection'", _n
assert B07.line(3).startswith("cheese-app-vector-db") and B07.line(3).endswith("0.0.0.0:8000->8000/tcp")
assert B09.at(26, 27) == ["78.8M   outputs", "50.9M   docker-volumes/chromadb"], B09.at(26, 27)
assert B10.line(2) == f"{C_VDB} {VDB_IP}/16", B10.line(2)

PRE = recorded("01", (5, 8))            # expected/01-prerequisites.txt (README:15–18)
assert "Google Cloud project with the Vertex AI API" in PRE[0]
assert "ml-workflow.json" in PRE[1] and "Vertex AI User" in PRE[2] and "About 10 GB" in PRE[3], PRE

COMPOSE = f"{V2}/src/vector-db/docker-compose.yml"
assert excerpt(COMPOSE, 23, 23).strip() == "- 8000:8000"
assert excerpt(COMPOSE, 25, 25).strip().startswith("- ./docker-volumes/chromadb:/data")
CLI = f"{V2}/src/vector-db/cli.py"
assert excerpt(CLI, 377, 377).strip() == 'query = "How is cheese made?"'
assert excerpt(CLI, 370, 370).strip() == 'print("chat()")'

TABLE = [md_plain(s) for s in excerpt(f"{V2}/README.md", 5, 10).split("\n")]
assert TABLE[0] == "Folder · Container · On your laptop · What it is", TABLE[0]
ROWS = [s.split(" · ") for s in TABLE[2:]]
assert [r[1] for r in ROWS] == [C_VDB, C_CLI, C_API, C_REACT], ROWS
assert [r[2] for r in ROWS] == ["http://localhost:8000", "none", "http://localhost:9000", "http://localhost:3000"]
ROW_KEYS = ("vdb", "cli", "api", "front")


# ------------------------------------------------------------------ local helpers
def _what(s: str, n: int = 30) -> str:
    """The README's 'What it is' cell, cut at a word boundary with the house '…'."""
    if len(s) <= n:
        return s
    k = s.rfind(" ", 0, n)
    return s[:k].rstrip(",:") + "…"


def _table() -> VGroup:
    """README 5–10 as the card shows it: header row (GREY) and four rows (Container mono, On your laptop
    mono PINK, What it is label); the Folder column is left out (a GREY note says so). .cells[i] = (name,
    url, what)."""
    hdr = [label("Container", 20, S.GREY), label("On your laptop", 20, S.GREY), label("What it is", 20, S.GREY)]
    rows = [[mono(r[1], 20, INK), mono(r[2], 20, ROUTE if r[2] != "none" else S.GREY), label(_what(r[3]), 20, INK)]
            for r in ROWS]
    grid = VGroup(*[VGroup(*c) for c in [hdr] + rows])
    col_x = [0.0]
    for j in range(2):
        col_x.append(col_x[-1] + max(r[j].width for r in [hdr] + rows) + 0.45)
    for i, r in enumerate([hdr] + rows):
        y = -i * 0.5
        for j, m in enumerate(r):
            m.move_to([col_x[j] + m.width / 2, y, 0])
    grid.cells = rows
    return grid


def mark_extra(scene, t: Terminal, line, kind=None):
    """PLAYS: the row tag 'extra' beside a typed command, or on the terminal's title bar when the
    command's last row leaves no room (it rides the bar until replaced). Returns the tag."""
    tg = beside(extra_row(kind), line, buff=0.4)
    if tg.get_right()[0] <= t.box.get_right()[0] - 0.1:
        pin(scene, line, tg)
        return tg
    return bar_tag(scene, t, extra_row(kind))


def bar_tag(scene, t: Terminal, tg):
    """PLAYS: a row-sized tag on the terminal's title bar (replacing the one there)."""
    old = getattr(t, "bar_tag", None)
    on_bar(t, tg)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    else:
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    t.add(tg)
    t.bar_tag = tg
    return tg


def clear_bar(scene, t: Terminal, *extra):
    """PLAYS: the title-bar tag (if any) leaves."""
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), *extra, run_time=0.3)
        t.bar_tag = None
    elif extra:
        scene.play(*extra, run_time=0.3)


def clear_lines(scene, t: Terminal, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def recolor(scene, row, sub: str, color, run_time: float = 0.4):
    """PLAYS: colour `sub` inside terminal row `row` (then re-seat the terminal)."""
    scene.play(substring(row, sub).animate.set_color(color), run_time=run_time)


def chunk_counter(value: int, color=TURN) -> VGroup:
    """The counter: a GREY 'chunks loaded' label over a big mono number."""
    num = mono(f"{value:,}", 36, color)
    lab = label("chunks loaded", 20, S.GREY)
    return VGroup(lab, num).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)


class VectorDb(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 11, len(SAY)

        # ========================================================== 0. the README's table becomes the laptop
        grid = _table()
        cut_note = label("Folder column and long descriptions cut", 20, S.GREY)
        body = VGroup(grid, cut_note)
        cut_note.next_to(grid, DOWN, buff=0.3).align_to(grid, LEFT)
        card0 = readme_card((5, 10), body)
        card0.move_to([0, 0.3, 0])
        assert card0.width < 2 * SAFE_X - 0.2, card0.width
        net = TwoLocalhosts(rows=("front", "api", "vdb"), front="react", cli=True, cable=True).move_to([0, 0.1, 0])
        net.shift(np.array([-net.frame.get_center()[0], 0.1 - net.frame.get_center()[1], 0]))
        targets = {"vdb": net.boxes["vdb"], "cli": net.cli, "api": net.boxes["api"], "front": net.boxes["front"]}
        doors = {"vdb": net.doors["vdb"], "api": net.doors["api"], "front": net.doors["front"]}
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(card0, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("four containers")
            self.play(each([r[0] for r in grid.cells], CONTAINER), run_time=0.8)
            vo.wait_until("on one Docker network")
            copies, anims = [], []
            for key, cells in zip(ROW_KEYS, grid.cells):
                tgt = targets[key].copy()
                copies.append(tgt)
                anims.append(FadeTransform(cells[0], tgt))
                if key in doors:
                    dc = doors[key].copy()
                    copies.append(dc)
                    anims.append(FadeTransform(cells[1], dc))
                else:
                    anims.append(FadeOut(cells[1]))
                anims.append(FadeOut(cells[2]))
            rest = VGroup(card0.frame, card0.head, *[m for m in grid[0]], cut_note)
            self.play(*anims, FadeOut(rest), FadeIn(net), run_time=1.3)
            self.remove(*copies)
            self.add(net)
            self.play(Indicate(net.cable, color=OWN, scale_factor=1.04), Indicate(net.net_label, color=OWN), run_time=0.7)
            net.heal(self)
            vo.wait_until("Chroma, the vector database")
            self.play(net.light("vdb", TURN), net.door_pulse("vdb"), run_time=0.6)
            vo.wait_until("a loader")
            self.play(net.normal("vdb"), net.cli.frame.animate.set_stroke(TURN), run_time=0.5)
            vo.wait_until("the API on 9000")
            self.play(net.cli.frame.animate.set_stroke(CONTAINER), net.light("api", TURN), net.door_pulse("api"),
                      run_time=0.6)
            vo.wait_until("and the React frontend")
            self.play(net.normal("api"), net.light("front", TURN), net.door_pulse("front"), run_time=0.6)
            self.wait(0.4)
            self.play(net.normal("front"), run_time=0.4)

        # ========================================================== 1. prerequisites, as a checklist
        cl = cloud_shape(None, CLOUD, cloud_w=0.62)
        it1 = VGroup(cl, label("Google Cloud project + Vertex AI API", 20, CLOUD)).arrange(RIGHT, buff=0.22)
        kg = key_glyph(0.62, S.GREY, dashed=False)
        it2 = VGroup(kg, mono("ml-workflow.json", 20, INK), label("· Vertex AI User", 20, S.GREY)).arrange(RIGHT, buff=0.18)
        it3 = disk_chip("about 10 GB")
        pre = card([it1, it2, it3], head="README · Prerequisites", buff=0.3)
        pre.move_to([-6.45 + pre.width / 2, 2.6 - pre.height / 2, 0])
        ill = illustration_tag("illustration · README:13–18")
        ill.next_to(pre.frame, UP, buff=0.08).align_to(pre.frame, LEFT).shift(RIGHT * 0.2)   # above: on the edge it covered the head
        cost = cost_tag("with your key: chat and embedding calls bill your project")
        cost.move_to([6.45 - cost.width / 2, 3.2, 0])       # above the card's right end (no tracker yet)
        assert cost.get_bottom()[1] > pre.get_top()[1] + 0.05, (cost.get_bottom(), pre.get_top())
        cost_tie = DashedLine(it1.get_right() + RIGHT * 0.12, [it1.get_right()[0] + 0.45, cost.get_bottom()[1], 0],
                              color=COST, stroke_width=2, dash_length=0.08)
        assert cost.get_right()[0] < SAFE_X - 0.05, cost.get_right()
        assert cost.get_left()[0] < it1.get_right()[0] + 0.25 and ill.get_top()[1] < cost.get_bottom()[1] + 0.6, cost.get_left()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(net), run_time=0.5)
            self.play(FadeIn(pre.frame), FadeIn(pre.head), FadeIn(ill), run_time=0.5)
            vo.wait_until("a Google Cloud project")
            self.play(FadeIn(it1, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("with the Vertex AI API")
            self.play(Indicate(it1[1], color=CLOUD, scale_factor=1.05), run_time=0.6)
            vo.wait_until("the ml workflow key")
            self.play(FadeIn(it2, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("and about 10 gigabytes")
            self.play(FadeIn(it3, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("With your key")
            self.play(Create(cost_tie), FadeIn(cost, shift=LEFT * 0.15), run_time=0.6)
            flash_tag(self, cost, COST)

        # ========================================================== 2. the honest note: a key for no account
        kchip = grey_chip("this recording: a well-formed key for no account")
        kchip.next_to(it2, RIGHT, buff=0.3)
        kchip.shift(RIGHT * max(0.0, pre.get_right()[0] + 0.25 - kchip.get_left()[0]))
        ktie = DashedLine(it2.get_right() + RIGHT * 0.08, kchip.get_left(), color=S.GREY, stroke_width=2, dash_length=0.08)
        assert kchip.get_right()[0] < SAFE_X - 0.05, kchip.get_right()
        lap = RoundedRectangle(width=5.2, height=2.0, corner_radius=0.14, stroke_color=LAPTOP,
                               stroke_width=3).set_fill(S.BG, 1).move_to([-3.6, -2.35, 0])
        lap_t = label("your laptop", 20, LAPTOP).next_to(lap.get_corner(UR), DL, buff=0.12)
        minis = VGroup(*[RoundedRectangle(width=1.1, height=0.62, corner_radius=0.08, stroke_color=CONTAINER,
                                          stroke_width=3).set_fill(tint(CONTAINER), 1) for _ in range(3)])
        minis.arrange(RIGHT, buff=0.45).move_to(lap).shift(DOWN * 0.22)
        ticks = VGroup(*[check_glyph(0.34, OWN).move_to(m) for m in minis])
        vx = cloud_shape("Vertex AI", CLOUD, cloud_w=2.6).move_to([3.6, -2.35, 0])
        call = route(lap.get_right() + RIGHT * 0.05, vx.get_left() + RIGHT * 0.05, color=ROUTE)
        miss = err_chip("account not found").next_to(vx, UP, buff=0.12)
        miss.shift(RIGHT * (call.get_end()[0] - miss.get_center()[0]))
        xmark = cross_glyph(0.3).move_to(call.get_end() + LEFT * 0.25)
        assert lap.get_top()[1] < pre.get_bottom()[1] - 0.15, (lap.get_top(), pre.get_bottom())
        assert miss.get_top()[1] < pre.get_bottom()[1] - 0.1 and vx.get_right()[0] < SAFE_X, miss.get_top()
        with self.voiceover(SAY[2]) as vo:
            self.play(Create(ktie), FadeIn(kchip, shift=LEFT * 0.15), run_time=0.6)
            self.play(Indicate(kg, color=S.GREY, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Everything that does not call Google")
            self.play(FadeIn(lap), FadeIn(lap_t), LaggedStart(*[FadeIn(m) for m in minis], lag_ratio=0.2), run_time=0.7)
            self.play(LaggedStart(*[Create(c) for c in ticks], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("the first Google call fails")
            self.play(FadeIn(vx), run_time=0.4)
            self.play(GrowArrow(call), run_time=0.6)
            self.play(FadeIn(xmark, scale=1.3), FadeIn(miss, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and we show where")
            self.play(Indicate(miss.text, color=ERR, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3. setup step 4: your project id in both scripts
        trk = tracker_se(4)
        t = term(P_V2, rows=11, title=T_LAPTOP, size=20)
        cdc = grey_chip("cd ~/cheese-app-v2", mono_font=True).next_to(t.box, UP, buff=0.14).align_to(t.box, LEFT)
        edc = grey_chip("or edit both files")
        under_term(t, edc, buff=0.14)
        assert cdc.get_top()[1] < TRACK_BOTTOM - 0.05, cdc.get_top()
        diff = [cut(B03.line(3), "api-service/docker-shell.sh"), B03.line(4), B03.line(7),
                B03.line(11), B03.line(12), cut(B03.line(16), "vector-db/docker-shell.sh"),
                B03.line(17), B03.line(20), B03.line(24), B03.line(25)]
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(pre, ill, cost, cost_tie, kchip, ktie, lap, lap_t, minis, ticks, vx, call,
                                     miss, xmark)), run_time=0.5)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t), FadeIn(cdc, shift=DOWN * 0.1), run_time=0.5)
            sed_ln = type_capture(self, t, B03, type_time=0.6)
            bar_tag(self, t, extra_row())
            self.play(FadeIn(edc, shift=DOWN * 0.1), run_time=0.3)
            rows3 = out(self, t, diff, run_time=0.7)
            vo.wait_until("Ours shows a placeholder")
            plus = [r for r in rows3 if r.text.startswith("+export")]
            self.play(*[substring(r, PROJECT_PH).animate.set_color(OWN) for r in plus], run_time=0.4)
            self.play(*[Indicate(substring(r, PROJECT_PH), color=OWN, scale_factor=1.08) for r in plus], run_time=0.6)
            self.add(t)
        del sed_ln

        # ========================================================== 4. the lecture's first step; cd, docker-shell.sh
        trk2 = tracker_v(1)
        lref("45 (APIs)")                      # validates the deck name; lecture_ref() would read 'slides 45'
        ref = tag("Lecture 18 · slide 45 (APIs)", S.GREY)
        ref.move_to([6.6 - ref.width / 2, 3.6 - ref.height / 2, 0])
        slide = card(["step 1: make sure the vector database is running"], head="slide 45 (APIs)", size=24)
        slide.move_to([0, 0.6, 0])
        with self.voiceover(SAY[4]) as vo:
            clear_bar(self, t, FadeOut(cdc), FadeOut(edc))
            clear_lines(self, t)
            swap_tracker(self, trk, trk2)
            trk = trk2
            resize(self, t, 3, run_time=0.5)
            vo.wait_until("The lecture's first step")
            self.play(FadeIn(ref), FadeIn(slide, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("make sure the vector database")
            self.play(Indicate(slide.body, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("Step 1")
            type_capture(self, t, B05, type_time=0.5)
            cd_prompt(self, t, P_V2_VDB)
            vo.wait_until("and run docker-shell.sh")
            self.play(track(trk, 2), run_time=0.4)
            type_capture(self, t, B06, type_time=0.4)
            vo.wait_until("Pause and run them")
            turn = bar_tag(self, t, turn_row())
            flash_tag(self, turn, TURN)
            self.add(t)

        # ========================================================== 5. network, loader, Chroma on 8000 with a host folder
        net5 = TwoLocalhosts(rows=("vdb",), front="react", cli=True, built=False)
        net5.shift(np.array([0.3, 0.75, 0]))
        assert net5.frame.get_bottom()[1] > t.box.get_top()[1] + 0.1, (net5.frame.get_bottom(), t.box.get_top())
        assert net5.frame.get_top()[1] < PIC_TOP, net5.frame.get_top()
        panel = code(COMPOSE, 19, 25, font_size=20, dedent=True, shown="vector-db/docker-compose.yml",
                     cuts={20: "chromadb/chroma:1.5.9", 25: ":/data"})
        panel.move_to([0, 0.75, 0])
        assert panel.get_bottom()[1] > t.box.get_top()[1] + 0.1 and panel.get_top()[1] < PIC_TOP, panel.get_top()
        build5 = [cut(B06.line(3), "FINISHED"), "…", cut(B06.line(24), "cheese-app-vector-db-cli:latest")]
        with self.voiceover(SAY[5]) as vo:
            clear_bar(self, t, FadeOut(slide), FadeOut(ref))
            self.play(FadeIn(net5), run_time=0.5)
            vo.wait_until("creates the network")
            out(self, t, [B06.line(2)], run_time=0.3)
            bar_tag(self, t, row_tag("docker network create"))
            net5.cable_on(self, run_time=0.8)
            vo.wait_until("builds the loader")
            clear_bar(self, t)
            o5 = out(self, t, build5, run_time=0.5)
            recolor(self, o5[-1], "cheese-app-vector-db-cli", CONTAINER)
            self.add(t)
            vo.wait_until("and Compose starts Chroma")
            o27 = out(self, t, [cut(B06.line(27), "Pulled"), (cut(B06.line(28), "Created"), CONTAINER)], run_time=0.4)
            net5.add_box(self, "vdb", run_time=0.6)
            pin(self, o27[0], beside(time_row(), o27[0], buff=0.5))
            self.play(net5.light("vdb", TURN), run_time=0.4)
            vo.wait_until("publishing 8000")
            self.play(net5.door_pulse("vdb", ROUTE), run_time=0.6)
            self.play(FadeOut(net5, shift=LEFT * 0.3), FadeIn(panel, shift=LEFT * 0.3), run_time=0.6)
            self.play(code_span(panel.code, 4, "8000:8000").animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(code_span(panel.code, 4, "8000:8000"), color=ROUTE, scale_factor=1.12), run_time=0.6)
            self.add(panel)
            vo.wait_until("keeping its data")
            vol = code_span(panel.code, 6, "./docker-volumes/chromadb:/data")
            u = under(vol, OWN)
            self.play(vol.animate.set_color(OWN), Create(u), run_time=0.6)
            self.add(panel)
            self.wait(1.0)

        # ========================================================== 6. step 2: download and load the cheese books
        cnt = chunk_counter(0).move_to([5.0, 2.05, 0])
        cnt.shift(RIGHT * (6.45 - cnt.get_right()[0]))
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(panel), FadeOut(u), track(trk, 3), run_time=0.5)
            resize(self, t, 10, run_time=0.5)
            assert cnt.get_bottom()[1] > t.box.get_top()[1] + 0.1, (cnt.get_bottom(), t.box.get_top())
            out(self, t, B06.at((31, 34), (36, 42)), wrap=True, run_time=0.8)
            vo.wait_until("download and load")
            type_at(self, t, B06, 44, type_time=0.8)
            vo.wait_until("Eleven files")
            o52 = out(self, t, [B06.line(50), B06.line(52)], run_time=0.4)
            recolor(self, o52[-1], "11", TURN)
            self.add(t)
            vo.wait_until("one finished line per book")
            o53 = out(self, t, [B06.line(53), (B06.line(65), TURN)], wrap=True, run_time=0.5)
            self.play(FadeIn(cnt, shift=DOWN * 0.1), run_time=0.3)
            total = 0
            for i, k in enumerate(BOOK_CHUNKS):
                total += k
                new = chunk_counter(total).move_to(cnt, aligned_edge=RIGHT)
                if i == 1:
                    out(self, t, ["…", B06.line(197), (B06.line(208), TURN)], wrap=True, run_time=0.4)
                self.play(Transform(cnt, new), run_time=0.22)
            assert total == CHUNKS
            vo.wait_until("14,356 chunks in all")
            self.play(cnt[1].animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(cnt[1], color=OWN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Pause while yours loads")
            turn6 = bar_tag(self, t, turn_row())
            flash_tag(self, turn6, TURN)
            self.add(t)
        del o53

        # ========================================================== 7. the RAG lecture's outputs, downloaded
        tab = term(P_V2_VDB, rows=5, title=T_TAB, size=20, place=False)
        tab.shift(np.array([-tab.box.get_center()[0], 2.7 - tab.box.get_top()[1], 0]))      # the tab on top
        l5 = dashed_chip("Lecture 5 · chunk → embed", size=22)
        with self.voiceover(SAY[7]) as vo:
            clear_bar(self, t)
            resize(self, t, 3, run_time=0.4)
            band_y = (tab.box.get_bottom()[1] + t.box.get_top()[1]) / 2 - 0.1     # between the tab and the strip
            cnt_to = cnt.copy().move_to([0, band_y, 0])
            cnt_to.shift(RIGHT * (6.45 - cnt_to.get_right()[0]))
            assert cnt_to.get_top()[1] < tab.box.get_bottom()[1] - 0.1 and cnt_to.get_bottom()[1] > t.box.get_top()[1] + 0.1
            self.play(FadeIn(tab, shift=DOWN * 0.15), Transform(cnt, cnt_to), run_time=0.5)
            ln9 = type_capture(self, tab, B09, type_time=0.6)[0]
            mark_extra(self, tab, ln9)
            o9 = out(self, tab, B09.at((25, 27)), run_time=0.4)
            vo.wait_until("the RAG lecture")
            l5.move_to([1.7, cnt.get_center()[1], 0])
            assert l5.get_right()[0] < cnt.get_left()[0] - 0.2, (l5.get_right(), cnt.get_left())
            self.play(FadeIn(l5, shift=RIGHT * 0.4), run_time=0.5)
            vo.wait_until("downloaded")
            dn = row_tag("downloaded, not recomputed")
            pin(self, o9[1], beside(dn, o9[1], min_x=0.0))
            assert o9[2].strut.get_right()[0] < dn.get_left()[0] - 0.3, "the arrow must pass clear of b09:27"
            arr = DashedVMobject(Arrow(l5.get_top(), dn.get_bottom() + DOWN * 0.02, buff=0.06, color=S.GREY,
                                       stroke_width=3, tip_length=0.18), num_dashes=10).set_stroke(S.GREY, 3)
            self.play(Create(arr), run_time=0.5)
            self.play(Indicate(substring(o9[1], "outputs"), color=TURN, scale_factor=1.1), run_time=0.6)
            self.add(tab)

        # ========================================================== 8. step 3: chat, and the first Google call
        inset_lap = grey_chip("laptop · cli.py")
        inset_vx = cloud_shape("Vertex AI", CLOUD, cloud_w=2.2)
        inset_lap.move_to([0.0, 2.05, 0])
        inset_vx.move_to([5.3, 2.05, 0])
        icall = route(inset_lap.get_right() + RIGHT * 0.05, inset_vx.get_left() + RIGHT * 0.1, color=ROUTE)
        icost = cost_row("with your key: billed").next_to(icall, UP, buff=0.08)
        assert icost.get_right()[0] < inset_vx.get_left()[0] - 0.05 and icost.get_left()[0] > inset_lap.get_right()[0], icost.get_right()
        ix = cross_glyph(0.28).move_to(icall.get_end() + LEFT * 0.2 + DOWN * 0.0)
        ans = grey_chip("with your key: an answer from the books")
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(tab, l5, arr, cnt)), track(trk, 4), run_time=0.5)
            resize(self, t, 10, run_time=0.5)
            assert inset_vx.get_bottom()[1] > t.box.get_top()[1] + 0.05, (inset_vx.get_bottom(), t.box.get_top())
            assert icost.get_top()[1] < PIC_TOP + 0.1 and inset_vx.get_top()[1] < PIC_TOP + 0.1, inset_vx.get_top()
            vo.wait_until("Step 3")
            type_at(self, t, B06, 209, type_time=0.7)
            vo.wait_until("The first Google call")
            self.play(FadeIn(inset_lap), FadeIn(inset_vx), run_time=0.4)
            self.play(GrowArrow(icall), FadeIn(icost, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("embedding the question")
            o8 = out(self, t, B06.at(211, 212, (219, 222)), run_time=0.5)
            self.play(o8[3].animate.set_color(TURN), run_time=0.3)
            self.add(t)
            vo.wait_until("fails here")
            out(self, t, ["…", (B06.line(297), ERR)], wrap=True, run_time=0.5)
            self.play(FadeIn(ix, scale=1.4), run_time=0.4)
            vo.wait_until("invalid grant")
            last = t.lines[-3:]
            self.play(*[Indicate(r, color=ERR, scale_factor=1.03) for r in last], run_time=0.7)
            self.add(t)
            vo.wait_until("With your key")
            ans.next_to(t.box, UP, buff=0.14).align_to(t.box, LEFT)
            assert ans.get_right()[0] < inset_lap.get_left()[0] - 0.1 or ans.get_top()[1] < inset_lap.get_bottom()[1] - 0.05, \
                (ans.get_corner(UR), inset_lap.get_corner(DL))
            self.play(FadeIn(ans, shift=DOWN * 0.1), run_time=0.5)
            flash_tag(self, ans, S.GREY)

        # ========================================================== 9. a small note: chat's fixed question
        p9 = code(CLI, 370, 378, font_size=20, shown="vector-db/cli.py", cuts={374: "# Get a collection object"})
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(inset_lap, inset_vx, icall, icost, ix, ans)), run_time=0.4)
            resize(self, t, 3, run_time=0.5)
            p9.move_to([0, (t.box.get_top()[1] + PIC_TOP) / 2, 0])
            assert p9.get_bottom()[1] > t.box.get_top()[1] + 0.05 and p9.get_top()[1] < PIC_TOP + 0.05, p9.get_top()
            self.play(FadeIn(p9, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("how is cheese made")
            q = code_span(p9.code, 7, 'query = "How is cheese made?"')
            bar = line_bar(p9.code, 7, TURN)
            self.play(FadeIn(bar), q.animate.set_color(TURN), run_time=0.5)
            self.add(p9, bar)
            fixed = row_tag("fixed question · edit this line")
            # on the blank line 376, right of line 375's end: no glyph under it
            above = code_span(p9.code, 5, 'collection_name = f"{method}-collection"')
            fixed.move_to([max(q.get_right()[0], above.get_right()[0]) + 0.4 + fixed.width / 2,
                           bar.get_top()[1] + 0.01 + fixed.height / 2, 0])     # sits on line 377's bar
            assert fixed.get_left()[0] > above.get_right()[0] + 0.2, (fixed.get_left(), above.get_right())   # past 375's end
            assert fixed.get_right()[0] < p9.get_right()[0] - 0.1, (fixed.get_right(), p9.get_right())
            vo.wait_until("there is no place to type yours")
            self.play(FadeIn(fixed, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("To ask another")
            flash_tag(self, fixed, S.GREY)
            self.play(Indicate(q, color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(p9, bar, fixed)             # the tag stays on top of the panel

        # ========================================================== 10. step 4: exit; Chroma stays; the phone book
        net10 = TwoLocalhosts(rows=("vdb",), front="react", cli=True, built=True, cable=True)
        # the strip grows to 5 rows here (b07's 2-row command + its 3 output rows stay readable together), so the
        # laptop gets a shorter frame (3.45 instead of 4.0: only the vdb row and the phone book live in it)
        net10.shift(np.array([0.3, 0.75, 0]))
        _bl = net10.frame.get_corner(DL)
        net10.frame.become(RoundedRectangle(width=net10.frame.width, height=3.45, corner_radius=0.16, stroke_color=LAPTOP,
                                            stroke_width=3).set_fill(S.BG, 1).move_to(_bl, aligned_edge=DL))
        net10.title.align_to(net10.frame, UP).shift(DOWN * 0.12)
        T10_TOP = BOTTOM + term(P_V2, rows=5, size=20).box.height
        net10.shift(UP * (T10_TOP + 0.12 - net10.frame.get_bottom()[1]))
        assert net10.frame.get_top()[1] < PIC_TOP + 0.01, net10.frame.get_top()
        hd = label(f"{NETWORK} · names", 20, NET)
        nm = mono(C_VDB, 20, INK)
        ar = label("→", 20, S.GREY)
        ad = mono(VDB_IP, 20, ROUTE)
        entry = VGroup(nm, ar, ad).arrange(RIGHT, buff=0.14)
        inner = VGroup(hd, entry).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        bfr = RoundedRectangle(width=inner.width + 0.5, height=inner.height + 0.4, corner_radius=0.12,
                               stroke_color=NET, stroke_width=2.5).set_fill(S.BG, 1)
        inner.move_to(bfr).align_to(bfr, LEFT).shift(RIGHT * 0.25)
        book = VGroup(bfr, inner)
        cab = net10.cable
        book.move_to([net10.frame.get_center()[0],
                      (net10.boxes["vdb"].get_top()[1] + net10.title.get_bottom()[1]) / 2, 0])
        assert book.get_bottom()[1] > net10.boxes["vdb"].get_top()[1] + 0.1, (book.get_bottom(), net10.boxes["vdb"].get_top())
        assert book.get_left()[0] < cab.get_x() - 0.2 < book.get_right()[0] - 0.2, (book.get_left(), cab.get_x())
        tie = Line(cab.get_top(), [cab.get_x(), book.get_bottom()[1], 0], color=NET, stroke_width=4)
        assert book.get_left()[0] > net10.frame.get_left()[0] + 0.1 and book.get_top()[1] < net10.title.get_bottom()[1] - 0.05, \
            (book.get_corner(UL), net10.title.get_bottom())
        assert book.get_right()[0] < net10.frame.get_right()[0] - 0.05, (book.get_right(), net10.frame.get_right())
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(p9, bar, fixed)), track(trk, 5), run_time=0.5)
            vo.wait_until("Step 4")
            type_at(self, t, B06, 298, type_time=0.3)
            out(self, t, [B06.line(299)], run_time=0.3)
            t.set_prompt(P_V2_VDB)
            vo.wait_until("Chroma keeps running")
            resize(self, t, 5, run_time=0.4)
            assert abs(t.box.get_top()[1] - T10_TOP) < 0.01, (t.box.get_top(), T10_TOP)
            self.play(FadeIn(net10), run_time=0.5)
            self.play(net10.light("vdb", OWN), run_time=0.4)
            vo.wait_until("as an extra docker ps shows")
            self.play(track(trk, 5, extra=True), run_time=0.4)
            type_capture(self, t, B07, type_time=0.6)
            o7 = out(self, t, B07.at(2, 3), wrap=True, run_time=0.4)
            recolor(self, o7[-1], "0.0.0.0:8000->8000/tcp", ROUTE)
            self.add(t)
            self.play(net10.door_pulse("vdb", ROUTE), run_time=0.6)
            vo.wait_until("and the network's phone book")
            type_capture(self, t, B10, type_time=0.6)
            o10 = out(self, t, [B10.line(2)], run_time=0.3)
            net10.show(self, tie, bfr, hd, anims=[Create(tie), FadeIn(bfr, scale=0.9), FadeIn(hd)], run_time=0.6)
            vo.wait_until("turns its name into an address")
            net10.show(self, nm, anims=[FadeIn(nm, shift=RIGHT * 0.1)], run_time=0.4)
            net10.show(self, ar, anims=[GrowFromCenter(ar)], run_time=0.3)
            self.play(Indicate(substring(o10[0], VDB_IP), color=ROUTE, scale_factor=1.1), run_time=0.5)
            self.add(t)
            net10.show(self, ad, anims=[FadeIn(ad, shift=RIGHT * 0.1)], run_time=0.4)
            self.play(Indicate(entry, color=NET, scale_factor=1.05), run_time=0.6)
            self.remove(entry)
            net10.heal(self)
            self.wait(0.6)

        self.play(FadeOut(net10), FadeOut(t), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
