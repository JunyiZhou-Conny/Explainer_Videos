"""S16 · Destroy, audit, recap (AC215 L22, the full follow-along). TRACKER [C] 8 in beats 0-2 (· extra
while c23 is on screen, · extra · our spelling while the audit card is); no tracker from beat 3 on.
Lecture tags: 22 · 40 (beat 0), 22 · 44 (beats 1-2), 22 · 15 (beat 3), 22 · 43 (beat 4). Ends part 2
on an empty frame.

Beats (script.md "## S16", one voiceover block each):
0. TRACKER [C] 8, LECTURE 22 · 40. An 8-row toolbox terminal at …:/app/deploy_k8s# types `pulumi destroy
   --stack dev --refresh -y` -> TERM(b50: 2) RED. On "Ours has nothing real": TRACKER [C] 8 · extra, the
   same command again (GREY 'extra' on the title bar) -> TERM(c23: 20–22); '- 1 deleted' flashes, then
   the line naming it (pulumi:pulumi:Stack deploy-k8s-dev: the stack's own record). On
   "yours deletes": the terminal shrinks to a 3-row strip (c23:20–22 kept); above it V6 stands full
   (every group solid, GREY 'illustration' tag in its free slot left of row B) with a GOLD meter under
   that tag. On "from the
   Ingress" V6 empties in reverse (ingress → app → storage → identity → provider → cluster + pool →
   network) while the meter winds down to zero.
1. LECTURE 22 · 44. Terminal and meter leave; TRACKER [C] 8 · extra · our spelling. A GOLD audit card
   (tag 'extra · our spelling', no output) types its four lines one per phrase: `gcloud container
   clusters list`, `gcloud compute forwarding-rules list`, `gcloud compute disks list`, `gcloud compute
   firewall-rules list`. On "Those are deleted in the background": three ghost icons blink under the
   empty tree (forwarding rule, pvc-… disk, registry images with the GOLD padlock 'retain_on_delete')
   and the GREY two-row chip "destroy failed: 'resource is in use'? / delete these, then destroy
   again"; on "look for disks named pvc" the GREY chip "look for pvc-… disks" and the ghost disk flashes.
2. LECTURE (held). The audit card and chips leave; TRACKER [C] 8. The padlock glows GOLD, a GREY chip
   "Artifact Registry › cheese-app-repository › delete images" under the ghost row; a GREY-dashed
   'L20 · one VM' icon blinks bottom left; the GOLD "Don't forget to delete" card and a YELLOW
   '▶ your turn' on "Pause and check".
3. No tracker. LECTURE 22 · 15. The AsksChecklist comes back small in the corner, every item ticked,
   and grows to full size; each row's one-liner becomes what did that job (GREEN), one per phrase.
4. LECTURE 22 · 43. The checklist shrinks back into the corner. Five lines, one per phrase, on the
   left; for each, a text-free thumbnail of its scene's picture (V6 tree, V8 shelf, nodes + a dashed
   new node, V4 ring with a Pod, three image crates) sends a copy into its GREY scene chip.
5. Clear. 'Test yourself · 1/5' (YELLOW) with question 1; on "Why does get all" the card becomes 2/5.
6. Card 3/5 on "How does the web Service", 4/5 on "Trace one click".
7. Card 5/5 on "Why can the frontend"; on "Answers are in" the card goes and the progress dots become
   the GREY pointer card 'answers: exercises.md · study guide (MLOps_Learning)'.
8. The pointer leaves; the GREY-dashed roadmap chip slides in: 'L23 · cheese-app-v4 · the two pulumi
   up runs from GitHub Actions, on every merge'. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the two commands and their outputs need 8 rows, so the terminal starts 8 rows tall and
  shrinks to a 3-row strip (keeping c23:20–22) before V6 appears above it; V6 is drawn already full
  (the state S12 left it in) instead of being built again. The meter is the GOLD CostDial (no digits)
  under V6's free slot left of row B, where the GREY 'illustration' tag sits (top centre is taken
  by the tracker's long '· extra · our spelling' caption in beat 1). V6 sits 0.3 higher than in S12
  so its ghost row clears the audit card's tag.
- Beat 0: V6's seven groups stand for the SHOW's chain (Ingress and nginx-f5 = 'ingress', the app
  objects = 'app' + 'storage', the namespace = 'identity', node pool + cluster = 'cluster + pool', NAT
  and VPC = 'network'); the PURPLE provider group empties between identity and cluster.
- Beat 1: the 'destroy failed' chip breaks over two rows (one row would be ~10 units wide) and reads
  "destroy failed: 'resource is in use'? / delete these, then destroy again".
- Beat 3: RecapAsks (below) builds the full card wide enough for the GREEN answers; common.py's
  AsksChecklist keeps the frame of the old one-liners and 'cloud LB · nginx Ingress · Services' ran
  past its edge (requested as a shared fix). Each answer flashes again on its second clause (Load balancing on
  'nginx and the Services').
- Beat 1: the audit card's tag is re-added above the card after typing (the card's opaque frame,
  re-seated, would hide it).
- Beat 3: the returning checklist starts with the notes S07 (Failover) and S13 (Load balancing) left
  on the grown card, so only the GREEN answers animate (Scaling keeps the stock note: S15 ticks it on
  the small card, solid plus the dashed half tick, which it keeps here).
- Beat 4: thumbnails are text-free glyphs (text never shrinks below 20 pt), and the 'TransformFromCopy'
  is a copy of the thumbnail riding on an arc into the chip's place while the chip fades in (a point morph from
  shapes into text would draw the chip's words tiny mid-way).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S16"]
assert len(SAY) == SAY_COUNT["S16"] == 9, len(SAY)

# ------------------------------------------------------------------ the real sources (checked)
B50, C23 = capture("b50"), capture("c23")
CMD = "pulumi destroy --stack dev --refresh -y"
assert B50.cmd == CMD == C23.cmd == readme(511).strip(), (B50.cmd, C23.cmd, readme(511))
assert B50.line(2).startswith("error: PULUMI_ACCESS_TOKEN must be set"), B50.line(2)
assert C23.line(21) == "Resources:" and C23.line(22).strip() == "- 1 deleted", (C23.line(21), C23.line(22))

P_K8S = toolbox_prompt("/app/deploy_k8s")
AUDIT = ("gcloud container clusters list", "gcloud compute forwarding-rules list",
         "gcloud compute disks list", "gcloud compute firewall-rules list")
S07_NOTE = "a restart, not a hot standby · keep replicas: 2"    # Failover's note, ticked in S07
S13_NOTE = "cloud LB at the door · nginx · Services across Pods"  # Load balancing's note, ticked in S13
EMPTY_ORDER = ("ingress", "app", "storage", "identity", "provider", "cluster", "network")

# Slide 43's five payoffs, each tied to where it was shown: (key word, rest, chip, thumbnail kind)
PAYOFFS = (("Self-service", "one pulumi up", "pulumi up", "tree"),
           ("Lower cost", "packing by requests", "scaling", "shelf"),
           ("Automatic adjustment", "node autoscaler", "scaling", "nodes"),
           ("Smooth running", "self-healing", "part 1", "ring"),
           ("Simpler development", "L20's images", "lecture 20", "crates"))

# Test-yourself cards: one row per clause; (s, 'm') = mono
QUESTIONS = (
    (("Which control-plane part decides where a new Pod runs,",),
     ("and which notices that a Pod died?",)),
    (("Why does", ("kubectl get all", "m"), "show only", ("service/kubernetes", "m"), ","),
     ("and what flag fixes it?",)),
    (("How does the", ("web", "m"), "Service know which Pods are its own,"),
     ("and why does the API reach Chroma at", ("vector-db:8000", "m"), "?")),
    (("Trace one click from", ("<IP>.sslip.io", "m"), "to the API Pod."),
     ("Why does the bare IP answer 404?",)),
    (("Why can the frontend scale to 3 but the API cannot,",),
     ("and what does the autoscaler add?",)),
)
Q_W = 12.0


def parts_row(*parts, size: float = 20, base=INK) -> VGroup:
    """A row of pieces: str -> label; (s, 'm') -> mono; (s, colour) -> label in that colour; a mobject
    is used as it is. Punctuation hugs the piece before it."""
    ms = []
    for p in parts:
        if isinstance(p, VMobject):
            ms.append(p)
        elif isinstance(p, str):
            ms.append(label(p, size, base))
        elif p[1] == "m":
            ms.append(mono(p[0], size, base))
        else:
            ms.append(label(p[0], size, p[1]))
    g = VGroup(*ms)
    for a, b in zip(ms, ms[1:]):
        punct = isinstance(b, Text) and b.original_text[:1] in ",:;?."
        b.next_to(a, RIGHT, buff=0.04 if punct else 0.14)
        if punct:
            b.align_to(a, DOWN)
        else:
            b.set_y(ms[0].get_y())
    return g


def qcard(rows_spec, size: float = 26) -> VGroup:
    """A YELLOW question card with mono spans. .frame .body"""
    rows = VGroup(*[parts_row(*r, size=size) for r in rows_spec]).arrange(DOWN, buff=0.2)
    frame = RoundedRectangle(width=Q_W, height=rows.height + 0.7, corner_radius=0.16, stroke_color=TURN,
                             stroke_width=3).set_fill(S.BG, 1)
    rows.move_to(frame)
    assert rows.width < Q_W - 0.5, rows.width
    g = VGroup(frame, rows)
    g.frame, g.body = frame, rows
    return g


def edge_tag(panel, tg, buff: float = 0.2):
    """Put tag tg on the top edge of a card/panel, at its right end."""
    fr = panel.frame
    return tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - buff, 0, 0]))


def typing(row, run_time: float = 0.8):
    """ANIM: a mono row appears glyph by glyph (typed into a card)."""
    return LaggedStart(*[FadeIn(g) for g in row.glyphs], lag_ratio=1.0, run_time=run_time)


class FullTree(ResourceTree):
    """V6 drawn already full (the state S12 left it in): every group solid, arrows in place."""

    def built_full(self):
        for key in ("network", "cluster", "provider", "identity", "storage", "app", "ingress"):
            g = self._group_mob(key, "full")
            for a, b in self.EDGES:
                if b == key and a in self.groups:
                    ar = arrow(self.groups[a].box.get_center(), g.box.get_center(), S.GREY, stroke=3, buff=0)
                    ar.put_start_and_end_on(self._edge_pt(self.groups[a], g), self._edge_pt(g, self.groups[a]))
                    self.arrows[(a, b)] = ar
                    self.add(ar)
            self.groups[key] = g
            self.filled[key] = set(self.spec[key][3])
            self.add(g)
        return self


def thumb(kind: str) -> VGroup:
    """A text-free thumbnail (about 1.0 x 0.6) of a scene's picture."""
    if kind == "tree":                       # V6: two rows of group boxes
        cols = (CLOUD, CLOUD, TOOL, OWN)
        top = VGroup(*[frame_box(0.2, 0.13, c, k=0.45, stroke=2, radius=0.03) for c in cols]).arrange(RIGHT, buff=0.06)
        bot = VGroup(*[frame_box(0.2, 0.13, OWN, k=0.45, stroke=2, radius=0.03) for _ in range(3)]).arrange(RIGHT, buff=0.06)
        bot.next_to(top, DOWN, buff=0.16).align_to(top, RIGHT)
        return VGroup(top, bot)
    if kind == "shelf":                      # V8: a node shelf packed with request blocks
        shelf = frame_box(1.0, 0.5, NODE, k=0.08, stroke=2, radius=0.05)
        blocks = VGroup(frame_box(0.34, 0.36, POD, k=0.5, stroke=2, radius=0.03),
                        frame_box(0.2, 0.36, POD, k=0.5, stroke=2, radius=0.03),
                        frame_box(0.2, 0.36, POD, k=0.5, stroke=2, radius=0.03)).arrange(RIGHT, buff=0.04)
        blocks.move_to(shelf).align_to(shelf, LEFT).shift(RIGHT * 0.06)
        return VGroup(shelf, blocks)
    if kind == "nodes":                      # the autoscaler: one node, then a second (dashed, arriving)
        n1 = frame_box(0.42, 0.42, NODE, k=0.3, stroke=2, radius=0.05)
        n2 = frame_box(0.42, 0.42, NODE, k=0.06, stroke=2, radius=0.05, dashed=True)
        return VGroup(n1, n2).arrange(RIGHT, buff=0.14)
    if kind == "ring":                       # V4: the controller's loop around a Pod
        ring_ = ring_arrows(0.28, TURN, stroke=3)
        pod = Circle(radius=0.12, stroke_color=POD, stroke_width=3).set_fill(tint(POD, 0.4), 1)
        return VGroup(ring_, pod)
    if kind == "crates":                     # S10: the same images as L20
        return VGroup(*[frame_box(0.28, 0.24, IMAGE, k=0.35, stroke=2, radius=0.03) for _ in range(3)]).arrange(RIGHT, buff=0.06)
    raise ValueError(kind)


class RecapAsks(AsksChecklist):
    """The AsksChecklist whose full card is built wide enough for ASK_ANSWERS from the start (in
    common.py the frame keeps the width of the old one-liners, and 'cloud LB · nginx Ingress ·
    Services' runs past its right edge)."""

    def _build(self, small: bool, center=None) -> VGroup:
        card_ = super()._build(small, center)
        if small:
            return card_
        saved = dict(self.notes)
        self.notes = {i: (ASK_ANSWERS[i], OWN) for i in range(3)}
        wide = super()._build(small, center)
        self.notes = saved
        if wide.frame.width > card_.frame.width:
            card_[1].align_to(wide[1], LEFT)
            card_.submobjects[0] = wide.frame
            card_.frame = wide.frame
        return card_


def text_span(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text (Text keeps no glyphs for spaces)."""
    flat = t.original_text.replace(" ", "")
    i = flat.index(sub.replace(" ", ""))
    assert len(flat) == len(t.submobjects), (len(flat), len(t.submobjects))
    return VGroup(*t.submobjects[i:i + len(sub.replace(" ", ""))])


def vm_icon() -> VGroup:
    """L20's VM as a small GREY-dashed memory icon. .frame .text"""
    return boxed(["L20 · one VM", "if it still runs"], PAST, dashed=True, k=0.05)


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 9

        # ========================================================== 0. destroy: README, then local; V6 empties
        trk = tracker_c(8)
        r40 = lref("40")
        t = toolbox_term(8, "/app/deploy_k8s")
        assert t.box.get_top()[1] < TRACK_BOTTOM - 0.3, t.box.get_top()
        rt = FullTree()
        rt.shift(UP * 0.3)                      # room under it for the ghost row above the audit card's tag
        rt.built_full()
        assert rt.get_top()[1] < PIC_TOP, rt.get_top()
        # the illustration tag sits in V6's free slot left of row B (top centre is taken by the tracker's
        # long '· extra · our spelling' caption in beat 1); the meter sits under it, above the strip
        ill = illustration_tag().move_to(rt.p(-4.9, 0.75))
        assert ill.get_right()[0] < rt.groups["identity"].box.get_left()[0] - 0.2
        dial = CostDial(0.36, "the meter").move_to(rt.p(-4.9, -0.45))
        assert dial.get_top()[1] < ill.get_bottom()[1] - 0.1, (dial.get_top(), ill.get_bottom())
        dial.tracker.set_value(0.62)
        xr = extra_row()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(r40), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("pulumi destroy, stack dev")
            type_capture(self, t, B50, type_time=0.8)
            e50 = out(self, t, [(B50.line(2), ERR)], wrap=True, run_time=0.3)
            self.play(Indicate(substring(e50[0], "PULUMI_ACCESS_TOKEN"), color=ERR, scale_factor=1.1), run_time=0.6)
            self.add(t)
            vo.wait_until("Ours has nothing real")
            self.play(track(trk, 8, True), run_time=0.3)
            type_capture(self, t, C23, type_time=0.6)
            on_bar(t, xr)
            self.play(FadeIn(xr), run_time=0.3)
            # line 20 names the one deleted resource: the stack's own record (QA 28:08)
            res = out(self, t, [C23.line(20), C23.line(21), C23.line(22)], run_time=0.3)
            self.play(Indicate(substring(res[2], "- 1 deleted"), color=TURN, scale_factor=1.12), run_time=0.6)
            self.play(Indicate(substring(res[0], "pulumi:pulumi:Stack deploy-k8s-dev"), color=TURN,
                               scale_factor=1.06), run_time=0.6)
            self.add(t)
            vo.wait_until("yours deletes what this stack created")
            self.play(FadeOut(xr), run_time=0.2)
            self.remove(xr)
            resize(self, t, 3, keep=list(res), run_time=0.5)
            on_bar(t, xr)
            assert t.box.get_top()[1] < dial.get_bottom()[1] - 0.1, (t.box.get_top(), dial.get_bottom())
            self.play(FadeIn(rt), FadeIn(ill), FadeIn(dial), FadeIn(xr), run_time=0.6)
            vo.wait_until("from the Ingress down to the network")
            self.add(dial.tracker)
            dial.tracker.add_updater(lambda m, dt: m.set_value(max(0.0, m.get_value() - dt * 0.2)))
            rt.empty(self, lag=0.38)
            dial.tracker.clear_updaters()
            self.play(dial.tracker.animate.set_value(0.0), run_time=0.3)
            self.remove(dial.tracker)
        dial.freeze()

        # ========================================================== 1. audit: what may survive
        r44 = lref("44")
        rows = [mono_line(s, 20, INK) for s in AUDIT]
        audit = card(rows, COST, size=20, head="what may survive · check", buff=0.14)
        audit.move_to([0, 0, 0]).align_to([-6.3, 0, 0], LEFT).align_to([0, -3.45, 0], DOWN)
        a_tag = edge_tag(audit, extra_tag("our spelling"))
        pvc = grey_chip("look for pvc-… disks")
        busy = two_row_chip("destroy failed: 'resource is in use'?", "delete these, then destroy again", S.GREY)
        side = VGroup(pvc, busy).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        side.move_to([0, audit.get_center()[1], 0]).align_to([audit.get_right()[0] + 0.45, 0, 0], LEFT)
        assert side.get_right()[0] < 6.5, side.get_right()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(t, xr, dial)), FadeOut(r40), FadeIn(r44), track(trk, 8, "our spelling"),
                      run_time=0.5)
            self.remove(t, xr, dial)
            self.play(FadeIn(audit.frame), FadeIn(audit.head), FadeIn(a_tag), run_time=0.4)
            vo.wait_until("list clusters")
            for r, cue in zip(rows, ("list clusters", "forwarding rules", "disks and", "firewall rules")):
                vo.wait_until(cue)
                self.play(typing(r, 0.6))
            self.add(audit, a_tag)                  # the tag stays on top of the card's opaque frame
            vo.wait_until("Those are deleted in the background")
            rt.ghosts(self)
            assert rt.ghost_g.get_bottom()[1] > a_tag.get_top()[1] + 0.1, (rt.ghost_g.get_bottom(), a_tag.get_top())
            assert rt.ghost_g.get_top()[1] < rt.groups["identity"].box.get_bottom()[1] - 0.15
            self.play(FadeIn(busy, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("look for disks named pvc")
            self.play(FadeIn(pvc, shift=LEFT * 0.15), Indicate(rt.ghost_g[1], color=CLOUD, scale_factor=1.15),
                      Indicate(substring(rows[2], "disks"), color=TURN, scale_factor=1.15), run_time=0.8)
            rt.heal(self)
            self.add(audit, a_tag)

        # ========================================================== 2. registry images, L20's VM, don't forget
        lock = rt.ghost_g[2][1]
        reg = grey_chip("Artifact Registry › cheese-app-repository › delete images")
        reg.next_to(rt.ghost_g, DOWN, buff=0.35)
        keep_inside(reg)
        dfc = dont_forget_card().move_to([0.9, -2.55, 0])
        vm = vm_icon().move_to([-4.75, -2.55, 0])
        yt = your_turn().next_to(dfc, RIGHT, buff=0.3)
        assert yt.get_right()[0] < 6.5 and vm.get_right()[0] < dfc.get_left()[0] - 0.3
        assert reg.get_bottom()[1] > dfc.get_top()[1] + 0.15, (reg.get_bottom(), dfc.get_top())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(audit, a_tag, side)), track(trk, 8), run_time=0.5)
            self.remove(audit, a_tag, side)
            glow = Circle(radius=0.45, stroke_color=COST, stroke_width=6).move_to(lock.glyph)
            self.play(Indicate(lock.glyph, color=COST, scale_factor=1.35),
                      Create(glow, rate_func=there_and_back), run_time=1.0)
            self.remove(glow)
            rt.heal(self)
            self.play(FadeIn(reg, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("delete them in the console")
            self.play(Indicate(reg.text, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Delete the lecture 20 machine")
            self.play(FadeIn(vm, shift=RIGHT * 0.15), run_time=0.4)
            self.play(vm.animate(rate_func=there_and_back).set_opacity(0.3), run_time=0.6)
            self.play(vm.animate(rate_func=there_and_back).set_opacity(0.3), run_time=0.6)
            self.play(FadeIn(dfc, scale=1.08), run_time=0.5)
            vo.wait_until("Pause and check")
            self.play(FadeIn(yt, shift=LEFT * 0.15), Indicate(dfc.title, color=COST, scale_factor=1.06), run_time=0.6)
            flash_tag(self, yt, TURN)

        # ========================================================== 3. back to the three asks
        r15 = lref("15")
        # the notes S07 and S13 left on the grown card (Scaling's stays stock: S15 ticks it on the small card)
        ac = RecapAsks(small=True, ticked=(0, 1, 2), notes={0: S07_NOTE, 1: S13_NOTE})
        ac.ticks[2] = "both"                    # S15 left Scaling with the solid tick and the dashed half tick
        ac.remove(ac.card)
        ac.card = ac._build(True)
        ac.add(ac.card)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(rt, ill, reg, dfc, vm, yt, trk, r44)), run_time=0.6)
            self.remove(rt, ill, reg, dfc, vm, yt, trk, r44)
            self.play(FadeIn(r15), FadeIn(ac), run_time=0.5)
            ac.grow(self, center=(0, 0.0))
            for i, (cue, more) in enumerate((("Failover", "and node auto repair"),
                                             ("Load balancing", "nginx and the Services"),
                                             ("Scaling", "and kubectl scale in your hands"))):
                vo.wait_until(cue)
                ac.light(self, i, run_time=0.5)
                ac.answer(self, i)
                assert ac.card.rows[i].note.get_right()[0] < ac.card.frame.get_right()[0] - 0.15, i
                if more:
                    vo.wait_until(more)
                    self.play(Indicate(ac.card.rows[i].note, color=OWN, scale_factor=1.06), run_time=0.7)
                    ac.heal(self)

        # ========================================================== 4. slide 43: five payoffs
        r43 = lref("43")
        lines, thumbs, chips = [], [], []
        for k, (word, rest, sc, kind) in enumerate(PAYOFFS):
            th = thumb(kind)
            th.move_to([-5.75, 2.1 - k * 1.1, 0])
            txt = label(f"{word} · {rest}", 26, INK, t2c={f"· {rest}": S.GREY})   # one Text: one baseline
            txt.move_to([0, th.get_y(), 0]).align_to([-4.85, 0, 0], LEFT)
            assert txt.get_left()[0] > th.get_right()[0] + 0.2, k
            ch = scene_chip(sc).next_to(txt, RIGHT, buff=0.35)
            lines.append(txt)
            thumbs.append(th)
            chips.append(ch)
        allp = VGroup(*thumbs, *lines, *chips)
        assert allp.get_left()[0] > -6.5 and allp.get_bottom()[1] > -3.45, (allp.get_left(), allp.get_bottom())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(r15), FadeIn(r43), run_time=0.4)
            ac.shrink(self)
            for k in range(5):
                if lines[k].get_top()[1] > ac.card.get_bottom()[1] - 0.05:
                    assert chips[k].get_right()[0] < ac.card.get_left()[0] - 0.15, k
            assert all(c.get_right()[0] < 6.5 for c in chips)
            for k, cue in enumerate(("Self-service", "Lower cost", "Automatic adjustment", "Smooth running",
                                     "Simpler development")):
                vo.wait_until(cue)
                self.play(FadeIn(thumbs[k], scale=0.8), FadeIn(lines[k], shift=RIGHT * 0.2), run_time=0.5)
                cp = thumbs[k].copy()
                self.play(cp.animate(path_arc=-PI / 3).move_to(chips[k]).set_opacity(0), FadeIn(chips[k], scale=1.1),
                          run_time=0.7)
                self.remove(cp)

        # ========================================================== 5-7. test yourself
        head = label("Test yourself", 30, TURN).move_to([-6.4, 2.55, 0], aligned_edge=LEFT)
        heads = [label(f"· {k + 1}/5", 30, TURN).next_to(head, RIGHT, buff=0.2) for k in range(5)]
        for h in heads:
            h.align_to(head, DOWN)
        qcards = [qcard(q).move_to([0, 0.15, 0]) for q in QUESTIONS]
        for q in qcards:
            assert q.get_top()[1] < head.get_bottom()[1] - 0.3 and q.get_bottom()[1] > -2.6, q.get_top()
        dots = VGroup(*[Circle(radius=0.11, stroke_color=S.GREY, stroke_width=2.5) for _ in range(5)])
        dots.arrange(RIGHT, buff=0.35).move_to([0, -2.9, 0])
        assert dots.get_top()[1] < min(q.get_bottom()[1] for q in qcards) - 0.2
        dots[0].set_fill(TURN, 1).set_stroke(TURN)
        cur = [qcards[0], heads[0]]

        def to_card(k):
            c0, h0 = cur
            nx = qcards[k]
            anims = [ReplacementTransform(c0.frame, nx.frame), FadeOut(c0.body, shift=UP * 0.2),
                     FadeIn(nx.body, shift=UP * 0.2), ReplacementTransform(h0, heads[k]),
                     dots[k - 1].animate.set_fill(S.GREY, 1).set_stroke(S.GREY),
                     dots[k].animate.set_fill(TURN, 1).set_stroke(TURN)]
            cur[0], cur[1] = nx, heads[k]
            return AnimationGroup(*anims, run_time=0.8)

        def mark(k, r):
            return Indicate(qcards[k].body[r], color=TURN, scale_factor=1.04, run_time=0.7)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(allp, ac, r43)), run_time=0.6)
            self.remove(allp, ac, r43, *thumbs, *lines, *chips)
            self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(heads[0], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Which control plane part")
            self.play(FadeIn(qcards[0], shift=UP * 0.15), FadeIn(dots, lag_ratio=0.15), run_time=0.7)
            vo.wait_until("and which one notices")
            self.play(mark(0, 1))
            vo.wait_until("Why does get all")
            self.play(to_card(1))
            vo.wait_until("and what flag fixes it")
            self.play(mark(1, 1))

        with self.voiceover(SAY[6]) as vo:
            vo.wait_until("How does the web Service")
            self.play(to_card(2))
            vo.wait_until("and why does the API reach Chroma")
            self.play(mark(2, 1))
            vo.wait_until("Trace one click")
            self.play(to_card(3))
            vo.wait_until("why does the bare IP")
            self.play(mark(3, 1))

        ans = card(["answers: exercises.md · study guide (MLOps_Learning)"], S.GREY, size=24).move_to(dots)
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("Why can the frontend")
            self.play(to_card(4))
            vo.wait_until("and what does the autoscaler add")
            self.play(mark(4, 1))
            vo.wait_until("Answers are in")
            self.play(FadeOut(cur[0], shift=UP * 0.2), FadeOut(cur[1]), FadeOut(head), run_time=0.5)
            self.play(ReplacementTransform(dots, ans), run_time=0.5)
            self.play(ans.animate.move_to([0, 0.15, 0]), run_time=0.5)

        # ========================================================== 8. next: L23
        road = dashed_chip("L23 · cheese-app-v4 · the two pulumi up runs from GitHub Actions, on every merge",
                           size=22)
        road.move_to([0, 0.15, 0])
        assert road.width < 12.6, road.width
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(ans, shift=UP * 0.2), run_time=0.4)
            self.remove(ans)
            self.play(FadeIn(road, shift=LEFT * 1.2), run_time=0.7)
            vo.wait_until("in version 4 of the app")
            self.play(Indicate(text_span(road.text, "cheese-app-v4"), color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("run from GitHub Actions")
            self.play(Indicate(text_span(road.text, "GitHub Actions, on every merge"), color=INK,
                               scale_factor=1.06), run_time=0.8)
        self.wait(0.4)
        self.play(FadeOut(road), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
