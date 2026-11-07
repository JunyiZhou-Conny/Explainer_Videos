"""S08 · Twenty-one commands: repeat, review, undo? (AC215 L20). No tracker in beats 0-4; TRACKER [M] 15
· extra in beats 5-6 (the teardown the README does not have). Lecture: 20 · 9 (beat 2), 20 · 10–11
(beat 3).

Beats (script.md "## S08", one voiceover block each):
0. The tally. A YELLOW counter top-left climbs 0 -> 21 ('commands on the VM'). A narrow column of GREY
   mono chips scrolls down the left: the 21 VM commands of README:48–219 (first row of each capture
   vm/01 … vm/46, the optional interactive api-service run excluded, long ones cut with '…'). Each
   chip throws one small block into V1's BLUE VM panel ('Compute Instance (VM)', bottom right), which
   grows into a tower; the block's colour is the series colour of what the command made (ORANGE:
   Docker and the 0777 folders, GREEN: the secret, the network, nginx.conf, TEAL: containers). On
   "console clicks" a GREY 'console clicks' chip, on "three Docker Hub scripts" a GREY 'laptop' frame
   with three TEAL `docker-hub.sh` chips, both above the VM panel. On "Each one added" a YELLOW ring
   around the tower.
1. The column, the chips above the VM and the ring leave. Three YELLOW-outlined speech bubbles pop on
   the left, tails toward the tower, one per phrase: 'Repeat? staging, tomorrow', 'Review? what
   exactly is on that VM?', 'Undo? delete every piece'.
2. LECTURE 20 · 9. The bubbles (and the counter) shrink into one GREY card 'too many steps to keep
   track of' / '→ automate'. The tower's blocks flicker into scrambled spots in the VM panel (GREY
   caption 'keep track of?'); on "let a tool do them" they line up neatly, sorted by colour, and
   'automate' turns YELLOW.
3. LECTURE 20 · 10–11. The card leaves; a copy of the tower turns into a GREEN file `__main__.py`
   ('Python') with a GREY 'git' ribbon. One GREY chip per phrase under it: 'servers', 'networks',
   'software'; 'Python' YELLOW on "Python here", the ribbon on "keep it in Git"; a GREY-dashed card
   'YAML / DSL' beside the file is struck RED on "No YAML file".
4. The file, chips and struck card leave. A GREY-dashed card 'earlier · Ansible playbooks (YAML)'
   with five rows 'images · VM · provision · containers · web server'; GREY arrows map them one to
   one onto five GREEN chips under 'this version · Pulumi (Python)'.
5. TRACKER [M] 15 · extra. The mapping leaves. A GOLD tag 'the README never deletes this VM' above
   the VM panel and a GOLD cost dial inside it that ticks. A schematic console list (tags `extra`,
   `illustration`): 'VM instances', a 'Delete' button, the row 'cheese-app-vm' whose box ticks on
   "select it"; a confirm dialog 'Delete instance?' with '☑ delete boot disk' and its own 'Delete'
   button; YELLOW '▶ your turn' beside that button on "Pause". The click stops the dial (GREY); the
   row becomes a GREY 'No VM instances' and the tower's blocks fall away at the same moment.
6. The console, tags, dial and tracker leave; the empty VM panel fades to a GREY outline; a GREY caption 'part 2 · as code' in it. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the 'console clicks' chip and the 'laptop' frame with the three `docker-hub.sh` chips sit
  above the VM panel, not beside the column (no room at >= 20 pt between the column and the panel).
  Blocks are coloured by what they made (series table) so the tower reads as Docker / folders /
  secret / network / containers.
- Beat 1: the bubbles stand left of the tower (the column has left), tails pointing at it: above the
  tower there is no room for three bubbles at 22 pt.
- Beat 2: the scramble happens inside the VM panel beside the card, not under it.
- Beat 3: a copy of the tower becomes the file, so the VM keeps its tower (it is still running until
  beat 5's delete; beat 6 empties it).
- Beat 5: the README tracker (step 15 · extra) is shown during the teardown (BRIEF: "No tracker until
  the teardown line"); the confirm dialog's tick is drawn (a box and a check glyph), not a '☑'
  character.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the 21 VM commands (README:48–219)
# (capture id, colour of what it made). The optional interactive api-service run (vm/38) is excluded.
VM_CMDS = [("01", SHARED), ("02", SHARED), ("03", SHARED),
           ("10", SHARED), ("11", SHARED), ("12", SHARED), ("13", SHARED), ("14", SHARED), ("15", SHARED),
           ("17", OWN), ("19", OWN),
           ("20", CONTAINER), ("21", CONTAINER), ("22", CONTAINER), ("23", CONTAINER),
           ("26", CONTAINER), ("27", CONTAINER), ("30", CONTAINER), ("42", CONTAINER),
           ("44", OWN), ("46", CONTAINER)]
assert len(VM_CMDS) == 21
CAPS = [capture(f"vm/{n}") for n, _ in VM_CMDS]
assert CAPS[0].cmd == "curl -fsSL https://get.docker.com -o get-docker.sh", CAPS[0].cmd
assert CAPS[-1].cmd.startswith("sudo docker run -d --name nginx "), CAPS[-1].cmd
assert CAPS[19].cmd_lines[0] == "echo 'user  nginx;", CAPS[19].cmd_lines[0]
assert all(c.cmd_lines[0] != "sudo docker run --rm -ti --name api-service \\" for c in CAPS)

CHIP_CHARS = 22


def short(c) -> str:
    """The command's first row, cut to CHIP_CHARS characters with '…' (multi-row ones always get '…')."""
    s = c.cmd_lines[0].rstrip(" \\").rstrip()
    more = c.k > 1
    if len(s) > CHIP_CHARS:
        return s[:CHIP_CHARS - 1].rstrip() + "…"
    return s + (" …" if more else "")


# ------------------------------------------------------------------ layout (scene units)
VM_SHIFT = RIGHT * 0.15 + DOWN * 0.9      # V1's VM panel -> x 0.75 .. 6.4, y -3.3 .. 0.25
TOWER_X = 2.4
BLOCK_W, BLOCK_H, BLOCK_P = 1.8, 0.11, 0.13
TOWER_BASE = -3.12
COL_X, COL_TOP, PITCH, ROWS = -6.4, 2.3, 0.6, 10


def block_at(i: int) -> np.ndarray:
    return np.array([TOWER_X, TOWER_BASE + BLOCK_H / 2 + i * BLOCK_P, 0])


def make_block(color) -> Rectangle:
    return Rectangle(width=BLOCK_W, height=BLOCK_H, stroke_color=color, stroke_width=1.5).set_fill(
        tint(color, 0.55), 1)


def bubble(head: str, rest: str) -> VGroup:
    """A YELLOW-outlined speech bubble with a tail on its right edge, pointing down-right."""
    t = VGroup(label(head, 24, TURN), label(rest, 22, INK)).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
    fr = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.42, corner_radius=0.2, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 1)
    t.move_to(fr)
    r = fr.get_right()
    tail = Polygon(r + UP * 0.12 + LEFT * 0.02, r + DOWN * 0.12 + LEFT * 0.02, r + RIGHT * 0.42 + DOWN * 0.3,
                   stroke_color=TURN, stroke_width=3).set_fill(S.BG, 1)
    g = VGroup(tail, fr, t)
    g.frame, g.text = fr, t
    return g


def checkbox(s: float = 0.3, color=S.GREY) -> Square:
    return Square(s, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)


def button(s: str, color=S.GREY) -> VGroup:
    t = label(s, 20, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=0.48, corner_radius=0.08, stroke_color=color,
                         stroke_width=2.5).set_fill(PANEL, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


class ByHand(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 7, len(SAY)
        self.camera.background_color = S.BG

        md = MasterDiagram(manual=True)
        md.shift(VM_SHIFT)

        # ------------------------------------------------------------ 0 · the tally
        with self.voiceover(SAY[0]) as vo:
            counter = label("0", 44, TURN).move_to([COL_X, 3.05, 0], aligned_edge=LEFT)
            count_lab = label("commands on the VM", 22, S.GREY).move_to([-5.35, 3.0, 0], aligned_edge=LEFT)
            md.vm(self)
            self.play(FadeIn(counter), FadeIn(count_lab), run_time=0.5)

            console = grey_chip("console clicks", 22).move_to([1.95, 1.6, 0])
            lap_fr = box(3.3, 2.45, LAPTOP, fill_opacity=0.05)
            lap_t = label("laptop", 20, LAPTOP)
            hub = VGroup(*[box_chip("docker-hub.sh") for _ in range(3)]).arrange(DOWN, buff=0.12)
            lap = VGroup(lap_fr, lap_t, hub)
            lap_fr.move_to([4.85, 1.5, 0])
            lap_t.move_to(lap_fr.get_corner(UL) + np.array([0.2, -0.24, 0]), aligned_edge=LEFT)
            hub.move_to(lap_fr.get_center() + DOWN * 0.2 + RIGHT * 0.1)

            visible, blocks = [], VGroup()
            shown_console = shown_hub = False
            for i, (c, (_, col)) in enumerate(zip(CAPS, VM_CMDS)):
                extras = []
                if not shown_console and vo.time_until("plus console clicks") <= 0.05:
                    extras.append(FadeIn(console, shift=DOWN * 0.15))
                    shown_console = True
                if not shown_hub and vo.time_until("plus three Docker Hub") <= 0.05:
                    extras += [FadeIn(lap_fr), FadeIn(lap_t),
                               LaggedStart(*[FadeIn(h, shift=DOWN * 0.15) for h in hub], lag_ratio=0.3)]
                    shown_hub = True
                left = 21 - i
                per = min(0.5, max(0.22, (vo.time_until("Each one added") - 0.2) / left))
                ch = grey_chip(short(c), 20, mono_font=True)
                anims = []
                if len(visible) < ROWS:
                    y = COL_TOP - len(visible) * PITCH
                else:
                    y = COL_TOP - (ROWS - 1) * PITCH
                    old = visible.pop(0)
                    anims += [FadeOut(old, shift=UP * 0.08), VGroup(*visible).animate.shift(UP * PITCH)]
                ch.move_to([COL_X + ch.width / 2, y, 0])
                b = make_block(col).move_to(block_at(i))
                new_count = label(str(i + 1), 44, TURN)
                new_count.move_to([COL_X + new_count.width / 2, counter.get_center()[1], 0])
                self.remove(counter)
                self.add(new_count)
                anims += [FadeIn(ch, shift=UP * 0.15), FadeIn(b, target_position=ch.get_right())]
                self.play(*anims, *extras, run_time=max(per, 0.5) if extras else per)
                visible.append(ch)
                blocks.add(b)
                counter = new_count
            if not shown_console:
                self.play(FadeIn(console, shift=DOWN * 0.15), run_time=0.4)
            if not shown_hub:
                self.play(FadeIn(lap_fr), FadeIn(lap_t), LaggedStart(*[FadeIn(h) for h in hub], lag_ratio=0.3),
                          run_time=0.6)
            self.remove(*blocks)
            self.add(blocks)
            vo.wait_until("Each one added")
            tower_ring = ring(blocks, TURN, buff=0.12)
            self.play(Create(tower_ring), Indicate(counter, color=TURN, scale_factor=1.15), run_time=0.8)

        # ------------------------------------------------------------ 1 · three questions
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(v, shift=LEFT * 0.3) for v in visible], FadeOut(console), FadeOut(lap),
                      FadeOut(tower_ring), run_time=0.6)
            bubbles = [bubble("Repeat?", "staging, tomorrow"), bubble("Review?", "what exactly is on that VM?"),
                       bubble("Undo?", "delete every piece")]
            ys = (1.75, 0.55, -0.65)
            for bb, y in zip(bubbles, ys):
                bb.move_to([0.3 - bb.frame.width / 2, y, 0])
            for bb, ph in zip(bubbles, ("Repeat:", "Review:", "Undo:")):
                vo.wait_until(ph)
                self.play(FadeIn(bb, scale=0.6), run_time=0.45)
                self.play(Indicate(bb.text[0], color=TURN, scale_factor=1.1), run_time=0.5)

        # ------------------------------------------------------------ 2 · slide 9: automate
        with self.voiceover(SAY[2]) as vo:
            ref9 = lref("9")
            auto = label("→ automate", 26, INK)
            idea = card(["too many steps to keep track of", auto], color=S.GREY, size=26)
            idea.move_to([-3.05, 0.55, 0])
            self.play(*[ReplacementTransform(bb, idea) for bb in bubbles[:1]],
                      *[FadeOut(bb, target_position=idea.get_center(), scale=0.4) for bb in bubbles[1:]],
                      FadeOut(counter), FadeOut(count_lab), FadeIn(ref9), run_time=0.8)
            vo.wait_until("too many steps")
            keep = label("keep track of?", 22, S.GREY).move_to([5.1, -0.2, 0])
            rng = np.random.default_rng(8)
            spots = []
            for _ in range(2):
                pts = [np.array([rng.uniform(1.0 + BLOCK_W / 2, 6.15 - BLOCK_W / 2), rng.uniform(-3.05, -0.6), 0])
                       for _ in blocks]
                spots.append(pts)
            self.play(*[b.animate.move_to(p) for b, p in zip(blocks, spots[0])], FadeIn(keep), run_time=0.6)
            self.play(*[b.animate.move_to(p) for b, p in zip(blocks, spots[1])], run_time=0.6)
            vo.wait_until("so let a tool")
            order = sorted(range(21), key=lambda k: ({SHARED: 0, OWN: 1, CONTAINER: 2}[VM_CMDS[k][1]], k))
            self.play(*[blocks[k].animate.move_to(block_at(j)) for j, k in enumerate(order)], FadeOut(keep),
                      auto.animate.set_color(TURN), run_time=0.9)
            self.play(Indicate(auto, color=TURN, scale_factor=1.1), run_time=0.6)
            self.play(FadeOut(ref9), run_time=vo.remaining(0.3))

        # ------------------------------------------------------------ 3 · slides 10-11: infrastructure as code
        with self.voiceover(SAY[3]) as vo:
            ref10 = lref("10–11")
            page = file_glyph(1.5, OWN).move_to([-4.6, 1.15, 0])
            fname = mono("__main__.py", 22, INK).next_to(page, RIGHT, buff=0.3).shift(UP * 0.22)
            lang = label("Python", 22, OWN).next_to(fname, DOWN, buff=0.14, aligned_edge=LEFT)
            gitr = tag("git", S.GREY).move_to(page.get_corner(UL) + np.array([0.05, 0.05, 0]))
            self.play(FadeOut(idea), FadeIn(ref10), run_time=0.5)
            self.play(TransformFromCopy(blocks, page), run_time=0.9)
            self.play(FadeIn(fname, shift=LEFT * 0.2), FadeIn(lang, shift=LEFT * 0.2), run_time=0.5)
            what = VGroup(*[grey_chip(s, 22) for s in ("servers", "networks", "software")]).arrange(RIGHT, buff=0.3)
            what.move_to([-3.4, -0.75, 0])
            feeds = VGroup(*[arrow(w.get_top(), page.get_bottom() + DOWN * 0.08, S.GREY, stroke=2.5)
                             for w in what])
            for w, f, ph in zip(what, feeds, ("the servers", "the networks", "the software")):
                vo.wait_until(ph)
                self.play(FadeIn(w, shift=UP * 0.15), GrowArrow(f), run_time=0.4)
            vo.wait_until("Python here")
            self.play(lang.animate.set_color(TURN).scale(1.12), run_time=0.35)
            self.play(lang.animate.scale(1 / 1.12), run_time=0.35)
            vo.wait_until("keep it in Git")
            self.play(FadeIn(gitr, scale=0.6), run_time=0.5)
            self.play(Circumscribe(gitr, color=TURN, buff=0.06), run_time=0.6)
            yaml_c = dashed_chip("YAML / DSL", PAST, 22)
            yaml_c.move_to([fname.get_right()[0] + 0.7 + yaml_c.width / 2, page.get_center()[1], 0])
            vo.wait_until("No YAML file")
            self.play(FadeIn(yaml_c), run_time=0.4)
            yaml_x = strike(yaml_c, ERR)
            self.play(Create(yaml_x), run_time=0.5)
            self.play(FadeOut(ref10), run_time=vo.remaining(0.3))

        # ------------------------------------------------------------ 4 · Ansible then, Pulumi now
        with self.voiceover(SAY[4]) as vo:
            stages = ("images", "VM", "provision", "containers", "web server")
            head_a = VGroup(label("earlier ·", 20, S.GREY), label("Ansible playbooks", 20, S.GREY),
                            label("(YAML)", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            rows_a = VGroup(*[label(s, 22, INK) for s in stages]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            inner = VGroup(head_a, rows_a).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            fr_a = outline_box(inner.width + 0.6, inner.height + 0.5, PAST, solid=False)
            fr_a.move_to([-5.0, 0.35, 0])
            inner.move_to(fr_a).align_to(fr_a, LEFT).shift(RIGHT * 0.3)
            ansible = VGroup(fr_a, inner)
            chips_p = VGroup(*[ok_chip(s, 22) for s in stages])
            x_p = -2.65
            for ch, r in zip(chips_p, rows_a):
                ch.move_to([x_p + ch.width / 2, r.get_center()[1], 0])
            head_p = VGroup(label("this version ·", 20, OWN), label("Pulumi (Python)", 20, OWN)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            head_p.move_to([x_p, head_a.get_center()[1], 0], aligned_edge=LEFT)
            maps = VGroup(*[arrow(np.array([fr_a.get_right()[0] + 0.1, r.get_center()[1], 0]),
                                  np.array([x_p - 0.12, r.get_center()[1], 0]), S.GREY, stroke=2.5)
                            for r in rows_a])
            self.play(FadeOut(page), FadeOut(fname), FadeOut(lang), FadeOut(gitr), FadeOut(what), FadeOut(feeds),
                      FadeOut(yaml_c), FadeOut(yaml_x), run_time=0.5)
            self.play(FadeIn(fr_a), FadeIn(head_a), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows_a], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("written in YAML")
            self.play(head_a[2].animate.set_color(TURN), run_time=0.4)
            self.play(Circumscribe(head_a[2], color=TURN, buff=0.05), run_time=0.7)
            vo.wait_until("This version")
            self.play(head_a[2].animate.set_color(S.GREY), run_time=0.3)
            self.play(FadeIn(head_p), run_time=0.4)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c, shift=RIGHT * 0.2))
                                    for a, c in zip(maps, chips_p)], lag_ratio=0.35), run_time=vo.until("one to one", 1.2))
            self.play(each(chips_p, OWN), run_time=1.0)

        # ------------------------------------------------------------ 5 · delete the VM now
        with self.voiceover(SAY[5]) as vo:
            tr = tracker_m(15, extra=True)
            gold = cost_tag("the README never deletes this VM").move_to([3.6, 1.0, 0])
            dial = CostDial(0.5, "cost").move_to([5.3, -1.75, 0])

            def ticking(seconds: float, *anims, turns_per_s: float = 0.12):
                self.play(*anims, dial.tracker.animate(rate_func=linear).increment_value(turns_per_s * seconds),
                          run_time=seconds)

            self.play(FadeOut(ansible), FadeOut(head_p), FadeOut(chips_p), FadeOut(maps), FadeIn(tr), run_time=0.5)
            self.play(FadeIn(gold, shift=DOWN * 0.15), FadeIn(dial), run_time=0.5)
            ticking(vo.until("delete this VM now", 0.4))
            ticking(0.6, Circumscribe(gold, color=COST, buff=0.06))

            # the schematic console list (illustration)
            fr = box(6.7, 5.1, S.GREY, fill=S.GREY_DARKER, fill_opacity=1).move_to([-3.05, -0.55, 0])
            title = label("VM instances", 24, INK).move_to(fr.get_corner(UL) + np.array([0.3, -0.45, 0]),
                                                         aligned_edge=LEFT)
            ill = illustration_tag()
            ill.move_to(fr.get_corner(UR) + np.array([-ill.width / 2, ill.height / 2 + 0.08, 0]))
            ext = extra_tag().next_to(ill, LEFT, buff=0.15)
            del_btn = button("Delete").next_to(title, RIGHT, buff=0.9)
            box1 = checkbox().move_to(fr.get_corner(UL) + np.array([0.45, -1.25, 0]))
            row_name = mono("cheese-app-vm", 22, INK).next_to(box1, RIGHT, buff=0.25)
            sep = Line(fr.get_left() + RIGHT * 0.2, fr.get_right() + LEFT * 0.2, color=S.GREY, stroke_width=1.5) \
                .move_to([fr.get_center()[0], box1.get_top()[1] + 0.2, 0])
            listing = VGroup(fr, title, ill, ext, del_btn, sep, box1, row_name)
            vo_t = vo.until("In the console", 0.3)
            ticking(vo_t)
            ticking(0.7, FadeIn(listing, shift=UP * 0.15))
            ticking(vo.until("select it", 0.3))
            tick1 = check_glyph(0.24, TURN).move_to(box1)
            ticking(0.5, Create(tick1), row_name.animate.set_color(TURN))
            ticking(vo.until("and delete it", 0.3))
            # confirm dialog
            dlg = box(5.2, 2.25, S.GREY, fill=PANEL, fill_opacity=1).move_to([-3.05, -1.75, 0])
            dlg_t = label("Delete instance?", 22, INK).move_to(dlg.get_corner(UL) + np.array([0.3, -0.38, 0]),
                                                               aligned_edge=LEFT)
            box2 = checkbox(0.28).move_to(dlg.get_corner(UL) + np.array([0.45, -1.0, 0]))
            tick2 = check_glyph(0.22, TURN).move_to(box2)
            boot = label("delete boot disk", 22, INK).next_to(box2, RIGHT, buff=0.2)
            ok_btn = button("Delete", TURN).move_to(dlg.get_corner(DR) + np.array([-0.85, 0.45, 0]))
            dialog = VGroup(dlg, dlg_t, box2, boot, ok_btn)
            ticking(0.25, del_btn.box.animate.set_fill(tint(TURN, 0.45), 1))
            ticking(0.25, del_btn.box.animate.set_fill(PANEL, 1))
            ticking(0.6, FadeIn(dialog, scale=0.95))
            ticking(0.5, Create(tick2), boot.animate.set_color(TURN))
            ticking(vo.until("Pause and delete", 0.3))
            turn = your_turn().next_to(ok_btn, LEFT, buff=0.25)
            ticking(0.5, FadeIn(turn, shift=RIGHT * 0.15))
            ticking(vo.until("the list should be", 0.3))
            # the click: the meter stops, the VM's blocks fall away as the list empties
            self.play(ok_btn.box.animate.set_fill(tint(TURN, 0.45), 1), run_time=0.3)
            dial.freeze()
            gone = label("No VM instances", 22, S.GREY).move_to(row_name, aligned_edge=LEFT).shift(LEFT * 0.55)
            self.play(FadeOut(dialog), FadeOut(turn), FadeOut(tick2),
                      ReplacementTransform(VGroup(box1, tick1, row_name), gone),
                      dial.animate.set_color(S.GREY),
                      LaggedStart(*[FadeOut(b, shift=DOWN * 0.4) for b in blocks[::-1]], lag_ratio=0.03),
                      run_time=0.8)
            listing.remove(box1, row_name)
            listing.add(gone)

        # ------------------------------------------------------------ 6 · part 2 as code
        with self.voiceover(SAY[6]) as vo:
            vmp = md.parts["vm"]
            self.play(FadeOut(listing), FadeOut(gold), FadeOut(dial), FadeOut(tr), run_time=0.5)
            self.play(vmp.frame.animate.set_fill(opacity=0).set_stroke(S.GREY, opacity=0.7),
                      vmp.title.animate.set_color(S.GREY), run_time=0.7)
            md.heal(self)
            cap = label("part 2 · as code", 26, S.GREY).move_to(vmp.frame)
            vo.wait_until("as code")
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(cap, color=S.GREY, scale_factor=1.06), run_time=0.6)

        self.play(FadeOut(md), FadeOut(cap), run_time=0.6)
        self.wait(0.3)
