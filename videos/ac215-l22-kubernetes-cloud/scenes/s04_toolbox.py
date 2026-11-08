"""S04 · The toolbox, still fixed twice (AC215 L22, the full follow-along). TRACKER [W] 1 (beats 0-1),
2 (beats 2-7), 3 (beats 8-9), 4 (beat 10).
Lecture: 22 · 34 (beat 8 only, while kubectl version meets "no cluster yet").

Beats (script.md "## S04", one voiceover block each):
0. TRACKER [W] 1. Two GREY README cards stacked, 'Deployment with Scaling using Kubernetes' (line 392)
   and 'Create & Deploy Cluster' (436); on "The README keeps this warm-up" the third, 'Create Simple
   Kubernetes Cluster Tutorial' (517), arrives below them; on "The lecture does it first" it slides
   to the top (the other two move down) and the GREY chip 'lecture order: slides 32–40 first' sits
   beside it; on "the gentlest first contact" its frame flashes YELLOW.
1. TRACKER [W] 1. README card 'README.md · lines 521–525' left (the five API names); a schematic
   console right ('console › APIs & Services', tag illustration, no logo) with the same five rows (own spacing),
   each with an 'Enable' button; the buttons tick GREEN one after another (except row 4). On "A small
   slip" README line 524 is struck GREY with an 'erratum' tag and the console's row 4 goes RED; on
   "Enable Artifact Registry instead" row 4 cross-fades into a GREEN 'Artifact Registry API' (beside
   the struck line) and its button ticks.
2. TRACKER [W] 2. Full-width 13-row terminal 'laptop' at …/cheese-app-v3/src$ ('src' flashes on "from
   the S R C folder"): `cd deployment`, the prompt becomes …/src/deployment$ (path flashes); `sh docker-shell.sh` -> TERM(b02: 2 wrap, 12 wrap
   RED, …, 150 + 151 cropped at "404  Not Found" (URL elided, '404  Not Found' RED), …, 166 wrap,
   167, 168 wrap RED); 'pull access denied' flashes RED.
3. The terminal shrinks to a 3-row strip holding the head of b02:168 (cropped after "pull access
   denied", RED). CODE(src/deployment/Dockerfile: 4) top left,
   'python:3.13-slim-bullseye' ORANGE, GREY chip 'bullseye's security pool: gone' beside it; under
   them a GREY card with an 'erratum' tag: 'docker-shell.bat (README:529): not in the repo → use WSL'
   ('use WSL' flashes on "Use WSL").
4. TRACKER [W] 2 · extra. The terminal grows to 10 rows. b02a line 1 typed (soft-wrapped), 'extra' beside it
   -> TERM(b02a: 10, 11, 19 wrap, 20 wrap): 10 and 19 RED, 11 and 20 GREEN; each pair flashes on its
   phrase; on "with its GKE auth plugin" 'google-cloud-cli-gke-gcloud-auth-plugin' turns PURPLE and
   flashes again on "Every kubectl call".
5. TRACKER [W] 2 · extra. b01 line 1 typed (folds) -> TERM(b01: 2 wrap); 'your-gcp-project' YELLOW;
   GREY ring on the README's 'ac215-project' in the typed command with the GREY default_tag above the
   terminal; the GREY row tag 'L20 · README:267 · your project id' beside the output.
6. TRACKER [W] 2. `sh docker-shell.sh` -> TERM(b03: 3 crop "FINISHED", …, 31 TEAL, 36 wrap RED,
   70 wrap, 71 crop "state backend" RED, 77 = the toolbox prompt (id GREY)); '92.3s' GREEN with the
   row tag 'Apple Silicon: emulated amd64 · much slower'; the title becomes 'laptop · toolbox'.
7. A YELLOW '▶ your turn' beside the toolbox prompt (flashes).
8. TRACKER [W] 3. LECTURE 22 · 34. `gcloud --version` -> TERM(b10: 2, …, 9, 11) + 'at the time of
   recording'; 'gke-gcloud-auth-plugin' PURPLE; `kubectl version` -> TERM(b11: 2, 4 wrap ORANGE);
   top right the small V1 thumbnail: GREY 'your laptop' with a PURPLE kubectl chip, its arrow to a
   GREY-dashed 'no cluster yet' box; a YELLOW dot runs along the arrow and comes back RED, a RED
   cross over the arrow; `kubectl version --client` -> TERM(b12: 2). The lecture tag fades with the thumbnail.
9. 'v1.35.9-dispatcher' (b12:2) YELLOW and flashes. Top: CODE(src/deployment/Dockerfile: 33) with
   'K8S_MINOR=1.34' YELLOW, beside it the GREY two-row chip "Google's own kubectl package wins /
   → a dispatcher that picks a matching client" with its 'erratum' tag.
10. TRACKER [W] 4. `gcloud auth list` -> TERM(b13: 3) RED; the GREY chip 'yours:
   deployment@<your project>.iam.gserviceaccount.com · active' above the terminal. Fade; empty frame.

Deviations from SHOW:
- Beat 1: the console lists the API names itself (the README card on the left carries the README's
  wording); the GREEN replacement takes the console's row 4, right of the struck README line (the
  console rows are taller than README lines, so they are spaced on their own). Row 4's 'Enable' does not tick until the replacement is there.
- Beat 2: b02:150-151 keep 'Failed to fetch', 'debian-security/pool/' and '404  Not Found' with the
  rest of the URL elided (one row each, as L20 did; the proxy column is cropped as the script says).
- Beat 4: b02a's command is soft-wrapped at the row edge like a real terminal (no ' \'): its quoted sed
  expression is longer than a row, and folding with ' \' would put a backslash inside the quotes
  (the rows join back to the exact command). b01 folds with ' \' as the script says.
- Beat 5: the default_tag sits just above the terminal (the folded command row has no room beside it)
  with a GREY ring on 'ac215-project' in the typed command.
- Beat 6: b03:3 is cropped after 'FINISHED' (the right-aligned 'docker:default' column); b03:70 is
  79 characters and wraps; b03:77 is printed only up to the prompt (its ' exit' was typed later).
- Beat 8: the "no cluster yet" thumbnail sits top right above the terminal (there is no room under
  line 4 inside a full-width terminal).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]
assert len(SAY) == SAY_COUNT["S04"] == 11

DOCKERFILE = "src/deployment/Dockerfile"

# ------------------------------------------------------------------ the real sources (checked)
B01, B02, B02A, B03 = capture("b01"), capture("b02"), capture("b02a"), capture("b03")
B10, B11, B12, B13 = capture("b10"), capture("b11"), capture("b12"), capture("b13")

assert B01.cmd.startswith("sed -i 's/\"ac215-project\" # Change/\"your-gcp-project\" # Change/' docker-shell.sh")
assert B01.line(2) == '13:export GCP_PROJECT="your-gcp-project" # Change to your GCP Project'
assert B02.cmd == "sh docker-shell.sh" and B03.cmd == B02.cmd
assert B02.line(2).startswith("Container 'cheese-app-deployment' is not running.")
assert B02.line(12).startswith(" => ERROR [ 2/16] RUN apt-get update")
assert all("debian-security/pool/" in B02.line(n) and "404  Not Found" in B02.line(n) for n in (150, 151))
assert B02.line(166).startswith("ERROR: failed to build: failed to solve:")
assert B02.line(167) == "Unable to find image 'cheese-app-deployment:latest' locally"
assert B02.line(168).startswith("docker: Error response from daemon: pull access denied")
assert B02A.cmd.startswith("sed -i 's/^FROM python:3.13-slim-bullseye/FROM python:3.13-slim-bookworm/;")
assert B02A.line(10) == "-FROM python:3.13-slim-bullseye" and B02A.line(11) == "+FROM python:3.13-slim-bookworm"
assert B02A.line(19).startswith("-    apt-get install -y google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin")
assert B02A.line(20).startswith("+    apt-get install -y google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin")
assert B03.line(3).startswith("[+] Building 92.3s (21/21) FINISHED")
assert B03.line(31) == "Container is running!!!"
assert B03.line(36).startswith("ERROR: (gcloud.auth.activate-service-account)")
assert B03.line(70).startswith("Logging into Pulumi using GCS bucket")
assert B03.line(71).startswith("error: could not log in to the state backend")
assert B03.crop(77, "#") == P_TOOLBOX
TOOLBOX_ID = P_TOOLBOX.split("@", 1)[1].split(":", 1)[0]
assert re.fullmatch(r"[0-9a-f]{12}", TOOLBOX_ID)
assert B10.cmd == "gcloud --version" and B10.line(2) == "Google Cloud SDK 592.0.0"
assert B10.line(9) == "gke-gcloud-auth-plugin 0.5.21" and B10.line(11) == "kubectl 1.35.9"
assert B11.cmd == "kubectl version" and B11.line(2) == "Client Version: v1.35.9-dispatcher"
assert B11.line(4).startswith("The connection to the server localhost:8080 was refused")
assert B12.cmd == "kubectl version --client" and B12.line(2) == "Client Version: v1.35.9-dispatcher"
assert B13.cmd == "gcloud auth list" and B13.line(3) == "No credentialed accounts."
assert excerpt(DOCKERFILE, 4, 4) == "FROM python:3.13-slim-bullseye"
assert excerpt(DOCKERFILE, 33, 33) == "ARG K8S_MINOR=1.34"
assert readme(392) == "## Deployment with Scaling using Kubernetes"
assert readme(436) == "## Create & Deploy Cluster"
assert readme(517).rstrip() == "## Create Simple Kubernetes Cluster Tutorial"
assert readme(267).startswith("- Go into `docker-shell.sh` and change `GCP_PROJECT` to your project id")
assert "docker-shell.bat" in readme(529)
README_CD = readme_rows(528, 528)[0].strip("- `")
assert README_CD == "cd deployment", README_CD
APIS = [readme(n).lstrip("* ").strip() for n in range(521, 526)]
assert APIS == ["Compute Engine API", "Service Usage API", "Cloud Resource Manager API",
                "Google Container Registry API", "Kubernetes Engine API"], APIS


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


def edge_flash(m, color=TURN, width: float = 6):
    """ANIM: an outline flashes `color` and returns."""
    return m.animate(rate_func=there_and_back).set_stroke(color, width)


class Toolbox(VoiceScene):
    def construct(self):
        # ========================================================== 0. the section order
        trk = tracker_w(1)
        heads = [(392, "Deployment with Scaling using Kubernetes"), (436, "Create & Deploy Cluster"),
                 (517, "Create Simple Kubernetes Cluster Tutorial")]
        CW = max(readme_card(n, h).width for n, h in heads)
        cards = [readme_card(n, h, card_w=CW) for n, h in heads]
        ys = [1.55, 0.05, -1.45]
        CX = -6.45 + CW / 2
        for c, y in zip(cards, ys):
            c.move_to([CX, y, 0])
        order = grey_chip("lecture order: slides 32–40 first")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(cards[0], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.5)
            vo.wait_until("keeps this warm-up")
            self.play(FadeIn(cards[2], shift=UP * 0.2), run_time=0.6)
            self.play(edge_flash(cards[2].frame, INK), run_time=0.6)
            vo.wait_until("The lecture does it first")
            self.play(cards[2].animate.move_to([CX, ys[0], 0]),
                      cards[0].animate.move_to([CX, ys[1], 0]),
                      cards[1].animate.move_to([CX, ys[2], 0]), run_time=0.9)
            order.next_to(cards[2], RIGHT, buff=0.25)
            assert order.get_right()[0] < 6.5, order.get_right()
            self.play(FadeIn(order, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("the gentlest first contact")
            self.play(edge_flash(cards[2].frame), run_time=0.8)
            self.play(Indicate(cards[2].body, color=TURN, scale_factor=1.04), run_time=0.7)

        # ========================================================== 1. five APIs (one has gone)
        rc = readme_card((521, 525), "\n".join(APIS))
        rc.move_to([0, 0.3, 0]).align_to([-6.45, 0, 0], LEFT)
        crumbs = VGroup(label("console", 20, INK), label("›", 20, S.GREY), label("APIs & Services", 20, INK))
        crumbs.arrange(RIGHT, buff=0.12)
        rows, buttons = [], []
        ROW_W = 5.8
        for i, name in enumerate(APIS):
            t = label(name, 20, INK)
            b = RoundedRectangle(width=ROW_W, height=0.48, corner_radius=0.06, stroke_color=CLOUD,
                                 stroke_width=2).set_fill(tint(CLOUD, 0.12), 1)
            bt = chip("Enable", CLOUD, size=20)
            r = VGroup(b, t, bt)
            t.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.2)
            bt.move_to(b).align_to(b, RIGHT).shift(LEFT * 0.1)
            assert t.get_right()[0] < bt.get_left()[0] - 0.15, name
            r.box, r.text, r.button = b, t, bt
            rows.append(r)
            buttons.append(bt)
        # the console's rows, centred on the README card's height
        cv_x0 = rc.frame.get_right()[0] + 0.55
        rows_g = VGroup(*rows).arrange(DOWN, buff=0.1)
        rows_g.move_to([cv_x0 + 0.35 + ROW_W / 2, rc.body.get_y() - 0.2, 0])
        crumbs.next_to(rows_g, UP, buff=0.32).align_to(rows_g, LEFT)
        inner = VGroup(crumbs, rows_g)
        cframe = box(ROW_W + 0.7, inner.height + 0.75, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        cframe.move_to(inner).align_to([cv_x0, 0, 0], LEFT).shift(DOWN * 0.04)
        ctag = illustration_tag()
        ctag.move_to(cframe.get_corner(UR) + np.array([-ctag.width / 2 - 0.2, 0, 0]))
        console = VGroup(cframe, crumbs, rows_g, ctag)
        assert cframe.get_right()[0] < 6.5, cframe.get_right()
        assert cframe.get_top()[1] < PIC_TOP and rc.get_top()[1] < PIC_TOP
        slip_line = rc.body[3]
        st = strike(slip_line, S.GREY)
        er1 = erratum_tag()
        er1.next_to(rc.frame, DOWN, buff=0.12).align_to(rc.frame, RIGHT)
        new_t = label("Artifact Registry API", 20, OWN).move_to(rows[3].text, aligned_edge=LEFT)
        ticks = []
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(*cards, order)), run_time=0.5)
            self.remove(*cards, order)
            self.play(FadeIn(rc, shift=RIGHT * 0.2), FadeIn(console, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("enable five APIs")
            for i in (0, 1, 2, 4):
                ck = check_glyph(0.28, OWN).move_to(buttons[i])
                ticks.append(ck)
                self.play(buttons[i].box.animate.set_stroke(OWN).set_fill(tint(OWN, 0.3), 1),
                          FadeOut(buttons[i].text), Create(ck), run_time=0.45)
            vo.wait_until("A small slip")
            self.play(Create(st), slip_line.animate.set_color(S.GREY), FadeIn(er1), run_time=0.6)
            self.play(rows[3].box.animate.set_stroke(ERR), rows[3].text.animate.set_color(ERR), run_time=0.4)
            vo.wait_until("has been shut down")
            self.play(Indicate(rows[3].text, color=ERR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Enable Artifact Registry instead")
            self.play(FadeOut(rows[3].text), FadeIn(new_t),
                      rows[3].box.animate.set_stroke(OWN), run_time=0.6)
            ck = check_glyph(0.28, OWN).move_to(buttons[3])
            ticks.append(ck)
            self.play(buttons[3].box.animate.set_stroke(OWN).set_fill(tint(OWN, 0.3), 1),
                      FadeOut(buttons[3].text), Create(ck), run_time=0.45)
            self.play(Indicate(new_t, color=OWN, scale_factor=1.08), run_time=0.6)
        gone1 = VGroup(rc, st, er1, cframe, crumbs, ctag, new_t, *ticks,
                       *[r.box for r in rows], *[rows[i].text for i in (0, 1, 2, 4)], *[b.box for b in buttons])

        # ========================================================== 2. cd, sh docker-shell.sh: it fails
        t = laptop_term(13, P_SRC)
        assert t.box.get_top()[1] < TRACK_BOTTOM - 0.1, t.box.get_top()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(gone1), track(trk, 2), run_time=0.6)
            self.remove(gone1, *gone1)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            src = bare_prompt(self, t)
            vo.wait_until("from the S R C folder")
            self.play(Indicate(substring(src, "src"), color=TURN, scale_factor=1.25), run_time=0.7)
            self.add(t)
            vo.wait_until("change into deployment")
            type_cmd(self, t, README_CD, type_time=0.6)
            cd_prompt(self, t, P_DEPLOY, color=TURN)
            vo.wait_until("and run docker-shell.sh")
            type_capture(self, t, B02, type_time=0.6)
            out(self, t, [B02.line(2), (B02.line(12), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("As committed, it fails")
            r404 = out(self, t, ["…", e404(150), e404(151), "…"], run_time=0.5)
            vo.wait_until("404 Not Found from Debian")
            hits = [substring(r, "404  Not Found") for r in r404[1:3]]
            self.play(*[h.animate.set_color(ERR) for h in hits], run_time=0.3)
            self.play(*[Indicate(h, color=ERR, scale_factor=1.1) for h in hits], run_time=0.6)
            self.add(t)
            out(self, t, [(B02.line(166), ERR), B02.line(167)], wrap=True, run_time=0.5)
            vo.wait_until("then pull access denied")
            pa = out(self, t, [(B02.line(168), ERR)], wrap=True, run_time=0.5)
            self.play(Indicate(substring(pa[0], "pull access denied"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t)

        # ========================================================== 3. bullseye; no .bat
        df4 = code(DOCKERFILE, 4)
        df4.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.6, 0], UP)
        gone_chip = grey_chip("bullseye's security pool: gone")
        gone_chip.next_to(df4, RIGHT, buff=0.3)
        assert gone_chip.get_right()[0] < 6.5, gone_chip.get_right()
        bat_row = VGroup(mono("docker-shell.bat", 22, INK), label("(README:529): not in the repo", 22, INK),
                         label("→ use WSL", 22, OWN)).arrange(RIGHT, buff=0.18)
        bat = card([bat_row])
        bat.move_to([0, 0, 0]).align_to(df4, LEFT).align_to([0, df4.get_bottom()[1] - 0.45, 0], UP)
        er3 = erratum_tag()
        er3.move_to(bat.frame.get_corner(UR) + np.array([-er3.width / 2 - 0.2, 0, 0]))
        assert bat.get_right()[0] < 6.5 and bat.get_bottom()[1] > strip_top(3) + 0.15, bat.get_bottom()
        with self.voiceover(SAY[3]) as vo:
            resize(self, t, 3, keep=0, run_time=0.6)
            out(self, t, [(B02.crop(168, "pull access denied", " …"), ERR)], run_time=0.4)
            vo.wait_until("the base image is Debian bullseye")
            self.play(FadeIn(df4, shift=RIGHT * 0.2), run_time=0.5)
            bs = code_span(df4.code, 0, "python:3.13-slim-bullseye")
            self.play(bs.animate.set_color(SHARED), run_time=0.4)
            self.play(Indicate(bs, color=SHARED, scale_factor=1.08), run_time=0.6)
            self.add(df4)
            vo.wait_until("whose security packages are gone")
            self.play(FadeIn(gone_chip, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("On Windows")
            self.play(FadeIn(bat, shift=UP * 0.15), FadeIn(er3), run_time=0.6)
            vo.wait_until("Use WSL")
            self.play(Indicate(bat_row[2], color=OWN, scale_factor=1.12), run_time=0.7)
            self.add(bat, er3)                 # re-seat the card, its tag on top

        # ========================================================== 4. the two one-line fixes (b02a)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(df4, gone_chip, bat, er3)), run_time=0.4)
            self.remove(df4, gone_chip, bat, er3)
            resize(self, t, 10, extra=[track(trk, 2, True)], run_time=0.6)
            assert B02A.k == 1 and B01.k == 1
            ra = type_cmd(self, t, B02A.cmd, type_time=1.4, soft=True)
            ea = mark_extra(self, t, ra, extra_row())
            vo.wait_until("Bullseye becomes bookworm")
            d1 = out(self, t, [(B02A.line(10), ERR), (B02A.line(11), OWN)], run_time=0.4)
            self.play(Indicate(substring(d1[0], "bullseye"), color=ERR, scale_factor=1.15),
                      Indicate(substring(d1[1], "bookworm"), color=OWN, scale_factor=1.15), run_time=0.7)
            self.add(t)
            vo.wait_until("and google cloud SDK becomes google cloud CLI")
            d2 = out(self, t, [(B02A.line(19), ERR), (B02A.line(20), OWN)], wrap=True, run_time=0.5)
            r19 = [r for r in d2 if r.text.startswith("-    apt-get")][0]
            r20 = [r for r in d2 if r.text.startswith("+    apt-get")][0]
            self.play(Indicate(substring(r19, "google-cloud-sdk"), color=ERR, scale_factor=1.12),
                      Indicate(substring(r20, "google-cloud-cli"), color=OWN, scale_factor=1.12), run_time=0.7)
            self.add(t)
            vo.wait_until("with its GKE auth plugin")
            plug_row = [r for r in d2 if "google-cloud-cli-gke-gcloud-auth-plugin" in r.text][0]
            plug = substring(plug_row, "google-cloud-cli-gke-gcloud-auth-plugin")
            self.play(plug.animate.set_color(TOOL), run_time=0.4)
            self.play(Indicate(plug, color=TOOL, scale_factor=1.03), run_time=0.6)
            self.add(t)
            vo.wait_until("Every kubectl call to GKE")
            self.play(Indicate(plug, color=TOOL, scale_factor=1.03), run_time=0.7)
            self.add(t)

        # ========================================================== 5. your project on line 13 (b01)
        with self.voiceover(SAY[5]) as vo:
            if ea is not None:
                self.play(FadeOut(ea), run_time=0.3)
                self.remove(ea)
            r1 = type_capture(self, t, B01, type_time=1.2)[0]
            e1 = mark_extra(self, t, r1, extra_row())
            o1 = out(self, t, [B01.line(2)], wrap=True, run_time=0.4)
            vo.wait_until("put your project")
            ph = substring(o1[0], '"your-gcp-project"')
            self.play(ph.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(ph, color=TURN, scale_factor=1.12), run_time=0.5)
            self.add(t)
            ac_row = [r for r in rows_of(r1) if '"ac215-project"' in r.text][0]
            ac = substring(ac_row, '"ac215-project"')
            ac_ring = ring(ac, S.GREY, buff=0.05, stroke=2.5)
            dft = under_term(t, default_tag())
            vo.wait_until("on line 13 of docker-shell.sh")
            l20 = row_tag("L20 · README:267 · your project id")
            pin(self, o1[-1], beside(l20, o1[-1]))
            self.play(Create(ac_ring), FadeIn(dft, shift=DOWN * 0.1), run_time=0.5)
            attach(self, ac_row, ac_ring)

        # ========================================================== 6. sh docker-shell.sh again: it builds
        with self.voiceover(SAY[6]) as vo:
            fades = [FadeOut(dft)] + ([FadeOut(e1)] if e1 is not None else [])
            self.play(*fades, track(trk, 2), run_time=0.4)
            self.remove(dft)
            if e1 is not None:
                self.remove(e1)
            type_capture(self, t, B03, type_time=0.6)
            vo.wait_until("it builds in about 92 seconds")
            r3 = out(self, t, [B03.crop(3, "FINISHED")], run_time=0.4)[0]
            sec = substring(r3, "92.3s")
            self.play(sec.animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(sec, color=OWN, scale_factor=1.2), run_time=0.5)
            self.add(t)
            apple = row_tag("Apple Silicon: emulated amd64 · slower")
            pin(self, r3, beside(apple, r3))
            vo.wait_until("and starts")
            out(self, t, ["…", (B03.line(31), CONTAINER)], run_time=0.4)
            vo.wait_until("The login then fails")
            out(self, t, [(B03.line(36), ERR)], wrap=True, run_time=0.6)
            vo.wait_until("because our key belongs to no account")
            out(self, t, [B03.line(70), (B03.crop(71, "state backend"), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("with yours")
            rp = out(self, t, [B03.crop(77, "#")], run_time=0.4)[0]
            self.play(substring(rp, TOOLBOX_ID).animate.set_color(S.GREY), retitle(t, T_TOOLBOX), run_time=0.5)
            self.add(t)
            self.play(Indicate(rp, color=CONTAINER, scale_factor=1.05), run_time=0.6)
            self.add(t)

        # ========================================================== 7. your turn
        rp.bare = True                       # the printed prompt is where the next command types
        t.set_prompt(P_TOOLBOX)
        yt = turn_row()
        with self.voiceover(SAY[7]) as vo:
            pin(self, rp, beside(yt, rp))
            flash_tag(self, yt, TURN)
            vo.wait_until("the rest of this part")
            self.play(Indicate(t.title, color=CONTAINER, scale_factor=1.1), run_time=0.7)
            self.add(t)

        # ========================================================== 8. check the tools (LECTURE 22 · 34)
        ref = lref("34")
        lap = boxed(["your laptop"], LAPTOP, box_w=2.5, box_h=1.15)
        kchip = tool_chip("kubectl")
        lap.move_to([1.55, 2.0, 0])
        lap.text.move_to(lap.frame.get_top() + DOWN * 0.27)
        kchip.move_to(lap.frame.get_bottom() + UP * 0.36)
        empty = boxed(["no cluster yet"], S.GREY, box_w=2.5, box_h=1.15, dashed=True)
        empty.move_to([5.05, 2.0, 0])
        k_ar = Arrow(kchip.get_right(), empty.frame.get_left(), color=TOOL, stroke_width=3, buff=0.12,
                     max_tip_length_to_length_ratio=0.15)
        thumb = VGroup(lap, kchip, k_ar, empty)
        assert empty.get_right()[0] < 6.5 and thumb.get_top()[1] < LREF_BOTTOM - 0.05
        with self.voiceover(SAY[8]) as vo:
            unpin(self, rp, yt, track(trk, 3), FadeIn(ref))
            vo.wait_until("check the tools")
            type_capture(self, t, B10, type_time=0.5)
            g10 = out(self, t, [B10.line(2), "…", B10.line(9), B10.line(11)], run_time=0.5)
            pin(self, g10[0], beside(time_row(), g10[0]))
            vo.wait_until("and its auth plugin are there")
            pl = substring(g10[2], "gke-gcloud-auth-plugin")
            self.play(pl.animate.set_color(TOOL), run_time=0.3)
            self.play(Indicate(pl, color=TOOL, scale_factor=1.1), run_time=0.6)
            self.add(t)
            vo.wait_until("Plain kubectl version")
            type_capture(self, t, B11, type_time=0.5)
            out(self, t, [B11.line(2)], run_time=0.3)
            vo.wait_until("then connection refused")
            g11 = out(self, t, [(B11.line(4), SHARED)], wrap=True, run_time=0.5)
            self.play(Indicate(substring(g11[0], "was refused"), color=SHARED, scale_factor=1.1), run_time=0.6)
            self.add(t)
            vo.wait_until("there is no cluster yet")
            self.play(FadeIn(lap), FadeIn(kchip), run_time=0.4)
            self.play(GrowArrow(k_ar), FadeIn(empty), run_time=0.6)
            vo.wait_until("so the server half has nobody to ask")
            dot = Dot(kchip.get_right() + RIGHT * 0.12, radius=0.09, color=TURN)
            self.play(dot.animate.move_to(empty.frame.get_left() + RIGHT * 0.1), run_time=0.7)
            x_ = cross_glyph(0.3, ERR).move_to(k_ar.get_center() + UP * 0.3)
            self.play(Create(x_), dot.animate.move_to(kchip.get_right() + RIGHT * 0.12).set_color(ERR),
                      run_time=0.7)
            type_capture(self, t, B12, type_time=0.5)
            g12 = out(self, t, [B12.line(2)], run_time=0.3)[0]
        self.play(FadeOut(VGroup(thumb, dot, x_, ref)), run_time=0.5)
        self.remove(thumb, dot, x_, ref)

        # ========================================================== 9. the dispatcher surprise
        df33 = code(DOCKERFILE, 33)
        df33.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, PIC_TOP, 0], UP)
        disp = two_row_chip("Google's own kubectl package wins", "→ a dispatcher that picks a matching client",
                            S.GREY)
        disp.next_to(df33, RIGHT, buff=0.3).align_to(df33, UP)
        er9 = erratum_tag()
        er9.next_to(disp, RIGHT, buff=0.2)
        assert er9.get_right()[0] < 6.5 and disp.get_bottom()[1] > t.box.get_top()[1] + 0.1, \
            (disp.get_right(), disp.get_bottom(), t.box.get_top())
        assert df33.get_bottom()[1] > t.box.get_top()[1] + 0.1
        with self.voiceover(SAY[9]) as vo:
            dv = substring(g12, "v1.35.9-dispatcher")
            self.play(dv.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(dv, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            vo.wait_until("the Dockerfile pins one kubectl version")
            self.play(FadeIn(df33, shift=DOWN * 0.15), run_time=0.5)
            pin_ = code_span(df33.code, 0, "K8S_MINOR=1.34")
            self.play(pin_.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(pin_, color=TURN, scale_factor=1.1), run_time=0.5)
            self.add(df33)
            vo.wait_until("but Google's own package wins")
            self.play(FadeIn(disp, shift=LEFT * 0.15), FadeIn(er9), run_time=0.6)
            vo.wait_until("a dispatcher that matches each cluster")
            self.play(Indicate(disp.text[1], color=INK, scale_factor=1.06),
                      Indicate(dv, color=TURN, scale_factor=1.12), run_time=0.8)
            self.add(t)

        # ========================================================== 10. auth list
        yours = grey_chip("yours: deployment@<your project>.iam.gserviceaccount.com · active")
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(df33, disp, er9)), track(trk, 4), run_time=0.5)
            self.remove(df33, disp, er9)
            vo.wait_until("gcloud auth list")
            type_capture(self, t, B13, type_time=0.5)
            vo.wait_until("Ours says no credentialed accounts")
            n13 = out(self, t, [(B13.line(3), ERR)], run_time=0.4)[0]
            self.play(Indicate(n13, color=ERR, scale_factor=1.06), run_time=0.6)
            self.add(t)
            vo.wait_until("yours lists the deployment service account")
            under_term(t, yours)
            assert yours.get_left()[0] > -6.55 and yours.get_top()[1] < TRACK_BOTTOM - 0.05
            self.play(FadeIn(yours, shift=DOWN * 0.1), run_time=0.5)
            flash_tag(self, yours, INK, 1.05)

        self.play(FadeOut(VGroup(trk, t, yours)), run_time=0.6)
        self.remove(trk, t, yours)
        self.wait(0.4)
