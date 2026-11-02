"""S02 · What a run records (the lecture's experiment-tracking checklist; task.py's four W&B calls).
Lecture: 9–13, 15.

Beats (script.md "## S02", one voiceover block each):
 0  LECTURE 9–10. The question "What should a run record hold?"; seven GREY column headers write
    in a row as named (our redrawing of slide 9): Environment, Code, Data, Model, Metrics,
    Artifacts, Notes.
 1  The headers move up; slide 10's table as four rows that snap into homes (each item grows out
    of its header): code → GitHub, data → data versioning, environment → pyproject.toml · uv.lock,
    each with a GREEN tick; the fourth row "weights · metrics · logs" (out of Model, Metrics,
    Artifacts) hangs on a YELLOW "?".
 2  Data-version aside. The table compacts upward, the data row lights, the other rows dim. The
    data row expands into the pair: the "data versioning" home becomes the GREEN "version record",
    the BLUE "snapshot" bucket joins it, the PINK "content hash" link draws and pulses. Then the
    pair gives way to CODE(task.py: 96–100) (wrapped) with line 97's URL lit, and a GREY note
    "a fixed release · not in config".
 3  LECTURE 11–13. The aside folds away (panel, note, the three rows with homes); the "?" row is
    caught by a BLUE ledger (V1, illustration) that slides in from the right: the row drops into
    the ledger's empty row place. GREY chip "W&B · hosted · MLflow if you must self-host".
 4  LECTURE 15. The ledger moves to the top; CODE(task.py: 152–153) at the bottom right; a GOLD
    key glyph flies from a GREY `--wandb_key` flag chip into the GOLD lock on the ledger's edge;
    on "never written in the code" `args.wandb_key` is underlined GOLD. No value anywhere.
 5  The login panel transforms into CODE(task.py: 312–322) (20 pt); the ledger's frame folds
    away around its row place. On "opens" a BLUE row slides in (name mobilenetv2_train_base_True);
    line 314 (project) and 321 (name) light as named; lines 316–319 light GREEN one by one as the
    four config chips clip on. On "active run" the outline turns YELLOW; the PINK `wandb.run`
    pointer appears and swings onto the row.
 6  The panel transforms into CODE(task.py: 335–338). "After training": the system tile and its
    traces draw. Line 336 lights: the `execution_time` chip clips on. Line 338 lights: padlock +
    "finished", outline GREY, the pointer drops into its `None` slot.
 7  Panel and pointer leave; the sealed row moves to the centre and enlarges; GREEN ticks on the
    config chips and the system tile; the history strip gets the RED dashed "empty" outline;
    GREY caption "the run records: config + system metrics · not: loss".
 8  Takeaway (YELLOW, centred): "If the question says record of a run, think: init opens it, a
    logger writes the metrics, finish closes it."
 9  The takeaway fades; PONDER card 1 (mcq_card, centred). After the block the timer drains
    (10 s, silent); the card fades to an empty frame (the answer opens S03).

Deviations from SHOW: beat 5 sets CODE(312–322) at 20 pt (11 rows at 22 pt do not fit beside the
full ledger row) and the ledger's frame and header fold away once the row lands (the full row,
9.0 wide, and the 7.2-wide panel cannot share a frame width; the project is read off line 314).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    ReplacementTransform,
    VGroup,
    Transform,
    VMobject,
    Write,
    linear,
)

from common import *  # noqa: F401,F403
from common import guard
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources
TASK = "package/trainer/task.py"
assert "cheese_4_labels.zip" in source_line(TASK, 97), source_line(TASK, 97)
assert source_line(TASK, 153).strip() == "wandb.login(key=args.wandb_key)", source_line(TASK, 153)
assert source_line(TASK, 313).strip() == "wandb.init(", source_line(TASK, 313)
assert source_line(TASK, 314).strip() == 'project="cheese-training-vertex-ai",', source_line(TASK, 314)
assert [source_line(TASK, n).strip().split(":")[0] for n in range(316, 320)] == \
    ['"learning_rate"', '"epochs"', '"batch_size"', '"model_name"']
assert source_line(TASK, 321).strip() == "name=model.name,", source_line(TASK, 321)
assert "execution_time" in source_line(TASK, 336), source_line(TASK, 336)
assert source_line(TASK, 338).strip() == "wandb.run.finish()", source_line(TASK, 338)
assert "wandb" not in excerpt(TASK, 96, 100)

HEADERS = ["Environment", "Code", "Data", "Model", "Metrics", "Artifacts", "Notes"]
SAFE = 6.6


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


def inside(m, t: float = 3.6):
    guard(m.get_left()[0] >= -SAFE and m.get_right()[0] <= SAFE and m.get_bottom()[1] >= -3.6
          and m.get_top()[1] <= t, f"outside the frame: {m.get_left()} {m.get_right()} {m.get_bottom()} {m.get_top()}")


def dimmed(m, k: float, base=None):
    """A copy of m (or of base) with every member's fill and stroke opacity times k."""
    t = (base if base is not None else m).copy()
    for f in t.get_family():
        if isinstance(f, VMobject):
            f.set_fill(opacity=f.get_fill_opacity() * k, family=False)
            f.set_stroke(opacity=f.get_stroke_opacity() * k, family=False)
    return t


def flash(mob, color=TURN, k: float = 1.12, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def table_row(item: str, home: str | None, home_font=None):
    """One row of slide 10's table: item chip → home chip + GREEN tick, or → YELLOW '?'."""
    it = chip(item, S.GREY, size=24)
    ar = label("→", 26, S.GREY)
    if home is None:
        hm = label("?", 34, TURN, weight="BOLD")
        mk = None
    else:
        hm = chip(home, S.GREY, size=24, font=home_font)
        mk = tick_mark(0.32)
    g = VGroup(it, ar, hm) if mk is None else VGroup(it, ar, hm, mk)
    g.item, g.arrow, g.home, g.mark = it, ar, hm, mk
    return g


def lay_row(r, y: float, item_right: float = -2.4):
    place(r.item, right=item_right, cy=y)
    place(r.arrow, left=item_right + 0.2, cy=y)
    place(r.home, left=r.arrow.get_right()[0] + 0.2, cy=y)
    if r.mark is not None:
        place(r.mark, left=r.home.get_right()[0] + 0.25, cy=y)
    return r


class RunRecord(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · seven things a run record holds
        q = label("What should a run record hold?", 32, INK)
        place(q, cx=0, cy=1.3)
        heads = VGroup(*[chip(h, S.GREY, size=24) for h in HEADERS]).arrange(RIGHT, buff=0.22)
        place(heads, cx=0, cy=0.0)
        inside(heads)
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "9–10")
            self.play(Write(q), run_time=1.0)
            vo.wait_until("The lecture lists")
            self.play(q.animate.set_color(S.GREY), run_time=0.4)
            for k, word in enumerate(("the environment", "the code", "the data", "the model", "the metrics",
                                      "the artifacts", "and your notes")):
                vo.wait_until(word)
                self.play(FadeIn(heads[k], shift=DOWN * 0.2), run_time=0.4)
            self.play(LaggedStart(*[flash(h, INK, 1.06, 0.4) for h in heads], lag_ratio=0.1), run_time=1.0)

        # ========================================================== 1 · slide 10: four rows, three homes
        rows = [table_row("code", "GitHub"), table_row("data", "data versioning"),
                table_row("environment", "pyproject.toml · uv.lock", MONO),
                table_row("weights · metrics · logs", None)]
        ys1 = [1.5, 0.6, -0.3, -1.2]
        for r, y in zip(rows, ys1):
            lay_row(r, y)
            inside(r)
        src = {0: [heads[1]], 1: [heads[2]], 2: [heads[0]], 3: [heads[3], heads[4], heads[5]]}
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(q), heads.animate.set_y(2.7), run_time=0.8)
            for k, word in ((0, "Code lives in GitHub"), (1, "data in a versioning system"),
                            (2, "and the environment in"), (3, "Weights, metrics and logs")):
                vo.wait_until(word)
                r = rows[k]
                self.play(ReplacementTransform(VGroup(*[h.copy() for h in src[k]]), r.item),
                          *[Transform(h, dimmed(h, 0.45)) for h in src[k]], run_time=0.6)
                self.play(FadeIn(r.arrow), FadeIn(r.home, shift=LEFT * 0.4), run_time=0.5)
                if r.mark is not None:
                    self.play(Create(r.mark), run_time=0.35)
                else:
                    self.play(flash(r.home, TURN, 1.4, 0.7))
        table = VGroup(*rows)

        # ========================================================== 2 · data-version aside
        ys2 = [2.65, 1.95, 1.25, 0.55]
        targets = [lay_row(r.copy(), y) for r, y in zip(rows, ys2)]
        dv = DataVersion()
        place(dv, cx=0, cy=-0.95)
        inside(dv)
        snap, rec = dv.parts["snapshot"], dv.parts["record"]
        pnl96 = src_panel(TASK, 96, 100, wrap=True)
        place(pnl96, cx=0, top=-0.4)
        inside(pnl96)
        url_bar = pnl96.bar(97, TURN, 0.22)
        fixed = note("a fixed release · not in config", size=24)
        place(fixed, right=6.4, cy=ys2[3])
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(heads), *[r.animate.become(t) for r, t in zip(rows, targets)], run_time=0.8)
            guard(fixed.get_left()[0] > rows[3].home.get_right()[0] + 0.8, "note runs into the ? row")
            guard(table.get_bottom()[1] > dv.get_top()[1] + 0.2, "table runs into the data pair")
            for r in rows:
                r.save_state()
            self.play(*[Transform(r, dimmed(r, 0.3)) for k, r in enumerate(rows) if k != 1],
                      rows[1].item.box.animate.set_stroke(TURN, 3), run_time=0.5)
            vo.wait_until("A data version is a pair")
            self.play(ReplacementTransform(rows[1].home.copy(), rec), run_time=0.8)
            vo.wait_until("the archived snapshot")
            self.play(FadeIn(snap, shift=RIGHT * 0.3), run_time=0.6)
            self.remove(rec, snap)
            self.add(dv)
            vo.wait_until("and the version record")
            self.play(flash(rec, OWN, 1.08, 0.6))
            vo.wait_until("linked by a content hash")
            dv.reveal(self, "link", run_time=0.6)
            self.play(dv.flash())
            vo.wait_until("This trainer instead")
            self.play(FadeOut(dv), FadeIn(pnl96, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(url_bar), run_time=0.5)
            vo.wait_until("and never writes it")
            self.play(FadeIn(fixed, shift=LEFT * 0.2), run_time=0.5)
            self.play(flash(fixed, S.GREY, 1.08))

        # ========================================================== 3 · the ledger catches the "?" row
        led = Ledger(slots=1, full=True)
        place(led, cx=0, cy=0.2)
        inside(led)
        host = grey_tag("W&B · hosted · MLflow if you must self-host")
        place(host, cx=0, top=led.get_bottom()[1] - 0.3)
        inside(host)
        slot0 = led.slot(0)
        qrow = rows[3]
        with self.voiceover(SAY[3]) as vo:
            lr = lref_swap(self, lr, "11–13")
            self.play(FadeOut(VGroup(pnl96, url_bar, fixed)), FadeOut(VGroup(*rows[:3])), run_time=0.6)
            self.play(Transform(qrow, qrow.saved_state.copy().move_to([0, 2.3, 0])), run_time=0.7)
            vo.wait_until("so the lecture automates")
            self.play(FadeIn(led, shift=LEFT * 3.0), run_time=1.0)
            self.play(Transform(qrow, dimmed(qrow, 0.55).move_to(slot0)), run_time=0.8)
            self.play(flash(led.parts["places"], TURN, 1.02, 0.6))
            vo.wait_until("Picture a ledger")
            self.play(FadeIn(host, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("is one row")
            self.play(led.parts["places"].animate.set_stroke(CLOUD, 3), run_time=0.5)

        # ========================================================== 4 · login with a key passed as a flag
        shift4 = np.array([-1.75 - led.get_center()[0], 3.5 - led.get_top()[1], 0])
        lock = padlock(0.45, KEY)
        pnl152 = src_panel(TASK, 152, 153)
        place(pnl152, right=6.4, top=-1.0)
        inside(pnl152)
        flag = chip("--wandb_key", S.GREY, size=CAPTION, font=MONO)
        place(flag, cx=-4.2, cy=pnl152.get_center()[1] - 0.2)
        key = key_glyph(0.36)
        place(key, cx=flag.get_center()[0], bottom=flag.get_top()[1] + 0.15)
        with self.voiceover(SAY[4]) as vo:
            lr = lref_swap(self, lr, "15")
            self.play(FadeOut(host), VGroup(led, qrow).animate.shift(shift4), run_time=0.8)
            place(lock, cx=led.get_center()[0] + 1.6, cy=led.get_bottom()[1])
            inside(led)
            self.play(FadeIn(pnl152, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("talks to that ledger")
            self.play(flash(led.parts["frame"], CLOUD, 1.02, 0.7), FadeIn(lock, scale=0.8), run_time=0.7)
            vo.wait_until("First it logs in")
            b153 = pnl152.bar(153, TURN, 0.2)
            self.play(FadeIn(b153), FadeIn(flag, shift=RIGHT * 0.2), FadeIn(key),
                      run_time=0.6)
            self.play(key.animate.next_to(lock, LEFT, buff=0.05), run_time=1.0)
            self.play(flash(lock, KEY, 1.25), run_time=0.6)
            vo.wait_until("never written in the code")
            ul = under(pnl152.span(153, "args.wandb_key"), KEY)
            self.play(Create(ul), flash(flag, KEY, 1.1), run_time=0.7)

        # ========================================================== 5 · init opens the row, sets the pointer
        places = led.parts["places"]
        up5 = 0.8
        pnl312 = src_panel(TASK, 312, 322, size=20)
        place(pnl312, right=6.5, top=1.0)
        inside(pnl312)
        row = LedgerRow(RUN_NAME, width=led.row_w, full=True)
        row.move_to(places.get_center() + UP * up5)
        inside(row, t=3.55)
        guard(row.get_bottom()[1] > pnl312.get_top()[1] + 0.1, "row runs into the init panel")
        rtag = illustration_tag()
        place(rtag, left=row.get_right()[0] + 0.2, top=row.get_top()[1] - 0.6)
        inside(rtag)
        ptr = RunPointer(tail=np.array([-4.2, 0.4, 0]), none_at=np.array([-5.0, -0.6, 0]))
        inside(ptr)
        tgt = np.array([-3.6, row.get_bottom()[1], 0])
        guard(ptr.none_slot.get_bottom()[1] > -3.6, "None slot")
        with self.voiceover(SAY[5]) as vo:
            led_chrome = led.parts_out("frame", "head", "tag")
            self.play(*led_chrome, FadeOut(VGroup(lock, key, ul, flag, b153)),
                      places.animate.shift(UP * up5), qrow.animate.shift(UP * up5),
                      ReplacementTransform(pnl152, pnl312), run_time=1.0)
            vo.wait_until("opens a new row")
            self.play(FadeIn(row, shift=LEFT * 0.6), FadeOut(qrow), *led.parts_out("places"),
                      FadeIn(rtag), run_time=0.8)
            vo.wait_until("with a project")
            b314 = pnl312.bar(314, TURN, 0.22)
            self.play(FadeIn(b314), run_time=0.5)
            vo.wait_until("a name")
            b321 = pnl312.bar(321, TURN, 0.22)
            self.play(FadeOut(b314), FadeIn(b321), flash(row.name_text, TURN, 1.06), run_time=0.5)
            vo.wait_until("and a config")
            self.play(FadeOut(b321), run_time=0.3)
            cfg_bars = VGroup()
            for n, key_, word in zip(range(316, 320), CONFIG_KEYS,
                                     ("learning rate", "epochs", "batch size", "and model name")):
                vo.wait_until(word)
                b = pnl312.bar(n, OWN, 0.22)
                cfg_bars.add(b)
                self.play(FadeIn(b), *row.clip(key_), run_time=0.4)
            vo.wait_until("It also makes that row")
            b313 = pnl312.bar(313, TURN, 0.22)
            self.play(*row.activate(), FadeIn(b313), run_time=0.6)
            vo.wait_until("and the pointer called")
            self.play(FadeIn(ptr), run_time=0.5)
            self.play(*ptr.point_to(tgt), run_time=0.8)

        # ========================================================== 6 · execution time, then finish seals
        pnl335 = src_panel(TASK, 335, 338)
        place(pnl335, right=6.5, top=-1.2)
        inside(pnl335)
        guard(pnl335.get_left()[0] > ptr.none_slot.get_right()[0] + 0.2
              or pnl335.get_top()[1] < ptr.none_slot.get_bottom()[1] - 0.2, "panel 335 runs into None")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(cfg_bars, b313)), ReplacementTransform(pnl312, pnl335), run_time=0.9)
            vo.wait_until("After training")
            row.reveal(self, "system", run_time=0.5)
            row.reveal(self, "traces", anim=Create, run_time=1.2)
            vo.wait_until("the execution time")
            b336 = pnl335.bar(336, OWN, 0.22)
            self.play(FadeIn(b336), *row.clip(EXEC_KEY), run_time=0.6)
            vo.wait_until("Then wandb dot run dot finish")
            b338 = pnl335.bar(338, TURN, 0.22)
            self.play(FadeIn(b338), run_time=0.4)
            self.play(*row.seal(), *row.parts_in("finished"), run_time=0.8)
            vo.wait_until("and the pointer falls back")
            self.play(*ptr.to_none(), run_time=0.8)

        # ========================================================== 7 · what the run recorded on its own
        cap = note("the run records: config + system metrics · not: loss", size=24)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(ptr, rtag, pnl335, b336, b338)), run_time=0.6)
            self.remove(led)
            self.play(row.animate.rescale(1.12).move_to([0, 0.6, 0]), run_time=0.9)
            inside(row)
            place(cap, cx=0, top=row.get_bottom()[1] - 0.4)
            inside(cap)
            fr = row.frame
            last_chip = row.parts[f"cfg:{EXEC_KEY}"]
            t_cfg = tick_mark(0.34)
            place(t_cfg, left=last_chip.get_right()[0] + 0.3, cy=last_chip.get_center()[1])
            tile = row.parts["system"][0]
            t_sys = tick_mark(0.3)
            place(t_sys, right=tile.get_right()[0] - 0.1, top=tile.get_top()[1] - 0.08)
            guard(fr.get_left()[0] >= -SAFE, "row")
            vo.wait_until("the config, and system charts")
            self.play(Create(t_cfg), run_time=0.4)
            self.play(Create(t_sys), flash(row.parts["traces"], OWN, 1.05), run_time=0.6)
            vo.wait_until("It did not record a loss")
            row.reveal(self, "empty", run_time=0.6)
            self.play(flash(row.parts["empty"], ERR, 1.04), run_time=0.6)
            vo.wait_until("Something still has to")
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)
        self.wait(0.6)

        # ========================================================== 8 · takeaway
        tk = takeaway("If the question says record of a run, think: init opens it, a logger writes the "
                      "metrics, finish closes it.")
        inside(tk)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(row, t_cfg, t_sys, cap)), FadeOut(lr), run_time=0.6)
            lr = None
            self.play(Write(tk), run_time=1.6)
            vo.wait_until("a logger writes")
            self.play(flash(tk, TURN, 1.04, 0.8))

        # ========================================================== 9 · PONDER 1
        card = mcq_card(["`init(config=…)` → `fit` → `finish`. The run shows config, no loss curve.",
                         "Which change adds a loss curve?"],
                        ["`name=…` in `wandb.init`",
                         '`wandb.config.update({"loss": …})` after fit',
                         "`WandbMetricsLogger()` in fit's `callbacks`",
                         "`wandb.login()` again before fit"])
        inside(card)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(tk), run_time=0.5)
            self.play(FadeIn(card, scale=0.95), run_time=0.6)
            vo.wait_until("The run shows its config")
            self.play(flash(card.question[0], INK, 1.03, 0.7))
            vo.wait_until("Which change puts")
            self.play(flash(card.question[1], TURN, 1.04, 0.7))
            vo.wait_until("Three options")
            self.play(LaggedStart(*[flash(o.text, INK, 1.04, 0.5) for o in card.options], lag_ratio=0.3),
                      run_time=1.4)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=10.0)
        self.play(FadeOut(card), run_time=0.6)
        self.wait(0.3)
