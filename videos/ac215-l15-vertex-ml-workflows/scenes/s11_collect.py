"""S11 · Collector and processor, by hand (README B › Data Collector steps 1-3, README B › Data
Processor steps 1-5, four extras, the V7 CallableImage set piece built, slides 34-37 redrawn).

Beats (script.md "## S11", one voiceover block each):
 0  TRACKER B2 1. A 3-row laptop terminal (20 pt), prompt ~/ml-workflow-aws: `cd src/data-collector`
    -> the prompt changes. CODE(src/data-collector/docker-shell.sh: 10): the bucket value YELLOW,
    tag `erratum`, chip "edit in all four: …", ▶ your turn. `sh docker-shell.sh` -> TERM(laptop/54:
    2) RED, row tag "captured before aws configure", GREY chip "our sh is not dash · …" over the
    terminal. CODE(docker-shell.sh: 13-21) (20 pt, full width): lines 14-16 `aws configure get`
    PINK, the check (18-20) RED bar.
 1  TRACKER B2 1. V1's drawer: ~/.aws with the GREY key card; a PINK arrow carries a copy of the key
    out as `-e AWS_ACCESS_KEY_ID` (docker-shell.sh:37) into the TEAL collector container. `sh
    docker-shell.sh` -> TERM(laptop/60: 3, squeezed) + "at the time of recording"; the prompt
    becomes root@<id>:/app# (▶ your turn). Two GREY chips, one per phrase: "builds linux/amd64
    (line 31) · Apple silicon emulates it" and "Ubuntu/Debian: sh is dash · skips the key check · run
    bash docker-shell.sh".
 2  LECTURE 15 · 34-36. V7 CallableImage built under CODE(src/data-collector/docker-entrypoint.sh:
    3-8): line 4 YELLOW = the switch; line 5 GREY bar -> the development card (choose dev); line 7
    BLUE bar -> the production card (choose prod); GREY-dashed note "the slide's version also logs
    in gcloud · not here". The lecture tag leaves with the picture.
 3  TRACKER B2 2. 12-row terminal at the root prompt types the search command (folds) -> TERM(
    laptop/60: 22 wrap, 24, …, 117, 118, …, 182, 183, …, 340, 341, …, 610-611, 654 from
    "S3UploadFailedError" wrap); the Searching / Done lines YELLOW, (InvalidAccessKeyId) RED. Chips
    over the terminal: "type the four queries exactly · …" and "stuck on one cheese? …". ▶ your turn.
 4  TRACKER B2 3 (chip "check your bucket · cannot pass here"), then B2 3 · extra: the for-loop
    listing (extra; folds) -> TERM(laptop/60: 659-663). The container terminal gives way to a
    5-row host terminal (~/ml-workflow-aws/src/data-collector): `ls -la ~; ls -la
    ~/persistent-folder/dataset` (extra) -> TERM(laptop/61: 9, 13-14, squeezed), line 9 ORANGE.
    Above it, the home folder: three folders side by side, persistent-folder ORANGE with chip
    "Docker made it · owned by root"; GREY chip "rerun from scratch: …".
 5  TRACKER B3 1 (section swap). Host terminal grows to 12 rows: `cd ../data-processor` (chip
    "exit the container first · this runs on your laptop") -> prompt; `sh docker-shell.sh` ->
    TERM(laptop/65: 50 cut, …, 71 cut) RED; TRACKER B3 1 · extra: the swap sed (extra; folds) ->
    TERM(laptop/66: 2-5), row tag "fix 1 again"; GREY chip "no Pipfile.lock here · the build
    resolves at build time" + a mono chip from laptop/67:730 and 733; `sh docker-shell.sh` -> the
    root prompt. Short typing times.
 6  TRACKER B3 2. `python cli.py --clean` (▶ your turn) -> TERM(laptop/68: 30 wrap, 31, 34-35, …,
    64, 107 from "S3UploadFailedError" wrap); line 30 YELLOW, Search Results {} GREEN + row tag "no
    duplicates among these 40", line 107 RED.
 7  TRACKER B3 3 (chip "check your bucket · cannot pass here"), B3 4: `python cli.py --prepare` ->
    TERM(laptop/68: 124, 126-127, 129, 133, 178 from "S3UploadFailedError" wrap); 126-127 YELLOW,
    129 and 133 GREEN. TRACKER B3 5 · extra: `ls -la /persistent/dataset; ls -la
    /persistent/dataset/tfrecords` (extra) -> TERM(laptop/68: 192-193).
 8  LECTURE 15 · 37. Terminal and tracker leave. Slide 37's two duty cards redrawn, each with a
    GREEN tick chip "AWS code does this". Then the cards and the tag leave; CODE(src/data-processor/
    tfrecords.py: 10-17), lines 12-15 YELLOW; under it the --query part of the typed search command
    (laptop/60:21) with the four strings YELLOW and an arrow from each to its folder-name line.
    Fade to empty.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
C54, C60, C61, C65, C66, C67, C68 = (capture(n) for n in ("54", "60", "61", "65", "66", "67", "68"))
assert C54.cmd == "sh docker-shell.sh" == C60.cmd == C65.cmd == C68.cmd
assert C61.cmd == "ls -la ~; ls -la ~/persistent-folder/dataset"
OUT54 = C54.at(2)
assert OUT54 == ["AWS not configured. Run: aws configure"]


def squeeze(s: str) -> str:
    """Runs of padding spaces (BuildKit's right-aligned timings, ls's columns) squeezed to two."""
    return re.sub(r" {3,}", "  ", s.rstrip())


BUILD60 = squeeze(C60.line(3))
assert BUILD60 == "[+] Building 40.4s (11/11) FINISHED  docker:default", BUILD60
SEARCH = C60.typed(21)
assert SEARCH == ('python cli.py --search --nums 10 --query "brie cheese" "gouda cheese" '
                  '"gruyere cheese" "parmigiano cheese"')
QUERIES = ("brie cheese", "gouda cheese", "gruyere cheese", "parmigiano cheese")
YL = TURN
ERR654 = from_phrase(C60.line(654), "S3UploadFailedError")
assert "(InvalidAccessKeyId)" in ERR654
OUT60 = ([C60.line(22), (C60.line(24), YL), "…", (C60.line(117), YL), (C60.line(118), YL), "…",
          (C60.line(182), YL), (C60.line(183), YL), "…", (C60.line(340), YL), (C60.line(341), YL), "…",
          (C60.line(610), YL), C60.line(611)])
assert C60.line(24) == "Searching for: brie cheese" and C60.line(341) == "Searching for: parmigiano cheese"
assert all(C60.line(n) == "[%] Done. Downloaded 10 images." for n in (117, 182, 340, 610))
assert C60.line(611) == "uploading file /persistent/dataset/raw.zip"
LOOP = C60.typed(658)
assert LOOP.startswith("for d in /persistent/dataset/raw/*")
OUT_LOOP = [cut(s, n=72) for s in C60.at((659, 663))]
assert OUT_LOOP[0] == "10 /persistent/dataset/raw/brie cheese" and OUT_LOOP[4].endswith("raw.zip")
OUT61 = [squeeze(s) for s in C61.at(9, 13, 14)]
assert OUT61[0].endswith("persistent-folder") and " root  root " in OUT61[0], OUT61
OUT65 = [cut(C65.line(50), n=72), "…", cut(C65.line(71), n=72)]
assert OUT65[0].endswith("exec /bin/sh: exec format error") and OUT65[2].startswith("ERROR: failed to build")
OUT66 = C66.at((2, 5))
assert OUT66[0] == "docker build -t $IMAGE_NAME -f Dockerfile ." and all(len(s) <= 72 for s in OUT66)
L730, L733 = C67.line(730), C67.line(733)
assert "Locking  dependencies..." in L730 and L733.endswith("✔ Success!")
LOCK_LINE = L730.split(" ", 2)[2].rstrip(".") + "… " + L733.split(" ", 2)[2]
CLEAN = C68.typed(21)
PREP = C68.typed(108)
LS68 = C68.typed(179)
assert CLEAN == "python cli.py --clean" and PREP == "python cli.py --prepare"
assert LS68 == "ls -la /persistent/dataset; ls -la /persistent/dataset/tfrecords"
assert C68.line(30).startswith("Labels: ['parmigiano cheese'") and C68.line(34) == "Search Results:"
assert C68.line(35).strip() == "{}" and C68.line(64) == "uploading file /persistent/dataset/clean.zip"
ERR107 = from_phrase(C68.line(107), "S3UploadFailedError")
ERR178 = from_phrase(C68.line(178), "S3UploadFailedError")
assert "clean.zip" in ERR107 and "tfrecords.zip" in ERR178
OUT_PREP = [C68.line(124), (C68.line(126), YL), (C68.line(127), YL), (C68.line(129), OWN),
            (C68.line(133), OWN)]
assert C68.line(126) == "train_xy count: 32" and C68.line(127) == "validate_xy count: 8"
assert C68.line(129).endswith("train_0000.tfrecords") and C68.line(133).endswith("val_0000.tfrecords")
OUT_LS68 = C68.at(192, 193)
assert OUT_LS68[0].endswith("train_0000.tfrecords") and OUT_LS68[1].endswith("val_0000.tfrecords")

assert excerpt("B/src/data-collector/docker-shell.sh", 10, 10).strip() == \
    f'export S3_BUCKET_NAME="{BUCKET_B}"'
assert "exec bash" in excerpt("B/src/data-collector/docker-entrypoint.sh", 5, 5)
assert excerpt("B/src/data-collector/docker-shell.sh", 37, 37).startswith("-e AWS_ACCESS_KEY_ID")
assert excerpt("B/src/data-processor/tfrecords.py", 12, 15).count("cheese") == 4


def fixed_tracker(key: str, step=None, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; the workaround of S01, S03-S09; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def text_chip(parts, color=S.GREY) -> VGroup:
    """A 20 pt chip (common.grey_chip's look) of mixed label / mono parts. .box .text"""
    t = VGroup(*[mono(x, 20, INK) if k == "mono" else label(x, 20, INK) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h = mono("|", 20).height + 0.24
    b = box(t.width + 0.48, h, color, fill_opacity=0.16, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def two_line_note(a: str, b: str, color=PAST) -> VGroup:
    """A GREY-dashed note of two label lines (past/elsewhere: the slide's version). .box .text"""
    t = VGroup(label(a, 20, color), label(b, 20, color)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    ob = outline_box(t.width + 0.48, t.height + 0.32, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def home_folder(name: str, color, owner: str) -> VGroup:
    """A folder glyph with its name under it and a small owner line ('student' / 'root')."""
    f = folder_icon(0.62, color)
    n = mono(name, 20, INK if color != SHARED else SHARED).next_to(f, DOWN, buff=0.14)
    o = label(owner, 20, color).next_to(n, DOWN, buff=0.08)
    g = VGroup(f, n, o)
    g.icon, g.name, g.owner = f, n, o
    return g


class CollectAndClean(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 9, len(SAY)
        self.bar_tags = []

        # ========================================================== 0. step 1: the bucket, no keys
        tr = fixed_tracker("B2", 1)
        t = term(P_MW, rows=3, size=SIZE)
        self.t = t
        p10 = code("B/src/data-collector/docker-shell.sh", 10, 10)
        p10.move_to([-6.45 + p10.width / 2, 2.7 - p10.height / 2, 0])
        er10 = erratum_tag().next_to(p10, RIGHT, buff=0.25).align_to(p10, UP)
        all4 = grey_chip("edit in all four: data-collector :10 · data-processor :10 · "
                         "model-training :9–10 · workflow :8–9")
        all4.next_to(p10, DOWN, buff=0.25).align_to(p10, LEFT)
        yt10 = your_turn().next_to(er10, DOWN, buff=0.2).align_to(er10, LEFT)
        assert all4.get_right()[0] < 6.5 and yt10.get_right()[0] < 6.5 and yt10.get_bottom()[1] > all4.get_top()[1] - 0.6
        p13 = code("B/src/data-collector/docker-shell.sh", 13, 21, font_size=20)
        p13.move_to([0, 2.85 - p13.height / 2, 0])
        dash0 = grey_chip("our sh is not dash · on Ubuntu or Debian this check is skipped")
        under_term(t, dash0)
        assert p13.get_bottom()[1] > dash0.get_top()[1] + 0.05, (p13.get_bottom(), dash0.get_top())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), FadeIn(t), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.5)
            type_cmd(self, t, "cd src/data-collector", type_time=0.7)
            cd_prompt(self, t, P_SRC("data-collector"))
            vo.wait_until("A small gap first")
            self.play(FadeIn(p10, shift=DOWN * 0.2), run_time=0.5)
            v10 = code_span(p10.code, 0, f'"{BUCKET_B}"')
            self.play(v10.animate.set_color(TURN), FadeIn(er10, shift=LEFT * 0.1), run_time=0.5)
            self.add(p10)
            vo.wait_until("all four part 2 scripts")
            self.play(FadeIn(all4, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(all4.text, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("so put yours in each one")
            self.play(FadeIn(yt10, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(code_span(p10.code, 0, f'"{BUCKET_B}"'), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            self.add(p10)
            vo.wait_until("Then, in this folder")
            self.play(FadeOut(VGroup(p10, er10, all4, yt10)), run_time=0.5)
            type_cmd(self, t, C54.cmd, type_time=0.6)
            vo.wait_until("Without keys")
            r54 = out(self, t, [(OUT54[0], ERR)], run_time=0.4)
            cb = beside(row_tag("captured before aws configure"), r54[0])
            pin(self, r54[0], cb)
            self.play(FadeIn(dash0, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the script stops itself")
            self.play(FadeIn(p13, shift=DOWN * 0.2), run_time=0.6)
            pk = [code_span(p13.code, k, "aws configure get") for k in (1, 2, 3)]
            self.play(*[g.animate.set_color(ROUTE) for g in pk], run_time=0.5)
            self.add(p13)
            chk = VGroup(*[line_bar(p13.code, k, ERR, 0.2) for k in (5, 6, 7)])
            self.play(FadeIn(chk), run_time=0.4)
            self.play(Indicate(code_span(p13.code, 6, 'echo "AWS not configured. Run: aws configure"'),
                               color=ERR, scale_factor=1.05),
                      Indicate(substring(r54[0], "AWS not configured."), color=ERR, scale_factor=1.08),
                      run_time=0.8)
            self.add(p13, chk)
            self.reseat()

        # ========================================================== 1. with keys: build, root shell
        dr = drawer().move_to([-4.6, 0.85, 0])
        kc = key_card().move_to(dr.slot(0) + DOWN * 0.15)
        box_c = outline_box(4.3, 1.5, IMAGE, solid=True, fill_opacity=0.08).move_to([3.9, 0.85, 0])
        box_t = mono("cheese-app-data-collector", 20, IMAGE).move_to(box_c.get_top() + DOWN * 0.3)
        e_chip = chip("-e AWS_ACCESS_KEY_ID", ROUTE, size=20, font=MONO).move_to([-0.35, 1.75, 0])
        e_src = label("docker-shell.sh:37", 20, S.GREY).next_to(e_chip, UP, buff=0.12)
        rt = route(kc.get_right() + RIGHT * 0.05, box_c.get_left() + DOWN * 0.15, arc=-0.5)
        pic1 = VGroup(dr, kc, box_c, box_t, e_chip, e_src, rt)
        assert pic1.get_top()[1] < PIC_TOP and pic1.get_bottom()[1] > dash0.get_top()[1], (pic1.get_top(), pic1.get_bottom())
        amd = grey_chip("builds linux/amd64 (line 31) · Apple silicon emulates it")
        dsh = text_chip([("Ubuntu/Debian: sh is dash · skips the key check · run", "label"),
                         ("bash docker-shell.sh", "mono")])
        amd.move_to([0, 1.55, 0])
        dsh.move_to([0, 0.75, 0])
        assert dsh.width < 12.9, dsh.width

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p13, chk)), FadeOut(dash0), run_time=0.5)
            self.play(FadeIn(dr), FadeIn(kc), FadeIn(box_c), FadeIn(box_t), run_time=0.6)
            ghost = kc.copy()
            self.play(Create(rt), FadeIn(e_chip, scale=0.9), FadeIn(e_src), run_time=0.7)
            self.play(MoveAlongPath(ghost, rt), run_time=1.0)
            self.play(ghost.animate.move_to(box_c.get_center() + DOWN * 0.2), run_time=0.4)
            type_cmd(self, t, C60.cmd, type_time=0.6)
            vo.wait_until("it builds in 40 seconds")
            r3 = out(self, t, [BUILD60], run_time=0.4)
            self.play(Indicate(substring(r3[0], "40.4s"), color=TURN, scale_factor=1.2), run_time=0.6)
            self.reseat()
            vo.wait_until("and opens a root shell")
            cd_prompt(self, t, P_ROOT, color=TURN)
            yt1 = on_bar(t, turn_row())
            self.bar(yt1)
            vo.wait_until("Two notes")
            self.play(FadeOut(VGroup(dr, kc, box_c, box_t, e_chip, e_src, rt, ghost)), run_time=0.5)
            tm = beside(time_row(), r3[0], buff=0.3)
            assert tm.get_right()[0] < t.box.get_right()[0] - 0.08, tm.get_right()
            pin(self, r3[0], tm)
            vo.wait_until("This script builds for A M D 64")
            self.play(FadeIn(amd, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(amd.text, color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("And on Ubuntu or Debian")
            self.play(FadeIn(dsh, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("so run bash docker-shell.sh")
            self.play(Indicate(dsh.text[1], color=TURN, scale_factor=1.08), run_time=0.8)

        # ========================================================== 2. V7: one image, two modes
        ep = code("B/src/data-collector/docker-entrypoint.sh", 3, 8, font_size=20)
        ep.move_to([-6.45 + ep.width / 2, 2.72 - ep.height / 2, 0])
        lt = lref("34–36")
        v = CallableImage(built=False)
        dy = -1.95
        v.shift(UP * dy)
        v.parts.shift(UP * dy)
        v.pivot = v.image.frame.get_left() + RIGHT * 0.05      # (the piece stores it at build time)
        assert v.parts.get_top()[1] < ep.get_bottom()[1] - 0.2 and v.parts.get_bottom()[1] > -3.6, \
            (v.parts.get_top(), ep.get_bottom(), v.parts.get_bottom())
        gnote = two_line_note("the slide's version also", "logs in gcloud · not here")
        gnote.next_to(ep, RIGHT, buff=0.35).align_to(ep, DOWN)
        assert gnote.get_right()[0] < 6.5 and gnote.get_top()[1] < lt.get_bottom()[1] - 0.1, gnote.get_right()
        b4 = line_bar(ep.code, 1, TURN, 0.22)
        b5 = line_bar(ep.code, 2, LAPTOP, 0.25)
        b7 = line_bar(ep.code, 4, CLOUD, 0.25)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t), FadeOut(amd), FadeOut(dsh), *self.unbar_anims(), run_time=0.5)
            self.remove(t)
            self.play(FadeIn(ep, shift=DOWN * 0.2), FadeIn(lt), run_time=0.6)
            vo.wait_until("The entry point script has a switch")
            self.play(FadeIn(b4), code_span(ep.code, 1, "if [[ $# -eq 0 ]]").animate.set_color(TURN), run_time=0.5)
            self.add(ep, b4)
            v.show(self, v.image, v.input, v.switch,
                   anims=[FadeIn(v.image, shift=UP * 0.2), FadeIn(v.input), Create(v.switch)], run_time=0.8)
            self.play(Indicate(v.switch, color=TURN, scale_factor=1.3), run_time=0.6)
            v.heal(self)
            vo.wait_until("No arguments")
            self.play(FadeIn(b5), run_time=0.3)
            v.show(self, v.branches["dev"], v.cards["dev"],
                   anims=[GrowArrow(v.branches["dev"]), FadeIn(v.cards["dev"], shift=LEFT * 0.2)], run_time=0.7)
            vo.wait_until("development mode")
            v.choose(self, "dev")
            vo.wait_until("Arguments: it runs them")
            self.play(FadeIn(b7), run_time=0.3)
            v.show(self, v.branches["prod"], v.cards["prod"],
                   anims=[GrowArrow(v.branches["prod"]), FadeIn(v.cards["prod"], shift=LEFT * 0.2)], run_time=0.7)
            vo.wait_until("production mode")
            v.choose(self, "prod")
            vo.wait_until("The lecture calls that")
            self.play(FadeIn(gnote, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(v.image.frame, color=IMAGE, scale_factor=1.04), run_time=0.8)
            v.heal(self)

        # ========================================================== 3. step 2: search, upload fails
        t = term(P_ROOT, rows=12, size=SIZE)
        self.t = t
        q_chip = grey_chip("type the four queries exactly · other names → KeyError in the processor")
        ctrl_c = grey_chip("stuck on one cheese? Ctrl-C and run again")
        under_term(t, q_chip)
        ctrl_c.next_to(q_chip, UP, buff=0.1).align_to(q_chip, RIGHT)
        assert ctrl_c.get_top()[1] < 3.4 and ctrl_c.get_left()[0] > tr.get_right()[0] + 0.3, (ctrl_c.get_top(), ctrl_c.get_left())
        yt3 = on_bar(t, turn_row())

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(ep, b4, b5, b7, gnote)), FadeOut(v), FadeOut(lt), track(tr, 2), run_time=0.6)
            self.play(FadeIn(t), run_time=0.4)
            cmd = type_cmd(self, t, SEARCH, type_time=2.0)
            self.bar(yt3)
            vo.wait_until("four cheeses")
            self.play(FadeIn(q_chip, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("ten images each")
            self.play(FadeIn(ctrl_c, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("It scrapes the web")
            out(self, t, OUT60[:1], wrap=True, run_time=0.4)
            out(self, t, OUT60[1:6], run_time=0.8, lag=0.15)
            vo.wait_until("writes four folders")
            out(self, t, OUT60[6:13], run_time=1.0, lag=0.15)
            vo.wait_until("zips them")
            r611 = out(self, t, OUT60[13:], run_time=0.4)
            self.play(Indicate(substring(r611[0], "raw.zip"), color=TURN, scale_factor=1.15), run_time=0.6)
            self.reseat()
            vo.wait_until("AWS rejects our fake key")
            r654 = out(self, t, [(ERR654, ERR)], wrap=True, run_time=0.5)
            hit = [r for r in r654 if "(InvalidAccessKeyId)" in r.text][0]
            self.play(Indicate(substring(hit, "(InvalidAccessKeyId)"), color=ERR, scale_factor=1.12), run_time=0.8)
            self.reseat()

        # ========================================================== 4. step 3 + extras: what is on disk
        nb = grey_chip("check your bucket · cannot pass here")
        under_term(t, nb)
        h = term(P_SRC("data-collector"), rows=5, size=SIZE)
        f1 = home_folder("ml-workflow-aws", LAPTOP, "student")
        f2 = home_folder("model-deployment-aws", LAPTOP, "student")
        f3 = home_folder("persistent-folder", SHARED, "root")
        folders = VGroup(f1, f2, f3).arrange(RIGHT, buff=0.9, aligned_edge=UP)
        tilde = mono("~/", 24, LAPTOP)
        home = VGroup(tilde, folders).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        home.move_to([-0.3, 1.75, 0])
        made = chip("Docker made it · owned by root", SHARED, size=20).next_to(f3, DOWN, buff=0.2)
        made.align_to(f3, RIGHT)
        rerun = grey_chip("rerun from scratch: delete persistent-folder first (old data wins over the bucket)")
        rerun.move_to([0, -0.35, 0])
        assert home.get_top()[1] < PIC_TOP and made.get_right()[0] < 6.5 and made.get_bottom()[1] > rerun.get_top()[1] + 0.05, \
            (home.get_top(), made.get_right(), made.get_bottom(), rerun.get_top())
        assert rerun.get_bottom()[1] > h.box.get_top()[1] + 0.05, (rerun.get_bottom(), h.box.get_top())

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(q_chip), FadeOut(ctrl_c), track(tr, 3), run_time=0.5)
            self.play(FadeIn(nb, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(nb.text, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("An extra listing")
            self.wipe(FadeOut(nb), track(tr, 3, True), *self.unbar_anims())
            type_cmd(self, t, LOOP, type_time=1.2)
            self.bar(on_bar(t, extra_row()))
            rl = out(self, t, OUT_LOOP, run_time=0.6)
            vo.wait_until("shows 40 images on disk")
            self.play(each([substring(r, "10") for r in rl[:4]], TURN, 1.3), run_time=0.9)
            self.reseat()
            vo.wait_until("On the laptop")
            self.play(FadeOut(t), *self.unbar_anims(), run_time=0.4)
            self.remove(t)
            self.t = t = h
            self.play(FadeIn(h), run_time=0.4)
            type_cmd(self, h, C61.cmd, type_time=0.8)
            self.bar(on_bar(h, extra_row()))
            r61 = out(self, h, OUT61, run_time=0.5)
            vo.wait_until("a root-owned persistent folder")
            self.paint(r61[0], "root  root", SHARED)
            self.paint(r61[0], "persistent-folder", SHARED)
            self.play(FadeIn(home, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(made, shift=UP * 0.1), Indicate(f3.icon, color=SHARED, scale_factor=1.15), run_time=0.6)
            vo.wait_until("appeared beside the clones")
            self.play(Indicate(VGroup(f1.icon, f2.icon), color=INK, scale_factor=1.08), run_time=0.6)
            self.play(FadeIn(rerun, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 5. the processor: fix 1 again
        exit_c = grey_chip("exit the container first · this runs on your laptop")
        nolock = grey_chip("no Pipfile.lock here · the build resolves at build time")
        lockc = chip(LOCK_LINE, S.GREY, size=20, font=MONO)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(home, made, rerun)), *self.unbar_anims(), run_time=0.4)
            tr = swap_tracker(self, tr, fixed_tracker("B3", 1))
            self.resize(12, keep=0)
            under_term(t, exit_c)
            self.play(FadeIn(exit_c, shift=DOWN * 0.1), run_time=0.3)
            type_cmd(self, t, "cd ../data-processor", type_time=0.5, soft=True)
            cd_prompt(self, t, P_SRC("data-processor"), run_time=0.4)
            type_cmd(self, t, C65.cmd, type_time=0.4)
            vo.wait_until("the A R M 64 line fails again")
            r65 = out(self, t, [(OUT65[0], ERR), "…", (OUT65[2], ERR)], run_time=0.4)
            self.play(Indicate(substring(r65[0], "exec format error"), color=ERR, scale_factor=1.1), run_time=0.5)
            self.reseat()
            vo.wait_until("and the same swap fixes it")
            self.play(FadeOut(exit_c), track(tr, 1, True), run_time=0.3)
            type_cmd(self, t, C66.cmd, type_time=0.8, soft=True)
            r66 = out(self, t, OUT66, run_time=0.4)
            fx = beside(row_tag("fix 1 again", OWN), r66[0])
            pin(self, r66[0], fx, run_time=0.3)
            under_term(t, nolock)
            lockc.next_to(nolock, UP, buff=0.1).align_to(nolock, RIGHT)
            self.play(FadeIn(nolock, shift=DOWN * 0.1), FadeIn(lockc, shift=DOWN * 0.1), run_time=0.4)
            type_cmd(self, t, C68.cmd, type_time=0.4)
            cd_prompt(self, t, P_ROOT, color=TURN, run_time=0.4)

        # ========================================================== 6. step 2: --clean
        with self.voiceover(SAY[6]) as vo:
            self.wipe(FadeOut(nolock), FadeOut(lockc), track(tr, 2))
            cl = type_cmd(self, t, CLEAN, type_time=0.7)
            ytc = beside(turn_row(), cl)
            pin(self, cl, ytc)
            vo.wait_until("A duplicate finder")
            out(self, t, [(C68.line(30), YL)], wrap=True, run_time=0.4)
            out(self, t, [C68.line(31)], run_time=0.3)
            vo.wait_until("finds none among these 40")
            r34 = out(self, t, [(C68.line(34), OWN), (C68.line(35), OWN)], run_time=0.4)
            nd = beside(row_tag("no duplicates among these 40", OWN), r34[1])
            pin(self, r34[1], nd)
            vo.wait_until("and the upload of clean dot zip fails")
            out(self, t, ["…", C68.line(64)], run_time=0.4)
            r107 = out(self, t, [(ERR107, ERR)], wrap=True, run_time=0.5)
            hit = [r for r in r107 if "(InvalidAccessKeyId)" in r.text][0]
            self.play(Indicate(substring(hit, "(InvalidAccessKeyId)"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.reseat()
            vo.wait_until("Pause and run it")
            if cl in t.lines.submobjects:
                flash_tag(self, ytc)
            self.reseat()

        # ========================================================== 7. steps 3-5: --prepare, on disk
        nb7 = grey_chip("check your bucket · cannot pass here")
        under_term(t, nb7)

        with self.voiceover(SAY[7]) as vo:
            self.play(track(tr, 3), FadeIn(nb7, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(nb7.text, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("then dash dash prepare")
            self.wipe(FadeOut(nb7), track(tr, 4))
            type_cmd(self, t, PREP, type_time=0.7)
            vo.wait_until("All 40 images split")
            rp = out(self, t, OUT_PREP[:3], run_time=0.5)
            vo.wait_until("in two real TFRecord files")
            rp2 = out(self, t, OUT_PREP[3:], run_time=0.4)
            self.play(each([substring(rp2[0], "train_0000.tfrecords"), substring(rp2[1], "val_0000.tfrecords")],
                           OWN, 1.1), run_time=0.7)
            self.reseat()
            vo.wait_until("The upload fails again")
            out(self, t, [(ERR178, ERR)], wrap=True, run_time=0.5)
            vo.wait_until("Step 5 finds them only on disk")
            self.play(track(tr, 5, True), run_time=0.4)
            ls = type_cmd(self, t, LS68, type_time=0.6)
            self.bar(on_bar(t, extra_row()))
            rls = out(self, t, [(s, OWN) for s in OUT_LS68], run_time=0.4)
            self.play(each([substring(rls[0], "train_0000.tfrecords"), substring(rls[1], "val_0000.tfrecords")],
                           OWN, 1.1), run_time=0.7)
            self.reseat()

        # ========================================================== 8. slide 37's duty cards; labels
        lt37 = lref("37")
        dc = duty_card([("Data Collector · download images, upload", True)])
        dp = duty_card([("Data Processor · verify, de-duplicate, convert to TFRecords", True)])
        dc.move_to([-6.45 + dc.width / 2, 1.7, 0])
        dp.move_to([-6.45 + dp.width / 2, 0.45, 0])
        oc = ok_chip("AWS code does this").next_to(dc, RIGHT, buff=0.3)
        op = ok_chip("AWS code does this").next_to(dp, RIGHT, buff=0.3)
        assert op.get_right()[0] < 6.5 and oc.get_right()[0] < 6.5, (op.get_right(), oc.get_right())
        tf = code("B/src/data-processor/tfrecords.py", 10, 17, cuts={17: '"labels": ['})
        tf.move_to([-6.45 + tf.width / 2, 2.75 - tf.height / 2, 0])
        qtext = SEARCH[SEARCH.index("--query"):]
        ql = mono_line(qtext, 20, INK)
        ql.move_to([0, -2.45, 0])
        assert ql.get_left()[0] > -6.5 and ql.get_right()[0] < 6.5, (ql.get_left(), ql.get_right())
        qsrc = label("the search command you typed (data collector, step 2)", 20, S.GREY)
        qsrc.next_to(ql, DOWN, buff=0.22)
        x_col = tf.get_right()[0] + 1.4
        col = VGroup()
        for k, q in enumerate(QUERIES):
            ln = tf.code.code_lines[2 + k]
            m = mono_line(f'"{q}"', 22, TURN)
            m.move_to([x_col + m.width / 2, ln.get_center()[1], 0])
            col.add(m)
        assert col.get_right()[0] < 6.5 and col.get_bottom()[1] > tf.get_bottom()[1] - 0.3, col.get_right()
        bars12 = VGroup(*[line_bar(tf.code, k, TURN, 0.2) for k in (2, 3, 4, 5)])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(t), FadeOut(tr), *self.unbar_anims(), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(lt37), FadeIn(dc, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(oc, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("then verify")
            self.play(FadeIn(dp, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(op, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("convert to TFRecords")
            self.play(Indicate(dp.rows[0].mark, color=OWN, scale_factor=1.4),
                      Indicate(dc.rows[0].mark, color=OWN, scale_factor=1.4), run_time=0.8)
            vo.wait_until("And the four labels")
            self.play(FadeOut(VGroup(dc, dp, oc, op)), FadeOut(lt37), run_time=0.5)
            self.play(FadeIn(tf, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(bars12),
                      *[code_span(tf.code, k, f'"{q}"').animate.set_color(TURN) for k, q in zip((2, 3, 4, 5), QUERIES)],
                      run_time=0.6)
            self.add(tf, bars12)
            vo.wait_until("your search queries")
            self.play(FadeIn(ql, shift=UP * 0.2), FadeIn(qsrc), run_time=0.6)
            qs = [substring(ql, f'"{q}"') for q in QUERIES]
            self.play(*[g.animate.set_color(TURN) for g in qs], run_time=0.4)
            self.add(ql)
            self.play(LaggedStart(*[TransformFromCopy(g, m) for g, m in zip(qs, col)], lag_ratio=0.2),
                      run_time=1.2)
            self.add(ql)
            arrs = VGroup()
            for k, m in enumerate(col):
                end = tf.code.code_lines[2 + k].get_right()
                arrs.add(Arrow(m.get_left() + LEFT * 0.08, [end[0] + 0.12, m.get_center()[1], 0], buff=0,
                               color=TURN, stroke_width=3, tip_length=0.16,
                               max_tip_length_to_length_ratio=0.25))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("so type them exactly")
            self.play(Indicate(ql, color=TURN, scale_factor=1.04), run_time=0.8)
            self.add(ql)

        self.play(FadeOut(VGroup(tf, bars12, ql, qsrc, col, arrs)), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def bar(self, tg):
        """Show a title-bar tag (on_bar) and remember it, so it fades with the terminal."""
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def resize(self, rows: int, keep=None):
        """common.resize() with the title-bar tags riding along."""
        dy = (rows - self.t.rows) * self.t.pitch
        resize(self, self.t, rows, keep=keep, extra=[tg.animate.shift(UP * dy) for tg in self.bar_tags])

    def wipe(self, *extra, run_time: float = 0.4):
        """PLAYS: the terminal's rows fade out (with `extra` alongside) and leave it for good."""
        t = self.t
        gone = list(t.lines.submobjects)
        for m in gone:
            t.lines.remove(m)
        if gone or extra:
            self.play(*[FadeOut(m) for m in gone], *extra, run_time=run_time)
        self.remove(*gone)
        self.reseat()

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        self.add(self.t, *self.bar_tags)

    def paint(self, row, sub, color, run_time: float = 0.4):
        """Colour substring `sub` of terminal row `row`."""
        self.play(substring(row, sub).animate.set_color(color), run_time=run_time)
        self.reseat()
