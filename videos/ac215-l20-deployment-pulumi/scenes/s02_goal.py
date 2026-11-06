"""S02 · From your laptop to one VM (AC215 L20). No tracker in beats 0-2; TRACKER [M] 1 from beat 3.
Lecture: 20 · 7 (the goal picture, beats 0-1), 20 · 8 (the four manual stages, beat 2).

Beats (script.md "## S02", one voiceover block each):
0. lecture_ref(20, "7"). V1 (MasterDiagram, manual variant, slid left so the VM sits in the middle)
   built in request order, one hop per phrase: the GREY browser window on top; the PINK 'HTTP 80'
   door on nginx and the PINK arrow browser -> door; TEAL nginx at the top of the BLUE VM panel; PINK
   arrows nginx -> frontend 3000 and nginx -> api-service 9000; api-service -> vector-db 8000. GREY
   `illustration` tag bottom left.
1. LECTURE (held). GREY dashed ghost arrows with the slide's arrowheads (frontend -> nginx, api ->
   nginx, vector-db -> api) flash beside the PINK arrows and rotate round to match them, then fade.
   "four containers": the four boxes pulse in turn. "a fifth": the dashed TEAL loader appears,
   pours dots into vector-db and leaves.
2. lecture_ref(20, "8"). The diagram slides right into the full manual layout: the GREY 'Your
   Machine' box on the left, the BLUE 'Docker Hub' panel in the middle, the dotted GCP outline round
   the VM. Slide 8's four stage chips along the bottom light YELLOW one per phrase: '1 Push' (arrow
   laptop -> Docker Hub), '2 Setup VM' (VM outline glows), '3 Deploy containers' (pull arrow, the
   four boxes and a dashed loader blink), '4 Web server' (nginx glows).
3. Everything fades (chips included: see deviations). TRACKER [M] 1. README card 'README.md · lines
   10–16' (the README's words, condensed as the SHOW gives them) on the left; on the right a
   GREY-dashed 'L18 · your laptop' sketch with three TEAL boxes, each ticking GREEN on its phrase.
4. A GREY note card with an `erratum` tag under the README card: "on v3's code: /status ->
   {"version":"3.0"}" and CODE(src/api-service/api/service.py: 34–36) inset; /status and 3.0 light.
5. A GREY-dashed chip 'L18 · cheese-app-v2 (refactored)' slides in under the sketch, a GREY arrow
   points down to a TEAL-outlined card 'this video · cheese-app-v3 / its own docker-shell.sh scripts'.
6. TRACKER [M] 1 · extra · our spelling, then · extra. A full-width `laptop` terminal: `git clone
   https://github.com/dlops-io/cheese-app-v3.git` (row tag `extra · our spelling`) -> TERM(p01: 2);
   p02's command (extra; folds) -> TERM(p02: 2) only. The hash YELLOW (not read), the date PINK; a
   GREY chip 'the course site links: main'. Fade; empty frame.

Deviations from SHOW: beat 2's chips do not shrink to a row under the top edge (text never scales
below 20 pt and the tracker holds that corner): they leave with the diagram when the tracker comes.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources (checked)
P01 = capture("p01")
P02 = capture("p02")
CLONE = "git clone https://github.com/dlops-io/cheese-app-v3.git"
assert P01.cmd == CLONE, P01.cmd
assert P01.line(2) == "Cloning into 'cheese-app-v3'...", P01.line(2)
assert P02.cmd.startswith("git -C cheese-app-v3 log -1 --format="), P02.cmd
HASH = "3ecef56fea879ac480d260c0906cd95baf05179a"
DATE = "2025-11-28"
assert P02.line(2).startswith(f"{HASH} {DATE} "), P02.line(2)

SERVICE = "src/api-service/api/service.py"
assert excerpt(SERVICE, 34, 36).split("\n")[0].strip() == '@api_app.get("/status")'
assert excerpt(SERVICE, 34, 36).split("\n")[2].strip() == 'return {"version": "3.0"}'

for n, s in ((10, "Ensure you have all your container built and works locally"),
             (12, "ChromaDB is up and running"), (14, "http://localhost:9000/docs"),
             (16, "http://localhost:3000/")):
    assert s in readme(n), (n, readme(n))

SHIFT = 3.4          # beats 0-1: the diagram slides left so the VM stands in the middle


def readme_body() -> VGroup:
    """The README's words (README:10-16), condensed as script.md's SHOW gives them."""
    def svc(name, rest, url=None):
        parts = [mono(name + ":", 22, CONTAINER)] + ([label(rest, 22, INK)] if rest else [])
        if url:
            parts.append(mono(url, 22, ROUTE))
        return VGroup(*parts).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    rows = VGroup(label("Ensure you have all your container", 22, INK),
                  label("built and works locally", 22, INK),
                  svc("vector-db", "ChromaDB is up and running"),
                  svc("api-service", None, "http://localhost:9000/docs"),
                  svc("frontend-react", None, "http://localhost:3000/"))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    rows[2:].shift(DOWN * 0.1)
    return rows


def laptop_sketch() -> VGroup:
    """GREY-dashed 'L18 · your laptop' with the three TEAL services. .frame .title .boxes{key}"""
    keys = ("vdb", "api", "front")
    names = {"vdb": "vector-db", "api": "api-service", "front": "frontend"}
    boxes = VGroup(*[svc_box(names[k], PORTS[k], box_w=2.5, box_h=0.72) for k in keys])
    boxes.arrange(DOWN, buff=0.2)
    title = label("L18 · your laptop", 22, S.GREY)
    inner = VGroup(title, boxes).arrange(DOWN, buff=0.25)
    fr = outline_box(inner.width + 1.6, inner.height + 0.5, LAPTOP, solid=False)
    inner.move_to(fr)
    boxes.shift(LEFT * 0.35)
    g = VGroup(fr, title, boxes)
    g.frame, g.title, g.boxes = fr, title, dict(zip(keys, boxes))
    return g


def two_line_card(rows, color, dashed: bool = False) -> VGroup:
    """A small outlined card holding label rows (all >= 20 pt). .box .rows"""
    t = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    ob = outline_box(t.width + 0.5, t.height + 0.32, color, solid=not dashed, fill_opacity=0.08)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.rows = ob, t
    return g


class TheGoal(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 7, len(SAY)

        # ========================================================== 0. the goal, in request order
        md = MasterDiagram(manual=True)
        md.shift(LEFT * SHIFT)
        md.slot = {k: md.p(*v) for k, v in md.SLOTS.items()}   # .slot is fixed in __init__: follow the shift
        ref7 = lref("7")
        ill = illustration_tag().move_to([-6.45, -2.6, 0], aligned_edge=LEFT)
        hops = VGroup()
        md.parts["routes"] = hops
        P = md.parts

        def hop(a, b):
            ar = route(a, b)
            ar.set_stroke(width=4)
            md.show(self, ar, anims=[GrowArrow(ar)], run_time=0.5, into=hops)
            return ar

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref7), run_time=0.4)
            md.vm(self)
            md.add(hops)                     # above the VM's opaque panel, under the boxes
            self.play(FadeIn(ill), run_time=0.3)
            md.browser(self)
            vo.wait_until("A browser sends a request to port 80")
            self.play(Indicate(P["browser"], color=INK, scale_factor=1.05), run_time=0.6)
            md.heal(self)
            md.box(self, "nginx")
            md.door(self, on="nginx")
            h_door = hop(P["browser"].get_bottom(), P["door80"].get_top() + UP * 0.02)
            vo.wait_until("where nginx passes pages")
            md.box(self, "front")
            nb = P["nginx"].frame
            h_front = hop(nb.get_bottom() + LEFT * 0.5, P["front"].frame.get_top() + RIGHT * 0.3)
            vo.wait_until("and data calls to the API")
            md.box(self, "api")
            h_api = hop(nb.get_bottom() + RIGHT * 0.5, P["api"].frame.get_top() + LEFT * 0.3)
            vo.wait_until("The API asks the vector database")
            md.box(self, "vdb")
            h_vdb = hop(P["api"].frame.get_bottom(), P["vdb"].frame.get_top())
            self.play(Indicate(P["vdb"].port, color=ROUTE, scale_factor=1.2), run_time=0.6)
            md.heal(self)

        # ========================================================== 1. arrowheads, and a fifth container
        ghosts = VGroup()
        for h in (h_front, h_api, h_vdb):
            s, e = h.get_start(), h.get_end()
            d = e - s
            n = np.array([-d[1], d[0], 0.0]) / np.linalg.norm(d)
            if (abs(d[0]) > abs(d[1]) and n[1] < 0) or (abs(d[0]) <= abs(d[1]) and n[0] < 0):
                n = -n                       # above a flat arrow, right of a steep one
            ga = DashedLine(e, s, color=S.GREY, stroke_width=4, dash_length=0.12)
            ga.add_tip(tip_length=0.2, tip_width=0.2)
            ga.scale(0.65).shift(n * 0.28)   # shorter than its PINK twin, so it stays clear of the boxes
            ghosts.add(ga)
        boxes4 = [P[k] for k in ("nginx", "front", "api", "vdb")]
        counts = [label(str(i + 1), 24, TURN).next_to(b.frame, LEFT, buff=0.12) for i, b in enumerate(boxes4)]
        five = label("5", 24, TURN).next_to(md.slot["loader"] + LEFT * 0.95, LEFT, buff=0.12)
        with self.voiceover(SAY[1]) as vo:
            self.play(LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.2), run_time=0.7)
            self.play(Indicate(ghosts, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("we draw requests the way they travel")
            self.play(*[Rotate(g, PI) for g in ghosts], run_time=0.8)
            self.play(*[Indicate(h, color=ROUTE, scale_factor=1.05) for h in (h_front, h_api, h_vdb)],
                      FadeOut(ghosts), run_time=0.7)
            md.heal(self)
            vo.wait_until("The slide shows four containers")
            for i, b in enumerate(boxes4):
                self.play(FadeIn(counts[i], scale=1.5), b.frame.animate.set_stroke(TURN), run_time=0.3)
            self.play(*[b.frame.animate.set_stroke(CONTAINER) for b in boxes4], run_time=0.3)
            md.heal(self)
            vo.wait_until("There is a fifth")
            md.loader(self, pour=True, leave=False)
            self.play(FadeIn(five, scale=1.5), run_time=0.3)
            data = set(P["data"].submobjects)      # the pour leaves each dot top-level too: keep them in V1 only
            self.mobjects = [m for m in self.mobjects if m not in data]
            md.heal(self)
            vo.wait_until("and then leaves")
            md.drop(self, P.pop("loader"), run_time=0.5, shift=DOWN * 0.2, extra=[FadeOut(VGroup(*counts, five))])

        # ========================================================== 2. slide 8: four manual stages
        ref8 = lref("8")
        with self.voiceover(SAY[2]) as vo:
            self.play(md.animate.shift(RIGHT * SHIFT), ReplacementTransform(ref7, ref8), run_time=0.8)
            md.slot = {k: md.p(*v) for k, v in md.SLOTS.items()}
            md.heal(self)
            md.gcp(self)
            md.laptop(self)
            md.registry(self)
            md.stage_chips(self)
            vo.wait_until("push the images")
            self.play(md.light_stage(1), run_time=0.4)
            md.push(self)
            vo.wait_until("set up the VM")
            self.play(md.light_stage(2), md.light("vm"), run_time=0.5)
            self.play(md.normal("vm"), run_time=0.5)
            vo.wait_until("deploy the containers")
            self.play(md.light_stage(3), run_time=0.4)
            md.pull(self)
            self.play(*[md.light(k, TURN) for k in ("nginx", "front", "api", "vdb")], run_time=0.4)
            md.loader(self, pour=False, leave=True)
            self.play(*[md.normal(k) for k in ("nginx", "front", "api", "vdb")], run_time=0.4)
            vo.wait_until("and put a web server in front")
            self.play(md.light_stage(4), md.light("nginx"), run_time=0.5)
            self.play(Indicate(P["nginx"], color=TURN, scale_factor=1.08), run_time=0.6)
            md.heal(self)
            vo.wait_until("That is our map for part 1")
            self.play(md.normal("nginx"), Indicate(md.stage_row, color=TURN, scale_factor=1.05), run_time=0.8)
            md.heal(self)

        # ========================================================== 3. README step 1: a check, not a command
        trk = tracker_m(1)
        card_ = readme_card((10, 16), readme_body())
        card_.move_to([-6.45 + card_.width / 2, 2.72 - card_.height / 2, 0])
        sk = laptop_sketch()
        sk.move_to([6.45 - sk.width / 2, 2.72 - sk.height / 2, 0])
        assert card_.get_right()[0] < sk.get_left()[0] - 0.2, (card_.get_right(), sk.get_left())
        assert card_.get_top()[1] < TRACK_BOTTOM - 0.1
        ticks = {}
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(md), FadeOut(ref8), FadeOut(ill), run_time=0.6)
            self.remove(md)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), run_time=0.5)
            self.play(Indicate(trk.caption, color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(trk)
            self.play(FadeIn(card_, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("your containers run locally")
            self.play(Create(sk.frame), FadeIn(sk.title), run_time=0.6)
            self.play(LaggedStart(*[GrowFromCenter(b) for b in sk.boxes.values()], lag_ratio=0.2), run_time=0.8)
            card_rows = {"vdb": card_.body[2], "api": card_.body[3], "front": card_.body[4]}
            for key, cue in (("vdb", "The vector database is up"), ("api", "the API shows its docs on port 9000"),
                             ("front", "and the frontend its home page on 3000")):
                vo.wait_until(cue)
                b = sk.boxes[key]
                tk = check_glyph(0.32).next_to(b, RIGHT, buff=0.18)
                ticks[key] = tk
                self.play(Create(tk), b.frame.animate.set_stroke(OWN),
                          Indicate(card_rows[key], color=OWN, scale_factor=1.04), run_time=0.6)
                self.add(card_)
        assert max(t.get_right()[0] for t in ticks.values()) < sk.frame.get_right()[0] - 0.05

        # ========================================================== 4. a small note: /status
        panel = code(SERVICE, 34, 36, font_size=20)
        head = VGroup(label("on v3's code:", 22, INK), mono("/status", 22, ROUTE), label("→", 22, INK),
                      mono('{"version":"3.0"}', 22, INK)).arrange(RIGHT, buff=0.15)
        etag = erratum_tag()
        inner = VGroup(head, panel).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        nbox = outline_box(inner.width + 0.4, inner.height + 0.5, S.GREY, solid=True, fill_opacity=0.06)
        inner.move_to(nbox).shift(DOWN * 0.08)
        etag.move_to(nbox.get_corner(UR) + np.array([-0.3 - etag.width / 2, 0, 0]))   # a tab on the top edge
        note_ = VGroup(nbox, inner, etag)
        note_.move_to([-6.45 + note_.width / 2, card_.get_bottom()[1] - 0.2 - note_.height / 2, 0])
        assert note_.get_bottom()[1] > -3.55, (note_.get_bottom(), note_.height, card_.height)
        assert note_.get_right()[0] < sk.get_left()[0] - 0.1 or note_.get_top()[1] < sk.get_bottom()[1] - 0.1, \
            (note_.get_right(), note_.get_top(), sk.get_left(), sk.get_bottom())
        api_url = card_.body[3][1]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(note_, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(etag, color=S.GREY, scale_factor=1.1), run_time=0.5)
            vo.wait_until("on this code, slash status is a better API check")
            st = code_span(panel.code, 0, "/status")
            self.play(Indicate(head[1], color=ROUTE, scale_factor=1.15), st.animate.set_color(ROUTE), run_time=0.7)
            self.play(Indicate(api_url, color=S.GREY, scale_factor=1.05), run_time=0.6)
            self.add(card_, note_)
            vo.wait_until("It answers version three point zero")
            v = code_span(panel.code, 2, '"3.0"')
            self.play(v.animate.set_color(TURN), head[3].animate.set_color(TURN), run_time=0.6)
            self.play(Indicate(head[3], color=TURN, scale_factor=1.1), run_time=0.6)
            self.add(note_)

        # ========================================================== 5. L18's v2 versus this video's v3
        v2 = dashed_chip("L18 · cheese-app-v2 (refactored)")
        v3 = two_line_card([label("this video · cheese-app-v3", 22, INK),
                            VGroup(label("its own", 22, INK), mono("docker-shell.sh", 22, INK),
                                   label("scripts", 22, INK)).arrange(RIGHT, buff=0.12)], CONTAINER)
        v2.move_to([sk.get_center()[0], sk.get_bottom()[1] - 0.4 - v2.height / 2, 0])
        v3.move_to([sk.get_center()[0], v2.get_bottom()[1] - 0.6 - v3.height / 2, 0])
        keep_inside(v3)
        v3.set_x(min(v3.get_x(), 6.45 - v3.width / 2))
        assert v3.get_bottom()[1] > -3.55 and v3.get_left()[0] > note_.get_right()[0] + 0.1, \
            (v3.get_bottom(), v3.get_left(), note_.get_right())
        v_ar = arrow(v2.get_bottom(), v3.get_top(), S.GREY, stroke=3, buff=0.06)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(v2, shift=LEFT * 0.4), run_time=0.6)
            vo.wait_until("it now teaches a refactored version 2")
            self.play(Indicate(v2, color=S.GREY, scale_factor=1.06), run_time=0.7)
            vo.wait_until("here you run version 3")
            self.play(GrowArrow(v_ar), run_time=0.4)
            self.play(FadeIn(v3, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("with this repository's scripts")
            self.play(Indicate(v3.rows[1][1], color=CONTAINER, scale_factor=1.12), run_time=0.7)

        # ========================================================== 6. which commit: main
        t = term(P_LAPTOP, rows=8, title=T_LAPTOP)
        site = grey_chip("the course site links: main")
        site.move_to([6.45 - site.width / 2, (t.box.get_top()[1] + TRACK_BOTTOM) / 2, 0])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(card_, note_, sk, v2, v3, v_ar, *ticks.values())),
                      track(trk, 1, "our spelling"), run_time=0.6)
            self.play(FadeIn(t, shift=UP * 0.3), run_time=0.4)
            ln = type_capture(self, t, P01, type_time=0.8)[0]
            tg = beside(extra_row("our spelling"), ln)
            pin(self, ln, tg)
            out(self, t, P01.at(2), run_time=0.3)
            self.play(track(trk, 1, True), run_time=0.4)
            ln2 = type_capture(self, t, P02, type_time=1.0)[0]
            tg2 = beside(extra_row(), ln2)
            pin(self, ln2, tg2)
            vo.wait_until("the branch the course site links")
            self.play(FadeIn(site, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("on recording day it was this November 2025 commit")
            rows = out(self, t, P02.at(2), wrap=True, run_time=0.4)
            first = rows[0]
            self.play(*[g.animate.set_color(TURN) for g in substring(first, HASH)], run_time=0.5)
            self.play(*[g.animate.set_color(ROUTE) for g in substring(first, DATE)], run_time=0.4)
            self.add(t)
            vo.wait_until("READMEs change")
            self.play(Indicate(site, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("git log shows which one you have")
            self.play(Indicate(rows_of(ln2)[0], color=TURN, scale_factor=1.04), run_time=0.8)
            self.add(t)
        self.play(FadeOut(VGroup(t, site, trk)), run_time=0.6)
        self.wait(0.3)
