"""S06 · Registry, endpoint, deploy, predict (V5, slide 12's five steps).
Lecture: 10–17, 41.

Beats (script.md "## S06", one voiceover block each):
 0  LECTURE 12. V5: slide 12 redrawn (GREY CLI container, dashed BLUE GCP box with the bucket and
    the Vertex AI panel: Model Registry, Endpoints; tag `illustration`). The five PINK numbered
    steps write in as the SAY names them; the GREEN model/ folder lands in the bucket with step 3.
 1  LECTURE 13–14. V5 leaves. CODE(model-deployment/cli.py: 101–114) folded to 101–105, …,
    109–114 (12 rows, 20 pt); lines 102, 103, 104 light one by one as a `JPEG bytes` chip unfolds
    into decode → float → resize 224×224, then line 114 lights and "model" joins the chain. A GREY
    chip "the slides: tf.saved_model.save · the repo today: ExportArchive (lines 117–123)" writes in.
 2  LECTURE 12. V5 returns lower (steps put away), the folder in the bucket. Top: CODE(cli.py:
    189–190), the two arguments of `Model.upload`; the catalog card slides into Model Registry with
    its PINK pointer to the folder; 189 lights with "where the files are", 190 with "which
    container". The panel becomes PANEL(model-deployment/README.md: 65, excerpt "Nothing is running
    yet and it costs nothing."); "callable?" with a RED ✗ writes in.
 3  CODE(cli.py: 198–199) lit; the BLUE `cheese-app-endpoint` plate rises in Endpoints; a GREY chip
    "exists? reuse : create" lights "reuse", then "create".
 4  CODE(cli.py: 213–215): the machine slides under the plate (214), the GOLD meter appears; a PINK
    "100 % traffic" arrow into the plate (213); the meter ticks; 215 (min_replica_count=1) lights;
    the panel becomes PANEL(README.md: 66, excerpt "… starts at least one machine …").
 5  Close-up (tag `illustration`): V5 steps aside, its plate and machine move up. CODE(cli.py: 251)
    wrapped; a JPEG chip becomes the envelope {"bytes_inputs": {"b64": …}} and rides the PINK route
    to the plate; the signature chain unfolds under it; four BLUE bars rise (tag `README example`,
    model-deployment/README.md:211) and the tallest lights YELLOW "argmax".
 6  V5 returns. CODE(cli.py: 269–270): meter stops, the machine slides out (269), the plate goes
    (270); the registry card and the bucket folder flash: they stay.
 7  LECTURE 16–17. V5 leaves. CODE(ml-workflow/src/workflow/model.py: 88–103) folded to 88–92, …,
    95–97 with a GREY chip "the pipeline's deploy step: the same two calls"; 88–92 (upload) then
    95–97 (deploy) light. Two cards write in one at a time: "Vertex AI · serve the trained model" |
    "Cloud Run · the model is one part of a bigger app".
 8  LECTURE 41 (tag only). Everything fades. TAKEAWAY (two segments), each row flashes as the SAY
    reaches it; empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Dot,
    LaggedStart,
    Line,
    Arrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    MoveAlongPath,
    ReplacementTransform,
    VGroup,
)

from common import *  # noqa: F401,F403
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources
M = "model-deployment/cli.py"
MP = "ml-workflow/src/workflow/model.py"
assert source_line(M, 102).strip().startswith("decoded = tf.io.decode_jpeg("), source_line(M, 102)
assert "convert_image_dtype" in source_line(M, 103), source_line(M, 103)
assert "size=(224, 224)" in source_line(M, 104), source_line(M, 104)
assert source_line(M, 110).strip() == "def serving_function(bytes_inputs):", source_line(M, 110)
assert source_line(M, 114).strip() == "return prediction_model(images, training=False)", source_line(M, 114)
assert "ExportArchive()" in source_line(M, 120), source_line(M, 120)
assert "tf.saved_model.save()" in source_line(M, 117), source_line(M, 117)
assert source_line(M, 187).strip() == "model = aiplatform.Model.upload(", source_line(M, 187)
assert source_line(M, 189).strip() == "artifact_uri=ARTIFACT_URI,", source_line(M, 189)
assert source_line(M, 190).strip() == "serving_container_image_uri=serving_container_image_uri,", source_line(M, 190)
assert source_line(M, 198).strip() == "if endpoints:", source_line(M, 198)
assert source_line(M, 199).strip() == "endpoint = endpoints[0]", source_line(M, 199)
assert "aiplatform.Endpoint.create(display_name=ENDPOINT_NAME)" in source_line(M, 202), source_line(M, 202)
assert source_line(M, 213).strip() == "traffic_percentage=100,", source_line(M, 213)
assert source_line(M, 214).strip() == "machine_type=MACHINE_TYPE,", source_line(M, 214)
assert source_line(M, 215).strip() == "min_replica_count=1,", source_line(M, 215)
assert 'MACHINE_TYPE = "n1-standard-2"' in source_text(M)            # the machine glyph's label
assert '{"bytes_inputs": {"b64": base64.b64encode(image)' in source_line(M, 251), source_line(M, 251)
assert source_line(M, 269).strip() == "endpoint.undeploy_all()", source_line(M, 269)
assert source_line(M, 270).strip() == "endpoint.delete()", source_line(M, 270)
assert "aip.Model.upload(" in source_line(MP, 88), source_line(MP, 88)
assert "deployed_model.deploy(" in source_line(MP, 95), source_line(MP, 95)
assert "Nothing is running yet and it costs nothing." in source_line("model-deployment/README.md", 65)
assert "starts at least one machine" in source_line("model-deployment/README.md", 66)
assert "[[0.0591, 0.1099, 0.6348, 0.1962]]" in source_line("model-deployment/README.md", 211)
assert README_PROBS == (0.0591, 0.1099, 0.6348, 0.1962), README_PROBS
assert ENDPOINT_NAME == "cheese-app-endpoint", ENDPOINT_NAME

# ------------------------------------------------------------------ layout
SAFE_L, SAFE_R = -6.45, 6.45
TOP_Y = 3.05                     # under the lecture tag (its bottom is at 3.13)
TAG_LEFT = 3.4                   # a panel whose right edge stays left of this may rise to 3.5
V5_Y = -1.1                      # V5's centre while a panel sits above it (beats 2–6)


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


def top_slot(m):
    """Put a panel in the band above V5: left-aligned; as high as the lecture tag allows."""
    top = 3.5 if m.width + SAFE_L <= TAG_LEFT else TOP_Y
    return place(m, left=SAFE_L, top=top)


def flash(mob, color: str = TURN, k: float = 1.15, run_time: float = 0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def note_chip(text: str, color: str = S.GREY, width: float = 6.0, text_color: str = INK):
    """A GREY-outlined note: serif rows with `code` mono, wrapped to `width`. .frame .rows"""
    rows = fit_rows(text, width, CAPTION, text_color)
    fr = box(rows.width + 0.4, rows.height + 0.26, color, fill=S.BG, fill_opacity=0.9, radius=0.14)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


def side_card(title: str, text: str, color: str = CLOUD, width: float = 5.6):
    """One half of S06's Vertex AI | Cloud Run card: a bold title row over a serif row."""
    t = label(title, 22, color, weight="BOLD")
    body = fit_rows(text, width - 0.5, CAPTION, INK)
    rows = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    fr = box(width, rows.height + 0.4, color, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(fr, rows)
    g.frame, g.title, g.body = fr, t, body
    return g


class RegistryToEndpoint(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0 · slide 12's five steps
        lr = None
        re_ = RegistryEndpoint(show=("cli", "gcp", "bucket", "vertex"))
        itag = illustration_tag()
        place(itag, left=re_.cli_frame.get_left()[0], top=re_.get_top()[1] - 0.05)
        re_.add(itag)                          # moves and fades with the piece
        re_.shift(UP * (-0.3 - re_.get_center()[1]))
        inside(re_)
        guard(re_.get_top()[1] <= TOP_Y, "V5 under the lecture tag")
        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, lr, "12")
            self.play(FadeIn(re_), run_time=0.9)
            vo.wait_until("get the saved model")
            self.play(*re_.parts_in("step1"), run_time=0.5)
            vo.wait_until("update its signature")
            self.play(*re_.parts_in("step2"), run_time=0.5)
            vo.wait_until("upload it to a bucket")
            self.play(*re_.parts_in("step3"), run_time=0.5)
            self.play(*re_.parts_in("folder"), flash(re_.bucket, OWN, 1.06), run_time=0.6)
            vo.wait_until("register it")
            self.play(*re_.parts_in("step4"), flash(re_.reg_frame, INK, 1.03), run_time=0.6)
            vo.wait_until("and deploy it")
            self.play(*re_.parts_in("step5"), run_time=0.5)
            self.play(flash(re_.ep_frame, INK, 1.03), run_time=0.6)

        # ========================================================== 1 · the serving signature
        sig = src_panel(M, [(101, 105), (109, 114)], size=20)
        top_slot(sig)
        inside(sig)
        jpeg = chip("JPEG bytes", S.GREY, size=CAPTION, font=MONO)
        chain = signature_chain()
        arrow0 = label("→", CAPTION, S.GREY)
        row = VGroup(jpeg, arrow0, chain).arrange(RIGHT, buff=0.15)
        place(row, left=SAFE_L + 0.1, top=sig.get_bottom()[1] - 0.35)
        inside(row)
        apart(row, sig, 0.15, "signature chain vs panel")
        pieces = list(chain.submobjects)            # chip, →, chip, →, chip, →, chip
        assert len(pieces) == 7, len(pieces)
        export = note_chip("the slides: `tf.saved_model.save` · the repo today: `ExportArchive` (lines 117–123)",
                           width=12.2)
        place(export, left=SAFE_L + 0.1, top=row.get_bottom()[1] - 0.3)
        inside(export)
        apart(export, row, 0.15, "ExportArchive chip vs chain")
        bars1 = {n: sig.bar(n, TURN, 0.22) for n in (102, 103, 104, 114)}
        with self.voiceover(SAY[1]) as vo:
            lr = lref_swap(self, lr, "13–14")
            self.play(*re_.parts_out("step1", "step2", "step3", "step4", "step5"), run_time=0.4)
            self.play(FadeOut(re_, shift=DOWN * 0.3), FadeIn(sig, shift=DOWN * 0.2), run_time=0.8)
            self.play(FadeIn(jpeg, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("decode the JPEG")
            self.play(FadeIn(bars1[102]), FadeIn(arrow0), FadeIn(pieces[0], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("convert to floats")
            self.play(FadeIn(bars1[103]), FadeIn(pieces[1]), FadeIn(pieces[2], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("resize to 224")
            self.play(FadeIn(bars1[104]), FadeIn(pieces[3]), FadeIn(pieces[4], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("then call the model")
            self.play(FadeIn(bars1[114]), FadeIn(pieces[5]), FadeIn(pieces[6], shift=RIGHT * 0.2), run_time=0.6)
            self.play(flash(pieces[6], CLOUD, 1.1), run_time=0.6)
            vo.wait_until("The slides save it one way")
            self.play(FadeIn(export, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("the Keras export archive")
            self.play(flash(export.rows, INK, 1.04), run_time=0.7)

        # ========================================================== 2 · register: a catalog card
        re_.shift(UP * (V5_Y - re_.get_center()[1]))
        inside(re_)
        up = src_panel(M, 189, 190)
        top_slot(up)
        inside(up)
        apart(up, re_, 0.05, "upload panel vs V5")
        rm65 = readme_panel("model-deployment", 65, clip={65: ("Nothing is running", None)})
        top_slot(rm65)
        inside(rm65)
        apart(rm65, re_, 0.05, "README 65 vs V5")
        b189, b190 = up.bar(189, EDGE, 0.25), up.bar(190, EDGE, 0.25)
        card = re_.card
        with self.voiceover(SAY[2]) as vo:
            lr = lref_swap(self, lr, "12")
            self.play(FadeOut(VGroup(sig, *bars1.values(), row, export)), run_time=0.6)
            self.play(FadeIn(re_, shift=UP * 0.2), FadeIn(up, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("Registering creates")
            self.play(*re_.register(), run_time=0.8)
            vo.wait_until("where the files are")
            self.play(FadeIn(b189), flash(card.rows[0], EDGE, 1.06), flash(re_.folder, OWN, 1.1), run_time=0.7)
            vo.wait_until("which container serves")
            self.play(FadeIn(b190), flash(card.rows[1], EDGE, 1.06), run_time=0.7)
            vo.wait_until("Nothing is running")
            self.play(FadeOut(VGroup(up, b189, b190), shift=UP * 0.15), FadeIn(rm65, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Can you call it")
            self.play(*re_.parts_in("callable"), run_time=0.6)
            vo.wait_until("Not yet")
            self.play(flash(re_.parts["callable"], ERR, 1.15), run_time=0.6)

        # ========================================================== 3 · the endpoint: an address
        ep = src_panel(M, 198, 199)
        top_slot(ep)
        inside(ep)
        apart(ep, re_, 0.05, "endpoint panel vs V5")
        rc = mono("exists? reuse : create", 22, INK)
        rc_fr = box(rc.width + 0.4, rc.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        rc.move_to(rc_fr)
        rchip = VGroup(rc_fr, rc)
        place(rchip, left=ep.get_right()[0] + 0.4, cy=ep.code.get_center()[1])
        inside(rchip)
        guard(rchip.get_right()[0] <= TAG_LEFT or rchip.get_top()[1] <= TOP_Y, "reuse chip vs lecture tag")
        apart(rchip, re_, 0.05, "reuse chip vs V5")
        w_reuse = rc[rc.text.index("reuse"):rc.text.index("reuse") + 5]
        w_create = rc[rc.text.index("create"):rc.text.index("create") + 6]
        b198 = VGroup(ep.bar(198, TURN, 0.22), ep.bar(199, TURN, 0.22))
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(rm65, shift=UP * 0.15), FadeIn(ep, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("an address")
            self.play(*re_.create_endpoint(), run_time=0.8)
            vo.wait_until("The repo reuses")
            self.play(FadeIn(b198), FadeIn(rchip, shift=LEFT * 0.15), run_time=0.7)
            self.play(w_reuse.animate.set_color(OWN), flash(re_.plate, CLOUD, 1.06), run_time=0.7)
            vo.wait_until("or creates it")
            self.play(w_create.animate.set_color(OWN), w_reuse.animate.set_color(INK), run_time=0.6)
            self.play(flash(re_.plate.title, CLOUD, 1.08), run_time=0.6)

        # ========================================================== 4 · deploy: a machine, billed hourly
        dp = src_panel(M, 213, 215)
        top_slot(dp)
        inside(dp)
        apart(dp, re_, 0.05, "deploy panel vs V5")
        rm66 = readme_panel("model-deployment", 66, clip={66: ("starts at least one machine", None)},
                            hi={"This is the part that costs money.": COST})
        top_slot(rm66)
        inside(rm66)
        apart(rm66, re_, 0.05, "README 66 vs V5")
        b213, b214, b215 = (dp.bar(n, TURN, 0.22) for n in (213, 214, 215))
        plate = re_.plate
        t_end = plate.get_top() + UP * 0.04
        t_start = np.array([plate.get_right()[0] - 0.45, re_.reg_frame.get_bottom()[1] - 0.05, 0])
        traffic = Arrow(t_start, t_end, buff=0, color=EDGE, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        t_lbl = label("100 % traffic", CAPTION, EDGE)
        place(t_lbl, right=traffic.get_left()[0] - 0.12, cy=(t_start[1] + re_.ep_frame.get_top()[1]) / 2 + 0.05)
        apart(t_lbl, re_.parts["callable"], 0.03, "traffic label vs callable?")
        guard(t_lbl.get_bottom()[1] >= re_.ep_frame.get_top()[1] - 0.02, "traffic label inside the gap")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(ep, b198, rchip), shift=UP * 0.15), FadeIn(dp, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("slides a machine")
            self.play(*re_.deploy(), FadeIn(b214), run_time=0.9)
            vo.wait_until("all the traffic")
            self.play(GrowArrow(traffic), FadeIn(t_lbl), FadeIn(b213), run_time=0.7)
            vo.wait_until("From now on")
            self.play(re_.meter_run(1.6), flash(re_.machine, COST, 1.06, 1.0))
            vo.wait_until("while it is deployed")
            self.play(FadeIn(b215), run_time=0.5)
            vo.wait_until("even when nobody")
            self.play(FadeOut(VGroup(dp, b213, b214, b215), shift=UP * 0.15), FadeIn(rm66, shift=UP * 0.15),
                      run_time=0.7)
            self.play(re_.meter_stop(0.3), run_time=0.3)
            self.play(re_.meter_run(1.6))

        # ========================================================== 5 · predict, close up
        pr = src_panel(M, 251, wrap=True)
        top_slot(pr)
        inside(pr)
        itag5 = illustration_tag()
        place(itag5, left=pr.get_right()[0] + 0.35, cy=min(pr.code.get_center()[1], TOP_Y - 0.3))
        inside(itag5)
        guard(itag5.get_right()[0] <= TAG_LEFT or itag5.get_top()[1] <= TOP_Y, "illustration tag vs lecture tag")
        zplate = plate.copy()
        zmach = re_.machine.copy()
        zgrp = VGroup(zplate, zmach)
        zgrp_t = zgrp.copy()
        place(zgrp_t, right=SAFE_R - 0.1, top=pr.get_bottom()[1] - 0.4)
        env = envelope()
        place(env, left=SAFE_L + 0.1, cy=zgrp_t[0].get_center()[1])
        route = Arrow(env.get_right() + RIGHT * 0.08, zgrp_t[0].get_left() + LEFT * 0.08, buff=0, color=EDGE,
                      stroke_width=4)
        guard(route.get_length() >= 0.6, "the request route is too short")
        jpg = chip("JPEG", S.GREY, size=CAPTION, font=MONO).move_to(env)
        sc = signature_chain()
        place(sc, right=SAFE_R - 0.1, top=zgrp_t.get_bottom()[1] - 0.3)
        bars = ScoreBars(max_h=1.3)
        place(bars, right=SAFE_R - 0.3, bottom=-3.1)
        ex_tag = readme_example_tag()
        place(ex_tag, right=bars.get_left()[0] - 0.4, bottom=bars.get_bottom()[1] + 0.6)
        bars_room = VGroup(bars.copy(), label("argmax", CAPTION).next_to(bars.names, DOWN, buff=0.08))
        for m in (zgrp_t, env, sc, bars_room, ex_tag):
            inside(m)
        apart(zgrp_t, pr, 0.15, "plate vs panel")
        apart(env, pr, 0.15, "envelope vs panel")
        apart(sc, zgrp_t, 0.15, "chain vs plate")
        apart(sc, env, 0.1, "chain vs envelope")
        apart(bars, sc, 0.1, "bars vs chain")
        apart(ex_tag, bars, 0.2, "tag vs bars")
        b251 = pr.bar(251, EDGE, 0.22)
        b64 = env.text[env.text.text.index('"bytes_inputs"'):env.text.text.index('"bytes_inputs"') + 14]
        with self.voiceover(SAY[5]) as vo:
            self.add(zgrp)
            self.play(FadeOut(re_), FadeOut(VGroup(traffic, t_lbl)), FadeOut(rm66, shift=UP * 0.15), run_time=0.6)
            self.play(zgrp.animate.move_to(zgrp_t), FadeIn(pr, shift=DOWN * 0.15), FadeIn(itag5), run_time=0.9)
            vo.wait_until("wraps each JPEG")
            self.play(FadeIn(jpg, scale=0.8), run_time=0.4)
            self.play(ReplacementTransform(jpg, env), FadeIn(b251), run_time=0.8)
            vo.wait_until("under the key")
            self.play(flash(b64, EDGE, 1.1), flash(pr.span(251, '"bytes_inputs"'), EDGE, 1.1), run_time=0.7)
            self.play(GrowArrow(route), run_time=0.6)
            dot = Dot(radius=0.11, color=EDGE).move_to(route.get_start())
            self.play(FadeIn(dot, scale=0.5), run_time=0.2)
            self.play(MoveAlongPath(dot, Line(route.get_start(), route.get_end())), run_time=0.7)
            self.play(FadeOut(dot), flash(zplate, EDGE, 1.06), run_time=0.4)
            vo.wait_until("The signature unfolds")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in sc], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("four scores")
            self.play(FadeIn(bars.base), FadeIn(bars.names), FadeIn(ex_tag),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars.bars], lag_ratio=0.15),
                      run_time=1.0)
            self.play(FadeIn(bars.nums), run_time=0.4)
            vo.wait_until("the largest")
            self.play(*bars.argmax(), run_time=0.7)

        # ========================================================== 6 · cleanup
        cl = src_panel(M, 269, 270)
        top_slot(cl)
        inside(cl)
        apart(cl, re_, 0.05, "cleanup panel vs V5")
        b269, b270 = cl.bar(269, TURN, 0.22), cl.bar(270, TURN, 0.22)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pr, b251, itag5, env, route, sc, bars, ex_tag)), FadeOut(zgrp), run_time=0.6)
            self.play(FadeIn(re_), FadeIn(VGroup(traffic, t_lbl)), FadeIn(cl, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("undeploys the model")
            anims = re_.cleanup()                   # [machine out, meter out, plate out]
            assert len(anims) == 3, len(anims)
            self.play(FadeIn(b269), re_.meter_stop(0.6), run_time=0.6)
            self.play(anims[0], anims[1], FadeOut(VGroup(traffic, t_lbl)), run_time=0.8)
            vo.wait_until("then deletes the endpoint")
            self.play(FadeIn(b270), anims[2], run_time=0.8)
            vo.wait_until("The registry card")
            self.play(flash(card, OWN, 1.05), run_time=0.7)
            vo.wait_until("and the bucket files")
            self.play(flash(re_.folder, OWN, 1.15), run_time=0.7)

        # ========================================================== 7 · the pipeline's step; Vertex AI or Cloud Run
        mp = src_panel(MP, [(88, 92), (95, 97)])
        top_slot(mp)
        inside(mp)
        same = note_chip("the pipeline's deploy step: the same two calls", width=8.0)
        place(same, left=SAFE_L + 0.1, top=mp.get_bottom()[1] - 0.2)
        inside(same)
        up_bars = VGroup(*[mp.bar(n, TURN, 0.22) for n in range(88, 93)])
        dp_bars = VGroup(*[mp.bar(n, TURN, 0.22) for n in range(95, 98)])
        vx = side_card("Vertex AI", "serve the trained model", CLOUD, 5.0)
        cr = side_card("Cloud Run", "the model is one part of a bigger app", CLOUD, 7.1)
        halves = VGroup(vx, cr).arrange(RIGHT, buff=0.25)
        place(halves, left=SAFE_L + 0.1, bottom=-3.5)
        for m in (same, halves):
            inside(m)
        apart(halves, same, 0.15, "cards vs chip")
        with self.voiceover(SAY[7]) as vo:
            lr = lref_swap(self, lr, "16–17")
            self.play(FadeOut(VGroup(cl, b269, b270)), FadeOut(re_), run_time=0.6)
            self.play(FadeIn(mp, shift=DOWN * 0.15), run_time=0.7)
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the same two calls")
            self.play(FadeIn(up_bars), flash(mp.span(88, "Model.upload"), TURN, 1.1), run_time=0.7)
            self.play(FadeIn(dp_bars), flash(mp.span(95, "deploy"), TURN, 1.1), run_time=0.7)
            vo.wait_until("rule of thumb")
            self.play(FadeIn(vx, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Cloud Run fits")
            self.play(FadeIn(cr, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("one part of a bigger app")
            self.play(flash(cr.body, INK, 1.04), run_time=0.7)

        # ========================================================== 8 · takeaway
        tk = takeaway("registered → not callable until deployed to an endpoint · "
                      "deployed → a machine billing until you undeploy (then delete the endpoint)")
        inside(tk)
        with self.voiceover(SAY[8]) as vo:
            lr = lref_swap(self, lr, "41")
            self.play(FadeOut(VGroup(mp, up_bars, dp_bars, same, halves)), run_time=0.6)
            self.play(*tk.write(), run_time=1.4)
            vo.wait_until("If the question says registered")
            self.play(flash(tk.rows[0], TURN, 1.04), run_time=0.6)
            vo.wait_until("If it says deployed")
            self.play(flash(tk.rows[1], TURN, 1.04), run_time=0.6)
            vo.wait_until("Then delete the endpoint")
            self.play(flash(tk.rows[-1], TURN, 1.04), run_time=0.6)
        self.play(FadeOut(tk), FadeOut(lr), run_time=0.6)
        self.wait(0.3)
