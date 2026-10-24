"""S08 · IAM: may this identity do this, here? (concept scene, no tracker) — AC215 L10.

Beats (script.md, ## S08; one voiceover block each; `lecture_ref(10, "26, 35, 42, 45")` top right
for the whole scene):
0. Title card 'authentication: who are you?' / 'authorization: what may you do, and where?'. On
   "Google calls this IAM" it gives way to V2 (IamGridRig): rows you / llm-service-account,
   columns your-gcp-project / ac215-project / project 129349313346. A GREY 'Owner' token drops
   into (you, your-gcp-project) with the unspoken chip 'you own the project · your code wears its
   own badge' (top left); the GREEN `roles/aiplatform.user` token drops into (SA, your project)
   and the cell flashes GREEN; the GREY 'Storage Admin' token lands beside it with a GREY note
   'granted, unused by v0'.
1. Three PINK requests. (1) embed under your column: its resource path appears as
   `projects/<GCP_PROJECT>/…`; on "writes that name" the placeholder glows and is filled in
   (`your-gcp-project`); the arrow lands, GREEN check. (2) the same embed with the unedited
   default: CODE(api-service/docker-shell.sh: 9) at the bottom, its `ac215-project` turns RED and
   a copy flies into request (2)'s path; the arrow lands, RED 403; on "edit both scripts" the
   CHANGE comment is underlined and the panel gives way to CODE(llm-rag/docker-shell.sh: 7) (the
   same line in the second script). (3) a tuned-model request under project 129349313346 with its
   path `projects/129349313346/…`: parked (no arrow yet), GREY pin 'part 2'.
2. The error ladder: two RED rungs. Lower: `DefaultCredentialsError` or `401` → 'authentication:
   no valid token', 'check: the path · the mount · the file name' (items on their words). A GREY
   'valid token' arrow climbs to the upper rung: `403` → 'authentication worked, authorization
   failed', 'causes: missing role · wrong project · API not enabled'.
3. 'API not enabled' flashes and becomes the head of a kind card, tag `erratum`: 'no README in
   this repo says to enable the Vertex AI API · probably done in an earlier lecture · if not, the
   403 says so, with an enable link'; under it a GREY chip `gcloud services enable
   aiplatform.googleapis.com` with the GREY `extra` tag.
4. The grid returns as it was; the check of (1) flashes, column 3 pulses, path (3) flashes, then
   its number, and the empty (SA, column 3) cell pulses on "whose IAM is checked"; the
   three candidates appear on their words (`GCP_PROJECT` chip, the key's `project_id` chip, the
   path). PONDER 2 (8 s) on the left, column 3 and the candidates stay visible.
5. The path rings YELLOW and column 3's head lights (the resource); the key's `project_id` greys
   ('where the badge was issued'), then `GCP_PROJECT` ('overridden by the path'); the number in
   the path flashes; arrow (3) lands in the empty (SA, project 129349313346) cell: RED 403; the
   'part 2' pin flashes. Closing picture: one GREEN badge, a BLUE Vertex AI door ('Gemini role')
   and a GREY dashed GCS bucket door ('storage role'), caption 'one badge · grants differ'. Fade
   to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer.components import ponder_card
from explainer.devops import check_mark

from common import (CLOUD, ERR, FUTURE, INK, KEY, LAPTOP, MONO, NARRATION, PASS, PROJECT_ID, ROUTE,
                    SA_EMAIL, SAY_COUNT, TURN, IamGridRig, arrow, badge, card, chip, code, code_span,
                    dashed_chip, door_glyph, each, err_chip, erratum_tag, extra_tag, flash_tag, greyed,
                    grey_chip, key_glyph, label, lref, mono, note, ring, under)
from explainer import style as S

SAY = NARRATION["S08"]
API_SHELL = "cheese-app-v0/api-service/docker-shell.sh"
RAG_SHELL = "cheese-app-v0/llm-rag/docker-shell.sh"
DEFAULT = "ac215-project"                      # quoted: docker-shell.sh's unedited default
TUNED = "129349313346"                         # quoted: rag.py:22's endpoint project
PONDER_2 = ("Your key works for embeddings. You paste the\ninstructor's endpoint projects/129349313346/….\n"
            "Which part decides whose IAM is checked:\nGCP_PROJECT, the key's project_id, or the path?")
GRID_Y = 1.0
PATH_Y = -1.85                                 # the resource-path row under the request chips
CAP_Y = -2.5                                   # captions under the candidates / the 'part 2' pin
PREFIX = "projects/"
SLOT = "<GCP_PROJECT>"


# ------------------------------------------------------------------ local pieces
def path_text(middle: str, color=INK) -> Text:
    """A request's resource path 'projects/<middle>/…' (PINK frame, the project in `color`)."""
    t = mono(PREFIX + middle + "/…", 20, ROUTE)
    assert len(t) == len(PREFIX) + len(middle) + 2, len(t)
    t[len(PREFIX):len(PREFIX) + len(middle)].set_color(color)
    t.middle = t[len(PREFIX):len(PREFIX) + len(middle)]
    return t


def req_chip(g: IamGridRig, c: int, text: str) -> VGroup:
    """A PINK request chip under column c (where IamGridRig.fire puts it), not added."""
    req = chip(text, ROUTE, size=g.size, font=MONO, fill_opacity=0.15)
    return req.move_to([g.cells[-1][c].get_center()[0], g.cells[-1][c].get_bottom()[1] - 0.5, 0])


def req_arrow(g: IamGridRig, req, r: int, c: int) -> Arrow:
    """The request's arrow up into cell (r, c): to the edge of column 0's stacked tokens, into the
    middle of an empty cell (else it is a tick under the grid; the verdict stays top-right)."""
    cell = g.cells[r][c]
    end_y = cell.get_bottom()[1] + 0.02 if c == 0 else cell.get_center()[1] + 0.05
    return Arrow(req.get_top(), [cell.get_center()[0], end_y, 0], buff=0.05,
                 color=ROUTE, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.5)


def land(scene, g: IamGridRig, r: int, c: int, ok: bool) -> VGroup:
    """Plays: the cell flashes and the verdict lands (GREEN check / RED 403). Returns the mark."""
    mark = g.verdict(r, c, ok)
    if c == 0 and ok:                  # column 0's token is as wide as the cell: a smaller check, centred
        cell = g.cells[r][c]           # in the gap between the top token and the cell's top edge
        tok_top = g.slot_point(r, c, 0, 2)[1] + 0.25
        mark = VGroup(check_mark(0.27, PASS))
        mark.move_to([cell.get_right()[0] - 0.1 - mark.width / 2, (tok_top + cell.get_top()[1]) / 2, 0])
    flash = g.cells[r][c].copy().set_stroke(PASS if ok else ERR, 5)
    scene.play(FadeIn(mark, scale=1.3), FadeIn(flash), run_time=0.45)
    scene.play(FadeOut(flash), run_time=0.3)
    scene.remove(flash)
    return mark


def fill_path(scene, old: Text, middle: str, color=INK, src=None, run_time: float = 0.8) -> Text:
    """Plays: the placeholder of `old` ('projects/<GCP_PROJECT>/…') is filled in with `middle`
    (from a copy of `src` when given: what became what). Returns the new path (on the scene)."""
    new = path_text(middle, color)
    new.move_to(old, aligned_edge=LEFT)
    n0, n1 = len(PREFIX), len(PREFIX) + len(SLOT)
    m0, m1 = len(PREFIX), len(PREFIX) + len(middle)
    pre, mid, suf = VGroup(*old[:n0]), VGroup(*old[n0:n1]), VGroup(*old[n1:])
    into = VGroup(*new[m0:m1])
    scene.remove(old)                  # its parts play on their own: no slice of `old` is left behind
    scene.add(pre, mid, suf)
    arrive = TransformFromCopy(src, into) if src is not None else FadeIn(into, shift=DOWN * 0.15)
    scene.play(FadeOut(mid, shift=UP * 0.15), arrive, Transform(suf, VGroup(*new[m1:]).copy()), run_time=run_time)
    scene.remove(pre, mid, suf, into)
    scene.add(new)
    return new


def rung(left, head: str, prefix: str, items) -> VGroup:
    """One RED rung of the error ladder: the error chip(s) left, the verdict and the GREY list
    right. .frame .left .head .items (the list's words, in order)"""
    hd = label(head, 26, INK)
    words = [label(s, 22, S.GREY) for s in items]
    row = [label(prefix, 22, S.GREY)]
    for i, w in enumerate(words):
        if i:
            row.append(label("·", 22, S.GREY))
        row.append(w)
    lst = VGroup(*row).arrange(RIGHT, buff=0.16)
    right = VGroup(hd, lst).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    to = mono("→", 30, ERR)
    body = VGroup(left, to, right).arrange(RIGHT, buff=0.4)
    frame = RoundedRectangle(width=11.8, height=body.height + 0.55, corner_radius=0.16, stroke_color=ERR,
                             stroke_width=3).set_fill(S.GREY_DARKER, 1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.4)
    g = VGroup(frame, body)
    g.frame, g.left, g.to, g.right, g.head, g.items, g.list = frame, left, to, right, hd, words, lst
    return g


def vertex_door() -> VGroup:
    """The closing picture's Vertex AI door: BLUE, 'Gemini role' (GREEN: the grant)."""
    d = door_glyph(0.6, 0.85, CLOUD)
    name = label("Vertex AI", 26, CLOUD)
    role = chip("Gemini role", PASS, size=20)
    txt = VGroup(name, role).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    g = VGroup(d, txt).arrange(RIGHT, buff=0.35)
    g.door = d
    return g


def bucket_door() -> VGroup:
    """The closing picture's bucket door: GREY dashed (L11's buckets), 'storage role'."""
    fr = Rectangle(width=0.6, height=0.85)
    d = DashedVMobject(fr, num_dashes=22, dashed_ratio=0.55).set_stroke(FUTURE, 3)
    name = label("GCS bucket", 26, S.GREY)
    role = dashed_chip("storage role")
    txt = VGroup(name, role).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    g = VGroup(d, txt).arrange(RIGHT, buff=0.35)
    g.door = d
    return g


def ponder_at(scene, question: str, seconds: float, card_w: float, center) -> VGroup:
    """pause_and_ponder, placed (left of column 3, above the candidates)."""
    pc = ponder_card(question, width=card_w).move_to(center)
    pc[0].set_fill(opacity=1)          # opaque: the grid's words must not ghost through the card
    scene.play(FadeIn(pc, scale=0.95), run_time=0.6)
    bar = pc[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return pc


class IamGrid(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 6, len(SAY)
        ref = lref("26, 35, 42, 45")

        # ========================================================== 0. who vs what-and-where; the grid
        l1 = VGroup(label("authentication:", 32, INK), label("who are you?", 32, KEY)).arrange(RIGHT, buff=0.25)
        l2 = VGroup(label("authorization:", 32, INK),
                    label("what may you do, and where?", 32, TURN)).arrange(RIGHT, buff=0.25)
        lines = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        tframe = RoundedRectangle(width=lines.width + 1.2, height=lines.height + 0.9, corner_radius=0.18,
                                  stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        tframe.move_to([0, 0.3, 0])
        lines.move_to(tframe)

        g = IamGridRig().move_to([0, GRID_Y, 0])
        owner = g.token("Owner", S.GREY, mono_font=False)
        role = g.token("roles/aiplatform.user", PASS)
        storage = g.token("Storage Admin", S.GREY, mono_font=False)
        own_chip = grey_chip("you own the project · your code wears its own badge")
        own_chip.move_to([-6.45 + own_chip.width / 2, 3.25, 0])
        unused = note("granted, unused by v0")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(tframe, scale=0.96), FadeIn(l1, shift=RIGHT * 0.2), run_time=0.9)
            vo.wait_until("Authorization decides")
            self.play(FadeIn(l2, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("and where")
            self.play(Indicate(l2[1], color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Google calls this IAM")
            self.play(FadeOut(VGroup(tframe, lines), shift=UP * 0.3), run_time=0.5)
            self.remove(tframe, lines)
            self.play(FadeIn(g, scale=1.05), run_time=0.8)
            vo.wait_until("a grid of identities")
            self.play(each(list(g.names), INK, scale=1.12, lag=0.3), run_time=0.8)
            vo.wait_until("roles")
            self.play(g.drop(owner, 0, 0), FadeIn(own_chip, shift=DOWN * 0.15))
            vo.wait_until("and resources")
            self.play(each(list(g.heads), INK, scale=1.1, lag=0.25), run_time=0.9)
            vo.wait_until("Your service account holds")
            self.play(Indicate(g.names[1], color=KEY, scale_factor=1.1), run_time=0.6)
            self.play(g.drop(role, 1, 0, slot=0, of=2))
            vo.wait_until("and that green cell does the work")
            hot = g.cells[1][0].copy().set_stroke(PASS, 6)
            self.play(FadeIn(hot), run_time=0.4)
            self.play(FadeOut(hot), Indicate(role.text, color=PASS, scale_factor=1.08), run_time=0.7)
            self.remove(hot)
            vo.wait_until("Storage Admin sits beside it")
            self.play(g.drop(storage, 1, 0, slot=1, of=2))
            vo.wait_until("granted but never used")
            unused.next_to(g.cells[1][0], DOWN, buff=0.25)
            self.play(FadeIn(unused, shift=UP * 0.15), Indicate(storage.text, color=S.GREY, scale_factor=1.08),
                      run_time=0.7)

        # ========================================================== 1. three requests, three cells
        req1, req2, req3 = req_chip(g, 0, "embed"), req_chip(g, 1, "embed"), req_chip(g, 2, "tuned model")
        p1 = path_text(SLOT, TURN)
        p1.move_to([req1.get_center()[0], PATH_Y, 0])
        p2 = path_text(SLOT, TURN)
        p2.move_to([req2.get_center()[0], PATH_Y, 0])
        p3 = path_text(TUNED)
        p3.move_to([6.4 - p3.width / 2, PATH_Y, 0])
        pin3 = grey_chip("part 2")
        pin3.move_to([6.4 - pin3.width / 2, CAP_Y, 0])
        panel = code(API_SHELL, 9).move_to([0, -3.5 + 0.64, 0])
        panel2 = code(RAG_SHELL, 7).move_to(panel)
        default_glyphs = code_span(panel.code, 0, DEFAULT)
        change = code_span(panel.code, 0, "CHANGE TO YOUR PROJECT ID")
        change2 = code_span(panel2.code, 0, "CHANGE TO YOUR PROJECT ID")
        default2 = code_span(panel2.code, 0, DEFAULT)
        default2.set_color(ERR)

        with self.voiceover(SAY[1]) as vo:
            sa_cells = [g.cells[1][c].copy().set_stroke(TURN, 5) for c in range(3)]
            self.play(LaggedStart(*[FadeIn(x, rate_func=there_and_back) for x in sa_cells], lag_ratio=0.5),
                      run_time=1.4)
            self.remove(*sa_cells)
            vo.wait_until("IAM checks the resource")
            self.play(FadeOut(VGroup(own_chip, unused)), run_time=0.4)
            self.remove(own_chip, unused)
            self.play(FadeIn(req1, shift=UP * 0.2), run_time=0.4)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the client writes that name")
            self.play(Indicate(p1.middle, color=TURN, scale_factor=1.15), run_time=0.7)
            p1 = fill_path(self, p1, PROJECT_ID)
            vo.wait_until("An embedding in your own project")
            a1 = req_arrow(g, req1, 1, 0)
            self.play(Create(a1), Indicate(g.heads[0], color=INK, scale_factor=1.1), run_time=0.8)
            mark1 = land(self, g, 1, 0, True)
            vo.wait_until("The same call")
            self.play(FadeOut(p1), FadeIn(panel, shift=UP * 0.2), FadeIn(req2, shift=UP * 0.2), run_time=0.6)
            self.remove(p1)
            self.play(FadeIn(p2, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("unedited default project")
            self.play(default_glyphs.animate.set_color(ERR), Indicate(p2.middle, color=TURN, scale_factor=1.1),
                      run_time=0.6)
            p2 = fill_path(self, p2, DEFAULT, ERR, src=default_glyphs)
            vo.wait_until("is refused with a 403")
            a2 = req_arrow(g, req2, 1, 1)
            self.play(Create(a2), run_time=0.6)
            mark2 = land(self, g, 1, 1, False)
            vo.wait_until("because your account has no role there")
            empty = g.cells[1][1].copy().set_stroke(ERR, 5)
            self.play(FadeIn(empty, rate_func=there_and_back), Indicate(g.heads[1], color=ERR, scale_factor=1.1),
                      run_time=0.9)
            self.remove(empty)
            vo.wait_until("That is why you edit both scripts")
            u1 = under(change, TURN)
            self.play(Create(u1), run_time=0.5)
            u2 = under(change2, TURN)
            self.play(FadeOut(VGroup(panel, u1), shift=LEFT * 0.4), FadeIn(VGroup(panel2, u2), shift=LEFT * 0.4),
                      run_time=0.8)
            self.remove(panel, u1)
            vo.wait_until("The third arrow")
            self.play(FadeOut(VGroup(panel2, u2, p2)), FadeIn(req3, shift=UP * 0.2), run_time=0.6)
            self.remove(panel2, u2, p2)
            self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("waits for part 2")
            self.play(FadeIn(pin3, shift=LEFT * 0.15), run_time=0.5)

        grid_all = VGroup(g, owner, role, storage, req1, a1, mark1, req2, a2, mark2, req3, p3, pin3)

        # ========================================================== 2. the error ladder
        low = rung(VGroup(err_chip("DefaultCredentialsError"),
                          VGroup(label("or", 22, S.GREY), err_chip("401")).arrange(RIGHT, buff=0.15)
                          ).arrange(DOWN, buff=0.18),
                   "authentication: no valid token", "check:", ("the path", "the mount", "the file name"))
        up = rung(err_chip("403", size=26), "authentication worked, authorization failed", "causes:",
                  ("missing role", "wrong project", "API not enabled"))
        low.move_to([0, -1.75, 0])
        up.move_to([0, 1.05, 0])
        up.left.move_to([low.left.get_center()[0], up.left.get_center()[1], 0])     # one column of errors
        up.to.next_to(up.left, RIGHT, buff=0.4)
        up.right.next_to(up.to, RIGHT, buff=0.4)
        rails = VGroup(*[Line([x, -3.3, 0], [x, 2.6, 0], color=S.GREY, stroke_width=4) for x in (-6.15, 6.15)])
        climb = arrow(low.frame.get_top() + LEFT * 3.2, up.frame.get_bottom() + LEFT * 3.2, S.GREY, buff=0.08)
        climb_txt = note("valid token").next_to(climb, RIGHT, buff=0.2)
        ladder_cap = note("the error ladder").move_to([-5.9, 3.25, 0], aligned_edge=LEFT)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(grid_all), run_time=0.6)
            self.remove(grid_all)
            self.play(Create(rails), FadeIn(ladder_cap), run_time=0.6)
            self.play(FadeIn(low.frame), FadeIn(low.left, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("means no valid token")
            self.play(FadeIn(low.to, shift=RIGHT * 0.15), FadeIn(low.head, shift=RIGHT * 0.2), run_time=0.6)
            for w, anchor in zip(low.items, ("check the path", "the mount", "and the file name")):
                vo.wait_until(anchor)
                rest = [low.list[0]] if w is low.items[0] else [low.list[low.list.submobjects.index(w) - 1]]
                self.play(FadeIn(VGroup(*rest, w), shift=UP * 0.1), run_time=0.4)
                self.play(w.animate.set_color(INK), run_time=0.3)
            vo.wait_until("A 403 means")
            self.play(GrowArrow(climb), FadeIn(climb_txt), run_time=0.6)
            self.play(FadeIn(up.frame), FadeIn(up.left, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("authentication worked")
            self.play(FadeIn(up.to, shift=RIGHT * 0.15), FadeIn(up.head, shift=RIGHT * 0.2), run_time=0.6)
            for w, anchor in zip(up.items, ("a missing role", "the wrong project", "or an API that")):
                vo.wait_until(anchor)
                rest = [up.list[0]] if w is up.items[0] else [up.list[up.list.submobjects.index(w) - 1]]
                self.play(FadeIn(VGroup(*rest, w), shift=UP * 0.1), run_time=0.4)
                self.play(w.animate.set_color(INK), run_time=0.3)

        ladder = VGroup(rails, ladder_cap, low, up, climb, climb_txt)

        # ========================================================== 3. a small gap: enabling the API
        api = up.items[2]
        crd = card(["no README in this repo says to enable the Vertex AI API",
                    "probably done in an earlier lecture",
                    "if not, the 403 says so, with an enable link"], head="API not enabled", size=24)
        crd.move_to([0, 0.75, 0])
        err_t = erratum_tag().next_to(crd.frame, UP, buff=0.12).align_to(crd.frame, RIGHT)
        cmd = grey_chip("gcloud services enable aiplatform.googleapis.com", mono_font=True)
        x_t = extra_tag()
        fix = VGroup(cmd, x_t).arrange(RIGHT, buff=0.3).next_to(crd.frame, DOWN, buff=0.45)

        with self.voiceover(SAY[3]) as vo:
            self.play(Indicate(api, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("no README here says")
            head_from = api.copy()
            self.remove(api)
            up.list.remove(api)
            self.play(FadeOut(ladder), ReplacementTransform(head_from, crd.head), FadeIn(crd.frame),
                      FadeIn(err_t, shift=LEFT * 0.15), run_time=0.8)
            self.remove(ladder)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in crd.body], lag_ratio=0.5), run_time=1.2)
            self.add(crd)
            vo.wait_until("If you never did")
            self.play(Indicate(crd.body[2], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("one extra gcloud command")
            self.play(FadeIn(cmd, shift=UP * 0.15), FadeIn(x_t, shift=LEFT * 0.15), run_time=0.6)
            flash_tag(self, x_t, S.GREY)

        # ========================================================== 4. the grid returns; ponder 2
        c_var = grey_chip("GCP_PROJECT", mono_font=True)
        k_g = key_glyph(0.6)
        c_key0 = grey_chip("project_id", mono_font=True, color=KEY)
        c_key = VGroup(k_g, c_key0).arrange(RIGHT, buff=0.15)
        c_var.move_to([-4.7, PATH_Y, 0])
        c_key.move_to([-1.3, PATH_Y, 0])
        cap_var = note("overridden by the path").next_to(c_var, DOWN, buff=0.22)
        cap_key = note("where the badge was issued").next_to(c_key, DOWN, buff=0.22)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(crd, err_t, fix)), run_time=0.5)
            self.remove(crd, err_t, fix)
            self.play(FadeIn(grid_all), run_time=0.8)
            vo.wait_until("Your key works for embeddings")
            self.play(Indicate(mark1, color=PASS, scale_factor=1.3), Indicate(req1.text, color=ROUTE), run_time=0.8)
            vo.wait_until("Now you paste")
            self.play(g.pulse_col(2))
            vo.wait_until("which begins with projects")
            self.play(Indicate(p3, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("and a long number")
            self.play(Indicate(p3.middle, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("whose IAM is checked")
            target = g.cells[1][2].copy().set_stroke(TURN, 5)
            self.play(FadeIn(target, rate_func=there_and_back), run_time=0.9)
            self.remove(target)
            vo.wait_until("the project variable")
            self.play(FadeIn(c_var, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the project inside your key")
            self.play(FadeIn(c_key, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("or the endpoint path")
            self.play(Indicate(p3, color=TURN, scale_factor=1.08), run_time=0.7)
        pc = ponder_at(self, PONDER_2, 8, 9.8, [-1.62, 1.0, 0])

        # ========================================================== 5. the path decides; one badge
        p_ring = ring(p3, TURN, buff=0.1)
        num = p3.middle
        a3 = req_arrow(g, req3, 1, 2)
        bdg = badge(SA_EMAIL).move_to([0, 1.55, 0])
        vd = vertex_door().move_to([-4.6, -0.75, 0], aligned_edge=LEFT)
        bd = bucket_door().move_to([1.4, -0.75, 0], aligned_edge=LEFT)
        b0 = bdg.frame.get_bottom()
        ar_v = arrow(b0 + LEFT * 1.2 + DOWN * 0.1, vd.door.get_top() + UP * 0.12, INK)
        ar_b = DashedLine(b0 + RIGHT * 1.2 + DOWN * 0.1, bd.door.get_top() + UP * 0.12, color=S.GREY,
                          stroke_width=3, dash_length=0.12)
        ar_b.add_tip(tip_length=0.18, tip_width=0.18)
        moral = label("one badge · grants differ", 30, INK).move_to([0, -2.6, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.5)
            self.remove(pc)
            self.play(Create(p_ring), Indicate(g.heads[2], color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Not the key's project")
            self.play(Transform(c_key, greyed(c_key)), run_time=0.6)
            vo.wait_until("where the badge was issued")
            self.play(FadeIn(cap_key, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Not the variable")
            self.play(Transform(c_var, greyed(c_var)), FadeIn(cap_var, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and that name wins")
            self.play(Indicate(num, color=TURN, scale_factor=1.15), Indicate(g.heads[2], color=TURN, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("It is someone else's project")
            self.play(Create(a3), run_time=0.7)
            vo.wait_until("so it is a 403")
            mark3 = land(self, g, 1, 2, False)
            vo.wait_until("part 2 draws it")
            flash_tag(self, pin3, S.GREY)

        # silent closing picture, kept short (~4 s) and moving until the last 0.8 s
        self.play(FadeOut(VGroup(grid_all, a3, mark3, p_ring, c_var, c_key, cap_var, cap_key)), run_time=0.45)
        self.remove(grid_all, a3, mark3, p_ring, c_var, c_key, cap_var, cap_key)
        self.play(FadeIn(bdg, scale=1.1), run_time=0.5)
        self.play(LaggedStart(AnimationGroup(GrowArrow(ar_v), FadeIn(vd, shift=LEFT * 0.2)),
                              AnimationGroup(Create(ar_b), FadeIn(bd, shift=LEFT * 0.2)), lag_ratio=0.5),
                  run_time=1.1)
        self.play(FadeIn(moral, shift=UP * 0.15), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.remove(*self.mobjects)
