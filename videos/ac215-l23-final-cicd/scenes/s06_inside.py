"""S06 · Inside the toolbox: whose Docker? — tracker B 3 · extra (README › Deployment Steps ·
docker-shell.sh). No lecture tag (script.md has no LECTURE mark in this scene). V5 SiblingContainers.

Beats (script.md "## S06"; one voiceover block each):
0. TRACKER B 3 · extra. V5 (GREY laptop frame, its folders, the TEAL crate, the Docker engine shelf
   holding cheese-app-deployment). Under it a two-row source strip of docker-shell.sh (header
   "docker-shell.sh · lines a–b" in its left column) steps through lines 35–46 two at a time, the
   narrated mount row PINK, line 39 GREY and never animated: 35–36 (the socket: thick PINK socket
   line + /var/run/docker.sock), 37–38 (/app, /secrets), 39–40 (/api-service), 41–42
   (/frontend-react, /vector-db), then 43–44 and 45–46: the badge flies from the secrets folder
   into the crate (V3) as the four -e lines are read.
1. The strip leaves; V5 stays. A PURPLE "docker build" spark (words stacked) hovers in the crate's
   free right-hand corner.
   PONDER 8 s (the card covers the picture while the timer runs).
2. The card leaves. The spark runs down the PINK socket into the laptop's engine; a TEAL cube lands
   on the shelf beside the toolbox, GREEN chip "sibling". Then a RED "docker system prune -a" runs
   the same way and a broom sweeps the whole shelf (a ghost, then undone).
3. The picture leaves. A toolbox terminal: GREY heading row "versions · extra", then laptop/32: 36,
   40, 46, 50–53, 55, 57, 59 as one block (36 cut after Python/3.14.8, 46 after 3.8.10) (not typed; the cryptography pair is cropped by text; 59 GREY).
   "at the time of recording" on the title bar. Four chips lift out of their lines, one per phrase:
   PURPLE aws-cli 2.39.6, Docker CLI 28.1.1, kubectl v1.28.15, ansible 6.7.0 (turns RED).
4. CODE(Dockerfile: 37) alone (20 pt, trimmed at 74). The `>` flashes; the line splits: a copy of
   "pip install ansible" slides left (PURPLE), `>` becomes a PINK arrow carrying "=9.0.0" into a
   file inside a GREY "/" box. A 5-row toolbox strip types laptop/33's two commands and prints 36–37
   (wrapped, '=9.0.0' RED) and 39–40, 42 (cut after ansible-core-2.13.13, wrapped); the file and the
   strip's RED name pulse together; the installed ansible-6.7.0 (last row) is underlined. On "on an old Python" laptop/32:46 (python version = 3.8.10…) fades in GREY under pip and flashes. On "Quoting fixes it" the split
   picture leaves and the two-line erratum card (erratum tag at its left) takes its row; its second
   line comes on "but leave it for now".
5. A 20 pt toolbox terminal, alone: heading row "every ansible-playbook run starts with:", then
   laptop/40: 36–37 (the cryptography pair, GREY, line 36 cut after "no longer supported") and
   38–41 (wrapped). Each group flashes on its phrase; then all fold into the GREY chip
   "warnings · hidden from here on".
6. A 5-row toolbox strip types `aws sts get-caller-identity` (extra) and prints laptop/34: 37 RED
   (wrapped). Above it the WHITE badge with a GREY chip "placeholder", then a GREY dashed chip
   "with your key: your account ID and your user".
7. Same strip (cleared), in a silent typing beat before the block: `ansible-inventory -i
   inventory.yml --graph` prints laptop/35: 38–41; then the first three rows flash GREEN and V4's
   InventoryTree builds above (top right, clear of the strip's title bar) from them, one node per phrase. Then the tree
   leaves, the strip grows to 7 rows, the loop of laptop/36: 35 is typed (folded) and 39, 47, 51,
   55, 59 print GREEN. Fade; empty frame.

Deviations from SHOW: V5 (9.0 x 5.2) and CODE(docker-shell.sh: 35–42) (8.9 x 3.4) cannot stand side
by side at 20 pt, so the code stands under V5 as a two-row strip (all of lines 35–46, two at a time,
header kept in the strip's left column) and steps along with the narration. Block 4's strip has 5
rows, not 3, so the ls listing and the head/tail output stay readable together. Block 5's line 36
is cut after "no longer supported" (a 285-character line). Block 4's ls rows are squeezed
(squeeze_spaces) before wrapping, so the listing reads as a list. Block 7's rows do not morph into
the tree (the Transform showed a shrunken box mid-way): the tree's nodes fly in from the rows. Block 6 adds the placeholder-badge chips
(no output is invented: "with your key" is GREY dashed, the future).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.devops import PANEL
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]

SH = "src/deployment/docker-shell.sh"
DF = "src/deployment/Dockerfile"

# ------------------------------------------------------------------ the real sources (checked)
assert excerpt(SH, 36, 36).strip() == "-v /var/run/docker.sock:/var/run/docker.sock \\"
assert excerpt(SH, 37, 37).strip() == '-v "$BASE_DIR":/app \\'
assert excerpt(SH, 39, 39).strip() == '-v "$HOME/.ssh":/home/app/.ssh \\'
assert excerpt(SH, 43, 43).strip().startswith("-e AWS_ACCESS_KEY_ID=")
assert excerpt(SH, 46, 46).strip().startswith("-e AWS_ACCOUNT_ID=")
assert excerpt(DF, 37, 37).strip().startswith("pip install ansible>=9.0.0 openshift")
assert toolbox_capture("33").cmds[1][1] == 'head -3 "/=9.0.0"; tail -1 "/=9.0.0"'
assert toolbox_capture("35").cmd == "ansible-inventory -i inventory.yml --graph"
assert toolbox_capture("34").cmd == "aws sts get-caller-identity"

V5_SHIFT = 0.2           # V5's frame: y -2.4 .. 2.8 (PIC_TOP)


# ------------------------------------------------------------------ helpers of this scene
def src_strip(a: int, b: int, hot=(), grey=(), hot_color=ROUTE):
    """A two-row source strip of docker-shell.sh lines a..b under V5 (y -3.58 .. -2.63): left
    column 'docker-shell.sh' / 'lines a–b' (GREY), a thin divider, the lines in mono 20 pt (rows in
    `hot` PINK, rows in `grey` GREY). .rows{n} .head"""
    rows = {}
    col = VGroup()
    for n in range(a, b + 1):
        s = excerpt(SH, n, n)
        c = hot_color if n in hot else (S.GREY if n in grey else INK)
        ln = mono_line(s, 20, c)
        rows[n] = ln
        col.add(ln)
    col.arrange(DOWN, aligned_edge=LEFT, buff=0.367 - col[0].height)
    head = VGroup(mono("docker-shell.sh", 20, S.GREY), label(f"lines {a}–{b}", 20, S.GREY))
    head.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    bg = RoundedRectangle(width=12.6, height=0.95, corner_radius=0.14, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(PANEL, 1)
    bg.move_to([0, -3.105, 0])
    head.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.25)
    div = Line(UP * 0.38, DOWN * 0.38, color=S.GREY_DARK, stroke_width=2)
    div.move_to([head.get_right()[0] + 0.25, bg.get_y(), 0])
    col.move_to(bg).align_to(div, LEFT).shift(RIGHT * 0.3)
    g = VGroup(bg, div, head, col)
    g.rows, g.head, g.body = rows, head, col
    return g


def swap_strip(scene, old, new, run_time: float = 0.5):
    """PLAYS: one strip view becomes the next (rows slide up, the header changes)."""
    scene.play(FadeOut(old.body, shift=UP * 0.25), FadeIn(new.body, shift=UP * 0.25),
               Transform(old.head, new.head), run_time=run_time)
    scene.remove(old, *old.get_family())
    scene.add(new)
    return new


def lines_of(t: Terminal, sub: str):
    """Every row of terminal t whose text contains sub."""
    return [ln for ln in t.lines if sub in getattr(ln, "text", "")]


def fade_all(scene, *mobs, run_time: float = 0.5):
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


class InsideToolbox(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 8, len(SAY)

        # ========================================================== 0. how the toolbox was started
        tr = tracker_b(3, True)
        v5 = SiblingContainers()
        v5.shift(UP * V5_SHIFT)
        # the 'sibling' chip of build() would touch the socket's path label: lift the label a little
        v5.socket_label.shift(UP * 0.35)
        st = src_strip(35, 36, hot=(36,))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(v5, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(st, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(v5.crate.text, color=IMAGE, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Line 36 mounts")
            self.play(Indicate(st.rows[36], color=ROUTE, scale_factor=1.04), run_time=0.6)
            v5.mount(self, "socket", run_time=0.8)
            self.play(Indicate(v5.socket_label, color=ROUTE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Then the deployment folder")
            st = swap_strip(self, st, src_strip(37, 38, hot=(37,)))
            v5.mount(self, "app", run_time=0.6)
            vo.wait_until("your secrets")
            self.play(st.rows[37].animate.set_color(INK), st.rows[38].animate.set_color(ROUTE), run_time=0.3)
            v5.mount(self, "secrets", run_time=0.6)
            vo.wait_until("and the three app folders")
            st = swap_strip(self, st, src_strip(39, 40, hot=(40,), grey=(39,)), run_time=0.4)
            v5.mount(self, "api", run_time=0.45)
            st = swap_strip(self, st, src_strip(41, 42, hot=(41, 42)), run_time=0.4)
            v5.mount(self, "frontend", run_time=0.45)
            v5.mount(self, "vectordb", run_time=0.45)
            vo.wait_until("Lines 43 to 46")
            st = swap_strip(self, st, src_strip(43, 44, hot=(43, 44), hot_color=TURN))
            v5.badge_in(self, run_time=0.8)
            st = swap_strip(self, st, src_strip(45, 46, hot=(45, 46), hot_color=TURN))
            self.play(Indicate(v5.badge, color=TURN, scale_factor=1.3), run_time=0.7)

        # ========================================================== 1. ponder: whose disk?
        with self.voiceover(SAY[1]) as vo:
            fade_all(self, st, run_time=0.4)
            vo.wait_until("Inside the toolbox")
            # hover_spark() would sit on the badge and /vector-db: the spark waits in the crate's free
            # right-hand corner instead, its words stacked
            sp = VGroup(spark(TOOL, 0.3), VGroup(label("docker", 20, TOOL), label("build", 20, TOOL))
                        .arrange(DOWN, buff=0.06))
            sp[1].next_to(sp[0], DOWN, buff=0.1)
            sp.move_to([3.25, 1.3, 0])
            self.play(FadeIn(sp, scale=0.6), run_time=0.6)
            self.play(Indicate(sp[1], color=TOOL, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Whose disk")
            self.play(Indicate(v5.crate.text, color=IMAGE, scale_factor=1.08),
                      Indicate(v5.title, color=INK, scale_factor=1.1), run_time=0.9)
        card = ponder(self, "Inside the toolbox, Ansible runs docker build\nfor the frontend.\n"
                            "Whose disk does the image land on:\nthe toolbox's, or your laptop's?", seconds=8)

        # ========================================================== 2. the laptop's: siblings
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.remove(card, *card.get_family())
            self.play(Indicate(v5.title, color=INK, scale_factor=1.2), run_time=0.7)
            vo.wait_until("No Docker engine runs")
            self.play(Circumscribe(v5.crate.frame, color=IMAGE, buff=0.06), run_time=0.9)
            vo.wait_until("talks through the socket")
            cube, sib = v5.build(self, sp, run_time=2.0)
            vo.wait_until("So the image lands beside")
            self.play(Indicate(sib.text, color=OWN, scale_factor=1.15),
                      Indicate(v5.images[0][1], color=IMAGE, scale_factor=1.06), run_time=0.9)
            vo.wait_until("That's also why a prune")
            v5.prune_ghost(self, run_time=2.4)

        # ========================================================== 3. versions (extra)
        x32 = toolbox_capture("32")
        t = toolbox_term("32", rows=11)
        rec = on_bar(t, time_row())
        # 36 cut after the CLI's own bundled Python (one row), so 46 (the toolbox's Python) fits
        vers = [cut(x32.line(36), "Python/3.14.8")] + x32.at(40) + [cut(x32.line(46), "3.8.10")] \
            + x32.at((50, 53), 55, 57)
        chips = VGroup(tool_chip("aws-cli 2.39.6"), tool_chip("Docker CLI 28.1.1"),
                       tool_chip("kubectl v1.28.15"), tool_chip("ansible 6.7.0"))
        chips.arrange(RIGHT, buff=0.35).move_to([0, 2.3, 0])
        bad = err_chip("ansible 6.7.0", mono_font=True).move_to(chips[3])
        with self.voiceover(SAY[3]) as vo:
            fade_all(self, v5, run_time=0.5)
            self.play(FadeIn(t), run_time=0.4)
            put_heading(self, t, "versions · extra")
            out(self, t, vers + [(x32.line(59), S.GREY)], wrap=True, run_time=1.0)
            self.play(FadeIn(rec), run_time=0.3)
            vo.wait_until("the AWS command line")
            src = [lines_of(t, "aws-cli/")[0], lines_of(t, "Docker version")[0],
                   lines_of(t, "Client Version")[0], lines_of(t, "Version: 6.7.0")[0]]
            for i, phrase in enumerate([None, "Docker,", "kubectl", "and Ansible are there"]):
                if phrase:
                    vo.wait_until(phrase)
                self.play(Indicate(src[i], color=TOOL, scale_factor=1.03), run_time=0.4)
                self.play(FadeTransform(src[i].copy(), chips[i]), run_time=0.6)
            vo.wait_until("but not the Ansible")
            self.play(FadeOut(chips[3]), FadeIn(bad), Indicate(src[3], color=ERR, scale_factor=1.05),
                      run_time=0.7)
            chips.remove(chips[3])
            chips.add(bad)
            self.play(Indicate(bad.text, color=ERR, scale_factor=1.12),
                      Indicate(lines_of(t, "python version")[0], color=TURN, scale_factor=1.04), run_time=0.6)

        # ========================================================== 4. the '>' redirect
        dfp = code(DF, 37, 37, font_size=20, trim=74)
        dfp.move_to([0, 2.75 - dfp.height / 2, 0])
        gt_g = code_span(dfp.code, 0, ">")
        left = code_span(dfp.code, 0, "pip install ansible").copy()
        ver = code_span(dfp.code, 0, "=9.0.0").copy()
        row_y = 0.85
        root = box(2.7, 0.95, S.GREY, fill_opacity=0.06)
        root.move_to([4.6, row_y, 0])
        root_t = mono("/", 22, S.GREY).move_to(root.get_corner(UL) + np.array([0.25, -0.25, 0]))
        fg = file_glyph(0.42, S.GREY).move_to(root).shift(LEFT * 0.75)
        fname = mono("=9.0.0", 22, ERR).next_to(fg, RIGHT, buff=0.15)
        arr = Arrow([-1.0, row_y, 0], [3.1, row_y, 0], color=ROUTE, stroke_width=5, buff=0,
                    max_tip_length_to_length_ratio=0.08)
        x33 = toolbox_capture("33")
        # the toolbox's Python (laptop/32: 46, shown in block 3), under pip on "on an old Python"
        py = mono(cut(x32.line(46), "3.8.10").strip(), 20, S.GREY)
        py.move_to([-3.9, row_y - 0.5, 0])
        st4 = toolbox_term("33", rows=5)
        err1 = label_box(['for later: quote it, "ansible>=9.0.0", on a newer base image',
                          "leave it for this lecture: deploy-provision-instance.yml:57 (warn:) "
                          "needs this old Ansible"], S.GREY, size=20)
        err1.text[1].set_opacity(0)
        etag = erratum_tag()
        VGroup(etag, err1).arrange(RIGHT, buff=0.2).move_to([0, row_y, 0])
        with self.voiceover(SAY[4]) as vo:
            fade_all(self, t, chips, rec, run_time=0.5)
            self.play(FadeIn(dfp, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("the greater than sign")
            self.play(gt_g.animate.set_color(ROUTE), Circumscribe(gt_g, color=ROUTE, buff=0.06),
                      run_time=0.8)
            vo.wait_until("is a shell redirect")
            self.play(left.animate.set_color(TOOL).move_to([-3.9, row_y, 0]),
                      ver.animate.move_to([-0.4, row_y + 0.35, 0]), run_time=0.8)
            self.play(ReplacementTransform(gt_g.copy(), arr), run_time=0.6)
            self.play(FadeIn(root), FadeIn(root_t),
                      ver.animate.move_to(fname).set_color(ERR), run_time=0.9)
            self.play(FadeIn(fg, scale=0.6), run_time=0.3)
            self.remove(ver)
            self.add(fname)
            vo.wait_until("So the root folder")
            self.play(FadeIn(st4, shift=UP * 0.15), run_time=0.4)
            type_cmd(self, st4, x33.cmds[0][1], type_time=0.4)
            # the ls columns are padded for a 120-cell terminal: squeezed, then wrapped at spaces
            out(self, st4, [squeeze_spaces(s) for s in x33.at((36, 37))], wrap=True, run_time=0.6)
            red = substring(lines_of(st4, "'=9.0.0'")[0], "'=9.0.0'")
            self.play(red.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(red, color=ERR, scale_factor=1.25),
                      Indicate(VGroup(fg, fname), color=ERR, scale_factor=1.15), run_time=0.9)
            vo.wait_until("pip wrote its log")
            st4.set_prompt(x33.prompt)
            type_cmd(self, st4, x33.cmds[1][1], type_time=0.9)
            out(self, st4, x33.at(39, 40) + [cut(x33.line(42), "ansible-core-2.13.13")], wrap=True,
                run_time=0.6)
            vo.wait_until("and installed Ansible 6")
            # the installed one (the wrapped tail of "Successfully installed"), not the download row
            a67 = substring(lines_of(st4, "ansible-6.7.0")[-1], "ansible-6.7.0")
            u67 = under(a67, ERR)
            self.play(a67.animate.set_color(ERR), Create(u67), run_time=0.6)
            vo.wait_until("on an old Python")
            self.play(FadeIn(py, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(py, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Quoting fixes it")
            self.play(FadeOut(VGroup(left, py, arr, root, root_t, fg, fname), shift=UP * 0.15), run_time=0.4)
            self.remove(left, py, arr, root, root_t, fg, fname)
            self.play(FadeIn(err1.frame), FadeIn(err1.text[0]), FadeIn(etag), run_time=0.6)
            vo.wait_until("but leave it for now")
            self.play(err1.text[1].animate.set_opacity(1), run_time=0.6)
            self.play(Indicate(err1.text[1], color=INK, scale_factor=1.03), run_time=0.8)

        # ========================================================== 5. the warnings, once
        x40 = toolbox_capture("40")
        w_rows = [(cut(x40.line(36), "no longer supported"), S.GREY), (x40.line(37), S.GREY)]
        t5 = term(x40.prompt, rows=14, title=T_TOOLBOX, size=20)
        hide = grey_chip("warnings · hidden from here on", size=22).move_to([0, 0.3, 0])
        with self.voiceover(SAY[5]) as vo:
            fade_all(self, dfp, st4, u67, err1, etag, run_time=0.5)
            self.play(FadeIn(t5), run_time=0.4)
            put_heading(self, t5, "every ansible-playbook run starts with:")
            g_crypto = out(self, t5, w_rows, wrap=True, run_time=0.5)
            g_coll = out(self, t5, x40.at(38, warnings=True), wrap=True, run_time=0.4)
            g_mod = out(self, t5, x40.at((39, 41), warnings=True), wrap=True, run_time=0.6)
            vo.wait_until("the old Python")
            self.play(Indicate(g_crypto, color=INK, scale_factor=1.02), run_time=0.8)
            vo.wait_until("a collection that doesn't")
            self.play(Indicate(g_coll, color=TURN, scale_factor=1.02), run_time=0.8)
            vo.wait_until("and an old module name")
            self.play(Indicate(g_mod, color=TURN, scale_factor=1.02), run_time=0.8)
            vo.wait_until("We hide them")
            body = VGroup(*t5.lines)
            for ln in list(t5.lines):
                t5.lines.remove(ln)
            self.play(FadeTransform(body, hide), run_time=0.9)
            self.play(FadeOut(t5), run_time=0.4)
            self.remove(t5, *t5.get_family())

        # ========================================================== 6. aws sts (extra)
        x34 = toolbox_capture("34")
        t6 = toolbox_term("34", rows=6)
        t6.shift(DOWN * 0.05)          # room for the inventory tree above it (beat 7)
        badge = badge_glyph(0.6).move_to([-1.6, 1.6, 0])
        ph = grey_chip("placeholder").next_to(badge, RIGHT, buff=0.3)
        yours = dashed_chip("with your key: your account ID and your user").move_to([0, 0.75, 0])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(hide), FadeIn(t6), run_time=0.5)
            self.remove(hide)
            ln = type_cmd(self, t6, x34.cmd, type_time=0.7)
            pin(self, ln, beside(extra_row(), ln))
            vo.wait_until("the security token is invalid")
            out(self, t6, [(s, ERR) for s in x34.at(37)], wrap=True, run_time=0.6)
            self.play(Indicate(lines_of(t6, "InvalidClientTokenId")[0], color=ERR, scale_factor=1.03),
                      run_time=0.7)
            vo.wait_until("Ours is a placeholder")
            self.play(FadeIn(badge, scale=1.3), FadeIn(ph, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("With your key")
            self.play(FadeIn(yours, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 7. inventory graph, syntax check
        x35, x36 = toolbox_capture("35"), toolbox_capture("36")
        tree = InventoryTree().move_to([3.6, 1.7, 0])   # clear of the strip's title bar
        # the graph is typed before the block (a silent typing beat): its output is what the first
        # sentence talks about
        fade_all(self, badge, ph, yours, run_time=0.4)
        t6.clear(self, run_time=0.3)
        t6.set_prompt(x35.prompt)
        type_cmd(self, t6, x35.cmd, type_time=0.8)
        g = out(self, t6, x35.at((36, 41)), run_time=0.5)
        with self.voiceover(SAY[7]) as vo:
            self.play(Indicate(g[0], color=OWN, scale_factor=1.05), FadeIn(tree.all, target_position=g[0]),
                      run_time=0.7)
            vo.wait_until("then appserver")
            self.play(Indicate(g[1], color=OWN, scale_factor=1.05), Create(tree.edges[0]),
                      FadeIn(tree.group, target_position=g[1]), run_time=0.7)
            vo.wait_until("then one host")
            self.play(Indicate(g[2], color=OWN, scale_factor=1.05), Create(tree.edges[1]),
                      FadeIn(tree.leaf, target_position=g[2]), run_time=0.7)
            self.remove(tree.all, tree.group, tree.leaf, tree.edges)
            self.add(tree)
            self.play(Circumscribe(tree.leaf, color=OWN, buff=0.06), run_time=0.8)
            vo.wait_until("And all five playbooks")
            gone = VGroup(*t6.lines)
            for ln in list(t6.lines):
                t6.lines.remove(ln)
            self.play(FadeOut(tree), FadeOut(gone), run_time=0.3)
            self.remove(tree, gone, *tree.get_family(), *gone.get_family())
            resize(self, t6, 7, run_time=0.4)
            t6.set_prompt(x36.prompt)
            type_cmd(self, t6, x36.cmd, type_time=1.0)
            out(self, t6, [(s, OWN) for s in x36.at(39, 47, 51, 55, 59)], run_time=0.6)
            vo.wait_until("The toolbox is ready")
            self.play(Indicate(VGroup(*t6.lines[-5:]), color=OWN, scale_factor=1.02), run_time=0.8)
        self.play(FadeOut(t6), FadeOut(tr), run_time=0.6)
        self.remove(t6, tr, *t6.get_family(), *tr.get_family())
        self.wait(0.3)
