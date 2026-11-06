"""S16 · Tear down, recap, and what's next (AC215 L18, part 2, last scene). No tracker. Lecture:
18 · 19–21 (APIs) in beat 2, 18 · 46 (APIs) then 18 · 40–41 (Frontend) in beat 3, off from beat 4.
Ends the video on an empty frame.

Beats (script.md "## S16", one voiceover block each):
0. A GOLD-outlined checklist card "Clean up · all done once already". One item per phrase writes in and
   its box ticks GREEN: Ctrl-C and exit in every container terminal (--rm deletes them) · docker compose
   down · src/vector-db, or src if you used Compose · branch 2025: stop its Chroma, git switch main ·
   docker system prune · check its list first (other projects too) · what prune keeps: docker volume rm
   cheese-app-frontend-react-node_modules · docker image ls, then remove the cheese-app-* and chromadb
   images by name if you need the space (GOLD "disk" chip) · your key stays in secrets/, outside every
   repository.
1. The card fades. S01's strip question "From 3000 to 9000: who carried it?" returns top-left. V1 as
   the whole trip on main (localhost:3000/newsletters, frontend-react on 3000 → :5173 with the PURPLE
   courier "Vite", a PURPLE "nginx · in production" chip under the laptop, the API on 9000, GREEN cable),
   one hop per phrase: 1, 2, 3 to the 3000 door; 3½ the courier carries "/api/…" along the cable by
   name; 4 the API's uvicorn flashes and a PINK router leaf "/api/newsletters" settles on its box; 5 the
   JSON comes back the same way; 6 the page. One PINK origin "page and calls" http · localhost · 3000
   under the browser, a struck slip "no permission needed"; the question gets a GREEN tick.
2. LECTURE 18 · 19–21 (APIs). The trip shrinks away; V2 appears with its cluster drawn as "your
   laptop" (the rest ghosted) and the struck "App is ready!" with "Well not really, we need to build
   it". The laptop rises back into the BLUE cluster and the lecture's layers return; NGINX, the
   registry and the persistent disk turn GREY dashed, one per phrase; a GREY dashed chip "Lectures
   19–22" and a GREEN tick "the pieces" under the struck chip.
3. LECTURE 18 · slide 46 (APIs), then 18 · 40–41 (Frontend). The map fades; a GREY card "your project:
   draw your solution and technical architecture", then two GREY repo chips "App Building Crash Course",
   "App Building Template" (names only).
4.–8. LECTURE off. "Test yourself" (YELLOW heading, "question k of 5 · answers in exercises.md"), one
   YELLOW question card at a time with a small text-free picture that pulses on its phrase: V1 outline
   (the browser pulses) · V3 icon (app card, socket, uvicorn in turn) · V6's two lamps · two API copies
   and one GREEN chat file (the copies, then the file) · the Vite and nginx couriers and a permission
   slip + GREY chip "answers: exercises.md". Fade out; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ the real names (checked)
E04 = capture("e04")
VOLUME = "cheese-app-frontend-react-node_modules"
assert any(s.split()[-1:] == [VOLUME] for s in E04.lines), E04.lines
assert any(s.startswith("chromadb/chroma") for s in E04.lines), E04.lines
assert any(s.startswith("cheese-app-") for s in E04.lines), E04.lines

STRIP_Q = "From 3000 to 9000: who carried it?"          # S01's strip form of the hook's card
TOP = 3.56

QUESTIONS = (
    "Trace one newsletters request on main\nthrough the lecture's steps. Which container\n"
    "does the browser talk to, and at which\nstep does the API's port come in?",
    "What do api.service:app, --host 0.0.0.0\nand --reload each do, and why does\n/square_root answer 307?",
    "/healthz vs /readyz: what does each one\ncheck in this API?",
    "Where does a chat stay between two\nmessages, and why can any copy\nof the API answer it?",
    "Which file decides where /api goes in\ndevelopment, which in production, and\nwhy did the 2025 API need CORSMiddleware\n"
    "while main's does not?",
)


# ------------------------------------------------------------------ the checklist card
def parts_row(*parts, size: float = 20) -> VGroup:
    """A row of pieces: 'text' label INK; ('text', 'm') mono INK; a piece whose text starts with
    '^' is glued to the one before (no space: punctuation, brackets)."""
    ms, glue = [], []
    for p in parts:
        s, kind = (p, "l") if isinstance(p, str) else p
        g = s.startswith("^")
        s = s[1:] if g else s
        ms.append(mono(s, size, INK) if kind == "m" else label(s, size, INK))
        glue.append(g)
    row = VGroup(*ms)
    for a, b, g in zip(ms, ms[1:], glue[1:]):
        b.next_to(a, RIGHT, buff=0.04 if g else 0.12)
    return row


ITEMS = (
    [parts_row(("Ctrl-C", "m"), "and", ("exit", "m"), "in every container terminal", "(", ("^--rm", "m"),
               "deletes them)")],
    [parts_row(("docker compose down", "m"), "·", ("src/vector-db", "m"), "^, or", ("src", "m"),
               "if you used Compose")],
    [parts_row("branch 2025: stop its Chroma,", ("git switch main", "m"))],
    [parts_row(("docker system prune", "m"), "· check its list first (other projects too)")],
    [parts_row("what prune keeps:", ("docker volume rm " + VOLUME, "m")),
     parts_row(("docker image ls", "m"), "^, then remove the", ("cheese-app-*", "m"), "and", ("chromadb", "m"),
               "images"),
     parts_row("by name if you need the space")],
    [parts_row("your key stays in", ("secrets/", "m"), "^, outside every repository")],
)


def tick_box(h: float = 0.32) -> VGroup:
    return RoundedRectangle(width=h, height=h, corner_radius=0.05, stroke_color=S.GREY, stroke_width=2.5)


def checklist() -> VGroup:
    """The clean-up card: GOLD frame, GREY head, six items (a tick box each, item 5 three rows, the
    GOLD disk chip after its last row). .frame .head .boxes .items .disk"""
    head = label("Clean up · all done once already", 22, S.GREY)
    items, boxes = [], []
    for rows in ITEMS:
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bx = tick_box()
        bx.next_to(rows[0], LEFT, buff=0.22)
        items.append(VGroup(bx, body))
        boxes.append(bx)
    col = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    dk = disk_chip()
    dk.next_to(ITEMS[4][2], RIGHT, buff=0.3)
    # the chip is taller than a text row: item 6 moves down so the chip clears its text
    items[5].shift(DOWN * max(0, items[5].get_top()[1] - dk.get_bottom()[1] + 0.12))
    inner = VGroup(head, col).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    w = max(inner.width, VGroup(col, dk).width) + 0.7
    fr = outline_box(w, inner.height + 0.6, COST, solid=True, fill_opacity=0.08)
    fr.fill.set_fill(S.GREY_DARKER, 1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    dk.next_to(ITEMS[4][2], RIGHT, buff=0.3)
    assert dk.get_bottom()[1] > items[5].get_top()[1] + 0.1, (dk.get_bottom(), items[5].get_top())
    g = VGroup(fr, head, *items)
    g.frame, g.head, g.items, g.boxes, g.disk = fr, head, items, boxes, dk
    return g


# ------------------------------------------------------------------ V2 with S02's layout fixes
class RecapMap(ArchitectureMap):
    """V2 as S02 draws it (the shared piece is not edited): the GCP line below the 'HTTPS 443'
    labels, Colab's box fits its words, the cluster's title clear of NGINX, the port labels beside
    NGINX, the users' arrow ending on the cluster's edge. Plus this scene's states: start as S02 left
    it (laptop(): the cluster is 'your laptop', the rest ghosted, the struck 'App is ready!' shown) and
    rise(scene) back into the cluster; dash(scene, key) marks one future part GREY dashed."""

    BOX = {"nginx": (4.1, -0.22), "app": (2.95, -1.22), "api": (5.2, -1.22), "vdb": (5.2, -2.42)}
    GCP_TOP = 0.92

    def __init__(self, **kw):
        super().__init__(built=True, **kw)
        e = self.layers["edges"]                  # the users' arrow ends on the cluster's top edge
        a = self.layers["people"].users.get_bottom()
        new = arrow(a, np.array([a[0], self.cluster_frame.get_top()[1], 0]), S.GREY)
        e.users_edge.become(new)
        e.users_label.next_to(new, LEFT, buff=0.12)

    def _make(self, name: str):
        sz, p = self.size, self.p
        if name == "tools":
            g = super()._make(name)
            for b in (g.colab, g.github):
                fr = box(2.3, 0.62, LAPTOP, fill_opacity=0.1).move_to(p(-5.4, b[0].get_y() - self.ref.get_y()))
                b.submobjects[0] = fr
                b[1].move_to(fr)
            return g
        if name == "gcp":
            fr = box(10.6, self.GCP_TOP + 3.3, CLOUD, dashed=True).move_to(p(1.2, (self.GCP_TOP - 3.3) / 2))
            t = label("GCP", sz, CLOUD).move_to(fr.get_corner(DL) + np.array([0.4, 0.25, 0]))
            return VGroup(fr, t)
        if name == "edges":
            g = super()._make(name)
            y = self.ref.get_y() + 1.17
            for e, lb in ((g[0], g[3]), (g[1], g[4])):
                lb.move_to([e.get_right()[0] + 0.12 + lb.width / 2, y, 0])
            return g
        if name == "cluster":
            g = super()._make(name)
            fr = self.cluster_frame
            fr.stretch_to_fit_height(4.0).move_to(p(4.075, -1.15))
            t1 = VGroup(label("compute instance /", 20, S.GREY), label("Kubernetes cluster", 20, S.GREY)).arrange(
                DOWN, buff=0.04)
            t1.next_to(fr.get_top(), DOWN, buff=0.1)
            g.submobjects[1] = t1
            self.cluster_title = t1
            ng0 = self.boxes["nginx"]
            ng = cbox(["NGINX"], 1.4, ng0.frame.height, size=sz, mono_font=False).move_to(ng0)
            ng.name.move_to(ng.frame)
            g.submobjects[g.submobjects.index(ng0)] = ng
            self.boxes["nginx"] = ng
            for k, side in (("3000", LEFT), ("9000", RIGHT)):
                old = self.ports[k]
                new = label(f"HTTP {k}", sz, ROUTE).next_to(ng, side, buff=0.1)
                g.submobjects[g.submobjects.index(old)] = new
                self.ports[k] = new
            return g
        if name == "disk":                        # lower, so the struck chip's caption and tick fit above
            g = super()._make(name).shift(DOWN * 0.4)
            x0, x1 = g[0].get_right()[0] + 0.1, p(1.7, 0)[0]     # 'NFS' clear of the disk's dashed outline
            g[2].set_x((x0 + x1) / 2)
            assert g[2].get_left()[0] > x0, (g[2].get_left(), x0)
            return g
        return super()._make(name)

    def laptop(self):
        """S02's end state, built without playing: the other layers ghosted (saved for rise()), the
        cluster frame GREY 'your laptop', the struck 'App is ready!' with its caption."""
        for n in self.shown:
            if n != "cluster":
                self._saved[n] = self.layers[n].copy()
                self.layers[n].fade(0.8)
        self.cluster_frame.set_stroke(LAPTOP).set_fill(S.BG, 1)
        t = label("your laptop", 22, LAPTOP).move_to(self.cluster_title)
        cl = self.layers["cluster"]
        cl.submobjects[cl.submobjects.index(self.cluster_title)] = t
        self.cluster_title = t
        c = ok_chip("App is ready!", size=22).move_to(self.p(*self.READY_C))
        c.box.set_fill(S.BG, 1)
        st = strike(c, ERR)
        cap = VGroup(label("Well not really,", 20, S.GREY), label("we need to build it", 20, S.GREY)).arrange(
            DOWN, buff=0.06).next_to(c, DOWN, buff=0.12)
        self.ready_chip, self.not_ready_mark = c, VGroup(st, cap)
        self.add(c, st, cap)
        # S13's end state: NGINX's slot holds the GREY 'vector-db-loader · exited 0', the two NGINX
        # edges and their HTTP 3000 / 9000 labels are gone (dev has no NGINX). NGINX and its edges are
        # kept aside: rise() puts NGINX back, dash('nginx') brings its edges back with it, GREY.
        ng = self.boxes["nginx"]
        e1, e2 = cl.submobjects[2], cl.submobjects[3]
        self._ng_parts = (e1, e2, self.ports["3000"], self.ports["9000"])
        for m in (ng, *self._ng_parts):
            cl.remove(m)
        ld = cbox(["vector-db-loader"], mono("vector-db-loader", self.size).width + 0.35, ng.frame.height,
                  size=self.size)
        ld.name.move_to(ld.frame).set_color(S.GREY)
        ld.frame.set_stroke(S.GREY, width=3)
        ld.move_to(ng)
        ex = label("exited 0", 20, S.GREY).next_to(ld, DOWN, buff=0.06)
        self.loader = VGroup(ld, ex)
        cl.add(self.loader)
        ng.frame.set_stroke(S.GREY, width=3).set_fill(S.BG, 1)
        ng.name.set_color(S.GREY)
        return self

    def rise(self, scene, run_time: float = 1.2):
        """PLAYS: the laptop becomes the BLUE cluster again (title back), the other layers return."""
        anims = self._restore_anims()
        anims.append(self.cluster_frame.animate.set_stroke(CLOUD).set_fill(tint(CLOUD, 0.06), 1))
        boxes = [b for k, b in self.boxes.items() if k != "nginx"]      # the four from S13 (loader too)
        boxes.insert(0, self.loader)
        anims.append(LaggedStart(*[b.animate(rate_func=there_and_back).shift(UP * 0.18) for b in boxes],
                                 lag_ratio=0.15))
        scene.play(*anims, run_time=run_time * 0.7)
        self.heal(scene)
        # the loader has done its job; NGINX, the production front, takes its slot GREY (not built yet)
        ng, ld = self.boxes["nginx"], self.loader
        self._detach(ld)
        scene.add(ld)
        self.show(scene, ng, anims=[FadeOut(ld, shift=DOWN * 0.1), FadeIn(ng, shift=DOWN * 0.1)],
                  run_time=run_time * 0.35, into=self.layers["cluster"])
        scene.remove(ld)
        new_t = VGroup(label("compute instance /", 20, S.GREY), label("Kubernetes cluster", 20, S.GREY)
                       ).arrange(DOWN, buff=0.04).move_to(self.cluster_title)
        self.cluster_title = self.swap(scene, self.cluster_title, new_t, run_time=run_time * 0.3)

    def dash(self, scene, key: str, run_time: float = 0.6):
        """PLAYS: a future part (a cluster box key or a layer name) turns GREY and faded inside a GREY
        dashed outline (L19–L22 build it). Returns the outline."""
        b = self.boxes.get(key)
        if b is not None:                         # the box's own outline becomes dashed
            r = ring(b.frame, PAST, buff=0, stroke=3, dashed=True)
            dim = [b.frame.animate.set_stroke(opacity=0).set_fill(S.BG, 1), b.name.animate.set_color(S.GREY)]
            if key == "nginx" and getattr(self, "_ng_parts", None):   # its two edges return, GREY
                parts = [m.set_color(S.GREY).set_opacity(0.6) for m in self._ng_parts]
                self._ng_parts = None
                cl = self.layers["cluster"]
                self.show(scene, r, *parts, anims=[*dim, Create(r), *[FadeIn(m) for m in parts]],
                          run_time=run_time, into=cl)
                return r
        else:                                     # a dashed outline round the part (the disk: not its NFS edge)
            m = self.layers[key]
            r = ring(m[0] if key == "disk" else m, PAST, buff=0.05, stroke=3, dashed=True)
            dim = [m.animate.set_color(S.GREY).fade(0.5)]
        self.show(scene, r, anims=[*dim, Create(r)], run_time=run_time)
        return r


def one_slide(slide: str) -> VGroup:
    """lref() for ONE slide (S02's helper): lecture_ref() reads 'slides 46 (APIs)' when the deck name
    follows the number; same tag, same place, 'slide 46'."""
    g = lref(slide)
    fixed = tag(f"Lecture 18 · slide {slide}", S.GREY)
    return fixed.move_to([6.6 - fixed.width / 2, g.get_y(), 0])


# ------------------------------------------------------------------ small pictures for the questions
def copies_icon() -> VGroup:
    """Two API copies (V3 icons) and one GREEN chat file between them, GREEN lines. .copies .file"""
    a = server_app_icon(0.8).move_to([0, 0.75, 0])
    b = server_app_icon(0.8).move_to([0, -0.75, 0])
    f = file_icon(None, OWN, h=0.9).move_to([1.9, 0, 0])
    la = Line(a.get_right(), f.get_left() + UP * 0.12, color=OWN, stroke_width=3)
    lb = Line(b.get_right(), f.get_left() + DOWN * 0.12, color=OWN, stroke_width=3)
    g = VGroup(la, lb, a, b, f)
    g.copies, g.file = VGroup(a, b), f
    return g


def courier_icon() -> VGroup:
    """The two couriers and the permission slip. .vite .nginx .slip"""
    v = courier_chip("Vite", size=26)
    n = courier_chip("nginx", size=26)
    s = slip_glyph(0.85)
    g = VGroup(v, n, s).arrange(DOWN, buff=0.4)
    g.vite, g.nginx, g.slip = v, n, s
    return g


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 9, len(SAY)

        # ========================================================== 0. the clean-up checklist
        ck = checklist()
        ck.move_to([0, 0.1, 0])
        assert ck.get_top()[1] < SAFE_Y and ck.get_bottom()[1] > -SAFE_Y, (ck.get_top(), ck.get_bottom())
        assert ck.disk.get_right()[0] < ck.frame.get_right()[0] - 0.15, (ck.disk.get_right(), ck.frame.get_right())
        assert ck.frame.width < 2 * SAFE_X, ck.frame.width
        cues = ("Exit every container", "compose down", "back to main", "prune after checking",
                "then remove the node modules", "Your key stays")
        ticks = []
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ck.frame), FadeIn(ck.head, shift=DOWN * 0.1), *[Create(b) for b in ck.boxes],
                      run_time=0.8)
            for k, cue in enumerate(cues):
                vo.wait_until(cue)
                body = ck.items[k][1]
                anims = [FadeIn(body, shift=RIGHT * 0.15)]
                if k == 4:
                    anims.append(FadeIn(ck.disk, scale=0.9))
                self.play(*anims, run_time=0.45)
                t = check_glyph(0.3).move_to(ck.boxes[k])
                ticks.append(t)
                self.play(Create(t), ck.boxes[k].animate.set_stroke(OWN), run_time=0.3)
            self.play(Indicate(ck.items[5][1], color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 1. the whole trip on main
        sq = question_card(STRIP_Q, size=22)
        sq.move_to([-6.5 + sq.width / 2, TOP - sq.height / 2, 0])
        tr = RequestTrace("localhost:3000/newsletters", rows=("front", "api"), front="react", courier="Vite")
        tr.shift(UP * 0.3)
        net = tr.net
        ill = illustration_tag().next_to(tr.browser, UP, buff=0.12).align_to(tr.browser, LEFT)
        ng = VGroup(label("in production:", 20, S.GREY), courier_chip("nginx")).arrange(RIGHT, buff=0.15)
        ng.next_to(net.frame, UP, buff=0.12).align_to(net.boxes["front"].frame, RIGHT)
        assert ng.get_top()[1] < TOP - sq.height - 0.05 or ng.get_left()[0] > sq.get_right()[0] + 0.2, ng.get_top()
        oc = origin_chips("http", "localhost", "3000")
        oc_head = label("page and calls:", 20, ROUTE)
        org = VGroup(oc_head, oc).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        org.next_to(tr.browser, DOWN, buff=0.2).align_to(tr.browser, LEFT)
        sg = slip_glyph(0.45)
        sg_x = Line(sg.get_corner(UL) + np.array([-0.06, 0.06, 0]), sg.get_corner(DR) + np.array([0.06, -0.06, 0]),
                    color=S.GREY, stroke_width=4)
        nn = label("no permission needed", 20, S.GREY)
        slip = VGroup(VGroup(sg, sg_x), nn).arrange(RIGHT, buff=0.15)
        slip.next_to(org, DOWN, buff=0.18).align_to(org, LEFT)
        leaf = VGroup(label("router:", 20, S.GREY), route_chip("/api/newsletters")).arrange(RIGHT, buff=0.15)
        api_in = net.inner["api"]
        leaf.next_to(net.boxes["api"].frame, DOWN, buff=0.35).align_to(api_in, RIGHT)
        stem = Line(api_in.get_bottom(), [api_in.get_x(), leaf.get_top()[1], 0], color=ROUTE, stroke_width=3)
        assert leaf.get_bottom()[1] > net.frame.get_bottom()[1] + 0.35, (leaf.get_bottom(), net.frame.get_bottom())
        ok = check_glyph(0.4).next_to(sq, RIGHT, buff=0.2)
        assert ill.get_top()[1] < sq.get_bottom()[1] - 0.05, (ill.get_top(), sq.get_bottom())
        assert tr.get_top()[1] < sq.get_bottom()[1] - 0.05 or net.frame.get_left()[0] > sq.get_right()[0] + 0.1
        assert ng.get_bottom()[1] > -SAFE_Y and slip.get_bottom()[1] > -SAFE_Y, (ng.get_bottom(), slip.get_bottom())
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(ck, ck.disk, *ticks)), run_time=0.5)
            self.play(FadeIn(sq, shift=DOWN * 0.15), FadeIn(tr), FadeIn(ill), run_time=0.8)
            vo.wait_until("the browser talks only to 3000")
            tr.hop(self, 1, "front", run_time=0.5)
            tr.hop(self, 2, "front", run_time=0.4)
            tr.hop(self, 3, "front", run_time=0.4)
            vo.wait_until("Inside, Vite in development")
            self.play(Indicate(net.courier, color=TOOL, scale_factor=1.25), run_time=0.6)
            net.heal(self)
            vo.wait_until("or nginx in production")
            self.play(FadeIn(ng, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("carries slash api by name")
            bd = tr._badge(3.5).move_to([net.p(net.CABLE_X, 0)[0] + 0.38,
                                         (net.row_y("front") + net.row_y("api")) / 2, 0])
            tr.set_caption(self, HOP_TEXT[3.5])
            tr._mark(self, [bd], [FadeIn(bd)], 0.3)
            net.courier_walk(self, text="/api/…", run_time=1.2)
            tr._walked = True
            vo.wait_until("where a router runs the function")
            tr.hop(self, 4, "api", run_time=0.6)
            net.show(self, stem, leaf, anims=[Create(stem), FadeIn(leaf, shift=DOWN * 0.1)], run_time=0.5)
            vo.wait_until("The JSON comes back the same way")
            tr.hop(self, 5, "front", run_time=0.6)
            tr.hop(self, 6, run_time=0.5)
            vo.wait_until("one origin")
            self.play(FadeIn(org, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(oc.port, color=ROUTE, scale_factor=1.2), net.door_pulse("front", ROUTE),
                      run_time=0.7)
            net.heal(self)
            vo.wait_until("no permission needed")
            self.play(FadeIn(slip, shift=UP * 0.1), run_time=0.4)
            self.play(Create(ok), sq.frame.animate.set_stroke(OWN), run_time=0.5)

        # ========================================================== 2. the lecture's blueprint, one last time
        ref2 = lref("19–21 (APIs)")
        m = RecapMap().laptop()
        with self.voiceover(SAY[2]) as vo:
            # the trip shrinks away while the blueprint comes in (no blank frame between them); the
            # answered hook card stays until the boxes rise
            self.play(FadeOut(VGroup(tr, ill, ng, org, slip), scale=0.5), FadeIn(m), FadeIn(ref2), run_time=1.0)
            self.remove(tr, ill, ng, org, slip)
            vo.wait_until("Your four boxes rise")
            self.play(FadeOut(VGroup(sq, ok), shift=UP * 0.15), run_time=0.3)
            self.remove(sq, ok)
            m.rise(self, run_time=1.4)
            vo.wait_until("NGINX in front")
            m.dash(self, "nginx", run_time=0.5)
            vo.wait_until("the registry")
            m.dash(self, "registry", run_time=0.5)
            vo.wait_until("and the persistent disk")
            m.dash(self, "disk", run_time=0.5)
            vo.wait_until("the next lectures build them")
            reg = m.layers["registry"]
            ch = dashed_chip("Lectures 19–22").next_to(reg, LEFT, buff=0.2).align_to(reg, DOWN)
            m.show(self, ch, run_time=0.4)
            m.tick_build(self, run_time=0.5)

        # ========================================================== 3. your project (A46, B40–B41)
        ref46 = one_slide("46 (APIs)")
        ref40 = lref("40–41 (Frontend)")
        pc = card(["your project: draw your solution", "and technical architecture"], S.GREY, size=32)
        repos = VGroup(grey_chip("App Building Crash Course", size=28), grey_chip("App Building Template", size=28)
                       ).arrange(RIGHT, buff=0.6)
        VGroup(pc, repos).arrange(DOWN, buff=0.6).move_to([0, 0.2, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(m), ReplacementTransform(ref2, ref46), run_time=0.6)
            self.play(FadeIn(pc, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("draw your solution")
            self.play(Indicate(pc.body, color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("and points to a crash course")
            self.play(ReplacementTransform(ref46, ref40), FadeIn(repos[0], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and a template repository")
            self.play(FadeIn(repos[1], shift=UP * 0.15), run_time=0.5)

        # ========================================================== 4-8. test yourself
        head = label("Test yourself", 30, TURN).move_to([-6.4, 2.75, 0], aligned_edge=LEFT)
        counters = [label(f"question {k + 1} of 5 · answers in exercises.md", 22, S.GREY) for k in range(5)]
        for c in counters:
            c.next_to(head, RIGHT, buff=0.4).align_to(head, DOWN)
        qcards = [question_card(q, 26, card_w=8.4).move_to([-2.2, 0.15, 0]) for q in QUESTIONS]
        IX, IY = 4.4, 0.15
        ti = trace_icon(1.3).move_to([IX, IY, 0])
        si = server_app_icon(2.0).move_to([IX, IY, 0])
        li = lamp_pair(("green", "amber")).move_to([IX, IY, 0])
        ci = copies_icon().move_to([IX, IY, 0])
        vi = courier_icon().move_to([IX, IY, 0])
        icons = [ti, si, li, ci, vi]
        for q, ic in zip(qcards, icons):
            assert q.get_right()[0] < ic.get_left()[0] - 0.2 and ic.get_right()[0] < 6.55, (q.get_right(), ic.get_corner(DR))
            assert q.get_left()[0] > -SAFE_X, q.get_left()
        ans = grey_chip("answers: exercises.md").next_to(qcards[4], DOWN, buff=0.35)
        assert ans.get_bottom()[1] > -SAFE_Y, ans.get_bottom()
        cur = None
        for k in range(5):
            with self.voiceover(SAY[4 + k]) as vo:
                if k == 0:
                    self.play(FadeOut(VGroup(pc, repos)), FadeOut(ref40), FadeIn(head, shift=DOWN * 0.1),
                              FadeIn(counters[0]), run_time=0.7)
                    vo.wait_until("One:")
                    self.play(FadeIn(qcards[0], shift=UP * 0.15), FadeIn(ti), run_time=0.6)
                else:
                    self.play(FadeOut(cur[0], shift=LEFT * 0.4), FadeOut(cur[1]), FadeOut(counters[k - 1]),
                              run_time=0.35)
                    self.play(FadeIn(qcards[k], shift=LEFT * 0.4), FadeIn(icons[k]), FadeIn(counters[k]),
                              run_time=0.45)
                cur = (qcards[k], icons[k])
                if k == 0:
                    vo.wait_until("trace a newsletters request")
                    self.play(Indicate(qcards[0].body[0], color=TURN, scale_factor=1.05), run_time=0.7)
                    vo.wait_until("Which container does the browser")
                    self.play(Indicate(VGroup(ti[0], ti[1]), color=TURN, scale_factor=1.2), run_time=0.8)
                    vo.wait_until("and where does port 9000")
                    self.play(Indicate(ti[4], color=TURN, scale_factor=1.2), run_time=0.8)
                elif k == 1:
                    vo.wait_until("api dot service colon app")
                    self.play(Indicate(si[2], color=TURN, scale_factor=1.3), run_time=0.7)
                    vo.wait_until("host 0.0.0.0")
                    self.play(Indicate(si[3], color=TURN, scale_factor=3.0), run_time=0.7)
                    vo.wait_until("and reload")
                    self.play(si[1].animate(rate_func=there_and_back).set_stroke(TURN, width=7), run_time=0.8)
                    vo.wait_until("why does square root")
                    self.play(Indicate(qcards[1].body[2], color=TURN, scale_factor=1.06), run_time=0.8)
                    vo.wait_until("without a slash")
                    self.play(Circumscribe(qcards[1].body[2], color=TURN, buff=0.08), run_time=1.0)
                    self.play(Indicate(si[2], color=TURN, scale_factor=1.3), run_time=0.7)
                elif k == 2:
                    vo.wait_until("healthz and")
                    self.play(Indicate(li[0], color=OWN, scale_factor=1.2), run_time=0.7)
                    vo.wait_until("readyz.")
                    self.play(Indicate(li[1], color=AMBER, scale_factor=1.2), run_time=0.7)
                    vo.wait_until("What does each one check")
                    self.play(Indicate(qcards[2].body[1], color=TURN, scale_factor=1.06), run_time=0.8)
                elif k == 3:
                    vo.wait_until("where does a chat stay")
                    self.play(Indicate(ci.file, color=OWN, scale_factor=1.2), run_time=0.7)
                    vo.wait_until("why can any copy")
                    self.play(each(list(ci.copies), TURN, scale=1.15, lag=0.4), run_time=1.0)
                    self.play(Indicate(ci.file, color=OWN, scale_factor=1.2), run_time=0.6)
                else:
                    vo.wait_until("goes in development")
                    self.play(Indicate(vi.vite, color=TOOL, scale_factor=1.2), run_time=0.6)
                    vo.wait_until("which in production")
                    self.play(Indicate(vi.nginx, color=TOOL, scale_factor=1.2), run_time=0.6)
                    vo.wait_until("and why did last year")
                    self.play(Indicate(vi.slip, color=ROUTE, scale_factor=1.3), run_time=0.7)
                    self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.5)
        self.play(Indicate(ans, color=INK, scale_factor=1.06), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
