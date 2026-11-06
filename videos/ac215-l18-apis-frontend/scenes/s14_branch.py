"""S14 · Tutorial 24 lives on branch 2025 (AC215 L18, part 2). No tracker in beats 0–2; tracker [T23]
"README @ branch 2025 › Tutorial (23): Vector DB · Backend APIs" (caption "branch 2025 · 14f2a14")
1 → 7 from beat 3 on. No lecture tag (script.md has no LECTURE line in S14).

Beats (script.md "## S14", one voiceover block each):
0. A GREY branch diagram: `main` · 447b5c3 with the folders api-service, frontend-react, vector-db
   (a dashed slot where frontend-simple was: struck RED on "Main dropped it"), and `2025` · 14f2a14
   branching off with the same folders plus frontend-simple YELLOW; last year's api-service gets the
   chip "last year's API" and an arrow "serves it" to frontend-simple. On "builds its own big images"
   a GOLD-outlined disk card: "branch 2025 builds its own API image · budget about 10 GB more ·
   short on space?" and the docker image rm line (main's four images), lit on "if your disk is tight".
1. The `laptop` terminal (13 rows, 20 pt, prompt ~/cheese-app-v2): `git switch 2025` (extra) →
   c01:2–8 (lines 2 and 8 RED, the four file names YELLOW, a row tag "your edits"); then
   `git stash && git switch 2025` (extra) → c01b:2 (from "WIP on main: 447b5c3", cut after it), 3–4,
   line 4 GREEN.
2. The terminal clears and shrinks to 7 rows. c02 (extra) → c02:2–6 (14f2a14 YELLOW, frontend-simple
   GREEN). CODE(2025 src/vector-db/docker-shell.sh:10) above, `llm-service-account.json` YELLOW, tag
   "erratum · the 2025 vector-db script reads this name"; c03 (extra) → c03:2–3, the same name
   YELLOW; c04 (extra) → c04:2–4.
3. Tracker [T23] 1. Prompt `student@laptop:~$` with the GREY chip "from the folder above
   cheese-app-v2"; `cd cheese-app-v2/src/vector-db` (c05, no output: the prompt changes); [T23] 2
   `sh docker-shell.sh` with a GREY card "docker-compose: command not found? → docker compose run
   --rm --service-ports cheese-app-vector-db-cli" → c06:3, …, 22–23, 26–30; [T23] 3 at the
   container prompt (line 33) the load → c06:41, …, 197; the chunk counter flashes to 14,356 GREEN
   with the GREY chip "your folder still holds main's data · output may differ slightly". On "tagged
   latest": `exit` (c06:198–199), then the extra c07 → c07:2–3, `chromadb/chroma:latest` YELLOW with
   "at the time of recording"; on "Chroma keeps running" its row lights GREEN.
4. Tracker [T23] 4. A new terminal `laptop · new terminal` (13 rows, prompt `student@laptop:~$`):
   `cd cheese-app-v2/src/api-service` (c10) → prompt changes; [T23] 5 `sh docker-shell.sh` → c11:3,
   …, 20, 21–25, 28–30 (13 rows, so the typed sh line stays in view); [T23] 6 at the prompt (line 32) `uvicorn_server` → c11:34–35, …, 49–50, …,
   67, 72, 74. ▶ your turn on the bar.
5. `WatchFiles` YELLOW with a GREY row tag "main: StatReload"; 49–50 and 67 YELLOW before 74. The
   terminal shrinks to a strip (67, 72, 74 stay); above it a GREY README card (2025 README.md ·
   lines 82–86, tag "read along · same idea as main") and, right, V6's two lamps GREY dashed with the
   chip "no probes yet" and the chip "2025 docs: localhost:9000/docs (no /api)".
6. Tracker [T23] 7. A `laptop · second tab` (9 rows): `curl -s -i http://localhost:9000/` (extra)
   → c12:2, 4, 8 (the JSON flashes GREEN). On "A small note": a GREY README card (lines 96–98,
   "Create Demo Routes") with the tag "erratum · already in the code", and c13 (extra) → c13:2–5, 7
   (line 30 YELLOW); on "the routers": the card becomes lines 116–118 ("Enable Cheese App API
   Routes") and c14 (extra) → c14:3–9; on "except RAG and agent" the llm-rag / llm-agent lines turn
   GREY, a bar tag "still commented out"; the chip "except RAG and agent · don't paste again" flashes.
7. The terminal goes. A TEAL API box (branch 2025) → PINK arrow → BLUE "Vertex AI · Gemini"; on the
   arrow the GREY chip "2025's model: gemini-2.0-flash-001 · us-central1"; on "retired" it is struck
   RED and the tag "erratum · with a key, chat fails until the model and region are updated" comes in;
   on "main uses" a GREEN chip "gemini-3.8-flash · global" slides from a `main` label onto the arrow.
8. CODE(2025 src/api-service/api/service.py:14–21): lines 15–16 and 18 YELLOW; a PINK permission slip
   "access-control-allow-origin: *" peels off line 18. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ the real sources (checked)
C01 = capture("c01")
C01B = capture("c01b")
C02 = capture("c02")
C03 = capture("c03")
C04 = capture("c04")
C05 = capture("c05")
C06 = capture("c06")
C07 = capture("c07")
C10 = capture("c10")
C11 = capture("c11")
C12 = capture("c12")
C13 = capture("c13")
C14 = capture("c14")
assert C01.cmd == "git switch 2025" and C01.exit == 1
assert C01.line(2).startswith("error: Your local changes") and C01.line(8) == "Aborting"
FILES = ["src/api-service/api/service.py", "src/api-service/docker-shell.sh", "src/docker-compose.yml",
         "src/vector-db/docker-shell.sh"]
assert [C01.line(n).strip() for n in range(3, 7)] == FILES
assert C01B.cmd == "git stash && git switch 2025"
assert "WIP on main: 447b5c3" in C01B.line(2) and C01B.line(4) == "Switched to a new branch '2025'"
STASH = cut(from_phrase(C01B.line(2), "WIP on main: 447b5c3"), "447b5c3")
assert STASH == "…WIP on main: 447b5c3…", STASH
assert C02.line(2).startswith("14f2a14") and C02.at((3, 6)) == ["api-service", "frontend-react", "frontend-simple",
                                                                 "vector-db"]
assert C03.at(2, 3) == ["llm-service-account.json", "ml-workflow.json"]
assert C04.cmd.startswith("sed -i 's/\"ac215-project\"/\"your-gcp-project\"/'") and "git diff --stat" in C04.cmd
assert C05.cmd == "cd cheese-app-v2/src/vector-db" and C05.lines == []
assert C06.cmd == "sh docker-shell.sh" and C06.line(3).startswith("[+] Building 36.5s (11/11) FINISHED")
assert "Image chromadb/chroma:latest   Pulled" in C06.line(22) and "Container cheese-app-vector-db Created" in C06.line(23)
assert C06.line(26) == "Container is running!!!" and C06.line(29) == "Python version: Python 3.12.16"
assert at_prompt(C06, 33)[1] == "python cli.py --download --load --chunk_type recursive-split"
assert C06.line(41) == "Number of files to process: 11"
assert C06.line(197) == "Finished inserting 163 items into collection 'recursive-split-collection'"
assert at_prompt(C06, 198)[1] == "exit" and C06.line(199) == "exit"
assert "chromadb/chroma:latest" in C07.line(3) and "Up 32 seconds" in C07.line(3)
assert C10.cmd == "cd cheese-app-v2/src/api-service" and C10.lines == []
assert C11.cmd == "sh docker-shell.sh" and C11.line(3).startswith("[+] Building 79.0s")
assert "naming to docker.io/library/cheese-app-api-service" in C11.line(20)
assert at_prompt(C11, 32)[1] == "uvicorn_server"
assert C11.line(35).endswith("using WatchFiles") and C11.line(49) == "Loading CNN Model..."
assert C11.line(67).strip().startswith("Total params") and C11.line(74) == "INFO:     Application startup complete."
assert C11.line(72) == "INFO:     Started server process [13]"
assert C12.cmd == "curl -s -i http://localhost:9000/"
# c12's last line carries the capture's own '[exit 0]' marker (curl printed no newline): drop it
JSON = re.sub(r"\[exit \d+\]$", "", C12.line(8))
assert JSON == '{"message":"Welcome to AC215"}', JSON
assert C12.at(2, 4) == ["HTTP/1.1 200 OK", "server: uvicorn"]
assert C13.line(2) == '30:@app.get("/square_root/")' and C13.line(7) == "10.198039027185569"
assert C14.line(3) == "# Additional routers here"
assert C14.line(8).startswith("# app.include_router(llm_rag_chat") and C14.line(9).startswith("# app.include_router(llm_agent")
# c14's one command line, folded by hand: Terminal.fold (explainer/devops.py) drops a character when
# it must hard-break a token (here inside the quoted python: "json.lo \\ / d(sys.stdin)"), and a soft
# wrap at the row edge splits words. These four pieces join with single spaces into the exact command;
# rows 1-2 end in ' \\' (outside any quote), row 3 breaks INSIDE the single-quoted python between
# list-comprehension clauses, where a pasted newline is still the same shell string and valid python.
C14_PIECES = ["sed -n '35,42p'", "api/service.py; curl -s http://localhost:9000/openapi.json |",
              "python3 -c 'import json,sys; [print(m.upper().ljust(6), p)",
              """for p,v in json.load(sys.stdin)["paths"].items() for m in v]'"""]
assert len(C14.cmd_lines) == 1 and " ".join(C14_PIECES) == C14.cmd_lines[0], C14.cmd_lines


def c14_rows(p: str) -> list[str]:
    """The rows c14 is typed as, after the prompt part `p`: ' \\' continuations outside the quotes,
    4-space indents; asserts they rejoin to exactly p + the captured command."""
    rows = [p + C14_PIECES[0] + " \\", "    " + C14_PIECES[1] + " \\", "    " + C14_PIECES[2],
            "    " + C14_PIECES[3]]
    back = rows[0].removesuffix(" \\") + "".join(
        " " + r[4:].removesuffix(" \\") for r in rows[1:])
    assert back == p + C14.cmd_lines[0], back
    return rows

DS_2025 = f"{V2_2025}/src/vector-db/docker-shell.sh"
assert excerpt(DS_2025, 10, 10) == 'export GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"'
SVC_2025 = f"{V2_2025}/src/api-service/api/service.py"
assert excerpt(SVC_2025, 15, 16) == "app.add_middleware(\n    CORSMiddleware,"
assert excerpt(SVC_2025, 18, 18).strip() == 'allow_origins=["*"],'
LLM_2025 = f"{V2_2025}/src/api-service/api/utils/llm_utils.py"
assert excerpt(LLM_2025, 19, 19) == 'GCP_LOCATION = "us-central1"'
assert excerpt(LLM_2025, 22, 22) == 'GENERATIVE_MODEL = "gemini-2.0-flash-001"'
SETTINGS = f"{V2}/src/api-service/api/settings.py"
assert 'os.getenv("GCP_LOCATION", "global")' in excerpt(SETTINGS, 7, 7)
assert 'os.getenv("GENERATIVE_MODEL", "gemini-3.8-flash")' in excerpt(SETTINGS, 10, 10)

R_8286 = readme_lines(82, 86, V2_2025)
assert R_8286.split("\n")[0] == "3. Review Container Configuration", R_8286
R_9698 = readme_lines(96, 98, V2_2025)
assert R_9698.split("\n") == ["Create Demo Routes", "• Open api/service.py in your editor",
                             "• Add the following code at the end of the file:"], R_9698
R_116 = readme_lines(116, 118, V2_2025)
assert R_116.split("\n") == ["Enable Cheese App API Routes", "1. Enable All Routes in api/service.py"], R_116
assert "localhost:9000/docs" in readme(112, V2_2025) and "localhost:9000/docs" in readme(142, V2_2025)

MAIN_IMAGES = [C_API, C_CLI, C_REACT, f"{C_REACT}:prod"]


# ------------------------------------------------------------------ local helpers (as in S06)
def mark_extra(scene, t: Terminal, line, kind=None):
    """PLAYS: the row tag 'extra' beside a typed command, or on the terminal's title bar when the
    command's last row leaves no room. Returns the tag."""
    tg = beside(extra_row(kind), line, buff=0.4)
    if tg.get_right()[0] <= t.box.get_right()[0] - 0.1:
        clear_bar(scene, t)
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


def clear_lines(scene, t: Terminal, *extra, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), *extra, run_time=run_time)
    scene.remove(*gone)


def row_with(rows, sub: str):
    """The first terminal row (of `rows`) whose text holds `sub`."""
    for r in rows:
        if sub in r.text:
            return r
    raise ValueError(f"{sub!r} in none of {[r.text for r in rows]}")


def paint(rows, subs, color):
    """ANIMS: colour each substring (in whichever row holds it)."""
    return [substring(row_with(rows, s), s).animate.set_color(color) for s in subs]


def folder_chip(name: str, color=S.GREY, dashed: bool = False) -> VGroup:
    """A repo folder as a chip (mono name); dashed = a slot that is no longer there."""
    if dashed:
        return dashed_chip(name, color, mono_font=True)
    return chip(name, color, size=20, font=MONO)


def chunk_counter(value: int, color=OWN) -> VGroup:
    """S06's counter: a GREY 'chunks loaded' label over a big mono number."""
    num = mono(f"{value:,}", 36, color)
    lab = label("chunks loaded", 20, S.GREY)
    return VGroup(lab, num).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)


def tracker_t23_fixed(step: int) -> ReadmeTracker:
    """tracker_t23(step) with its 'README @ branch 2025 › …' head put back above the dots (as S12's
    tracker_p_fixed): common.tracker() re-arranges a 'README @ ref' head with VGroup.arrange(), which
    re-centres it mid-frame (y 0.16); the head goes back to a plain tracker's offset over the dots."""
    tr = tracker_t23(step)
    ref = tracker_b(1)
    off = ref.head.get_y() - ref.dots.get_y()
    tr.head.shift(UP * (tr.dots.get_y() + off - tr.head.get_y()))
    place_tracker(tr)
    assert abs((tr.head.get_y() - tr.dots.get_y()) - off) < 1e-6 and tr.get_top()[1] <= TRACK_TOP + 1e-6
    assert tr.get_bottom()[1] > TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


class Branch2025(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 9, len(SAY)

        # ========================================================== 0. two branches, one with the simple frontend
        names = ["api-service", "frontend-react", "frontend-simple", "vector-db"]
        y_main, y_25 = 2.3, 0.75

        def branch_head(name, sha, y):
            b = chip(name, S.GREY, size=24, font=MONO)
            s = mono(sha, 20, S.GREY)
            g = VGroup(b, s).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            return g.move_to([-6.45 + g.width / 2, y, 0])

        h_main = branch_head("main", "447b5c3", y_main)
        h_25 = branch_head("2025", "14f2a14", y_25)
        widths = [folder_chip(n).width for n in names]
        gap = (SAFE_X - 0.1 - (h_25.get_right()[0] + 0.3) - sum(widths)) / 3
        assert gap > 0.15, gap
        x0, cols_x = h_25.get_right()[0] + 0.3, []
        for w in widths:
            cols_x.append(x0 + w / 2)
            x0 += w + gap
        f_main = VGroup(*[folder_chip(n).move_to([x, y_main, 0]) for n, x in zip(names, cols_x) if n != "frontend-simple"])
        ghost = folder_chip("frontend-simple", S.GREY, dashed=True).move_to([cols_x[2], y_main, 0])
        ghost_x = cross_glyph(0.3).move_to(ghost)
        f_25 = [folder_chip(n, TURN if n == "frontend-simple" else S.GREY).move_to([x, y_25, 0])
                for n, x in zip(names, cols_x)]
        assert f_25[0].get_left()[0] > h_25.get_right()[0] + 0.15, (f_25[0].get_left(), h_25.get_right())
        assert f_25[-1].get_right()[0] < SAFE_X - 0.05, f_25[-1].get_right()
        for a, b in zip(f_25, f_25[1:]):
            assert a.get_right()[0] < b.get_left()[0] - 0.1, (a.get_right(), b.get_left())
        stem = Line(h_main[1].get_bottom() + DOWN * 0.08, h_25[0].get_top() + UP * 0.08, color=S.GREY, stroke_width=3)
        stem.shift(RIGHT * (h_main[0].get_center()[0] - stem.get_center()[0]))
        last_api = grey_chip("last year's API").next_to(f_25[0], DOWN, buff=0.22).align_to(f_25[0], LEFT)
        serves = CurvedArrow(f_25[0].get_corner(DR) + LEFT * 0.2 + DOWN * 0.02, f_25[2].get_bottom() + DOWN * 0.02,
                             angle=PI / 3, color=ROUTE, stroke_width=3, tip_length=0.18)
        serves_t = label("serves it", 20, ROUTE).move_to([cols_x[1] + 0.9, serves.get_bottom()[1] - 0.22, 0])

        disk_rows = VGroup(
            label("branch 2025 builds its own API image · budget about 10 GB more", 20, INK),
            label("short on space? remove main's images first:", 20, S.GREY),
            mono(f"docker image rm {MAIN_IMAGES[0]} \\", 20, INK),
            mono(f"  {MAIN_IMAGES[1]} {MAIN_IMAGES[2]} \\", 20, INK),
            mono(f"  {MAIN_IMAGES[3]}", 20, INK),
        )
        dcard = card(list(disk_rows), color=COST, head="disk", buff=0.12)
        dcard.move_to([0, -2.15, 0])
        cmd_rows = VGroup(*dcard.body[2:])
        assert dcard.get_bottom()[1] > -SAFE_Y + 0.05 and dcard.get_top()[1] < serves_t.get_bottom()[1] - 0.1, \
            (dcard.get_top(), serves_t.get_bottom())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(h_main, shift=RIGHT * 0.2), LaggedStart(*[FadeIn(f) for f in f_main], lag_ratio=0.2),
                      run_time=0.9)
            vo.wait_until("Main dropped it")
            self.play(FadeIn(ghost), run_time=0.4)
            self.play(Create(ghost_x), ghost.animate.set_opacity(0.5), run_time=0.5)
            vo.wait_until("branch 2025 keeps it")
            self.play(Create(stem), FadeIn(h_25, shift=DOWN * 0.2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.15) for f in f_25], lag_ratio=0.15), run_time=0.8)
            self.play(Indicate(f_25[2], color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("with last year's API")
            self.play(Indicate(f_25[0], color=TURN, scale_factor=1.1), FadeIn(last_api, shift=UP * 0.1), run_time=0.6)
            self.play(Create(serves), FadeIn(serves_t), run_time=0.7)
            vo.wait_until("Branch 2025 builds its own big images")
            self.play(FadeIn(dcard, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("if your disk is tight")
            self.play(cmd_rows.animate.set_color(COST), run_time=0.4)
            vo.wait_until("remove main's images first")
            self.play(Indicate(h_main[0], color=COST, scale_factor=1.15), Indicate(cmd_rows, color=COST, scale_factor=1.02),
                      run_time=0.8)

        # ========================================================== 1. git switch refuses; stash, then switch
        t = term(P_V2, rows=13, title=T_LAPTOP, size=20)
        assert t.box.get_top()[1] < SAFE_Y - 0.1, t.box.get_top()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(h_main, f_main, ghost, ghost_x, stem, h_25, *f_25, last_api, serves, serves_t,
                                     dcard)), run_time=0.5)
            self.play(FadeIn(t), run_time=0.4)
            ln1 = type_capture(self, t, C01, type_time=0.5)[0]
            mark_extra(self, t, ln1)
            o1 = out(self, t, [(C01.line(2), ERR)] + [(s, INK) for s in C01.at((3, 6))] +
                     [C01.line(7), (C01.line(8), ERR)], wrap=True, run_time=0.6)
            vo.wait_until("your edits to four files")
            self.play(*paint(o1, FILES, TURN), run_time=0.5)
            mine = row_tag("your edits", TURN)
            pin(self, row_with(o1, FILES[0]), beside(mine, row_with(o1, FILES[0]), buff=0.5))
            self.add(t)
            vo.wait_until("An extra stash")
            ln2 = type_capture(self, t, C01B, type_time=0.5)[0]
            mark_extra(self, t, ln2)
            o2 = out(self, t, [STASH, C01B.line(3), (C01B.line(4), OWN)], run_time=0.5)
            self.play(Indicate(o2[-1], color=OWN, scale_factor=1.04), run_time=0.6)
            self.add(t)
            self.wait(1.2)                       # the switch is read before the terminal clears

        # ========================================================== 2. last year's commit; the second key name
        p2 = code(DS_2025, 10, 10, font_size=20, shown="2025 · src/vector-db/docker-shell.sh")
        with self.voiceover(SAY[2]) as vo:
            clear_lines(self, t)
            resize(self, t, 7, run_time=0.5)
            p2.move_to([0, 1.25, 0])
            assert p2.get_bottom()[1] > t.box.get_top()[1] + 0.3 and p2.get_top()[1] < 2.6, (p2.get_bottom(), t.box.get_top())
            ln = type_capture(self, t, C02, type_time=0.5)[-1]
            mark_extra(self, t, ln)
            o3 = out(self, t, C02.at((2, 6)), wrap=True, run_time=0.5)
            self.play(substring(row_with(o3, "14f2a14"), "14f2a14").animate.set_color(TURN),
                      substring(row_with(o3, "frontend-simple"), "frontend-simple").animate.set_color(OWN), run_time=0.5)
            self.play(Indicate(substring(row_with(o3, "frontend-simple"), "frontend-simple"), color=OWN,
                               scale_factor=1.1), run_time=0.5)
            self.add(t)
            vo.wait_until("Its vector db script")
            self.play(FadeIn(p2, shift=DOWN * 0.15), run_time=0.5)
            key = code_span(p2.code, 0, "llm-service-account.json")
            self.play(key.animate.set_color(TURN), run_time=0.4)
            self.add(p2)
            err = erratum_tag("erratum · the 2025 vector-db script reads this name")
            err.next_to(p2, UP, buff=0.18).align_to(p2, RIGHT)
            assert err.get_top()[1] < SAFE_Y - 0.05, err.get_top()
            self.play(FadeIn(err, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("so copy your key")
            ln = type_capture(self, t, C03, type_time=0.6)[-1]
            mark_extra(self, t, ln)
            o4 = out(self, t, C03.at(2, 3), run_time=0.4)
            self.play(o4[0].animate.set_color(TURN), Indicate(key, color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(t, p2)
            vo.wait_until("and set your project ID again")
            ln = type_capture(self, t, C04, type_time=0.7)[-1]
            mark_extra(self, t, ln)
            o5 = out(self, t, C04.at((2, 4)), run_time=0.4)
            self.play(Indicate(o5[-1], color=INK, scale_factor=1.04), run_time=0.6)
            self.wait(1.2)

        # ========================================================== 3. Tutorial (23) vector DB: the same load
        trk = tracker_t23_fixed(1)
        above = grey_chip("from the folder above cheese-app-v2")
        # Compose v2 fallback: edit the script's last line (a bare `docker compose run` in the shell
        # would miss GCP_PROJECT / GOOGLE_APPLICATION_CREDENTIALS, which only docker-shell.sh exports)
        compose = card([label("docker-compose: command not found? In docker-shell.sh, make the last line", 20, INK),
                        mono("docker compose run --rm --service-ports $IMAGE_NAME", 20, INK)], buff=0.14)
        compose.move_to([0, 1.95, 0])
        cnt = chunk_counter(CHUNKS)
        main_data = grey_chip("your folder still holds main's data · output may differ slightly")
        with self.voiceover(SAY[3]) as vo:
            clear_bar(self, t, FadeOut(p2), FadeOut(err), FadeIn(trk, shift=RIGHT * 0.3))
            clear_lines(self, t)
            resize(self, t, 11, run_time=0.4)
            under_term(t, above, buff=0.14).align_to(t.box, LEFT)
            compose.move_to([0, (t.box.get_top()[1] + PIC_TOP) / 2, 0])
            assert compose.get_bottom()[1] > t.box.get_top()[1] + 0.1 and compose.get_top()[1] < PIC_TOP, \
                (compose.get_bottom(), t.box.get_top())
            assert compose.get_right()[0] < SAFE_X - 0.05, compose.get_right()
            t.set_prompt(P_LAPTOP)
            bare_prompt(self, t)
            self.play(FadeIn(above, shift=DOWN * 0.1), run_time=0.3)
            type_capture(self, t, C05, type_time=0.5)
            cd_prompt(self, t, P_V2_VDB)
            # the 'above' chip stays while the narration names the folder (no `cd ..` capture exists)
            vo.wait_until("from the folder above")
            self.play(Indicate(above, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("as the 2025 README spells them")
            self.play(track(trk, 2), FadeOut(above), run_time=0.4)
            type_capture(self, t, C06, type_time=0.4)
            self.play(FadeIn(compose, shift=DOWN * 0.1), run_time=0.4)
            out(self, t, [cut(C06.line(3), "FINISHED"), "…", cut(C06.line(22), "Pulled"),
                          (cut(C06.line(23), "Created"), CONTAINER)] + C06.at((26, 30)), run_time=0.7)
            self.play(track(trk, 3), run_time=0.4)
            type_at(self, t, C06, 33, type_time=0.7)
            self.play(FadeOut(compose), run_time=0.3)
            o6 = out(self, t, [C06.line(41), "…", (C06.line(197), OWN)], wrap=True, run_time=0.5)
            cnt.move_to([0, (t.box.get_top()[1] + PIC_TOP) / 2, 0]).shift(RIGHT * (6.45 - cnt.get_right()[0]))
            main_data.move_to([-6.45 + main_data.width / 2, cnt[1].get_center()[1], 0])
            assert main_data.get_right()[0] < cnt.get_left()[0] - 0.2, (main_data.get_right(), cnt.get_left())
            assert cnt.get_bottom()[1] > t.box.get_top()[1] + 0.1 and cnt.get_top()[1] < PIC_TOP, cnt.get_top()
            self.play(FadeIn(cnt, scale=1.2), run_time=0.4)
            self.play(Indicate(cnt[1], color=OWN, scale_factor=1.15), FadeIn(main_data, shift=RIGHT * 0.1), run_time=0.7)
            self.add(t)
            del o6
            vo.wait_until("Its Chroma image is tagged latest")
            self.play(FadeOut(cnt), FadeOut(main_data), run_time=0.3)
            type_at(self, t, C06, 198, type_time=0.3)
            out(self, t, [C06.line(199)], run_time=0.3)
            t.set_prompt(P_V2_VDB)
            ln = type_capture(self, t, C07, type_time=0.8)[-1]
            mark_extra(self, t, ln)
            o7 = out(self, t, C07.at(2, 3), wrap=True, run_time=0.4)
            latest = row_with(o7, "chromadb/chroma:latest")
            self.play(substring(latest, "chromadb/chroma:latest").animate.set_color(TURN), run_time=0.4)
            bar_tag(self, t, time_row())
            self.add(t)
            vo.wait_until("Leave with exit")
            ex = row_with(t.lines, "$ exit") if any("$ exit" in r.text for r in t.lines) else None
            anims = [substring(latest, C_VDB).animate.set_color(OWN),
                     substring(row_with(o7, "Up 32 seconds"), "Up 32 seconds").animate.set_color(OWN)]
            self.play(*anims, run_time=0.5)
            if ex is not None:
                self.play(Indicate(substring(ex, "exit"), color=TURN, scale_factor=1.15), run_time=0.5)
            self.play(Indicate(substring(row_with(o7, "Up 32 seconds"), "Up 32 seconds"), color=OWN, scale_factor=1.1),
                      run_time=0.6)
            self.add(t)

        # ========================================================== 4. Tutorial (23) backend: a new terminal, uvicorn_server
        t2 = term(P_LAPTOP, rows=13, title=T_NEW, size=20)
        with self.voiceover(SAY[4]) as vo:
            clear_bar(self, t)
            self.play(FadeOut(t), track(trk, 4), run_time=0.5)
            self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.4)
            bare_prompt(self, t2)
            both = grey_chip("the folder that holds both clones")
            under_term(t2, both, buff=0.14).align_to(t2.box, LEFT)
            assert both.get_top()[1] < TRACK_BOTTOM - 0.05, both.get_top()
            vo.wait_until("from the folder that holds both clones")
            self.play(FadeIn(both, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(substring(t2.lines[-1], "~"), color=TURN, scale_factor=1.3) if len(t2.lines) else
                      Indicate(both.text, color=S.GREY), run_time=0.6)
            self.add(t2)
            vo.wait_until("change into the API folder")
            type_capture(self, t2, C10, type_time=0.5)
            cd_prompt(self, t2, P_V2_API)
            self.play(FadeOut(both), run_time=0.3)
            vo.wait_until("sh docker-shell.sh")
            self.play(track(trk, 5), run_time=0.4)
            type_capture(self, t2, C11, type_time=0.4)
            out(self, t2, [cut(C11.line(3), "FINISHED"), "…", (cut(C11.line(20), C_API), CONTAINER)] +
                C11.at((21, 25), (28, 30)), run_time=0.7)
            vo.wait_until("and uvicorn server")
            self.play(track(trk, 6), run_time=0.4)
            type_at(self, t2, C11, 32, type_time=0.4)
            o11 = out(self, t2, C11.at((34, 35), "…", (49, 50), "…", 67, 72, 74), wrap=True, run_time=0.8)
            vo.wait_until("Pause and start it")
            turn = bar_tag(self, t2, turn_row())
            flash_tag(self, turn, TURN)
            self.add(t2)

        # ========================================================== 5. two differences: WatchFiles; the model before startup
        r35 = row_with(o11, "using WatchFiles")
        r49 = row_with(o11, "Loading CNN Model")
        r67 = row_with(o11, "Total params")
        i49 = list(o11).index(r49)
        r50 = list(o11)[i49 + 1:list(o11).index(r67) - 1]          # file line 50 (wrapped), before the '…' row
        assert r50 and r50[0].text.startswith("best_model_path") and all(r.text != "…" for r in r50), [r.text for r in r50]
        r74 = row_with(o11, "Application startup complete")
        stat = row_tag("main: StatReload", S.GREY)
        rcard = readme_card((82, 86), R_8286, size=20, name="2025 README.md")
        rtag = tag("read along · same idea as main", S.GREY)
        lamps = lamp_pair(("dashed", "dashed"))
        noprobe = grey_chip("no probes yet")
        docs = card([label("2025 docs:", 20, S.GREY), VGroup(mono("localhost:9000/docs", 20, ROUTE),
                                                             label("(no /api)", 20, S.GREY)).arrange(RIGHT, buff=0.3)],
                    size=20, buff=0.08)
        with self.voiceover(SAY[5]) as vo:
            clear_bar(self, t2)
            vo.wait_until("the reloader is WatchFiles")
            self.play(substring(r35, "WatchFiles").animate.set_color(TURN), run_time=0.4)
            pin(self, r35, beside(stat, r35, buff=0.45))
            self.add(t2)
            vo.wait_until("and the model loads")
            self.play(*[r.animate.set_color(TURN) for r in [r49, *r50, r67]], run_time=0.6)
            vo.wait_until("before application startup complete")
            self.play(Indicate(r74, color=INK, scale_factor=1.05), run_time=0.6)
            self.add(t2)
            vo.wait_until("so start-up waits")
            resize(self, t2, 3, keep=[r67, row_with(o11, "Started server process"), r74], run_time=0.5)
            top = t2.box.get_top()[1]
            rcard.move_to([-6.45 + rcard.width / 2, 0, 0])
            rcard.shift(UP * ((top + 0.25 + rcard.height / 2) - rcard.get_center()[1]))
            rtag.next_to(rcard, UP, buff=0.12).align_to(rcard, RIGHT)
            assert rtag.get_top()[1] < PIC_TOP, rtag.get_top()
            assert rcard.get_top()[1] + 0.25 < TRACK_BOTTOM, (rcard.get_top(), TRACK_BOTTOM)
            right_x = (rcard.get_right()[0] + SAFE_X) / 2
            col = VGroup(lamps, noprobe, docs)
            lamps.move_to([right_x, 0, 0])
            noprobe.next_to(lamps, DOWN, buff=0.15)
            docs.next_to(noprobe, DOWN, buff=0.3)
            col.shift(UP * (top + 0.2 - col.get_bottom()[1]))
            assert col.get_top()[1] < PIC_TOP, col.get_top()
            assert col.get_bottom()[1] > top + 0.1, (col.get_bottom(), top)
            assert docs.get_left()[0] > rcard.get_right()[0] + 0.15 and docs.get_right()[0] < SAFE_X - 0.05, \
                (docs.get_left(), rcard.get_right(), docs.get_right())
            self.play(FadeIn(lamps, scale=0.9), FadeIn(noprobe, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("with no readiness probe")
            self.play(Indicate(noprobe.text, color=S.GREY, scale_factor=1.1), run_time=0.5)
            self.play(FadeIn(rcard, shift=RIGHT * 0.2), FadeIn(rtag), run_time=0.5)
            self.play(FadeIn(docs, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(docs.body[1][0], color=ROUTE, scale_factor=1.08), run_time=0.6)
            self.wait(1.2)

        # ========================================================== 6. verify 9000; the README steps already done
        tab = term(P_V2_API, rows=9, title=T_TAB, size=20)
        cA = readme_card((96, 98), R_9698, size=20, name="2025 README.md")
        cB = readme_card((116, 118), R_116, size=20, name="2025 README.md")
        err6 = erratum_tag("erratum · already in the code")
        dont = grey_chip("except RAG and agent · don't paste again")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rcard, rtag, lamps, noprobe, docs, t2)), track(trk, 7), run_time=0.5)
            self.play(FadeIn(tab, shift=UP * 0.2), run_time=0.4)
            top = tab.box.get_top()[1]
            for c in (cA, cB):
                c.move_to([-6.45 + c.width / 2, (top + PIC_TOP) / 2 - 0.05, 0])
                assert c.get_bottom()[1] > top + 0.1 and c.get_top()[1] < PIC_TOP + 0.05, (c.get_bottom(), c.get_top(), top)
            err6.next_to(cA, RIGHT, buff=0.45).align_to(cA, UP)
            dont.next_to(err6, DOWN, buff=0.2).align_to(err6, LEFT)
            assert dont.get_right()[0] < SAFE_X - 0.05 and err6.get_right()[0] < SAFE_X - 0.05, (dont.get_right(), err6.get_right())
            ln = type_capture(self, tab, C12, type_time=0.5)[-1]
            mark_extra(self, tab, ln)
            o12 = out(self, tab, C12.at(2, 4) + [JSON], run_time=0.4)
            self.play(o12[-1].animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(o12[-1], color=OWN, scale_factor=1.06), run_time=0.6)
            self.add(tab)
            vo.wait_until("A small note")
            self.play(FadeIn(cA, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(err6, shift=DOWN * 0.1), run_time=0.3)
            clear_bar(self, tab)
            clear_lines(self, tab, run_time=0.3)
            ln = type_capture(self, tab, C13, type_time=0.7)[-1]
            mark_extra(self, tab, ln)
            o13 = out(self, tab, C13.at((2, 5), 7), run_time=0.4)
            self.play(o13[0].animate.set_color(TURN), run_time=0.3)
            self.add(tab)
            vo.wait_until("and the routers")
            clear_bar(self, tab)
            clear_lines(self, tab, run_time=0.3)
            err6b = err6.copy().next_to(cB, RIGHT, buff=0.45).align_to(cB, UP)
            dont.next_to(err6b, DOWN, buff=0.2).align_to(err6b, LEFT)
            self.play(FadeTransform(cA, cB), Transform(err6, err6b), run_time=0.6)
            self.bring_to_front(err6)
            # one long line whose quoted python is longer than a row: typed as c14_rows() (see C14_PIECES)
            p14 = tab.prompt + " "
            rows14 = c14_rows(p14)
            assert all(len(r) <= tab.max_chars for r in rows14), [len(r) for r in rows14]

            def fold14(text, first_prefix=0):
                assert text == p14 + C14.cmd_lines[0], text
                return rows14
            tab.fold = fold14
            try:
                ln = type_cmd(self, tab, C14.cmd_lines[0], type_time=0.9, soft=False)
            finally:
                del tab.fold
            assert [r.text for r in ln.rows] == rows14, [r.text for r in ln.rows]
            mark_extra(self, tab, ln)
            self.wait(0.8)      # the whole command holds before its output scrolls the first rows up
            o14 = out(self, tab, C14.at((3, 9)), run_time=0.5)
            self.play(*[r.animate.set_color(TURN) for r in o14[1:5]], run_time=0.4)
            self.add(tab)
            vo.wait_until("except RAG and agent")
            self.play(*[r.animate.set_color(S.GREY) for r in o14[5:7]], run_time=0.4)
            bar_tag(self, tab, row_tag("still commented out"))
            self.add(tab)
            vo.wait_until("Don't paste them again")
            self.play(FadeIn(dont, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, dont, S.GREY)
            flash_tag(self, err6, S.GREY)

        # ========================================================== 7. last year's Gemini model is retired
        y7 = 1.0
        api = cbox([C_API], box_w=4.0, box_h=0.9).move_to([-4.45, y7, 0])
        api_note = label("branch 2025", 20, S.GREY).next_to(api, DOWN, buff=0.15)
        vx = cloud_shape("Vertex AI · Gemini", CLOUD, cloud_w=3.3).move_to([5.0, y7, 0])
        vx.shift(RIGHT * (SAFE_X - 0.1 - vx.get_right()[0]))
        call = route(api.get_right() + RIGHT * 0.1, vx.get_left() + RIGHT * 0.15)
        m25 = VGroup(label("2025's model:", 20, S.GREY), mono("gemini-2.0-flash-001 · us-central1", 20, INK)) \
            .arrange(DOWN, buff=0.1).next_to(call, UP, buff=0.35)
        assert m25.get_top()[1] < PIC_TOP and m25[1].width < call.get_length() - 0.2, (m25.get_top(), m25[1].width)
        x25 = strike(m25[1])
        err7 = erratum_tag("erratum · with a key, chat fails until the model and region are updated")
        err7.move_to([0, -2.4, 0])
        main_lb = chip("main", S.GREY, size=24, font=MONO)
        m_now = VGroup(main_lb, ok_chip("gemini-3.8-flash · global", mono_font=True)).arrange(RIGHT, buff=0.3)
        m_now.move_to([-6.45 + m_now.width / 2, -1.2, 0])
        m_to = m_now.copy()                     # on the arrow: the chip under it, the 'main' label under the chip
        m_to[1].next_to(call, DOWN, buff=0.2)
        m_to[0].next_to(m_to[1], DOWN, buff=0.12)
        assert m_to[1].get_right()[0] < vx.get_left()[0] - 0.1 and m_to[1].get_left()[0] > api.get_right()[0] + 0.1, \
            (m_to[1].get_left(), m_to[1].get_right(), api.get_right(), vx.get_left())
        assert m_to.get_bottom()[1] > m_now.get_top()[1] + 0.1 and err7.get_top()[1] < m_now.get_bottom()[1] - 0.2
        assert err7.get_right()[0] < SAFE_X and vx.get_right()[0] < SAFE_X, (err7.get_right(), vx.get_right())
        with self.voiceover(SAY[7]) as vo:
            clear_bar(self, tab)
            self.play(FadeOut(VGroup(tab, cB, err6, dont)), run_time=0.5)
            self.play(FadeIn(api), FadeIn(api_note), FadeIn(vx), run_time=0.5)
            self.play(GrowArrow(call), FadeIn(m25, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("is retired")
            self.play(Create(x25), m25[1].animate.set_color(ERR), run_time=0.5)
            vo.wait_until("even with a key")
            self.play(FadeIn(err7, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, err7, S.GREY)
            vo.wait_until("main uses a current one")
            self.play(FadeIn(m_now, shift=RIGHT * 0.2), run_time=0.4)
            self.play(Transform(m_now, m_to), run_time=0.8)
            self.play(Indicate(m_now[1].text, color=OWN, scale_factor=1.1), run_time=0.5)
            self.wait(1.0)

        # ========================================================== 8. what matters next: the CORS middleware
        p8 = code(SVC_2025, 14, 21, font_size=22, shown="2025 · src/api-service/api/service.py")
        p8.move_to([-2.2, 0.0, 0])
        slip = permission_slip()
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(api, api_note, vx, call, m25, x25, err7, m_now)), run_time=0.5)
            assert p8.get_top()[1] < PIC_TOP and p8.get_left()[0] > -SAFE_X, p8.get_corner(UL)
            self.play(FadeIn(p8, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("CORS middleware")
            bars = [line_bar(p8.code, k, TURN) for k in (1, 2)]
            self.play(*[FadeIn(b) for b in bars], code_span(p8.code, 1, "add_middleware").animate.set_color(TURN),
                      code_span(p8.code, 2, "CORSMiddleware").animate.set_color(TURN), run_time=0.5)
            self.add(p8, *bars)
            vo.wait_until("that allows every origin")
            star = code_span(p8.code, 4, 'allow_origins=["*"]')
            b4 = line_bar(p8.code, 4, TURN)
            self.play(FadeIn(b4), star.animate.set_color(TURN), run_time=0.4)
            self.add(p8, *bars, b4)
            vo.wait_until("the permission slip")
            slip.move_to(star)
            slip.set_opacity(0)
            target = permission_slip().move_to([p8.get_right()[0] + 0.3 + slip.width / 2, star.get_center()[1] + 0.9, 0])
            if target.get_right()[0] > SAFE_X - 0.05:
                target.shift(LEFT * (target.get_right()[0] - SAFE_X + 0.05))
            self.add(slip)
            self.play(Transform(slip, target), run_time=0.9)
            self.play(Indicate(slip.text, color=ROUTE, scale_factor=1.06), run_time=0.6)
            self.wait(1.5)

        self.play(FadeOut(VGroup(p8, *bars, b4, slip)), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
