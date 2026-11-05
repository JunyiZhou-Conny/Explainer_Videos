"""S02 · The blueprint, and your folders (AC215 L18). No tracker until beat 5.
Lecture: 18 · 4–5, 7–13, 14–19, 43 (APIs).

Beats (script.md "## S02", one voiceover block each):
0. lecture_ref(18, "4–5 (APIs)"). A4 redrawn: a wide GREY arrow POC · Prototype · MVP with dashed
   phase lines, the bar "Build Cheese App" under MVP with a dashed YELLOW box. It slides up; A5's
   board builds under it: left panel "ML pipeline" (Data Collector → Data Processor → Model Training →
   Model Deploy, Vector DB under Model Deploy) with a GREEN tick; right panel "App Dev" with two
   WHITE-outlined tiles "Backend API" and "Frontend", pulsing YELLOW on "the app".
1. lecture_ref "7–13 (APIs)". The board clears. V2 ArchitectureMap builds one layer per phrase: title
   chip, the people bands, GitHub + Colab, Vertex AI with Gemini, the GCP boundary and the GREY App
   box; on "protocol and port" the PINK edge labels (HTTPS 443, HTTP/HTTPS 80).
2. lecture_ref "14–19 (APIs)". Bucket, registry, persistent disk (+ NFS), then the cluster replaces
   the App box: NGINX, Cheese App 3000, API Service 9000, Vector DB 8000, each flashed on its phrase.
3. Lecture tag off. ArchitectureMap.to_laptop: the rest of the map ghosts, the cluster frame turns
   GREY and is titled "your laptop" (the four boxes keep their ports); the ghosted title chip gives
   way to a GREY chip "the same building blocks have AWS and Azure names (slide 22)".
4. lecture_ref "43 (APIs)". The laptop frame grows into a frame around the viewer's real folders
   (p06: 2–4, 7–8, 11, 17–18, 24–30, drawn as a tree): cheese-app-v1/ (README.md, src/ with
   api-service/, frontend-simple/ and a GREY chip "+ 7 empty folders"), cheese-app-v2/ (README.md,
   src/ with api-service/, docker-compose.yml, frontend-react/, vector-db/), and persistent-folder/,
   secrets/ beside them. GREEN "Git root" brackets on the two clones, src's folders flash, secrets/
   gets the GREY label "secrets outside the Git folder"; a GREY card "v1 keeps empty folders for the
   slide's services · v2 holds only the three it runs"; v2's three services flash.
5. Lecture tag off. Tracker SE 1. A 6-row terminal `laptop` types p01 (folds; row tag
   `extra · our spelling`) → p01:2; tracker SE 2; p02 → p02:2. A README card (README.md · line 18)
   "Clone or download from here" above; YELLOW `▶ your turn` on the title bar.
6. Tracker SE 3. The terminal shrinks to a 3-row strip and types `mkdir -p secrets persistent-folder`
   (`extra · our spelling`) → no output. Above it persistent-folder/ and secrets/ with a GREY owner
   chip "student" each and their `ls -la` lines (p06:34, 39; owner YELLOW); GREY dashed ghost "root"
   chips appear and are struck RED with "on Linux, Docker would create them as root"; ml-workflow.json
   slides into secrets/.
7. Tracker SE 3 · extra. The terminal grows to 6 rows and types p04's line 1 (extra; folds) →
   p04: 2–4; 447b5c3 on lines 2 and 4 YELLOW, refs/heads/2025 PINK. Above: v2's main line, whose
   YELLOW 'main' pointer moves twice, and a branch 2025; a GREY folder frontend-simple drops off main
   onto 2025. Everything fades; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene
from explainer.devops import file_tree, tag

from common import *  # noqa: F401,F403

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources (checked)
P01, P02, P04, P05, P06 = (capture(k) for k in ("p01", "p02", "p04", "p05", "p06"))
assert P01.cmd == "git clone https://github.com/dlops-io/cheese-app-v1.git", P01.cmd
assert P02.cmd == "git clone https://github.com/dlops-io/cheese-app-v2.git", P02.cmd
assert P01.at(2) == ["Cloning into 'cheese-app-v1'..."] and P02.at(2) == ["Cloning into 'cheese-app-v2'..."]
assert P05.cmd == "mkdir -p secrets persistent-folder" and P05.lines == [], P05.lines
assert P04.cmd.startswith("git ls-remote https://github.com/dlops-io/cheese-app-v2.git;"), P04.cmd
assert P04.line(2).startswith("447b5c3") and P04.line(2).endswith("HEAD"), P04.line(2)
assert P04.line(3).startswith("14f2a14") and P04.line(3).endswith("refs/heads/2025"), P04.line(3)
assert P04.line(4).startswith("447b5c3") and P04.line(4).endswith("refs/heads/main"), P04.line(4)
# the tree of beat 4 (p06 file lines: name → line)
TREE_LINES = {3: "./cheese-app-v1", 4: "./cheese-app-v1/README.md", 7: "./cheese-app-v1/src",
              8: "./cheese-app-v1/src/api-service", 11: "./cheese-app-v1/src/frontend-simple",
              17: "./cheese-app-v2", 18: "./cheese-app-v2/README.md", 24: "./cheese-app-v2/src",
              25: "./cheese-app-v2/src/api-service", 26: "./cheese-app-v2/src/docker-compose.yml",
              27: "./cheese-app-v2/src/frontend-react", 28: "./cheese-app-v2/src/vector-db",
              29: "./persistent-folder", 30: "./secrets", 31: "./secrets/ml-workflow.json"}
for n, s in TREE_LINES.items():
    assert P06.line(n) == s, (n, P06.line(n))
V1_EMPTY = [P06.line(n).rsplit("/", 1)[1] for n in (9, 10, 12, 13, 14, 15, 16)]
assert V1_EMPTY == ["data-collector", "data-processor", "model-deploy", "model-training", "newsletter",
                    "podcast", "vector-db"], V1_EMPTY
LS_PF, LS_SEC = P06.line(34), P06.line(39)
assert LS_PF.split()[2:4] == ["student", "student"] and LS_PF.endswith(" ."), LS_PF
assert LS_SEC.split()[2:4] == ["student", "student"] and LS_SEC.endswith(" ."), LS_SEC
assert P06.line(32) == "persistent-folder:" and P06.line(37) == "secrets:"
CARD_18 = md_plain(readme_lines(18, 18, V1)).removeprefix("• ")   # the README's bullet dropped
assert CARD_18 == "Clone or download from here", CARD_18

TREE_SIZE = 20
GCP_RIGHT = 1.55        # S02 beat 3: the GCP boundary's right edge once the cluster has left it


def grey_glyphs(tree):
    """Folders on the laptop are GREY (BLUE is the cloud); names are WHITE."""
    for r in tree.rows:
        r.glyph.set_color(S.GREY)
        r.name_text.set_color(INK)
    return tree


def tile(rows, tile_w: float, tile_h: float, color=S.GREY, size: float = 20, fill=None):
    """A slide tile: a rounded box with one or two rows of label text."""
    fr = RoundedRectangle(width=tile_w, height=tile_h, corner_radius=0.1, stroke_color=color,
                          stroke_width=3).set_fill(fill or tint(color, 0.12), 1)
    t = VGroup(*[label(s, size, INK) for s in rows]).arrange(DOWN, buff=0.06).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def flash_box(b, color=TURN):
    """ANIM: a box's outline thickens in `color` and back, its words flash (a filled box is never
    Indicated whole: its fill would turn solid and hide the words)."""
    return AnimationGroup(b.frame.animate(rate_func=there_and_back).set_stroke(color, width=7),
                          Indicate(b[1] if not hasattr(b, "name") else b.name, color=color, scale_factor=1.08))


class BlueprintMap(ArchitectureMap):
    """V2 with this scene's layout fixes (the shared piece is not edited; see the report): the GCP
    line sits below the 'HTTPS 443' labels, Colab's box fits its words, the cluster's title is clear of
    NGINX, its port labels are two rows inside the frame, and the users' arrow ends on
    the cluster's edge (the opaque cluster used to hide it and its 'HTTP/HTTPS 80' label)."""

    BOX = {"nginx": (4.1, -0.22), "app": (2.95, -1.22), "api": (5.2, -1.22), "vdb": (5.2, -2.42)}
    GCP_TOP = 0.92

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
            assert t1.get_bottom()[1] > self.boxes["nginx"].get_top()[1] + 0.05, (t1.get_bottom(), self.boxes["nginx"].get_top())
            g.submobjects[1] = t1
            self.cluster_title = t1
            ng0 = self.boxes["nginx"]
            ng = cbox(["NGINX"], 1.4, ng0.frame.height, size=sz, mono_font=False).move_to(ng0)
            ng.name.move_to(ng.frame)
            g.submobjects[g.submobjects.index(ng0)] = ng
            self.boxes["nginx"] = ng
            for k, side in (("3000", LEFT), ("9000", RIGHT)):     # beside NGINX, above their arrows
                old = self.ports[k]
                new = label(f"HTTP {k}", sz, ROUTE).next_to(ng, side, buff=0.1)
                assert fr.get_left()[0] + 0.05 < new.get_left()[0] and new.get_right()[0] < fr.get_right()[0] - 0.05
                g.submobjects[g.submobjects.index(old)] = new
                self.ports[k] = new
            return g
        return super()._make(name)

    def layer(self, scene, name: str, run_time: float = 0.9):
        if name != "cluster" or "app" not in self.layers:
            return super().layer(scene, name, run_time)
        g = self._make(name)
        self.layers[name] = g
        old = self.layers.pop("app")
        self.shown.remove("app")
        self._detach(old)
        scene.add(old)
        self.show(scene, g, anims=[FadeIn(g, lag_ratio=0.1), FadeOut(old)], run_time=run_time)
        scene.remove(old)
        if "edges" in self.layers:                 # the users' arrow now ends on the cluster's edge
            e = self.layers["edges"]
            a = self.layers["people"].users.get_bottom()
            new = arrow(a, np.array([a[0], self.cluster_frame.get_top()[1], 0]), S.GREY)
            scene.play(Transform(e.users_edge, new), e.users_label.animate.next_to(new, LEFT, buff=0.12),
                       run_time=0.4)
            self.heal(scene)
        self.shown.append(name)
        return g


def one_slide(slide: str) -> VGroup:
    """lref() for ONE slide: lecture_ref() reads 'slides 43 (APIs)' when the deck name follows the
    number (its one-slide test sees '43 (APIs)', not a digit); same tag, same place, 'slide 43'."""
    g = lref(slide)
    fixed = tag(f"Lecture 18 · slide {slide}", S.GREY)
    return fixed.move_to([6.6 - fixed.width / 2, g.get_y(), 0])


class Blueprint(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 8, len(SAY)

        # ========================================================== 0. where this lecture sits (A4, A5)
        ref0 = lref("4–5 (APIs)")
        x0, x1, x2, x3 = -5.6, -2.0, 1.75, 5.6
        body = Polygon([x0, 0.33, 0], [x3 - 0.45, 0.33, 0], [x3, 0, 0], [x3 - 0.45, -0.33, 0], [x0, -0.33, 0],
                       stroke_color=S.GREY, stroke_width=3).set_fill(tint(S.GREY, 0.14), 1)
        phases = VGroup(*[label(s, 22, INK).move_to([(a + b) / 2, 0, 0])
                          for s, a, b in (("POC", x0, x1), ("Prototype", x1, x2), ("MVP", x2, x3 - 0.3))])
        bar = tile(["Build Cheese App"], x3 - 0.35 - x2 - 0.15, 0.5, S.GREY).move_to(
            [(x2 + 0.15 + x3 - 0.35) / 2, -0.78, 0])
        here = DashedVMobject(RoundedRectangle(width=bar.width + 0.24, height=bar.height + 0.22,
                                               corner_radius=0.12), num_dashes=40).set_stroke(TURN, 3)
        here.move_to(bar)
        lines_ = VGroup(*[DashedLine([x, 0.33, 0], [x, -1.15, 0], dash_length=0.08).set_stroke(S.GREY, 2)
                          for x in (x1, x2)])
        road = VGroup(lines_, body, phases, bar, here)
        road.move_to([0, 0.5, 0])
        road_up = road.copy().shift(UP * (2.75 - road.get_top()[1]))

        # A5's board, under the roadmap once it has slid up
        top_b, bot_b = 0.95, -3.25
        left_p = outline_box(7.55, top_b - bot_b, S.GREY).move_to([(-6.45 + 1.1) / 2, (top_b + bot_b) / 2, 0])
        right_p = outline_box(4.95, top_b - bot_b, S.GREY).move_to([(1.5 + 6.45) / 2, (top_b + bot_b) / 2, 0])
        lt = label("ML pipeline", 22, INK).next_to(left_p.get_corner(UL), DR, buff=0.22)
        rt = label("App Dev", 22, INK).next_to(right_p.get_corner(UL), DR, buff=0.22)
        names = (("Data", "Collector"), ("Data", "Processor"), ("Model", "Training"), ("Model", "Deploy"))
        tiles = VGroup(*[tile(r, 1.5, 1.0) for r in names]).arrange(RIGHT, buff=0.32)
        tiles.move_to([left_p.get_center()[0], -0.55, 0])
        links = VGroup(*[Line(a.get_right(), b.get_left(), color=S.GREY, stroke_width=3).scale(0.7)
                         for a, b in zip(tiles[:-1], tiles[1:])])
        vdb = tile(("Vector", "DB"), 1.5, 1.0).next_to(tiles[3], DOWN, buff=0.45)
        link_v = Line(tiles[3].get_bottom(), vdb.get_top(), color=S.GREY, stroke_width=3).scale(0.7)
        tick = check_glyph(0.5).move_to(left_p.get_corner(UR) + np.array([-0.45, -0.4, 0]))
        app_tiles = VGroup(tile(["Backend API"], 2.05, 1.0, INK, fill=S.BG),
                           tile(["Frontend"], 2.05, 1.0, INK, fill=S.BG)).arrange(RIGHT, buff=0.35)
        app_tiles.move_to([right_p.get_center()[0], -0.95, 0])
        pipeline = VGroup(left_p, lt, tiles, links, vdb, link_v)
        assert pipeline.get_left()[0] >= -6.55 and right_p.get_right()[0] <= 6.55
        assert road_up.get_bottom()[1] > top_b + 0.1, road_up.get_bottom()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0), FadeIn(body), FadeIn(lines_), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in phases], lag_ratio=0.3), run_time=0.9)
            self.play(FadeIn(bar, shift=UP * 0.15), Create(here), run_time=0.7)
            vo.wait_until("The course project has its machine learning pipeline")
            self.play(Transform(road, road_up), run_time=0.7)
            self.play(FadeIn(left_p), FadeIn(lt), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in tiles],
                                                              lag_ratio=0.2), run_time=1.0)
            self.play(Create(links), FadeIn(vdb, shift=DOWN * 0.15), Create(link_v), run_time=0.6)
            self.play(Create(tick), run_time=0.4)
            vo.wait_until("what is still missing is the app")
            self.play(FadeIn(right_p), FadeIn(rt), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(t, scale=0.9) for t in app_tiles], lag_ratio=0.3), run_time=0.7)
            self.play(*[t.frame.animate.set_stroke(TURN, width=5) for t in app_tiles], run_time=0.4)
            vo.wait_until("a backend API")
            self.play(Indicate(app_tiles[0].text, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and a frontend")
            self.play(Indicate(app_tiles[1].text, color=TURN, scale_factor=1.12), run_time=0.6)
            self.play(*[t.frame.animate.set_stroke(INK, width=3) for t in app_tiles], run_time=0.3)

        # ========================================================== 1. the blueprint, layer by layer (A7–A13)
        ref1 = lref("7–13 (APIs)")
        m = BlueprintMap()
        board = VGroup(road, pipeline, tick, right_p, rt, app_tiles)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(board), ReplacementTransform(ref0, ref1), run_time=0.6)
            m.layer(self, "title", run_time=0.7)
            vo.wait_until("the blueprint")
            self.play(Indicate(m.layers["title"].text, color=INK, scale_factor=1.06), run_time=0.7)
            m.heal(self)
            vo.wait_until("Developers, users")
            m.layer(self, "people", run_time=0.8)
            vo.wait_until("GitHub and Colab")
            m.layer(self, "tools", run_time=0.7)
            vo.wait_until("Vertex AI inside")
            m.layer(self, "vertex", run_time=0.6)
            m.layer(self, "gcp", run_time=0.6)
            m.layer(self, "app", run_time=0.5)
            vo.wait_until("and every arrow is labeled")
            m.layer(self, "edges", run_time=0.9)
            vo.wait_until("its protocol and port")
            e = m.layers["edges"]
            self.play(LaggedStart(*[Indicate(lb, color=ROUTE, scale_factor=1.15) for lb in e[3:]], lag_ratio=0.3),
                      run_time=1.0)
            m.heal(self)

        # ========================================================== 2. bucket, registry, disk, cluster (A14–A19)
        ref2 = lref("14–19 (APIs)")
        with self.voiceover(SAY[2]) as vo:
            self.play(ReplacementTransform(ref1, ref2), run_time=0.5)
            vo.wait_until("Then come a bucket")
            m.layer(self, "bucket", run_time=0.6)
            vo.wait_until("a registry of images")
            m.layer(self, "registry", run_time=0.6)
            vo.wait_until("and a persistent disk")
            m.layer(self, "disk", run_time=0.6)
            vo.wait_until("On the right sits a cluster")
            m.layer(self, "cluster", run_time=0.9)
            for key, port, cue in (("nginx", None, "NGINX in front"), ("app", "3000", "the app on 3000"),
                                   ("api", "9000", "the API on 9000"), ("vdb", "8000", "the vector database")):
                vo.wait_until(cue)
                anims = [flash_box(m.boxes[key])]
                if port:
                    anims.append(Indicate(m.ports[port], color=ROUTE, scale_factor=1.06))   # 1.2 crossed the frame
                self.play(*anims, run_time=0.7)
                m.heal(self)

        # ========================================================== 3. today: on your laptop (A22 in a chip)
        aws = grey_chip("the same building blocks have AWS and Azure names (slide 22)")
        aws.box.set_fill(S.BG, 1)
        aws.move_to(m.layers["title"])
        with self.voiceover(SAY[3]) as vo:
            title = m.layers.pop("title")             # the chip takes the title's place
            m.shown.remove("title")
            m.drop(self, title, extra=[FadeOut(ref2)], run_time=0.4)
            vo.wait_until("that whole right-hand side")
            # The cluster lifts out of the BLUE boundary and slides down to the bottom right; the GCP
            # boundary closes behind it (right edge left of the laptop); the cloud's edges into it (NFS,
            # the users' HTTP/HTTPS 80) go with it.
            cl = m.layers["cluster"]
            gcp_fr = m.layers["gcp"][0]
            disk_l, e = m.layers["disk"], m.layers["edges"]
            lift, slide = UP * 0.2 + RIGHT * 0.12, DOWN * 0.55
            gcp_new = box(GCP_RIGHT - gcp_fr.get_left()[0], gcp_fr.height, CLOUD, dashed=True)
            gcp_new.align_to(gcp_fr, LEFT).align_to(gcp_fr, UP)
            m.drop(self, disk_l[1], disk_l[2], e.users_edge, e.users_label, run_time=0.5,
                   extra=[cl.animate.shift(lift), Transform(gcp_fr, gcp_new)])
            self.play(cl.animate.shift(slide), run_time=0.6)
            m.heal(self)
            assert m.cluster_frame.get_left()[0] > gcp_fr.get_right()[0] + 0.2, "laptop vs GCP"
            assert m.cluster_frame.get_right()[0] < 6.6 and m.cluster_frame.get_bottom()[1] > -3.6
            m.to_laptop(self, run_time=1.2)
            self.play(FadeIn(aws, shift=DOWN * 0.15), run_time=0.4)
            vo.wait_until("runs on your laptop")
            self.play(m.cluster_frame.animate(rate_func=there_and_back).set_stroke(TURN, width=6), run_time=0.8)
            m.heal(self)

        # ========================================================== 4. A43's folder rule on your real tree
        ref4 = one_slide("43 (APIs)")
        v1 = grey_glyphs(file_tree(["cheese-app-v1/", "  README.md", "  src/", "    api-service/",
                                    "    frontend-simple/"], size=TREE_SIZE, indent=0.3))
        empty = grey_chip("+ 7 empty folders")
        empty.next_to(v1.rows[-1], DOWN, buff=0.14).align_to(v1.rows[-1].glyph, LEFT)
        v1g = VGroup(v1, empty)
        v2 = grey_glyphs(file_tree(["cheese-app-v2/", "  README.md", "  src/", "    api-service/",
                                    "    docker-compose.yml", "    frontend-react/", "    vector-db/"],
                                   size=TREE_SIZE, indent=0.3))
        side = grey_glyphs(file_tree(["persistent-folder/", "secrets/"], size=TREE_SIZE))
        cols = VGroup(v1g, v2, side).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        cols.move_to([0, 0, 0]).shift(UP * (1.45 - cols.get_top()[1]))
        brackets, roots = VGroup(), VGroup()
        for g in (v1g, v2):
            b = RoundedRectangle(width=g.width + 0.3, height=g.height + 0.3, corner_radius=0.12,
                                 stroke_color=OWN, stroke_width=3).move_to(g)
            lb = label("Git root", 20, OWN).next_to(b, UP, buff=0.08).align_to(b, LEFT).shift(RIGHT * 0.1)
            brackets.add(b)
            roots.add(lb)
        sec_row = side.rows[1]
        outside = VGroup(label("secrets outside", 20, S.GREY), label("the Git folder", 20, S.GREY)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        sec_ring = ring(sec_row, S.GREY, buff=0.1, dashed=True)
        lap_frame = RoundedRectangle(width=13.1, height=4.65, corner_radius=0.16, stroke_color=LAPTOP,
                                     stroke_width=3).set_fill(S.BG, 1).move_to([0, 0.15, 0])
        lap_title = label("your laptop", 22, LAPTOP)
        lap_title.move_to(lap_frame.get_corner(UR) + np.array([-0.25 - lap_title.width / 2, -0.32, 0]))
        note_card = card(["v1 keeps empty folders for the slide's services · v2 holds only the three it runs"],
                         size=20).move_to([0, -2.85, 0])
        assert lap_title.get_bottom()[1] > side.get_top()[1] + 0.1, "title vs persistent-folder/"
        assert lap_frame.get_bottom()[1] < brackets.get_bottom()[1] - 0.1
        assert lap_frame.get_bottom()[1] > note_card.get_top()[1] + 0.05
        assert cols.get_left()[0] > -6.35 and cols.get_right()[0] < 6.35, (cols.get_left(), cols.get_right())
        v1_src = VGroup(v1.rows[3], v1.rows[4], empty)
        v2_src = VGroup(*v2.rows[3:7])
        v2_three = VGroup(v2.rows[3], v2.rows[5], v2.rows[6])
        with self.voiceover(SAY[4]) as vo:
            fr_c = m.cluster_frame.copy()
            tt_c = m.cluster_title.copy()
            self.add(fr_c, tt_c)
            self.play(FadeOut(m), FadeOut(aws), FadeIn(ref4), run_time=0.6)
            self.play(Transform(fr_c, lap_frame), Transform(tt_c, lap_title), run_time=0.9)
            self.play(LaggedStart(FadeIn(v1g, shift=DOWN * 0.15), FadeIn(v2, shift=DOWN * 0.15),
                                  FadeIn(side, shift=DOWN * 0.15), lag_ratio=0.3), run_time=1.1)
            vo.wait_until("one Git folder per app")
            self.play(*[Create(b) for b in brackets], *[FadeIn(r, shift=UP * 0.1) for r in roots], run_time=0.8)
            vo.wait_until("one folder per service under src")
            self.play(each([v1.rows[2].name_text, v2.rows[2].name_text], TURN, scale=1.15), run_time=0.7)
            self.play(each([*v1_src, *v2_src], TURN, scale=1.06, lag=0.1), run_time=1.2)
            vo.wait_until("and secrets outside the Git folder")
            self.play(Create(sec_ring), FadeIn(outside, shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(sec_row, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Version 1 even keeps empty folders")
            self.play(FadeIn(note_card, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(empty, color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("version 2 holds only its three")
            self.play(each(list(v2_three), TURN, scale=1.1, lag=0.25), run_time=1.0)

        # ========================================================== 5. steps 1 and 2: clone both
        tr = tracker_se(1)
        t = term(P_LAPTOP, rows=6, title=T_LAPTOP)
        rc = readme_card(18, CARD_18).move_to([0, 1.2, 0])
        assert rc.get_bottom()[1] > t.box.get_top()[1] + 0.2 and rc.get_top()[1] < TRACK_BOTTOM - 0.1
        tree_all = VGroup(fr_c, tt_c, cols, brackets, roots, outside, sec_ring, note_card)
        spell = on_bar(t, extra_row("our spelling"))          # the clone/mkdir rows have no room beside them
        turn = turn_row().next_to(spell, LEFT, buff=0.2)
        bar3 = on_bar(term(P_LAPTOP, rows=3), extra_row("our spelling")).get_center()
        bar6 = on_bar(term(P_LAPTOP, rows=6), extra_row()).get_center()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(tree_all), FadeOut(ref4), FadeIn(tr, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.3),
                      run_time=0.8)
            vo.wait_until("clone both repositories")
            c1 = type_capture(self, t, P01, type_time=1.2)[0]
            self.play(FadeIn(spell, shift=LEFT * 0.1), run_time=0.4)
            t.add(spell)                     # rides with (and stays above) its terminal
            out(self, t, P01.at(2), run_time=0.4)
            self.play(track(tr, 2), run_time=0.5)
            self.add(tr)
            c2 = type_capture(self, t, P02, type_time=1.2)[0]
            out(self, t, P02.at(2), run_time=0.4)
            vo.wait_until("The READMEs say clone or download")
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(rc.body, color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("git clone is our spelling")
            self.play(*[Indicate(substring(r, "git clone"), color=TURN, scale_factor=1.15)
                        for r in (rows_of(c1)[0], rows_of(c2)[0])], run_time=0.8)
            self.add(t)
            vo.wait_until("Pause and clone them")
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            t.add(turn)
            flash_tag(self, turn, TURN)
            self.add(t)

        # ========================================================== 6. step 3: your own folders
        def folder_row(name: str, ls: str, y: float):
            f = VGroup(folder_glyph(0.3, S.GREY), mono(name, 22, INK)).arrange(RIGHT, buff=0.16)
            f.move_to([-5.9 + f.width / 2, y, 0])
            own = grey_chip("student", mono_font=True).next_to(f, RIGHT, buff=0.4)
            ghost = dashed_chip("root", mono_font=True).next_to(own, RIGHT, buff=0.3)
            ln = mono_line(ls, 20, OUTPUT)
            ln.shift(np.array([-5.5 - ln.strut.get_left()[0], y - 0.46 - ln.strut.get_center()[1], 0]))
            return f, own, ghost, ln

        pf, pf_own, pf_ghost, pf_ls = folder_row("persistent-folder/", LS_PF, 2.3)
        sf, sf_own, sf_ghost, sf_ls = folder_row("secrets/", LS_SEC, 1.15)
        sf_own.align_to(pf_own, LEFT)
        pf_ghost.next_to(pf_own, RIGHT, buff=0.3)
        sf_ghost.next_to(sf_own, RIGHT, buff=0.3)
        ghosts = VGroup(pf_ghost, sf_ghost)
        cuts = VGroup(*[strike(g, ERR) for g in ghosts])
        why = label("on Linux, Docker would create them as root", 20, S.GREY)
        ls_tag = row_tag("ls -la · extra")
        ls_tag.move_to([6.4 - ls_tag.width / 2, pf.get_y(), 0])
        key = file_icon("ml-workflow.json", S.GREY, h=0.32)
        key.move_to([-5.3 + key.width / 2, -0.1, 0])
        no_write = VGroup(cross_glyph(0.26), label("the container cannot write", 20, ERR)).arrange(RIGHT, buff=0.15)
        why.move_to([pf_own.get_left()[0] + why.width / 2, key.get_y(), 0])
        no_write.next_to(why, DOWN, buff=0.18).align_to(why, LEFT)
        pic6 = VGroup(pf, pf_own, pf_ls, sf, sf_own, sf_ls, ghosts, cuts, why, ls_tag, key, no_write)
        assert pic6.get_top()[1] < TRACK_BOTTOM - 0.05 and pic6.get_right()[0] < 6.5, (pic6.get_top(), pic6.get_right())
        with self.voiceover(SAY[6]) as vo:
            t.remove(turn)
            self.play(FadeOut(rc), FadeOut(turn), track(tr, 3), run_time=0.5)
            self.add(tr)
            resize(self, t, 3, extra=[spell.animate.move_to(bar3)], run_time=0.6)
            assert t.box.get_top()[1] < pic6.get_bottom()[1] - 0.1, (t.box.get_top(), pic6.get_bottom())
            mk = type_capture(self, t, P05, type_time=1.0)[0]
            flash_tag(self, spell)
            self.add(t)
            bare_prompt(self, t)
            vo.wait_until("create secrets and persistent folder yourself")
            self.play(LaggedStart(FadeIn(pf, shift=RIGHT * 0.2), FadeIn(sf, shift=RIGHT * 0.2), lag_ratio=0.3),
                      run_time=0.7)
            self.play(FadeIn(pf_ls), FadeIn(sf_ls), FadeIn(ls_tag), FadeIn(pf_own), FadeIn(sf_own), run_time=0.6)
            self.play(substring(pf_ls, "student").animate.set_color(TURN),
                      substring(sf_ls, "student").animate.set_color(TURN), run_time=0.5)
            self.add(pf_ls, sf_ls)
            vo.wait_until("Left to Docker on Linux")
            self.play(FadeIn(ghosts, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("they would belong to root")
            self.play(*[Create(c) for c in cuts], FadeIn(why), run_time=0.6)
            vo.wait_until("and the container could not write there")
            self.play(FadeIn(no_write, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Your ml workflow key goes into secrets")
            self.play(FadeIn(key, shift=DOWN * 0.4), run_time=0.7)
            self.play(Indicate(sf, color=INK, scale_factor=1.08), run_time=0.6)

        # ========================================================== 7. main moved twice; 2025 holds Tutorial 24
        y_main, y_25 = 2.0, 0.75
        xs = (-3.2, -0.6, 2.0)
        main_l = Line([-4.6, y_main, 0], [2.6, y_main, 0], color=S.GREY, stroke_width=4)
        dots = VGroup(*[Dot([x, y_main, 0], radius=0.11, color=S.GREY) for x in xs])
        main_lb = mono("main", 22, INK).next_to(main_l, LEFT, buff=0.25)
        # 2025 = 14f2a14, where main stood before it moved twice: the branch forks at the first dot
        fork = VMobject().set_points_smoothly([[xs[0], y_main, 0], [xs[0] + 0.5, (y_main + y_25) / 2 + 0.1, 0],
                                               [xs[0] + 1.2, y_25, 0]]).set_stroke(S.GREY, 4)
        b25_l = Line([xs[0] + 1.2, y_25, 0], [2.6, y_25, 0], color=S.GREY, stroke_width=4)
        b25_lb = mono("2025", 22, INK).next_to(b25_l, LEFT, buff=0.25)
        ptr = VGroup(Triangle(color=TURN).set_fill(TURN, 1).scale(0.12).rotate(PI),
                     mono("main", 20, TURN)).arrange(UP, buff=0.06)
        ptr.next_to(dots[0], UP, buff=0.08)
        fs = VGroup(folder_glyph(0.28, S.GREY), mono("frontend-simple", 20, INK)).arrange(RIGHT, buff=0.12)
        fs.next_to(Dot([-2.3, y_main, 0]), DOWN, buff=0.18).align_to(Dot([-2.3, 0, 0]), LEFT)
        fs_dest = fs.copy().next_to(Dot([0.8, y_25, 0]), UP, buff=0.18)
        later = grey_chip("at the end of this video").next_to(b25_l, RIGHT, buff=0.15)
        branch = VGroup(main_l, dots, main_lb, fork, b25_l, b25_lb)
        pic7 = VGroup(branch, ptr, fs, later)
        assert pic7.get_top()[1] < PIC_TOP and later.get_right()[0] < 6.5, (pic7.get_top(), later.get_right())
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pic6), track(tr, 3, extra=True), run_time=0.6)
            self.add(tr)
            plain = spell                    # 'extra · our spelling' becomes plain 'extra'
            new = extra_row().move_to(bar6)
            old_text = spell.text
            spell.remove(old_text)
            resize(self, t, 6, extra=[Transform(spell.box, new.box), FadeOut(old_text), FadeIn(new.text)],
                   run_time=0.6)
            self.remove(old_text, new.text)
            spell.add(new.text)
            spell.text = new.text
            self.add(t)
            assert t.box.get_top()[1] < fs_dest.get_bottom()[1] - 0.1, (t.box.get_top(), fs_dest.get_bottom())
            self.play(Create(main_l), FadeIn(main_lb), FadeIn(dots), Create(fork), Create(b25_l), FadeIn(b25_lb),
                      run_time=0.8)
            self.play(FadeIn(fs, shift=DOWN * 0.1), FadeIn(ptr, shift=DOWN * 0.1), run_time=0.4)
            ls = type_capture(self, t, P04, type_time=1.4)[0]
            flash_tag(self, plain)
            self.add(t)
            outs = out(self, t, P04.at((2, 4)), run_time=0.5)
            vo.wait_until("the main branch of version 2 moved twice")
            self.play(ptr.animate.next_to(dots[1], UP, buff=0.08), run_time=0.5)
            self.play(ptr.animate.next_to(dots[2], UP, buff=0.08), run_time=0.5)
            vo.wait_until("We follow main as you clone it today")
            self.play(substring(outs[0], "447b5c3").animate.set_color(TURN),
                      substring(outs[2], "447b5c3").animate.set_color(TURN),
                      dots[2].animate.set_color(TURN), run_time=0.5)
            self.add(t)
            self.play(Indicate(ptr, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("The simple frontend the lecture teaches")
            self.play(Indicate(fs, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("now sits on a branch called 2025")
            self.play(substring(outs[1], "refs/heads/2025").animate.set_color(ROUTE), run_time=0.4)
            self.add(t)
            self.play(fs.animate(path_arc=-0.6).move_to(fs_dest), run_time=1.0)
            vo.wait_until("which we visit at the end")
            self.play(FadeIn(later, shift=LEFT * 0.15), Indicate(b25_lb, color=INK, scale_factor=1.15), run_time=0.6)
        self.wait(1.0)                       # let the chip be read before the frame empties
        self.play(FadeOut(VGroup(pic7, t, tr)), run_time=0.7)
        self.wait(0.3)
