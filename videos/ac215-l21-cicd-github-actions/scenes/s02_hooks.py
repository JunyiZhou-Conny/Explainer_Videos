"""S02 · Hooks stay on your laptop (AC215 L21, lecture recap; no tracker). Lecture: 21 · slides 2–3
(beats 0–2), 5–6 (beats 3–5), 7 (beat 6), 14–16 (beats 7–8).

Beats (script.md "## S02", one voiceover block each):
0. lecture_ref "2–3". V1 HookChain builds top centre: the GREY laptop frame "Git local hooks" with
   a GREY commit arrow inside it and a small door on its right edge. Two GREY tags fall onto it as
   they are named: 'pre-commit' on the commit arrow, 'pre-push' on the outer door. On "In lecture 9"
   the GREY dashed chip "lecture 9 · README Part 4" sits under the frame.
1. The chip leaves, the commit arrow gives way to the chain (the 'pre-commit' tag moves up to the
   title row): 'hygiene ×7' → 'Black' → 'Flake8' (PURPLE), each flashing on its phrase. Under the
   frame CODE(.pre-commit-config.yaml: 29–35), 'at the time of recording' beside line 30's rev,
   then a Transform to CODE(37–44) (20 pt) on "then Flake8"; line 43 (the 120 flag) YELLOW on "both
   at 120 columns", line 44 (files: ^src/…) YELLOW on "only on files under src". On "ends with
   tests" the GREY dashed 'Tests' box slides in at the chain's end; on "run none" it is struck RED,
   "CI runs these" under it.
2. The code panel leaves. A GREEN commit dot passes the three gates (each flashes GREEN). A second
   GREY laptop frame "no pre-commit install" (empty) appears below; its dot goes straight through.
   "depend on the laptop": both frames are circled in turn.
3. lecture_ref "5–6". Both laptops shrink into one small GREY laptop icon at the left edge. V1
   ServerDoor: BLUE "shared repository" with a door, GREY 'pre-receive' gate in front of it, GREY
   'post-receive' bell inside. On "so it can refuse it" a dot arrives, the gate shuts RED, the dot
   bounces back. On "The update hook" the chip "update: per branch" lands on the gate.
4. A dot enters through the open gate and lands inside; only then the bell rings (PINK arcs) with
   three GREY chips "integration tests", "notifications", "clean-up". On "no longer say no" the
   door is circled GREY behind the landed dot.
5. The chips and the dot fade first. The server becomes "GitHub.com", pre-receive turns GREY dashed
   with "your own scripts: not on GitHub.com"; the BLUE 'Actions' badge docks on the bell and the
   GREEN 'branch protection' gate in front of the door (each flashes on its phrase). The GREY
   caption "Actions on a push is the bell, not the gate." writes under the server and stays.
6. lecture_ref "7". A small GREY chat window "#build-alerts" right of the server; a dashed PINK
   arrow from the server toward it with a PINK "?" on it.
7. lecture_ref "14–16". Server, chat and caption clear; the laptop icon grows back into the first
   laptop's chain (top left). A dot passes the chain (each gate flashes GREY), then `git push`: the
   dot flies PINK into the BLUE "Shared Repository" frame (bottom right), which has no gates, only
   an empty GREY dashed slot; on "nothing runs them at all" the slot is circled.
8. The frame fills with slide 16's three boxes on their phrases (Build Container TEAL, Check Code,
   Test Summary); the dot passes them. On "from every laptop" a second laptop "no pre-commit
   install" appears bottom left and its dot arrives and passes the same three boxes. GREEN caption
   "continuous integration". Everything fades: empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources (checked)
CFG = ".pre-commit-config.yaml"
assert excerpt(CFG, 30, 30).strip() == "rev: 24.1.1"
assert excerpt(CFG, 34, 34).strip() == "args: ['--line-length', '120']"
assert excerpt(CFG, 35, 35).strip() == r"files: ^src/.*\.py$"
assert excerpt(CFG, 43, 43).strip() == "args: ['--max-line-length=120', '--extend-ignore=E203,W503']"
assert excerpt(CFG, 44, 44).strip() == r"files: ^src/.*\.py$"
assert VERSIONS["black (hook)"] == "24.1.1" and len(HYGIENE) == 7

CHAIN_Y = 1.6                    # the laptop frame's centre in beats 0-2 (top 2.9: under the lecture tag)
SERVER_C = np.array([1.2, 0.8, 0])
CHAT_C = np.array([5.0, -2.35, 0])


class LocalHooks(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 9, len(SAY)

        # ========================================================== 0. local hooks: the recap
        lr = lref("2–3")
        hc = HookChain().move_to([0, CHAIN_Y, 0])
        gy = hc.gates.get_center()[1]
        fl, fr_ = hc.frame.get_left()[0], hc.frame.get_right()[0]
        commit_ar = Arrow([fl + 0.35, gy, 0], [fr_ - 0.55, gy, 0], buff=0, color=S.GREY, stroke_width=3,
                          tip_length=0.2, max_tip_length_to_length_ratio=0.1)
        door = Rectangle(width=0.16, height=1.0, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
        door.move_to([fr_, gy, 0])
        pre_c = tag("pre-commit", S.GREY).next_to(commit_ar, UP, buff=0.12).align_to(commit_ar, LEFT)
        pre_c.shift(RIGHT * 0.5)
        pre_p = tag("pre-push", S.GREY).next_to(door, RIGHT, buff=0.15)
        past = dashed_chip("lecture 9 · README Part 4").next_to(hc.frame, DOWN, buff=0.22)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(lr), FadeIn(VGroup(hc.frame, hc.title), shift=UP * 0.2), run_time=0.7)
            self.play(GrowArrow(commit_ar), FadeIn(door), run_time=0.6)
            vo.wait_until("A pre-commit hook runs on your laptop")
            self.play(FadeIn(pre_c, shift=DOWN * 0.35), run_time=0.5)
            self.play(Indicate(pre_c, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("before the commit even exists")
            self.play(Indicate(commit_ar, color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("A pre-push hook")
            self.play(FadeIn(pre_p, shift=LEFT * 0.35), run_time=0.5)
            self.play(Indicate(door, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("In lecture 9")
            self.play(FadeIn(past, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(past, color=INK, scale_factor=1.06), run_time=0.6)

        # ========================================================== 1. this repo's chain
        p1 = code(CFG, 29, 35)
        p1.move_to([0, 0, 0]).align_to(np.array([0, 0.05, 0]), UP)
        p2 = code(CFG, 37, 44, font_size=20)
        p2.move_to(p1).align_to(p1, UP)
        rev = code_span(p1.code, 1, "24.1.1")
        rec = time_row().next_to(rev, RIGHT, buff=0.45)
        bars1 = VGroup(line_bar(p1.code, 5), line_bar(p1.code, 6))
        bar43, bar44 = line_bar(p2.code, 6), line_bar(p2.code, 7)
        title_row = pre_c.copy().next_to(hc.title, RIGHT, buff=0.3)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(past), FadeOut(commit_ar), pre_c.animate.move_to(title_row), run_time=0.5)
            self.remove(past, commit_ar)
            self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.2) for g in hc.gates], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(a) for a in hc.arrows], lag_ratio=0.3), run_time=0.9)
            self.add(hc)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(rec, shift=LEFT * 0.15), FadeIn(bars1), run_time=0.5)
            vo.wait_until("seven hygiene checks")
            self.play(hc.flash(0, TOOL), run_time=0.6)
            vo.wait_until("then Black")
            self.play(hc.flash(1, TOOL), Indicate(rev, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("then Flake8")
            self.play(FadeOut(rec), FadeOut(bars1), ReplacementTransform(p1, p2), hc.flash(2, TOOL),
                      run_time=0.7)
            self.remove(rec, bars1)
            vo.wait_until("both at 120 columns")
            self.play(FadeIn(bar43), Indicate(code_span(p2.code, 6, "120"), color=TURN), run_time=0.6)
            vo.wait_until("and only on files under src")
            self.play(FadeIn(bar44), Indicate(code_span(p2.code, 7, "^src/"), color=TURN), run_time=0.6)
            vo.wait_until("The lecture's chain ends with tests")
            # add_tests, split: the box slides in now, the strike lands on "run none"
            t_lab = label("Tests", hc.size, S.GREY)
            t_box = outline_box(t_lab.width + 0.36, 0.62, S.GREY)
            t_lab.move_to(t_box)
            tests = VGroup(t_box, t_lab).next_to(hc.gates[-1], RIGHT, buff=0.42)
            t_ar = DashedLine(hc.gates[-1].get_right() + RIGHT * 0.06, tests.get_left() + LEFT * 0.06,
                              color=S.GREY, stroke_width=2.5, dash_length=0.08)
            self.play(FadeIn(tests, shift=LEFT * 0.3), Create(t_ar), run_time=0.6)
            vo.wait_until("This repo's hooks run none")
            st = Line(tests.get_corner(DL), tests.get_corner(UR), color=ERR, stroke_width=4)
            ci_cap = label("CI runs these", 20, S.GREY).next_to(tests, DOWN, buff=0.15)
            if ci_cap.get_right()[0] > hc.frame.get_right()[0] - 0.1:
                ci_cap.align_to(tests, RIGHT)
            self.play(Create(st), run_time=0.4)
            vo.wait_until("it leaves the tests to CI")
            self.play(FadeIn(ci_cap, shift=UP * 0.15), run_time=0.4)
            self.play(Indicate(ci_cap, color=INK, scale_factor=1.08), run_time=0.6)
            hc.keep(self, t_ar, tests, st, ci_cap)

        # ========================================================== 2. hooks only where installed
        mate = HookChain((), title="no pre-commit install", frame_w=hc.frame.width, frame_h=1.2)
        mate.move_to([0, -1.25, 0])
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p2, bar43, bar44)), run_time=0.5)
            self.remove(p2, bar43, bar44)
            d1 = hc.commit(self)
            hc.pass_through(self, d1)
            self.play(d1.animate.move_to(door), Indicate(door, color=PASS, scale_factor=1.15), run_time=0.4)
            vo.wait_until("A teammate's laptop")
            self.play(FadeIn(mate, shift=UP * 0.3), run_time=0.6)
            d2 = mate.commit(self)
            mate.pass_through(self, d2, step=0.9)
            self.play(Flash(d2, color=S.GREY), run_time=0.5)
            vo.wait_until("So the checks depend on the laptop")
            self.play(Circumscribe(hc.frame, color=INK, buff=0.05), run_time=0.8)
            self.play(Circumscribe(mate.frame, color=INK, buff=0.05), run_time=0.8)

        # ========================================================== 3. remote hooks: the gate
        lr2 = lref("5–6")
        icon = laptop_icon(0.9)
        sd = ServerDoor(box_w=4.0, box_h=2.6)
        sd.shift(SERVER_C - sd.server.get_center())
        icon.move_to([sd.start[0] - 1.25, sd.start[1], 0])
        laptops = VGroup(hc, mate, d1, d2, door, pre_c, pre_p)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(lr), FadeTransform(laptops, icon), run_time=0.9)
            self.play(FadeIn(lr2), run_time=0.3)
            self.remove(*laptops)
            vo.wait_until("they run on the server")
            self.play(FadeIn(sd, shift=LEFT * 0.3), run_time=0.7)
            self.play(Indicate(sd.name, color=GITHUB, scale_factor=1.08), run_time=0.6)
            vo.wait_until("A pre-receive hook")
            self.play(Indicate(sd.gate.text, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("so it can refuse it")
            r_dot = sd.refuse(self)
            vo.wait_until("The update hook")
            sd.update_chip(self)
            vo.wait_until("one branch at a time")
            self.play(Indicate(sd.update_c, color=INK, scale_factor=1.06), FadeOut(r_dot), run_time=0.6)
            self.remove(r_dot)

        # ========================================================== 4. remote hooks: the bell
        with self.voiceover(SAY[4]) as vo:
            self.play(Indicate(sd.bell_text, color=INK, scale_factor=1.1), run_time=0.6)
            in_dot = sd.enter(self)
            vo.wait_until("for integration tests")
            sd.ring(self, ("integration tests", "notifications", "clean-up"))
            vo.wait_until("It can report")
            self.play(Indicate(sd.bell, color=ROUTE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("but it can no longer say no")
            self.play(Circumscribe(sd.door, color=S.GREY, buff=0.08), Flash(in_dot, color=PASS), run_time=0.8)

        # ========================================================== 5. what GitHub.com gives you
        cap = sd.caption().next_to(sd.server, DOWN, buff=0.3)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(in_dot), run_time=0.3)
            self.remove(in_dot)
            sd.drop(self, sd.chips, sd.waves)
            vo.wait_until("doesn't run your own pre-receive scripts")
            # ServerDoor.github(), split: relabel + dashed gate now, each new piece on its own phrase
            new_name = label("GitHub.com", 22, GITHUB).move_to(sd.name, aligned_edge=LEFT)
            dashed = dashed_copy(VGroup(*sd.gate.posts, sd.gate.bar), S.GREY)
            note_ = grey_chip("your own scripts: not on GitHub.com").next_to(sd.gate.text, DOWN, buff=0.12)
            note_.shift(RIGHT * (sd.door.get_left()[0] - 0.15 - note_.get_right()[0]))
            sd.drop(self, sd.update_c, run_time=0.3)
            sd.update_c = None
            self.play(FadeOut(sd.name), FadeIn(new_name), FadeOut(sd.gate.posts), FadeOut(sd.gate.bar),
                      FadeIn(dashed), FadeIn(note_), run_time=0.8)
            sd.remove(sd.gate, sd.name)
            self.remove(sd.gate, sd.name)
            sd.name, sd.gate_dashed = new_name, dashed
            act = github_chip("Actions").next_to(sd.bell, UP, buff=0.12)
            prot = gate_glyph(0.9, 0.6, PASS).move_to(sd.door.get_left() + LEFT * 0.42)
            prot.text = label("branch protection", 20, PASS).next_to(prot, UP, buff=0.12)
            prot.text.shift(LEFT * max(0, prot.text.get_right()[0] - (sd.door.get_left()[0] - 0.12)))
            sd.actions, sd.protection = act, prot
            sd.keep(self, new_name, dashed, note_)
            self.play(Indicate(note_, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Actions, which runs after the push")
            self.play(FadeIn(act, shift=DOWN * 0.3), run_time=0.5)
            self.play(Indicate(act, color=GITHUB, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and branch protection")
            self.play(FadeIn(prot, shift=RIGHT * 0.3), FadeIn(prot.text), run_time=0.5)
            sd.keep(self, act, prot, prot.text)
            sd.protect(self)
            vo.wait_until("which can say no")
            self.play(Write(cap), run_time=0.9)

        # ========================================================== 6. hooks act only inside Git
        lr3 = lref("7")
        chat = chat_window(win_w=2.8, win_h=1.4).move_to(CHAT_C)
        a = sd.server.get_right() + RIGHT * 0.12 + DOWN * 0.3
        b = chat.get_top() + UP * 0.12
        hook_ar = route(a, b, arc=-0.7, dashed=True)
        q = label("?", 28, ROUTE).move_to(hook_ar.get_center() + RIGHT * 0.45 + UP * 0.2)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(lr2), run_time=0.25)
            self.play(FadeIn(lr3), run_time=0.3)
            self.play(Circumscribe(sd.server, color=GITHUB, buff=0.05), run_time=0.8)
            vo.wait_until("To tell a chat what happened")
            self.play(FadeIn(chat, shift=LEFT * 0.3), run_time=0.6)
            self.play(Create(hook_ar), FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("the lecture reaches for webhooks")
            self.play(Indicate(q, color=ROUTE, scale_factor=1.4), run_time=0.7)

        # ========================================================== 7. slides 14-15: nothing checks it
        lr4 = lref("14–16")
        hc2 = HookChain().move_to([-2.6, CHAIN_Y, 0])
        sr = SharedRepo()
        sr.move_to([6.5 - sr.width / 2, -1.6, 0])
        top_in = np.array([sr.landing[0], sr.frame.get_center()[1] + 0.38, 0])      # above Build Container
        top_mid = np.array([sr.title.get_right()[0] + 0.5, top_in[1], 0])          # right of the title
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(sd, chat, hook_ar, q, cap)), FadeOut(lr3), run_time=0.5)
            self.play(FadeIn(lr4), run_time=0.3)
            self.remove(sd, chat, hook_ar, q, cap)
            self.play(ReplacementTransform(icon, hc2), run_time=0.9)
            vo.wait_until("On your laptop")
            d3 = hc2.commit(self)
            hc2.pass_through(self, d3, color=S.GREY)
            vo.wait_until("Then you push")
            self.play(FadeIn(sr, shift=LEFT * 0.3), run_time=0.5)
            hc2.push(self, d3, top_mid, arc=-0.5)
            vo.wait_until("nothing runs them at all")
            self.play(Circumscribe(sr.slot, color=S.GREY, buff=0.06), run_time=0.9)
            self.play(Indicate(sr.slot, color=INK, scale_factor=1.03), run_time=0.6)

        # ========================================================== 8. slide 16: the checks move
        mate2 = HookChain((), title="no pre-commit install", frame_w=3.9, frame_h=1.2)
        mate2.move_to([-6.4 + mate2.width / 2, -1.6, 0])
        ci = label("continuous integration", 28, PASS).next_to(sr.frame, DOWN, buff=0.25)
        with self.voiceover(SAY[8]) as vo:
            vo.wait_until("build a container")
            sr.fill(self, per=0.75)
            vo.wait_until("Same idea, new home")
            sr.pass_through(self, d3, step=0.25)
            self.play(FadeOut(d3), run_time=0.3)
            self.remove(d3)
            vo.wait_until("for every push to main")
            self.play(FadeIn(mate2, shift=UP * 0.2), run_time=0.5)
            d4 = mate2.commit(self)
            vo.wait_until("from every laptop")
            mate2.push(self, d4, top_in, arc=0.4, run_time=0.7)
            sr.pass_through(self, d4, step=0.25)
            vo.wait_until("That move is continuous integration")
            self.play(FadeIn(ci, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(ci, color=PASS, scale_factor=1.08), run_time=0.7)
        self.wait(1.0)

        everything = VGroup(lr4, hc2, sr, mate2, d4, ci)
        self.play(FadeOut(everything), run_time=0.6)
        self.remove(everything, *everything.get_family())
        self.wait(0.3)
