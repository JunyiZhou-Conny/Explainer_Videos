"""S10 · Setup and the images stack (AC215 L22, the full follow-along). TRACKER [D] 1 (beats 0-3),
2-4 (beat 4), 5 (beat 5), 5 · extra (beat 6), 6 / 6 · extra (beats 7-8), 7 (beat 9). No lecture tag.

Beats (script.md "## S10", one voiceover block each):
0. TRACKER [D] 1. README card 'README.md · lines 398–402' (the five API names) left; a schematic
   console 'console › APIs & Services' (Checklist, tag illustration) right with the same five rows:
   they tick GREEN one after another on "enables the five APIs"; on "turn on the Vertex AI API too"
   a sixth row slides in YELLOW, 'Vertex AI API · the API Pods call it' with an 'extra' tag, and
   ticks YELLOW; on "which the API Pods call" its words flash.
1. README card 'README.md · lines 236–259' at the top (the README's three sentences about the two
   accounts; its two 'service account called …' lines flash BLUE, then GREEN, on "the two service
   accounts"); under it two key cards (tag illustration): the BLUE key with a RED rim 'deployment'
   ('the toolbox, Pulumi' / "and here: the nodes' identity", the second line YELLOW on "the nodes'
   identity") and the GREEN key 'gcp-service' ('the API Pods' / 'through Workload Identity' / 'no key
   file in the cluster', the last line flashing on "with no key file").
2. Two GREY console cards (tag illustration): 'IAM › Service accounts › gcp-service › Permissions'
   with the row 'grant deployment · Service Account Admin' (YELLOW on "very likely needs") and the GREY
   two-row chip 'unverified here' / 'follows from the documented roles' (on "we could not test
   this"); under it the GREY card 'or, as project owner:' with the gcloud add-iam-policy-binding
   command (folded). On "And create the registry repository" that card gives way to 'Artifact
   Registry › Create repository' with the row 'cheese-app-repository · location: us' (the name flashes
   on "cheese app repository"), and on "which no code creates" the GREEN card with `gcloud artifacts
   repositories create …` (folded, no output) and the tag 'extra · our spelling'.
3. A 7-row 'laptop' terminal (20 pt, tag 'extra' on its bar): p05:1 typed (folds) -> TERM(p05: 2,
   6–7, 11); 'cheese-app-v3' and 'secrets' flash on "beside the repository", 'deployment.json' YELLOW.
   Above: the two folders side by side, the BLUE/RED key 'deployment.json' drops into 'secrets', and
   the GREY chip 'placeholder key for no account'.
4. TRACKER [D] 2, 3, 4 fast. A 12-row 'laptop' terminal (20 pt) at …/cheese-app-v3/src$: `cd
   deployment` -> (no output, the prompt becomes …/src/deployment$); `sh docker-shell.sh` -> TERM(b03:
   31) and the b03:77 prompt (title -> 'laptop · toolbox'); `gcloud --version` -> TERM(b10: 2); `kubectl
   version` -> TERM(b11: 4 wrap); `kubectl version --client` -> TERM(b12: 2); `gcloud auth list` ->
   TERM(b13: 3) RED. On "if the toolbox is still running" the GREY chip 'docker-shell.sh:23–25 ·
   already running → it attaches' above the terminal.
5. TRACKER [D] 5. The terminal shrinks to 9 rows; the GREY README card 'README.md · line 416' ("This
   step is only required if you have NOT already done this") above it. `cd deploy_images` -> (no
   output); `pulumi stack init dev` -> TERM(b20: 2 wrap) RED; `pulumi config set gcp:project
   ac215-project --stack dev` (folds) -> TERM(b21: 2 wrap) RED, with the row-sized default tag beside
   the folded command and 'ac215-project' ringed GREY. On "Pulumi access token must be set" both
   errors' token names flash; the card flashes on "only if you have not built it before"; on "our
   bucket login failed" the GREY chip 'no bucket login → Pulumi tries its cloud service' beside it.
6. TRACKER [D] 5 · extra. The card leaves, the terminal grows to 14 rows. `pulumi login --local` (tag
   'extra · not for you' on the bar) -> TERM(c00: 2), the container id GREY; `pulumi stack init dev`
   -> TERM(c01: 2) GREEN (flashes on "Now the stack is created"); `pulumi config set gcp:project
   ac215-project --stack dev` -> (no output), the default tag beside it.
7. TRACKER [D] 6. `pulumi preview --stack dev` -> TERM(b22: 2 wrap) RED; TRACKER [D] 6 · extra, the
   same command (tag 'extra' on the bar) -> TERM(c03: 29, 31–33, 40, …, 50–52 wrap, …, 63): line 29
   GREY, 31–33 GREEN (on "three image builds"), 40 ORANGE (on "skipped in a preview"), 50–52 with the
   timestamp YELLOW (on "three tags stamped with the time", not read) and the row-sized default tag
   beside line 50; 63 YELLOW (on "Plus 4 to create"); on "three images and the stack itself" 31–33
   flash and the row tag '+1 · the stack itself' lands beside line 29.
8. The terminal shrinks to a 3-row strip holding c03:50–51. StackPipe ('V5 mini'): three TEAL images
   fly into the BLUE 'Artifact Registry' box and the three PINK '-tags' chips appear; on "deploy k8s
   looks them up" they merge into the PINK pipe 'StackReference organization/deploy-images/dev' to the
   GREEN 'deploy_k8s' box (a scene-local Pipe subclass keeps the crates drawn above the registry
   box, see the report's common.py request); on "to know which images to run" the strip's tag rows and the box flash.
9. TRACKER [D] 7. The pipe leaves, the terminal grows to 5 rows. `pulumi up --stack dev -y` ->
   TERM(b23: 2 wrap) RED. Above the terminal, stacked: the GREY chip 'Apple Silicon: a long build is
   normal' (on "builds and pushes three images"), the GREY-dashed chip 'L20 · the real build, up to the
   push · the API image ≈ 5 GB' (on "Skip it if you did it in lecture 20"), the GREY scene chip 'the
   condition → S11' (on "with one condition we meet next") and the YELLOW '▶ your turn' (on "pause and
   run it"). Fade; empty frame.

Deviations from SHOW:
- Beat 1: the README card quotes three of README:236–259's own lines (the heading and the two
  'service account called …' sentences), not all 24 lines.
- Beat 2: the two console cards and the two command cards do not fit the frame together, so the
  owner-only gcloud card gives way to the Artifact Registry card when the narration turns to it. The
  gcloud command's continuation rows are not indented: its --member row is 75 characters, the widest a
  20 pt mono card can hold inside the frame.
- Beat 3: the terminal is 20 pt (p05:11 is 72 characters); 'placeholder key for no account' sits
  in the folder picture above it (a full-width row has no room beside it). The picture (two folders,
  the key) is ours, so the upper half is not empty for that beat.
- Beat 4: the six commands keep their README order; the 'attaches' remark is a GREY chip quoting
  docker-shell.sh:23–25 (the script's own branch for a running container).
- Beat 5: the README card line 416 is shown with its words (markdown stripped), plus a GREY chip that
  says why the error appears (the narration's "our bucket login failed").
- Beat 7: c03:51 (106 characters, one long token) is broken at the 72-character edge, like a
  terminal, over two rows; the default tag stands beside line 50 (line 51 fills its rows).
- Beat 9: the '▶ your turn' sits above the terminal with the chips (the command row has no room for
  it), and a GREY scene chip 'the condition → S11' marks "one condition we meet next".
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S10"]
assert len(SAY) == SAY_COUNT["S10"] == 10

# ------------------------------------------------------------------ the real sources (checked)
P05 = capture("p05")
B03, B10, B11, B12, B13 = capture("b03"), capture("b10"), capture("b11"), capture("b12"), capture("b13")
B20, B21, B22, B23 = capture("b20"), capture("b21"), capture("b22"), capture("b23")
C00, C01, C02, C03 = capture("c00"), capture("c01"), capture("c02"), capture("c03")

assert P05.cmd.startswith("ls -la; ls -la secrets; ls cheese-app-v3/src/deployment")
assert P05.line(6).endswith(" cheese-app-v3") and P05.line(7).endswith(" secrets")
assert P05.line(11).endswith(" deployment.json")
assert B03.cmd == "sh docker-shell.sh" and B03.line(31) == "Container is running!!!"
assert B03.crop(77, "#") == P_TOOLBOX
TOOLBOX_ID = P_TOOLBOX.split("@", 1)[1].split(":", 1)[0]
assert re.fullmatch(r"[0-9a-f]{12}", TOOLBOX_ID)
assert B10.cmd == "gcloud --version" and B10.line(2) == "Google Cloud SDK 592.0.0"
assert B11.cmd == "kubectl version" and B11.line(4).startswith("The connection to the server localhost:8080")
assert B12.cmd == "kubectl version --client" and B12.line(2) == "Client Version: v1.35.9-dispatcher"
assert B13.cmd == "gcloud auth list" and B13.line(3) == "No credentialed accounts."
TOKEN_ERR = "error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions"
assert B20.cmd == "pulumi stack init dev" and B20.line(2) == TOKEN_ERR
assert B21.cmd == "pulumi config set gcp:project ac215-project --stack dev" and B21.line(2) == TOKEN_ERR
assert B22.cmd == "pulumi preview --stack dev" and B22.line(2) == TOKEN_ERR
assert B23.cmd == "pulumi up --stack dev -y" and B23.line(2) == TOKEN_ERR
assert C00.cmd == "pulumi login --local" and C00.line(2).startswith(f"Logged in to {TOOLBOX_ID} as root")
assert C01.cmd == "pulumi stack init dev" and C01.line(2) == "Created stack 'dev'"
assert C02.cmd == B21.cmd and C02.lines == []
assert C03.cmd == B22.cmd
assert C03.line(29).strip() == "+  pulumi:pulumi:Stack deploy-images-dev create"
assert all(C03.line(n).strip().startswith("+  docker-build:index:Image build-cheese-app-") for n in (31, 32, 33))
assert C03.line(40).strip() == "warning: Skipping preview build because some inputs are unknown."
assert C03.line(50).strip().startswith("cheese-app-api-service-tags")
assert C03.line(51).endswith('cheese-app-api-service:20261107205032"') and C03.line(52).strip() == "]"
assert C03.line(63).strip() == "+ 4 to create"
STAMP = "20261107205032"

# the README (assets/source/README.md @ 3ecef56)
APIS = [readme(n).lstrip("* ").strip() for n in range(398, 403)]
assert APIS == ["Compute Engine API", "Service Usage API", "Cloud Resource Manager API",
                "Artifact Registry API", "Kubernetes Engine API"], APIS
README_CD = readme_rows(405, 405)[0].strip("- `")
assert README_CD == "cd deployment", README_CD
assert "`sh docker-shell.sh`" in readme(406)
assert [readme(n).strip("`") for n in (408, 409, 410)] == [B10.cmd, B11.cmd, B12.cmd]
assert "`gcloud auth list`" in readme(413)
assert readme(416) == "**This step is only required if you have NOT already done this**"
assert readme(417) == "- cd into `deploy_images`"
CD_IMAGES = "cd deploy_images"
assert [readme(n) for n in (420, 421, 428, 433)] == [B20.cmd, B21.cmd, B22.cmd, B23.cmd]
assert readme(236) == "#### Setup GCP Service Account for deployment"
assert 'create a new service account called "deployment"' in readme(238)
assert readme(251) == "- Follow the same process Create another service account called `gcp-service`"
assert "is already running. Shelling into existing container" in excerpt("src/deployment/docker-shell.sh", 24, 24)

IAM_CMD = ["gcloud iam service-accounts add-iam-policy-binding \\",
           "gcp-service@<your project>.iam.gserviceaccount.com \\",
           "--member=serviceAccount:deployment@<your project>.iam.gserviceaccount.com \\",
           "--role=roles/iam.serviceAccountAdmin"]
AR_CMD = ["gcloud artifacts repositories create cheese-app-repository \\",
          "  --repository-format=docker --location=us"]


def mark_extra(scene, t, line, tg):
    """PLAYS: an extra tag beside the command's last row when it fits (pinned: it scrolls with the
    row; returns None), else on the title bar (returns it: the caller fades it)."""
    row = rows_of(line)[-1]
    if row.strut.get_right()[0] + 0.45 + tg.width < t.box.get_right()[0] - 0.1:
        pin(scene, line, beside(tg, line))
        return None
    on_bar(t, tg)
    scene.play(FadeIn(tg), run_time=0.3)
    scene.remove(tg)
    t.add(tg)                        # part of the terminal: a later scene.add(t) keeps it on top
    scene.add(t)
    return tg


def drop_bar_tag(scene, t, tg, *extra):
    """PLAYS: fade a tag that mark_extra() put on the title bar and take it off the terminal."""
    t.remove(tg)
    scene.add(tg)
    scene.play(FadeOut(tg), *extra, run_time=0.3)
    scene.remove(tg)


def cmd_card(rows, color, head=None, pad: float = 0.25) -> VGroup:
    """A card of verbatim mono command rows (20 pt), optional GREY head line. .frame .body .head"""
    body = VGroup(*[mono_line(r, 20, INK) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    hd = label(head, 20, S.GREY) if head else None
    inner = VGroup(*([hd] if hd else []), body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = outline_box(inner.width + 2 * pad, inner.height + 0.4, color, solid=True, fill_opacity=0.08)
    fr.fill.set_fill(S.GREY_DARKER, 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.body, g.head = fr, body, hd
    return g


def key_card(kind: str, name: str, lines, color) -> VGroup:
    """A GREY illustration card: the key glyph and the account name, then short lines. .rows"""
    k = key_icon(kind, name=False, key_w=0.9)
    nm = mono(name, 22, color if kind != "deploy" else INK)
    top = VGroup(k, nm).arrange(RIGHT, buff=0.3)
    rows = [label(s, 22, INK) for s in lines]
    c = card([top, *rows], S.GREY, card_w=6.0, buff=0.14)
    c.rows = rows
    c.key = k
    return c


class Pipe(StackPipe):
    """StackPipe with the crates kept above the registry box (common.py request 1): the shared
    to_registry() adds the opaque box after the crates, so the registry looked empty while the tag
    chips faded in. Same geometry and timing as the shared method."""

    def to_registry(self, scene):
        reg = boxed("Artifact Registry", CLOUD, box_w=2.7, box_h=2.1, k=0.12).move_to(self.p(-1.6, 0.8))
        reg.text.align_to(reg.frame, UP).shift(DOWN * 0.12)
        self.reg = reg
        self.show(scene, reg, run_time=0.4)
        small = [crate(n, 2.3, 0.42, size=20) for n in self.NAMES]
        VGroup(*small).arrange(DOWN, buff=0.08).move_to(reg.frame).shift(DOWN * 0.2)
        self._ensure(scene)
        scene.play(LaggedStart(*[Transform(c, s_) for c, s_ in zip(self.crates, small)], lag_ratio=0.3),
                   run_time=1.0)
        self.remove(self.crates)         # draw the crates above the opaque registry box
        self.add(self.crates)
        self.heal(scene)
        tg = VGroup(*[route_chip(f"{n}-tags", size=20) for n in ("api", "frontend", "vector-db")])
        tg.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(reg, RIGHT, buff=0.3)
        self.tags_ = tg
        self.show(scene, *tg, run_time=0.5)


class ImagesStack(VoiceScene):
    def construct(self):
        # ========================================================== 0. the five APIs, plus Vertex AI
        trk = tracker_d(1)
        rc = readme_card((398, 402), "\n".join(APIS))
        vx = VGroup(label("Vertex AI API · the API Pods call it", 20, TURN), extra_tag()).arrange(RIGHT, buff=0.25)
        cl = Checklist("console › APIs & Services", APIS + [vx])
        rc.move_to([0, 0.2, 0]).align_to([-6.45, 0, 0], LEFT)
        cl.move_to([0, 0.2, 0]).align_to([6.45, 0, 0], RIGHT)
        assert cl.get_left()[0] > rc.get_right()[0] + 0.2, (cl.get_left(), rc.get_right())
        assert cl.get_top()[1] < PIC_TOP and rc.get_top()[1] < PIC_TOP
        r5 = cl.rows[5]
        cl.rows.remove(r5)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), run_time=0.5)
            self.play(FadeIn(rc, shift=RIGHT * 0.2), FadeIn(cl, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("enables the five APIs")
            for i in range(5):
                cl.tick(self, i, OWN, run_time=0.35)
            vo.wait_until("turn on the Vertex AI API too")
            self.play(FadeIn(r5, shift=LEFT * 0.4), run_time=0.6)
            cl.rows.add(r5)
            self.add(cl)
            cl.tick(self, 5, TURN, run_time=0.4)
            vo.wait_until("which the API Pods call")
            self.play(Indicate(vx[0], color=TURN, scale_factor=1.06), run_time=0.8)
        self.play(FadeOut(VGroup(rc, cl)), run_time=0.5)
        self.remove(rc, cl)

        # ========================================================== 1. the two service accounts
        rc1 = readme_card((236, 259), "\n".join([
            "Setup GCP Service Account for deployment",
            '… create a new service account called "deployment".',
            "Follow the same process Create another service account called gcp-service"]), size=20)
        rc1.move_to([0, 1.35, 0])
        kd = key_card("deploy", "deployment", ["the toolbox, Pulumi", "and here: the nodes' identity"], CLOUD)
        ks = key_card("service", "gcp-service", ["the API Pods", "through Workload Identity",
                                                 "no key file in the cluster"], OWN)
        kd.move_to([-3.2, 0, 0]).align_to([0, rc1.get_bottom()[1] - 0.45, 0], UP)
        ks.move_to([3.2, 0, 0]).align_to(kd, UP)
        tags1 = VGroup()
        for c in (kd, ks):
            tg = illustration_tag()
            tg.move_to(c.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
            tags1.add(tg)
        assert rc1.get_top()[1] < PIC_TOP and abs(rc1.get_left()[0]) < 6.5
        assert ks.get_bottom()[1] > -3.45 and ks.get_right()[0] < 6.5, (ks.get_bottom(), ks.get_right())
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(rc1, shift=DOWN * 0.15), run_time=0.6)
            self.play(LaggedStart(Indicate(rc1.body[1], color=CLOUD, scale_factor=1.04),
                                  Indicate(rc1.body[2], color=OWN, scale_factor=1.04), lag_ratio=0.5),
                      run_time=1.2)
            vo.wait_until("The deployment account")
            self.play(FadeIn(kd, shift=UP * 0.2), FadeIn(tags1[0]), run_time=0.6)
            self.play(Indicate(kd.rows[0], color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and here it is also")
            self.play(kd.rows[1].animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(kd.rows[1], color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("The gcp service account")
            self.play(FadeIn(ks, shift=UP * 0.2), FadeIn(tags1[1]), run_time=0.6)
            self.play(Indicate(ks.rows[0], color=OWN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("with no key file")
            self.play(ks.rows[2].animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(ks.rows[2], color=OWN, scale_factor=1.08), run_time=0.7)
        self.play(FadeOut(VGroup(rc1, kd, ks, tags1)), run_time=0.5)
        self.remove(rc1, kd, ks, tags1)

        # ========================================================== 2. two one-time steps
        iam = console_view(["IAM", "Service accounts", "gcp-service", "Permissions"],
                           [("grant deployment · Service Account Admin", CLOUD)])
        iam.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.7, 0], UP)
        unv = two_row_chip("unverified here", "follows from the documented roles", S.GREY)
        unv.next_to(iam, RIGHT, buff=0.3)
        assert unv.get_right()[0] < 6.5, unv.get_right()
        owner = cmd_card(IAM_CMD, S.GREY, head="or, as project owner:", pad=0.15)
        owner.move_to([0, 0, 0]).align_to([0, iam.get_bottom()[1] - 0.3, 0], UP)
        assert owner.get_right()[0] < 6.55 and owner.get_left()[0] > -6.55, (owner.get_left(), owner.get_right())
        ar = console_view(["Artifact Registry", "Create repository"],
                          [("cheese-app-repository · location: us", CLOUD)])
        ar.move_to([0, 0, 0]).align_to(iam, LEFT).align_to([0, iam.get_bottom()[1] - 0.3, 0], UP)
        mk = cmd_card(AR_CMD, OWN)
        mk.move_to([0, 0, 0]).align_to(iam, LEFT).align_to([0, ar.get_bottom()[1] - 0.3, 0], UP)
        et = extra_tag("our spelling")
        et.next_to(mk, UP, buff=0.1).align_to(mk, RIGHT)
        assert et.get_left()[0] > ar.get_right()[0] + 0.1, (et.get_left(), ar.get_right())
        assert mk.get_bottom()[1] > -3.45 and mk.get_right()[0] < 6.5, (mk.get_bottom(), mk.get_right())
        assert owner.get_bottom()[1] > -3.45
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(iam, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("The deployment account very likely needs")
            row = iam.rows[0]
            self.play(row.text.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(row.text, color=TURN, scale_factor=1.05), run_time=0.6)
            self.play(FadeIn(owner, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("we could not test this")
            self.play(FadeIn(unv, shift=LEFT * 0.15), run_time=0.5)
            flash_tag(self, unv, INK, 1.05)
            vo.wait_until("And create the registry repository")
            self.play(FadeOut(owner, shift=DOWN * 0.15), FadeIn(ar, shift=UP * 0.15), run_time=0.7)
            self.remove(owner)
            vo.wait_until("cheese app repository")
            nm = VGroup(*ar.rows[0].text.submobjects[:len("cheese-app-repository")])
            self.play(Indicate(nm, color=TURN, scale_factor=1.1), run_time=0.7)
            self.add(ar)
            vo.wait_until("which no code creates")
            self.play(FadeIn(mk, shift=UP * 0.15), FadeIn(et), run_time=0.6)
            self.play(Indicate(mk.body, color=OWN, scale_factor=1.03), run_time=0.7)
        self.play(FadeOut(VGroup(iam, unv, ar, mk, et)), run_time=0.5)
        self.remove(iam, unv, ar, mk, et)

        # ========================================================== 3. the key beside the repository (p05)
        t3 = term(P_LAPTOP, 7, T_LAPTOP, size=20)
        e3 = on_bar(t3, extra_row())
        f_repo = VGroup(folder_icon(0.7, LAPTOP), mono("cheese-app-v3/", 22, INK)).arrange(DOWN, buff=0.15)
        f_sec = VGroup(folder_icon(0.7, LAPTOP), mono("secrets/", 22, INK)).arrange(DOWN, buff=0.15)
        VGroup(f_repo, f_sec).arrange(RIGHT, buff=2.2).move_to([-2.2, 1.75, 0])
        key = key_icon("deploy", name="deployment.json", key_w=0.9)
        key.move_to([2.6, 1.95, 0])
        ph = grey_chip("placeholder key for no account")
        assert t3.box.get_top()[1] < 1.0, t3.box.get_top()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(t3, shift=UP * 0.2), FadeIn(e3), FadeIn(f_repo), FadeIn(f_sec), run_time=0.6)
            self.remove(e3)
            t3.add(e3)                       # on the bar: part of the terminal from now on
            self.add(t3)
            type_capture(self, t3, P05, type_time=0.6)
            rows3 = out(self, t3, [P05.line(2), P05.line(6), P05.line(7), P05.line(11)], run_time=0.4)
            vo.wait_until("in the secrets folder")
            self.play(FadeIn(key, shift=DOWN * 0.2), run_time=0.4)
            self.play(key.animate.next_to(f_sec, RIGHT, buff=0.35), run_time=0.7)
            ph.next_to(key, DOWN, buff=0.25).align_to(key, LEFT)
            keep_inside(ph)
            dj = substring(rows3[3], "deployment.json")
            self.play(FadeIn(ph, shift=UP * 0.1), dj.animate.set_color(TURN), run_time=0.5)
            self.add(t3)
            vo.wait_until("beside the repository")
            self.play(Indicate(substring(rows3[1], "cheese-app-v3"), color=TURN, scale_factor=1.1),
                      Indicate(substring(rows3[2], "secrets"), color=TURN, scale_factor=1.1),
                      Indicate(f_repo, color=TURN, scale_factor=1.05),
                      Indicate(f_sec, color=TURN, scale_factor=1.05), run_time=0.8)
            self.add(t3)
        self.play(FadeOut(VGroup(t3, f_repo, f_sec, key, ph)), run_time=0.5)
        self.remove(t3, f_repo, f_sec, key, ph)

        # ========================================================== 4. the toolbox steps again, fast
        t = term(P_SRC, 12, T_LAPTOP, size=20)
        att = grey_chip("docker-shell.sh:23–25 · already running → it attaches")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(t, shift=UP * 0.2), track(trk, 2), run_time=0.5)
            type_cmd(self, t, README_CD, type_time=0.35)
            cd_prompt(self, t, P_DEPLOY, color=TURN, run_time=0.4)
            type_capture(self, t, B03, type_time=0.35)
            out(self, t, [(B03.line(31), CONTAINER)], run_time=0.3)
            rp = out(self, t, [B03.crop(77, "#")], run_time=0.3)[0]
            self.play(substring(rp, TOOLBOX_ID).animate.set_color(S.GREY), retitle(t, T_TOOLBOX), run_time=0.4)
            self.add(t)
            rp.bare = True
            t.set_prompt(P_TOOLBOX)
            vo.wait_until("if the toolbox is still running")
            under_term(t, att)
            self.play(FadeIn(att, shift=DOWN * 0.1), run_time=0.4)
            self.play(track(trk, 3), run_time=0.3)
            type_capture(self, t, B10, type_time=0.3)
            out(self, t, [B10.line(2)], run_time=0.25)
            type_capture(self, t, B11, type_time=0.3)
            out(self, t, [B11.line(4)], wrap=True, run_time=0.3)
            type_capture(self, t, B12, type_time=0.3)
            out(self, t, [B12.line(2)], run_time=0.25)
            self.play(track(trk, 4), run_time=0.3)
            type_capture(self, t, B13, type_time=0.3)
            out(self, t, [(B13.line(3), ERR)], run_time=0.3)

        # ========================================================== 5. the images stack: init, config
        rc5 = readme_card(416, "This step is only required\nif you have NOT already done this")
        rc5.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.2, 0], UP)
        why = two_row_chip("no bucket login", "→ Pulumi tries its cloud service", S.GREY)
        why.next_to(rc5, RIGHT, buff=0.3)
        assert why.get_right()[0] < 6.5, why.get_right()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(att), track(trk, 5), run_time=0.4)
            self.remove(att)
            resize(self, t, 8, keep=0, run_time=0.6)
            assert rc5.get_bottom()[1] > t.box.get_top()[1] + 0.1, (rc5.get_bottom(), t.box.get_top())
            self.play(FadeIn(rc5, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("only if you have not built it before")
            self.play(Indicate(rc5.body, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("change into deploy images")
            type_cmd(self, t, CD_IMAGES, type_time=0.4)
            cd_prompt(self, t, toolbox_prompt("/app/deploy_images"), color=TURN, run_time=0.4)
            vo.wait_until("pulumi stack init dev")
            type_capture(self, t, B20, type_time=0.4)
            e20 = out(self, t, [(B20.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("and set G C P project to yours")
            r21 = type_capture(self, t, B21, type_time=0.6)[0]
            ac_row = [r for r in rows_of(r21) if "ac215-project" in r.text][0]
            ac_ring = ring(substring(ac_row, "ac215-project"), S.GREY, buff=0.05, stroke=2.5)
            d21 = default_row()
            pin(self, r21, beside(d21, r21), anim=AnimationGroup(FadeIn(d21), Create(ac_ring)))
            attach(self, ac_row, ac_ring)
            e21 = out(self, t, [(B21.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("Ours says Pulumi access token must be set")
            toks = [substring(r, "PULUMI_ACCESS_TOKEN") for r in (e20[0], e21[0])]
            self.play(*[Indicate(x, color=ERR, scale_factor=1.1) for x in toks], run_time=0.7)
            self.add(t)
            vo.wait_until("our bucket login failed")
            self.play(FadeIn(why, shift=LEFT * 0.15), run_time=0.5)
            flash_tag(self, why, INK, 1.05)

        # ========================================================== 6. the local backend (not for you)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rc5, why)), track(trk, 5, "not for you"), run_time=0.4)
            self.remove(rc5, why)
            resize(self, t, 14, run_time=0.5)
            r00 = type_capture(self, t, C00, type_time=0.4)[0]
            e6 = mark_extra(self, t, r00, extra_row("not for you"))
            g00 = out(self, t, [C00.line(2)], run_time=0.3)[0]
            self.play(substring(g00, TOOLBOX_ID).animate.set_color(S.GREY), run_time=0.3)
            self.add(t)
            vo.wait_until("don't run it")
            if e6 is not None:
                flash_tag(self, e6, INK, 1.08)
            vo.wait_until("Now the stack is created")
            type_capture(self, t, C01, type_time=0.4)
            g01 = out(self, t, [(C01.line(2), OWN)], run_time=0.3)[0]
            self.play(Indicate(g01, color=OWN, scale_factor=1.08), run_time=0.6)
            self.add(t)
            r02 = type_capture(self, t, C02, type_time=0.5)[0]
            ac02 = [r for r in rows_of(r02) if "ac215-project" in r.text][0]
            ring02 = ring(substring(ac02, "ac215-project"), S.GREY, buff=0.05, stroke=2.5)
            d02 = default_row()
            pin(self, r02, beside(d02, r02), anim=AnimationGroup(FadeIn(d02), Create(ring02)))
            attach(self, ac02, ring02)
            bare_prompt(self, t)

        # ========================================================== 7. pulumi preview: + 4 to create
        with self.voiceover(SAY[7]) as vo:
            if e6 is not None:
                drop_bar_tag(self, t, e6, track(trk, 6))
            else:
                self.play(track(trk, 6), run_time=0.3)
            resize(self, t, 14, keep=0, run_time=0.4)      # a clean screen: b22 ran before login --local
            r22 = type_capture(self, t, B22, type_time=0.35)[0]
            pin(self, r22, beside(row_tag("README backend · before login --local"), r22), run_time=0.3)
            out(self, t, [(B22.line(2), ERR)], wrap=True, run_time=0.3)
            self.play(track(trk, 6, True), run_time=0.3)
            r03 = type_capture(self, t, C03, type_time=0.35)[0]
            e7 = mark_extra(self, t, r03, extra_row())
            g29 = out(self, t, [(C03.line(29), S.GREY)], run_time=0.25)[0]
            vo.wait_until("three image builds")
            g31 = out(self, t, [(C03.line(n), OWN) for n in (31, 32, 33)], run_time=0.5)
            vo.wait_until("skipped in a preview")
            g40 = out(self, t, [(C03.line(40), SHARED)], run_time=0.3)[0]
            self.play(Indicate(substring(g40, "Skipping preview build"), color=SHARED, scale_factor=1.08),
                      run_time=0.6)
            self.add(t)
            vo.wait_until("and three tags stamped with the time")
            s51 = C03.line(51)
            g50 = out(self, t, ["…", C03.line(50), s51[:72], s51[72:], C03.line(52)], run_time=0.5)
            r50, r51a, r51b = g50[1], g50[2], g50[3]
            st = substring(r51b, STAMP)
            self.play(st.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(st, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            ac_ring7 = ring(substring(r51a, "ac215-project"), S.GREY, buff=0.05, stroke=2.5)
            d50 = default_row()
            pin(self, r50, beside(d50, r50), anim=AnimationGroup(FadeIn(d50), Create(ac_ring7)))
            attach(self, r51a, ac_ring7)
            vo.wait_until("Plus 4 to create")
            g63 = out(self, t, ["…", (C03.line(63), TURN)], run_time=0.4)[-1]
            self.play(Indicate(g63, color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(t)
            vo.wait_until("three images and the stack itself")
            self.play(*[Indicate(r, color=OWN, scale_factor=1.04) for r in g31], run_time=0.7)
            self.add(t)
            plus1 = row_tag("+1 · the stack itself")
            pin(self, g29, beside(plus1, g29))
            flash_tag(self, plus1, INK, 1.08)

        # ========================================================== 8. tags -> registry -> StackReference
        sp = Pipe()
        with self.voiceover(SAY[8]) as vo:
            if e7 is not None:
                drop_bar_tag(self, t, e7)
            resize(self, t, 3, keep=[r50, r51a, r51b], extra=[track(trk, 6)], run_time=0.6)
            assert t.box.get_top()[1] < -1.25, t.box.get_top()
            sp.images(self)
            sp.to_registry(self)
            vo.wait_until("deploy k8s looks them up")
            sp.pipe(self)
            vo.wait_until("to know which images to run")
            self.play(Indicate(sp.k8s, color=OWN, scale_factor=1.06),
                      Indicate(r51b, color=TURN, scale_factor=1.04), run_time=0.8)
            self.add(t)
            sp.heal(self)

        # ========================================================== 9. pulumi up: build and push
        apple = grey_chip("Apple Silicon: a long build is normal")
        l20c = dashed_chip("L20 · the real build, up to the push · the API image ≈ 5 GB")
        cond = scene_chip("the condition · next")
        yt = your_turn()
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(sp), track(trk, 7), run_time=0.5)
            self.remove(sp)
            resize(self, t, 5, keep=0, run_time=0.5)
            col = VGroup(l20c, apple, cond).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            col.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, t.box.get_top()[1] + 0.35, 0], DOWN)
            yt.next_to(cond, RIGHT, buff=0.4)
            assert col.get_top()[1] < PIC_TOP and l20c.get_right()[0] < 6.5
            vo.wait_until("pulumi up, stack dev, dash y")
            type_capture(self, t, B23, type_time=0.5)
            out(self, t, [(B23.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("it builds and pushes three images")
            self.play(FadeIn(apple, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Skip it if you did it in lecture 20")
            self.play(FadeIn(l20c, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("with one condition we meet next")
            self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("otherwise, pause and run it")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        self.play(FadeOut(VGroup(trk, t, apple, l20c, cond, yt)), run_time=0.6)
        self.remove(trk, t, apple, l20c, cond, yt)
        self.wait(0.4)
