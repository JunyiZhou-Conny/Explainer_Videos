"""S06 · The API and the frontend (AC215 L20). TRACKER [M] 11 (beats 0-6), 12 (beat 7).
Lecture: 20 · 7–8 (beat 0 only, while the small V2 picture of the VM is on screen).

Beats (script.md "## S06", one voiceover block each):
0. TRACKER [M] 11. lecture_ref(20, "7–8"). A small V2 (the VM from the inside: BLUE frame, dotted
   PINK fence, GREEN cable, the vector DB already plugged in with its data dots and door 8000, a
   YELLOW dashed empty slot where the API goes) top right over an 8-row terminal `cheese-app-vm`.
   The picture and the lecture tag leave, the terminal grows to 13 rows, and it types the README's
   `sudo docker run -d --name api-service \\` block (vm/30: 1–10) -> TERM(vm/30: 11 YELLOW wrap, 12).
1. The typed block stays; flags glow one per phrase: the two `-v` lines GREEN, `-p 9000:9000` PINK,
   `GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-service.json` GREEN, `CHROMADB_HOST=cheese-app-vector-db`
   PINK; `GCP_PROJECT=ac215-project` gets the GREY default tag; `GCS_BUCKET_NAME=cheese-app-models`
   dims to GREY with a row tag 'passed, never used'. Then the pull finishes (vm/30: …, 55–57 wrap, digest
   and id GREY), the terminal shrinks to 8 rows, the small V2 comes back and a TEAL `api-service`
   box plugs into the cable, door '9000' on the VM's box (inside the fence).
2. TRACKER [M] 11 · extra. `sudo docker logs api-service 2>&1 | head -60` (extra) -> TERM(vm/31: 2,
   5, …, 26 YELLOW, 27 wrap, …, 53 wrap GREEN). A GREY-dashed bucket 'Models' (slide 7's store)
   appears left, a GREY chip 'GitHub release → /persistent/experiments', then a GREY strike and the
   bucket dims.
3. `sudo docker ps; sudo docker images` (extra) -> TERM(vm/32: 5 crop, 7 crop): '5.07GB' YELLOW, a
   GOLD-outlined disk chip 'about 5 GB on the VM disk'; the api box pulses at 'TensorFlow inside'.
4. Three curls, one per phrase, each typed (extra): vm/33 -> 2, 8 GREEN; vm/35 (folds) -> 8, 14
   wrap; vm/34 -> 2, 8 RED. Left: GREY erratum tag, a GREY chip 'public image older than your
   clone: no /status' and 'your own images answer it'.
5. A README card (README.md · line 131) left. The terminal clears and types the README's interactive
   block (vm/38: 1–12, fast) -> TERM(vm/38: 13 wrap) RED; the running api box pulses.
6. TRACKER [M] 11 · extra. `sudo docker rm -f api-service` (extra) -> TERM(vm/39: 2), the api box
   stops (GREY); the interactive block again (vm/40: 1–12, fast) -> 13, 16, …, the container prompt
   of line 24 typing `exit` (id GREY), 25; then the detached block again (vm/41: 1–10, fast) ->
   11 (GREY); the api box runs again. A GREY chip 'optional · the dev mode from L18'.
7. TRACKER [M] 12. The frontend command (folds) -> TERM(vm/42: 2, …, 55–57); a TEAL `frontend` box
   plugs in, door '3000'. TRACKER [M] 12 · extra: vm/43 (extra, folds) -> 6, 7 (+ 'at the time of
   recording'), 12, 13 YELLOW with a PINK row tag 'the page calls /api-service/… on its own address'.
   YELLOW '▶ your turn' on the terminal's title bar. Fade; empty frame.

Deviations from SHOW:
- V2 is drawn as a small in-scene copy of the VM (MiniVm: three slots, doors, cable, fence; no phone
  book, no network label) because the shared NamePhoneBook is 9.5 units wide and has no compact
  variant; it sits top right over an 8-row terminal, as S04's corner VM did.
- Beats 0-1: the 10-row README block plus its output needs 13 rows, so the small V2 leaves while the
  block is typed and comes back (with the API plug) after the flags have glowed; the pull's last
  lines (vm/30: 55–57) print at the end of beat 1, so the block stays whole while its flags glow.
  The lecture tag goes with the picture.
- Beats 1 and 7: the 'Digest: sha256:…' lines (vm/30:55, vm/42:55) are cropped after 8 hex digits
  (never read; a wrapped digest left 'Digest:' alone on a row).
- Beat 3: vm/32 lines 5 and 7 are 86 characters; they are cropped after 'DISK USAGE' / '5.07GB'.
- Beat 4: one 8-row terminal instead of three separate strips (the corner V2 keeps its place).
- Beat 5: the terminal clears before the 12-row interactive block so the error lands on time.
- Beat 7: '▶ your turn' sits on the title bar: the frontend command has scrolled off by the time the
  narration says 'Pause'.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources (checked)
V30, V31, V32, V33 = capture("vm/30"), capture("vm/31"), capture("vm/32"), capture("vm/33")
V34, V35, V38, V39 = capture("vm/34"), capture("vm/35"), capture("vm/38"), capture("vm/39")
V40, V41, V42, V43 = capture("vm/40"), capture("vm/41"), capture("vm/42"), capture("vm/43")

assert V30.cmd_lines[0] == "sudo docker run -d --name api-service \\" and len(V30.cmd_lines) == 10
assert V30.cmd_lines[1:] == V41.cmd_lines[1:] and V41.cmd_lines[0] == V30.cmd_lines[0]
assert V30.line(11) == "Unable to find image 'dlops/cheese-app-api-service:latest' locally"
assert V30.line(12).startswith("latest: Pulling from") and V30.line(55).startswith("Digest: sha256:")
assert V30.line(56).startswith("Status: Downloaded newer image")
assert re.fullmatch(r"[0-9a-f]{64}", V30.line(57)) and re.fullmatch(r"[0-9a-f]{64}", V41.line(11))
assert V31.cmd == "sudo docker logs api-service 2>&1 | head -60"
assert V31.line(2) == "Container is running!!!" and V31.line(5) == "Python version: Python 3.12.12"
assert V31.line(26) == "Loading CNN Model..." and V31.line(27).startswith("best_model_path: /persistent/experiments/")
assert V31.line(53).startswith("INFO:     Uvicorn running on http://0.0.0.0:9000")
assert V32.cmd == "sudo docker ps; sudo docker images"
assert "DISK USAGE" in V32.line(5) and V32.line(7).startswith("dlops/cheese-app-api-service:latest") \
    and "5.07GB" in V32.line(7)
assert V33.cmd == "curl -s -i http://localhost:9000/" and V33.line(2) == "HTTP/1.1 200 OK"
assert V33.line(8) == '{"message":"Welcome to AC215"}[exit 0]'     # no newline before the exit marker
ROOT_BODY = V33.crop(8, "}")
assert V35.cmd.startswith("curl -s http://localhost:9000/docs") and "<title>API Server - Swagger UI</title>" in V35.line(8)
assert V35.line(14).startswith("{'title': 'API Server'")
assert V34.cmd == "curl -s -i http://localhost:9000/status" and V34.line(2) == "HTTP/1.1 404 Not Found"
assert V34.line(8) == '{"detail":"Not Found"}[exit 0]'
STATUS_BODY = V34.crop(8, "}")
assert V38.cmd_lines[0] == "sudo docker run --rm -ti --name api-service \\" and len(V38.cmd_lines) == 12
assert V38.line(13).startswith('docker: Error response from daemon: Conflict. The container name "/api-service" is already in use')
assert readme(131).startswith("If you want to run in interactive mode like we did in development")
assert V39.cmd == "sudo docker rm -f api-service" and V39.line(2) == "api-service"
assert V40.cmd_lines == V38.cmd_lines and V40.line(13) == "Container is running!!!"
assert V40.line(16) == "Python version: Python 3.12.12" and V40.line(25) == "exit"
assert V42.cmd == "sudo docker run -d --name frontend -p 3000:3000 --network cheese-app-network dlops/cheese-app-frontend-react"
assert V42.line(2) == "Unable to find image 'dlops/cheese-app-frontend-react:latest' locally"
assert V42.line(55).startswith("Digest: sha256:") and re.fullmatch(r"[0-9a-f]{64}", V42.line(57))
assert V43.line(6) == "<title>Formaggio</title>" and "Next.js 15.0.2" in V43.line(7)
assert V43.line(12).strip() == "✓ Ready in 67ms" and V43.line(13) == "BASE_API_URL: /api-service"

# ------------------------------------------------------------------ the small V2 (top right)
MV_X0, MV_X1, MV_Y0, MV_Y1 = 1.7, 6.4, 0.78, 2.84       # the VM frame
MV_SLOT = {"vdb": 2.51, "api": 4.05, "front": 5.59}       # box centres (x)
MV_BOX_Y, MV_BOX_W, MV_BOX_H = 2.0, 1.46, 0.86
MV_CABLE_Y = 1.3
MV_NAMES = {"vdb": ("cheese-app-", "vector-db"), "api": ("api-service",), "front": ("frontend",)}


class MiniVm(Piece):
    """The VM from the inside, small (x 1.56 .. 6.54, y 0.65 .. 3.07 with its fence and doors): BLUE
    frame, dotted PINK fence, GREEN cable, title bottom left; slots for the vector DB, the API and the
    frontend. PLAYS plug(key) · stop(key) · start(key). .boxes{key} .doors{key} .plugs{key}"""

    def __init__(self, **kw):
        super().__init__(**kw)
        w, h = MV_X1 - MV_X0, MV_Y1 - MV_Y0
        c = np.array([(MV_X0 + MV_X1) / 2, (MV_Y0 + MV_Y1) / 2, 0])
        self.frame = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=CLOUD,
                                      stroke_width=3).set_fill(tint(CLOUD, 0.05), 1).move_to(c)
        fr = RoundedRectangle(width=w + 0.28, height=h + 0.26, corner_radius=0.18)
        self.fence = DashedVMobject(fr, num_dashes=int((w + h) * 9), dashed_ratio=0.4).set_stroke(ROUTE, 2.5)
        self.fence.move_to(c)
        self.title = mono(T_VM, 20, CLOUD).move_to([MV_X0 + 0.2, 1.0, 0], aligned_edge=LEFT)
        self.cable = Line([MV_X0 + 0.2, MV_CABLE_Y, 0], [MV_X1 - 0.2, MV_CABLE_Y, 0], color=OWN, stroke_width=6)
        self.add(self.fence, self.frame, self.title, self.cable)
        self.boxes, self.doors, self.plugs = {}, {}, {}

    def make_box(self, key: str) -> VGroup:
        fr = RoundedRectangle(width=MV_BOX_W, height=MV_BOX_H, corner_radius=0.1, stroke_color=CONTAINER,
                              stroke_width=3).set_fill(tint(CONTAINER, 0.18), 1)
        nm = VGroup(*[label(r, 20, INK) for r in MV_NAMES[key]]).arrange(DOWN, buff=0.03)
        assert nm.width < MV_BOX_W - 0.08 and nm.height < MV_BOX_H - 0.1, key
        nm.move_to(fr)
        g = VGroup(fr, nm).move_to([MV_SLOT[key], MV_BOX_Y, 0])
        if key == "vdb":
            nm.shift(UP * 0.07)
            dots = VGroup(*[Dot(radius=0.04, color=CONTAINER) for _ in range(10)]).arrange(RIGHT, buff=0.06)
            dots.move_to([MV_SLOT[key], MV_BOX_Y - MV_BOX_H / 2 + 0.1, 0])
            g.add(dots)
        g.frame, g.name = fr, nm
        return g

    def parts_for(self, key: str):
        x = MV_SLOT[key]
        b = self.make_box(key)
        pl = Line([x, MV_BOX_Y - MV_BOX_H / 2, 0], [x, MV_CABLE_Y, 0], color=OWN, stroke_width=4)
        d = door(PORTS[key]).move_to([x, MV_Y1, 0])
        return b, pl, d

    def put(self, key: str):
        """Build `key` already plugged (no animation)."""
        b, pl, d = self.parts_for(key)
        self.add(pl, b, d)
        self.boxes[key], self.plugs[key], self.doors[key] = b, pl, d

    def plug(self, scene, key: str, run_time: float = 0.8):
        b, pl, d = self.parts_for(key)
        self.boxes[key], self.plugs[key], self.doors[key] = b, pl, d
        self.show(scene, pl, b, d, anims=[FadeIn(b, shift=DOWN * 0.3), Create(pl), GrowFromCenter(d)],
                  run_time=run_time)
        return b

    def stop(self, scene, key: str, run_time: float = 0.5):
        b = self.boxes[key]
        scene.play(b.frame.animate.set_stroke(S.GREY).set_fill(tint(S.GREY, 0.1), 1),
                   self.doors[key].animate.set_opacity(0.3), run_time=run_time)
        self.heal(scene)

    def start(self, scene, key: str, run_time: float = 0.5):
        b = self.boxes[key]
        scene.play(b.frame.animate.set_stroke(CONTAINER).set_fill(tint(CONTAINER, 0.18), 1),
                   self.doors[key].animate.set_opacity(1), run_time=run_time)
        self.heal(scene)


def api_slot() -> VMobject:
    """The empty YELLOW dashed slot where the API will plug in (beat 0)."""
    r = RoundedRectangle(width=MV_BOX_W, height=MV_BOX_H, corner_radius=0.1)
    return DashedVMobject(r, num_dashes=22, dashed_ratio=0.5).set_stroke(TURN, 3).move_to([MV_SLOT["api"], MV_BOX_Y, 0])


LEFT_X = -6.45          # left column above the 8-row terminal: x -6.45 .. 1.4, y 0.75 .. 2.75


def at_left(m, y: float):
    return m.move_to([LEFT_X + m.width / 2, y, 0])


class ApiAndFrontend(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 8, len(SAY)

        # ========================================================== 0. run api service: it pulls first
        trk = tracker_m(11)
        ref = lref("7–8")
        mv = MiniVm()
        mv.put("vdb")
        slot = api_slot()
        t = vm_term(8)
        assert mv.fence.get_bottom()[1] > t.box.get_top()[1] + 0.03, (mv.fence.get_bottom(), t.box.get_top())
        assert mv.doors["vdb"].get_top()[1] < ref.get_bottom()[1], mv.doors["vdb"].get_top()
        assert mv.fence.get_left()[0] > tracker_m(11, True).get_right()[0] + 0.15, mv.fence.get_left()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), FadeIn(mv), FadeIn(t, shift=UP * 0.2),
                      run_time=0.6)
            mv.show(self, slot, anims=[Create(slot)], run_time=0.5)
            self.play(slot.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.6)
            self.play(FadeOut(mv), FadeOut(ref), run_time=0.4)
            self.remove(mv, ref)
            mv.remove(slot)
            resize(self, t, 13, run_time=0.5)
            rows = type_capture(self, t, V30, type_time=0.16)
            assert all(not hasattr(r, "rows") for r in rows) and len(rows) == 10
            vo.wait_until("The image is not on the VM yet")
            r11 = out(self, t, [(V30.line(11), TURN)], wrap=True, run_time=0.4)
            self.play(*[Indicate(r, color=TURN, scale_factor=1.04) for r in r11], run_time=0.6)
            self.add(t)
            vo.wait_until("so docker run pulls it first")
            out(self, t, [V30.line(12)], run_time=0.4)

        # ========================================================== 1. the flags, one per phrase
        def glow(row, sub, color, scale=1.08):
            g = substring(row, sub)
            self.play(g.animate.set_color(color), run_time=0.3)
            self.play(Indicate(g, color=color, scale_factor=scale), run_time=0.5)
            self.add(t)
            return g

        with self.voiceover(SAY[1]) as vo:
            vo.wait_until("Two mounts")
            m1, m2 = substring(rows[1], '-v "$(pwd)/persistent-folder/":/persistent'), \
                substring(rows[2], '-v "$(pwd)/secrets/":/secrets')
            self.play(m1.animate.set_color(OWN), m2.animate.set_color(OWN), run_time=0.3)
            vo.wait_until("persistent folder and secrets")
            self.play(Indicate(m1, color=OWN, scale_factor=1.05), run_time=0.5)
            self.play(Indicate(m2, color=OWN, scale_factor=1.05), run_time=0.5)
            self.add(t)
            vo.wait_until("port 9000")
            glow(rows[3], "-p 9000:9000", ROUTE, 1.15)
            vo.wait_until("the key path")
            glow(rows[4], "GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-service.json", OWN, 1.04)
            vo.wait_until("and the database by name")
            glow(rows[7], "CHROMADB_HOST=cheese-app-vector-db", ROUTE, 1.06)
            vo.wait_until("The project is the README's default")
            dt = beside(default_row(), rows[6])
            pin(self, rows[6], dt)
            vo.wait_until("and the bucket name is passed but never used")
            self.play(substring(rows[5], "GCS_BUCKET_NAME=cheese-app-models").animate.set_color(S.GREY),
                      run_time=0.4)
            self.add(t)
            nu = beside(row_tag("passed, never used"), rows[5])
            pin(self, rows[5], nu)
        # the pull ends; the picture comes back with the API plugged in
        out(self, t, ["…", (V30.crop(55, "sha256:3412a226", "…"), S.GREY), V30.line(56), (V30.line(57), S.GREY)],
            wrap=True,
            run_time=0.5)
        resize(self, t, 8, run_time=0.5)
        self.play(FadeIn(mv), run_time=0.4)
        self.add(mv)
        mv.plug(self, "api")

        # ========================================================== 2. logs: CNN model, uvicorn; no bucket
        models = VGroup(pail(1.0, S.GREY, dashed=True), label("Models", 24, INK)).arrange(RIGHT, buff=0.25)
        at_left(models, 2.15)
        gh = grey_chip("GitHub release → /persistent/experiments")
        at_left(gh, 1.2)
        assert gh.get_right()[0] < mv.fence.get_left()[0] - 0.1, gh.get_right()
        mstrike = Line(models.get_corner(DL) + LEFT * 0.08, models.get_corner(UR) + RIGHT * 0.08,
                       color=S.GREY, stroke_width=4)
        with self.voiceover(SAY[2]) as vo:
            self.play(track(trk, 11, True), run_time=0.4)
            lg = type_capture(self, t, V31, type_time=0.6)[0]
            pin(self, lg, beside(extra_row(), lg))
            out(self, t, V31.at(2, 5, "…"), run_time=0.4)
            vo.wait_until("loading CNN model")
            out(self, t, [(V31.line(26), TURN), V31.line(27)], wrap=True, run_time=0.5)
            vo.wait_until("then uvicorn running on port 9000")
            out(self, t, ["…", (V31.line(53), OWN)], wrap=True, run_time=0.5)
            self.play(Indicate(mv.boxes["api"].frame, color=OWN, scale_factor=1.08), run_time=0.6)
            mv.heal(self)
            vo.wait_until("The model comes from a GitHub release")
            self.play(FadeIn(models, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(gh, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("not a bucket")
            self.play(Create(mstrike), run_time=0.4)
            vo.wait_until("so our picture grays out")
            self.play(models.animate.set_opacity(0.45), run_time=0.6)

        # ========================================================== 3. the image is big
        dk = disk_chip("about 5 GB on the VM disk")
        at_left(dk, 1.75)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(models, gh, mstrike)), run_time=0.4)
            self.remove(models, gh, mstrike)
            ps = type_capture(self, t, V32, type_time=0.5)[0]
            pin(self, ps, beside(extra_row(), ps))
            ir = out(self, t, [V32.crop(5, "DISK USAGE"), V32.crop(7, "5.07GB")], run_time=0.4)
            vo.wait_until("about five gigabytes on disk")
            g = substring(ir[1], "5.07GB")
            self.play(g.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(g, color=TURN, scale_factor=1.2), run_time=0.5)
            self.add(t)
            self.play(FadeIn(dk, shift=RIGHT * 0.2), run_time=0.4)
            vo.wait_until("with TensorFlow inside")
            self.play(Indicate(mv.boxes["api"], color=TURN, scale_factor=1.1), run_time=0.7)
            mv.heal(self)

        # ========================================================== 4. three curls
        er = erratum_tag()
        at_left(er, 2.3)
        e1 = grey_chip("public image older than your clone: no /status")
        e2 = grey_chip("your own images answer it")
        at_left(e1, 1.65)
        at_left(e2, 1.05)
        assert e1.get_right()[0] < mv.fence.get_left()[0] - 0.1, e1.get_right()
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(dk), run_time=0.3)
            self.remove(dk)
            type_capture(self, t, V33, type_time=0.6)
            vo.wait_until("the root says welcome to AC215")
            o1 = out(self, t, [(V33.line(2), OWN), (ROOT_BODY, OWN)], run_time=0.4)
            pin(self, o1[0], beside(extra_row(), o1[0]))
            vo.wait_until("and slash docs shows the docs page")
            c2 = type_capture(self, t, V35, type_time=0.8)[0]
            pin(self, c2, beside(extra_row(), c2))
            dr = out(self, t, [V35.line(8), V35.line(14)], wrap=True, run_time=0.4)
            self.play(Indicate(substring(dr[0], "Swagger UI"), color=TURN, scale_factor=1.15), run_time=0.5)
            self.add(t)
            vo.wait_until("Slash status says 404")
            type_capture(self, t, V34, type_time=0.6)
            o3 = out(self, t, [(V34.line(2), ERR), (STATUS_BODY, ERR)], run_time=0.4)
            pin(self, o3[0], beside(extra_row(), o3[0]))
            vo.wait_until("the public image is older than your clone")
            self.play(FadeIn(er, shift=RIGHT * 0.2), FadeIn(e1, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(e2, shift=RIGHT * 0.2), run_time=0.4)

        # ========================================================== 5. the interactive variant: name in use
        rc = readme_card(131, "If you want to run in interactive mode\nlike we did in development:")
        at_left(rc, 1.75)
        assert rc.get_right()[0] < mv.fence.get_left()[0] - 0.1 and rc.get_bottom()[1] > t.box.get_top()[1] + 0.1, \
            (rc.get_right(), rc.get_bottom())
        assert rc.get_top()[1] < TRACK_BOTTOM - 0.05, rc.get_top()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(er, e1, e2)), run_time=0.3)
            self.remove(er, e1, e2)
            self.play(FadeIn(rc, shift=RIGHT * 0.2), run_time=0.5)
            t.clear(self, run_time=0.3)
            self.add(t)
            vo.wait_until("Run as written")
            type_capture(self, t, V38, type_time=0.1)
            vo.wait_until("it fails")
            out(self, t, [(V38.line(13), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("the name api service is in use")
            self.play(Indicate(t.find("Conflict"), color=ERR, scale_factor=1.03), run_time=0.6)
            self.add(t)
            vo.wait_until("because the detached container still runs")
            self.play(Indicate(mv.boxes["api"], color=CONTAINER, scale_factor=1.12), run_time=0.7)
            mv.heal(self)

        # ========================================================== 6. rm -f, the shell, back to detached
        opt = grey_chip("optional · the dev mode from L18")
        at_left(opt, 1.75)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(rc), track(trk, 11, True), run_time=0.4)
            self.remove(rc)
            rm = type_capture(self, t, V39, type_time=0.5)[0]
            pin(self, rm, beside(extra_row(), rm))
            out(self, t, V39.at(2), run_time=0.3)
            mv.stop(self, "api")
            vo.wait_until("and the variant opens a shell")
            type_capture(self, t, V40, type_time=0.08)
            out(self, t, V40.at(13, 16, "…"), run_time=0.4)
            ex = type_at(self, t, V40, 24, type_time=0.3)
            cid = at_prompt(V40, 24)[0].split("@")[1].split(":")[0]
            self.play(substring(ex, cid).animate.set_color(S.GREY_DARK), run_time=0.3)
            self.add(t)
            out(self, t, V40.at(25), run_time=0.3)
            t.set_prompt(P_VM)
            vo.wait_until("It is optional")
            self.play(FadeIn(opt, shift=RIGHT * 0.2), run_time=0.4)
            vo.wait_until("we exit and start the detached one again")
            type_capture(self, t, V41, type_time=0.08)
            out(self, t, [(V41.line(11), S.GREY)], run_time=0.3)
            mv.start(self, "api")

        # ========================================================== 7. the frontend; your turn
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(opt), track(trk, 12), run_time=0.4)
            self.remove(opt)
            type_capture(self, t, V42, type_time=0.8)
            out(self, t, [V42.line(2), "…"], wrap=True, run_time=0.3)
            mv.plug(self, "front")
            out(self, t, [(V42.crop(55, "sha256:255a23b2", "…"), S.GREY), V42.line(56), (V42.line(57), S.GREY)], wrap=True,
                run_time=0.4)
            vo.wait_until("The extra check shows the title")
            self.play(track(trk, 12, True), run_time=0.4)
            fc = type_capture(self, t, V43, type_time=0.8)[0]
            pin(self, fc, beside(extra_row(), fc))
            fr = out(self, t, V43.at(6, 7, 12), run_time=0.4)
            vo.wait_until("Formaggio")
            g = substring(fr[0], "Formaggio")
            self.play(g.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(g, color=TURN, scale_factor=1.15), run_time=0.5)
            self.add(t)
            pin(self, fr[1], beside(time_row(), fr[1]))
            vo.wait_until("and the base API URL")
            br = out(self, t, [(V43.line(13), TURN)], run_time=0.4)[0]
            vo.wait_until("which the page calls on its own address")
            pt = beside(row_tag([("the page calls", "label"), ("/api-service/…", "mono"),
                                 ("on its own address", "label")], ROUTE), br)
            pin(self, br, pt)
            vo.wait_until("Pause and start both")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt), run_time=0.3)
            flash_tag(self, yt, TURN)

        self.play(FadeOut(VGroup(trk, t, mv, yt)), run_time=0.6)
        self.remove(trk, t, mv, yt)
        self.wait(0.3)
