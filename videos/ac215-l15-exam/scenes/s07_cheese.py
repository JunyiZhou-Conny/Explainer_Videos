"""S07 · The Cheese App pipeline, and the same DAG on AWS (V6, slide 37's zig-zag).
Lecture: 34–37, 39–40.

Beats (script.md "## S07", one voiceover block each):
 0  LECTURE 37. V6 (TwoClouds, lifted 0.25): slide 37's zig-zag redrawn, four WHITE nodes "Data
    Collector", "Data Processor", "Model Training", "Model Deploy" on the BLUE Vertex region, GREY
    dotted connections (their kind is told in beat 2); each node fills YELLOW, then gets its GREEN ✓.
 1  LECTURE 34. Bottom band: CODE(ml-workflow/src/workflow/cli.py: 190–203) folded to 190–193, …,
    202–203 (7 rows: the collector's @dsl.container_component, line 193 image=DATA_COLLECTOR_IMAGE
    lit) and the excerpt chip `cli.py · line 27 (excerpt)` "dlops/cheese-app-data-collector"; the
    collector and processor turn TEAL with a TEAL chip "image from Docker Hub"; a GREY note
    "slide 34: Artifact Registry · repo: Docker Hub · any registry Vertex can reach". Then the band
    becomes a README card (ml-workflow/README.md lines 73, 76, 78, excerpts): 73 lights at "cannot
    see your laptop", 78 at "Training and deploy", and the PURPLE chip "Python + Vertex AI SDK"
    lands above the training/deploy pair.
 2  Tag out, chips out, nodes back to pending. A `.after()` / `.output` chip pair asks the
    question; every edge turns PINK dashed. The BLUE bucket blackboard spreads under the chain; the
    chain runs again and raw.zip, clean.zip, model/ chalk in (GREEN write arrows) as each step
    finishes. PANEL(ml-workflow/README.md: 70, excerpt) "The pipeline only decides when each step
    starts." lit YELLOW; the edges flash.
 3  Excerpt chip model.py · line 84 `ARTIFACT_URI = f"gs://{bucket_name}/model"`; a PINK arrow
    from deploy reaches into model/ by name; the training → deploy edge flashes. "Delete one": the
    edge is cut (RED ✗, it fades), training and deploy start together, model/ is not written yet,
    the bucket holds a GREY dashed "model/ · last run"; deploy's arrow turns RED into it, RED stamp
    "stale read", deploy ringed RED.
 4  LECTURE 37 again. The cut edge returns, training and deploy succeed, the board goes. GREY
    chip "slide 37 · processor → training: TF records" with a TEAL arrow processor → training
    "TF records"; the GREEN chip "main today · training downloads its own dataset" writes in, the
    TEAL arrow is struck GREY and a BLUE arrow from a "release download" glyph enters training;
    excerpt chip task.py · line 104. The three edges flash: order, not data.
 5  Tag out. AWS: the four nodes give way to five SageMaker steps (DataCollector … DeployModel),
    region title "SageMaker Pipelines", connections GREY dotted. CODE(ml-workflow-aws/src/workflow/
    cli.py: 262–268) folded to 262–263, …, 265–268, lines 266–267 lit PINK; the DataProcessor →
    ModelTraining edge turns solid PINK and an `S3Uri` token rides it; the panel gives way to the
    excerpt chips of lines 219, 277, 309, and each other edge turns solid as its chip lands.
 6  CODE(ml-workflow-aws/src/workflow/cli.py: 320–324), line 322 lit; it gives way to the
    `steps=[…]` list's five chips; they shuffle twice; the graph above does not move; the edges
    flash at "order comes from the references".
 7  Everything fades. TAKEAWAY "SageMaker Pipelines → the same DAG idea: referencing a step's
    properties makes the edge", rows flash with the SAY; then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    CurvedArrow,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    VGroup,
)

import common as C
from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources
WF = "ml-workflow/src/workflow/cli.py"
MP = "ml-workflow/src/workflow/model.py"
TK = "ml-workflow/src/model-training/package/trainer/task.py"
AWS = "ml-workflow-aws/src/workflow/cli.py"
RM = "ml-workflow/README.md"
assert source_line(WF, 27).strip() == f'DATA_COLLECTOR_IMAGE = "{COLLECTOR_IMAGE}"', source_line(WF, 27)
assert source_line(WF, 190).strip() == "@dsl.container_component", source_line(WF, 190)
assert source_line(WF, 193).strip() == "image=DATA_COLLECTOR_IMAGE,", source_line(WF, 193)
assert source_line(WF, 203).strip() == "return container_spec", source_line(WF, 203)
assert source_line(MP, 84).strip() == 'ARTIFACT_URI = f"gs://{bucket_name}/model"', source_line(MP, 84)
assert "releases/download/v4.0/cheese_4_labels.zip" in source_line(TK, 104), source_line(TK, 104)
assert source_line(TK, 103).strip() == "download_file(", source_line(TK, 103)
assert source_line(AWS, 262).strip() == "step_train = TrainingStep(", source_line(AWS, 262)
assert "step_process.properties.ProcessingOutputConfig" in source_line(AWS, 266), source_line(AWS, 266)
assert '.Outputs["tfrecords"].S3Output.S3Uri' in source_line(AWS, 267), source_line(AWS, 267)
assert "step_collect.properties.ProcessingOutputConfig" in source_line(AWS, 219), source_line(AWS, 219)
assert "step_train.properties.ModelArtifacts.S3ModelArtifacts" in source_line(AWS, 277), source_line(AWS, 277)
assert "step_create_model.properties.ModelName" in source_line(AWS, 309), source_line(AWS, 309)
assert source_line(AWS, 320).strip() == "sm_pipeline = Pipeline(", source_line(AWS, 320)
assert source_line(AWS, 322).strip().startswith("steps=[step_collect,"), source_line(AWS, 322)
assert CHEESE_FILES == ("raw.zip", "clean.zip", "model/"), CHEESE_FILES
assert "(raw.zip → clean.zip → model/)" in md_plain(source_line(RM, 70)), source_line(RM, 70)
assert "The pipeline only decides when each step starts." in md_plain(source_line(RM, 70))
R73 = "Vertex AI Pipelines runs on Google's machines, which cannot see your laptop"
R76 = "Container components (data collector, data processor) run one of our images."
R78A = "Python components (model training, model deploy in workflow/model.py)"
R78B = "they call the Vertex AI SDK to start a training job or deploy a model."
assert R73 in md_plain(source_line(RM, 73)), source_line(RM, 73)
assert "published to Docker Hub" in md_plain(source_line(RM, 73)), source_line(RM, 73)
assert md_plain(source_line(RM, 76)).strip().lstrip("- ").strip() == R76, source_line(RM, 76)
assert R78A in md_plain(source_line(RM, 78)) and R78B in md_plain(source_line(RM, 78)), source_line(RM, 78)
SHUFFLE_1 = [STEP_VARS[k] for k in (2, 0, 4, 1, 3)]
SHUFFLE_2 = [STEP_VARS[k] for k in (4, 3, 1, 2, 0)]

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
LIFT = 0.25                      # V6 sits 0.25 higher than built: region y -0.05..3.0
BAND_TOP = -0.15                 # the evidence band under the region (beats 1, 5, 6)
BAND_BOT = -3.5


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


def inside(m, l=SAFE_L, r=SAFE_R, b=-3.58, t=3.55):
    guard(m.get_left()[0] >= l and m.get_right()[0] <= r and m.get_bottom()[1] >= b and m.get_top()[1] <= t,
          f"out of the frame: {m.get_left()[0]:.2f} {m.get_right()[0]:.2f} {m.get_bottom()[1]:.2f} "
          f"{m.get_top()[1]:.2f}")


def apart(a, b, gap=0.1, msg=""):
    """a and b do not overlap (their boxes are at least `gap` apart on one axis)."""
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {msg}")


def flash(mob, color: str = TURN, k: float = 1.15, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def as_kind(dag, a: str, b: str, kind: str, hidden: bool = False):
    """Rebuild one wire of a Dag as `kind` before it is on screen (no animation). hidden=True: the
    new stroke stays invisible until the Piece that hides it is revealed."""
    w = dag.wire[(a, b)]
    line, tip = w._build(kind)
    w.remove(w.line, w.tip)
    w.add(line, tip)
    w.line, w.tip, w.kind = line, tip, kind
    dag.edges = [(x, y, kind if (x, y) == (a, b) else k) for x, y, k in dag.edges]
    if hidden:
        for m in (line, tip):
            C._save_op(m)
            C._set_op(m, 0)


def note_chip(rows_text, color: str = S.GREY, text_color: str = INK):
    """A GREY-outlined note: one serif row per item. .frame .rows"""
    rows = VGroup(*[label(s, CAPTION, text_color) for s in rows_text]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(rows.width + 0.4, rows.height + 0.28, color, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


def numbered(n: int, text: str):
    """A README card row: GREY line number + the README's words (serif)."""
    return VGroup(mono(str(n), CAPTION, S.GREY), label(text, CAPTION, INK)).arrange(RIGHT, buff=0.2)


def short_ex(sub: str, path: str, n: int):
    """An excerpt chip of one source line, headed "path · line n (excerpt)", sub checked."""
    return excerpt_chip(sub, f"{path} · line {n} (excerpt)", line=source_line(path, n))


def release_glyph():
    """A BLUE "release download" chip with a small download arrow on its left."""
    c = chip("release download", CLOUD, size=CAPTION)
    a = Arrow(UP * 0.2, DOWN * 0.2, buff=0, color=CLOUD, stroke_width=4, tip_length=0.14,
              max_tip_length_to_length_ratio=0.5)
    base = Line(LEFT * 0.16, RIGHT * 0.16, color=CLOUD, stroke_width=4).next_to(a, DOWN, buff=0.02)
    ic = VGroup(a, base).next_to(c, LEFT, buff=0.12)
    return VGroup(ic, c)


class CheesePipeline(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        tc = TwoClouds(show=("region", "chain"))      # board, files and SageMaker steps hidden
        for a, b in zip(tc.keys, tc.keys[1:]):
            as_kind(tc.chain, a, b, "pending")
        for a, b in zip(SAGEMAKER, SAGEMAKER[1:]):
            as_kind(tc.sm, a, b, "pending", hidden=True)
        tc.shift(UP * LIFT)
        inside(tc.region)
        guard(tc.region.get_top()[1] <= C.LREF_BOTTOM - 0.05, "V6 region under the lecture tag")
        nd = tc.chain.node
        col, prc, trn, dep = (nd[k] for k in tc.keys)

        # ========================================================== 0 · slide 37's zig-zag runs
        lr = None
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "37")
            self.play(FadeIn(tc), run_time=0.9)
            vo.wait_until("collector, processor")
            for k in tc.keys:
                self.play(*tc.chain.run(k), run_time=0.35)
                self.play(*tc.chain.succeed(k), run_time=0.35)
            vo.wait_until("Each gets a green check")
            self.play(LaggedStart(*[flash(nd[k].ok, OWN, 1.4) for k in tc.keys], lag_ratio=0.25), run_time=1.4)

        # ========================================================== 1 · two kinds of steps
        cli = src_panel(WF, [(190, 193), (202, 203)])
        place(cli, left=SAFE_L, top=BAND_TOP)
        inside(cli)
        b193 = cli.bar(193)
        b190 = cli.bar(190)
        ex27 = excerpt_chip(f'"{COLLECTOR_IMAGE}"', "cli.py · line 27 (excerpt)", line=source_line(WF, 27))
        place(ex27, right=SAFE_R, top=BAND_TOP)
        s34 = note_chip(["slide 34: Artifact Registry", "repo: Docker Hub", "any registry Vertex can reach"])
        place(s34, right=SAFE_R, top=ex27.get_bottom()[1] - 0.3)
        inside(s34)
        apart(cli, ex27, 0.15, "cli panel / excerpt 27")
        apart(cli, s34, 0.15, "cli panel / slide 34 note")
        teal = chip("image from Docker Hub", CTR, size=CAPTION)
        place(teal, left=col.frame.get_left()[0] - 0.05, cy=prc.frame.get_center()[1])
        apart(teal, prc, 0.15, "TEAL chip / processor")
        apart(teal, col, 0.15, "TEAL chip / collector")
        guard(teal.get_left()[0] >= tc.region.get_left()[0] + 0.05, "TEAL chip inside the region")
        purple = chip("Python + Vertex AI SDK", TOOL, size=CAPTION)
        place(purple, right=tc.region.get_right()[0] - 0.12, bottom=trn.frame.get_top()[1] + 0.06)
        guard(purple.get_top()[1] <= tc.region.get_top()[1] - 0.05, "PURPLE chip inside the region")
        apart(purple, dep, 0.15, "PURPLE chip / deploy")
        rcard = readme_card(f"{RM} · lines 73, 76, 78 (excerpts)",
                            [numbered(73, f"… {R73} …"), numbered(76, R76),
                             numbered(78, f"{R78A} … {R78B}")])
        place(rcard, left=SAFE_L, top=BAND_TOP)
        inside(rcard)
        guard(rcard.width <= 12.9, "README card width")
        row78 = rcard.rows[2]
        if row78.width > 12.0:
            raise ValueError("row 78 too wide")
        with self.voiceover(SAY[1]) as vo:
            lr = lref_swap(self, lr, "34")
            self.play(FadeIn(cli, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The collector and processor")
            self.play(FadeIn(b190), flash(cli.span(190, "container_component"), TURN, 1.08),
                      *[n.frame.animate.set_stroke(CTR, 3.5) for n in (col, prc)], run_time=0.7)
            vo.wait_until("pull published images")
            self.play(FadeIn(b193), FadeIn(ex27, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(teal, shift=UP * 0.1), flash(ex27.chip, CTR, 1.05), run_time=0.6)
            vo.wait_until("Docker Hub in this repo")
            self.play(flash(teal, CTR, 1.08), run_time=0.6)
            vo.wait_until("the Artifact Registry")
            self.play(FadeIn(s34, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("because Google")
            self.play(FadeOut(VGroup(cli, b190, b193, ex27, s34)), run_time=0.5)
            self.play(FadeIn(rcard, shift=UP * 0.15), run_time=0.6)
            hb73 = ring(rcard.rows[0], TURN, buff=0.06)
            self.play(FadeIn(hb73), run_time=0.4)
            vo.wait_until("Training and deploy")
            hb78 = ring(rcard.rows[2], TOOL, buff=0.06)
            self.play(FadeOut(hb73), FadeIn(hb78), FadeIn(purple, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("call the Vertex AI SDK")
            self.play(flash(purple, TOOL, 1.08), *[flash(n.frame, TOOL, 1.04) for n in (trn, dep)], run_time=0.7)

        # ========================================================== 2 · why .after(): the bucket
        q_after = chip(".after()", EDGE, size=CAPTION, font=MONO)
        q_not = label("and not", CAPTION, S.GREY)
        q_out = chip(".output", S.GREY, size=CAPTION, font=MONO)
        q = VGroup(q_after, q_not, q_out).arrange(RIGHT, buff=0.2)
        q.move_to([0, -2.85, 0])
        q_strike = strike(q_out, S.GREY)
        rd70 = readme_panel("ml-workflow", 70, clip={70: ("The pipeline only", None)})
        place(rd70, cx=0, bottom=BAND_BOT)
        inside(rd70)
        rd70_bar = rd70.bar("The pipeline only decides when each step starts.", TURN)
        board = tc.parts["board"]
        files = tc.files
        writes = {}
        for k, f in zip(tc.keys, CHEESE_FILES):
            writes[f] = tc.reach(f, k, OWN)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(lr), FadeOut(VGroup(rcard, hb78, purple, teal)),
                      *[n.frame.animate.set_stroke(INK, 2.5) for n in (col, prc)], run_time=0.6)
            lr = None
            self.play(FadeIn(q_after, shift=UP * 0.1), run_time=0.4)
            restyles = []
            for a, b in zip(tc.keys, tc.keys[1:]):
                restyles += tc.chain.restyle(a, b, "order")
            self.play(*restyles, run_time=0.8)
            vo.wait_until("and not dot output")
            self.play(FadeIn(VGroup(q_not, q_out), shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(q_strike), run_time=0.3)
            vo.wait_until("The steps never call")
            resets = [a for k in tc.keys for a in nd[k].reset()]
            self.play(*resets, run_time=0.5)
            self.play(LaggedStart(*[flash(nd[k].frame, INK, 1.05) for k in tc.keys], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("Each reads from the bucket")
            self.play(FadeOut(VGroup(q, q_strike)), *tc.parts_in("board", anim=lambda m: GrowFromEdge(m, UP)),
                      run_time=0.7)
            self.play(*tc.chain.run("collector"), run_time=0.4)
            vo.wait_until("raw zip")
            self.play(*tc.chain.succeed("collector"), FadeIn(writes["raw.zip"]), *tc.chalk("raw.zip"),
                      *tc.chain.run("processor"), run_time=0.5)
            vo.wait_until("clean zip")
            self.play(*tc.chain.succeed("processor"), FadeIn(writes["clean.zip"]), *tc.chalk("clean.zip"),
                      FadeOut(writes["raw.zip"]), *tc.chain.run("training"), run_time=0.5)
            vo.wait_until("the model folder")
            self.play(*tc.chain.succeed("training"), FadeIn(writes["model/"]), *tc.chalk("model/"),
                      FadeOut(writes["clean.zip"]), run_time=0.5)
            self.play(*tc.chain.run("deploy"), FadeOut(writes["model/"]), run_time=0.4)
            self.play(*tc.chain.succeed("deploy"), run_time=0.4)
            vo.wait_until("The pipeline only decides")
            self.play(FadeIn(rd70, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(rd70_bar), *[tc.chain.wire[(a, b)].light(EDGE) for a, b in zip(tc.keys, tc.keys[1:])],
                      run_time=0.9)

        # ========================================================== 3 · deploy finds model/ by name
        ex84 = short_ex('ARTIFACT_URI = f"gs://{bucket_name}/model"', MP, 84)
        place(ex84, cx=0, bottom=BAND_BOT + 0.1)
        inside(ex84)
        apart(ex84, board, 0.15, "excerpt 84 / board")
        grab = tc.reach("model/", "deploy", EDGE)
        cut_w = tc.chain.wire[("training", "deploy")]
        cut_x = x_mark(0.34).move_to(cut_w.path.point_from_proportion(0.5))
        ghost = ghost_file("model/ · last run")
        place(ghost, left=files["model/"].get_left()[0], cy=files["model/"].get_center()[1])
        stale = stamp("stale read", ERR)
        place(stale, left=ghost.get_right()[0] + 0.3, cy=ghost.get_center()[1])
        inside(stale)
        guard(stale.get_right()[0] <= board[0].get_right()[0] - 0.05, "stamp inside the board")
        bad = _red_arrow(dep, ghost)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(rd70, rd70_bar)), run_time=0.4)
            self.play(FadeIn(ex84, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(grab), run_time=0.5)
            vo.wait_until("in the model folder")
            self.play(flash(files["model/"], OWN, 1.15), flash(ex84.chip, TURN, 1.04), run_time=0.7)
            vo.wait_until("and the edges make")
            self.play(cut_w.light(TURN, 1.0), run_time=1.0)
            vo.wait_until("Delete one")
            self.play(FadeIn(cut_x, scale=1.3), FadeOut(grab), run_time=0.4)
            self.play(*tc.chain.parts_out("wire:training->deploy"), FadeOut(cut_x),
                      *trn.reset(), *dep.reset(), *tc.parts_out("file:model/"), run_time=0.6)
            self.play(FadeIn(ghost), run_time=0.4)
            vo.wait_until("and deploy may grab")
            self.play(*trn.run(), *dep.run(), run_time=0.5)
            self.play(FadeIn(bad), run_time=0.5)
            vo.wait_until("the stale read")
            dring = ring(dep.frame, ERR, buff=0.08)
            self.play(FadeIn(stale, scale=1.2), FadeIn(dring), run_time=0.5)

        # ========================================================== 4 · slide 37 vs main today
        s37 = chip("slide 37 · processor → training: TF records", S.GREY, size=CAPTION)
        main = chip("main today · training downloads its own dataset", OWN, size=CAPTION)
        chips_row = VGroup(s37, main).arrange(RIGHT, buff=0.3)
        place(chips_row, cx=0, top=BAND_TOP - 0.25)
        inside(chips_row)
        tf_arrow = CurvedArrow(prc.frame.get_top() + UP * 0.06 + LEFT * 0.3,
                               trn.frame.get_left() + LEFT * 0.08 + UP * 0.12,
                               angle=-1.2, color=CTR, stroke_width=4, tip_length=0.16)
        tf_lab = label("TF records", CAPTION, CTR)
        place(tf_lab, right=tf_arrow.get_left()[0] - 0.08, cy=trn.frame.get_center()[1])
        apart(tf_lab, col, 0.12, "TF records label / collector")
        rel = release_glyph()
        place(rel, right=tc.region.get_right()[0] - 0.15, top=tc.region.get_top()[1] - 0.15)
        apart(rel, trn, 0.3, "release glyph / training")
        apart(rel, dep, 0.15, "release glyph / deploy")
        rel_arrow = Arrow(rel.get_left() + RIGHT * 0.02, trn.frame.get_right() + UP * 0.12, buff=0.06,
                          color=CLOUD, stroke_width=4, tip_length=0.16, max_tip_length_to_length_ratio=0.4)
        ex104 = short_ex("releases/download/v4.0/cheese_4_labels.zip", TK, 104)
        place(ex104, cx=0, top=chips_row.get_bottom()[1] - 0.45)
        inside(ex104)
        with self.voiceover(SAY[4]) as vo:
            lr = lref_swap(self, lr, "37")
            self.play(FadeOut(VGroup(ex84, ghost, stale, bad, dring)), *tc.chain.parts_in("wire:training->deploy"),
                      *trn.succeed(), *dep.succeed(), *tc.parts_in("file:model/"), run_time=0.6)
            self.play(*tc.parts_out("board", *[f"file:{f}" for f in CHEESE_FILES]), run_time=0.5)
            self.play(FadeIn(s37, shift=UP * 0.1), FadeIn(tf_arrow), FadeIn(tf_lab), run_time=0.6)
            vo.wait_until("on the main branch today")
            self.play(FadeIn(main, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("training downloads")
            tf_strike = strike(tf_lab, S.GREY)
            self.play(tf_arrow.animate.set_color(S.GREY), tf_lab.animate.set_color(S.GREY), FadeIn(tf_strike),
                      FadeIn(rel, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(rel_arrow), FadeIn(ex104, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("so these edges carry order")
            self.play(*[tc.chain.wire[(a, b)].light(EDGE, 1.0) for a, b in zip(tc.keys, tc.keys[1:])], run_time=1.0)
            vo.wait_until("not data")
            self.play(flash(main, OWN, 1.05), run_time=0.6)

        # ========================================================== 5 · AWS: references make the edges
        aws = src_panel(AWS, [(262, 263), (265, 268)])
        place(aws, cx=0, top=BAND_TOP)
        inside(aws)
        b_ref = VGroup(aws.bar(266, EDGE, 0.25), aws.bar(267, EDGE, 0.25))
        sm = tc.sm
        tok = None
        ex_chips = VGroup(short_ex("step_collect.properties.ProcessingOutputConfig", AWS, 219),
                          short_ex("step_train.properties.ModelArtifacts.S3ModelArtifacts", AWS, 277),
                          short_ex("step_create_model.properties.ModelName", AWS, 309))
        ex_chips.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        place(ex_chips, cx=0, top=BAND_TOP - 0.05)
        inside(ex_chips)
        follow = [("DataCollector", "DataProcessor"), ("ModelTraining", "CreateModel"),
                  ("CreateModel", "DeployModel")]
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(lr), FadeOut(VGroup(s37, main, tf_arrow, tf_lab, tf_strike, rel, rel_arrow, ex104)),
                      run_time=0.5)
            lr = None
            self.play(*tc.to_sagemaker(), run_time=1.0)
            vo.wait_until("runs the same idea")
            self.play(flash(tc.region_title, CLOUD, 1.1), run_time=0.6)
            vo.wait_until("The training step")
            self.play(FadeIn(aws, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("points at")
            self.play(FadeIn(b_ref), flash(aws.span(266, "step_process.properties"), EDGE, 1.06), run_time=0.6)
            vo.wait_until("output property")
            self.play(*sm.restyle("DataProcessor", "ModelTraining", "data"), run_time=0.6)
            tok = sm.node["DataProcessor"].token("S3Uri")
            tok.move_to(sm.wire[("DataProcessor", "ModelTraining")].path.get_start())
            self.play(FadeIn(tok, scale=0.8), run_time=0.25)
            self.play(sm.wire[("DataProcessor", "ModelTraining")].ride(tok, run_time=0.8))
            vo.wait_until("and that reference")
            self.play(FadeOut(VGroup(aws, b_ref, tok)), run_time=0.4)
            for chip_, (a, b) in zip(ex_chips, follow):
                self.play(FadeIn(chip_, shift=UP * 0.1), *sm.restyle(a, b, "data"), run_time=0.45)

        # ========================================================== 6 · shuffle the steps list
        p320 = src_panel(AWS, 320, 324, wrap=True)
        place(p320, cx=0, top=BAND_TOP)
        inside(p320)
        b322 = p320.bar(322)
        row = tc.steps_list()
        place(row, cx=0, cy=-1.7)
        inside(row)
        sm_wires = [sm.wire[(a, b)] for a, b in zip(SAGEMAKER, SAGEMAKER[1:])]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(ex_chips), FadeIn(p320, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(b322), flash(p320.span(322, "steps=["), TURN, 1.1), run_time=0.6)
            vo.wait_until("and the graph")
            self.play(FadeOut(VGroup(p320, b322)), FadeIn(row, shift=DOWN * 0.2), run_time=0.6)
            self.play(*tc.shuffle(row, SHUFFLE_1), run_time=0.9)
            vo.wait_until("order comes from")
            self.play(LaggedStart(*[w.light(EDGE, 0.8) for w in sm_wires], lag_ratio=0.25),
                      *tc.shuffle(row, SHUFFLE_2), run_time=1.4)

        # ========================================================== 7 · takeaway
        tk = takeaway("SageMaker Pipelines → the same DAG idea: referencing a step's properties makes the edge")
        inside(tk)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(tc, row)), run_time=0.6)
            self.play(*tk.write(), run_time=1.4)
            vo.wait_until("Referencing")
            self.play(flash(tk.rows[-1], TURN, 1.04), run_time=0.6)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)


def _red_arrow(node, target):
    """RED arrow from a node's bottom into a bucket file (deploy grabbing last run's model)."""
    return Arrow(node.frame.get_bottom(), target.get_top() + UP * 0.05, buff=0.06, color=ERR, stroke_width=4,
                 tip_length=0.16, max_tip_length_to_length_ratio=0.3)
