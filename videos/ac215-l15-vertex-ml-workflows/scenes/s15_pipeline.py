"""S15 · A pipeline drawn by references (README B › SageMaker Pipelines steps 1-3, slides 28-30,
33 and 37-38 redrawn, V8 ReferenceDAG built).

Beats (script.md "## S15", one voiceover block each):
 0  TRACKER B7 (appears, 3 dots, dim) -> step 1. LECTURE 15 · 28-29. Two columns: GREY-dashed "the
    lecture · KFP DSL" (`@dsl.component` -> `.output` -> "compile → YAML") and BLUE "this tutorial ·
    SageMaker SDK" (step classes -> property references (PINK) -> JSON definition (GREEN)); a GREEN
    "plain Python" band spans both. Tag and picture leave together.
 1  V8 begins: five WHITE step boxes in a pile on the right (shifted up to clear the panel).
    CODE(cli.py: 165) at the bottom, `expire_after="30d"` GREEN; "cached · 30d" settles on
    DataCollector and copies to DataProcessor, ModelTraining, DeployModel; CreateModel gets "no
    cache_config". Then CODE(cli.py: 180-191) on the left (line 186 cut): `name="DataCollector"`
    YELLOW, `ProcessingOutput(` / `output_name="raw-data"` PINK.
 2  The cache chips go and the pile moves right (code panels are wide). CODE(cli.py: 219-220) at
    the bottom: the reference lights PINK token by token; chip "a string" struck RED, "a reference"
    GREEN; PINK edge DataCollector -> DataProcessor (the two boxes pull into line).
 3  CODE(cli.py: 266-267, line 266 cut): `Outputs["tfrecords"]` PINK -> edge DataProcessor ->
    ModelTraining; CODE(cli.py: 277, cut): `step_train.properties.ModelArtifacts` PINK -> edge
    ModelTraining -> CreateModel. Edges pulse: a chain of four.
 4  CODE(cli.py: 309): `step_create_model.properties.ModelName` PINK -> edge CreateModel ->
    DeployModel: the chain of five. CODE(cli.py: 320-327, line 322 cut): line 322 YELLOW; LECTURE
    15 · 33 with lines 326-327 PURPLE: laptop -> SageMaker, a λ tile travels (the deploy Lambda),
    then two PURPLE arrows `upsert` / `start`. Tag and picture leave together.
 5  The graph dims; line 322's list enlarged (steps_list, 24 pt). PONDER(8 s).
 6  The list reverses (names fly to their new places), then shuffles again; the graph does not
    move; its PINK edges pulse. Chip "order = references · list = a set".
 7  TRACKER B7 1 · extra · built offline, not sent. The graph steps aside; a 15-row terminal types
    laptop/92 line 1 (cut) -> TERM(laptop/92: 30 from "Running within a PipelineSession" wrap, …,
    59, 113, 143, 186, 246, 260, …, 279): the five "Name" lines YELLOW (246: chip "the SDK adds the
    suffix"), 143 PINK, 279 GREY. Then the graph returns and a GREEN JSON sheet is pressed out of
    it, a GREY-dashed "YAML (the lecture, slide 29)" sheet beside it. LECTURE 15 · 30 (this block).
 8  LECTURE 15 · 37-38. V8 re-lays as a row (higher up); slide 37's four-node chain (GREY dashed)
    above it; "Model Deploy" splits onto CreateModel (a BLUE Model card) and DeployModel (a λ tile);
    bridge chip "Cloud Functions → Lambda" lower right. Then (chain and tag leave) CODE(
    deploy_model_lambda.py: 47-57, cut lines) with `update_endpoint(` / `create_endpoint(` YELLOW;
    top right the `cheese-app-endpoint` plate with its configuration card swapping beside it.
 9  The shared drawer: V8 back to its row; the BLUE bucket with empty trays (declared outputs);
    raw.zip, clean.zip, tfrecords.zip drop into the bucket root by name; code-ref chips
    (data-collector/cli.py:65, data-processor/cli.py:68); "?" on ModelTraining "not verified here";
    note "edges set the order · files travel by name".
10  TRACKER B7 1. 6-row terminal at the container prompt: `python cli.py --pipeline` -> TERM(
    laptop/90: 108, …, 153-154 wrap) RED; ▶ your turn; chip "with keys: SageMaker Pipeline started:
    <ARN> · no output shown"; erratum card (Lambda runtime, cli.py:297). TRACKER B7 2:
    CONSOLE("SageMaker Unified Studio › Build › ML Pipelines"): the five-box graph redrawn from
    laptop/92 (4th box CreateModel-CreateModel), all pending; tag illustration · not run here.
11  The console graph runs: boxes YELLOW then GREEN in turn; "next run" DataCollector cached; on
    "green" DeployModel GREEN while the plate shows "Creating" ORANGE, then "wait for InService"
    YELLOW; GOLD cost tags (each step's machine, a new Lambda per run, cheese-app-endpoint).
12  TRACKER B7 3. 9-row terminal: `python cli.py --data_collector` (chip "shown in S14"),
    `--data_processor`, `--model_training`, `--model_deploy`, each with its own last error line
    (laptop/90: 98, 208, 263, 318 to "(InvalidClientTokenId)") RED; card "each flag …". Fade to empty.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
CLI = "B/src/workflow/cli.py"
DML = "B/src/workflow/deploy_model_lambda.py"
assert excerpt(CLI, 165, 165).strip() == 'cache_cfg = CacheConfig(enable_caching=True, expire_after="30d")'
assert excerpt(CLI, 181, 181).strip() == 'name="DataCollector",'
assert excerpt(CLI, 191, 191).strip() == 'output_name="raw-data",'
assert excerpt(CLI, 219, 219).strip() == "source=step_collect.properties.ProcessingOutputConfig"
assert excerpt(CLI, 220, 220).strip() == '.Outputs["raw-data"].S3Output.S3Uri,'
assert excerpt(CLI, 267, 267).strip() == '.Outputs["tfrecords"].S3Output.S3Uri'
assert excerpt(CLI, 277, 277).strip() == "model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,"
assert excerpt(CLI, 309, 309).strip() == '"model_name": step_create_model.properties.ModelName,'
assert excerpt(CLI, 322, 322).strip().startswith("steps=[step_collect, step_process, step_train,")
assert excerpt(CLI, 326, 327).split("\n")[0].strip() == "sm_pipeline.upsert(role_arn=role)"
assert excerpt(CLI, 297, 297).strip() == "deploy_model_lambda = Lambda("
assert "sm_client.update_endpoint(" in excerpt(DML, 49, 49)
assert "sm_client.create_endpoint(" in excerpt(DML, 55, 55)
assert 'upload_file(zip_file, S3_BUCKET_NAME, "raw.zip")' in excerpt("B/src/data-collector/cli.py", 65, 65)
assert 'upload_file(zip_file, S3_BUCKET_NAME, "clean.zip")' in excerpt("B/src/data-processor/cli.py", 68, 68)

C92, C90 = capture("92"), capture("90")
assert C92.cmd.startswith("docker run --rm --entrypoint pipenv") and C92.cmd.endswith("pipeline_offline.py")
L92_30 = from_phrase(C92.line(30), "Running within a PipelineSession")
assert L92_30.startswith("…Running within a PipelineSession, there will be No Wait"), L92_30
NAME_NUMS = (59, 113, 186, 246, 260)
NAMES92 = [C92.line(n) for n in NAME_NUMS]
assert [s.strip() for s in NAMES92] == ['"Name": "DataCollector",', '"Name": "DataProcessor",',
                                        '"Name": "ModelTraining",', '"Name": "CreateModel-CreateModel",',
                                        '"Name": "DeployModel",'], NAMES92
L92_143 = C92.line(143)
assert L92_143.strip() == '"Get": "Steps.DataCollector.ProcessingOutputConfig.Outputs[\'raw-data\'].S3Output.S3Uri"'
_k = L92_143.index(".Outputs")
L92_143A, L92_143B = L92_143[:_k], L92_143[_k:]   # the row break moves; the text is unchanged
L92_279 = C92.line(279)
assert L92_279.startswith("[capture stub] Pipeline.upsert() and start() NOT sent")

T100 = C90.typed(100)
assert T100 == "python cli.py --pipeline"
L90_108 = C90.line(108)
assert L90_108 == "INFO:botocore.credentials:Found credentials in environment variables."
L90_110 = unbox(C90.line(110)).strip()
assert L90_110 == "/app/cli.py:32 in <module>", L90_110
L90_115 = unbox(C90.line(115)).strip()
assert L90_115 == "❱  32 ACCOUNT_ID = sts_client.get_caller_identity()['Account']", L90_115
L90_153 = C90.at(153, 154)
assert L90_153[0].startswith("ClientError: An error occurred (InvalidClientTokenId)")
COMPONENTS = [(45, 98), (155, 208), (210, 263), (265, 318)]   # (typed line, its last error line)
FLAGS = [C90.typed(a) for a, _ in COMPONENTS]
assert FLAGS == ["python cli.py --data_collector", "python cli.py --data_processor",
                 "python cli.py --model_training", "python cli.py --model_deploy"], FLAGS
ERRS = [cut(C90.line(b), "(InvalidClientTokenId)") for _, b in COMPONENTS]
assert all(e == "ClientError: An error occurred (InvalidClientTokenId)…" for e in ERRS), ERRS

CONSOLE_NAMES = ("DataCollector", "DataProcessor", "ModelTraining", "CreateModel-CreateModel", "DeployModel")
PONDER_Q = "Reverse the list steps=[…]\nin Pipeline(...).\nDoes the run order change?"
LX = -6.45                                    # the left edge of panels and cards
DX = 1.8                                      # V8 steps right while the wide reference panels show


def fixed_tracker(key: str, step=None, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (the head's arrange() centres it at
    y 0; the workaround of S01, S03-S14; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def at_bl(m, y: float = -3.52):
    """Bottom-left of the frame (panels under the graph)."""
    return m.move_to([LX + m.width / 2, y + m.height / 2, 0])


def at_tl(m, y: float = 2.75):
    """Top-left of the picture area (under the tracker)."""
    return m.move_to([LX + m.width / 2, y - m.height / 2, 0])


def two_line_chip(top: str, bottom: str, color=S.GREY) -> VGroup:
    t = VGroup(label(top, 20, INK), label(bottom, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    b = box(t.width + 0.48, t.height + 0.3, color, fill_opacity=0.16, radius=0.16)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def lecture_node(s: str, node_w: float = 2.2) -> VGroup:
    """A node of a redrawn lecture picture (GREY dashed, label font)."""
    t = label(s, 20, S.GREY)
    ob = outline_box(max(node_w, t.width + 0.3), 0.5, PAST, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def model_card_icon(text: str = "Model") -> VGroup:
    """A small BLUE SageMaker Model card (V5's model card in miniature)."""
    t = label(text, 20, INK)
    g0 = file_glyph(0.3, CLOUD)
    row = VGroup(g0, t).arrange(RIGHT, buff=0.12)
    b = box(row.width + 0.36, 0.5, CLOUD, fill_opacity=0.18, radius=0.08)
    row.move_to(b)
    return VGroup(b, row)


def folded_line(path: str, n: int, at: str, font_size: float = 20) -> VGroup:
    """CODE(path: n) with the one source line folded over two rows before `at` (the text unchanged,
    the second row indented 4), header 'line n' (code() would count two lines)."""
    src = excerpt(path, n, n).strip()
    k = src.index(at)
    p = code_panel(src[:k] + "\n    " + src[k:], shown_path(path), n, "python", font_size=font_size)
    where = p.header[1]
    new = label(f"· line {n}", CAPTION, S.GREY).move_to(where, aligned_edge=LEFT)
    p.header.remove(where)
    p.header.add(new)
    assert p.width < 2 * SAFE_X - 0.1, p.width
    return p


class PropertyDAG(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 13, len(SAY)
        self.bar_tags = []
        self.t = None

        # ========================================================== 0. KFP DSL vs SageMaker SDK
        tr = fixed_tracker("B7")
        lt = lref("28–29")
        xl, xr = -3.3, 3.3
        hl = dashed_chip("the lecture · KFP DSL", PAST)
        hr = chip("this tutorial · SageMaker SDK", CLOUD, size=20)
        lefts = [dashed_chip("@dsl.component", PAST, mono_font=True), dashed_chip(".output", PAST, mono_font=True),
                 dashed_chip("compile → YAML", PAST)]
        rights = [chip("step classes", CLOUD, size=20), chip("property references", ROUTE, size=20),
                  chip("JSON definition", OWN, size=20)]
        ys = [1.15, -0.05, -1.25]
        hl.move_to([xl, 2.2, 0])
        hr.move_to([xr, 2.2, 0])
        for m, y in zip(lefts, ys):
            m.move_to([xl, y, 0])
        for m, y in zip(rights, ys):
            m.move_to([xr, y, 0])
        downs_l = [arrow(lefts[i].get_bottom(), lefts[i + 1].get_top(), S.GREY, buff=0.08) for i in range(2)]
        downs_r = [arrow(rights[i].get_bottom(), rights[i + 1].get_top(), CLOUD, buff=0.08) for i in range(2)]
        across = [arrow(lefts[i].get_right(), rights[i].get_left(), S.GREY, stroke=2, buff=0.25) for i in range(3)]
        py_band = outline_box(11.0, 0.62, OWN, solid=True, fill_opacity=0.12)
        py_band.move_to([0, -2.45, 0])
        py_t = label("plain Python", 22, INK).move_to(py_band)
        pic0 = VGroup(hl, hr, *lefts, *rights, *downs_l, *downs_r, *across, py_band, py_t)
        assert pic0.get_top()[1] < lt.get_bottom()[1] - 0.05 and hl.get_top()[1] < TRACK_BOTTOM - 0.05, pic0.get_top()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), run_time=0.5)
            self.play(track(tr, 1), run_time=0.5)
            vo.wait_until("The slides write steps")
            self.play(FadeIn(lt), FadeIn(hl, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(lefts[0], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("wired by dot output")
            self.play(GrowArrow(downs_l[0]), FadeIn(lefts[1], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and compiled to YAML")
            self.play(GrowArrow(downs_l[1]), FadeIn(lefts[2], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Here:")
            self.play(FadeIn(hr, shift=DOWN * 0.1), GrowArrow(across[0]), FadeIn(rights[0], shift=LEFT * 0.1),
                      run_time=0.6)
            vo.wait_until("property references")
            self.play(GrowArrow(across[1]), GrowArrow(downs_r[0]), FadeIn(rights[1], shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and JSON")
            self.play(GrowArrow(across[2]), GrowArrow(downs_r[1]), FadeIn(rights[2], shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(py_band), FadeIn(py_t, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(py_t, color=OWN, scale_factor=1.1), run_time=0.6)

        # ========================================================== 1. caching · the collector step
        v = ReferenceDAG()
        v.shift(UP * 0.35)
        p165 = at_bl(code(CLI, 165, 165, font_size=20, dedent=True))
        assert p165.get_top()[1] < min(b.get_bottom()[1] for b in v.boxes) - 0.08, p165.get_top()
        assert max(b.get_top()[1] for b in v.boxes) < 3.2
        p180 = at_tl(code(CLI, 180, 191, font_size=20, dedent=True, cuts={186: '"brie cheese",'}))
        assert p180.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.15, p180.get_right()
        assert p180.get_bottom()[1] > -3.55
        assert excerpt(CLI, 185, 185).strip() == '"--nums", "50",' and '"--nums","10",' in excerpt(CLI, 66, 66)
        nums_c = grey_chip("pipeline: 50 per cheese · standalone collector: 10")
        nums_c.next_to(p180, DOWN, buff=0.2).align_to(p180, LEFT)
        assert nums_c.get_bottom()[1] > -3.55 and nums_c.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1, \
            nums_c.get_corner(DR)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(pic0), FadeOut(lt), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in v.boxes], lag_ratio=0.15), run_time=1.0)
            self.remove(*v.boxes)
            self.add(v)
            self.play(FadeIn(p165, shift=UP * 0.2), run_time=0.5)
            self.paint(p165, 0, 'expire_after="30d"', OWN)
            v.cache(self)
            assert all(c.get_right()[0] < 6.6 for c in v.chips), [c.get_right() for c in v.chips]
            vo.wait_until("The first step")
            self.play(FadeOut(p165), run_time=0.4)
            self.play(FadeIn(p180, shift=RIGHT * 0.2), run_time=0.6)
            self.paint(p180, 1, 'name="DataCollector"', TURN)
            self.play(Indicate(v.boxes[0].text, color=TURN, scale_factor=1.12),
                      code_span(p180.code, 5, '"50"').animate.set_color(TURN),
                      FadeIn(nums_c, shift=UP * 0.1), run_time=0.6)     # 50 here, 10 in S14's run
            self.add(p180)
            v.heal(self)
            vo.wait_until("with one declared output")
            self.paint(p180, 10, "ProcessingOutput(", ROUTE)
            self.paint(p180, 11, 'output_name="raw-data"', ROUTE)
            self.play(Indicate(code_span(p180.code, 11, '"raw-data"'), color=ROUTE, scale_factor=1.12), run_time=0.6)
            self.add(p180)

        # ========================================================== 2. the first reference, the first edge
        p219 = at_bl(code(CLI, 219, 220, font_size=20, dedent=True))
        toks219 = [(0, "step_collect"), (0, ".properties"), (0, ".ProcessingOutputConfig"), (1, ".Outputs"),
                   (1, '["raw-data"]'), (1, ".S3Output"), (1, ".S3Uri")]
        s_chip = grey_chip("a string")
        r_chip = ok_chip("a reference")
        VGroup(s_chip, r_chip).arrange(RIGHT, buff=0.4)
        s_chip.move_to([LX + s_chip.width / 2, p219.get_top()[1] + 0.5, 0])
        r_chip.next_to(s_chip, RIGHT, buff=0.4)
        s_x = strike(s_chip)

        with self.voiceover(SAY[2]) as vo:
            v.uncache(self)
            self.play(FadeOut(p180), FadeOut(nums_c), v.animate.shift(RIGHT * DX + DOWN * 0.35), run_time=0.8)
            v.heal(self)
            assert p219.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1, p219.get_right()
            self.play(Indicate(v.boxes[1].text, color=TURN, scale_factor=1.12), run_time=0.6)
            v.heal(self)
            vo.wait_until("takes as input a property")
            self.play(FadeIn(p219, shift=UP * 0.2), run_time=0.5)
            self.play(LaggedStart(*[code_span(p219.code, k, s).animate.set_color(ROUTE) for k, s in toks219],
                                  lag_ratio=0.35), run_time=2.0)
            self.add(p219)
            vo.wait_until("Not a string:")
            self.play(FadeIn(s_chip, shift=UP * 0.1), run_time=0.4)
            self.play(Create(s_x), run_time=0.4)
            self.play(FadeIn(r_chip, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and it draws an edge")
            v.edge(self, 0, run_time=1.4)
            self.play(Indicate(v.edges[(0, 1)], color=ROUTE, scale_factor=1.1), run_time=0.6)
            v.heal(self)

        # ========================================================== 3. two more references
        p266 = at_bl(code(CLI, 266, 267, font_size=20, dedent=True, cuts={266: "step_process.properties"}))
        p277 = at_bl(folded_line(CLI, 277, ".S3ModelArtifacts"))
        for p in (p266, p277):
            assert p.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1, p.get_right()

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p219, s_chip, s_x, r_chip)), run_time=0.4)
            self.play(FadeIn(p266, shift=UP * 0.2), run_time=0.5)
            self.paint(p266, 0, "step_process.properties", ROUTE)
            self.paint(p266, 1, '.Outputs["tfrecords"]', ROUTE)
            v.edge(self, 1, run_time=1.2)
            vo.wait_until("and the model step")
            self.play(FadeOut(p266), run_time=0.3)
            self.play(FadeIn(p277, shift=UP * 0.2), run_time=0.5)
            self.play(code_span(p277.code, 0, "step_train.properties.ModelArtifacts").animate.set_color(ROUTE),
                      code_span(p277.code, 1, ".S3ModelArtifacts").animate.set_color(ROUTE), run_time=0.5)
            self.add(p277)
            v.edge(self, 2, run_time=1.2)
            vo.wait_until("Each reference")
            v.pulse(self)
            v.heal(self)

        # ========================================================== 4. the fifth edge · Pipeline(...)
        p309 = at_bl(code(CLI, 309, 309, font_size=20, dedent=True))
        assert p309.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1, p309.get_right()
        p320 = at_tl(code(CLI, 320, 327, font_size=20, dedent=True, cuts={322: "step_process,"}))
        lt33 = lref("33")
        lap = laptop_glyph(1.3).move_to([-5.4, -2.35, 0])
        sm_b = outline_box(2.3, 1.1, CLOUD, solid=True, fill_opacity=0.15).move_to([-0.9, -2.35, 0])
        sm_t = label("SageMaker", 22, INK).move_to(sm_b)
        a_up = arrow(lap.get_right() + UP * 0.25, sm_b.get_left() + UP * 0.25, TOOL, stroke=4, buff=0.15)
        a_st = arrow(lap.get_right() + DOWN * 0.25, sm_b.get_left() + DOWN * 0.25, TOOL, stroke=4, buff=0.15)
        up_t = mono("upsert", 20, TOOL).next_to(a_up, UP, buff=0.06)
        st_t = mono("start", 20, TOOL).next_to(a_st, DOWN, buff=0.06)
        lam = lambda_icon(0.45, text=None).move_to(lap.get_center() + UP * 0.1)
        pic33 = VGroup(lap, sm_b, sm_t)
        assert sm_b.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1
        assert p320.get_bottom()[1] > up_t.get_top()[1] + 0.1, (p320.get_bottom(), up_t.get_top())
        assert st_t.get_bottom()[1] > -3.55 and p320.get_right()[0] < 3.0, (st_t.get_bottom(), p320.get_right())

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(p277), run_time=0.3)
            self.play(FadeIn(p309, shift=UP * 0.2), Indicate(v.boxes[4].text, color=TURN, scale_factor=1.1),
                      run_time=0.6)
            v.heal(self)
            self.paint(p309, 0, "step_create_model.properties.ModelName", ROUTE)
            v.edge(self, 3, run_time=1.2)
            assert v.layout == "column"
            vo.wait_until("Then the pipeline lists")
            self.play(FadeOut(p309), run_time=0.3)
            self.play(FadeIn(p320, shift=RIGHT * 0.2), run_time=0.5)
            bar322 = line_bar(p320.code, 2, TURN, 0.25)
            self.play(FadeIn(bar322), run_time=0.4)
            vo.wait_until("creates the deploy Lambda")
            self.play(FadeIn(lt33), FadeIn(pic33), run_time=0.5)
            self.play(FadeIn(lam, scale=0.6), run_time=0.3)
            self.play(lam.animate.move_to(sm_b.get_top() + UP * 0.38), run_time=0.8)
            vo.wait_until("upserts its definition")
            self.paint(p320, 6, "sm_pipeline.upsert(role_arn=role)", TOOL)
            self.add(bar322)                                     # paint() re-seats the panel over the bar
            self.play(GrowArrow(a_up), FadeIn(up_t), run_time=0.6)
            vo.wait_until("and starts it")
            self.paint(p320, 7, "sm_pipeline.start()", TOOL)
            self.add(bar322)
            self.play(GrowArrow(a_st), FadeIn(st_t), run_time=0.6)
            self.play(Indicate(sm_t, color=CLOUD, scale_factor=1.08), run_time=0.6)

        # ========================================================== 5. ponder: reverse the list
        lst = steps_list(size=22)
        lst.order = STEP_VARS
        at_tl(lst, 2.6)
        assert lst.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1, lst.get_right()
        graph = VGroup(*v.boxes, *v.edges.values())          # (v's own bounding box holds its anchor dot)
        dim = Rectangle(width=graph.width + 0.3, height=graph.height + 0.3, stroke_width=0)
        dim.set_fill(S.BG, 0.6).move_to(graph)
        assert dim.get_left()[0] > lst.get_right()[0] + 0.1, (dim.get_left(), lst.get_right())

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(bar322, p320, pic33, lam, a_up, a_st, up_t, st_t)), FadeOut(lt33), run_time=0.5)
            self.play(FadeIn(lst, shift=DOWN * 0.15), FadeIn(dim), run_time=0.6)
            vo.wait_until("Reverse the list")
            self.play(Indicate(lst, color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Does the run order change?")
            self.play(Indicate(VGroup(*lst.items), color=TURN, scale_factor=1.06), run_time=0.8)
            self.add(lst)
        card_p = ponder(self, PONDER_Q, seconds=8, center=(-1.85, -0.75), width=8.8)

        # ========================================================== 6. no: references set the order
        set_c = ok_chip("order = references · list = a set")
        set_c.move_to([LX + set_c.width / 2, 0.6, 0])
        assert set_c.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(card_p), FadeOut(dim), run_time=0.5)
            lst = self.shuffle(lst, tuple(reversed(STEP_VARS)))
            vo.wait_until("The order comes from")
            v.pulse(self)
            vo.wait_until("each input names")
            v.pulse(self)
            vo.wait_until("The list is a set")
            lst = self.shuffle(lst, ("step_create_model", "step_deploy_lambda", "step_collect", "step_train",
                                     "step_process"))
            self.play(FadeIn(set_c, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(set_c.text, color=OWN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 7. extra: the JSON, built offline
        lt30 = lref("30")
        t = term(P_SRC("workflow"), rows=15, size=SIZE)
        assert t.box.get_top()[1] < TRACK_BOTTOM - 0.02 and t.box.get_top()[1] < lt30.get_bottom()[1], t.box.get_top()
        cmd92 = cut(C92.cmd, n=t.max_chars - len(P_SRC("workflow")) - 1)
        lines92 = [(L92_30, S.GREY), "…", (NAMES92[0], TURN), (NAMES92[1], TURN), (L92_143A, ROUTE),
                   (L92_143B, ROUTE), (NAMES92[2], TURN), (NAMES92[3], TURN), (NAMES92[4], TURN), "…",
                   (L92_279, S.GREY)]
        sheet = json_sheet([s.strip() for s in NAMES92])
        at_tl(sheet, 2.6)
        yaml_s = card(["YAML", "(the lecture, slide 29)"], PAST, size=20, dashed=True)
        yaml_s.next_to(sheet, DOWN, buff=0.35).align_to(sheet, LEFT)
        assert sheet.get_right()[0] < min(b.get_left()[0] for b in v.boxes) - 0.1 and yaml_s.get_bottom()[1] > -3.55

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(lst), FadeOut(set_c), FadeOut(v), track(tr, 1, "built offline, not sent"), run_time=0.6)
            self.play(FadeIn(t), FadeIn(lt30), run_time=0.4)
            self.t = t
            self.bar(on_bar(t, extra_row("built offline, not sent")))
            type_cmd(self, t, cmd92, type_time=0.8)
            rows = out(self, t, lines92, wrap=True, run_time=1.0)
            self.reseat()
            vo.wait_until("the JSON definition")
            self.play(Indicate(VGroup(*[r for r in rows if r.text.startswith("[capture stub]")]), color=S.GREY,
                               scale_factor=1.03), run_time=0.6)
            self.reseat()
            vo.wait_until("Five steps")
            names = [r for r in rows if '"Name"' in r.text]
            assert len(names) == 5
            self.play(LaggedStart(*[Indicate(r, color=TURN, scale_factor=1.05) for r in names], lag_ratio=0.25),
                      run_time=1.2)
            self.reseat()
            suf = grey_chip("the SDK adds the suffix")
            pin(self, names[3], beside(suf, names[3]))
            vo.wait_until("each edge a get")
            gets = [r for r in rows if r.text in (L92_143A, L92_143B)]
            self.play(*[Indicate(r, color=ROUTE, scale_factor=1.04) for r in gets], run_time=0.8)
            self.reseat()
            vo.wait_until("Upsert sends this")
            self.play(FadeOut(t), *self.unbar_anims(), run_time=0.5)
            self.t = None
            self.play(FadeIn(v), run_time=0.5)
            self.play(TransformFromCopy(VGroup(*[b.frame for b in v.boxes]), sheet.frame),
                      FadeIn(sheet.body), FadeIn(sheet.title), run_time=1.0)
            self.add(v)
            self.play(FadeIn(yaml_s, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 8. slide 37: deploy splits in two
        lt37 = lref("37–38")
        ROW_DY = 0.9
        new_anchor = np.array([0.0, ROW_DY, 0.0])
        rx = [-5.2 + 2.6 * i for i in range(5)]
        ry = 0.6 + ROW_DY                     # the row's y while the code shows (first: 0.6)
        ry0 = 0.6
        nodes = [lecture_node("Data Collector"), lecture_node("Data Processor"), lecture_node("Model Training"),
                 lecture_node("Model Deploy", 2.6)]
        ny = 1.65
        for n_, x in zip(nodes, rx[:3] + [(rx[3] + rx[4]) / 2]):
            n_.move_to([x, ny, 0])
        n_arrows = [arrow(nodes[i].get_right(), nodes[i + 1].get_left(), S.GREY, stroke=2, buff=0.08)
                    for i in range(3)]
        splits = [DashedLine(nodes[3].get_bottom(), [rx[k], ry0 + 0.33, 0], color=S.GREY, stroke_width=2.5)
                  for k in (3, 4)]
        chain37 = VGroup(*nodes, *n_arrows)
        assert chain37.get_top()[1] < TRACK_BOTTOM - 0.02 and chain37.get_right()[0] < 6.6
        mcard = model_card_icon().move_to([rx[3], ry0 - 0.75, 0])
        lam8 = lambda_icon(0.5, text=None).move_to([rx[4], ry0 - 0.75, 0])
        lam8_up = [rx[4], ry - 0.75, 0]
        bchip = bridge_chip(6)
        bchip.move_to([6.45 - bchip.width / 2, -3.2, 0])
        pdml = at_tl(code(DML, 47, 57, font_size=20, dedent=True,
                          cuts={48: 'print("Updating Endpoint', 50: "EndpointName=endpoint_name,",
                                52: 'print(f"update_endpoint_response', 56: "EndpointName=endpoint_name,"}),
                     ry - 0.45)
        assert pdml.get_bottom()[1] > -3.55, pdml.get_bottom()
        plate = endpoint_plate(ENDPOINT_B, machine=None)
        plate.move_to([6.45 - plate.width / 2, 2.4, 0])
        cfg1 = file_card("cheese-app-endpoint-config-<time>", CLOUD)
        cfg2 = file_card("cheese-app-endpoint-config-<new time>", CLOUD)
        for c_ in (cfg1, cfg2):
            c_.next_to(plate, LEFT, buff=0.55)
        cfg_a = arrow(cfg2.get_right(), plate.get_left(), CLOUD, buff=0.08)
        assert cfg2.get_top()[1] < TRACK_BOTTOM - 0.05 and cfg2.get_left()[0] > -6.6, cfg2.get_corner(UL)
        assert pdml.get_right()[0] < lam8.get_left()[0] - 0.1, pdml.get_right()

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(sheet), FadeOut(yaml_s), FadeOut(lt30), track(tr, 1), run_time=0.5)
            v.ref.shift(-v.ref.get_center())                     # the row: y 0.6, centred
            v.relayout(self, "row", run_time=1.0)
            assert abs(v.boxes[0].frame.get_center()[1] - ry0) < 0.01 and v.boxes[4].get_right()[0] < 6.6
            assert chain37.get_bottom()[1] > v.boxes[0].get_top()[1] + 0.3
            self.play(FadeIn(lt37), LaggedStart(*[FadeIn(n_, shift=DOWN * 0.1) for n_ in nodes], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in n_arrows], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("Here, deploy splits")
            self.play(Indicate(nodes[3].text, color=TURN, scale_factor=1.1), run_time=0.5)
            self.play(*[Create(s) for s in splits], run_time=0.6)
            vo.wait_until("Create model makes")
            self.play(FadeIn(mcard, shift=UP * 0.1), Indicate(v.boxes[3].text, color=CLOUD, scale_factor=1.1),
                      run_time=0.6)
            v.heal(self)
            vo.wait_until("and a Lambda")
            self.play(FadeIn(lam8, scale=0.6), Indicate(v.boxes[4].text, color=CLOUD, scale_factor=1.1), run_time=0.6)
            v.heal(self)
            vo.wait_until("a small function")
            self.play(FadeIn(bchip, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("creates or updates")
            self.play(FadeOut(chain37), FadeOut(VGroup(*splits)), FadeOut(lt37), FadeOut(bchip), FadeOut(mcard),
                      run_time=0.4)
            v.ref.shift(new_anchor - v.ref.get_center())          # the row moves up to y 1.5
            v.relayout(self, "row", run_time=0.6)
            assert abs(v.boxes[0].frame.get_center()[1] - ry) < 0.01
            self.play(FadeIn(pdml, shift=UP * 0.2), FadeIn(plate), FadeIn(cfg1), GrowArrow(cfg_a),
                      lam8.animate.move_to(lam8_up), run_time=0.6)
            self.paint(pdml, 8, "sm_client.create_endpoint(", TURN, run_time=0.4)
            self.paint(pdml, 2, "sm_client.update_endpoint(", TURN, run_time=0.4)
            bars_dml = VGroup(line_bar(pdml.code, 2, TURN, 0.2), line_bar(pdml.code, 8, TURN, 0.2))
            self.play(FadeIn(bars_dml), run_time=0.3)
            self.play(FadeOut(cfg1, shift=UP * 0.3), FadeIn(cfg2, shift=UP * 0.3), run_time=0.5)
            self.play(Indicate(plate.text, color=CLOUD, scale_factor=1.06), run_time=0.5)

        # ========================================================== 9. the shared drawer
        ref1 = grey_chip("src/data-collector/cli.py:65", mono_font=True)
        ref2 = grey_chip("src/data-processor/cli.py:68", mono_font=True)
        note_c = two_line_chip("edges set the order ·", "files travel by name", ROUTE)
        note_c.move_to([6.45 - note_c.width / 2, 1.75, 0])

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(bars_dml, pdml, plate, cfg2, cfg_a, lam8)), run_time=0.5)
            v.ref.shift(np.array([0.0, 0.0, 0.0]) - v.ref.get_center())   # back to its own layout: row y 0.6
            v.relayout(self, "row", run_time=0.8)
            vo.wait_until("The edges set the order")
            v.pulse(self)
            v.drawer(self)
            assert v.bucket_g.get_bottom()[1] > -3.55
            vo.wait_until("but files also travel")
            v.files(self)
            VGroup(ref1, ref2).arrange(RIGHT, buff=0.3).next_to(v.bucket_g, DOWN, buff=0.15)
            assert VGroup(ref1, ref2).get_bottom()[1] > -3.58 and VGroup(ref1, ref2).get_right()[0] < 6.6, \
                VGroup(ref1, ref2).get_corner(DR)
            self.play(FadeIn(ref1, shift=UP * 0.1), FadeIn(ref2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("raw, clean and")
            self.play(LaggedStart(*[Indicate(f, color=INK, scale_factor=1.1) for f in v.files_g], lag_ratio=0.3),
                      run_time=1.0)
            v.heal(self)
            vo.wait_until("We could not check")
            v.unknown(self, 2, "? not verified here")
            self.play(Indicate(v.unknown_chip, color=INK, scale_factor=1.06), run_time=0.6)
            v.heal(self)
            vo.wait_until("how the training job")
            self.play(Indicate(v.boxes[2].text, color=TURN, scale_factor=1.1), run_time=0.6)
            v.heal(self)
            assert note_c.get_bottom()[1] > v.boxes[4].get_top()[1] + 0.1
            assert note_c.get_left()[0] > v.unknown_chip.get_right()[0] + 0.1, note_c.get_left()
            self.play(FadeIn(note_c, shift=DOWN * 0.1), run_time=0.5)
            v.pulse(self)

        # ========================================================== 10. step 1: --pipeline · step 2: console
        t = term(P_APP, rows=8, size=SIZE)
        keys_c = grey_chip("with keys: SageMaker Pipeline started: <ARN> · no output shown")
        err_card = card(["if upsert fails on the Lambda runtime: add", 'runtime="python3.12" to Lambda(...) (cli.py:297)',
                         "from the code, not run"], S.GREY, size=20)
        et = erratum_tag()
        keys_c.next_to(t.box, UP, buff=0.15).align_to(t.box, LEFT)
        err_card.next_to(keys_c, UP, buff=0.2).align_to(t.box, LEFT)
        et.next_to(err_card, RIGHT, buff=0.3).align_to(err_card, UP)
        assert err_card.get_top()[1] < TRACK_BOTTOM - 0.05 and et.get_right()[0] < 6.6, (err_card.get_top(), et.get_right())

        form = console_form("SageMaker Unified Studio › Build › ML Pipelines", [("note", "cheese-pipeline")],
                            form_w=12.7)
        form.move_to([0, 2.82 - form.height / 2, 0])
        form.frame.stretch_to_fit_height(2.82 + 3.5, about_edge=UP)
        g2 = ReferenceDAG(layout="column", names=CONSOLE_NAMES)
        top_c = form[1].get_center()[1] - 0.25 - 0.31          # under the console's separator line
        g2.shift(np.array([-3.0, top_c, 0]) - g2.p(2.5, 2.2))
        ill = illustration_tag("illustration · not run here")
        ill.move_to([form.frame.get_right()[0] - 0.2 - ill.width / 2, form.title_text.get_center()[1], 0])
        assert ill.get_left()[0] > form.title_text.get_right()[0] + 0.2, ill.get_left()
        assert g2.get_bottom()[1] > form.frame.get_bottom()[1] + 0.05 and form.frame.get_bottom()[1] > -3.58, \
            (g2.get_bottom(), form.frame.get_bottom())

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(v), FadeOut(VGroup(ref1, ref2, note_c)), track(tr, 1), run_time=0.6)
            self.play(FadeIn(t), run_time=0.4)
            self.t = t
            ln = type_cmd(self, t, T100, type_time=0.6)
            pin(self, ln, beside(turn_row(), ln))
            vo.wait_until("stops at the same line 32")
            out(self, t, [L90_108, L90_110, (L90_115, ERR), "…"] + [(s, ERR) for s in L90_153], wrap=True,
                run_time=0.6)
            self.reseat()
            vo.wait_until("With keys")
            self.play(FadeIn(keys_c, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("If instead upsert fails")
            self.play(FadeIn(err_card, shift=UP * 0.1), FadeIn(et), run_time=0.5)
            self.play(Indicate(err_card.body[1], color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Step 2:")
            self.play(FadeOut(VGroup(t, keys_c, err_card, et)), track(tr, 2), run_time=0.5)
            self.t = None
            self.play(FadeIn(form), FadeIn(ill), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in g2.boxes], lag_ratio=0.15), run_time=0.8)
            self.add(g2)
            for i in range(4):
                g2.edge(self, i, run_time=0.5)

        # ========================================================== 11. it runs (illustration)
        rerun = grey_chip("next run")
        rerun.next_to(g2.boxes[0].frame, RIGHT, buff=0.25)
        plate2 = endpoint_plate(ENDPOINT_B, machine=None)
        plate2.next_to(g2.boxes[4].frame, RIGHT, buff=0.55)
        creating = chip("Creating", SHARED, size=20).next_to(plate2, RIGHT, buff=0.2)
        wait_c = chip("wait for InService", TURN, size=20).next_to(creating, UP, buff=0.2).align_to(creating, LEFT)
        pa = arrow(g2.boxes[4].frame.get_right(), plate2.get_left(), CLOUD, buff=0.1)
        cost1 = cost_tag("each step's machine · a new Lambda per run")
        cost2 = cost_tag("cheese-app-endpoint (ml.m5.large) stays up")
        VGroup(cost1, cost2).arrange(DOWN, buff=0.15, aligned_edge=RIGHT)
        VGroup(cost1, cost2).move_to([6.2 - VGroup(cost1, cost2).width / 2, 0.15, 0])
        assert VGroup(cost1, cost2).get_top()[1] < rerun.get_bottom()[1] - 0.4
        assert wait_c.get_right()[0] < 6.5 and plate2.get_right()[0] < 6.5, (wait_c.get_right(), plate2.get_right())
        assert cost1.get_left()[0] > g2.boxes[2].get_right()[0] + 0.3, cost1.get_left()
        assert VGroup(cost1, cost2).get_bottom()[1] > plate2.get_top()[1] + 0.2

        with self.voiceover(SAY[11]) as vo:
            for i in range(4):
                g2.states(self, {i: "running"}, run_time=0.3)
                g2.states(self, {i: "succeeded"}, run_time=0.3)
            g2.states(self, {4: "running"}, run_time=0.3)
            vo.wait_until("caching skips")
            self.play(FadeIn(rerun, shift=LEFT * 0.1), run_time=0.4)
            a0 = g2.state(0, "cached", run_time=0.6)
            g2.boxes[0].badge.next_to(rerun, RIGHT, buff=0.15)      # beside 'next run', not over the edge
            self.play(a0)
            g2.heal(self)
            self.play(Indicate(g2.boxes[0].text, color=S.GREY, scale_factor=1.1), run_time=0.5)
            g2.heal(self)
            self.play(FadeIn(cost1, shift=LEFT * 0.1), run_time=0.5)          # what each run costs
            vo.wait_until("And a green deploy model")
            g2.states(self, {4: "succeeded"}, run_time=0.5)
            self.play(GrowArrow(pa), FadeIn(plate2), run_time=0.5)
            self.play(FadeIn(creating, shift=UP * 0.1), FadeIn(cost2, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("wait until the endpoint")
            self.play(FadeIn(wait_c, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(wait_c.text, color=TURN, scale_factor=1.08), run_time=0.6)
            self.play(Indicate(cost2.text, color=COST, scale_factor=1.04), run_time=0.6)

        # ========================================================== 12. step 3: each component's flag
        t = term(P_APP, rows=9, size=SIZE)
        each_c = card(["each flag: its own step, as a separate job",
                       "--model_deploy makes another endpoint (from the code, not run)",
                       "delete it before the next --pipeline, or DeployModel fails"], S.GREY, size=20)
        each_c.next_to(t.box, UP, buff=0.2).align_to(t.box, LEFT)
        assert each_c.get_top()[1] < TRACK_BOTTOM - 0.05 and each_c.get_right()[0] < 6.6, each_c.get_corner(UR)

        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(form, ill, g2, rerun, plate2, creating, wait_c, pa, cost1, cost2)),
                      track(tr, 3), run_time=0.6)
            self.play(FadeIn(t), run_time=0.4)
            self.t = t
            for k, (cmd, err) in enumerate(zip(FLAGS, ERRS)):
                ln = type_cmd(self, t, cmd, type_time=0.45)
                if k == 0:
                    pin(self, ln, beside(row_tag("shown in S14"), ln))
                out(self, t, [(err, ERR)], run_time=0.3)
                self.reseat()
                if k == 0:
                    vo.wait_until("Here, all four stop")
            vo.wait_until("With keys, model deploy")
            self.play(FadeIn(each_c, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(each_c.body[1], color=TURN, scale_factor=1.04), run_time=0.7)
            self.wait(0.6)

        self.play(FadeOut(VGroup(t, each_c, tr)), run_time=0.8)
        self.t = None
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def paint(self, panel, k: int, sub: str, color, run_time: float = 0.5):
        """PLAYS: colour `sub` on code line k of `panel` and re-seat the panel (split trap)."""
        self.play(code_span(panel.code, k, sub).animate.set_color(color), run_time=run_time)
        self.add(panel)

    def shuffle(self, old, order, size: float = 22, run_time: float = 1.2):
        """PLAYS: the steps=[…] list `old` becomes steps_list(order): each name flies to its new place,
        the punctuation cross-fades. Returns the new list (on the scene as one mobject)."""
        split = min((2, 3), key=lambda k: max(len(", ".join(order[:k])), len(", ".join(order[k:]))))
        new = steps_list(order, size=size, split=split)
        assert new.get_right()[0] - new.get_left()[0] < 8.8, (order, new.width)
        new.move_to(old.get_corner(UL), aligned_edge=UL)
        old_by = {it_name: it for it_name, it in zip(old.order, old.items)}
        new_by = {it_name: it for it_name, it in zip(order, new.items)}
        old_ids = {id(g) for it in old.items for g in it}
        new_ids = {id(g) for it in new.items for g in it}
        old_p = [g for ln in old.lines for g in ln.glyphs if id(g) not in old_ids]
        new_p = [g for ln in new.lines for g in ln.glyphs if id(g) not in new_ids]
        anims = [ReplacementTransform(old_by[n], new_by[n], path_arc=-0.6) for n in order]
        self.play(*anims, *[FadeOut(g) for g in old_p], *[FadeIn(g) for g in new_p], run_time=run_time)
        self.remove(old, *old.get_family(), *new.get_family())
        self.add(new)
        new.order = tuple(order)
        return new

    def bar(self, tg):
        """Show a title-bar tag (on_bar; left of the tags already there) and remember it."""
        if self.bar_tags:
            tg.next_to(self.bar_tags[-1], LEFT, buff=0.15)
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        if self.t is not None:
            self.add(self.t, *self.bar_tags)
