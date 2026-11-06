"""S05 · The vector DB and its loader (AC215 L20). TRACKER [M] 9 (beats 0-1), 9 · extra (2),
10 (3-7), 10 · extra (8). Lecture: 20 · 7–8 (beat 0 only: slide 8's stage '3 Deploy containers').

Beats (script.md "## S05", one voiceover block each):
0. TRACKER [M] 9. lecture_ref(20, "7–8"). Slide 8's four stage chips, '1 Push' and '2 Setup VM'
   GREEN, '3 Deploy containers' YELLOW. Full terminal `cheese-app-vm`: `sudo docker pull
   chromadb/chroma:latest` -> TERM(vm/20: 2, …, 26–27); `sudo docker stop cheese-app-vector-db ||
   true` -> TERM(vm/21: 2) ORANGE; `sudo docker rm cheese-app-vector-db || true` -> TERM(vm/22: 2)
   ORANGE. 'No such container' pulses ORANGE; both typed `|| true` turn GREEN; a GREEN row tag
   'safe to run again'.
1. The README's `sudo docker run -d \\` block (vm/23: 1–9) -> TERM(vm/23: 10) GREY (the id, never
   read). Flags glow one per phrase: `-d` YELLOW, `--network cheese-app-network` GREEN, `-p
   8000:8000` PINK, `--restart always` YELLOW, `-v …:/chroma/chroma` GREY. On "Its name goes into
   the phone book" the terminal shrinks to a 3-row strip and V2 `NamePhoneBook` (cable + book, as S04
   left it) appears above it: the TEAL `cheese-app-vector-db` box plugs into the cable, the PINK door
   '8000' opens on the VM's wall and the name is written in the book.
2. TRACKER [M] 9 · extra. The strip types vm/24's line 1 (extra, folds) -> TERM(vm/24: 3 wrap, 4, 5):
   `0.0.0.0:8000->8000/tcp` PINK (V2's door 8000 flashes), the heartbeat (the vector-DB box
   flashes), `"1.0.0"` with 'at the time of recording'.
3. TRACKER [M] 10. V2 leaves, the terminal grows back to full size and a small GREEN card 'names on
   this network · cheese-app-vector-db' (V2's book, top right) stands in for the phone book. `sudo
   docker pull dlops/cheese-app-vector-db-cli` -> TERM(vm/26: 2, …, 45–46 wrap); the README's `sudo
   docker run --rm \\` block (vm/27: 1–9). `CHROMADB_HOST=cheese-app-vector-db` PINK with a row tag
   'a name, not an address' while the card's entry glows; `GCP_PROJECT=ac215-project` with the GREY
   default row tag.
4. The terminal shrinks to a strip and V2 returns (the card goes). TERM(vm/27: 13, 18–20, 24, 25
   wrap, …, 37, …, 169 wrap, …, 180 wrap) scrolls past; '11' YELLOW. The dashed TEAL loader plugs
   in, knocks on 'cheese-app-vector-db:8000' and pours dots into the vector DB while a YELLOW counter
   left of V2 climbs with every 'Finished inserting' line (BOOK_CHUNKS, vm/27:37 … 180) to 14,356.
   A GREY row tag 'precomputed embeddings · key not used' beside the last line.
5. The loader leaves V2 (--rm): its box fades, its book line is struck GREY. YELLOW '▶ your turn'.
6. The counter and the strip go; V2 moves to the middle: the dots fade from the vector-DB box, a
   YELLOW '?' sits over it, a dashed GREY outline marks the empty spot where the loader stood.
   PONDER(8 s).
7. The '?' lifts: the dots are back inside the vector-DB box; a YELLOW arrow 'inside the container'
   points at them; the box flashes on "which keeps running"; a GREY chip 'remove the container →
   gone · the loader refills it'.
8. TRACKER [M] 10 · extra. V2 leaves; a fresh full terminal types vm/25's line 1 (extra) ->
   TERM(vm/25: 3, 21) with `persist_path: "/data"` YELLOW; then vm/28's line 1 (extra, folds) ->
   TERM(vm/28: 8–11, …, 18–19, …, 23): RED row tag 'empty' on the README's folder, GREEN row tag
   'here' on `/data:`, `chroma.sqlite3` GREEN. The terminal shrinks to a 4-row strip; above it a GREY
   ghost of block 1's `-v ./docker-volumes/chromadb:/chroma/chroma` with an `erratum · README:95`
   tag, an arrow to the GREEN fix chip `-v ./docker-volumes/chromadb:/data`, and a GREY line 'then
   rerun: stop · rm · run · loader'. Fade; empty frame.

Deviations from SHOW:
- Beats 1-4: a full-width terminal and V2 cannot share the frame (V2 needs the space above a 3-row
  strip; text never shrinks), so V2 enters at the end of beat 1 over the strip, leaves for the full
  terminal of beat 3 (a small GREEN 'names on this network' card stands in for its phone book, and its
  entry glows) and returns in beat 4.
- Beat 2: the 3-row strip cannot hold all of vm/24's rows at once, so they scroll past in reading order
  (port, heartbeat, version), each highlighted as it is named.
- Beat 4: the strip scrolls; the counter also climbs through the 'Finished inserting' lines hidden in
  the '…' gaps (vm/27:50 … 168), and a '…' marks every gap. The narration's "precomputed embeddings,
  placeholder key" is a GREY row tag beside the last line.
- Beat 5: by then the typed `docker run --rm` line has scrolled out of the strip, so '▶ your turn'
  sits on the strip's title bar.
- Beat 6: the strip fades out as well (V2 alone, moved to the middle); the PONDER card sits over V2.
- Beat 8: '…' lines mark the gaps 12–17 and 20–22 of vm/28; the erratum ghost, the fix and the rerun
  note sit above a 4-row strip (the terminal shrinks after the listing) rather than on the 10-row
  terminal, which leaves no room for them.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources (checked)
V20, V21, V22, V23 = capture("vm/20"), capture("vm/21"), capture("vm/22"), capture("vm/23")
V24, V25, V26, V27, V28 = capture("vm/24"), capture("vm/25"), capture("vm/26"), capture("vm/27"), capture("vm/28")

assert V20.cmd == "sudo docker pull chromadb/chroma:latest", V20.cmd
assert V20.line(2).startswith("latest: Pulling") and V20.line(27) == "docker.io/chromadb/chroma:latest"
assert V20.line(26).startswith("Status: Downloaded newer image")
assert V21.cmd == "sudo docker stop cheese-app-vector-db || true" and V21.exit == 0
assert V22.cmd == "sudo docker rm cheese-app-vector-db || true" and V22.exit == 0
for c in (V21, V22):
    assert c.line(2) == "Error response from daemon: No such container: cheese-app-vector-db", c.line(2)
assert V23.cmd_lines == [s.rstrip() for s in readme_rows(89, 97)], (V23.cmd_lines, readme_rows(89, 97))
assert re.fullmatch(r"[0-9a-f]{64}", V23.line(10)), V23.line(10)
assert V24.cmd.startswith("sudo docker ps; curl -s http://localhost:8000/api/v2/heartbeat")
assert "0.0.0.0:8000->8000/tcp" in V24.line(3) and V24.line(3).endswith("cheese-app-vector-db")
assert V24.line(4).startswith('{"nanosecond heartbeat":') and V24.line(5) == '"1.0.0"'
assert V25.cmd == "sudo docker logs cheese-app-vector-db 2>&1 | head -30"
assert V25.line(3) == 'persist_path: "/data"' and V25.line(21) == "Saving data to: /data"
assert V26.cmd == "sudo docker pull dlops/cheese-app-vector-db-cli"
assert V26.line(2) == "Using default tag: latest" and V26.line(45).startswith("Digest: sha256:")
assert V26.line(46).startswith("Status: Downloaded newer image")
assert V27.cmd_lines == [s.rstrip() for s in readme_rows(104, 112)], (V27.cmd_lines, readme_rows(104, 112))
assert V27.line(13) == "Python version: Python 3.12.12"
assert V27.at((18, 20)) == ["download()", "load()", "Creating collection: recursive-split-collection"]
assert V27.line(24) == "Number of files to process: 11"
assert V27.line(25).startswith("Processing file: outputs/embeddings-recursive-split-")
assert V27.line(169).startswith("Processing file: outputs/embeddings-") and "Tolminc" in V27.line(169)
for n, k in zip(BOOK_LINES, BOOK_CHUNKS):
    assert V27.line(n) == f"Finished inserting {k} items into collection 'recursive-split-collection'", (n, k)
assert V28.cmd.startswith("ls -la docker-volumes/ docker-volumes/chromadb; sudo docker exec cheese-app-vector-db")
assert V28.line(8) == "docker-volumes/chromadb:" and V28.line(9) == "total 8"
assert V28.line(18) == "/data:" and V28.line(23).endswith("chroma.sqlite3")
GHOST = "-v ./docker-volumes/chromadb:/chroma/chroma"
FIX = "-v ./docker-volumes/chromadb:/data"
assert readme(95).strip() == GHOST + " \\", readme(95)

SUMS = list(np.cumsum(BOOK_CHUNKS))
assert SUMS[-1] == CHUNKS == 14356

# V2's place over a 3-row strip: up as in S04, and right, so the counter fits on its left
NB_SHIFT = np.array([0.6, 0.36, 0])


def stage_row() -> VGroup:
    """Slide 8's four stages (as S04 draws them), '3 Deploy containers' current."""
    st = VGroup(*[chip(s, S.GREY, size=20) for s in STAGES_MANUAL]).arrange(RIGHT, buff=0.25)
    st.move_to([0, 2.3, 0])
    return st


def mini_book() -> VGroup:
    """V2's phone book in small: a GREEN card with the one name written so far. .entry"""
    hd = label("names on this network", 20, S.GREY)
    en = label(C_VDB, 20, INK)
    body = VGroup(hd, en).arrange(DOWN, buff=0.16)
    fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.36, corner_radius=0.12,
                          stroke_color=OWN, stroke_width=2.5).set_fill(tint(OWN, 0.08), 1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.entry = en
    return g


def counter_text(v: int) -> Text:
    return steady(f"{v:,}", 36, TURN)


def row_with(t: Terminal, sub: str):
    """The terminal row (on screen) that holds `sub`."""
    return t.find(sub)


class VectorDb(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 9, len(SAY)

        # ========================================================== 0. stage 3: pull, stop, rm
        trk = tracker_m(9)
        ref = lref("7–8")
        stages = stage_row()
        assert stages.get_top()[1] < TRACK_BOTTOM - 0.1 and stages.get_left()[0] > -6.5
        t = vm_term(rows=10)
        assert t.box.get_top()[1] < stages.get_bottom()[1] - 0.15, (t.box.get_top(), stages.get_bottom())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in stages], lag_ratio=0.15), run_time=0.6)
            self.play(stages[0].box.animate.set_stroke(OWN, width=3), stages[1].box.animate.set_stroke(OWN, width=3),
                      stages[2].box.animate.set_stroke(TURN, width=4), run_time=0.4)
            self.play(Indicate(stages[2].text, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(stages)
            vo.wait_until("Pull the Chroma image")
            self.play(FadeIn(t, shift=UP * 0.3), run_time=0.4)
            type_capture(self, t, V20, type_time=0.7)
            out(self, t, V20.at(2, "…", (26, 27)), run_time=0.5)
            vo.wait_until("then stop and remove")
            stop = type_capture(self, t, V21, type_time=0.6)[0]
            e1 = out(self, t, [(V21.line(2), SHARED)], wrap=True, run_time=0.4)
            rm = type_capture(self, t, V22, type_time=0.6)[0]
            e2 = out(self, t, [(V22.line(2), SHARED)], wrap=True, run_time=0.4)
            vo.wait_until("The error, no such container")
            nsc = [substring(r, "No such container") for r in (e1[0], e2[0])]
            self.play(*[Indicate(g, color=SHARED, scale_factor=1.1) for g in nsc], run_time=0.7)
            self.add(t)
            vo.wait_until("or true makes the step")
            # the fold may split '|| true' over two rows (rm: '… || \' / 'true'): colour both parts
            ors = []
            for ln in (stop, rm):
                parts = [substring(r, w) for r in rows_of(ln) for w in ("||", "true")
                         if w in r.text.replace(C_VDB, "")]
                assert len(parts) == 2, [r.text for r in rows_of(ln)]
                ors.append(VGroup(*parts))
            self.play(*[g.animate.set_color(OWN) for g in ors], run_time=0.4)
            self.play(*[Indicate(g, color=OWN, scale_factor=1.25) for g in ors], run_time=0.6)
            self.add(t)
            safe = beside(row_tag("safe to run again", OWN), rm)
            pin(self, rm, safe)

        # ========================================================== 1. run the vector DB
        nb = NamePhoneBook(built=True)
        nb.shift(NB_SHIFT)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(stages, ref)), run_time=0.4)
            self.remove(stages, ref)
            run = type_capture(self, t, V23, type_time=0.2)
            idr = out(self, t, [(V23.line(10), S.GREY)], run_time=0.3)
            rr = {k: rows_of(ln)[0] for k, ln in zip(("d", "name", "net", "p", "e1", "e2", "v", "re", "img"), run)}
            assert rr["net"].text.strip() == "--network cheese-app-network \\" and rr["v"].text.strip().startswith(GHOST)
            vo.wait_until("Then run it detached")
            self.play(substring(rr["d"], "-d").animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(substring(rr["d"], "-d"), color=TURN, scale_factor=1.4), run_time=0.5)
            self.add(t)
            vo.wait_until("on cheese app network")
            g = substring(rr["net"], "--network cheese-app-network")
            self.play(g.animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(g, color=OWN, scale_factor=1.08), run_time=0.5)
            self.add(t)
            vo.wait_until("publishing port 8000")
            g = substring(rr["p"], "-p 8000:8000")
            self.play(g.animate.set_color(ROUTE), run_time=0.3)
            self.play(Indicate(g, color=ROUTE, scale_factor=1.12), run_time=0.5)
            self.add(t)
            vo.wait_until("restarting always")
            g = substring(rr["re"], "--restart always")
            self.play(g.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(g, color=TURN, scale_factor=1.1), run_time=0.5)
            self.add(t)
            vo.wait_until("with a data folder mounted")
            g = substring(rr["v"], GHOST)
            self.play(g.animate.set_color(S.GREY), run_time=0.3)
            self.play(Indicate(g, color=S.GREY, scale_factor=1.06), run_time=0.5)
            self.add(t)
            vo.wait_until("Its name goes into the phone book")
            resize(self, t, 3, run_time=0.5)
            assert nb.vm.get_bottom()[1] > t.box.get_top()[1] + 0.05, (nb.vm.get_bottom(), t.box.get_top())
            self.play(FadeIn(nb), run_time=0.5)
            nb.plug(self, "vdb", run_time=0.7)
            self.play(nb.light_entry("vdb", OWN), run_time=0.5)
            nb.heal(self)

        # ========================================================== 2. extra: ps, heartbeat, version
        with self.voiceover(SAY[2]) as vo:
            self.play(track(trk, 9, True), run_time=0.4)
            chk = type_capture(self, t, V24, type_time=0.5)[0]
            pin(self, chk, beside(extra_row(), chk))
            vo.wait_until("the port is published")
            pr = out(self, t, [V24.line(3)], wrap=True, run_time=0.4)
            prow = next(r for r in pr if "0.0.0.0:8000->8000/tcp" in r.text)
            g = substring(prow, "0.0.0.0:8000->8000/tcp")
            self.play(g.animate.set_color(ROUTE), Indicate(nb.doors["vdb"], color=ROUTE, scale_factor=1.2),
                      run_time=0.6)
            self.add(t)
            nb.heal(self)
            vo.wait_until("the heartbeat answers")
            out(self, t, V24.at(4), run_time=0.4)
            self.play(Indicate(nb.boxes["vdb"], color=CONTAINER, scale_factor=1.08), run_time=0.6)
            nb.heal(self)
            vo.wait_until("Chroma version one")
            vr = out(self, t, V24.at(5), run_time=0.4)
            pin(self, vr[0], beside(time_row(), vr[0]))
            self.play(Indicate(vr[0], color=INK, scale_factor=1.2), run_time=0.5)
            self.add(t)

        # ========================================================== 3. the loader's command
        card = mini_book()
        with self.voiceover(SAY[3]) as vo:
            self.play(track(trk, 10), run_time=0.4)
            resize(self, t, 10, extra=[FadeOut(nb)], run_time=0.6)
            self.remove(nb)
            card.move_to([6.45 - card.width / 2, 0, 0])
            card.set_y((t.box.get_top()[1] + PIC_TOP) / 2 + 0.05)
            assert card.get_bottom()[1] > t.box.get_top()[1] + 0.05 and card.get_top()[1] < 2.95, card.get_top()
            self.play(FadeIn(card, shift=LEFT * 0.2), run_time=0.4)
            type_capture(self, t, V26, type_time=0.5)
            out(self, t, V26.at(2, "…", (45, 46)), wrap=True, run_time=0.4)
            lrun = type_capture(self, t, V27, type_time=0.15)
            host = rows_of(lrun[2])[0]
            proj = rows_of(lrun[1])[0]
            assert "CHROMADB_HOST=cheese-app-vector-db" in host.text and "GCP_PROJECT=ac215-project" in proj.text
            vo.wait_until("It finds the database by name")
            g = substring(host, "CHROMADB_HOST=cheese-app-vector-db")
            self.play(g.animate.set_color(ROUTE), run_time=0.3)
            self.add(t)
            pin(self, host, beside(row_tag("a name, not an address", ROUTE), host))
            vo.wait_until("cheese app vector db, not by address")
            self.play(Indicate(card.entry, color=OWN, scale_factor=1.12),
                      Indicate(substring(host, "cheese-app-vector-db"), color=ROUTE, scale_factor=1.1), run_time=0.8)
            self.add(t)
            vo.wait_until("The project is the README's default")
            gp = substring(proj, "ac215-project")
            self.play(Indicate(gp, color=S.GREY, scale_factor=1.15), run_time=0.5)
            self.add(t)
            pin(self, proj, beside(default_row(), proj))

        # ========================================================== 4. the loader runs: 14,356 chunks
        ctr_l = label("chunks inserted", 20, S.GREY)
        ctr = counter_text(0)
        VGroup(ctr_l, ctr).arrange(DOWN, buff=0.2).move_to([-5.15, 0.55, 0])
        with self.voiceover(SAY[4]) as vo:
            resize(self, t, 3, extra=[FadeOut(card)], run_time=0.5)
            self.remove(card)
            self.play(FadeIn(nb), run_time=0.5)
            nb.heal(self)
            assert ctr_l.get_right()[0] < nb.vm.get_left()[0] - 0.2, (ctr_l.get_right(), nb.vm.get_left())
            out(self, t, V27.at(13, 18), run_time=0.4)
            nb.loader(self)
            vo.wait_until("creates the collection")
            out(self, t, V27.at(19, 20), run_time=0.4)
            vo.wait_until("and loads eleven files")
            nf = out(self, t, V27.at(24), run_time=0.3)
            self.play(substring(nf[0], "11").animate.set_color(TURN), FadeIn(ctr_l), FadeIn(ctr), run_time=0.4)
            self.play(Indicate(substring(nf[0], "11"), color=TURN, scale_factor=1.4), run_time=0.4)
            self.add(t)
            out(self, t, [V27.line(25), "…"], wrap=True, run_time=0.4, chunk=3)
            out(self, t, V27.at(37), wrap=True, run_time=0.3)
            new = counter_text(SUMS[0]).move_to(ctr)
            self.play(Transform(ctr, new), run_time=0.25)
            nb.pour(self, n=12, run_time=1.4)
            out(self, t, ["…"], run_time=0.2)
            for v in SUMS[1:10]:
                new = counter_text(v).move_to(ctr)
                self.play(Transform(ctr, new), run_time=0.16)
            vo.wait_until("14,356 chunks in all")
            out(self, t, [V27.line(169), "…", V27.line(180)], wrap=True, run_time=0.4, chunk=3)
            new = counter_text(SUMS[10]).move_to(ctr)
            self.play(Transform(ctr, new), run_time=0.3)
            self.play(Indicate(ctr, color=TURN, scale_factor=1.2), run_time=0.6)
            last = t.lines[-1]
            assert last.text == "'recursive-split-collection'", last.text
            vo.wait_until("The embeddings come precomputed")
            pre = beside(row_tag("precomputed embeddings · key not used"), last)
            pin(self, last, pre)
            vo.wait_until("so our placeholder key never mattered")
            flash_tag(self, pre, S.GREY)
            self.add(t)

        # ========================================================== 5. --rm: the loader is gone
        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("The loader ran with the remove flag")
            nb.unload(self, run_time=0.7)
            vo.wait_until("Pause and run both containers")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 6. the question
        spot = DashedVMobject(RoundedRectangle(width=1.46, height=1.0, corner_radius=0.1),
                              num_dashes=24, dashed_ratio=0.45).set_stroke(S.GREY, 2.5)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(ctr, ctr_l, yt)), run_time=0.4)
            self.remove(ctr, ctr_l, yt)
            self.play(FadeOut(t), nb.animate.shift(-NB_SHIFT), run_time=0.7)
            self.remove(t)
            nb.heal(self)
            spot.move_to(nb.p(nb.SLOT_X["loader"], 0.15))
            nb.show(self, spot, anims=[Create(spot)], run_time=0.5)
            vo.wait_until("The loader is gone")
            self.play(Indicate(spot, color=S.GREY, scale_factor=1.06), run_time=0.6)
            nb.heal(self)
            vo.wait_until("Are the 14,356 chunks gone too")
            self.play(nb.data.animate.set_opacity(0), run_time=0.4)
            nb.heal(self)
            nb.question(self, "vdb")
        card_p = ponder(self, "The loader ran with --rm\nand is gone.\nAre the 14,356 chunks gone too?", 8)

        # ========================================================== 7. the answer: inside the container
        inside = label("inside the container", 20, TURN)
        inside.move_to([-6.45 + inside.width / 2, -0.75, 0])
        dots_c = nb.data.get_center()
        pointer = Arrow(inside.get_top() + RIGHT * 0.4, dots_c + LEFT * 0.62 + DOWN * 0.02, buff=0.08,
                        color=TURN, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        gone = grey_chip("remove the container → gone · the loader refills it")
        gone.move_to([0.8, -2.45, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card_p), run_time=0.4)
            self.remove(card_p)
            nb.unquestion(self)
            self.play(nb.data.animate.set_opacity(1), run_time=0.5)
            nb.heal(self)
            self.play(GrowArrow(pointer), FadeIn(inside, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("they sit in the vector database container")
            self.play(Indicate(nb.data, color=TURN, scale_factor=1.15), run_time=0.6)
            nb.heal(self)
            vo.wait_until("which keeps running")
            self.play(Indicate(nb.boxes["vdb"], color=CONTAINER, scale_factor=1.08), run_time=0.7)
            nb.heal(self)
            vo.wait_until("Remove it, and the loader")
            self.play(FadeIn(gone, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, gone, INK)

        # ========================================================== 8. where inside: /data, the slip
        t2 = vm_term(rows=10)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(nb, pointer, inside, gone)), track(trk, 10, True), run_time=0.6)
            self.remove(nb, pointer, inside, gone)
            self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.4)
            lg = type_capture(self, t2, V25, type_time=0.5)[0]
            pin(self, lg, beside(extra_row(), lg))
            pp = out(self, t2, [(V25.line(3), TURN), V25.line(21)], run_time=0.4)
            vo.wait_until("A small slip")
            self.play(Indicate(pp[0], color=TURN, scale_factor=1.08), run_time=0.5)
            self.add(t2)
            vo.wait_until("Chroma saves to slash data")
            self.play(Indicate(substring(pp[1], "/data"), color=TURN, scale_factor=1.3), run_time=0.5)
            self.add(t2)
            ls = type_capture(self, t2, V28, type_time=0.35)[0]
            pin(self, ls, beside(extra_row(), ls))
            vo.wait_until("so the folder the README mounts stays empty")
            em = out(self, t2, V28.at((8, 11)), run_time=0.4)
            pin(self, em[0], beside(row_tag("empty", ERR), em[0]))
            dt = out(self, t2, ["…", *V28.at(18, 19), "…", (V28.line(23), OWN)], run_time=0.5)
            pin(self, dt[1], beside(row_tag("here", OWN), dt[1]))
            self.play(Indicate(dt[-1], color=OWN, scale_factor=1.05), run_time=0.5)
            self.add(t2)
            vo.wait_until("To keep the data on the VM disk")
            resize(self, t2, 4, run_time=0.6)
            ghost = mono(GHOST, 22, S.GREY)
            et = erratum_tag("erratum · README:95")
            row_a = VGroup(ghost, et).arrange(RIGHT, buff=0.35)
            fix = ok_chip(FIX, size=22, mono_font=True)
            rerun = label("then rerun: stop · rm · run · loader", 20, S.GREY)
            grp = VGroup(row_a, fix, rerun).arrange(DOWN, buff=0.5)
            grp.move_to([0, (t2.box.get_top()[1] + PIC_TOP) / 2, 0])
            fix.align_to(ghost, LEFT)
            rerun.align_to(ghost, LEFT)
            g_old, g_new = substring_text(ghost, "/chroma/chroma"), substring_text(fix.text, "/data")
            down = Arrow(g_old.get_bottom(), g_new.get_top() + UP * 0.12, buff=0.08, color=OWN,
                         stroke_width=4, max_tip_length_to_length_ratio=0.3)
            assert grp.get_left()[0] > -6.5 and grp.get_right()[0] < 6.5, (grp.get_left(), grp.get_right())
            assert grp.get_bottom()[1] > t2.box.get_top()[1] + 0.1 and grp.get_top()[1] < PIC_TOP, grp.get_top()
            self.play(FadeIn(ghost, shift=DOWN * 0.15), FadeIn(et), run_time=0.5)
            self.play(Indicate(g_old, color=ERR, scale_factor=1.15), run_time=0.5)
            vo.wait_until("mount slash data instead")
            self.play(GrowArrow(down), FadeIn(fix, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(g_new, color=OWN, scale_factor=1.25), run_time=0.5)
            vo.wait_until("rerun the stop, remove and run lines")
            self.play(FadeIn(rerun, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("then the loader")
            self.play(Indicate(rerun, color=INK, scale_factor=1.06), run_time=0.5)

        self.play(FadeOut(VGroup(trk, t2, ghost, et, down, fix, rerun)), run_time=0.6)
        self.remove(trk, t2, ghost, et, down, fix, rerun)
        self.wait(0.3)


def substring_text(txt: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a plain Text (no spaces in `sub`): its last occurrence."""
    s = txt.text if hasattr(txt, "text") else txt.original_text
    s_ns = "".join(s.split())
    i = s_ns.rfind(sub)
    assert i >= 0, (sub, s)
    return VGroup(*txt.submobjects[i:i + len(sub)])
