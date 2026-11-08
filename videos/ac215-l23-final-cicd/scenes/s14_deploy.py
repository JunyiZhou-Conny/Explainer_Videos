"""S14 · Follow one tag to the server — TRACKER C 6 → C 7 (workflow › ci_cd_aws.yml · not in the
README). V6 TimestampTrail (deploy), BeadChain, V7's server (the trail's), V8 ReleaseLoop and
ReleaseToggle. Lecture: 23 · slides 18–19 (beat 5), 11–12 (beats 9–10).

Beats (script.md "## S14", one voiceover block each):
0. TRACKER C 6. CODE(.github/workflows/ci_cd_aws.yml: 113–123): line 114 (the socket) PINK, 115
   (`/deployment`) GREEN, 116 (`/root/.ssh`) PINK, 117–120 (`-e …`) GREY, 121 (`DOCKER_TAG`) YELLOW.
1. TRACKER C 6. The panel transforms into CODE(ci_cd_aws.yml: 123–131) (dedented, lines 129–130
   shortened with `…`, GREY chip "… = shortened here"); each `&&` link folds into a chain bead under
   the panel: `cd /deployment` → permissions → `ls` → ECR login → `deploy-setup-containers.yml …
   docker_tag=$DOCKER_TAG` (YELLOW) → `deploy-setup-webserver.yml`; the beads light in turn, the
   `&&` links flash on "Each link".
2. TRACKER C 6. Laptop terminal (11 rows), heading row "ci_cd_aws.yml · lines 110–131 · run by
   hand", `extra` on the title bar, "the workflow's own commands, run by hand" above it →
   TERM(laptop/53: 22–27, 29–30): the tag GREEN, `drwx------` / `-rw-------` flash, 29 (wrapped)
   and 30 RED. The terminal shrinks to a 3-row strip (22, the last row of 29, 30); the chain returns
   above it: three beads GREEN, the ECR bead RED, the two playbook beads GREY dashed + chip "never ran".
3. V6 TimestampTrail (deploy): the GREEN tag card is stamped above 'GitHub runner · date', rides
   DOCKER_TAG → toolbox → 'ansible-playbook · docker_tag=…' (that line YELLOW); the S09 fork small and
   GREY dashed, GREY chip "same value · the extra variable wins over set_fact"; three PINK pulls from
   ECR to the server's three TEAL containers.
4. Each container is recreated: old blinks out, GREY dashed gap + chip "short gap", new in (':new').
5. LECTURE 23 · 18–19. The server moves left; right, a GREY dashed inset "L22 · the slides' K8s
   deploy": a rolling update (a new pod comes up before each old one goes). Under both: "this repo:
   one machine · swap, not roll"; the server swaps one container again.
6. TRACKER C 7, ▶ your turn. S05's GREEN "your edits" checklist returns and becomes the YELLOW
   "commit these four" checklist (its Dockerfile row transforms into "Dockerfile · the Helm fix");
   one tick per sentence; GREY chip "CI deploys to the committed address" by row 1; then a RED box
   "git add . = every modified file · docker-shell.sh:17 (account ID) · inventory.yml:24 (NEXTAUTH
   secret)".
7. TRACKER C 7. Laptop terminal at student@laptop:~/cheese-app-aws$ with the three lines written out
   (`written out, not run` on the bar; GREY chips "the slide's three commands, with a dot and this
   repo's keyword" and "a public repo publishes line 24's secret · keep it private"); each line
   lights YELLOW on its phrase; ▶ your turn beside `git push`. The terminal shrinks to a 3-row
   strip; a schematic Actions run page (illustration): job Explore-GitHub-Actions, the file's eleven
   step names, ticking GREEN top to bottom (finishes in a short hold after the block).
8. TRACKER C 7. V8 ReleaseLoop; Monitor lights; two chips, one per clause: "green run = every step
   that ran exited 0" and "reload the site · sudo docker container ls → the IMAGE column shows the
   new tag".
9. LECTURE 23 · 11–12. V8's toggle: belt, the RELEASE button (hand above) and the 'auto' ring side
   by side, unlabelled; a PINK `/run-deploy-app` ribbon hovers between them. PONDER (10 s).
10. LECTURE (held). The card leaves; the ribbon drops into the hand; "continuous delivery" under the
   button; the hand presses; a GREY dashed Test box on the belt ("nothing is tested first"); then the
   Test box turns solid GREEN with chip "L21", the ribbon and the button fade, the ring takes the
   button's place: "continuous deployment" and "every merge to main · Milestone 5". Fade; empty frame.

Deviations from SHOW: the tracker cannot show "C 6 · extra" in beat 2 (tracker_c always reads
"· not in the README"), so the `extra` tag sits on the terminal's title bar instead. Beat 1's
second panel is dedented by 12 and shortens lines 129–130 with `…` (every kept piece is asserted to
be in the source line; a GREY chip says so): line 130 is 216 characters. Beat 5 uses the trail's own
server (three containers) as "V7's server". Beat 8 shows ReleaseLoop with Release (no this_repo
chips) and places its two chips under the loop, right-aligned under Monitor. Beat 10's Test box is
a stand-alone copy of V8's Test box placed on the toggle's belt (the loop is not on screen).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from explainer.devops import glyph_range

SAY = NARRATION["S14"]

WF = ".github/workflows/ci_cd_aws.yml"
C53 = capture("53")
assert not C53.typed
assert C53.line(22) == f"Deploying with tag: {TAG_CI}", C53.line(22)
assert C53.line(24).startswith("drwx------") and C53.line(26).startswith("-rw-------")
assert "GetAuthorizationToken" in C53.line(29) and C53.line(30).startswith("Error: Cannot perform")
assert excerpt(WF, 113, 113).strip().startswith("docker run --rm --name cheese-app-deployment")
assert excerpt(WF, 114, 114).strip() == "-v /var/run/docker.sock:/var/run/docker.sock \\"
assert excerpt(WF, 121, 121).strip() == "-e DOCKER_TAG \\"
assert excerpt(WF, 123, 123).strip() == '/bin/bash -c "cd /deployment && \\'
assert excerpt(WF, 131, 131).strip() == 'ansible-playbook deploy-setup-webserver.yml -i inventory.yml"'
assert excerpt(WF, 109, 109).strip() == "run: |" and excerpt(WF, 99, 99).strip() == "- name: Run Deployment Container"
assert excerpt("src/deployment/inventory.yml", 30, 30).strip() == "<EXTERNAL_IP>:"
assert "chromadb/chroma:latest" in excerpt("src/deployment/deploy-setup-containers.yml", 151, 151)
assert excerpt("src/deployment/docker-shell.sh", 17, 17).strip() == f'export AWS_ACCOUNT_ID="{ACCOUNT}"'
assert "nextauth_secret" in excerpt("src/deployment/inventory.yml", 24, 24)

STEP_NAMES = [ln.strip()[len("- name: "):].strip() for ln in source_text(WF).split("\n")
              if ln.strip().startswith("- name: ")]
assert len(STEP_NAMES) == 11 and STEP_NAMES[0] == "Check out repository code", STEP_NAMES
assert STEP_NAMES[-1] == "Run Deployment Container"
assert "Explore-GitHub-Actions:" in source_text(WF)

# the && chain of ci_cd_aws.yml:123-131, one bead per link (BeadChain with this scene's labels)
BEADS = ("cd /deployment", "permissions", "ls", "ECR login",
         "deploy-setup-containers.yml … docker_tag=$DOCKER_TAG", "deploy-setup-webserver.yml")
BEAD_LINES = ((0,), (1, 2, 3, 4), (5,), (6,), (7,), (8,))      # panel lines (file line - 123) per bead

S05_ROWS = ["docker-shell.sh:10 · ../../../secrets", None, "Dockerfile · drop Helm (33–34, 36)",
            "docker-shell.sh:26 · three ../", "docker-shell.sh:17 · your account ID"]
COMMIT_ROWS = ["inventory.yml:30 · your server's IP",
               "inventory.yml:4 on · line 7 commented again (undo step 9)",
               "Dockerfile · the Helm fix",
               "deploy-setup-containers.yml:151 · Chroma pinned"]
GIT_LINES = ("git add .", 'git commit -m "your message /run-deploy-app"', "git push")
Y5 = 0.1             # beat 5: the server and the K8s inset sit on this line
PONDER_Q = ("By the lecture's definitions,\nis typing /run-deploy-app\ncontinuous delivery or continuous "
            "deployment?\nWhat would make it the other?")


# ------------------------------------------------------------------ helpers of this scene
def gone(scene, *mobs, run_time: float = 0.5):
    """FadeOut mobjects that are not members of a piece, and take them off the scene."""
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def shortened_panel(path: str, a: int, b: int, dedent: int, edits: dict, font_size: float = 20):
    """CODE(path: a–b) with the common indent removed and some lines shortened with '…'. Every piece
    kept around a '…' must occur in the source line, in order (nothing is invented)."""
    rows = excerpt(path, a, b).split("\n")
    for n, new in edits.items():
        orig = rows[n - a]
        pos = 0
        for piece in [p.strip() for p in new.split("…") if p.strip()]:
            i = orig.find(piece, pos)
            assert i >= 0, (n, piece, orig)
            pos = i + len(piece)
        indent = orig[:len(orig) - len(orig.lstrip())]
        rows[n - a] = indent + new
    for r in rows:
        assert r[:dedent].strip() == "", r
    src = "\n".join(r[dedent:] for r in rows)
    guard(src)
    return code_panel(src, path, a, "yaml", font_size=font_size)


def at_top(m, top: float = 2.75):
    return m.move_to([0, 0, 0]).shift(UP * (top - m.get_top()[1]))


def run_page():
    """A schematic GitHub Actions run page (illustration): job Explore-GitHub-Actions and the step
    names of ci_cd_aws.yml in two columns, each with an idle state mark. .frame .marks .rows .tag"""
    head = VGroup(label("GitHub", 20, CLOUD), label("Actions › your run · job", 20, S.GREY),
                  mono("Explore-GitHub-Actions", 20, INK)).arrange(RIGHT, buff=0.2)
    rows = VGroup()
    for nm in STEP_NAMES:
        m = state_mark("idle", 0.3)
        t = label(nm, 20, INK)
        r = VGroup(m, t).arrange(RIGHT, buff=0.18)
        r.mark, r.text = m, t
        rows.add(r)
    col1 = VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    col2 = VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    cols = VGroup(col1, col2).arrange(RIGHT, buff=0.7, aligned_edge=UP)
    inner = VGroup(head, cols).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    fr = RoundedRectangle(width=max(inner.width + 0.8, 10.0), height=inner.height + 0.7, corner_radius=0.16,
                          stroke_color=CLOUD, stroke_width=2.5).set_fill(PANEL, 1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4)
    sep = Line([fr.get_left()[0], head.get_bottom()[1] - 0.2, 0], [fr.get_right()[0], head.get_bottom()[1] - 0.2, 0],
               color=S.GREY_DARK, stroke_width=2)
    tg = illustration_tag()
    tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(fr, sep, inner, tg)
    g.frame, g.rows, g.tag = fr, rows, tg
    return g


def pod(state: str):
    c = crate("pod", box_w=1.15, box_h=0.75, sub=":" + state)
    if state == "new":
        c.sub.set_color(OWN)
    return c


def light(scene, line):
    g = _glyphs(line)
    scene.play(g.animate.set_color(TURN), run_time=0.3)
    scene.play(Indicate(g, color=TURN, scale_factor=1.04), run_time=0.5)


class FollowTheTag(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 11, len(SAY)
        tr = tracker_c(6)

        # ========================================================== 0. the deploy step's docker run
        p0 = at_top(code(WF, 113, 123))
        bars = {k: line_bar(p0.code, k, col, 0.22) for k, col in
                ((1, ROUTE), (2, OWN), (3, ROUTE), (8, TURN))}
        env_bars = VGroup(*[line_bar(p0.code, k, S.GREY, 0.22) for k in (4, 5, 6, 7)])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(p0, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(code_span(p0.code, 0, "docker run"), color=IMAGE, scale_factor=1.12),
                      Indicate(code_span(p0.code, 9, "cheese-app-deployment"), color=IMAGE, scale_factor=1.08),
                      run_time=1.0)
            vo.wait_until("with the socket")
            self.play(FadeIn(bars[1]), run_time=0.4)
            self.play(Indicate(code_span(p0.code, 1, "/var/run/docker.sock"), color=ROUTE, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("two folders")
            self.play(FadeIn(bars[2]), run_time=0.35)
            self.play(FadeIn(bars[3]), run_time=0.35)
            vo.wait_until("and five environment")
            self.play(LaggedStart(*[FadeIn(b) for b in env_bars], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("docker tag among them")
            self.play(FadeIn(bars[8]), run_time=0.4)
            self.play(Indicate(code_span(p0.code, 8, "DOCKER_TAG"), color=TURN, scale_factor=1.2), run_time=0.7)

        # ========================================================== 1. one long && command → beads
        p1 = at_top(shortened_panel(WF, 123, 131, 12, {
            129: 'aws ecr get-login-password --region us-east-1 | docker login … && \\',
            130: '… deploy-setup-containers.yml … docker_tag=\\$DOCKER_TAG\\" -vv && \\'}))
        short = grey_chip("… = shortened here", size=20)
        short.move_to([p1.code.get_right()[0] - short.width / 2, p1.header.get_y(), 0])
        bc = BeadChain(BEADS, max_w=12.4)
        bc.move_to([0, 0, 0]).shift(UP * ((p1.get_bottom()[1] - 0.15) - bc.get_top()[1]))
        bc.beads[4].text.set_color(TURN)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(*bars.values(), env_bars)), ReplacementTransform(p0, p1), run_time=0.9)
            self.remove(*bars.values(), env_bars)
            self.play(FadeIn(short, shift=LEFT * 0.1), run_time=0.4)
            self.play(LaggedStart(*[TransformFromCopy(VGroup(*[p1.code.code_lines[k] for k in ks]), bc.beads[i])
                                    for i, ks in enumerate(BEAD_LINES)], lag_ratio=0.15),
                      FadeIn(bc.links), run_time=1.4)
            bc._reseat(self)
            vo.wait_until("fix permissions")
            self.play(bc.light(1, TURN), run_time=0.6)
            vo.wait_until("log in to E C R")
            self.play(bc.light(3, TURN), run_time=0.6)
            vo.wait_until("run deploy setup containers")
            self.play(bc.light(4, TURN), run_time=0.7)
            self.play(Indicate(code_span(p1.code, 7, "docker_tag=\\$DOCKER_TAG"), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("then deploy setup webserver")
            self.play(bc.light(5, TURN), run_time=0.6)
            vo.wait_until("Each link runs only if")
            self.play(LaggedStart(*[Indicate(ln, color=ROUTE, scale_factor=1.3) for ln in bc.links], lag_ratio=0.3),
                      run_time=1.6)

        # ========================================================== 2. run by hand (extra): stops at ECR login
        t = laptop_term(11)
        xtag = on_bar(t, extra_row())
        bh = under_term(t, byhand_tag())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(p1), FadeOut(short), FadeOut(bc), run_time=0.5)
            self.remove(p1, short, *p1.get_family(), *short.get_family())
            self.remove(bc)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            put_heading(self, t, "ci_cd_aws.yml · lines 110–131 · run by hand")
            self.play(FadeIn(xtag), FadeIn(bh, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("it prints the tag")
            r22 = out(self, t, [(C53.line(22), OWN)], run_time=0.4)[0]
            self.play(Indicate(substring(r22, TAG_CI), color=OWN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and lists the key")
            ls_rows = out(self, t, C53.at((23, 27)), run_time=0.7)
            self.play(Indicate(substring(ls_rows[1], "drwx------"), color=OWN, scale_factor=1.12),
                      Indicate(substring(ls_rows[3], "-rw-------"), color=OWN, scale_factor=1.12),
                      Indicate(substring(ls_rows[3], PEM_CODE), color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("then stops at the E C R login")
            r29 = out(self, t, [(s, ERR) for s in C53.at(29)], wrap=True, run_time=0.6)
            r30 = out(self, t, [(C53.line(30), ERR)], run_time=0.3)[0]
            vo.wait_until("with our placeholder key")
            self.play(Indicate(substring(r29[0], "UnrecognizedClientException"), color=ERR, scale_factor=1.08),
                      run_time=0.6)
            new_bar_y = STRIP_TOP - t.bar_h / 2
            resize(self, t, 3, keep=[r22, r29[-1], r30],
                   extra=[xtag.animate.set_y(new_bar_y), bh.animate.set_y(STRIP_TOP + 0.12 + bh.height / 2)],
                   run_time=0.7)
            bc.move_to([0, 0.75, 0])
            self.play(FadeIn(bc), run_time=0.4)
            vo.wait_until("Neither playbook runs")
            for i in range(3):
                bc.state(self, i, "ok", run_time=0.15)
            bc.state(self, 3, "fail", run_time=0.3)
            bc.state(self, 4, "never", run_time=0.25)
            bc.state(self, 5, "never", run_time=0.25)
            never = dashed_chip("never ran", PAST, 20)
            never.next_to(bc.beads[5], RIGHT, buff=0.35)
            self.play(FadeIn(never, shift=LEFT * 0.1), run_time=0.4)
        self.wait(1.2)

        # ========================================================== 3. V6: one tag from date to the server
        tt = TimestampTrail("deploy", TAG_CI)
        anc = tt.stations["ansible"]
        fork = dashed_chip("S09 · set_fact: env or .docker-tag", PAST, 20)
        fork.move_to([6.4 - fork.width / 2, 0.45, 0])
        wins = grey_chip("same value · the extra variable wins over set_fact", 20)
        wins.move_to([fork.get_left()[0] - 0.3 - wins.width / 2, 0.45, 0])
        beats = arrow(anc.get_bottom(), fork.get_top(), TOOL, 3, buff=0.06)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(t, xtag, bh, bc, never)), run_time=0.5)
            self.remove(t, xtag, bh, bc, never, *t.get_family())
            self.play(FadeIn(tt, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("The date stamps it")
            tt.stamp(self, run_time=0.8)
            vo.wait_until("It reaches Ansible")
            tt.ride(self, per=0.55)
            vo.wait_until("as an extra variable")
            self.play(anc.text[1].animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(anc.text[1], color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("which beats anything")
            self.play(GrowArrow(beats), FadeIn(fork, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(wins, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("so the server pulls")
            tt.pull(self, run_time=1.0)
            self.play(LaggedStart(*[Indicate(c.sub, color=OWN) for c in tt.containers], lag_ratio=0.2),
                      run_time=0.6)

        # ========================================================== 4. each container recreated
        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("Then each container")
            tt.recreate(self, 0, run_time=1.4)
            vo.wait_until("the new one starts")
            tt.recreate(self, 1, gap_chip=False, run_time=1.0)
            tt.recreate(self, 2, gap_chip=False, run_time=1.0)

        # ========================================================== 5. slides 18-19: swap, not roll
        lr = lref("18–19")
        srv = tt.server
        inset_fr = outline_box(5.8, srv.frame.height, PAST).move_to([3.3, Y5, 0])
        inset_t = label("L22 · the slides' K8s deploy", 20, S.GREY)
        inset_t.move_to(inset_fr.get_top() + DOWN * 0.28)
        slots = [np.array([3.3 + (i - 1.5) * 1.3, Y5 - 0.2, 0]) for i in range(4)]
        olds = [pod("old").move_to(slots[i]) for i in range(3)]
        under_both = label("this repo: one machine · swap, not roll", 22, INK).move_to([0, Y5 - 1.85, 0])
        with self.voiceover(SAY[5]) as vo:
            rest = [m for m in tt.submobjects if m is not srv]
            self.play(FadeOut(VGroup(beats, fork, wins)), run_time=0.3)
            self.remove(beats, fork, wins)
            tt.drop(self, *rest, run_time=0.5)
            self.play(srv.animate.move_to([-3.25, Y5, 0]), FadeIn(lr), run_time=0.7)
            vo.wait_until("to a Kubernetes cluster")
            self.play(Create(inset_fr), FadeIn(inset_t), LaggedStart(*[FadeIn(p, scale=0.9) for p in olds],
                                                                     lag_ratio=0.2), run_time=0.9)
            vo.wait_until("a rolling update")
            live = {0: olds[0], 1: olds[1], 2: olds[2]}
            free = 3
            for i in range(3):
                nw = pod("new").move_to(slots[free])
                self.play(FadeIn(nw, scale=1.1), run_time=0.45)
                self.play(FadeOut(live[i]), run_time=0.4)
                self.remove(live[i])
                live[i] = None
                free, slot_new = i, nw
                live[("n", i)] = slot_new
            vo.wait_until("One machine can only swap")
            self.play(FadeIn(under_both, shift=UP * 0.1), run_time=0.5)
            tt.recreate(self, 1, gap_chip=False, run_time=1.0)
            vo.wait_until("it doesn't roll")
            self.play(Indicate(under_both, color=TURN, scale_factor=1.05), run_time=0.7)
        new_pods = [v for k, v in live.items() if isinstance(k, tuple)]
        lecture5 = VGroup(inset_fr, inset_t, *new_pods, under_both)

        # ========================================================== 6. what to commit
        old_ck = Checklist("your edits", [r if r else VGroup(label("Linux: bash, not sh", 20, INK), erratum_tag())
                                          .arrange(RIGHT, buff=0.18) for r in S05_ROWS],
                           color=OWN, tag_text=None)
        for r in old_ck.rows:
            ck = check_mark(0.3, OWN, stroke=4).move_to(r.box).shift(UP * 0.04 + RIGHT * 0.03)
            r.add(ck)
        ck = Checklist("commit these four", COMMIT_ROWS, color=TURN, tag_text=None)
        ck.move_to([0, 0, 0]).shift(np.array([-6.3 - ck.get_left()[0], 2.6 - ck.get_top()[1], 0]))
        old_ck.shift(np.array([-6.3 - old_ck.get_left()[0], 2.6 - old_ck.get_top()[1], 0]))
        yt = your_turn()
        yt.move_to(ck.frame.get_corner(UR) + np.array([-yt.width / 2 - 0.2, 0, 0]))
        ci_chip = label_box(["CI deploys to the", "committed address"], S.GREY, size=20)
        ci_chip.text.set_color(INK)
        ci_chip.next_to(ck.frame, RIGHT, buff=0.3).align_to(ck.rows[0], UP)
        warn = label_box(["git add .  =  every modified file",
                          "docker-shell.sh:17 (account ID) · inventory.yml:24 (NEXTAUTH secret)"], ERR, size=20)
        warn.text[0].set_color(ERR)
        warn.text[1].set_color(INK)
        warn.next_to(ck.frame, DOWN, buff=0.45).align_to(ck.frame, LEFT)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(lr), FadeOut(lecture5), FadeOut(tt), run_time=0.5)
            self.remove(lr, lecture5, tt, *lecture5.get_family(), *tt.get_family())
            self.play(track(tr, 7), FadeIn(old_ck, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("Commit four things")
            self.play(Circumscribe(old_ck.frame, color=OWN, buff=0.05), run_time=0.6)
            others = [old_ck.rows[i] for i in (0, 1, 3, 4)]
            self.play(ReplacementTransform(old_ck.frame, ck.frame), ReplacementTransform(old_ck.head, ck.head),
                      ReplacementTransform(old_ck.rows[2], ck.rows[2]), *[FadeOut(r) for r in others],
                      *[FadeIn(ck.rows[i]) for i in (0, 1, 3)], run_time=1.0)
            self.remove(old_ck, *old_ck.get_family(), ck.frame, ck.head, *ck.rows)
            self.add(ck)
            self.play(FadeIn(yt, scale=1.1), run_time=0.4)
            vo.wait_until("Your server address")
            ck.tick(self, 0, TURN)
            vo.wait_until("C I deploys whatever")
            self.play(FadeIn(ci_chip, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Step 9 undone")
            ck.tick(self, 1, TURN)
            vo.wait_until("The Helm fix")
            ck.tick(self, 2, TURN)
            vo.wait_until("The Chroma pin")
            ck.tick(self, 3, TURN)
            vo.wait_until("Git add dot also commits")
            self.play(FadeIn(warn, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("so keep the repository private")
            self.play(Circumscribe(warn.frame, color=ERR, buff=0.05), Indicate(warn.text[1], color=ERR, scale_factor=1.04),
                      run_time=0.9)

        # ========================================================== 7. the slide's three commands
        t2 = term(P_REPO, rows=6)
        sh = on_bar(t2, row_tag("written out, not run"))
        c_slide = under_term(t2, grey_chip("the slide's three commands, with a dot and this repo's keyword", 20))
        c_pub = grey_chip("a public repo publishes line 24's secret · keep it private", 20)
        c_pub.next_to(c_slide, UP, buff=0.15).align_to(c_slide, RIGHT)
        page = run_page()
        page.move_to([0, 0, 0]).shift(np.array([0, (2.75 + (STRIP_TOP + 0.2)) / 2, 0]))
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(ck, yt, ci_chip, warn)), run_time=0.5)
            self.remove(ck, yt, ci_chip, warn, *ck.get_family())
            self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(sh), run_time=0.5)
            lines = [type_cmd(self, t2, g, type_time=0.35) for g in GIT_LINES]
            self.play(FadeIn(c_slide, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("git add dot")
            light(self, lines[0])
            self.play(FadeIn(c_pub, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("git commit with")
            light(self, lines[1])
            vo.wait_until("and git push")
            light(self, lines[2])
            vo.wait_until("Pause, and push")
            pin(self, lines[2], beside(turn_row(), lines[2]))
            self.play(FadeOut(VGroup(c_slide, c_pub)), run_time=0.3)
            self.remove(c_slide, c_pub)
            resize(self, t2, 3, extra=[sh.animate.set_y(STRIP_TOP - t2.bar_h / 2)], run_time=0.6)
            self.play(FadeIn(page, shift=UP * 0.15), run_time=0.5)
        for r in page.rows:          # ~4 s: the steps tick GREEN top to bottom
            ok = state_mark("ok", 0.3).move_to(r.mark)
            self.play(Transform(r.mark, ok), run_time=0.36)
        self.wait(0.5)

        # ========================================================== 8. what green means; your own check
        lp = ReleaseLoop(release=True)
        lp.shift(UP * (2.7 - lp.get_top()[1]))
        mon = lp.boxes["monitor"]
        g1 = ok_chip("green run = every step that ran exited 0", 22)
        g2 = grey_chip("reload the site · sudo docker container ls → the IMAGE column shows the new tag", 20)
        g1.move_to([6.4 - g1.width / 2, lp.get_bottom()[1] - 0.45, 0])
        g2.move_to([6.4 - g2.width / 2, g1.get_y() - 0.65, 0])
        link = DashedLine(mon.get_bottom(), [mon.get_x(), g1.get_top()[1], 0], color=TURN, stroke_width=3,
                          dash_length=0.1)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(t2, sh, page)), run_time=0.5)
            self.remove(t2, sh, page, *t2.get_family(), *page.get_family())
            self.play(FadeIn(lp, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("A green run means")
            lit = box(mon.frame.width, mon.frame.height, TURN, fill_opacity=0.12).move_to(mon.frame)
            self.play(Transform(mon.frame, lit), lp.light("monitor", TURN), run_time=0.7)
            lp._reseat(self)
            self.play(Create(link), FadeIn(g1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("not that the app works")
            self.play(Indicate(g1.text, color=PASS, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Reload your site")
            self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and find the new tag")
            self.play(Indicate(g2.text, color=INK, scale_factor=1.04), run_time=0.8)

        # ========================================================== 9. delivery or deployment? PONDER
        lr2 = lref("11–12")
        tg = ReleaseToggle()
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(lp, g1, g2, link)), run_time=0.5)
            self.remove(lp, g1, g2, link, *lp.get_family())
            self.play(FadeIn(lr2), FadeIn(tg), run_time=0.5)
            tg.ends(self, run_time=0.6)
            self.play(tg.animate.shift(np.array([-0.6, -0.4, 0])), run_time=0.5)
            vo.wait_until("is typing slash run deploy app")
            rb = tg.hover_ribbon(self, KEYWORD, run_time=0.5)
            self.play(rb.animate.shift(UP * 0.6), run_time=0.4)
            vo.wait_until("continuous delivery")
            self.play(Circumscribe(tg.button, color=INK, buff=0.08), run_time=0.7)
            vo.wait_until("or continuous deployment")
            self.play(Circumscribe(tg.ring, color=INK, buff=0.08), run_time=0.7)
            vo.wait_until("What would make it the other")
            self.play(Indicate(rb.text, color=ROUTE, scale_factor=1.1), run_time=0.7)
        card = ponder(self, PONDER_Q, seconds=10)

        # ========================================================== 10. delivery; MS5 makes it deployment
        test = label_box("Test", S.GREY, dashed=True, box_w=1.55)
        test.move_to([0.4, tg.cards.get_y(), 0])
        test_ok = label_box("Test", INK, box_w=1.55)
        test_ok.frame.become(box(1.55, test.frame.height, PASS, fill_opacity=0.2))
        test_ok.move_to(test)
        l21 = ok_chip("L21", 20).next_to(test, UP, buff=0.15)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.remove(card, *card.get_family())
            tg.into_hand(self, run_time=0.9)
            n1 = tg.label_end(self, "continuous delivery", at="button")
            vo.wait_until("A person decides")
            self.play(tg.hand.animate(rate_func=there_and_back).shift(DOWN * 0.18),
                      tg.button.frame.animate(rate_func=there_and_back).set_fill(ERR, 0.95),
                      Indicate(tg.button.text, color=INK), run_time=0.8)
            vo.wait_until("and nothing is tested first")
            self.play(FadeIn(test, scale=0.9), run_time=0.5)
            self.play(Indicate(test.text, color=S.GREY, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Deploy every merge to main")
            tg.drop(self, n1, tg.rib, run_time=0.4)
            self.play(FadeOut(tg.button), FadeOut(tg.hand), tg.ring.animate.move_to(tg.button.get_center()),
                      run_time=0.7)
            tg._gone(self, tg.button, tg.hand)
            vo.wait_until("behind the tests")
            self.play(ReplacementTransform(test, test_ok), FadeIn(l21, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("and it becomes continuous deployment")
            self.play(LaggedStart(*[c.animate.move_to(tg.ring.get_center()).set_opacity(0) for c in reversed(tg.cards)],
                                  lag_ratio=0.3), Rotate_safe(tg.ring.ring), run_time=1.4)
            tg._reseat(self)
            n2 = tg.label_end(self, "continuous deployment", at="ring")
            vo.wait_until("That is Milestone 5")
            ms5 = label("every merge to main · Milestone 5", 20, PASS).next_to(n2, DOWN, buff=0.15)
            self.play(FadeIn(ms5, shift=UP * 0.1), run_time=0.5)

        rest = VGroup(tg, test_ok, l21, ms5, lr2)
        self.play(FadeOut(rest), FadeOut(tr), run_time=0.6)
        self.remove(rest, tr, *rest.get_family())
        self.wait(0.3)


def _glyphs(line, prompt: str = P_REPO):
    """The command glyphs of a typed line (a folded command: every row), without the prompt."""
    rows = line.rows if hasattr(line, "rows") else [line]
    return VGroup(glyph_range(rows[0], len(prompt) + 1), *[glyph_range(r, 0) for r in rows[1:]])
