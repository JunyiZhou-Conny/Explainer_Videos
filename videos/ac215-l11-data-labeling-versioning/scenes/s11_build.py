"""S11 · The starter that no longer builds — tracker I2 → I3 (+ extra row); `lref("26, 29–32")`.

Beats (script.md, ## S11; one voiceover block each):
0. TRACKER I2. README card (data-versioning README 234–238, "Make sure you are inside the
   data-versioning folder: cd data-versioning") + GREY chip "already inside since scene 10 · this
   line is for a new terminal". TRACKER I3: `sh docker-shell.sh` → 86: 2, …, 1075–1081, …, 1125 cut
   after "failed to solve:" (wrap); 1075 and 1078–1079 YELLOW, 1081 RED; ▶ your turn.
1. Erratum card: CODE(starter Dockerfile:36), `google-cloud-sdk` RED, caption "Google renamed the
   apt package · main fixed line 36 in ebf09c8 · the starter branch never got it". TRACKER I3 ·
   extra row: a strip types 87's sed (' \\' folds before the quoted edit and after '&&'; tags
   `extra`, "our editor; use yours · this sed -i is GNU syntax") → 87: 2, shown large with
   `google-cloud-cli` GREEN, "your new line 36"; ▶.
2. TRACKER I3: `sh docker-shell.sh` (▶) → 88: 2–3 (squashed), …, 27–31; chips on 3 and 30. Then V4
   replays broken, one stage per printed line: 32 (gcloud side note RED, key crossed), 39 from
   "failed to detect credentials" (gcsfuse pipe stops short), 41 (YELLOW sign 'GCS bucket mounted'
   beside CODE(entrypoint.sh:11) + chip "printed no matter what"), 42 (stage 3 RED, "special device
   does not exist"). 33–38 and 40 never printed.
3. TRACKER I3 · extra: root prompt (88:45) + chip "no set -e"; ls -la cheese_dataset → 46–48 RED;
   which dvc → 50; dvc --version → 52 + "pinned by uv.lock · at the time of recording". YELLOW rule
   card "ls cheese_dataset before dvc add" parks in the corner.
4. MountLayers with a real key (`illustration`): -v, gcsfuse, inner bind, four blank tiles inside;
   the host's cheese_dataset/ dark. PONDER 8 s.
5. The pipes glow inside the container only ("the container's own mounts"); exit (88:66–67); host
   prompt; ls -la cheese_dataset (extra) → 89: 2–4, `root` ORANGE; chips "made by the entrypoint's
   mkdir -p, through /app" and "here the mount failed · with a real key, this view is the same".
   Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]
DV = "data-versioning"
ENTRY = "data-versioning@data-versioning-ac215/docker-entrypoint.sh"
DOCKERFILE = "data-versioning@data-versioning-ac215/Dockerfile"
TS = 20                       # terminal size in this scene (72 characters a row)
ALREADY = "already inside since scene 10 · this line is for a new terminal"
RENAMED = ("Google renamed the apt package", "main fixed line 36 in ebf09c8",
           "the starter branch never got it")
GNU = "our editor; use yours · this sed -i is GNU syntax"
PONDER_Q = "Inside, ls cheese_dataset lists\nfour photos; on your laptop it's empty.\nIs the mount broken?"


def words(*parts, size: float = 20, color=INK) -> VGroup:
    """One row of label/mono pieces: plain strings are label font, ('x', 'mono') pieces mono."""
    ms = [mono(p[0], size, color) if isinstance(p, tuple) else label(p, size, color) for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=0.12)


def fold_before(t, *marks: str):
    """A fold for terminal t that breaks a command with ' \\' right before each of `marks` (spaces
    outside quotes), the next row indented by 4: rows paste back as one valid shell command."""
    def fold(text: str, first_prefix: int = 0) -> list[str]:
        rows, cur = [], text
        for m in marks:
            i = cur.index(" " + m, first_prefix if not rows else 0)
            rows.append(cur[:i] + " \\")
            cur = "    " + cur[i + 1:]
        rows.append(cur)
        assert all(len(r) <= t.max_chars for r in rows), rows
        assert " ".join(r.removesuffix(" \\").strip() for r in rows) == text.strip(), rows
        return rows
    return fold


def band_mid(t) -> float:
    """The centre of the free band between the tracker row and terminal t's top edge."""
    return (PIC_TOP + t.box.get_top()[1] + 0.12) / 2


class StarterFix(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 6, len(SAY)

        # ========================================================== 0. I2 → I3: the starter fails to build
        ref = lref("26, 29–32")
        tr = tracker("I", 2)
        t = term(P_VERSIONING, rows=4, size=TS)
        c234 = readme_card((234, 238), VGroup(
            words("Make sure you are inside the", (DV, "mono"), "folder:"),
            mono("cd data-versioning", 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.18), size=20, repo=DV)
        c234.move_to([0, 1.25, 0])
        already = grey_chip(ALREADY).next_to(c234, DOWN, buff=0.2)
        c86 = capture("86")
        assert c86.cmd in readme(243, DV) and readme(237, DV) == "cd data-versioning"
        y, r = TURN, ERR
        lines86 = [c86.line(2), "…", (c86.line(1075), y), c86.line(1076), c86.line(1077), (c86.line(1078), y),
                   (c86.line(1079), y), c86.line(1080), (c86.line(1081), r), "…",
                   (cut(c86.line(1125), "failed to solve:"), r)]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(c234, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            self.play(Indicate(c234.body[1], color=INK, scale_factor=1.05), run_time=0.7)
            self.play(FadeIn(already, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("so run sh docker-shell.sh")
            self.play(track(tr, 3), run_time=0.4)
            ln86 = type_cmd(self, t, c86.cmd, type_time=0.5)
            vo.wait_until("Pause and run it")
            yt = beside(turn_row(), ln86)
            pin(self, ln86, yt)
            flash_tag(self, yt, TURN)
            vo.wait_until("On the starter branch")
            self.play(FadeOut(VGroup(c234, already), shift=UP * 0.15), run_time=0.4)
            self.remove(c234, already)
            resize(self, t, 14, run_time=0.6)
            out(self, t, lines86, wrap=True, run_time=1.4)
            vo.wait_until("package google-cloud-sdk has no installation candidate")
            e81 = t.find("has no installation candidate")
            self.play(Indicate(substring(e81, "google-cloud-sdk"), color=ERR, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The message even names the replacement")
            hit = t.find("  google-cloud-cli")
            hb = hl_bar(substring(hit, "google-cloud-cli"), TURN, 0.3)
            self.play(FadeIn(hb), Indicate(substring(hit, "google-cloud-cli"), color=TURN, scale_factor=1.15),
                      run_time=0.8)
            hit.submobjects.insert(0, hb)

        # ========================================================== 1. erratum: Dockerfile:36, the one-word fix
        p36 = code(DOCKERFILE, 36, font_size=20).move_to([0, 1.75, 0])
        sdk = code_span(p36.code, 0, "google-cloud-sdk")
        bar36 = line_bar(p36.code, 0, ERR, opacity=0.2)
        er = erratum_tag()
        er.move_to([p36.get_right()[0] - er.width / 2, p36.header.get_center()[1], 0])
        kind = card(list(RENAMED), S.GREY, size=22).next_to(p36, DOWN, buff=0.35)
        c87 = capture("87")
        s = term(P_VERSIONING, rows=4, size=TS)   # 3 folded command rows + its output
        xt = on_bar(s, extra_row())
        gnu = grey_chip(GNU)
        new36 = c87.line(2)
        big = mono(new36.strip(), 24, INK, t2c={"google-cloud-cli": PASS}).move_to([0, 0.45, 0])
        cap36 = note("your new line 36", INK, 22).next_to(big, DOWN, buff=0.2)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t), FadeIn(p36, shift=UP * 0.2), run_time=0.7)
            self.remove(t, *t.lines)
            self.play(FadeIn(bar36), FadeIn(er, shift=LEFT * 0.1), sdk.animate.set_color(ERR), run_time=0.6)
            vo.wait_until("Google renamed the package")
            self.play(FadeIn(kind, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the main branch fixed line 36")
            self.play(Indicate(kind.body[1], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and the starter never got the fix")
            self.play(Indicate(kind.body[2], color=INK, scale_factor=1.04),
                      Indicate(sdk, color=ERR, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Make the same one-word change")
            self.play(FadeOut(kind), FadeIn(s, shift=UP * 0.2), track(tr, 3, extra="row"), run_time=0.6)
            self.remove(kind)
            gnu.next_to(s.box, UP, buff=0.15).align_to(s.box, RIGHT)
            s.fold = fold_before(s, "'36s/", "sed -n")
            type_cmd(self, s, c87.cmd, type_time=1.2)
            del s.fold
            vo.wait_until("as an extra")
            self.play(FadeIn(xt, shift=LEFT * 0.1), FadeIn(gnu, shift=UP * 0.1), run_time=0.5)
            r87 = out(self, s, [new36], run_time=0.3)[-1]
            self.play(substring(r87, "google-cloud-cli").animate.set_color(PASS),
                      TransformFromCopy(substring(r87, new36.strip()), big), run_time=0.9)
            self.play(FadeIn(cap36, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Pause and edit it")
            yt1 = turn_row().next_to(xt, LEFT, buff=0.15)
            self.play(FadeIn(yt1, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt1, TURN)

        # ========================================================== 2. run again: the entrypoint fails, stage by stage
        c88 = capture("88")
        fm = FuseMount()
        side = fm.side_note()
        side.set_color(ERR)
        x_key = cross_mark(0.45, ERR).move_to(fm.key[0])
        mx = fm.mnt.get_center()[0]
        top = fm.bucket.frame.get_bottom()[1]
        stub = pipe([[mx, top, 0], [mx, top - 0.35, 0]], ERR, glow=False, dashed=True)
        x_pipe = cross_mark(0.3, ERR).move_to([mx, top - 0.55, 0])
        sign = fm.sign()
        msg = note("special device does not exist", ERR).next_to(fm.mnt_images, DOWN, buff=0.18).align_to(
            fm.mnt, LEFT)
        p11 = code(ENTRY, 11)
        p11.move_to([-1.45, 2.62 - p11.height / 2, 0])
        always = grey_chip("printed no matter what").next_to(p11, RIGHT, buff=0.3)
        l39 = c88.line(39)
        from39 = "…" + l39[l39.index("failed to detect credentials"):]

        def fail(i):
            g = fm.stages[i]
            return AnimationGroup(g.frame.animate.set_stroke(ERR), g.text.animate.set_color(ERR))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p36, bar36, er, big, cap36, gnu, xt, yt1)), track(tr, 3), run_time=0.5)
            self.remove(p36, bar36, er, big, cap36, gnu, xt, yt1)
            resize(self, s, 9, keep=0, run_time=0.6)
            ln88 = type_cmd(self, s, c88.cmd, type_time=0.4)
            yt2 = beside(turn_row(), ln88)
            pin(self, ln88, yt2)
            flash_tag(self, yt2, TURN)
            vo.wait_until("The first build is slow")
            r3 = out(self, s, [c88.line(2), squash(c88.line(3))], run_time=0.4)[-1]
            slow = grey_chip("slow the first time · at the time of recording").next_to(s.box, UP, buff=0.2) \
                .align_to(s.box, RIGHT)
            self.play(FadeIn(slow, shift=LEFT * 0.1), Indicate(substring(r3, "409.4s"), color=INK), run_time=0.5)
            out(self, s, ["…", *c88.at((27, 31))], run_time=0.6)
            r30 = s.find("Python 3.11.17")
            tm = beside(time_row(), r30, buff=0.3)
            pin(self, r30, tm)
            vo.wait_until("Then the entrypoint runs")
            self.play(Indicate(substring(r30, "3.11.17"), color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("the way a missing key fails")
            self.play(FadeOut(slow), run_time=0.3)
            self.remove(slow)
            unpin(self, r30, tm)
            resize(self, s, 3, keep=1, run_time=0.5)
            self.play(FadeIn(fm), run_time=0.7)
            vo.wait_until("The gcloud tool cannot find the key file")
            out(self, s, [(c88.line(32), ERR)], wrap=True, run_time=0.5)
            self.play(FadeIn(side, shift=LEFT * 0.1), Create(x_key), fail(0), run_time=0.7)
            vo.wait_until("and neither can gcsfuse")
            out(self, s, [(from39, ERR)], wrap=True, run_time=0.5)
            self.play(FadeOut(side), run_time=0.4)
            self.remove(side)
            self.play(Create(stub), run_time=0.5)
            self.play(Create(x_pipe), fail(1), run_time=0.5)
            vo.wait_until("Yet the next line says bucket mounted")
            out(self, s, [c88.line(41)], run_time=0.3)
            self.play(FadeIn(sign, scale=1.15), run_time=0.5)
            flash_tag(self, sign, TURN)
            vo.wait_until("because the script prints it")
            self.play(FadeOut(VGroup(fm.stages, fm.bucket)), FadeIn(p11, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(always, shift=LEFT * 0.1), Indicate(p11.code, color=TURN, scale_factor=1.04),
                      run_time=0.7)
            vo.wait_until("Then the bind mount fails")
            self.play(FadeOut(VGroup(p11, always)), FadeIn(VGroup(fm.stages, fm.bucket)), run_time=0.5)
            self.remove(p11, always)
            out(self, s, [(c88.line(42), ERR)], wrap=True, run_time=0.4)
            self.play(FadeIn(msg, shift=UP * 0.1), fail(2), Indicate(fm.mnt_images.text, color=ERR), run_time=0.7)
            vo.wait_until("special device does not exist")
            self.play(Indicate(msg, color=ERR, scale_factor=1.08), run_time=0.6)

        # ========================================================== 3. a root prompt anyway: extra checks
        rule = card([words(("ls cheese_dataset", "mono"), "before", ("dvc add", "mono"), size=22)], TURN, size=22,
                    head="rule for today")
        xt3 = extra_row()
        p45, cmd45 = c88.istep(45)
        assert cmd45 == "ls -la cheese_dataset"

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(fm, x_key, stub, x_pipe, sign, msg)), run_time=0.5)
            self.remove(fm, x_key, stub, x_pipe, sign, msg)
            resize(self, s, 9, keep=0, run_time=0.6)
            on_bar(s, xt3)                # place on the 9-row title bar (after resize)
            s.set_prompt(p45)
            ln_root = bare_prompt(self, s)
            self.play(Indicate(substring(ln_root, "root@9a9e6dff5c15:/app#"), color=INK, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("because the entrypoint does not stop")
            nse = beside(row_tag("no set -e"), ln_root, buff=0.4)
            pin(self, ln_root, nse)
            flash_tag(self, nse, INK)
            vo.wait_until("Extra checks")
            self.play(FadeIn(xt3, shift=LEFT * 0.1), track(tr, 3, extra=True), run_time=0.5)
            istep(self, s, c88.line(45), type_time=0.4)
            out(self, s, [(x, ERR) for x in c88.at((46, 48))], run_time=0.4)
            e48 = s.find("..")
            vo.wait_until("the cheese dataset folder is empty")
            self.play(each([s.find("total 8"), e48], ERR, scale=1.05), run_time=0.7)
            vo.wait_until("and DVC 3.63.0 is installed")
            istep(self, s, c88.line(49), type_time=0.3)
            out(self, s, c88.at(50), run_time=0.3)
            istep(self, s, c88.line(51), type_time=0.3)
            r52 = out(self, s, c88.at(52), run_time=0.3)[-1]
            vo.wait_until("pinned by the lock file")
            pinned = beside(row_tag("pinned by uv.lock · at the time of recording"), r52, buff=0.4)
            pin(self, r52, pinned)
            self.play(Indicate(substring(r52, "3.63.0"), color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("So the rule for today")
            rule.move_to([0, band_mid(s), 0])
            self.play(FadeIn(rule, scale=1.1), run_time=0.6)
            vo.wait_until("list the folder before you add it")
            self.play(Indicate(rule.body, color=TURN, scale_factor=1.06), run_time=0.6)
            self.play(rule.animate.move_to([6.5 - rule.width / 2, 2.25, 0]), run_time=0.7)

        # ========================================================== 4. two views with a real key; Ponder 7
        ml = MountLayers()
        ill = illustration_tag().next_to(ml.laptop, UP, buff=0.12).align_to(ml.laptop, RIGHT)
        tiles = ml.photos(4)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(xt3, rule)), track(tr, 3), run_time=0.4)
            self.remove(xt3, rule)
            resize(self, s, 3, keep=1, run_time=0.6)
            self.play(FadeIn(ml), FadeIn(ill), run_time=0.7)
            self.play(ml.light_v(), run_time=0.7)
            vo.wait_until("With a real key")
            self.play(ml.light_fuse(), run_time=0.7)
            self.play(ml.light_inner(), run_time=0.7)
            vo.wait_until("lists your four photos")
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.15) for x in tiles], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("on your laptop, the same folder is empty")
            self.play(ml.dark(), Indicate(ml.host_data.text, color=LAPTOP, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Is the mount broken?")
            self.play(Indicate(ml.host_data.text, color=INK, scale_factor=1.06), run_time=0.6)
        pc = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 5. no: both mounts live in the container
        glow = VGroup(*[p.core.copy().set_stroke(ROUTE, 12, opacity=0.35) for p in (ml.fuse, ml.inner)])
        own = note("the container's own mounts").next_to(ml.laptop, DOWN, buff=0.1).align_to(ml.box, RIGHT)
        c89 = capture("89")
        made = grey_chip("made by the entrypoint's mkdir -p, through /app")
        same = grey_chip("here the mount failed · with a real key, this view is the same")
        xt5 = extra_row()

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            vo.wait_until("Both mounts exist only inside the container")
            self.play(FadeIn(glow), Indicate(ml.box_title, color=IMAGE, scale_factor=1.08), run_time=0.7)
            self.play(FadeIn(own, shift=LEFT * 0.1), run_time=0.5)
            istep(self, s, c88.line(66), type_time=0.2)
            out(self, s, c88.at(67), run_time=0.3)
            s.set_prompt(P_VERSIONING)
            bare_prompt(self, s)
            vo.wait_until("Your laptop sees the empty folder")
            self.play(Indicate(ml.host_data.text, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("through the repo mount")
            self.play(Indicate(ml.v_label, color=INK, scale_factor=1.04),
                      ml.v_pipe.animate.set_stroke(width=8), run_time=0.7)
            vo.wait_until("an extra listing shows it")
            self.play(FadeOut(VGroup(ml, glow, own, ill, tiles, ml.v_pipe, ml.v_label, ml.fuse, ml.inner,
                                     ml.inner_label)), run_time=0.5)
            self.remove(ml, glow, own, ill, tiles, ml.v_pipe, ml.v_label, ml.fuse, ml.inner, ml.inner_label)
            resize(self, s, 6, keep=1, run_time=0.5)
            on_bar(s, xt5)                # place on the 6-row title bar (after resize)
            self.play(FadeIn(xt5, shift=LEFT * 0.1), track(tr, 3, extra=True), run_time=0.4)
            type_cmd(self, s, c89.cmd, type_time=0.3)
            out(self, s, c89.at((2, 4)), run_time=0.4)
            r3 = s.find("drwxr-sr-x    2 root")
            vo.wait_until("owned by root")
            made.next_to(s.box, UP, buff=0.2).align_to(s.box, LEFT)
            same.next_to(made, UP, buff=0.2).align_to(s.box, LEFT)
            self.play(substring(r3, "root").animate.set_color(ROOT), FadeIn(made, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(substring(r3, "root"), color=ROOT, scale_factor=1.2), run_time=0.6)
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
            flash_tag(self, same, INK)

        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)

