"""S03 · Get the code: clone, or switch branches (README "Get the Code", both ways in; V2).

Beats (script.md "## S03", one voiceover block each):
 0  TRACKER F/1. The 12-row terminal (title `laptop`, prompt ~/AC215) and a GREY note under the
    tracker "~/AC215 = the README's <your-workspace>" (the prompt's ~/AC215 flashes). It types the
    README's `git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git`
    (house fold: three rows ending in " \\") -> mega-laptop/01 line 2; `--branch
    flexible-workflow` (its own row) flashes, gets a GREY underline and, beside it, the GREY label
    "checks out this branch · the others come along". TRACKER F/2: `cd mega-pipeline` (no
    output), the new path part flashes BLUE. ▶ your turn on the cd row.
 1  TRACKER F/2 · extra. The terminal clears; `git branch` and `git log --oneline -1` (the two
    commands of mega-laptop/03, typed separately, each with an `extra` tag) -> lines 2, 3;
    `* flexible-workflow` flashes, `cc67f3b` flashes and flies up under the tracker into the GREY
    note "cc67f3b = the commit we recorded · 2026-09-18 · yours may be newer". `ls -a
    transcribe_audio` (extra; the second command of mega-laptop/04) -> lines 10-18 (the two `git branch` rows scroll away); Dockerfile, docker-shell.sh,
    pyproject.toml, uv.lock turn GREEN as they are named and a copy of each flies into a GREEN
    recipe card; its caption "committed" on "which you wrote".
 2  TRACKER L/1 (the tracker switches section). The terminal clears, title `laptop · lecture 3
    clone`, prompt ~/AC215-l03; GREY chip top right "cloned fresh? skip to 4:59" (SKIP_TO).
    `cd mega-pipeline` (no output). TRACKER L/1 · extra: `git status --short` -> mega-l03-laptop/01
    lines 2-4, `git status --short --ignored | grep '^!!'` -> lines 5-8 (both extra).
 3  On "Three piles", copies of the seven status lines fly into V2's three piles while the
    terminal shrinks to the 3-row strip (markers -> pile names, folders -> pile headers, file
    names -> rows, mega-pipeline.json -> the GOLD key). YELLOW pencil "edited" as cli.py is
    named, the tracked label on "is tracked"; untracked rows, then their label; ignored rows flash
    one by one, the key pulses and gets the tag "stand-in file · not a real key" (under the key);
    the dashed frame flashes.
 4  TRACKER L/2. README chip under the tracker: README.md · line 43 "# get the branches you
    don't have yet". The strip types `git fetch origin` -> the prompt returns (it flashes); the
    chip's phrase flashes on "a clone already has every branch"; the GREY tag "nothing new
    upstream · yours may list updates" in the top band (flashes on "Yours may").
 5  TRACKER L/3. V2 and the chip fade; the terminal grows to 13 rows (cleared): `git checkout
    flexible-workflow` -> mega-l03-laptop/04 lines 2-9 (wrap): 13 rows, nothing scrolls. RED
    bracket "1" on lines 2-4, RED bracket "2" on lines 5-8, `Aborting` underlined RED.
 6  The brackets go; the strip keeps the last three rows (`Aborting` and its underline); V2
    returns with the branch's files waiting above it (stand-in tag put away); RED wall 1 rises
    over the edited cli.py (which flashes RED), wall 2 over the untracked pile; the files slide
    down and stop at the walls (a small bump). "Nothing changed": `Aborting` flashes.
 7  TRACKER L/4. README chip under the tracker: line 48 "Either stash them (git stash) or throw
    them away (git checkout -- .)". `git stash` -> 05 line 2 (cut); cli.py lifts into a stash box,
    the pencil fades, wall 1 falls. The retry `git checkout flexible-workflow` is typed as that
    sentence ends; on "On a retry" -> 06 lines 2-6 (wrap; the
    strip ends on `Please move or remove them …`, `Aborting`); the files bump wall 2, which
    flashes RED and stays.
 8  TRACKER L/4 · extra. The tag `erratum · covers only edited files` over the chip's right end.
    `git stash -u` (extra) -> 07 line 2 (cut); the untracked pair lifts into a second stash box,
    wall 2 falls. TRACKER L/4: `git checkout flexible-workflow` -> 08 lines 2-3; line 3 turns
    GREEN and the branch's files land: four in the tracked frame, two in the untracked one; the
    branch name fades as they land. Above the piles: the GREY chip `git checkout -- .` (shown,
    never typed) and its notes, RED "throws your edits away", GREY "leaves untracked files where
    they are", each as it is said.
 9  TRACKER L/5. `git branch` -> 09 lines 2-3, `* flexible-workflow` GREEN. V2 and the chips
    fade; a static GREY "your turn" card with ▶ your turn, right-aligned above the strip: first a
    serif block "first: copy out your lecture 3 Dockerfile, / pyproject.toml, uv.lock · the switch
    replaces them" (tag extra), then the seven commands as typed (`git stash -u` tagged extra). The
    block flashes YELLOW with the ▶ wiggle on "Pause and switch" (on "Before you switch" once
    script.md carries that sentence).
10  TRACKER L/5 · extra. The card clears; the strip grows to 4 rows; V2 returns (state after the
    switch). `head -2 transcribe_audio/Dockerfile` (extra; its tag with a flash of the ignored
    Dockerfile on "lecture 3 Dockerfile") -> 11 lines 2-3; an excerpt chip
    `FROM python:3.12-slim-bookworm` (mega-l03-laptop/01 line 9, "line 1 · before") appears
    above the ignored pile, the ignored Dockerfile card flips and the chip becomes
    `FROM python:3.14-slim-bookworm` (11 line 3, "line 2 · after"). `ls -la transcribe_audio`
    (extra) -> 10 lines 12, "…", 14; the pyproject.toml and uv.lock cards flip; GREY tag "the
    branch's files · same sizes as a fresh clone"; GREY tag "replaced · no warning" + `erratum`;
    a GREY fix card "want your lecture 3 Dockerfile, / pyproject.toml, uv.lock (or
    docker-shell.sh)? / copy them out before switching".
11  The key glows on "The old key"; `ls transcribe_audio/secrets` (extra) -> 11 line 4, the line
    and V2's secrets/ row pulse GOLD. README chip line 50 "Your secrets/ folder … stay put" (its
    phrase flashes on "as the README says"); the key flashes RED on "Every build there". GREY
    fix card "delete each
    <component>/secrets/ now · your key goes in secrets/ beside the repo · why: end of part 1".
    `git stash list` (extra, typed on "secrets folder now") -> 10 lines 21-22 (cut) on "Your
    edits wait"; on "in the stash" the pair's box becomes `stash@{0}`, the cli.py box
    `stash@{1}`. Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 0: the house fold puts `--branch flexible-workflow` on its own row, so its label sits
  beside that row instead of above the terminal.
- Beat 1: the capture's `git branch; git log --oneline -1` and `ls; ls -a transcribe_audio` are
  typed as separate commands (conventions: `;` lines are typed one command at a time; `ls` is not
  shown, so it is not typed). The terminal does not clear before `ls -a`: it scrolls, so the
  `cc67f3b …` row stays on screen while the sentence goes on.
- Beat 1: the recipe card holds all four files the SHOW highlights (docker-shell.sh included).
- Beat 1: the commit note sits under the tracker, not beside `cc67f3b …`: the row leaves 4.3 units
  and the note is 7.3 wide; the hash flies from the row into the note. The SAY anchor is "at the
  commit we recorded" once script.md says so, "at the pinned commit" until then (said()).
- Beat 2: the chip names the time S04 starts (SKIP_TO) instead of "the next chapter": the part 1
  upload may carry no chapter marks.
- Beat 9: the card leads with the lecture 3 files warning (the switch replaces them silently, and
  `git stash -u` does not save ignored files), so it comes before the pause, not after it in
  beat 10; nine rows fit only 0.14 apart and right-aligned (its top passes the tracker band).
- Beat 3: the strip keeps the second status command and the prompt; copies of the seven output
  lines sort into the piles line by line while the terminal shrinks, all on "Three piles" (a
  separate lift first put the pencil 2 s behind "Your edited cli.py"), then each pile is
  emphasised as it is named. The stand-in tag sits under the key, clear of the untracked frame
  (centred on the ignored frame, it covered that frame's corner).
- Beat 4: the tag "nothing new upstream · yours may list updates" (6.7 wide) sits in the top band
  right of the tracker: it fits neither beside the returned prompt in the strip nor beside the
  README chip, which is under the tracker because at 7.7 wide it doesn't fit right of it.
- Beats 4, 7, 11: README chips sit under the tracker, not right of it (too wide for the top band).
- Beat 6: the branch's files wait just above the walls and slide ~0.6 down: higher, they would
  cross the tracker.
- Beat 8: the erratum tag sits in the top band over the README chip's right end (on the chip's
  top edge it crossed the frame next to the quote). The branch's files land split four/two in
  the emptied frames (ThreePiles.land() leaves the six-file row across both frames, its last
  file on the tracked frame's edge and the branch name inside the untracked frame).
- Tags with an opaque fill flash with flash_tag() (text + outline): Indicate on the whole tag
  painted the fill white over the text.
- Beats 6-9: V2 sits lower than in beats 3-4 (frames on the strip) and its stand-in tag is put
  away (it would cross the strip); beats 10-11 raise V2 above a 4-row strip.
- Beat 10: the FROM chip shows the lecture 3 line as V2 returns, before `head -2` is typed (the
  narration names the old Dockerfile first). The strip grows to 4 rows so `ls -la
  transcribe_audio` stays on screen with its three output rows; its `extra` tag sits on the
  strip's title bar (the 64-character row has no room).
  `ls -la transcribe_audio` is typed as the SHOW gives it; the capture ran
  `ls -la transcribe_audio transcribe_audio/secrets`, whose rows 12, "…", 14 are printed: the cut
  (secrets/) is marked, and row 8 (Dockerfile) is left out because head -2 has just shown that
  file replaced and the 4-row strip holds the command and three rows (six would push V2 into the
  chips above it).
- Rows of 60+ characters (the long prompts) take a 20 pt `extra` tag at the frame's edge.
- Beats 10-11: the fix chips are 3-line GREY cards at the top right (as one-line chips they are
  13+ wide); beat 10's "replaced · no warning" + `erratum` sit under the tracker.
"""

from common import *
from common import _hidden, _set_op
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    RoundedRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Wiggle,
    there_and_back,
)

from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]
assert len(SAY) == 12, len(SAY)

ML, L3 = "mega-laptop", "mega-l03-laptop"

# ------------------------------------------------------------------ commands and real outputs
CLONE = capture("01", ML)
assert CLONE.cmd == "git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git"
CLONE_OUT = CLONE.at(2)
assert CLONE_OUT == ["Cloning into 'mega-pipeline'..."]
CD = capture("02", ML)
assert CD.cmd == "cd mega-pipeline" and not CD.lines
_br = capture("03", ML)
BRANCH_F, LOG1 = _br.cmd.split("; ")
assert (BRANCH_F, LOG1) == ("git branch", "git log --oneline -1")
BRANCH_OUT, LOG_OUT = _br.line(2), _br.line(3)
assert BRANCH_OUT == "* flexible-workflow" and LOG_OUT.startswith("cc67f3b ")
_ls = capture("04", ML)
LS_A = _ls.cmd.split("; ")[1]
assert LS_A == "ls -a transcribe_audio"
LS_OUT = _ls.at((10, 18))
assert LS_OUT[0] == "." and LS_OUT[-1] == "uv.lock" and "docker-shell.sh" in LS_OUT
RECIPE = ["Dockerfile", "docker-shell.sh", "pyproject.toml", "uv.lock"]

_st = capture("01", L3)
ST1, ST2, _head1 = _st.cmd.split("; ")
assert (ST1, ST2) == ("git status --short", "git status --short --ignored | grep '^!!'")
ST1_OUT, ST2_OUT = _st.at((2, 4)), _st.at((5, 8))
assert ST1_OUT[0] == " M transcribe_audio/cli.py" and ST2_OUT[2].endswith("secrets/mega-pipeline.json")
FROM_OLD = _st.line(9)
assert _head1 == "head -1 transcribe_audio/Dockerfile" and FROM_OLD == "FROM python:3.12-slim-bookworm"
assert capture("02", L3).cmd == CD.cmd
FETCH = capture("03", L3)
assert FETCH.cmd == "git fetch origin" and not FETCH.lines
CHECKOUT = capture("04", L3)
assert CHECKOUT.cmd == "git checkout flexible-workflow"
CO_OUT = CHECKOUT.at((2, 9))
assert CO_OUT[-1] == "Aborting"
STASH = capture("05", L3)
assert STASH.cmd == "git stash"
STASH_OUT = STASH.at(2)
CO2 = capture("06", L3)
assert CO2.cmd == CHECKOUT.cmd
CO2_OUT = CO2.at((2, 6))
STASH_U = capture("07", L3)
assert STASH_U.cmd == "git stash -u"
CO3 = capture("08", L3)
assert CO3.cmd == CHECKOUT.cmd
CO3_OUT = CO3.at((2, 3))
assert CO3_OUT[1] == "Switched to a new branch 'flexible-workflow'"
BR3 = capture("09", L3)
assert BR3.cmd == "git branch"
BR3_OUT = BR3.at((2, 3))
_after = capture("10", L3)
LS_LA = "ls -la transcribe_audio"                     # as script.md gives it (see the docstring)
assert _after.cmd.split("; ")[1].startswith(LS_LA + " ")
LA_OUT = _after.at(12, "…", 14)                       # the cut (line 13, secrets/) marked "…"
assert [s.split()[-1] for s in LA_OUT] == ["pyproject.toml", "…", "uv.lock"]
assert [LA_OUT[0].split()[4], LA_OUT[2].split()[4]] == ["249", "85761"]   # = the branch's files at cc67f3b
assert _after.line(8).split()[4] == "1274"            # Dockerfile: proven by head -2 (FROM ... 3.14)
STASH_LIST = _after.cmd.split("; ")[2]
assert STASH_LIST == "git stash list"
LIST_OUT = _after.at(21, 22)
assert LIST_OUT[0].startswith("stash@{0}: ") and LIST_OUT[1].startswith("stash@{1}: ")
_rep = capture("11", L3)
HEAD2, LS_SEC = _rep.cmd.split("; ")
assert (HEAD2, LS_SEC) == ("head -2 transcribe_audio/Dockerfile", "ls transcribe_audio/secrets")
HEAD2_OUT, SEC_OUT = _rep.at(2, 3), _rep.at(4)
FROM_NEW = HEAD2_OUT[1]
assert FROM_NEW == "FROM python:3.14-slim-bookworm" and SEC_OUT == ["mega-pipeline.json"]

# ------------------------------------------------------------------ README quotes (assets/source)
README = "mega-pipeline/README.md"
L43 = excerpt(README, 43, 43)
L48 = excerpt(README, 48, 48).replace("`", "")
L50 = excerpt(README, 50, 50).replace("`", "")
PH43 = "# get the branches you don't have yet"
PH48 = "Either stash them (git stash) or throw them away (git checkout -- .)"
PH50 = "Your secrets/ folder … stay put"
assert PH43 in L43 and PH48 in L48
assert L50.startswith("Your secrets/ folder ") and "stay put" in L50
assert excerpt(README, 35, 36) == f"{CLONE.cmd}\n{CD.cmd}"
assert excerpt(README, 42, 45).split("\n")[1].startswith(FETCH.cmd + " ")

# ------------------------------------------------------------------ layout
Y_UNDER = 2.57          # the row under the tracker (tracker bottom 2.92)
Y_BAND = 3.21           # the top band, right of the tracker
X_R = 6.32              # right edge for chips and cards
V2_P1 = 0.52            # V2's shift from its built position: beats 3-4 (stand-in tag on)
V2_P2 = 0.19            # beats 6-9 (frames just above the 3-row strip, stand-in tag off)
V2_P3 = 0.61            # beats 10-11 (above a 4-row strip)
INCOMING_Y = 2.66       # where the branch's files wait (just under the tracker)
# Beat 2's "cloned fresh? skip to …" chip: where S04 starts in the full video and in part 1 (part 1
# starts at 0:00), i.e. S01 + S02 + S03 durations, rounded down: re-check it whenever S01-S03 change
# length. It must never land after S04's start; landing a second or two early (in this scene's
# fade-out) is fine. 2026-10-17 QA draft: S01 90.86 + S02 73.13 + S03 135.72 = 299.7 (4:59.7);
# after this pass S03 ends at 135.7 (explainer.check) / 136.0 (720p30): S04 at ~299.9.
SKIP_TO = "4:59"


def at_left(m, x: float, y: float):
    return m.move_to([x + m.width / 2, y, 0])


def at_right(m, x: float, y: float):
    return m.move_to([x - m.width / 2, y, 0])


def show(m):
    """FadeIn for a member hidden with _hidden() (as Piece.parts_in does)."""
    _set_op(m)
    m.hidden = False
    return FadeIn(m)


def morph(src, dst):
    """(mover, Transform): a copy of `src` (terminal glyphs) becomes the hidden member `dst`;
    after the play, remove the mover and _set_op(dst)."""
    _set_op(dst)
    tgt = dst.copy()
    _set_op(dst, 0)
    mv = src.copy()
    return mv, Transform(mv, tgt)


def note_card(lines, color: str = S.GREY):
    """A GREY card of 1-3 serif lines (a fix chip too long for one line)."""
    return card_rows(lines, frame_color=color, buff=0.1)


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def flash_tag(tg, color: str = S.WHITE, k: float = 1.08, run_time: float = 0.8) -> list:
    """Indicate for a tag (opaque dark fill): the text takes `color`, the pill's outline glows,
    the fill stays dark (Indicate on the whole tag would paint the fill and hide the text).
    Two animations, not an AnimationGroup: the group a play adds to the scene would draw the
    pill again over its text. Use as self.play(*flash_tag(t))."""
    return [Indicate(tg.text, color=color, scale_factor=k, run_time=run_time),
            tg.box.animate(rate_func=there_and_back, run_time=run_time).set_stroke(color).scale(k)]


def land_split(v2, run_time: float = 1.0) -> list:
    """The branch's files land in the emptied piles: four in the tracked frame, two in the
    untracked one (ThreePiles.land() would leave the six-file row across both frames, its last
    file on the tracked frame's edge and the branch name inside the untracked frame); the
    branch name fades as they land (the strip's GREEN "Switched to a new branch" says it)."""
    files, name = v2.incoming[0], v2.incoming[1]
    tgt = files.copy()
    VGroup(*tgt[:4]).arrange(RIGHT, buff=0.26).move_to(v2.piles["tracked"].frame)
    VGroup(*tgt[4:]).arrange(RIGHT, buff=0.26).move_to(v2.piles["untracked"].frame)
    drop = v2.piles["tracked"].frame.get_center()[1] - files.get_center()[1]
    return [Transform(files, tgt, run_time=run_time),
            name.animate(run_time=run_time * 0.6).shift(UP * drop * 0.5).set_opacity(0),
            Indicate(v2.piles["tracked"].frame, color=VENV, scale_factor=1.0, run_time=run_time),
            Indicate(v2.piles["untracked"].frame, color=VENV, scale_factor=1.0, run_time=run_time)]


def bump(m, d: float = 0.12):
    return m.animate(rate_func=there_and_back).shift(DOWN * d)


def slim_tag(s: str, color: str = S.GREY) -> VGroup:
    """A 20 pt tag one row high with tight padding (for a nearly full terminal row)."""
    txt = label(s, CAPTION, color)
    h = 0.34
    b = RoundedRectangle(width=txt.width + 0.26, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    txt.move_to(b)
    g = VGroup(b, txt)
    g.box, g.text = b, txt
    return g


def fit_tag(t, line, s: str = "extra"):
    """A GREY tag beside terminal line `line` (its last row): the house 22 pt tag, a 20 pt one,
    or a slim 20 pt one at the frame's edge when the row leaves little room. Not added."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    end = row.glyphs.get_right()[0]
    for size in (TAG, CAPTION):
        tg = beside(tag(s, S.GREY, size=size), t, line)
        if tg.get_left()[0] >= end + 0.1:
            return tg
    tg = slim_tag(s)
    tg.move_to([t.box.get_right()[0] - 0.07 - tg.width / 2, row.strut.get_center()[1], 0])
    if tg.get_left()[0] < end + 0.08:
        raise ValueError(f"no room for the tag {s!r} beside {row.text!r}")
    return tg


def tprint(scene, t, lines, wrap: bool = False, run_time: float = 0.5, lag: float = 0.12):
    """Terminal.print, but never more rows at once than the terminal has (Terminal.print would
    place the extra rows below the frame): long lines fold at the row width (wrap) or are cut."""
    rows = []
    for s in lines:
        if wrap:
            while len(s) > t.max_chars:
                rows.append(s[:t.max_chars])
                s = s[t.max_chars:]
        rows.append(s)
    out = VGroup()
    chunks = [rows[i:i + t.rows] for i in range(0, len(rows), t.rows)]
    for c in chunks:
        out.add(*t.print(scene, c, run_time=run_time / len(chunks), lag=lag))
    return out


def said(say: str, *phrases: str) -> str:
    """The first of `phrases` that the SAY line contains: the anchor survives a pending script.md
    rewording (the last phrase is the current wording; neither found -> the usual warning)."""
    return next((p for p in phrases if p in " ".join(say.split())), phrases[-1])


def first_turn_card(first: list[str], cmds: list, buff: float = 0.14) -> VGroup:
    """turn_card with a serif "first" block (lines 0.16 apart, so the extra tag on the first line
    clears the second) above the commands, rows `buff` apart (turn_card's 0.2 would push the nine
    rows into the tracker band). .frame .rows .tag .first as turn_card; the block is drawn over
    the frame."""
    c = turn_card(cmds)
    lines = VGroup(*[label(s, CAPTION, INK) for s in first]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    xt = extra_tag().next_to(lines[0], RIGHT, buff=0.3)
    block = VGroup(lines, xt)
    c.rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    body = VGroup(block, c.rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    c.frame.become(box(body.width + 0.6, body.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95,
                       radius=0.14))
    body.move_to(c.frame).align_to(c.frame, LEFT).shift(RIGHT * 0.3)
    c[2].next_to(c.frame, UP, buff=0.08).align_to(c.frame, LEFT).shift(RIGHT * 0.12)   # "your turn"
    c.tag.move_to(c.frame.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    c.add(block)
    c.first = block
    return c


class GetTheCode(VoiceScene):
    def construct(self):
        tr = tracker("F", 1)
        t = term(P_WS, rows=12)

        # ========================================================== 0 · clone the branch, cd
        # the paths in mono: the serif face draws "~" as a raised accent
        ws_note = VGroup(mono("~/AC215", CAPTION, S.GREY), note("= the README's"),
                         mono("<your-workspace>", CAPTION, S.GREY)).arrange(RIGHT, buff=0.15)
        at_left(ws_note, -6.45, Y_UNDER)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            p0 = bare_prompt(self, t)
            vo.wait_until("From your workspace folder")
            tilde = glyph_range(p0, P_WS.index("~"), len(P_WS) - 1)
            self.play(FadeIn(ws_note, shift=DOWN * 0.1), flash(tilde, TURN, 1.2, 0.9))
            vo.wait_until("clone the repo")
            cl = type_cmd(self, t, CLONE.cmd, type_time=1.8)
            t.print(self, CLONE_OUT, run_time=0.4)
            vo.wait_until("dash dash branch")
            frow = next(r for r in cl.rows if "--branch flexible-workflow" in r.text)
            flag = substring(frow, "--branch flexible-workflow")
            self.play(flash(flag, TURN, 1.1, 0.8))
            ul = under(flag, S.GREY, stroke=3)
            lab = beside(note("checks out this branch · the others come along"), t, frow, buff=0.35)
            pin(self, frow, ul, anim=Create(ul), run_time=0.4)
            pin(self, frow, lab, run_time=0.5)

            vo.wait_until("Then cd into")
            self.play(tr.goto(2), run_time=0.5)
            cdl = type_cmd(self, t, CD.cmd, type_time=0.6)
            cd_prompt(self, t, P_REPO)
            yt0 = beside(your_turn(), t, cdl)
            pin(self, cdl, yt0, run_time=0.4)
            vo.wait_until("Pause and run both")
            self.play(Wiggle(yt0, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 1 · two extra checks
        # under the tracker (where beat 0's workspace note was): beside the `cc67f3b …` row only 4.3
        # of its 7.3 units fit; the hash flies up from the row into it
        rec = VGroup(mono("cc67f3b", CAPTION, S.GREY),
                     note("= the commit we recorded · 2026-09-18 · yours may be newer")).arrange(RIGHT, buff=0.15)
        at_left(rec, -6.45, Y_UNDER)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ws_note), caption_extra(tr, True), run_time=0.4)
            t.clear(self, run_time=0.3)
            b1 = type_cmd(self, t, BRANCH_F, type_time=0.45)
            pin(self, b1, fit_tag(t, b1), run_time=0.3)
            bo = t.print(self, [BRANCH_OUT], run_time=0.3)[0]
            vo.wait_until("git branch shows")
            self.play(flash(substring(bo, "flexible-workflow"), TURN, 1.15))
            g1 = type_cmd(self, t, LOG1, type_time=0.8)
            pin(self, g1, fit_tag(t, g1), run_time=0.3)
            lo = t.print(self, [LOG_OUT], run_time=0.3)[0]
            vo.wait_until(said(SAY[1], "at the commit we recorded", "at the pinned commit"))
            sha = substring(lo, "cc67f3b")
            self.play(flash(sha, TURN, 1.2))
            self.play(TransformFromCopy(sha, rec[0]), FadeIn(rec[1], shift=RIGHT * 0.15), run_time=0.6)

            vo.wait_until("and transcribe audio holds")
            la = type_cmd(self, t, LS_A, type_time=0.9)
            pin(self, la, fit_tag(t, la), run_time=0.3)
            lso = t.print(self, LS_OUT, run_time=0.6, lag=0.08)
            rows = {s: ln for s, ln in zip(LS_OUT, lso)}
            card = recipe_card(files=RECIPE, caption="committed")
            card.move_to([3.3, rows["cli.py"].strut.get_center()[1], 0])
            for i, (name, cue) in enumerate(zip(RECIPE, ("its Dockerfile", "the script",
                                                         "pyproject.toml and", "uv.lock, which"))):
                vo.wait_until(cue)
                ln = rows[name]
                self.play(ln.glyphs.animate.set_color(VENV), *([FadeIn(VGroup(card.frame, card[1]))]
                                                               if i == 0 else []), run_time=0.3)
                self.play(TransformFromCopy(ln.glyphs, card.rows[i]), flash(ln.glyphs, VENV, 1.12),
                          run_time=0.6)
            vo.wait_until("which you wrote")
            self.play(FadeIn(card.caption, shift=UP * 0.1), flash(card.frame, VENV, 1.04), run_time=0.6)

        # ========================================================== 2 · the lecture 3 clone
        fresh = chip(f"cloned fresh? skip to {SKIP_TO}", S.GREY, size=CAPTION)
        at_right(fresh, X_R, Y_UNDER)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(card), FadeOut(rec), run_time=0.3)
            tr = switch_section(self, tr, "L", 1)
            t.clear(self, run_time=0.3)
            t.set_prompt(P_L03)
            self.play(retitle(t, "laptop · lecture 3 clone"), run_time=0.5)
            p2 = bare_prompt(self, t)
            self.play(flash(t.title, S.WHITE, 1.1),
                      flash(glyph_range(p2, P_L03.index("~"), len(P_L03) - 1), CLOUD, 1.1), run_time=0.8)
            vo.wait_until("if you cloned fresh")
            self.play(FadeIn(fresh, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("Step 1")
            type_cmd(self, t, CD.cmd, type_time=0.6)
            cd_prompt(self, t, P_L03_REPO, run_time=0.6)
            self.play(caption_extra(tr, True), run_time=0.3)
            vo.wait_until("Two extra checks")
            s1 = type_cmd(self, t, ST1, type_time=0.55)
            pin(self, s1, fit_tag(t, s1), run_time=0.25)
            st_a = t.print(self, ST1_OUT, run_time=0.35)
            s2 = type_cmd(self, t, ST2, type_time=0.9)
            pin(self, s2, fit_tag(t, s2), run_time=0.25)
            st_b = t.print(self, ST2_OUT, run_time=0.4)
            bp2 = bare_prompt(self, t)

        # ========================================================== 3 · three piles (V2)
        v2 = ThreePiles()
        v2.shift(UP * V2_P1)
        P = v2.piles
        hidden = [v2.pencil, v2.key]
        for p in P.values():
            hidden += [p.frame, p.kind, p.folder]
            for r in p.rows:
                hidden += [r.glyph, r.text]
        for m in hidden:
            _hidden(m)
        # the stand-in tag sits under the key, clear of the untracked frame's corner (centred on
        # the ignored frame, its left end covered that corner)
        st_tag = v2.parts["standin"]
        st_tag.set_x(v2.key.get_center()[0])
        st_tag.shift(RIGHT * max(0.0, P["untracked"].frame.get_right()[0] + 0.15 - st_tag.get_left()[0]))
        status = list(st_a) + list(st_b)
        kinds = {"M": "tracked", "??": "untracked", "!!": "ignored"}
        pairs, groups, movers = [], [], []
        for ln in status:                      # each status line splits: marker, folder, file
            mark, path = ln.text.split()
            pile = kinds[mark]
            folder, name = path.split("/", 1)
            mine = [(substring(ln, mark), P[pile].kind), (substring(ln, folder + "/"), P[pile].folder)]
            if name == "secrets/mega-pipeline.json":
                mine += [(substring(ln, "secrets/"), v2.row(pile, "secrets/").text),
                         (substring(ln, "mega-pipeline.json"), v2.key)]
            else:
                mine.append((substring(ln, name), v2.row(pile, name).text))
            mv, an = zip(*[morph(a, b) for a, b in mine])
            pairs += mine
            movers += mv
            groups.append(AnimationGroup(*an))
        glyphs = [r.glyph for p in P.values() for r in p.rows]
        with self.voiceover(SAY[3]) as vo:
            self.add(*movers)
            # the seven lines fly into the piles while the terminal shrinks to the strip (which
            # keeps the command that printed them): all of it on "Three piles"
            frames = [p.frame for p in P.values()]
            for f in frames:
                _set_op(f)               # not on screen yet: Create brings each frame in
            resize(self, t, 3, keep=[*s2.rows, bp2], run_time=1.2,
                   extra=(LaggedStart(*groups, lag_ratio=0.15), *[Create(f) for f in frames],
                          FadeOut(fresh)))
            self.remove(*movers, *frames)
            self.add(v2)
            for _, dst in pairs:
                _set_op(dst)

            vo.wait_until("Your edited cli.py")
            self.play(*[show(g) for g in glyphs], show(v2.pencil),
                      flash(v2.row("tracked", "cli.py").text, TURN, 1.2), run_time=0.8)
            vo.wait_until("is tracked")
            self.play(flash(P["tracked"].kind, VENV, 1.2), flash(P["tracked"].frame, VENV, 1.04),
                      run_time=0.8)
            vo.wait_until("Your two new files")
            self.play(flash(P["untracked"].rows, S.WHITE, 1.12, 0.8))
            vo.wait_until("are untracked")
            self.play(flash(P["untracked"].kind, S.WHITE, 1.2), flash(P["untracked"].frame, S.WHITE, 1.03),
                      run_time=0.8)
            vo.wait_until("In transcribe audio")
            self.play(flash(P["ignored"].folder, S.WHITE, 1.15, 0.6))
            for name, cue in (("Dockerfile", "the Dockerfile, pyproject"),
                              ("pyproject.toml", "pyproject.toml, uv.lock"),
                              ("uv.lock", "uv.lock and the key")):
                vo.wait_until(cue)
                self.play(flash(v2.row("ignored", name).text, S.WHITE, 1.15, 0.5))
            vo.wait_until("and the key")
            self.play(flash(v2.key, KEY, 1.4, 0.7), *v2.parts_in("standin"), run_time=0.7)
            vo.wait_until("are ignored")
            self.play(flash(P["ignored"].kind, S.WHITE, 1.2), flash(P["ignored"].frame, S.WHITE, 1.03))

        # ========================================================== 4 · git fetch origin
        chip43 = at_left(readme_chip("README.md · line 43", PH43, max_w=12.6), -6.45, Y_UNDER)
        quiet = at_right(grey_tag("nothing new upstream · yours may list updates"), X_R, Y_BAND)
        with self.voiceover(SAY[4]) as vo:
            self.play(tr.goto(2), FadeIn(chip43, shift=DOWN * 0.1), run_time=0.6)
            type_cmd(self, t, FETCH.cmd, type_time=0.7)
            back = bare_prompt(self, t)
            vo.wait_until("Here it prints nothing")
            self.play(flash(back.glyphs, TURN, 1.08, 0.9))
            vo.wait_until("a clone already has")
            self.play(flash(chip43.phrase, S.WHITE, 1.06, 0.9))
            vo.wait_until("and nothing had changed")
            self.play(FadeIn(quiet, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("Yours may list updates")
            self.play(*flash_tag(quiet, S.WHITE, 1.08, 0.8))

        # ========================================================== 5 · checkout refuses
        with self.voiceover(SAY[5]) as vo:
            self.play(tr.goto(3), FadeOut(chip43), FadeOut(quiet), FadeOut(v2), run_time=0.5)
            resize(self, t, 13, keep=0, run_time=0.6)
            type_cmd(self, t, CHECKOUT.cmd, type_time=0.9)
            vo.wait_until("and Git refuses")
            co = t.print(self, CO_OUT, wrap=True, run_time=0.7, lag=0.06)
            assert len(t.lines) == 13 and co[-1].text == "Aborting"
            n1 = sum(-(-len(s) // t.max_chars) for s in CO_OUT[:3])      # rows of lines 2-4
            n2 = sum(-(-len(s) // t.max_chars) for s in CO_OUT[3:7])     # rows of lines 5-8
            br1 = bracket(list(co[:n1]), "1")
            br2 = bracket(list(co[n1:n1 + n2]), "2")
            abort = co[-1]
            ul_ab = under(abort.glyphs, ERR)
            vo.wait_until("for two reasons")
            self.play(FadeIn(br1, shift=RIGHT * 0.1), run_time=0.4)
            self.play(FadeIn(br2, shift=RIGHT * 0.1), run_time=0.4)
            pin(self, abort, ul_ab, anim=Create(ul_ab), run_time=0.4)

        # ========================================================== 6 · two walls
        _hidden(v2.parts["standin"])
        v2.shift(DOWN * (V2_P1 - V2_P2))
        inc = v2.incoming
        inc.shift(UP * (INCOMING_Y - inc.get_center()[1]))
        with self.voiceover(SAY[6]) as vo:
            resize(self, t, 3, keep=list(t.lines[-3:]), run_time=0.7, extra=(FadeOut(br1), FadeOut(br2)))
            v2.parts_in("incoming")          # unhidden now: it fades in with the piles
            self.play(FadeIn(v2), run_time=0.6)
            vo.wait_until("would be overwritten")
            self.play(*v2.parts_in("wall1", anim=GrowFromCenter),
                      flash(v2.row("tracked", "cli.py"), ERR, 1.12, 0.8), run_time=0.8)
            vo.wait_until("and two untracked files")
            self.play(*v2.parts_in("wall2", anim=GrowFromCenter),
                      flash(P["untracked"].rows, ERR, 1.1, 0.8), run_time=0.8)
            vo.wait_until("where the branch has files")
            self.play(v2.slide_in(run_time=1.0))
            self.play(bump(inc, 0.1), flash(VGroup(v2.wall1, v2.wall2), ERR, 1.06, 0.5), run_time=0.5)
            vo.wait_until("Nothing changed")
            self.play(flash(abort.glyphs, ERR, 1.15, 0.8))

        # ========================================================== 7 · git stash, retry
        chip48 = at_left(readme_chip("README.md · line 48", PH48, max_w=12.6), -6.45, Y_UNDER)
        with self.voiceover(SAY[7]) as vo:
            self.play(tr.goto(4), FadeIn(chip48, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("the first reason")         # typed as "git stash" is said
            type_cmd(self, t, STASH.cmd, type_time=0.45)
            t.print(self, STASH_OUT, run_time=0.3)
            vo.wait_until("puts your edits away")
            self.play(*v2.stash(1, run_time=1.5))     # the lift and wall 1's fall span the clause
            type_cmd(self, t, CO2.cmd, type_time=0.8)  # the retry, typed as the sentence ends
            vo.wait_until("On a retry")
            tprint(self, t, CO2_OUT, wrap=True, run_time=0.9, lag=0.06)
            vo.wait_until("still block it")
            self.play(bump(inc, 0.1), flash(v2.wall2, ERR, 1.1, 0.8), run_time=0.8)

        # ========================================================== 8 · git stash -u; the checkout works
        # in the top band over the chip's right end (on the chip's edge it crossed the frame and
        # crowded the quote)
        err8 = at_right(erratum_tag("covers only edited files"), X_R, Y_BAND)
        dash = cmd_chip("git checkout -- .")
        n_red = note("throws your edits away", ERR)
        n_grey = note("leaves untracked files where they are")
        notes8 = VGroup(n_red, n_grey).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        grp8 = VGroup(dash, notes8).arrange(RIGHT, buff=0.3)
        with self.voiceover(SAY[8]) as vo:
            self.play(caption_extra(tr, True), FadeIn(err8, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("covers only edited files")
            self.play(*flash_tag(err8, S.WHITE, 1.08, 0.8))
            su = type_cmd(self, t, STASH_U.cmd, type_time=0.6)     # typed as "An extra git stash"
            pin(self, su, fit_tag(t, su), run_time=0.25)
            t.print(self, STASH_U.at(2), run_time=0.3)
            vo.wait_until("stashes untracked files too")
            self.play(*v2.stash(2, run_time=1.0), caption_extra(tr, False))
            type_cmd(self, t, CO3.cmd, type_time=0.8)
            vo.wait_until("and the checkout works")
            ok = t.print(self, CO3_OUT, run_time=0.4)
            self.play(ok[1].glyphs.animate.set_color(VENV), *land_split(v2, run_time=1.0))
            at_left(grp8, -6.35, P["tracked"].kind.get_top()[1] + 0.12 + grp8.height / 2)
            vo.wait_until("The other option")
            self.play(FadeIn(dash, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("discards your edits")
            self.play(FadeIn(n_red, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and leaves untracked")
            self.play(FadeIn(n_grey, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 9 · git branch; your turn
        # the switch silently replaces the ignored lecture 3 files (beat 10 proves it): the card says
        # so first, so a viewer who pauses here copies them out before switching
        card9 = first_turn_card(["first: copy out your lecture 3 Dockerfile,",
                                 "pyproject.toml, uv.lock · the switch replaces them"],
                                [CD.cmd, FETCH.cmd, CHECKOUT.cmd, STASH.cmd, (STASH_U.cmd, "extra"),
                                 CHECKOUT.cmd, BR3.cmd])
        # on the strip, right-aligned: its top rises past the tracker band's bottom, so it stays
        # right of the tracker
        card9.shift(UP * (STRIP_TOP + 0.14 - card9.frame.get_bottom()[1])
                    + RIGHT * (X_R + 0.08 - card9.frame.get_right()[0]))
        warned = "Before you switch" in " ".join(SAY[9].split())   # script.md's reworded line
        with self.voiceover(SAY[9]) as vo:
            self.play(tr.goto(5), run_time=0.4)
            type_cmd(self, t, BR3.cmd, type_time=0.4)
            b9 = t.print(self, BR3_OUT, run_time=0.3)
            vo.wait_until("star, flexible-workflow")
            self.play(b9[0].glyphs.animate.set_color(VENV), run_time=0.3)
            self.play(flash(b9[0].glyphs, VENV, 1.15, 0.7))
            self.play(FadeOut(v2), FadeOut(VGroup(chip48, err8, grp8)), run_time=0.4)
            self.play(FadeIn(card9, shift=UP * 0.15), run_time=0.5)
            if warned:
                vo.wait_until("Before you switch")
                self.play(flash(card9.first[0], TURN, 1.05, 0.9))   # the lines: not the opaque tag
            vo.wait_until("Pause and switch")
            self.play(Wiggle(card9.tag, scale_value=1.15, rotation_angle=0.025 * TAU),
                      *([] if warned else [flash(card9.first[0], TURN, 1.05, 0.9)]), run_time=0.9)

        # ========================================================== 10 · the ignored files were replaced
        v2.shift(UP * (V2_P3 - V2_P2))
        old = excerpt_chip(FROM_OLD, "transcribe_audio/Dockerfile · line 1 · before", line=FROM_OLD)
        at_right(old, X_R, 2.62)
        new = excerpt_chip(FROM_NEW, "transcribe_audio/Dockerfile · line 2 · after", line=FROM_NEW)
        new.shift(old.chip.get_left() - new.chip.get_left())
        same = at_right(grey_tag("the branch's files · same sizes as a fresh clone"), X_R, 2.48)
        quiet10 = VGroup(grey_tag("replaced · no warning"), erratum_tag()).arrange(RIGHT, buff=0.2)
        at_left(quiet10, -6.45, Y_UNDER)
        fix10 = note_card(["want your lecture 3 Dockerfile,",
                           "pyproject.toml, uv.lock (or docker-shell.sh)?",
                           "copy them out before switching"])
        at_right(fix10, X_R + 0.08, 0)
        fix10.shift(UP * (2.0 - fix10.frame.get_bottom()[1]))
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(card9), caption_extra(tr, True), run_time=0.4)
            resize(self, t, 4, run_time=0.6, extra=(FadeIn(v2), FadeIn(old, shift=DOWN * 0.1)))
            h2 = type_cmd(self, t, HEAD2, type_time=0.7)
            xt_h2 = fit_tag(t, h2)
            vo.wait_until("lecture 3 Dockerfile")
            # pin()'s steps by hand, so the tag's FadeIn shares its play with the row's flash
            self.play(FadeIn(xt_h2, shift=LEFT * 0.1), flash(v2.row("ignored", "Dockerfile").text,
                                                            S.WHITE, 1.15), run_time=0.5)
            h2_row = h2.rows[-1] if hasattr(h2, "rows") else h2
            self.remove(xt_h2)
            h2_row.add(xt_h2)
            self.add(h2_row)
            hout = t.print(self, HEAD2_OUT, run_time=0.4)
            self.play(v2.flip_card("ignored", "Dockerfile", run_time=1.0), FadeTransform(old, new),
                      flash(substring(hout[1], "3.14"), TURN, 1.3), run_time=1.0)
            type_cmd(self, t, LS_LA, type_time=0.6)
            lout = t.print(self, LA_OUT, run_time=0.35)
            xt10 = extra_tag()
            xt10.move_to([t.box.get_right()[0] - 0.2 - xt10.width / 2, t.title.get_center()[1], 0])
            self.play(v2.flip_card("ignored", "pyproject.toml", run_time=0.8),
                      v2.flip_card("ignored", "uv.lock", run_time=0.8), FadeIn(xt10),
                      FadeOut(new), run_time=0.8)
            vo.wait_until("the branch's")
            self.play(FadeIn(same, shift=LEFT * 0.2),
                      *[flash(substring(ln, ln.text.split()[4]), S.WHITE, 1.2) for ln in lout
                        if ln.text != "…"],
                      run_time=0.7)
            vo.wait_until("without a word")
            self.play(FadeIn(quiet10, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("copy them out first")
            self.play(FadeOut(same), FadeIn(fix10, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 11 · the key stays put; the stash
        chip50 = at_left(readme_chip("README.md · line 50", PH50), -6.45, Y_UNDER)
        fix11 = note_card(["delete each <component>/secrets/ now",
                           "your key goes in secrets/ beside the repo",
                           "why: end of part 1"])
        at_right(fix11, X_R + 0.13, 2.75)
        with self.voiceover(SAY[11]) as vo:
            # "The old key": the key glows as the coda's cards go
            self.play(FadeOut(VGroup(quiet10, fix10, xt10)), flash(v2.key, KEY, 1.5), run_time=0.8)
            ls2 = type_cmd(self, t, LS_SEC, type_time=0.7)
            pin(self, ls2, fit_tag(t, ls2), run_time=0.25)
            sec = t.print(self, SEC_OUT, run_time=0.3)[0]
            vo.wait_until("transcribe audio;")
            self.play(flash(sec.glyphs, KEY, 1.1), flash(v2.row("ignored", "secrets/"), KEY, 1.1),
                      run_time=0.8)
            vo.wait_until("your secrets stay put")
            self.play(FadeIn(chip50, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("as the README says")
            self.play(flash(chip50.phrase, S.WHITE, 1.06, 0.8))
            vo.wait_until("Every build there")
            self.play(flash(v2.key, ERR, 1.4, 0.9))
            vo.wait_until("so delete each")
            self.play(FadeIn(fix11, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("secrets folder now")       # its output lands on "Your edits wait"
            gl = type_cmd(self, t, STASH_LIST, type_time=0.6)
            pin(self, gl, fit_tag(t, gl), run_time=0.25)
            vo.wait_until("Your edits wait")
            t.print(self, LIST_OUT, run_time=0.4)
            vo.wait_until("in the stash")
            self.play(v2.relabel(2, "stash@{0}"), v2.relabel(1, "stash@{1}"), run_time=0.6)
            self.wait(0.6)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
