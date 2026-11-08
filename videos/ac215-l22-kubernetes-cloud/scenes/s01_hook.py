"""S01 · Who restarts it at 2 a.m.? (cold open of AC215 L22, the full follow-along). No tracker.
Lecture: 22 · 4–5, 7, 8–9, 9 and 11, 12 (each tag only while its picture is on screen).

Beats (script.md "## S01", one voiceover block each):
0. LECTURE 22 · 4–5. V2 FleetMorph, slide 5 redrawn: a BLUE 'VM' with TEAL nginx on top and
   Frontend / API 1 / API 2 under it (short PINK lines), a PINK 'HTTP 80' door on its top edge. On
   "a web server in front" nginx flashes, on "a frontend and two APIs" the trio flashes; the GREY
   browser drops above with its PINK arrow to the door; a request pulse runs down the arrow and the
   lines on "If one of them crashes"; on "who restarts it" a YELLOW '?' settles
   right of the VM. (Emphasis = outline flash + text pulse: Indicate would fill the opaque boxes.)
1. LECTURE 22 · 7. The '?' goes. GREY clock '2:00 a.m.' top left; API 1 cracks RED and the request
   bounces with a RED ×; the GREY phone 'the app owner' shakes right of the VM; 'the operator' slides
   in along the PINK 'SSH' tunnel; on "restarts it by hand" API 1 is TEAL again.
2. No lecture tag. The GREY-dashed chip 'L20 · one VM · Docker restarts containers · nobody restarts
   the VM' slides in under the VM, pulses once; on "if the machine itself failed" the VM's outline
   flashes RED; the chip fades.
3. LECTURE 22 · 8–9. The story's extras fade; the VM becomes three BLUE VMs (slide 9's layout: VM 1
   Frontend + 'HTTP 80'; VM 2 nginx over API 1 and a dashed 'API 1 · backup'; VM 3 likewise for API
   2) and the GREY speech card 'put it on several servers' settles above them. On "The operator
   answers with three machines" the three VM outlines flash; on "a backup copy"
   the two backups flash.
4. LECTURE (held). The speech card goes and the fleet slides 1.2 lower; the two backups glow and stay
   outlined YELLOW (back to TEAL in beat 5); on "Name one failure" the two APIs flash. PONDER(8 s):
   a wider 3-line card (the script's words) above the whole fleet; the fleet slides back up in beat 5.
5. LECTURE 22 · 9, 11. The card goes. On "The machine itself" VM 2's outline turns RED and both
   copies flash RED; on "takes both copies at once" everything inside VM 2 goes dark;
   on "And even when a backup survives" VM 3's backup flashes; on "a person still has to switch" a
   GREY lever and hand appear under VM 3 with 'switch: by hand' and the lever is pulled.
6. LECTURE 22 · 12. The VMs fade; the AsksChecklist grows centre (three empty boxes, a GREY
   one-liner under each); each item flashes YELLOW on its phrase.
7. No lecture tag. The card shrinks into the top-right corner (below the lecture-tag slot), its
   boxes flash on "we tick each item"; 'Kubernetes' writes in the centre in WHITE; everything fades
   to an empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S01"]

PONDER_Q = ("Each backup sits on the same VM as its original.\nWhat still takes that API down,\n"
             "and who switches to the backup?")   # script's words; 3 lines so the card clears the fleet
PONDER_AT = (0, 1.35)          # card y -0.29 .. 2.99: above the lowered fleet (door top -0.47), under the tag
FLEET_DROP = 1.2               # the fleet sits this much lower while the ponder card is up


def ponder_wide(scene, question: str, seconds: float, center, width: float = 11.5, k: float = 0.94) -> VGroup:
    """PLAYS: ponder() with a wider, slightly smaller card (ponder() takes no scale). Returns the card."""
    c = ponder_card(question, width=width).scale(k)
    c[0].set_fill(S.BG, 1)
    c.move_to([center[0], center[1], 0])
    scene.play(FadeIn(c, scale=0.95), run_time=0.6)
    bar = c[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return c


def swap_ref(scene, old, slides: str | None, run_time: float = 0.4):
    """PLAYS: the lecture tag `old` (or None) cross-fades into lref(slides) (or nothing). Returns the new tag."""
    new = lref(slides) if slides else None
    anims = []
    if old is not None:
        anims.append(FadeOut(old))
    if new is not None:
        anims.append(FadeIn(new))
    if anims:
        scene.play(*anims, run_time=run_time)
    if old is not None:
        scene.remove(old)
    return new


def flash(boxes, color, width: float = 6):
    """ANIMs: each boxed() part's outline flashes `color` and its text pulses (Indicate on the whole box
    would fill the opaque box solid)."""
    out = []
    for b in boxes:
        out.append(b.frame.edge.animate(rate_func=there_and_back).set_stroke(color, width))
        out.append(Indicate(b.text, color=color, scale_factor=1.1))
    return out


def go_dark(v, k: float = 0.3):
    """ANIMs: everything inside VM `v` dims to `k` of its opacity (fills and strokes as they are, so an
    unfilled outline never gains a fill), and its outline turns RED at full strength."""
    out = []
    for m in v.get_family():
        if m is v.frame.edge or m in v.frame.edge.get_family() or not m.has_points():
            continue
        out.append(m.animate.set_fill(opacity=m.get_fill_opacity() * k)
                   .set_stroke(opacity=m.get_stroke_opacity() * k))
    out.append(v.frame.edge.animate.set_stroke(ERR, 4, opacity=1))
    return out


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 8, len(SAY)
        fm = FleetMorph()

        # ========================================================== 0. one VM, a small app
        with self.voiceover(SAY[0]) as vo:
            ref = swap_ref(self, None, "4–5")
            fm.one_vm(self, run_time=1.0)
            vo.wait_until("a web server in front")
            self.play(*flash([fm.boxes["nginx"]], TURN), run_time=0.8)
            fm.heal(self)
            vo.wait_until("a frontend and two APIs")
            trio = [fm.boxes[k] for k in ("front", "api1", "api2")]
            self.play(*flash(trio, TURN),
                      ShowPassingFlash(fm.links.copy().set_stroke(TURN, 5), time_width=0.6), run_time=0.9)
            fm.heal(self)
            fm.browser(self, run_time=0.8)
            vo.wait_until("If one of them crashes in the night")
            self.play(ShowPassingFlash(fm.req.copy().set_stroke(TURN, 6), time_width=0.6),
                      ShowPassingFlash(fm.links.copy().set_stroke(TURN, 5), time_width=0.6), run_time=1.0)
            fm.heal(self)
            vo.wait_until("who restarts it")
            fm.question(self)

        # ========================================================== 1. two in the morning
        with self.voiceover(SAY[1]) as vo:
            ref = swap_ref(self, ref, "7")
            fm.drop(self, fm.q, run_time=0.3)
            fm.clock(self)
            vo.wait_until("one API container crashes")
            fm.crash(self, "api1")
            vo.wait_until("The app owner finds out")
            fm.app_owner(self)
            vo.wait_until("and the operator logs in")
            fm.operator(self, "api1", run_time=1.6)
            self.play(fm.op.animate.shift(LEFT * 0.3), run_time=0.3)   # its label clears the VM's left edge
            fm.heal(self)
            vo.wait_until("restarts it by hand")
            fm.heal_box(self, "api1")
            self.play(*flash([fm.boxes["api1"]], CONTAINER, 7), run_time=0.7)
            fm.heal(self)

        # ========================================================== 2. L20: Docker restarts containers, not VMs
        with self.voiceover(SAY[2]) as vo:
            ref = swap_ref(self, ref, None)
            fm.l20_chip(self)
            vo.wait_until("but only on that one machine")
            self.play(Indicate(fm.l20, color=TURN, scale_factor=1.05), run_time=0.8)
            fm.heal(self)
            vo.wait_until("if the machine itself failed")
            self.play(fm.vm[0].edge.animate(rate_func=there_and_back).set_stroke(ERR, 7), run_time=1.0)
            fm.heal(self)
            vo.wait_until("the whole site waited for you")
            fm.drop(self, fm.l20, run_time=0.6)

        # ========================================================== 3. several servers, a backup beside each API
        with self.voiceover(SAY[3]) as vo:
            ref = swap_ref(self, ref, "8–9")
            fm.drop(self, fm.clock_g, fm.owner_g, fm.op, fm.tunnel, fm.win, fm.req, run_time=0.5)
            fm.three_vms(self, run_time=1.2)
            vo.wait_until("The operator answers with three machines")
            self.play(*[v.frame.edge.animate(rate_func=there_and_back).set_stroke(TURN, 6) for v in fm.vms],
                      run_time=0.9)
            fm.heal(self)
            vo.wait_until("and a backup copy beside each API")
            bks = [v.backup for v in fm.vms if v.backup is not None]
            self.play(*flash(bks, TURN), run_time=0.9)
            fm.heal(self)

        # ========================================================== 4. PONDER: what still takes it down?
        with self.voiceover(SAY[4]) as vo:
            fleet = VGroup(*fm.vms)
            fm.drop(self, fm.say, run_time=0.4)        # the speech card has done its job; room for the card
            self.play(fleet.animate.shift(DOWN * FLEET_DROP), run_time=0.6)
            fm.heal(self)
            fm.glow_backups(self)
            bks = [v.backup for v in fm.vms if v.backup is not None]
            self.play(*[b.frame.edge.animate.set_stroke(TURN, 4) for b in bks], run_time=0.5)   # stay lit
            fm.heal(self)
            vo.wait_until("Name one failure")
            mains = [v.main for v in fm.vms[1:]]
            self.play(*flash(mains, TURN), run_time=0.9)
            fm.heal(self)
            vo.wait_until("and say who switches")
            self.play(*[Indicate(b.text, color=TURN, scale_factor=1.12) for b in bks], run_time=0.8)
            fm.heal(self)
        card = ponder_wide(self, PONDER_Q, seconds=8, center=PONDER_AT)

        # ========================================================== 5. the machine itself; a person switches
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card), *[b.frame.edge.animate.set_stroke(CONTAINER, 3) for b in bks], run_time=0.4)
            self.remove(card)
            fm.heal(self)
            self.play(fleet.animate.shift(UP * FLEET_DROP), run_time=0.5)
            fm.heal(self)
            ref = swap_ref(self, ref, "9, 11")
            vo.wait_until("The machine itself")
            v2 = fm.vms[1]
            self.play(v2.frame.edge.animate.set_stroke(ERR, 5), *flash([v2.main, v2.backup], ERR), run_time=0.9)
            fm.heal(self)
            vo.wait_until("takes both copies at once")
            self.play(*go_dark(v2), run_time=0.8)
            fm.heal(self)
            vo.wait_until("And even when a backup survives")
            self.play(*flash([fm.vms[2].backup], TURN), run_time=0.9)
            fm.heal(self)
            vo.wait_until("a person still has to switch over by hand")
            fm.lever(self, 2)

        # ========================================================== 6. the lecture's three asks
        with self.voiceover(SAY[6]) as vo:
            fm.fade_all(self, run_time=0.5)
            ref = swap_ref(self, ref, "12")
            ac = AsksChecklist()
            self.play(FadeIn(ac, scale=0.9), run_time=0.7)
            for i, cue in enumerate(("Failover", "Load balancing", "Scaling")):
                vo.wait_until(cue)
                ac.light(self, i, run_time=0.8)

        # ========================================================== 7. the card goes to the corner; Kubernetes
        with self.voiceover(SAY[7]) as vo:
            ref = swap_ref(self, ref, None)
            ac.shrink(self, run_time=0.8)
            vo.wait_until("and we tick each item")
            boxes = [r.box for r in ac.card.rows]
            self.play(AnimationGroup(*[Indicate(b, color=TURN, scale_factor=1.3) for b in boxes], lag_ratio=0.2), run_time=1.0)
            ac.heal(self)
            vo.wait_until("The tool for all three is Kubernetes")
            word = label("Kubernetes", 56, INK)
            self.play(Write(word), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(word), FadeOut(ac), run_time=0.7)
        self.remove(word, ac)
        self.wait(0.5)
