"""S11 · The deployment toolbox, fixed twice (AC215 L20). TRACKER [P] 3 (beats 0-8), 4 (beats 9-10).
Lecture: 20 · 14, 20 (beat 0 only, while V5 first shows the toolbox inside the laptop).

Beats (script.md "## S11", one voiceover block each):
0. TRACKER [P] 3. lecture_ref(20, "14, 20"). V5 ControlRoom left: the GREY laptop holding the TEAL
   container `cheese-app-deployment`. CODE(src/deployment/docker-shell.sh: 9-17) right; lines 9-17
   light one by one, the names on 13-17 fly into the container as rows (GCP_PROJECT, GCP_REGION,
   GCP_ZONE, GOOGLE_APPLICATION_ / CREDENTIALS, PULUMI_BUCKET), then the GREY
   PULUMI_CONFIG_PASSPHRASE="" row with its chip "Dockerfile:51".
1. The env rows leave; the panel scrolls to CODE(docker-shell.sh: 34-43). One wire per phrase in
   V5 (socket GREY, /app GREEN, /secrets GOLD, docker_config PURPLE + chip 'credential helpers',
   three build contexts TEAL), each with its line bar on the panel.
2. Terminal `laptop` at src/deployment (the prompt's path flashes). README card (line 266) "cd into
   deployment" + GREY erratum + "→ src/deployment". TRACKER [P] 3 · extra · or edit the file: b01
   (folds) -> TERM(b01: 2 wrap), "your-gcp-project" YELLOW, row tag 'ours: a placeholder'.
3. TRACKER [P] 3. The terminal grows to 13 rows: `sh docker-shell.sh` -> TERM(b02: 2 wrap,
   3 crop, 12 wrap, …, 135-137 crop "404  Not Found" (URL elided) RED, …, 166 wrap RED, 167 ORANGE,
   168 wrap RED).
4. The terminal shrinks to a 3-row strip. CODE(Dockerfile: 3-12) left (line 4 RED, 'bullseye' RED,
   lines 11-12 ORANGE, GREY erratum); top right the small toolbox (TEAL) with its Dockerfile bricks
   ('line 4' RED, 'lines 29–30' GREY); bottom right an ORANGE shelf 'Debian 11 · bullseye-security'
   whose boxes slide off into a GREY-dashed 'archive'. 'Fix 1': panel and shelf go, the toolbox
   moves top left, the terminal grows to 9 rows; TRACKER · extra; b02a (folds) -> TERM(b02a: 2)
   GREEN; brick 'line 4' GREEN.
5. TRACKER [P] 3. `sh docker-shell.sh` -> TERM(b02b: 3 crop, 12-17 crop GREEN, 18 wrap RED, …,
   34 wrap ORANGE, 37-38 GREEN, 46 RED, 47 wrap RED); inset CODE(Dockerfile: 29-30) top right, line
   30 RED; brick 'lines 29–30' RED.
6. TRACKER · extra. b02c (folds) -> TERM(b02c: 2-23 wrap, blank rows dropped), '-' rows RED, '+'
   rows GREEN; brick 'lines 29–30' GREEN; YELLOW '▶ your turn' on the title bar.
7. TRACKER [P] 3. `sh docker-shell.sh` -> TERM(b02d: 3 crop GREEN, …, 31, 34 (+ at the time of
   recording), 35, 36 wrap RED). The toolbox widens: its bricks go, the entrypoint's five lamps come
   (docker-entrypoint.sh:10-27); lamp 1 'activate key' RED; GREY chip 'our key: made for no account'.
8. TERM(b02d: 52, 61 GREEN (lamps 2-3 GREEN), 63, 65, 66 RED (lamp 4 RED), 70 wrap, 71 wrap RED
   (lamp 5 RED), 76, 77 = the toolbox prompt (id GREY)); chip 'with your key: five GREEN lamps'.
9. TRACKER [P] 4. Title 'laptop · toolbox'; the printed prompt becomes the prompt. `gcloud
   --version` -> TERM(b03: 2, …, 11), `pulumi version` -> TERM(b04: 2), `kubectl version --client`
   -> TERM(b05: 2), 'at the time of recording' on the first two; 'v1.35.9-dispatcher' YELLOW + GREY
   ghost 'Dockerfile:33 · K8S_MINOR=1.34'; PURPLE note 'apt picks Google's kubectl package (1:592)
   over pkgs.k8s.io 1.34' with a PURPLE arrow; gcloud's 'kubectl 1.35.9' row PURPLE.
10. `gcloud auth list` -> TERM(b06: 3) RED + GREY ghost 'yours: * deployment@<your project>…'.
   TRACKER · extra: the GREY card (extra · not in the README) `gcloud artifacts repositories create
   cheese-app-repository --repository-format=docker --location=us` + GREEN 'look for: Created
   repository' above the terminal; YELLOW '▶ your turn' on the title bar. Fade; empty frame.

Deviations from SHOW:
- V5 (7.2 x 5.2) cannot sit beside a full-width terminal or over a strip, so it carries beats 0-1
  (env and wires, with the code panel beside it); from beat 4 on the toolbox is a slim TEAL band
  (MiniBox) above a 9-row terminal: Dockerfile bricks along its base (beats 4-6), then the
  entrypoint's five lamps in a row (beats 7-8). Same names, colours and states as V5's phases.
- Beats 0-1: the panels beside V5 have ~5.75 units: docker-shell.sh 9-17 is cut after each name
  (values of 9-13, 16, 17 hidden; 16 after 'GOOGLE_APPLICATION_', its rest is the container's
  second row), 34-43 is dedented with the host side of each -v elided (V5's wires show it); both
  headers say 'docker-shell.sh' (the full path does not fit; the terminal shows src/deployment).
- Beat 3: b02:3 cropped after '(6/20)' (the right-aligned 'docker:default' column); 135-137 keep
  'debian-security/pool/' and '404  Not Found' with the rest of the URL elided (one row each).
- Beat 4: the Dockerfile panel is lines 3-12 (lines 1-2 are blank; 1-12 does not render), cut to
  fit beside the toolbox. The shelf lives in the right half of the frame, not inside V5.
- Beat 4 'the RED brick swaps for a GREEN one' and beat 5/6's brick 'lines 29–30' happen on the
  band's bricks. Beat 5: b02b:3 cropped like b02:3, lines 12-17 cropped at a word boundary (one row
  per step; the timings are cut off). Beat 7: b02d:3 cropped after 'FINISHED'.
- Beat 9: '…' between b03 lines 2 and 11 (lines 3-10 are skipped); kubectl's row carries the ghost
  instead of a second 'at the time of recording' tag (both do not fit one row).
- Beat 10: the registry card sits above the terminal (there is no room under it).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]
assert len(SAY) == SAY_COUNT["S11"] == 11

# ------------------------------------------------------------------ the real sources (checked)
B01, B02, B02A, B02B = capture("b01"), capture("b02"), capture("b02a"), capture("b02b")
B02C, B02D = capture("b02c"), capture("b02d")
B03, B04, B05, B06 = capture("b03"), capture("b04"), capture("b05"), capture("b06")

assert B01.cmd.startswith("sed -i 's/\"ac215-project\" # Change/\"your-gcp-project\" # Change/' docker-shell.sh")
assert B01.line(2) == '13:export GCP_PROJECT="your-gcp-project" # Change to your GCP Project'
assert B02.cmd == "sh docker-shell.sh" and B02B.cmd == B02.cmd and B02D.cmd == B02.cmd
assert B02.line(2).startswith("Container 'cheese-app-deployment' is not running.")
assert B02.line(3).startswith("[+] Building 4.1s (6/20)")
assert B02.line(12).startswith(" => ERROR [ 2/16] RUN apt-get update")
assert all("debian-security/pool/" in B02.line(n) and "404  Not Found" in B02.line(n) for n in (135, 136, 137))
assert B02.line(166).startswith("ERROR: failed to build: failed to solve:")
assert B02.line(167) == "Unable to find image 'cheese-app-deployment:latest' locally"
assert B02.line(168).startswith("docker: Error response from daemon: pull access denied")
assert B02A.cmd.startswith("sed -i 's/^FROM python:3.13-slim-bullseye/FROM python:3.13-slim-bookworm/'")
assert B02A.line(2) == "4:FROM python:3.13-slim-bookworm"
assert B02B.line(3).startswith("[+] Building 12.6s (12/20)")
assert all(B02B.line(n).startswith(f" => [ {n - 10}/16] RUN") for n in range(12, 18))
assert B02B.line(18).startswith(" => ERROR [ 8/16] RUN apt-get update")
assert B02B.line(34).startswith("3.380 Package google-cloud-sdk is not available")
assert B02B.line(37) == "3.380 However the following packages replace it:"
assert B02B.line(38) == "3.380   google-cloud-cli"
assert B02B.line(46) == "3.383 E: Package 'google-cloud-sdk' has no installation candidate"
assert B02B.line(47).startswith("3.383 E: Package 'google-cloud-sdk-gke-gcloud-auth-plugin'")
assert B02C.cmd.startswith("sed -i 's/google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin/")
assert B02C.line(10) == "-FROM python:3.13-slim-bullseye" and B02C.line(11) == "+FROM python:3.13-slim-bookworm"
assert B02C.line(19).startswith("-    apt-get install -y google-cloud-sdk ")
assert B02C.line(20).startswith("+    apt-get install -y google-cloud-cli ")
DIFF_LINES = [n for n in range(2, 24) if B02C.line(n).strip()]
assert DIFF_LINES == [2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 15, 17, 18, 19, 20, 22, 23], DIFF_LINES
assert B02D.line(3).startswith("[+] Building 91.9s (21/21) FINISHED")
assert B02D.line(31) == "Container is running!!!"
assert B02D.line(34) == "Python version: Python 3.13.18"
assert B02D.line(35).startswith("UV version: uv 0.13.7")
assert B02D.line(36).startswith("ERROR: (gcloud.auth.activate-service-account)") and \
    "'invalid_grant: Invalid grant: account not found'" in B02D.line(36)
assert B02D.line(52) == "Updated property [core/project]."
assert B02D.line(61) == "Adding credentials for: us-docker.pkg.dev"
assert B02D.line(63) == "Bucket does not exist. Creating..."
assert B02D.line(65).startswith("Creating gs://your-gcp-project-pulumi-state-bucket/")
assert B02D.line(66).startswith("You are attempting to access protected data")
assert B02D.line(70).startswith("Logging into Pulumi using GCS bucket")
assert B02D.line(71).startswith("error: could not log in to the state backend")
assert B02D.line(76) == "No stacks found."
assert B02D.line(77).rstrip() == P_TOOLBOX
TOOLBOX_ID = P_TOOLBOX.split("@", 1)[1].split(":", 1)[0]
assert re.fullmatch(r"[0-9a-f]{12}", TOOLBOX_ID)
assert B03.cmd == "gcloud --version" and B03.line(2) == "Google Cloud SDK 592.0.0" and B03.line(11) == "kubectl 1.35.9"
assert B04.cmd == "pulumi version" and B04.line(2) == "v3.274.0"
assert B05.cmd == "kubectl version --client" and B05.line(2) == "Client Version: v1.35.9-dispatcher"
assert B06.cmd == "gcloud auth list" and B06.line(3) == "No credentialed accounts."
assert readme(266) == "- cd into `deployment`"
assert excerpt("src/deployment/Dockerfile", 4, 4) == "FROM python:3.13-slim-bullseye"
assert excerpt("src/deployment/Dockerfile", 33, 33) == "ARG K8S_MINOR=1.34"
assert excerpt("src/deployment/Dockerfile", 51, 51) == 'ENV PULUMI_CONFIG_PASSPHRASE=""'
assert excerpt("src/deployment/docker-shell.sh", 13, 13).startswith('export GCP_PROJECT="ac215-project"')

REGISTRY_CMD = ("gcloud artifacts repositories create cheese-app-repository",
                "--repository-format=docker --location=us")         # digest.md:104 (not in the README)
assert " ".join(REGISTRY_CMD) in (PROJECT / "digest.md").read_text(encoding="utf-8")


def crop_row(s: str, n: int = 64) -> str:
    """A build line cropped at a word boundary so it fits one 22 pt row (ends in '…')."""
    if len(s) <= n + 1:
        return s
    k = s.rfind(" ", 0, n)
    return s[:k].rstrip() + "…"


def e404(n: int) -> str:
    """b02:n cropped after '404  Not Found' with the URL elided to its debian-security/pool/ part."""
    s = B02.crop(n, "404  Not Found")
    i = s.index("https://")
    j = s.index("/debian-security/pool/")
    k = s.index("  404  Not Found")
    r = s[:i] + "…" + s[j:j + len("/debian-security/pool/")] + "…" + s[k:]
    assert len(r) <= 65, r
    return r


def mark_extra(scene, t, line, tg):
    """PLAYS: an extra tag beside the command's last row when it fits (pinned: it scrolls with the
    row; returns None), else on the title bar (returns it: the caller fades it)."""
    row = rows_of(line)[-1]
    if row.strut.get_right()[0] + 0.45 + tg.width < t.box.get_right()[0] - 0.1:
        pin(scene, line, beside(tg, line))
        return None
    on_bar(t, tg)
    scene.play(FadeIn(tg), run_time=0.3)
    return tg


# ------------------------------------------------------------------ the small toolbox (beats 4-8)
BAND_Y0, BAND_Y1 = 1.15, 2.75
BRICKS = (("line 4", 1.15), ("", 0.75), ("lines 29–30", 1.75), ("", 0.75))


class MiniBox(Piece):
    """The toolbox, small: a slim TEAL container (x x0 .. x1, y 1.15 .. 2.75) above a 9-row terminal,
    'cheese-app-deployment' top left. PLAYS bricks() (the Dockerfile wall along its base) · brick(name,
    state) · widen(x0, x1) (bricks go, the band spans the frame) · lamps() (the entrypoint's chain of
    five) · lamp_set(i, state) · note(text) (GREY chip top right). .brick_map .lamp_list"""

    def __init__(self, x0: float, x1: float, **kw):
        super().__init__(**kw)
        self.x0, self.x1 = x0, x1
        self.frame = RoundedRectangle(width=x1 - x0, height=BAND_Y1 - BAND_Y0, corner_radius=0.12,
                                      stroke_color=CONTAINER, stroke_width=3).set_fill(tint(CONTAINER, 0.12), 1)
        self.frame.move_to([(x0 + x1) / 2, (BAND_Y0 + BAND_Y1) / 2, 0])
        self.name = mono(C_TOOLBOX, 20, INK).move_to([x0 + 0.22, BAND_Y1 - 0.3, 0], aligned_edge=LEFT)
        self.add(self.frame, self.name)
        self.brick_map, self.bricks_g, self.lamp_list, self.lamps_g, self.chip = {}, None, [], None, None

    def left(self) -> float:
        return self.frame.get_left()[0]

    def bricks(self, scene, run_time: float = 0.7):
        x = self.left() + 0.22
        items = []
        for n, w in BRICKS:
            b = RoundedRectangle(width=w, height=0.42, corner_radius=0.04, stroke_color=S.GREY,
                                 stroke_width=2).set_fill(tint(S.GREY, 0.15), 1)
            b.move_to([x + w / 2, BAND_Y0 + 0.4, 0])
            g = VGroup(b)
            if n:
                g.add(label(n, 20, INK).move_to(b))
                self.brick_map[n] = g
            items.append(g)
            x += w + 0.1
        self.bricks_g = VGroup(*items)
        self.show(scene, self.bricks_g, anims=[LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in items],
                                                           lag_ratio=0.12)], run_time=run_time)
        return items

    def brick(self, scene, name: str, state: str = "red", run_time: float = 0.5, extra=()):
        col = {"red": ERR, "green": OWN, "grey": S.GREY}[state]
        b = self.brick_map[name][0]
        scene.play(b.animate.set_stroke(col).set_fill(tint(col, 0.28), 1), *extra, run_time=run_time)
        self.heal(scene)

    def widen(self, scene, x0: float = -6.45, x1: float = 6.45, run_time: float = 0.7):
        new = self.frame.copy().stretch_to_fit_width(x1 - x0).move_to([(x0 + x1) / 2, self.frame.get_y(), 0])
        g = self.bricks_g
        self._detach(g)
        scene.play(FadeOut(g, shift=DOWN * 0.15), Transform(self.frame, new),
                   self.name.animate.move_to([x0 + 0.22, BAND_Y1 - 0.3, 0], aligned_edge=LEFT), run_time=run_time)
        scene.remove(g)
        self.brick_map, self.bricks_g = {}, None
        self.heal(scene)

    def lamps(self, scene, run_time: float = 0.8):
        x = self.left() + 0.4
        items, links = [], []
        for i, n in enumerate(LAMPS):
            lp = lamp("off", 0.17).move_to([x, BAND_Y0 + 0.42, 0])
            t = label(n, 20, INK).next_to(lp, RIGHT, buff=0.14)
            g = VGroup(lp, t)
            g.lamp, g.text = lp, t
            items.append(g)
            x = t.get_right()[0] + 0.62
            if i:
                a = items[i - 1].text.get_right() + RIGHT * 0.08
                links.append(Line(a, lp.get_left() + LEFT * 0.04, color=S.GREY_DARK, stroke_width=2))
        assert items[-1].get_right()[0] < self.frame.get_right()[0] - 0.1
        self.lamp_list = items
        self.lamps_g = VGroup(*links, *items)
        self.show(scene, self.lamps_g, anims=[LaggedStart(*[FadeIn(g) for g in items], lag_ratio=0.15),
                                              FadeIn(VGroup(*links))], run_time=run_time)
        return items

    def lamp_set(self, scene, i: int, state: str = "green", run_time: float = 0.4):
        g = self.lamp_list[i]
        new = lamp(state, 0.17).move_to(g.lamp)
        self.swap(scene, g.lamp, new, run_time=run_time)
        g.lamp = new
        return new

    def note(self, scene, text: str, color=S.GREY, run_time: float = 0.5):
        c = grey_chip(text, color=color)
        c.move_to([self.frame.get_right()[0] - 0.2 - c.width / 2, BAND_Y1 - 0.32, 0])
        if self.chip is None:
            self.show(scene, c, run_time=run_time)
        else:
            self.swap(scene, self.chip, c, run_time=run_time)
        self.chip = c
        return c


class Toolbox(VoiceScene):
    def construct(self):
        # ========================================================== 0. the toolbox and its environment
        trk = tracker_p(3)
        ref = lref("14, 20")
        cr = ControlRoom()
        cr.shift(np.array([-2.95, -0.35, 0]))
        p1 = code("src/deployment/docker-shell.sh", 9, 17, font_size=20, shown="docker-shell.sh",
                  cuts={9: "SECRETS_DIR=", 10: "SSH_DIR=", 11: "SECRETS_DIR=", 12: "SSH_DIR=",
                        13: "GCP_PROJECT=", 16: "GOOGLE_APPLICATION_", 17: "PULUMI_BUCKET="})
        p1.move_to([0, -0.35, 0]).align_to([0.78, 0, 0], LEFT)
        assert p1.get_right()[0] < 6.58 and p1.get_left()[0] > cr.laptop_fr.get_right()[0] + 0.1, p1.get_right()

        # env rows inside the container (ControlRoom.env's layout, built here so the names can fly in)
        groups, y = [], 1.3
        avail = cr.container.get_right()[0] - cr.p(-0.7, 0)[0] - 0.1
        for n, col in [(n, INK) for n in ENV_NAMES] + [('PULUMI_CONFIG_PASSPHRASE=""', S.GREY)]:
            parts = [n]
            if label(n, 20).width > avail:
                k = n.rfind("_", 0, len(n) - 1) + 1
                parts = [n[:k], n[k:]]
            g = []
            for j, part in enumerate(parts):
                g.append(label(part, 20, col).move_to(cr.p(-0.7 + 0.3 * j, y), aligned_edge=LEFT))
                y -= 0.31
            groups.append(g)
        src51 = grey_chip("Dockerfile:51").next_to(groups[-1][-1], DOWN, buff=0.08).align_to(cr.container, RIGHT)
        src51.shift(LEFT * 0.12)
        assert all(r.get_right()[0] < cr.container.get_right()[0] - 0.05 for g in groups for r in g)
        shown_name = {13: "GCP_PROJECT", 14: "GCP_REGION", 15: "GCP_ZONE", 16: "GOOGLE_APPLICATION_",
                      17: "PULUMI_BUCKET"}

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), FadeIn(cr), run_time=0.8)
            vo.wait_until("the README packs them into one container")
            self.play(Indicate(cr.container, color=CONTAINER, scale_factor=1.03), run_time=0.8)
            cr.heal(self)
            vo.wait_until("the deployment toolbox")
            self.play(Indicate(cr.name, color=TURN, scale_factor=1.12), run_time=0.7)
            cr.heal(self)
            vo.wait_until("Lines 9 to 17")
            self.play(FadeIn(p1, shift=LEFT * 0.2), run_time=0.5)
            bars = [line_bar(p1.code, k, TURN, 0.16) for k in range(9)]
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.35), run_time=1.4)
            self.play(*[b.animate.set_opacity(0) for b in bars[:4]], run_time=0.3)
            self.remove(*bars[:4])
            flat, anims = [], []
            for i, line in enumerate(range(13, 18)):
                span = code_span(p1.code, line - 9, shown_name[line])
                anims.append(ReplacementTransform(span.copy(), groups[i][0]))
                flat.append(groups[i][0])
                for extra in groups[i][1:]:
                    anims.append(FadeIn(extra, shift=RIGHT * 0.2))
                    flat.append(extra)
            cr.show(self, *flat, anims=[LaggedStart(*anims, lag_ratio=0.2)], run_time=1.4,
                    into=cr._phase("env"))
            cr.show(self, *groups[-1], src51, anims=[FadeIn(VGroup(*groups[-1]), shift=RIGHT * 0.2),
                                                     FadeIn(src51, shift=UP * 0.1)],
                    run_time=0.5, into=cr._phase("env"))
        self.play(FadeOut(ref), *[FadeOut(b) for b in bars[4:]], run_time=0.4)
        self.remove(ref, *bars[4:])

        # ========================================================== 1. the wires (lines 34-43)
        el = {35: "/var/run/docker.sock", 38: '"$SSH_DIR/.ssh"', 39: '"$(pwd)/docker_config.json":/root',
              40: '"$(pwd)/pulumi-plugins"', 41: '"$BASE_DIR/../api-service"',
              42: '"$BASE_DIR/../frontend-react"', 43: '"$BASE_DIR/../vector-db"'}
        p2 = code("src/deployment/docker-shell.sh", 34, 43, font_size=20, dedent=True,
                  shown="docker-shell.sh", cuts={34: "--rm"}, elide=el)
        p2.move_to([0, -0.35, 0]).align_to(p1, LEFT)
        assert p2.get_right()[0] < 6.58 and p2.get_top()[1] < PIC_TOP, (p2.get_right(), p2.get_top())
        mount_line = (35, 36, 37, 39, 41, 42, 43)
        helpers = tool_chip("credential helpers", mono_font=False)
        helpers.next_to(p2, DOWN, buff=0.14).align_to(p2, RIGHT)
        keep_inside(helpers)

        def wire(i, extra=()):
            bar = line_bar(p2.code, mount_line[i] - 34, cr.WIRE_COL[i], 0.22)
            self.play(FadeIn(bar), *extra, run_time=0.25)
            self.remove(bar)
            p2.add(bar)
            self.add(p2)
            return cr.wire(self, i, 0.45)

        with self.voiceover(SAY[1]) as vo:
            cr.clear(self, "env", run_time=0.4)
            self.play(FadeOut(p1, shift=UP * 0.5), run_time=0.35)     # scroll: out, then in (no overlap)
            self.remove(p1)
            self.play(FadeIn(p2, shift=UP * 0.5), run_time=0.4)
            vo.wait_until("They mount the Docker socket")
            w0 = wire(0)
            vo.wait_until("so it builds on your Docker")
            self.play(Indicate(w0[0], color=INK, scale_factor=1.12), run_time=0.6)
            cr.heal(self)
            vo.wait_until("then deployment as slash app")
            wire(1)
            vo.wait_until("the secrets")
            w2 = wire(2)
            self.play(Indicate(w2[1], color=COST, scale_factor=1.05), run_time=0.5)
            cr.heal(self)
            vo.wait_until("a Docker config")
            wire(3)
            self.play(FadeIn(helpers, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and the three service folders")
            for i in (4, 5, 6):
                wire(i)

        # ========================================================== 2. cd, set the project
        t = laptop_term(8, P_DEPLOY)
        rc = readme_card(266, readme_lines(266, 266))
        rc.move_to([0, 2.05, 0]).align_to([-6.45, 0, 0], LEFT)
        er = erratum_tag().next_to(rc, RIGHT, buff=0.3)
        fix_ar = Arrow(ORIGIN, RIGHT * 0.9, color=S.GREY, stroke_width=3, buff=0,
                       max_tip_length_to_length_ratio=0.3).next_to(er, RIGHT, buff=0.2)
        fix = grey_chip("src/deployment", mono_font=True).next_to(fix_ar, RIGHT, buff=0.2)
        assert fix.get_right()[0] < 6.5 and rc.get_bottom()[1] > t.box.get_top()[1] + 0.1, rc.get_bottom()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(cr, p2, helpers)), run_time=0.5)
            self.remove(cr, p2, helpers)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(rc, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(er), GrowArrow(fix_ar), FadeIn(fix, shift=RIGHT * 0.15), run_time=0.6)
            cd_prompt(self, t, P_DEPLOY, color=TURN)
            vo.wait_until("In docker-shell.sh")
            self.play(track(trk, 3, "or edit the file"), run_time=0.4)
            r1 = type_cmd(self, t, B01.cmd, type_time=1.6, soft=True)
            xt_bar = mark_extra(self, t, r1, extra_row("or edit the file"))
            o1 = out(self, t, [B01.line(2)], wrap=True, run_time=0.4)
            vo.wait_until("set GCP project to your project ID")
            g = substring(o1[0], '"your-gcp-project"')
            self.play(g.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(g, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            vo.wait_until("ours is a placeholder")
            ph = row_tag("ours: a placeholder")
            pin(self, o1[-1], beside(ph, o1[-1]))

        # ========================================================== 3. the first run: 404, pull access denied
        with self.voiceover(SAY[3]) as vo:
            anims = [FadeOut(VGroup(rc, er, fix_ar, fix)), track(trk, 3)]
            if xt_bar is not None:
                anims.append(FadeOut(xt_bar))
            resize(self, t, 13, extra=anims, run_time=0.6)
            self.remove(rc, er, fix_ar, fix)
            if xt_bar is not None:
                self.remove(xt_bar)
            type_capture(self, t, B02, type_time=0.6)
            out(self, t, [B02.line(2), B02.crop(3, "(6/20)"), B02.line(12)], wrap=True, run_time=0.5)
            vo.wait_until("Downloads answer 404 not found")
            r404 = out(self, t, ["…"] + [(e404(n), ERR) for n in (135, 136, 137)] + ["…"], run_time=0.6)
            self.play(*[Indicate(substring(r, "404  Not Found"), color=ERR, scale_factor=1.08)
                        for r in r404[1:4]], run_time=0.6)
            self.add(t)
            vo.wait_until("the build stops")
            out(self, t, [(B02.line(166), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("and the script runs the container anyway")
            out(self, t, [(B02.line(167), AMBER)], run_time=0.4)
            vo.wait_until("pull access denied")
            pa = out(self, t, [(B02.line(168), ERR)], wrap=True, run_time=0.5)
            self.play(Indicate(substring(pa[0], "pull access denied"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t)

        # ========================================================== 4. line 4: bullseye -> bookworm
        df = code("src/deployment/Dockerfile", 3, 12, font_size=20,
                  cuts={3: "# Use the official", 6: "# Set the", 7: "DEBIAN_FRONTEND=", 8: "UV_PROJECT_",
                        12: "install -y curl"})
        df.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.78, 0], UP)
        assert df.get_bottom()[1] > strip_top(3) + 0.1, df.get_bottom()
        mb = MiniBox(1.25, 6.45)
        er4 = erratum_tag().move_to([0, df.code.code_lines[1].get_y(), 0]).align_to([df.get_right()[0] + 0.2, 0, 0], LEFT)
        assert er4.get_right()[0] < mb.left() - 0.1, er4.get_right()
        # the ORANGE shelf and the GREY-dashed archive (bottom right)
        sh_label = label("Debian 11 · bullseye-security", 20, SHARED).move_to([-0.2, 0.62, 0], aligned_edge=LEFT)
        sh_line = Line([-0.25, -0.55, 0], [2.7, -0.55, 0], color=SHARED, stroke_width=4)
        pkgs = [RoundedRectangle(width=0.5, height=0.5, corner_radius=0.05, stroke_color=SHARED, stroke_width=2)
                .set_fill(tint(SHARED, 0.25), 1).move_to([0.15 + 0.68 * i, -0.28, 0]) for i in range(4)]
        arch = DashedVMobject(RoundedRectangle(width=2.7, height=1.5, corner_radius=0.1), num_dashes=40,
                              dashed_ratio=0.5).set_stroke(S.GREY, 2.5).move_to([4.95, -0.45, 0])
        arch_t = label("archive", 20, S.GREY).move_to(arch.get_top() + DOWN * 0.3)
        slots = [arch.get_bottom() + np.array([-0.95 + 0.63 * i, 0.4, 0]) for i in range(4)]
        assert sh_label.get_right()[0] < 6.5 and arch.get_right()[0] < 6.5
        with self.voiceover(SAY[4]) as vo:
            # the strip keeps the error's HEAD (b02:168 cropped), not the tail of its wrapped rows
            resize(self, t, 3, keep=0, run_time=0.6)
            out(self, t, [(B02.crop(168, "cheese-app-deployment", " …"), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("The cause is line 4")
            self.play(FadeIn(df, shift=RIGHT * 0.2), FadeIn(mb), run_time=0.6)
            b4 = line_bar(df.code, 1, ERR, 0.25)
            self.play(FadeIn(b4), run_time=0.3)
            mb.bricks(self)
            mb.brick(self, "line 4", "red")
            vo.wait_until("the base image is Debian 11")
            bs = code_span(df.code, 1, "bullseye")
            self.play(bs.animate.set_color(ERR), FadeIn(er4, shift=LEFT * 0.1), run_time=0.4)
            self.add(df)
            b11 = [line_bar(df.code, k, SHARED, 0.22) for k in (8, 9)]
            self.play(*[FadeIn(b) for b in b11], FadeIn(sh_label, shift=UP * 0.1), Create(sh_line),
                      LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in pkgs], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("whose security updates moved to an archive")
            self.play(Create(arch), FadeIn(arch_t), run_time=0.5)
            self.play(LaggedStart(*[p.animate(path_arc=-0.6).move_to(s).set_stroke(S.GREY).set_fill(tint(S.GREY, 0.2), 1)
                                    for p, s in zip(pkgs, slots)], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("Fix 1")
            gone = VGroup(df, b4, *b11, er4, sh_label, sh_line, *pkgs, arch, arch_t)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(gone, *gone)
            resize(self, t, 9, extra=[mb.animate.shift(LEFT * (mb.left() + 6.45)), track(trk, 3, True)],
                   run_time=0.7)
            mb.heal(self)
            ra = type_cmd(self, t, B02A.cmd, type_time=1.4, soft=True)
            ea = mark_extra(self, t, ra, extra_row())
            vo.wait_until("change bullseye to bookworm")
            oa = out(self, t, [(B02A.line(2), OWN)], run_time=0.4)[0]
            mb.brick(self, "line 4", "green",
                     extra=[Indicate(substring(oa, "bookworm"), color=OWN, scale_factor=1.15)])
            self.add(t)

        # ========================================================== 5. second run: google-cloud-sdk is gone
        inset = code("src/deployment/Dockerfile", 29, 30, font_size=20, cuts={30: "google-cloud-sdk"})
        inset.move_to([0, (BAND_Y0 + BAND_Y1) / 2, 0]).align_to([6.4, 0, 0], RIGHT)
        assert inset.get_left()[0] > mb.frame.get_right()[0] + 0.1 and inset.get_bottom()[1] > t.box.get_top()[1]
        with self.voiceover(SAY[5]) as vo:
            self.play(track(trk, 3), *([FadeOut(ea)] if ea is not None else []), run_time=0.4)
            if ea is not None:
                self.remove(ea)
            type_capture(self, t, B02B, type_time=0.6)
            steps = out(self, t, [B02B.crop(3, "(12/20)")] + [(crop_row(B02B.line(n)), OWN) for n in range(12, 18)],
                        run_time=0.8, lag=0.1)
            assert len(steps) == 7
            vo.wait_until("Now it stops at line 29")
            out(self, t, [(B02B.line(18), ERR)], wrap=True, run_time=0.4)
            self.play(FadeIn(inset, shift=LEFT * 0.2), run_time=0.4)
            b30 = line_bar(inset.code, 1, ERR, 0.25)
            self.play(FadeIn(b30), run_time=0.3)
            mb.brick(self, "lines 29–30", "red")
            vo.wait_until("google cloud SDK has no installation candidate")
            r5 = out(self, t, ["…", (B02B.line(34), AMBER), (B02B.line(37), OWN), (B02B.line(38), OWN),
                               (B02B.line(46), ERR), (B02B.line(47), ERR)], wrap=True, run_time=0.6)
            row46 = [r for r in r5 if "has no installation candidate" in r.text and "'google-cloud-sdk'" in r.text][0]
            self.play(Indicate(substring(row46, "has no installation candidate"), color=ERR, scale_factor=1.08),
                      run_time=0.6)
            self.add(t)
            vo.wait_until("Google renamed it")
            row37 = [r for r in r5 if "replace it:" in r.text][0]
            row38 = [r for r in r5 if r.text.endswith("google-cloud-cli")][0]
            self.play(Indicate(substring(row37, "However the following packages replace it:"), color=OWN,
                               scale_factor=1.05), run_time=0.6)
            self.add(t)
            vo.wait_until("google cloud CLI")
            self.play(Indicate(substring(row38, "google-cloud-cli"), color=OWN, scale_factor=1.2), run_time=0.6)
            self.add(t)

        # ========================================================== 6. fix 2: the real diff
        def diff_item(n):
            s = B02C.line(n)
            if n in (10, 19):
                return (s, ERR)
            if n in (11, 20):
                return (s, OWN)
            return s

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(inset, b30)), track(trk, 3, True), run_time=0.4)
            self.remove(inset, b30)
            rc6 = type_cmd(self, t, B02C.cmd, type_time=1.4, soft=True)
            e6 = mark_extra(self, t, rc6, extra_row())
            vo.wait_until("Here is the real diff")
            h1 = out(self, t, [diff_item(n) for n in DIFF_LINES if n <= 14], wrap=True, run_time=0.6)
            pair1 = [r for r in h1 if r.text.startswith(("-FROM", "+FROM"))]
            self.play(*[Indicate(r, color=r[1].get_color(), scale_factor=1.04) for r in pair1], run_time=0.6)
            self.add(t)
            vo.wait_until("one line each")
            h2 = out(self, t, [diff_item(n) for n in DIFF_LINES if n > 14], wrap=True, run_time=0.6)
            pair2 = [r for r in h2 if r.text.startswith(("-    apt-get", "+    apt-get"))]
            assert len(pair1) == 2 and len(pair2) == 2
            self.play(*[Indicate(r, color=r[1].get_color(), scale_factor=1.03) for r in pair2], run_time=0.6)
            self.add(t)
            mb.brick(self, "lines 29–30", "green")
            vo.wait_until("Pause and make both edits")
            yt6 = on_bar(t, turn_row())
            self.play(FadeIn(yt6), *([FadeOut(e6)] if e6 is not None else []), run_time=0.3)
            if e6 is not None:
                self.remove(e6)
            flash_tag(self, yt6, TURN)

        # ========================================================== 7. third run: builds; the key is refused
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(yt6), track(trk, 3), run_time=0.4)
            self.remove(yt6)
            type_capture(self, t, B02D, type_time=0.6)
            r3 = out(self, t, [(B02D.crop(3, "FINISHED"), OWN), "…", B02D.line(31)], run_time=0.5)
            self.play(Indicate(substring(r3[0], "91.9s"), color=OWN, scale_factor=1.2), run_time=0.6)
            self.add(t)
            vo.wait_until("and the entrypoint starts")
            mb.widen(self)
            mb.lamps(self)
            rv = out(self, t, [B02D.line(34), B02D.line(35)], run_time=0.4)
            pin(self, rv[0], beside(time_row(), rv[0]))
            vo.wait_until("First error")
            out(self, t, [(B02D.line(36), ERR)], wrap=True, run_time=0.6)
            mb.lamp_set(self, 0, "red")
            vo.wait_until("Our key belongs to no account")
            mb.note(self, "our key: made for no account")
            vo.wait_until("yours activates the deployment account")
            self.play(Indicate(mb.lamp_list[0].text, color=TURN, scale_factor=1.12), run_time=0.6)
            mb.heal(self)

        # ========================================================== 8. project, helper, bucket, login
        with self.voiceover(SAY[8]) as vo:
            out(self, t, [(B02D.line(52), OWN), (B02D.line(61), OWN)], run_time=0.4)
            mb.lamp_set(self, 1, "green")
            mb.lamp_set(self, 2, "green")
            vo.wait_until("Then the state bucket")
            out(self, t, [B02D.line(63), B02D.line(65), (B02D.line(66), ERR)], run_time=0.5)
            mb.lamp_set(self, 3, "red")
            vo.wait_until("and Pulumi could not log in")
            out(self, t, [B02D.line(70), (B02D.line(71), ERR)], wrap=True, run_time=0.6)
            mb.lamp_set(self, 4, "red")
            vo.wait_until("Yours creates the bucket the first time")
            rp = out(self, t, [B02D.line(76), B02D.line(77).rstrip()], run_time=0.4)
            self.play(substring(rp[1], TOOLBOX_ID).animate.set_color(S.GREY), run_time=0.3)
            self.add(t)
            mb.note(self, "with your key: five GREEN lamps")
            vo.wait_until("and leaves you here")
            self.play(Indicate(rp[1], color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(t)

        # ========================================================== 9. check the tools
        rp[1].bare = True                       # the printed prompt is where the next command types
        t.set_prompt(P_TOOLBOX)
        note9 = tool_chip("apt picks Google's kubectl package (1:592) over pkgs.k8s.io 1.34", mono_font=False)
        note9.move_to([0, 2.15, 0]).align_to([6.4, 0, 0], RIGHT)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(mb), track(trk, 4), retitle(t, T_TOOLBOX), run_time=0.6)
            self.remove(mb)
            vo.wait_until("Check the tools")
            type_capture(self, t, B03, type_time=0.6)
            g3 = out(self, t, [B03.line(2), "…", B03.line(11)], run_time=0.4)
            pin(self, g3[0], beside(time_row(), g3[0]))
            vo.wait_until("Pulumi")
            type_capture(self, t, B04, type_time=0.5)
            g4 = out(self, t, [B04.line(2)], run_time=0.3)
            pin(self, g4[0], beside(time_row(), g4[0]))
            vo.wait_until("and kubectl")
            type_capture(self, t, B05, type_time=0.6)
            g5 = out(self, t, [B05.line(2)], run_time=0.3)[0]
            vo.wait_until("One surprise")
            dv = substring(g5, "v1.35.9-dispatcher")
            self.play(dv.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(dv, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            vo.wait_until("newer than the Dockerfile pins")
            ghost = row_tag([("Dockerfile:33 ·", "label"), ("K8S_MINOR=1.34", "mono")], S.GREY)
            pin(self, g5, beside(ghost, g5))
            vo.wait_until("because Google's apt repository")
            a0 = np.array([note9.get_right()[0] - 0.5, note9.get_bottom()[1] - 0.05, 0])
            a1 = ghost.get_right() + RIGHT * 0.1
            ar9 = CurvedArrow(a0, a1, angle=-0.5, color=TOOL, stroke_width=3, tip_length=0.2)
            self.play(FadeIn(note9, shift=DOWN * 0.1), run_time=0.5)
            self.play(Create(ar9), run_time=0.6)
            vo.wait_until("with a higher version")
            flash_tag(self, note9, TOOL, 1.04)
            vo.wait_until("and apt picks it")
            k9 = substring(g3[2], "kubectl 1.35.9")
            self.play(k9.animate.set_color(TOOL), run_time=0.3)
            self.play(Indicate(k9, color=TOOL, scale_factor=1.1), run_time=0.6)
            self.add(t)

        # ========================================================== 10. auth list; the registry; your turn
        rows10 = VGroup(*[mono(s, 20, INK) for s in REGISTRY_CMD]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        reg = outline_box(12.9, 1.55, S.GREY, solid=True, fill_opacity=0.08).move_to([0, (BAND_Y0 + BAND_Y1) / 2, 0])
        reg.fill.set_fill(S.GREY_DARKER, 1)
        rows10.move_to(reg).align_to(reg, LEFT).shift(RIGHT * 0.3 + DOWN * 0.08)
        look = ok_chip("look for: Created repository").move_to(rows10[1]).align_to(reg, RIGHT).shift(LEFT * 0.25)
        x10 = extra_tag("not in the README")
        x10.move_to(reg.get_corner(UR) + np.array([-x10.width / 2 - 0.25, 0, 0]))
        assert look.get_left()[0] > rows10[1].get_right()[0] + 0.2 and x10.get_top()[1] < 3.0
        card10 = VGroup(reg, rows10, look, x10)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(note9, ar9)), run_time=0.4)
            self.remove(note9, ar9)
            vo.wait_until("Last check")
            ra10 = type_capture(self, t, B06, type_time=0.5)[0]
            vo.wait_until("Ours says no credentialed accounts")
            n10 = out(self, t, [(B06.line(3), ERR)], run_time=0.4)[0]
            vo.wait_until("Yours lists the deployment account as active")
            room10 = t.box.get_right()[0] - 0.1 - (n10.strut.get_right()[0] + 0.45)
            for cand in ("deployment@<your project>.iam.gserviceaccount.com", "deployment@<your project>.iam…",
                         "deployment@<your project>…", "deployment@…"):
                yours = row_tag([("yours: *", "label"), (cand, "mono")], S.GREY)
                if yours.width < room10:
                    break
            pin(self, n10, beside(yours, n10))
            vo.wait_until("check the file name in secrets")
            flash_tag(self, yours, INK)
            vo.wait_until("Then create the registry repository")
            self.play(track(trk, 4, True), FadeIn(VGroup(reg, rows10), shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(x10), FadeIn(look, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("Pause and run both")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt), reg.frame.animate.set_stroke(TURN), run_time=0.4)
            flash_tag(self, yt, TURN)
            assert ra10 is not None

        self.play(FadeOut(VGroup(trk, t, card10, yt)), run_time=0.6)
        self.remove(trk, t, card10, yt)
        self.wait(0.4)
