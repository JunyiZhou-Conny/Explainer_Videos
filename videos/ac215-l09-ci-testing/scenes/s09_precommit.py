"""S09 · The gate on your machine (README Part 4, tracker D1 -> D5). Ends part 1.

Beats (script.md, ## S09; one voiceover block each):
0. TRACKER D1 (tracker D appears); `Lecture 9 · slides 34, 41–44` (top right, until the refusal in
   beat 7). A 10-row terminal types `pip install pre-commit` (README:240) -> part4-01: 2–3, …, 35
   (wrap); an ORANGE tag "on the host · outside the container" over the terminal; `pre-commit-4.7.0`
   ringed with `at the time of recording`; a GREY remedy chip "pip refuses? (PEP 668) → pipx install
   pre-commit, or any venv". TRACKER D2: `pre-commit install` (README:246) -> part4-02: 2, the hook
   path ringed. `▶ your turn` on both.
1. V5 hand-over chain: the terminal's `.git/hooks/pre-commit` flies into the hook card; git commit ->
   .git/hooks/pre-commit (GREY tag "machine-specific · never committed") -> pre-commit -> the
   TEAL-outlined .pre-commit-config.yaml -> nine empty arches.
2. CODE(.pre-commit-config.yaml) in four 10-line windows (7–16, 17–26, 27–36, 35–44; comment lines
   28 and 37 cropped to their hook names) over the nine arches, which take their names as the
   windows pass: whitespace, end of file; YAML … private keys; black; flake8. `'120'` underlined;
   lines 35 and 44 `files: ^src/.*\\.py$` YELLOW; GREY dashed chip "tests/ · never matched".
3. TRACKER D3: `git commit -m "Your commit message"` (README:255) -> part4-03: 2–3 (wrap), 4–6, …,
   15–23, …, 27. The `[WARNING]` row ringed with `at the time of recording`; the nine Skipped rows ringed;
   `nothing to commit, working tree clean` highlighted. `▶ your turn`.
4. TRACKER D4: `pre-commit run --all-files` (README:262) -> part4-04: 2–14, …, 16 (line 9 RED,
   line 11 YELLOW). The terminal shrinks to a strip (rows 9, 11, 13) under the V1 gate (9 named
   arches, staging tray, HISTORY vault): six arches pass, JSON skips, black's arch flashes amber,
   the envelope bounces back to the tray. `▶ your turn`. PONDER (6 s).
5. The strip prints part4-04: 18 (Flake8 Passed, GREEN). Above it a before/after pair of utils.py:7,
   the comma fixed; captions "Failed ≠ broken: black changed the file" / "look at the change → re-stage".
6. TRACKER D4 · extra: `git diff` -> part4-05: 2 (wrap), …, 10–11, …, 16–18; `git add -u` -> no
   output. TRACKER D3: the commit again -> part4-07: 2–12; strip (rows 10–12) under the gate: seven
   arches GREEN, two GREY dashed, the envelope goes into the vault; `[main b72d50d]` GREEN.
   `▶ your turn`. TRACKER D5: `pre-commit run` (README:265) -> part4-08: 2–10, all arches GREY dashed.
7. TRACKER D5 · extra: the sed line (folds) -> no output, GREY note "on a Mac: sed -i '' …";
   `git commit -m "try an unused import"` -> part4-11: 9–13, …, 18–22 (both Failed RED, line 11 `files
   were modified` RED as scripted, F401 RED). Strip (rows 9, 18, 22) under the gate: an `import os` envelope, black amber, flake8
   RED, back to the tray; `git status` -> part4-12: 2–3, …, 6–8, "still staged · not committed";
   the restore line (folds) -> no output, the envelope leaves the tray; the vault stays shut. A
   YELLOW card "this gate never ran a test" appears and parks in the top-right corner. Fade to an
   empty frame (end of part 1).

Deviations (reported to the coordinator):
- pre-commit pads every hook row with dots to 79 characters; the house terminal holds 65 (22 pt).
  The rows are shown with a shorter dot leader (`hook_row`): every word, verdict and order is the
  capture's own; only the number of padding dots differs.
- part4-04:15 (the emoji line) is never printed (SCENE-NOTES trap): 2–16 is shown as 2–14, …, 16.
- The remedy chip and the ORANGE tag stand above the terminal (not inside it, where they would hide
  output). The chip leaves out "said at S05" (an authoring note).
- Beat 7 follows the script: "Both RED" — black's "files were modified" (YELLOW in beat 4), both
  Failed verdicts and the F401 row are RED here.
- The gate pictures need the frame, so the terminal shrinks to a 3-row strip under them (beats 4–7),
  keeping the rows the narration names.
- Beat 2's arches are a shorter Turnstile (arch_h 1.0) that the chain's turnstile turns into: with
  the chain's 1.3 the 10-line panel and the arch names above the lamps collide.
- `pre-commit run --all-files` leaves no room for a row tag: `▶ your turn` stands over the
  terminal's top-right corner and the command is underlined YELLOW. Beat 6's "pause and walk the
  loop" puts `▶ your turn` on the `[main b72d50d]` row (the command has scrolled out of the strip).
- Local workarounds for common.py: CommitGate builds its arch names before moving its turnstile
  (they sit 0.75 low; `place_gate` rebuilds them); Terminal.print/type scroll by sliding the old
  rows up past the box, over the tracker, and print more rows than fit below the box (`room`/`out`
  fade the oldest rows in place and print in chunks).
- Critic pass (pacing): the gate replays in beats 4, 6 and 7 ran up to 5.5 s behind the narration;
  they now fade in with the terminal's shrink, step faster, and beat 6 uses `quick_pass` (a shorter
  door than CommitGate.pass_through, with the `[main b72d50d]` ring on the door's shut).
"""

import re

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer import style as S
from explainer.devops import tag

from common import (ERR, INK, LAPTOP, MODIFIED, NARRATION, P_LAPTOP, PASS, STATE, SYSTEM, TURN,
                    CHEESE_HOOKS, CommitGate, HandoverChain, Turnstile, attach, bare_prompt, beside, box,
                    capture, code_panel, code_span, dashed_chip, excerpt, extra_row, glyph_range, label,
                    line_bar, lref, mono, mono_line, pin, ponder_card, readme, recording_tag, resize, ring,
                    row_tag, shown_path, substring, term, track, tracker, turn_row, type_cmd, under, unpin,
                    your_turn)

SAY = NARRATION["S09"]
CFG = "cheese-app-ci-cd/.pre-commit-config.yaml"
CROP = {28: "  # Black formatter", 37: "  # Flake8 linter"}     # the stale "L17, Slide" refs never shown
WINDOWS = ((7, 16), (17, 26), (27, 36), (35, 44))
COLS = 65                                                     # the house terminal at 22 pt

_HOOK = re.compile(r"^(.*?[^.])(\.{3,})((?:\(no files to check\))?(?:Passed|Failed|Skipped))$")


def hook_row(s: str, n: int = COLS) -> str:
    """A pre-commit row with its dot leader shortened to fit `n` columns (words unchanged)."""
    m = _HOOK.match(s)
    if not m:
        return s
    name, _, tail = m.groups()
    dots = n - len(name) - len(tail)
    assert dots >= 3, s
    return name + "." * dots + tail


def fit(lines, colors=None):
    """Capture lines ready to print: hook rows squeezed, optional colour per file line index."""
    out = []
    for i, s in enumerate(lines):
        s = hook_row(s)
        c = (colors or {}).get(i)
        out.append((s, c) if c else s)
    return out


def room(scene, t, n: int, run_time: float = 0.3) -> None:
    """Make room for n new rows without the toolkit's fly-up: the oldest rows fade where they are,
    then the rest slide up (long outputs would otherwise sail over the tracker)."""
    over = len(t.lines) + n - t.rows
    if over <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:over])
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(gone), run_time=run_time * 0.4)
    for m in gone:
        t.lines.remove(m)
    scene.remove(gone)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.6)


def out(scene, t, lines, wrap: bool = False, run_time: float = 0.6, lag: float = 0.08,
        chunk: int | None = None) -> VGroup:
    """Print capture lines ((text, colour) or text) in chunks that fit the terminal (`chunk` rows,
    default 4); wrapped lines fold at the edge as Terminal.print(wrap=True) does. Returns every
    printed row."""
    items = []
    for x in lines:
        s, c = (x, None) if isinstance(x, str) else x
        while wrap and len(s) > t.max_chars:
            items.append((s[:t.max_chars], c))
            s = s[t.max_chars:]
        assert len(s) <= t.max_chars, s
        items.append((s, c))
    k = max(1, min(t.rows, chunk or 4))
    chunks = [items[i:i + k] for i in range(0, len(items), k)]
    rows = VGroup()
    for ch in chunks:
        room(scene, t, len(ch))
        rows.add(*t.print(scene, [(s, c) if c else s for s, c in ch], run_time=run_time / len(chunks) + 0.1,
                          lag=lag))
    return rows


def typ(scene, t, cmd: str, type_time: float | None = None):
    """type_cmd, with room made first (see room())."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    p = t.prompt + " "
    room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
    return type_cmd(scene, t, cmd, type_time)


def flash(tg, color, scale: float = 1.15, run_time: float = 0.7):
    """Indicate a tag's words only (indicating the whole tag floods its dark fill)."""
    return Indicate(tg.text, color=color, scale_factor=scale, run_time=run_time)


def each(pieces, color, scale: float = 1.1, lag: float = 0.15):
    """Flash scattered pieces one by one: one Indicate on their group would scale them about the
    group's centre and pull glyphs off their rows (SCENE-NOTES trap)."""
    return LaggedStart(*[Indicate(p, color=color, scale_factor=scale) for p in pieces], lag_ratio=lag)


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def row_with(rows, sub: str):
    for r in rows:
        if sub in r.text:
            return r
    raise KeyError(sub)


def tag_on(scene, line, mk, anim=None, buff: float = 0.45, tm=None):
    """Pin a row tag (mk()) beside a typed command (its last row, or its first when the last is too
    long). Returns (row, tag) for unpin()."""
    rs = rows_of(line)
    row = rs[-1]
    t = beside(mk(), row, buff=buff)
    if t.get_right()[0] > 6.55:
        row = rs[0]
        t = beside(mk(), row, buff=buff)
    if t.get_right()[0] > 6.55 and mk is turn_row and tm is not None:
        # no room in the row: the house tag over the terminal's top-right corner, the command
        # underlined YELLOW (the underline scrolls with the row; drop_tag() clears both)
        yt = your_turn()
        top = tm.box.get_top()[1]
        yt.move_to([6.4 - yt.width / 2, top + 0.06 + yt.height / 2, 0])
        typed = VGroup(*[glyph_range(r, len(P_LAPTOP) + 1 if r is rs[0] else 0) for r in rs])
        ul = under(typed, TURN, stroke=3)
        scene.play(FadeIn(yt, shift=LEFT * 0.1), Create(ul), *([anim] if anim is not None else []),
                   run_time=0.5)
        attach(scene, rs[-1], ul)
        return (rs[-1], ul), yt
    assert t.get_right()[0] <= 6.55, line.text if hasattr(line, "text") else line
    if anim is not None:
        pin(scene, row, t, anim=AnimationGroup(FadeIn(t, shift=LEFT * 0.1), anim))
    else:
        pin(scene, row, t)
    return row, t


def drop_tag(scene, row, t):
    """Take a tag_on() tag off again (a pinned row tag, or the corner tag and its underline)."""
    if isinstance(row, tuple):
        r, ul = row
        scene.play(FadeOut(VGroup(t, ul)), run_time=0.3)
        if ul in r.submobjects:
            r.remove(ul)
        scene.remove(t, ul)
    else:
        unpin(scene, row, t)


def cfg_panel(a: int, b: int):
    """CODE(.pre-commit-config.yaml: a–b) at 20 pt, the two stale comment lines cropped."""
    lines = excerpt(CFG, a, b).split("\n")
    for n, s in CROP.items():
        if a <= n <= b:
            assert lines[n - a].startswith(s + " - L17"), lines[n - a]
            lines[n - a] = s
    p = code_panel("\n".join(lines), shown_path(CFG), a, "yaml", font_size=20)
    return p.move_to([0, 0, 0]).align_to([-5.9, 0, 0], LEFT).align_to([0, 2.8, 0], UP)


def place_gate(gate: CommitGate) -> VGroup:
    """The gate with its arch names, centred, bottom at -1.3 (over a 3-row strip). The names are
    rebuilt first: CommitGate builds them before it moves its turnstile, so they sit 0.75 low."""
    gate.turnstile.name_labels(CHEESE_HOOKS)
    g = VGroup(gate, gate.turnstile.labels)
    g.move_to([0, 0, 0])
    g.shift(UP * (-1.3 - g.get_bottom()[1]))
    return g


def reset_arches(gate: CommitGate) -> None:
    """All arches idle again, without playing (the gate is off screen)."""
    for a in gate.arches:
        a.frame.become(a._frame("idle"))
        a.lamp.set_color(STATE["idle"])
        a.beam.set_stroke(STATE["idle"], opacity=0.35)
        a.state = "idle"


def step_to(scene, gate, i: int, state: str, run_time: float = 0.25):
    """The envelope moves under arch i, which takes `state`."""
    a = gate.arches[i]
    scene.play(gate.envelope.animate.move_to([a.get_center()[0], gate.home[1], 0]), a.to(state),
               run_time=run_time)


def late_in(m, start: float = 0.65):
    """FadeIn over the last part of a resize: the shrinking terminal's top edge has passed below the
    gate before the gate shows (both in one play crossed the arches)."""
    return FadeIn(m, rate_func=lambda x: smooth(max(0.0, (x - start) / (1 - start))))


def quick_pass(scene, gate: CommitGate, states, step_time: float = 0.16, *with_shut) -> None:
    """CommitGate.pass_through with a shorter door (the narration names the arches and the vault in
    about three seconds): through every arch, the door opens, the envelope goes in, the door shuts
    (with `with_shut` animations)."""
    env = gate.envelope
    for i, s in enumerate(states):
        step_to(scene, gate, i, s, run_time=step_time)
    scene.play(env.animate.move_to([gate.vault.get_left()[0] - env.width / 2 - 0.05, gate.home[1], 0]),
               gate.open(), run_time=0.35)
    scene.play(env.animate.move_to(gate.vault.frame), FadeOut(env), run_time=0.35)
    gate.remove(env)
    scene.remove(env)
    gate.envelope = None
    scene.play(gate.shut(), *with_shut, run_time=0.6 if with_shut else 0.3)


def remedy_chip() -> VGroup:
    parts = VGroup(label("pip refuses? (PEP 668) →", 20, S.GREY), mono("pipx install pre-commit", 20, INK),
                   label(", or any venv", 20, S.GREY))
    parts.arrange(RIGHT, buff=0.15)
    parts[2].shift(LEFT * 0.1)
    for p in parts[1:]:
        p.align_to(parts[0], DOWN)
    b = box(parts.width + 0.45, parts.height + 0.3, S.GREY, fill_opacity=0.1, radius=0.12)
    parts.move_to(b)
    return VGroup(b, parts)


def mac_chip() -> VGroup:
    parts = VGroup(label("on a Mac:", 20, S.GREY), mono("sed -i '' …", 20, INK)).arrange(RIGHT, buff=0.18)
    b = box(parts.width + 0.45, parts.height + 0.3, S.GREY, fill_opacity=0.1, radius=0.12)
    parts.move_to(b)
    return VGroup(b, parts)


def pair_card() -> VGroup:
    """utils.py:7 before and after black (part4-05: 10–11), the comma fixed. .before .after"""
    before = mono_line("def power(base,exponent):", 26, INK)
    after = mono_line("def power(base, exponent):", 26, INK)
    w1, w2 = label("before", 22, S.GREY), label("after black", 22, PASS)
    w2.next_to(w1, DOWN, buff=0.55, aligned_edge=LEFT)
    x = max(w1.get_right()[0], w2.get_right()[0]) + 0.5
    before.shift([x - before.strut.get_left()[0], w1.get_center()[1] - before.strut.get_center()[1], 0])
    after.shift([x - after.strut.get_left()[0], w2.get_center()[1] - after.strut.get_center()[1], 0])
    head = VGroup(mono("src/api-service/api/utils.py", 20, S.GREY), label("· line 7", 20, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    body = VGroup(w1, w2, before, after)
    head.next_to(body, UP, buff=0.35, aligned_edge=LEFT)
    inner = VGroup(head, body)
    frame = box(inner.width + 0.8, inner.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    frame.move_to(inner)
    g = VGroup(frame, head, w1, w2, before, after)
    g.frame, g.head, g.w1, g.w2, g.before, g.after = frame, head, w1, w2, before, after
    return g


class PreCommitGate(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)
        pip, inst = capture("part4-01"), capture("part4-02")
        clean, allf, diff = capture("part4-03"), capture("part4-04"), capture("part4-05")
        add, again, staged = capture("part4-06"), capture("part4-07"), capture("part4-08")
        brk, blocked, status, restore = (capture("part4-10"), capture("part4-11"), capture("part4-12"),
                                         capture("part4-13"))
        for c, n in ((pip, 240), (inst, 246), (clean, 255), (allf, 262), (again, 255), (staged, 265)):
            assert c.cmd == readme(n), (c.cmd, readme(n))
        assert add.lines == [] and brk.lines == [] and restore.lines == []
        assert again.line(11).startswith("[main b72d50d]")

        # ========================================================== 0. install the gate (D1, D2)
        tr = tracker("D", 1)
        ref = lref("34, 41–44")
        t = term(P_LAPTOP, rows=10)
        host = tag("on the host · outside the container", SYSTEM)
        host.move_to([-6.3 + host.width / 2, 2.35, 0])
        remedy = remedy_chip()
        remedy.move_to([-6.3 + remedy.width / 2, 1.8, 0])
        rec = recording_tag()
        rec.move_to([6.35 - rec.width / 2, 2.35, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.7)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.6), FadeIn(t), run_time=0.6)
            vo.wait_until("Outside the container")
            self.play(FadeIn(host, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("pip install pre-commit")
            p_ln = typ(self, t, pip.cmd, type_time=0.9)
            res = out(self, t, pip.at((2, 3), "…", 35), wrap=True, run_time=0.8)
            vo.wait_until("4.7.0 at the time")
            ver_row = row_with(res, "pre-commit-4.7.0")
            ver = substring(ver_row, "pre-commit-4.7.0")
            vring = ring(ver, S.GREY, buff=0.05)
            self.play(Create(vring), FadeIn(rec, shift=LEFT * 0.15), ver.animate.set_color(INK), run_time=0.6)
            attach(self, ver_row, vring)
            self.play(FadeIn(remedy, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("then, from the repo root")
            p_row, p_tag = tag_on(self, p_ln, turn_row, buff=0.15)
            i_ln = typ(self, t, inst.cmd, type_time=0.7)
            i_row, i_tag = tag_on(self, i_ln, turn_row, anim=track(tr, 2))
            inst_out = out(self, t, inst.at(2), run_time=0.4)[0]
            vo.wait_until("a hook file now sits")
            hook_glyphs = substring(inst_out, ".git/hooks/pre-commit")
            hring = ring(hook_glyphs, LAPTOP, buff=0.05)
            self.play(Create(hring), hook_glyphs.animate.set_color(INK), run_time=0.6)
            attach(self, inst_out, hring)
            vo.wait_until("Pause and run both")
            self.play(flash(p_tag, TURN), flash(i_tag, TURN), run_time=0.8)

        # ========================================================== 1. the hand-over chain (V5)
        hc = HandoverChain("cheese")
        hook_note = hc.hook_note()
        flyer = hook_glyphs.copy()

        with self.voiceover(SAY[1]) as vo:
            self.add(flyer)
            self.play(FadeOut(VGroup(t, host, remedy, rec)), run_time=0.5)
            self.remove(t, host, remedy, rec)
            self.play(FadeIn(hc.git, shift=DOWN * 0.15), GrowArrow(hc.arrows[0]), run_time=0.6)
            self.play(ReplacementTransform(flyer, hc.hook.text), FadeIn(hc.hook.box), FadeIn(hc.hook.glyph),
                      run_time=1.0)
            vo.wait_until("before every commit")
            self.play(Indicate(hc.git.text, color=INK, scale_factor=1.12),
                      ShowPassingFlash(hc.arrows[0].copy().set_stroke(INK, 6), time_width=0.6), run_time=0.8)
            vo.wait_until("It lives in dot git")
            self.play(FadeIn(hook_note, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("every clone installs it again")
            self.play(flash(hook_note, INK, 1.08), run_time=0.8)
            vo.wait_until("It hands over to pre-commit")
            self.play(GrowArrow(hc.arrows[1]), FadeIn(hc.tool, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("which reads the repo's config")
            self.play(GrowArrow(hc.arrows[2]), FadeIn(hc.config, shift=DOWN * 0.15), run_time=0.7)
            ts = hc.turnstile
            self.play(GrowArrow(hc.drop), FadeIn(ts.floor),
                      LaggedStart(*[FadeIn(a, shift=DOWN * 1.5) for a in ts.arches], lag_ratio=0.08),
                      run_time=1.1)

        # ========================================================== 2. the config: nine hooks
        small = Turnstile(9, None, arch_w=0.66, arch_h=1.0, gap=0.26)       # shorter: room for 10 lines;
        # the gate's 0.92 pitch, so "large files" and "merge markers" read as two names
        names = small.name_labels(CHEESE_HOOKS)
        sg = VGroup(small, names)
        sg.move_to([0, 0, 0])
        sg.shift(UP * (-3.52 - sg.get_bottom()[1]))
        panels = [cfg_panel(a, b) for a, b in WINDOWS]
        assert all(p.get_bottom()[1] > sg.get_top()[1] + 0.1 for p in panels), \
            [(p.get_bottom()[1], sg.get_top()[1]) for p in panels]
        which = ((0, 1), (2, 3, 4, 5, 6), (7,), (8,))

        def show_names(idx):
            return LaggedStart(*[FadeIn(names[i], shift=UP * 0.1) for i in idx], lag_ratio=0.2)

        def scroll(old, new, *extra, run_time=0.6):
            new.shift(DOWN * 0.3)
            self.play(FadeOut(old, shift=UP * 0.3), FadeIn(new, shift=UP * 0.3), *extra, run_time=run_time)

        with self.voiceover(SAY[2]) as vo:
            chain = VGroup(hc.links, hc.drop, hook_note)
            self.play(FadeOut(chain), run_time=0.5)
            self.remove(chain, *hc.links, hc.hook.text)
            self.play(ReplacementTransform(ts, small), run_time=0.8)
            self.play(FadeIn(panels[0], shift=UP * 0.2), run_time=0.7)
            vo.wait_until("seven hygiene guards")
            ids0 = VGroup(*[line_bar(panels[0].code, k - 7, TURN, 0.16) for k in (12, 14)])
            self.play(FadeIn(ids0), show_names(which[0]), run_time=0.8)
            vo.wait_until("to private keys")
            scroll(VGroup(panels[0], ids0), panels[1])
            self.play(show_names(which[1]), run_time=1.0)
            vo.wait_until("Then black")
            p2 = panels[2]
            scroll(panels[1], p2, run_time=0.45)
            self.play(show_names(which[2]), Indicate(code_span(p2.code, 32 - 27, "black"), color=TURN,
                                                     scale_factor=1.1), run_time=0.6)
            vo.wait_until("and flake8")
            p3 = panels[3]
            scroll(p2, p3, run_time=0.45)
            self.play(show_names(which[3]), Indicate(code_span(p3.code, 41 - 35, "flake8"), color=TURN,
                                                     scale_factor=1.1), run_time=0.6)
            vo.wait_until("both at width 120")
            u120 = under(code_span(p3.code, 43 - 35, "120"), TURN, stroke=3)
            self.play(Create(u120), each([names[7], names[8]], TURN, 1.15),
                      run_time=0.8)
            vo.wait_until("both seeing only Python files under src")
            bars = VGroup(line_bar(p3.code, 0, TURN, 0.22), line_bar(p3.code, 9, TURN, 0.22))
            self.play(FadeIn(bars), run_time=0.6)
            self.play(each([code_span(p3.code, 0, "^src/"), code_span(p3.code, 9, "^src/")], TURN, 1.12), run_time=0.7)
            vo.wait_until("the tests are never linted")
            never = dashed_chip("tests/ · never matched")
            first = p3.code.code_lines[0]
            never.move_to([first.get_right()[0] + 0.7 + never.width / 2, first.get_center()[1], 0])
            self.play(FadeIn(never, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 3. the README's commit, clean tree (D3)
        t = term(P_LAPTOP, rows=12)
        rec3 = recording_tag()
        rec3.move_to([6.35 - rec3.width / 2, (t.box.get_top()[1] + 2.9) / 2, 0])

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(p3, bars, u120, never, small, names)
            self.play(FadeOut(gone), track(tr, 3), run_time=0.6)
            self.remove(gone)
            self.play(FadeIn(t), run_time=0.4)
            c_ln = typ(self, t, clean.cmd, type_time=1.0)
            vo.wait_until("Pause and run it")
            c_row, c_tag = tag_on(self, c_ln, turn_row)
            self.play(flash(c_tag, TURN), run_time=0.6)
            vo.wait_until("The first run downloads")
            first = out(self, t, clean.at((2, 3)), wrap=True, run_time=0.8)
            out(self, t, clean.at((4, 6), "…"), wrap=True, run_time=0.6)
            vo.wait_until("plus a harmless warning")
            w_row = row_with(first, "[WARNING]")
            wring = ring(substring(w_row, "[WARNING]"), S.GREY, buff=0.05)
            self.play(Create(wring), FadeIn(rec3, shift=LEFT * 0.15), run_time=0.6)
            attach(self, w_row, wring)
            vo.wait_until("Then every hook says skipped")
            self.play(FadeOut(rec3), run_time=0.3)
            self.remove(rec3)
            skipped = out(self, t, fit(clean.at((15, 23))), run_time=0.9)
            sring = ring(skipped, S.GREY, buff=0.06)
            self.play(Create(sring), run_time=0.5)
            attach(self, skipped[0], sring)
            vo.wait_until("git says nothing to commit")
            done = out(self, t, clean.at("…", 27), run_time=0.3)[1]
            dring = ring(done.glyphs, TURN, buff=0.06)
            self.play(Create(dring), run_time=0.5)
            attach(self, done, dring)
            vo.wait_until("hooks check staged files")
            self.play(Indicate(substring(done, "nothing to commit"), color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("nothing was staged")
            self.play(each([substring(r, "(no files to check)") for r in skipped], INK, 1.06, lag=0.08), run_time=0.8)

        # ========================================================== 4. run --all-files (D4): black refuses
        gate = CommitGate(9, CHEESE_HOOKS, with_tray=True)
        gpic = place_gate(gate)

        with self.voiceover(SAY[4]) as vo:
            a_ln = typ(self, t, allf.cmd, type_time=1.0)
            a_row, a_tag = tag_on(self, a_ln, turn_row, anim=track(tr, 4), tm=t)
            res = out(self, t, fit(allf.at((2, 14), "…", 16), {7: ERR, 9: MODIFIED}), run_time=1.0)
            black_ln, mod_ln, ref_ln = res[7], res[9], res[11]
            assert "Black" in black_ln.text and "modified" in mod_ln.text and "reformatted" in ref_ln.text
            vo.wait_until("Pause and run it")
            self.play(flash(a_tag, TURN), run_time=0.6)
            drop_tag(self, a_row, a_tag)
            resize(self, t, 3, keep=[black_ln, mod_ln, ref_ln], extra=[late_in(gpic)], run_time=0.7)
            vo.wait_until("Six hooks pass")
            for i, s in enumerate(["pass", "pass", "pass", "pass", "skip", "pass", "pass"]):
                step_to(self, gate, i, s, run_time=0.15)
            vo.wait_until("one has no files to check")
            self.play(each([gate.arches[4], gate.turnstile.labels[4]], S.GREY, 1.15),
                      run_time=0.6)
            vo.wait_until("then black fails")
            a7 = gate.arches[7]
            self.play(gate.envelope.animate.move_to([a7.get_left()[0] - gate.envelope.width / 2 + 0.3,
                                                     gate.home[1], 0]), a7.to("modified"), run_time=0.4)
            self.play(Indicate(a7, color=MODIFIED, scale_factor=1.15), run_time=0.6)
            vo.wait_until("files were modified by this hook")
            self.play(Indicate(substring(mod_ln, "files were modified by this hook"), color=MODIFIED,
                               scale_factor=1.08), run_time=0.7)
            vo.wait_until("it reformatted utils.py")
            self.play(gate.go_home(), Indicate(substring(ref_ln, "utils.py"), color=INK, scale_factor=1.12),
                      run_time=0.8)
            vo.wait_until("A quick ponder")
            self.play(FadeOut(gpic), run_time=0.5)
            self.remove(gpic)
            card = ponder_card("black just Failed on utils.py.\nflake8 runs next — will it report\n"
                               "the E231 and E303 from before?").move_to([0, 0.75, 0])
            vo.wait_until("flake8 runs next")
            self.play(FadeIn(card, scale=0.95), run_time=0.6)
        ponder_timer(self, card, 6)        # PONDER 3: the card sits above the strip, not over it

        # ========================================================== 5. no: flake8 saw clean code
        pair = pair_card()
        pair.move_to([0, 0.95, 0])
        comma = substring(pair.before, ",")
        fixed = substring(pair.after, ", e")
        c_ring = ring(comma, ERR, buff=0.06)
        f_ul = under(fixed, PASS, stroke=4)
        cap1 = VGroup(label("Failed", 24, ERR), label("≠ broken: black changed the file", 24, INK))
        cap1.arrange(RIGHT, buff=0.15)
        cap1[1].align_to(cap1[0], DOWN)
        cap2 = VGroup(label("look at the change", 24, INK), label("→", 24, S.GREY), label("re-stage", 24, INK))
        cap2.arrange(RIGHT, buff=0.18)
        caps = VGroup(cap1, cap2).arrange(DOWN, buff=0.2)
        caps.next_to(pair, DOWN, buff=0.3)
        assert caps.get_bottom()[1] > -1.4, caps.get_bottom()

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            self.remove(card)
            vo.wait_until("Black had already rewritten the file")
            self.play(FadeIn(VGroup(pair.frame, pair.head, pair.w1, pair.before)), run_time=0.6)
            self.play(Create(c_ring), run_time=0.4)
            self.play(FadeIn(pair.w2), TransformFromCopy(pair.before, pair.after), run_time=0.9)
            self.play(Create(f_ul), c_ring.animate.set_stroke(opacity=0.35), run_time=0.5)
            vo.wait_until("so flake8 saw clean code")
            fl = out(self, t, fit(allf.at(18), {0: PASS}), run_time=0.4)[0]
            self.play(Indicate(substring(fl, "Passed"), color=PASS, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Failed here does not mean broken")
            self.play(FadeIn(cap1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("it means the hook changed files")
            self.play(Indicate(substring(mod_ln, "files were modified"), color=MODIFIED, scale_factor=1.1),
                      Indicate(f_ul, color=PASS), run_time=0.8)
            vo.wait_until("look at the change")
            self.play(FadeIn(cap2[0], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("then re-stage")
            self.play(FadeIn(cap2[1:], shift=RIGHT * 0.15), run_time=0.5)

        # ========================================================== 6. diff, add, commit again (D4x, D3, D5)
        reset_arches(gate)

        with self.voiceover(SAY[6]) as vo:
            rest = VGroup(pair, c_ring, f_ul, caps)
            self.play(FadeOut(rest), run_time=0.5)
            self.remove(rest, *pair, *caps)
            resize(self, t, 12)
            vo.wait_until("git diff shows the fix")
            d_ln = typ(self, t, diff.cmd, type_time=0.4)
            d_row, d_tag = tag_on(self, d_ln, extra_row, anim=track(tr, 4, extra=True))
            out(self, t, fit(diff.at(2, "…", (10, 11), "…", (16, 18)), {2: ERR, 3: PASS, 5: ERR}), wrap=True,
                run_time=0.8)
            vo.wait_until("git add dash u")
            unpin(self, d_row, d_tag)
            g_ln = typ(self, t, add.cmd, type_time=0.4)
            g_row, g_tag = tag_on(self, g_ln, extra_row)
            room(self, t, 1)
            bare_prompt(self, t)
            vo.wait_until("Commit again")
            unpin(self, g_row, g_tag, track(tr, 3, extra=False), run_time=0.4)
            typ(self, t, again.cmd, type_time=0.6)
            k_out = out(self, t, fit(again.at((2, 12))), run_time=0.6, chunk=11)
            vo.wait_until("seven hooks pass")
            gpic = VGroup(gate, gate.turnstile.labels)
            resize(self, t, 3, keep=[k_out[8], k_out[9], k_out[10]], extra=[late_in(gpic)], run_time=0.7)
            main = k_out[9]
            mid = substring(main, "[main b72d50d]")
            mring = ring(mid, PASS, buff=0.05)
            quick_pass(self, gate, ["pass", "pass", "skip", "pass", "skip", "pass", "pass", "pass", "pass"], 0.16,
                       mid.animate.set_color(PASS), Create(mring),
                       Indicate(gate.vault.text, color=PASS, scale_factor=1.15))     # "a real commit enters history"
            attach(self, main, mring)
            vo.wait_until("pause and walk the loop")
            m_row, m_tag = tag_on(self, main, turn_row)
            self.play(flash(m_tag, TURN), run_time=0.6)
            vo.wait_until("plain pre-commit run")
            unpin(self, m_row, m_tag)
            s_ln = typ(self, t, staged.cmd, type_time=0.6)
            s_row, s_tag = tag_on(self, s_ln, turn_row, anim=track(tr, 5))
            vo.wait_until("checks only staged files")
            self.play(gate.turnstile.mark_all(["skip"] * 9, run_time=0.8), run_time=0.8)
            vo.wait_until("everything skips")
            out(self, t, fit(staged.at((2, 10))), run_time=0.8)

        # ========================================================== 7. the refusal (D5 · extra), end of part 1
        mac = mac_chip()
        q = label("this gate never ran a test", 26, TURN)
        qbox = RoundedRectangle(width=q.width + 0.7, height=q.height + 0.5, corner_radius=0.16,
                                stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.95)
        q.move_to(qbox)
        qcard = VGroup(qbox, q).move_to([0, -2.45, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(gpic), track(tr, 5, extra=True), run_time=0.5)
            self.remove(gpic)
            resize(self, t, 12)
            mac.move_to([6.35 - mac.width / 2, (t.box.get_top()[1] + 2.9) / 2, 0])
            vo.wait_until("sed adds and stages")
            b_ln = typ(self, t, brk.cmd, type_time=1.4)
            tag_on(self, b_ln, extra_row)
            room(self, t, 1)
            bare_prompt(self, t)
            vo.wait_until("on a Mac")
            self.play(FadeIn(mac, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("after it.")
            k2 = typ(self, t, blocked.cmd, type_time=0.9)
            tag_on(self, k2, extra_row)
            bl = out(self, t, fit(blocked.at((9, 13), "…", (18, 22)), {0: ERR, 2: ERR, 6: ERR, 10: ERR}),
                     run_time=0.9)
            b9, b18, b22 = bl[0], bl[6], bl[10]
            assert "Black" in b9.text and "Flake8" in b18.text and "F401" in b22.text
            vo.wait_until("black reformats the file")
            self.play(each([substring(b9, "Failed"), substring(bl[2], "files were modified")], ERR, 1.1), run_time=0.7)
            vo.wait_until("flake8 reports F401")
            self.play(Indicate(substring(b22, "F401 'os' imported but unused"), color=ERR, scale_factor=1.08),
                      run_time=0.7)
            reset_arches(gate)
            env = gate.new_envelope("import os")
            gpic = VGroup(gate, gate.turnstile.labels)
            resize(self, t, 3, keep=[b9, b18, b22], extra=[FadeOut(mac), FadeOut(ref), late_in(gpic)],
                   run_time=0.7)
            self.remove(mac, ref)
            vo.wait_until("which no formatter can fix")
            for i, s in enumerate(["pass", "pass", "skip", "pass", "skip", "pass", "pass"]):
                step_to(self, gate, i, s, run_time=0.14)
            step_to(self, gate, 7, "modified", run_time=0.3)
            a8 = gate.arches[8]
            self.play(env.animate.move_to([a8.get_left()[0] - env.width / 2 + 0.3, gate.home[1], 0]),
                      a8.to("fail"), run_time=0.35)
            self.play(Indicate(a8, color=ERR, scale_factor=1.15), gate.go_home(), run_time=0.7)
            vo.wait_until("git status confirms")
            typ(self, t, status.cmd, type_time=0.4)
            still = out(self, t, status.at((2, 3), "…", (6, 8)), run_time=0.6)[3:]
            assert still[0].text.startswith("Changes to be committed"), still[0].text
            stag = beside(row_tag("still staged · not committed", TURN), still[0])
            pin(self, still[0], stag)
            self.play(each([env.text, gate.tray.shape, gate.tray.text], TURN, 1.12), run_time=0.7)
            vo.wait_until("Restore the file")
            r_ln = typ(self, t, restore.cmd, type_time=0.8)
            tag_on(self, r_ln, extra_row, anim=FadeOut(env, shift=DOWN * 0.3))
            gate.remove(env)
            self.remove(env)
            gate.envelope = None
            vo.wait_until("your machine now says no")
            self.play(Indicate(gate.vault.door[1], color=INK, scale_factor=1.25),
                      each([gate.arches[7], gate.arches[8]], ERR, 1.1), run_time=0.9)
            vo.wait_until("But this gate never ran")
            self.play(FadeOut(t), run_time=0.4)
            self.remove(t)
            self.play(FadeIn(qcard, scale=0.9), each(list(gate.arches), S.GREY, 1.08, lag=0.06),
                      run_time=0.8)
            vo.wait_until("Part 2 builds one")
            corner = [6.5 - qcard.width / 2, 3.55 - qcard.height / 2, 0]
            self.play(qcard.animate.move_to(corner), run_time=1.0)
            vo.wait_until("what even it can miss")
            self.play(Indicate(q, color=TURN, scale_factor=1.06), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


def ponder_timer(scene, card, seconds: float) -> None:
    """pause_and_ponder's timer for a card already on screen (it went up during the narration)."""
    bar = card[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
