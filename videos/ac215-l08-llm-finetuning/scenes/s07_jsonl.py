"""S07 · Rows to JSONL, then upload (README "Dataset › Prepare" step 2 and "Dataset › Upload").
Lecture: 5, then 8 (the tag shows in beats 0-1 as slide 5, in beat 4 as slide 8).

Beats (script.md "## S07", one voiceover block each):
 0  LECTURE 5. TRACKER DsPrep 2. V4 conveyor along the bottom, station 1 (the GREEN CSV-row card
    `question,answer`) on the left. Above it CODE(dataset-creator/cli.py: 240–247, 20 pt); lines 242
    and 245 light. A copy of the CSV card rides to station 2 and becomes the GREEN text card
    `human: …` / `bot: …`; the code panel gives way to PANEL(dataset-creator/13: 3, 4 cut after
    "large wheels.", folded at a word boundary), header `train.csv`, tags scripted · extra, with the
    GREY tag "for autotrain-runner · track A doesn't use it"; the panel leaves and the station-2 card
    dims.
 1  CODE(dataset-creator/cli.py: 251–257, 20 pt). Station 3 builds above the belt: a copy of the CSV
    card unfolds into nested boxes `contents` → `role: user` / `role: model` → `parts` → `text`
    (legends on the borders), each lit with its code line; `question` drops into the user turn,
    `answer` into the model turn.
 2  TRACKER DsPrep 2 · extra. The conveyor and the code leave. PANEL(dataset-creator/12: 3–8, …,
    13–16), header `head -1 data/train.jsonl | python -m json.tool`, tags scripted · extra; the keys
    contents / role / parts / text light YELLOW. It turns in place into the README's example
    (expected/readme-prepare-gemini-format: 4–9, …, 14–17) as a GREY quote card headed
    `README.md · lines 191–212`, tag expected: the lit keys move to their places, only the rest
    changes; caption "same nesting". Then the card collapses into the single real line
    PANEL(dataset-creator/11: 2 cut after "Glad you ask!", folded to fit), header `head -c 400
    data/train.jsonl`: the seven lit keys fly into it; caption "one example per line"; on "the L in
    JSONL" the l of `train.jsonl` lights YELLOW, "= JSON lines".
 3  The panel leaves; CODE(dataset-creator/cli.py: 259–273 folded to 260–264, 267, 270–273, 20 pt):
    260–262 light, `test_size=0.1` and `random_state=42` YELLOW. On "17 examples" the code gives way
    to V4's splitter: 19 GREEN row bricks gather at the fork (GREY seed chip random_state=42), 17 go
    to `train.jsonl · 17`, 2 to `test.jsonl · 2`; a 3-row TEAL container strip (tags scripted ·
    extra) types `ls -la data; wc -l data/*.jsonl data/*.csv` -> dataset-creator/10 lines 10–14
    (names+sizes), 15–17; `2 data/test.jsonl` and `17 data/train.jsonl` light. On "The code's
    comment" CODE(cli.py: 266–267) at the top with the GREY cap "≤ 256 · per the comment on line
    266" beside line 267; the test bin flashes.
 4  LECTURE 8. The splitter and the strip leave; the single JSONL line returns at the top and its
    model turn lights YELLOW; under it token boxes "Glad" "you" "ask" "!" "…" (tag illustration)
    fill one at a time while a YELLOW arrow slides under them: "predict the next token". The tag
    leaves at the end of the idea.
 5  Second laptop terminal (13 rows, `laptop · second terminal`, tag extra): `ls -la data; git -C ..
    status --short --ignored` -> laptop/15 lines 5–14 (names+sizes), 15; the files turn GREY,
    line 15 `!! dataset-creator/data/` GREEN with the GREY note "ignored · .gitignore lines 8–9";
    the PINK mount chip `dataset-creator/ → /app` in the top band pulses.
 6  TRACKER DsUp 1. Full-width TEAL container terminal (tags no key · billed): `python cli.py
    --upload` -> dataset-creator/14 lines 2–3, …, 9–10, …, 36 (RED, wrapped); "was not found."
    flashes. The terminal shrinks to a strip; V2's stage above it: the PINK route to the bucket pin
    stops at the container wall with a RED "no key" stamp. Then the stage gives way to a GREY
    dashed "with your key, look for" card: excerpt chip cli.py line 293 `print("Uploading file:",
    data_file, destination_blob_name)`, "× 5 files · then check your bucket", and a RED chip
    "403? → your bucket in env.dev · both roles · API enabled".
 7  The card and the strip leave. Erratum: excerpt chip cli.py line 280 `bucket =
    storage_client.bucket(GCS_BUCKET_NAME)`, GREY note "assumes the bucket exists", GREEN fix
    "create it first (the card in Prerequisites)", GREY card "changed env.dev? `exit`, then `sh
    docker-shell.sh` again: it is read at start (docker-shell.sh lines 8, 19–21)". Then the "your
    turn" card: `python cli.py --upload`, GOLD "storage: cents". 2 s hold; empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _header_text, _mixed_row, _mono_rows
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real captures and sources
CLI = "dataset-creator/cli.py"
CSVH = capture("dataset-creator/13")
assert CSVH.cmd.startswith("head -4 data/train.csv"), CSVH.cmd
assert CSVH.line(3) == '"human: What makes Comte different from Gruyere?', CSVH.line(3)
assert CSVH.line(4).startswith("bot: Glad you ask!"), CSVH.line(4)
PRETTY = capture("dataset-creator/12")
assert PRETTY.cmd == "head -1 data/train.jsonl | python -m json.tool", PRETTY.cmd
GEMQ = capture("expected/readme-prepare-gemini-format")
ONE = capture("dataset-creator/11")
assert ONE.cmd.startswith("head -c 400 data/train.jsonl"), ONE.cmd
LSD = capture("dataset-creator/10")
assert LSD.cmd == "ls -la data; wc -l data/*.jsonl data/*.csv", LSD.cmd
assert LSD.line(15).split() == ["2", "data/test.jsonl"] and LSD.line(16).split() == ["17", "data/train.jsonl"]
HOSTD = capture("laptop/15")
assert HOSTD.cmd == "ls -la data; git -C .. status --short --ignored", HOSTD.cmd
assert HOSTD.line(15) == "!! dataset-creator/data/", HOSTD.line(15)
UPL = capture("dataset-creator/14")
assert UPL.cmd == "python cli.py --upload" and UPL.exit == 1, (UPL.cmd, UPL.exit)
assert "DefaultCredentialsError" in UPL.line(36) and "was not found." in UPL.line(36)
assert "line 279, in upload" in UPL.line(9) and "storage.Client()" in UPL.line(10)
L266, L267, L280, L293 = (source_line(CLI, n) for n in (266, 267, 280, 293))
assert "256" in L266 and L267.strip() == "df_test = df_test[:256]", (L266, L267)
assert "test_size=0.1, random_state=42" in source_line(CLI, 261)
GI = source_text(".gitignore").split("\n") if (SOURCE / ".gitignore").exists() else []
assert GI[7] == GI[8] == "/dataset-creator/data/*", GI[:10]
DSH = source_text("dataset-creator/docker-shell.sh").split("\n")
assert DSH[7] == "source ../env.dev" and "GCS_BUCKET_NAME" in DSH[20], DSH

# the pretty-printed line (3-8, 13-16) and the README's example (4-9, 14-17): the same 11 rows
PRETTY_ROWS = PRETTY.at((3, 8), "…", (13, 16))
QUOTE_ROWS = GEMQ.at((4, 9), "…", (14, 17))
KEYS = ['"contents"', '"role"', '"parts"', '"text"']
ONE_LINE = ONE.cut(2, "Glad you ask!")
TOKENS = ["Glad", "you", "ask", "!"]

# ------------------------------------------------------------------ layout
TOP_Y = 2.87                     # top of a full-width panel (just under the tracker)
BELT_Y = -2.74                   # the conveyor belt (labels under it, cards above it)
PANEL_W = TERM_W


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def glow(frame, color: str = TURN):
    """A bright outline runs once around a card's frame (Indicate would tint its dark fill)."""
    from manim import ShowPassingFlash
    return ShowPassingFlash(frame.copy().set_fill(opacity=0).set_stroke(color, 7), time_width=0.6)


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def mono_panel(lines, header: str, quote: bool = False, width: float = PANEL_W) -> VGroup:
    """PANEL (dark, like log_panel) or, quote=True, the GREY README quote card, from the same mono
    rows at the same place (so one turns into the other in place). .frame .rows .header"""
    max_chars = int((width - 0.5) / cell_width(CAPTION))
    rows = _mono_rows(lines, CAPTION, OUTPUT, max_chars)
    h = rows.height + 0.4
    if quote:
        frame = box(width, h, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.15)
    else:
        frame = RoundedRectangle(width=width, height=h, corner_radius=0.15, stroke_color=S.GREY_DARK,
                                 stroke_width=2).set_fill(PANEL, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.25)
    head = _header_text(header).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.12)
    g = VGroup(frame, rows, head)
    g.frame, g.rows, g.header = frame, rows, head
    g.move_to([0, 0, 0])
    return g


def key_glyphs(rows) -> list:
    """[(row index, glyphs)] of every quoted key (contents / role / parts / text), in reading order."""
    out = []
    for i, r in enumerate(rows):
        pos = 0
        while True:
            found = [(r.text.find(k, pos), k) for k in KEYS if r.text.find(k, pos) >= 0]
            if not found:
                break
            j, k = min(found)
            out.append((i, glyph_range(r, j, j + len(k))))
            pos = j + len(k)
    return out


def rest_of(rows, keys) -> VGroup:
    """Every glyph of `rows` that is not one of the key glyphs."""
    ks = {id(g) for _, kg in keys for g in kg}
    return VGroup(*[g for r in rows for g in r.glyphs if id(g) not in ks])


def legend_box(text: str, w: float, h: float, color: str, mono_: bool = True) -> VGroup:
    """A box with its name sitting on the top border (a fieldset legend). .frame .legend"""
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.1, stroke=2.5)
    t = mono(text, CAPTION, color) if mono_ else label(text, CAPTION, color)
    bg = RoundedRectangle(width=t.width + 0.16, height=t.height + 0.06, corner_radius=0.04,
                          stroke_width=0).set_fill(S.BG, 1)
    lg = VGroup(bg, t).move_to(fr.get_corner(UP + LEFT) + np.array([0.18 + t.width / 2 + 0.08, 0, 0]))
    g = VGroup(fr, lg)
    g.frame, g.legend = fr, lg
    return g


def seat(inner, outer, pad: float = 0.1):
    """Move the legend box `inner` so its frame sits centred in x on outer's frame, `pad` above
    outer's bottom edge (the legends then have the room above)."""
    f, o = inner.frame, outer.frame
    inner.shift(np.array([o.get_center()[0] - f.get_center()[0], o.get_bottom()[1] + pad - f.get_bottom()[1], 0]))
    return inner


def nested_card() -> VGroup:
    """V4 station 3: contents → role: user / role: model → parts → text (question / answer)."""
    turns = VGroup()
    for role, field, col in (("role: user", "question", OWN), ("role: model", "answer", OWN)):
        txt = mono(field, CAPTION, INK)
        tb = legend_box("text", 1.62, 0.66, INK)
        pb = legend_box("parts", 1.9, 1.12, INK)
        rb = legend_box(role, 2.3, 1.58, col)
        seat(pb, rb)
        seat(tb, pb)
        txt.move_to(tb.frame).shift(DOWN * 0.07)        # below the "text" legend
        g = VGroup(rb, pb, tb, txt)
        g.role, g.parts, g.text, g.field = rb, pb, tb, txt
        turns.add(g)
    turns.arrange(RIGHT, buff=0.16)
    cb = legend_box("contents", turns.width + 0.36, 1.58 + 0.46, OWN)
    turns.shift(np.array([cb.frame.get_center()[0] - turns.get_center()[0],
                          cb.frame.get_bottom()[1] + 0.1 - turns[0].role.frame.get_bottom()[1], 0]))
    card = VGroup(cb, turns)
    card.contents, card.turns = cb, turns
    return card


def dim(card) -> list:
    """Animations that dim a shape card (frame, tint and rows), keeping its dark fill."""
    return [card.frame.animate.set_stroke(opacity=0.35), card[1].animate.set_fill(opacity=0.02),
            *[r.glyphs.animate.set_opacity(0.35) for r in card.rows]]


def fold_rows(s: str, width: int) -> list[str]:
    return [r for r, *_ in wrap_output(s, width)]


class RowsToJsonl(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0 · station 1 -> station 2 (train.csv)
        lr = lref("5")
        tr = tracker("DsPrep", 2)
        cv = Conveyor(STATIONS[:3])
        cv.shift(UP * (BELT_Y - cv.belt.get_center()[1]))
        csv = shape_card(["question,answer"], OWN)
        cv.put(0, csv)
        LIFT = 2.0                      # the belt starts higher and slides down when the code comes
        for k in (1, 2):
            cv.labels[k].set_opacity(0.35)
        p0 = src_panel(CLI, 240, 247, size=20)
        place(p0, cx=0, top=TOP_Y)
        assert p0.get_bottom()[1] > csv.get_top()[1] + 0.15, (p0.get_bottom(), csv.get_top())
        card2 = shape_card(["human: …", "bot: …"], OWN)
        cv.put(1, card2)
        csv_rows = [CSVH.line(3), *fold_rows(CSVH.cut(4, "large wheels."), 72)]
        pan2 = mono_panel(csv_rows, "train.csv")
        tags2 = VGroup(scripted_tag(), extra_tag()).arrange(RIGHT, buff=0.15)
        place(pan2, cx=0, cy=0.9)
        tags2.next_to(pan2.header, RIGHT, buff=0.35)
        auto = grey_tag("for autotrain-runner · track A doesn't use it")
        auto.next_to(pan2.frame, DOWN, buff=0.18).align_to(pan2.frame, RIGHT)
        assert auto.get_bottom()[1] > card2.get_top()[1] + 0.1, (auto.get_bottom(), card2.get_top())
        with self.voiceover(SAY[0]) as vo:
            VGroup(cv, csv).shift(UP * LIFT)
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(lr), run_time=0.6)
            self.play(FadeIn(cv), FadeIn(csv, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Follow one pair")
            self.play(glow(csv.frame, OWN), cv.light(0), run_time=0.8)
            vo.wait_until("It starts as a CSV row")
            self.play(flash(csv.rows, TURN, 1.12), run_time=0.7)
            vo.wait_until("glue it into")
            self.play(VGroup(cv, csv).animate.shift(DOWN * LIFT), run_time=0.6)
            self.play(FadeIn(p0, shift=UP * 0.15), run_time=0.6)
            b242, b245 = p0.bar(242, TURN), p0.bar(245, TURN)
            self.play(FadeIn(b242), p0.span(242, '"human: "').animate.set_color(TURN), run_time=0.4)
            self.play(FadeIn(b245), p0.span(245, '"bot: "').animate.set_color(TURN), run_time=0.4)
            vo.wait_until("with human and bot")
            ride = csv.copy()
            self.add(ride)
            self.play(ride.animate.move_to(card2), cv.labels[1].animate.set_opacity(1), run_time=0.8)
            self.play(FadeOut(ride.rows), run_time=0.25)
            self.play(Transform(ride.frame, card2.frame), Transform(ride[1], card2[1]), cv.light(1), run_time=0.4)
            self.remove(ride, ride.frame, ride[1], ride.rows)
            self.add(card2.frame, card2[1])
            self.play(FadeIn(card2.rows), run_time=0.3)
            self.remove(card2.frame, card2[1], card2.rows)
            self.add(card2)
            vo.wait_until("the text column")
            self.play(FadeOut(VGroup(p0, b242, b245)), run_time=0.4)
            self.play(TransformFromCopy(card2, pan2.frame), FadeIn(pan2.rows), FadeIn(pan2.header),
                      FadeIn(tags2), run_time=0.7)
            hb = VGroup(substring(pan2.rows[0], "human:"), substring(pan2.rows[1], "bot:"))
            self.play(hb.animate.set_color(TURN), FadeIn(auto, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Track A doesn't")
            self.play(flash(auto, S.GREY, 1.08), run_time=0.6)
            self.play(FadeOut(VGroup(pan2, tags2, auto), shift=DOWN * 0.2),
                      *dim(card2), cv.labels[1].animate.set_color(S.GREY).set_opacity(0.6),
                      cv.marks[1].animate.set_color(INK), run_time=0.7)

        # ========================================================== 1 · station 3: Gemini's contents
        p1 = src_panel(CLI, 251, 257, size=20)
        place(p1, cx=0, top=TOP_Y)
        nest = nested_card()
        cv.put(2, nest, buff=0.2)
        assert p1.get_bottom()[1] > nest.get_top()[1] + 0.1, (p1.get_bottom(), nest.get_top())
        assert nest.get_right()[0] < 6.55 and nest.get_left()[0] > card2.get_right()[0] + 0.1
        u, m = nest.turns
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(p1, shift=UP * 0.15), cv.labels[2].animate.set_opacity(1), run_time=0.6)
            ride = csv.copy()
            self.add(ride)
            self.play(ride.animate.move_to(nest.contents.frame), cv.light(2), run_time=0.9)
            vo.wait_until("a list called contents")
            b251 = p1.bar(251, TURN)
            self.play(FadeOut(ride.rows), run_time=0.2)
            self.play(Transform(ride.frame, nest.contents.frame), FadeOut(ride[1]), FadeIn(nest.contents.legend),
                      FadeIn(b251),
                      p1.span(251, '"contents"').animate.set_color(TURN), run_time=0.6)
            self.remove(ride, ride.frame, ride[1], ride.rows)
            self.add(nest.contents)
            vo.wait_until("with a user turn")
            b253 = p1.bar(253, TURN)
            self.play(FadeIn(u.role, shift=DOWN * 0.1), FadeIn(b253), run_time=0.5)
            vo.wait_until("and a model turn")
            b254 = p1.bar(254, TURN)
            self.play(FadeIn(m.role, shift=DOWN * 0.1), FadeIn(b254), run_time=0.5)
            vo.wait_until("each holding parts")
            spans = VGroup(p1.span(253, '"parts"'), p1.span(254, '"parts"'))
            self.play(FadeIn(u.parts), FadeIn(m.parts), spans.animate.set_color(TURN), run_time=0.5)
            spans2 = VGroup(p1.span(253, '"text"'), p1.span(254, '"text"'))
            self.play(FadeIn(u.text), FadeIn(m.text), spans2.animate.set_color(TURN), run_time=0.5)
            q_src = p1.span(253, 'row["question"]')
            a_src = p1.span(254, 'row["answer"]')
            self.play(TransformFromCopy(q_src, u.field), run_time=0.6)
            self.play(TransformFromCopy(a_src, m.field), run_time=0.6)

        # ========================================================== 2 · the real train.jsonl, the README's example, one line
        pp = mono_panel(PRETTY_ROWS, PRETTY.cmd)
        qq = mono_panel(QUOTE_ROWS, expected_where("expected/readme-prepare-gemini-format"), quote=True)
        for g in (pp, qq):
            place(g, cx=0, top=TOP_Y - 0.05)
        assert pp.get_bottom()[1] > -3.0, pp.get_bottom()
        tags_p = VGroup(scripted_tag(), extra_tag()).arrange(RIGHT, buff=0.15).next_to(pp.header, RIGHT, buff=0.35)
        tag_q = expected_tag().next_to(qq.header, RIGHT, buff=0.35)
        kp, kq = key_glyphs(pp.rows), key_glyphs(qq.rows)
        assert [len(g) for _, g in kp] == [len(g) for _, g in kq] and len(kp) == 7, (len(kp), len(kq))
        cap_same = note("same nesting", TURN, 26)
        place(cap_same, cx=0, top=qq.get_bottom()[1] - 0.25)
        one_rows = fold_rows(ONE_LINE, 72)
        assert len(one_rows) == 2, one_rows
        oo = mono_panel(one_rows, ONE.cmd.split(";")[0])
        place(oo, cx=0, cy=1.2)
        tags_o = VGroup(scripted_tag(), extra_tag()).arrange(RIGHT, buff=0.15).next_to(oo.header, RIGHT, buff=0.35)
        ko = key_glyphs(oo.rows)
        assert len(ko) == 7, len(ko)
        cap_one = VGroup(note("one example per line", TURN, 26), note("(one line, folded here to fit)"))
        cap_one.arrange(DOWN, buff=0.12)
        place(cap_one, cx=0, top=oo.get_bottom()[1] - 0.35)
        jl = mono("train.jsonl", 34, OWN)
        jl_eq = label("= JSON lines", 34, INK)
        jg = VGroup(jl, jl_eq).arrange(RIGHT, buff=0.35)
        place(jg, cx=0, top=cap_one.get_bottom()[1] - 0.45)
        assert jg.get_bottom()[1] > -3.4, jg.get_bottom()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p1, b251, b253, b254, cv, csv, card2, nest)), caption_extra(tr), run_time=0.7)
            self.play(FadeIn(pp.frame), FadeIn(pp.header), FadeIn(tags_p),
                      LaggedStart(*[FadeIn(r) for r in pp.rows], lag_ratio=0.05), run_time=0.8)
            self.play(*[g.animate.set_color(TURN) for _, g in kp], run_time=0.5)
            vo.wait_until("the same nesting")
            for _, g in kq:
                g.set_color(TURN)
            self.play(Transform(pp.frame, qq.frame), FadeOut(pp.header), FadeOut(tags_p),
                      FadeOut(rest_of(pp.rows, kp)), run_time=0.5)
            self.play(*[ReplacementTransform(a, b) for (_, a), (_, b) in zip(kp, kq)],
                      FadeIn(qq.header), FadeIn(tag_q), run_time=0.8)
            self.play(FadeIn(rest_of(qq.rows, kq)), FadeIn(cap_same, shift=UP * 0.1), run_time=0.6)
            self.remove(pp.frame)
            self.add(qq.frame)
            self.bring_to_back(qq.frame)
            vo.wait_until("but each example")
            for _, g in ko:
                g.set_color(TURN)
            self.play(FadeOut(rest_of(qq.rows, kq)), FadeOut(cap_same), FadeOut(qq.header), FadeOut(tag_q),
                      run_time=0.4)
            self.play(Transform(qq.frame, oo.frame),
                      *[ReplacementTransform(a, b) for (_, a), (_, b) in zip(kq, ko)], run_time=1.0)
            self.play(FadeIn(rest_of(oo.rows, ko)), FadeIn(oo.header), FadeIn(tags_o), run_time=0.5)
            self.remove(qq.frame)
            self.add(oo.frame)
            self.bring_to_back(oo.frame)
            self.play(FadeIn(cap_one, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("That's the L")
            self.play(FadeIn(jg, shift=UP * 0.1), run_time=0.5)
            lit = jl[-1].copy().set_color(TURN)            # the l of jsonl, lit (drawn over it)
            jg.add(lit)
            self.play(FadeIn(lit), text_tail(jl_eq, "lines").animate.set_color(TURN), run_time=0.4)
            self.play(flash(VGroup(lit, text_tail(jl_eq, "l")), TURN, 1.4), run_time=0.6)
        one_on_screen = VGroup(oo.frame, oo.rows, oo.header, tags_o)

        # ========================================================== 3 · train_test_split: 17 / 2, the 256 cap
        p3 = src_panel(CLI, [(260, 262), 267, (270, 271)], size=20,
                       wrap={270: ["as json_file"], 271: ["lines=True"]})   # 263-264, 272-273 left out: 14 rows
        place(p3, cx=0, top=TOP_Y)
        assert p3.get_bottom()[1] > -3.5, p3.get_bottom()
        sp = splitter(17, 2)
        sp[3].next_to(sp.fork[0], UP, buff=0.2)
        sp.shift(np.array([-1.5, -0.25, 0]) - sp.input_point())
        bricks = VGroup(*[RoundedRectangle(width=0.44, height=0.28, corner_radius=0.04, stroke_color=OWN,
                                           stroke_width=2).set_fill(OWN, 0.35) for _ in range(19)])
        bricks.arrange_in_grid(rows=4, cols=5, buff=0.1)
        place(bricks, left=-5.6, cy=sp.input_point()[1])
        n19 = note("19 rows").next_to(bricks, UP, buff=0.15)
        seed = chip("random_state=42", S.GREY, size=CAPTION, font=MONO)
        seed.next_to(sp.fork[0], DOWN, buff=0.55).shift(LEFT * 0.62)    # clear of the test arrow and the bricks
        seed_lab = VGroup(seed)
        t3 = term(P_CTR_DC, rows=3, container="dc")
        tags3 = frame_tags(t3, scripted_tag(), extra_tag())
        p266 = src_panel(CLI, 266, 267, size=20)
        place(p266, cx=0, top=TOP_Y - 0.1)
        cap256 = note("≤ 256 · per the comment on line 266")
        r267 = p266.code.code_lines[p266.rows_of(267)[0]]
        cap256.next_to(r267, RIGHT, buff=0.6)
        assert cap256.get_right()[0] < p266.get_right()[0] - 0.1, (cap256.get_right(), p266.get_right())
        assert p266.get_bottom()[1] > sp.get_top()[1] + 0.1, (p266.get_bottom(), sp.get_top())
        assert seed.get_bottom()[1] > STRIP_TOP + 0.05, seed.get_bottom()
        assert sp.get_right()[0] < 6.4, sp.get_right()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(one_on_screen, cap_one, jg)), caption_extra(tr, on=False), run_time=0.6)
            self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("holds out")
            bars = VGroup(*[p3.bar(n, TURN) for n in (260, 261, 262)])
            self.play(FadeIn(bars), p3.span(261, "test_size=0.1").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("with a fixed seed")
            self.play(p3.span(261, "random_state=42").animate.set_color(TURN), run_time=0.4)
            self.play(flash(p3.span(261, "random_state=42"), TURN, 1.1), run_time=0.5)
            vo.wait_until("examples for training")
            self.play(FadeOut(VGroup(p3, bars)), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in bricks], lag_ratio=0.04), FadeIn(n19),
                      FadeIn(sp), FadeIn(seed_lab), run_time=0.8)
            ip = sp.input_point()
            tgt_tr = sp.bins[0].get_left() + LEFT * 0.05
            tgt_te = sp.bins[1].get_left() + LEFT * 0.05
            order = list(range(19))
            test_ids = {4, 13}
            self.play(LaggedStart(*[b.animate.move_to(ip) for b in bricks], lag_ratio=0.05),
                      FadeOut(n19), run_time=1.0)
            self.play(LaggedStart(*[bricks[i].animate.move_to(tgt_te if i in test_ids else tgt_tr).set_opacity(0)
                                    for i in order], lag_ratio=0.05), run_time=1.1)
            self.remove(bricks)
            self.play(flash(sp.bins[0], OWN, 1.1), flash(sp.bins[1], OWN, 1.15), run_time=0.6)
            # the extra check in the container: ls + wc
            self.play(FadeIn(t3, shift=UP * 0.2), FadeIn(tags3, shift=UP * 0.2), caption_extra(tr), run_time=0.5)
            bare_prompt(self, t3)
            type_cmd(self, t3, LSD.cmd, 0.6)
            show(self, t3, LSD, *LSD.names_sizes((10, 12)), run_time=0.3)
            show(self, t3, LSD, *LSD.names_sizes((13, 14)), run_time=0.3)
            rows = show(self, t3, LSD, (15, 17), run_time=0.35)
            r15, r16 = rows[0], rows[1]
            self.play(substring(r15, "2 data/test.jsonl").animate.set_color(TURN),
                      substring(r16, "17 data/train.jsonl").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("The code's comment")
            self.play(FadeIn(p266, shift=DOWN * 0.15), run_time=0.6)
            b266 = p266.bar(266, TURN)
            self.play(FadeIn(b266), run_time=0.4)
            vo.wait_until("hence the cap")
            self.play(FadeIn(cap256, shift=LEFT * 0.1), p266.span(267, "[:256]").animate.set_color(TURN),
                      flash(sp.bins[1], TURN, 1.15), run_time=0.7)

        # ========================================================== 4 · LECTURE 8: still next-token prediction
        o4 = mono_panel(one_rows, ONE.cmd.split(";")[0])
        place(o4, cx=0, cy=1.9)
        toks = VGroup(*[chip(s, S.GREY, size=26, font=MONO) for s in TOKENS + ["…"]]).arrange(RIGHT, buff=0.22)
        toks.move_to([0, -0.35, 0])
        for c in toks:
            c.box.set_stroke(S.GREY, opacity=0.6)
            c.text.set_opacity(0)
        ill = illustration_tag().next_to(toks, RIGHT, buff=0.35)
        arr = Arrow(UP * 0.0, UP * 0.55, buff=0, color=TURN, stroke_width=5, tip_length=0.2,
                    max_tip_length_to_length_ratio=0.5)
        arr.next_to(toks[0], DOWN, buff=0.12)
        cap4 = note("predict the next token", TURN, 28).move_to([0, -1.75, 0])
        assert ill.get_right()[0] < 6.5, ill.get_right()
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(sp, seed_lab, p266, b266, cap256, t3, tags3)), caption_extra(tr, on=False),
                      run_time=0.6)
            lr = lref_swap(self, lr, "8")
            self.play(FadeIn(o4), run_time=0.5)
            mg = model_glyphs(o4.rows)
            self.play(mg.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("training is still")
            self.play(FadeIn(toks), FadeIn(ill), GrowArrow(arr), FadeIn(cap4, shift=UP * 0.1), run_time=0.6)
            for k in range(len(TOKENS)):
                self.play(arr.animate.next_to(toks[k], DOWN, buff=0.12), run_time=0.35)
                self.play(toks[k].text.animate.set_opacity(1), toks[k].box.animate.set_stroke(TURN, opacity=1),
                          run_time=0.3)
                self.play(toks[k].box.animate.set_stroke(OWN, opacity=1), run_time=0.15)
            vo.wait_until("now on the instructor")
            self.play(arr.animate.next_to(toks[-1], DOWN, buff=0.12), toks[-1].text.animate.set_opacity(1),
                      run_time=0.4)
            self.play(flash(mg, TURN, 1.04), run_time=0.6)
        self.play(FadeOut(VGroup(o4, toks, ill, arr, cap4, lr)), run_time=0.6)

        # ========================================================== 5 · from the laptop: data/ left in the clone, ignored
        t5 = term(P_DC, rows=13, title=SECOND)
        tags5 = frame_tags(t5, extra_tag())
        mnt = VGroup(mono("dataset-creator/", CAPTION, LAPTOP),
                     Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=LOOKUP, stroke_width=4, tip_length=0.16),
                     mono("/app", CAPTION, CTR), note("bind mount", LOOKUP)).arrange(RIGHT, buff=0.18)
        place(mnt, right=6.45, cy=2.84)
        assert mnt.get_bottom()[1] > t5.box.get_top()[1] + 0.03 and mnt.get_left()[0] > -1.9, mnt.get_corner(DOWN + LEFT)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(t5, shift=UP * 0.2), FadeIn(tags5, shift=UP * 0.2), caption_extra(tr), run_time=0.6)
            bare_prompt(self, t5)
            type_cmd(self, t5, HOSTD.cmd, 0.7)
            files = show(self, t5, HOSTD, *HOSTD.names_sizes((5, 14)), run_time=0.6)
            vo.wait_until("the bind mount")
            self.play(FadeIn(mnt, shift=DOWN * 0.1), files.animate.set_color(LAPTOP), run_time=0.6)
            self.play(flash(mnt[1], LOOKUP, 1.3), run_time=0.6)
            vo.wait_until("Git status shows")
            r15 = show(self, t5, HOSTD, 15, run_time=0.4)[0]
            self.play(r15.animate.set_color(OWN), run_time=0.4)
            gi = note("ignored · .gitignore lines 8–9")
            beside(gi, t5, r15, buff=0.5)
            pin(self, r15, gi, run_time=0.4)
            vo.wait_until("so it stays out")
            self.play(flash(r15, OWN, 1.06), run_time=0.6)

        # ========================================================== 6 · upload: the no-key failure, what to look for
        t6 = term(P_CTR_DC, rows=10, container="dc")
        tags6 = frame_tags(t6, nokey_tag(), billed_tag())
        stg = Stage(show=())
        blk = stg.blocked("--upload")
        ghost = DashedLine_route(stg)
        look = look_card()
        place(look, cx=0, top=2.55)
        e403 = chip("403? → your bucket in env.dev · both roles · API enabled", ERR, size=CAPTION)
        place(e403, cx=0, top=look.get_bottom()[1] - 0.25)
        assert e403.get_bottom()[1] > STRIP_TOP + 0.05, e403.get_bottom()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t5, tags5, mnt)), run_time=0.5)
            tr = switch_section(self, tr, "DsUp", 1)
            self.play(FadeIn(t6, shift=UP * 0.2), FadeIn(tags6, shift=UP * 0.2), run_time=0.5)
            bare_prompt(self, t6)
            cmd6 = type_cmd(self, t6, UPL.cmd, 0.6)
            vo.wait_until("This time it fails")
            show(self, t6, UPL, 2, 3, "…", 9, 10, "…", run_time=0.6)
            r36 = t6.print(self, [(UPL.line(36), ERR)], wrap=True, run_time=0.4)
            assert len(r36) == 2, [r.text for r in r36]
            vo.wait_until("with a default credentials")
            self.play(flash(wrapped_glyphs(r36, "DefaultCredentialsError"), ERR, 1.08), run_time=0.6)
            # the strip and the stage come while the error is still being read, so the stage
            # (and its no-key stamp) stays up through "file not found" and "With a key"
            resize(self, t6, 3, keep=[cmd6, *r36], run_time=0.6,
                   extra=[tags6.animate.set_y(STRIP_TOP - t6.bar_h / 2)])
            self.add(stg)
            self.play(*stg.parts_in("laptop", "key", "dc", "mounts_dc", "cloud", "pin_global", "pin_bucket",
                                    "pin_tune", "pin_us"), run_time=0.6)
            self.play(Create(ghost), run_time=0.6)
            vo.wait_until("file not found")
            nf = wrapped_glyphs(r36, "was not found.")
            self.play(Create(blk.stub), flash(nf, ERR, 1.12), run_time=0.5)
            self.play(FadeIn(blk.stamp, scale=1.3), run_time=0.4)
            self.play(flash(blk.stamp, ERR, 1.15), run_time=0.6)
            vo.wait_until("With a key")
            self.play(flash(stg.pins["pin_bucket"], CLOUD, 1.12), run_time=0.7)
            vo.wait_until("Look for one line")
            self.play(FadeOut(VGroup(stg, ghost, blk)), run_time=0.5)
            self.play(FadeIn(look.frame), FadeIn(look.title), run_time=0.4)
            self.play(FadeIn(look.items[0], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("five in all")
            self.play(FadeIn(look.items[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("then find them")
            self.play(FadeIn(e403, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 7 · erratum: create the bucket; env.dev is read at start; your turn
        err = erratum_tag()
        e280 = excerpt_chip("bucket = storage_client.bucket(GCS_BUCKET_NAME)", f"{CLI} · line 280 (excerpt)", line=L280)
        n280 = note("assumes the bucket exists")
        top7 = VGroup(e280, n280).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        place(top7, cx=0, top=2.6)
        err.next_to(e280.header, RIGHT, buff=0.3)
        fix = fix_chip("create it first (the card in Prerequisites)")
        place(fix, left=e280.get_left()[0], top=top7.get_bottom()[1] - 0.3)
        env = card_rows([_mixed_row(["changed env.dev?", "`exit`", ", then", "`sh docker-shell.sh`", "again:"]),
                         _mixed_row(["it is read at start:", "`docker-shell.sh`", "lines 8, 19–21"])])
        place(env, left=e280.get_left()[0], top=fix.get_bottom()[1] - 0.3)
        tc = turn_card([UPL.cmd, (Prose("storage: cents"), COST)])
        place(tc, cx=0, top=env.get_bottom()[1] - 0.6)
        stack7 = VGroup(top7, err, fix, env, tc)
        stack7.shift(UP * (0.0 - stack7.get_center()[1]))
        assert stack7.get_top()[1] < 2.85, stack7.get_top()
        assert tc.get_bottom()[1] > -3.5 and top7.get_right()[0] < 6.5, (tc.get_bottom(), top7.get_right())
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(look, e403, t6, tags6)), run_time=0.4)
            self.play(FadeIn(e280, shift=UP * 0.1), FadeIn(err), run_time=0.4)
            vo.wait_until("and upload assumes")
            self.play(FadeIn(n280, shift=LEFT * 0.1), flash(e280.text, TURN, 1.05), run_time=0.6)
            vo.wait_until("Make it first")
            self.play(FadeIn(fix, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("If you just changed")
            self.play(FadeIn(env, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Then pause")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.5)
            self.play(flash(tc.tag, TURN, 1.1), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(top7, err, fix, env, tc, tr)), run_time=0.8)
        self.wait(0.3)


def text_tail(t, word: str) -> VGroup:
    """The glyphs of the last occurrence of `word` in a Text (Text keeps no glyphs for spaces)."""
    s = t.text.replace(" ", "")
    i = s.rfind(word.replace(" ", ""))
    assert i >= 0 and len(t.submobjects) == len(s), (word, t.text)
    if word == "l":                       # the l of "lines"
        i = s.rfind("lines")
    return VGroup(*t.submobjects[i:i + len(word.replace(" ", ""))])


def model_glyphs(rows) -> VGroup:
    """The glyphs of the model turn `{"role":"model","parts":[{"text":"Glad you ask!` across the rows."""
    out = VGroup()
    started = False
    for r in rows:
        j = 0
        if not started:
            j = r.text.find('{"role":"model"')
            if j < 0:
                continue
            started = True
        end = r.text.find(" …")
        out.add(*glyph_range(r, j, end if end >= 0 else None))
    assert started and len(out), "model turn not found"
    return out


def DashedLine_route(stg) -> VGroup:
    """The route --upload would take with a key: a GREY dashed path from the container wall to the
    bucket pin (the real PINK route stops at the wall)."""
    from manim import DashedVMobject
    a = stg.route("--upload")
    d = DashedVMobject(a, num_dashes=14, dashed_ratio=0.55).set_stroke(S.GREY, 3.5, opacity=0.9)
    return d


def look_card() -> VGroup:
    """The GREY dashed "with your key, look for" card (no output panel): the excerpt chip of
    cli.py line 293 and "× 5 files · then check your bucket". .frame .title .items"""
    e293 = excerpt_chip('print("Uploading file:", data_file, destination_blob_name)',
                        f"{CLI} · line 293 (excerpt)", line=L293)
    five = label("× 5 files · then check your bucket", CAPTION, INK)
    items = VGroup(e293, five).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    ttl = label("with your key, look for", CAPTION, S.GREY)
    body = VGroup(ttl, items).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    fr = box(body.width + 0.7, body.height + 0.55, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14, dashed=True)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.title, g.items = fr, ttl, items
    return g
