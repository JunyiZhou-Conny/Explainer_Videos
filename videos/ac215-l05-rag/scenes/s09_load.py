"""S09 · Load: records, an index, a folder on your disk (README "Load" steps 1–3, three extras).
Lecture: A30–A38.

Beats (script.md "## S09", one voiceover block each):
 0  LECTURE A30–A31. TRACKER Load (no step lit yet). Mini-map, "vector database" lit. A GREY table
    glyph answers the SQL chip WHERE price BETWEEN 10 AND 50 (two rows light GREEN, GREEN tick);
    the PINK question "chunks that mean something like this" bounces off it (RED cross) and lands
    in the TEAL cylinder ("vector database").
 1  V5: three GREEN arrows drop into rows of four cells (id 1021665fac86c5a5-0 …, document as
    blurred text, metadata {book, author, year}, embedding); a YELLOW box walks the cells as they
    are named. cli.py · lines 132–138 appears with the metadata cell (book, author, year lines
    lit), then Transforms into cli.py · lines 127–130 as the id cell lights: the book name's
    hash (lines 128–129) plus the row number (line 130; the rows' -0, -1, -2 light).
 2  The rows stack into the GREEN collection char-split-collection (chip cli.py · line 277
    f"{method}-collection"). cli.py · lines 280–290 (line 285 wrapped): line 282 RED as the
    collection empties, lines 287–288 GREEN as it is recreated, the chip becomes cli.py · line
    288 {"hnsw:space": "cosine"}; the records drop back in (a full rebuild).
 3  LECTURE A32–A38. Mini-map back. A small GREY strip of the lecture's four stages, "Indexing"
    lit. A PINK pointer walks down a column of 28 rows while a counter ticks to 8,248 ("slow");
    the rows lift into a layered graph (tag our illustration of HNSW): a sparse top layer, denser
    layers below; the PINK pointer hops down to a neighbor.
 4  TRACKER Load 1. TEAL terminal (13 rows) types python cli.py --load --chunk_type char-split ->
    cli-container/30 lines 2–8 (wrapped), GREY tag "first run · before any embeddings existed";
    line 5's "did not exist. Creating new." and line 8 YELLOW; GREY note "0 here = your embed step
    didn't finish".
 5  The terminal clears; the same command (tag recorded · the staff's vectors (68e0bde)) ->
    recorded-embeddings/01 lines 2–12, 19–22, …, 152–153 (wrapped; the first rows scroll):
    line 5 and line 8 YELLOW, the embedding column GREEN; above the terminal a GREEN counter adds
    the books up to 8,248; "Inserted 500 items..." lights at "in batches of 500".
 6  TRACKER Load 2. The terminal clears; python cli.py --load --chunk_type recursive-split ->
    recorded-embeddings/02 lines 2 (cut), 3–8, …, 163–164 (wrapped). The terminal shrinks to the
    strip as the counter becomes char-split-collection's count; recursive-split-collection stacks
    beside it (14,228); ▶ your turn card: both load commands and the Chroma UI link (step 3,
    below). Hold 2 s.
 7  TRACKER Load 2 · extra. The second laptop terminal (9 rows) types the curl … | grep … line of
    recorded-embeddings/03 (extra; folds) -> lines 2–5, both "dimension":256 YELLOW; above, a
    GREY ghost of laptop/17b line 3 "dimension":null (tag "before the first insert").
 8  Back in the container strip, cleared. GREY card "an extra Python check · in the study guide"
    / "one metadata dict per book" -> recorded-embeddings/07 lines 11, …, 22 (line 22 RED,
    erratum); excerpt chip cli.py · line 178 filename.split(".")[0] over the Woman's Institute
    file name, cut RED at its first dot; GREEN fix card (fix · not in the repo), rows writing in
    as named: os.path.splitext(filename)[0] · delete outputs/*Womans Institute Library of
    Cookery.jsonl · then chunk, embed, load.
 9  V5 zooms out: the two collections shrink into the cylinder of the TEAL Chroma box, whose /data
    window has a PINK route to the GREY docker-volumes/chromadb/ folder on your laptop (the route
    pulses, /data and the folder blink together). The second laptop terminal types ls -la
    docker-volumes/chromadb; du -sh docker-volumes/chromadb (extra; folds) ->
    recorded-embeddings/04 lines 2–8 (UUID rows cut with …): 59781120 and 82M YELLOW; GREEN
    "index" tags on the two UUID folders and "2 index folders · one per collection" by the
    folder (tag your numbers will differ); "root root" YELLOW; README chip README.md · line 160
    "persistent".
10  TRACKER Load 3. A GREY browser frame (tag illustration) at ac215-llm-rag.dlops.io/chromaui with a
    schematic collection list and the GREY note "if Chrome asks to reach your local network,
    allow it"; a PINK arrow from the page through the GREY door :8000 to the TEAL Chroma box.
    Below, headed curl -si -H 'Origin: …' localhost:8000 (extra): laptop/12 line 5 (GREEN) and
    a GREY ghost "no such line for another site" (laptop/12b).
11  The full V1 returns; its top lane glows end to end, GREEN ticks on chunking, embedding and the
    database; caption "part 1: the index is built"; the bottom lane pulses PINK at "In part 2".
    Fade to an empty frame (end of part 1).

Deviations from SHOW (see the scene report):
- Beat 1 shows the metadata lines first and the id lines second, in the order the SAY names them
  (SHOW: id first, then Transforms into metadata).
- The rows stack into the collection at the start of beat 2 ("Records go into a collection"),
  not at the end of beat 1.
- Beats 4–6 use one 13-row terminal (SHOW: 10 rows, then 13): type_cmd puts the command on the
  row under the prompt, and 10 rows would scroll it away. Beat 6 cuts recorded-embeddings/02
  line 2 with … (as S08 does) so the 13 rows keep the typed command. Beat 6 clears the terminal
  first, as beat 5 does (SHOW does not say so): its rows hold only step 2's command and output,
  never a line of the char-split run (review-bot item, QA_FOLLOWUPS.md); beat 5's counter sits in
  the band above the terminal, right of the tracker. Tags on a typed command sit on its prompt
  row (the command row has no room).
- Beat 6's strip keeps the first wrapped row of recorded-embeddings/02 line 164; its last
  character turns into … as the strip forms (a cut line, as the conventions mark one).
- Beat 7 opens the second laptop terminal straight at ~/AC215/llm-rag (S05 already showed the
  "new terminal: cd here first" step and the beat has 6.7 s) with 9 rows (the curl line folds
  onto 4 rows, as S10 folds it: inside the URL with "\" and no indent, so the rows retype as one
  valid command); the ghost sits above it. Beat 9 reuses that terminal.
- The counters' numbers are scaled to their labels' size (Counter's LaTeX digits read small).
- Beat 9 shows the picture first (concept before command), then the terminal; nothing travels
  along the /data route (script conventions: the route pulses, both sides blink). The UUID rows
  are cut after 8 hex digits so a GREEN "index" tag fits on each; "one per collection" sits by
  the folder.
- The recorded outputs of 03, 04 and 07 carry the "recorded · the staff's vectors (68e0bde)"
  tag (script conventions: every panel from recorded-embeddings/01–09); the fix card carries
  "fix · not in the repo".
- Beat 10's two strips sit under the browser frame (a 58-character line does not fit beside it).
- recorded-embeddings/01 line 12's invisible byte-order mark is dropped before printing (it has
  no glyph and would shift every highlight on that row).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    ShowPassingFlash,
    Transform,
    VGroup,
)

from common import (
    CTR,
    DATA,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    MINI_CENTER,
    NARRATION,
    P_CTR,
    P_REPO,
    STRIP_TOP,
    TURN,
    _type_rows,
    Counter,
    HnswGraph,
    MiniMap,
    RagMap,
    RecordTable,
    ScanColumn,
    StageStrip,
    beside,
    capture,
    caption_extra,
    check_card,
    collection_glyph,
    cylinder,
    differ_tag,
    door,
    erratum_tag,
    excerpt,
    excerpt_chip,
    extra_tag,
    fix_tag,
    grey_tag,
    illustration_tag,
    lref,
    note,
    our_illustration_tag,
    pin,
    question_card,
    readme_chip,
    resize,
    sans,
    src_panel,
    staff_tag,
    table_glyph,
    term,
    tracker,
    turn_card,
    type_cmd,
)
from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    OUTPUT,
    box,
    browser_window,
    check_mark,
    chip,
    cross_mark,
    folder_glyph,
    glyph_range,
    label,
    mono,
    mono_line,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ commands and real outputs
LOAD_CMD = "python cli.py --load --chunk_type char-split"            # README.md line 151
LOAD2_CMD = "python cli.py --load --chunk_type recursive-split"      # README.md line 152
assert LOAD_CMD in excerpt("README.md", 151, 151) and LOAD2_CMD in excerpt("README.md", 152, 152)
CHROMA_URL = "ac215-llm-rag.dlops.io/chromaui"                       # README.md line 162 (a link)
assert "https://" + CHROMA_URL in excerpt("README.md", 162, 162)

FIRST = capture("30", "cli-container")                 # the first run, before any embeddings
assert FIRST.cmd == LOAD_CMD and FIRST.exit == 0
assert FIRST.line(5).endswith("did not exist. Creating new.")
assert FIRST.line(8) == "Number of files to process: 0"

REC1 = capture("01", "recorded-embeddings")            # the same command on the staff's vectors
assert REC1.cmd == LOAD_CMD and REC1.exit == 0
assert REC1.line(5).startswith("Deleted existing collection") and REC1.line(8).endswith(": 11")
assert REC1.line(19) == "Inserted 500 items..." and REC1.line(153).startswith("Finished inserting 24")


def no_bom(s: str) -> str:
    """Line 12 holds an invisible byte-order mark (the book file's first character): it has no
    glyph, so it would shift every highlight on that row. Nothing visible changes."""
    return s.replace("﻿", "")


REC1_HEAD = REC1.at((2, 8))
REC1_TABLE = [no_bom(s) for s in REC1.at((9, 12))]
REC1_BATCH = REC1.at((19, 22))
REC1_TAIL = REC1.at("…", (152, 153))

REC2 = capture("02", "recorded-embeddings")
assert REC2.cmd == LOAD2_CMD and REC2.exit == 0
REC2_OUT = [REC2.line(2)[:64] + "…"] + REC2.at((3, 8), "…", (163, 164))
assert REC2.line(8) == "Number of files to process: 11" and REC2.line(163) == "Inserted 35 items..."

NAMES = capture("03", "recorded-embeddings")           # extra: the collections' dimension
assert NAMES.exit == 0 and NAMES.line(3) == '"dimension":256' and NAMES.line(5) == '"dimension":256'
# The curl line folds as S10 folds the same check: at spaces, and once inside its URL at a "/" with
# no space before the "\" and no indent after it (bash joins backslash-newline, so the URL stays one
# word). type_cmd's hard break there ends the row with " \" and indents the next, which retyped
# splits the URL into two words.
_u = NAMES.cmd.split()
assert _u[:2] == ["curl", "-s"] and _u[3:6] == ["|", "grep", "-oE"] and len(_u) == 7, _u
_cut = _u[2].index("/databases")
CURL_ROWS = [f"{P_REPO} curl -s \\", f"    {_u[2][:_cut]}\\", f"{_u[2][_cut:]} | grep -oE \\", f"    {_u[6]}"]
_joined = "\n".join(CURL_ROWS)[len(P_REPO) + 1:].replace("\\\n", "")
assert " ".join(_joined.split()) == NAMES.cmd and all(len(r) <= 65 for r in CURL_ROWS), CURL_ROWS
GHOST = capture("17b", "laptop").line(3)               # the same check before the first insert
assert GHOST == '"dimension":null'

META = capture("07", "recorded-embeddings")            # extra: one metadata dict per book
assert META.line(11) == "count: 8248" and META.line(22) == "{'book': 'Womans Institute Library of Cookery'}"
SPLIT = 'filename.split(".")[0]'
assert SPLIT in excerpt("cli.py", 178, 178)
WOMAN_FILE = "Womans Institute Library of Cookery. Volume 2_ Milk, Butter and Cheese Eggs Vegetables.txt"
WOMAN_SHOWN = "Womans Institute Library of Cookery. Volume 2_ Milk, Butter … .txt"
WOMAN_CUT = WOMAN_SHOWN.index(".")

VOL = capture("04", "recorded-embeddings")             # extra: the database folder on the laptop
assert VOL.exit == 0 and VOL.cmd == "ls -la docker-volumes/chromadb; du -sh docker-volumes/chromadb"
assert "59781120" in VOL.line(6) and VOL.line(8).startswith("82M")


def uuid_row(n: int) -> str:
    """An ls -la row of a UUID folder, cut with … after the UUID's first 8 hex digits."""
    s = VOL.line(n)
    k = s.rindex(" ") + 9
    return s[:k] + "…"


VOL_OUT = [VOL.line(2), VOL.line(3), VOL.line(4), uuid_row(5), VOL.line(6), uuid_row(7), VOL.line(8)]

CORS = capture("12", "laptop")                         # extra: the CORS header for the course site
CORS_LINE = CORS.line(5)
assert CORS_LINE == "access-control-allow-origin: https://ac215-llm-rag.dlops.io"
CORS_B = capture("12b", "laptop")                      # another site: no such line
assert not any(s.startswith("access-control-allow-origin") for s in CORS_B.lines)
CORS_HEAD = "curl -si -H 'Origin: …' localhost:8000"

COLL_CHIP = 'f"{method}-collection"'
assert COLL_CHIP in excerpt("cli.py", 277, 277)
HNSW = '{"hnsw:space": "cosine"}'
assert HNSW in excerpt("cli.py", 288, 288)

# ------------------------------------------------------------------ layout
TAB_C = np.array([-3.35, 0.45, 0])        # beat 0: the SQL table
CYL_C = np.array([3.35, 0.45, 0])         # beat 0: the vector database
TABLE_TOP = 2.35                          # beat 1: V5's rows
PANEL_TOP = -0.15                         # beat 1: the code panel under them
COLL_Y = 2.42                             # beat 2: the collection, top left
PANEL2_TOP = 1.78                         # beat 2: cli.py · lines 280–290
SCAN_C = np.array([-3.95, -0.45, 0])      # beat 3: the slow scan
HNSW_C = np.array([0.5, -0.45, 0])        # beat 3: the layered graph (centred once the scan leaves)
HNSW_W, HNSW_GAP = 7.6, 1.2               # beat 3: its width and layer spacing
PIC_Y = 1.95                              # beat 9: the picture above the 9-row terminal


def mixed(parts, size: float = CAPTION, color: str = INK) -> VGroup:
    """One row of serif pieces and `mono` pieces (in backticks); (text, colour) for a colour."""
    mobs = []
    for p in parts:
        s, col = (p, color) if isinstance(p, str) else p
        if len(s) > 1 and s.startswith("`") and s.endswith("`"):
            mobs.append(mono(s[1:-1], size, col))
        else:
            mobs.append(label(s, size, col))
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


def row_with(rows, sub: str):
    """The printed terminal row (of a list just printed) whose text contains `sub`."""
    for r in rows:
        if sub in r.text:
            return r
    raise KeyError(sub)


def big_digits(c: Counter, k: float = 1.35) -> Counter:
    """Counter draws its number with LaTeX digits about 0.73 of its label's size: scale the number
    to the label's visual size (DecimalNumber keeps the scale when its value changes) and put it
    back beside the label. Its left edge stays fixed as it counts."""
    c.num.scale(k)
    c.num.next_to(c.label, RIGHT, buff=0.15).align_to(c.label, DOWN)
    return c


def compact_collection(name: str) -> VGroup:
    """collection_glyph with its name to the right of the slabs (a flat layout for a top row)."""
    g = collection_glyph(name)
    g.name.next_to(g.stack, RIGHT, buff=0.3)
    return g


def window(name: str, w: float = 1.1, h: float = 0.46) -> VGroup:
    """A TEAL container window (as V2's /data)."""
    fr = box(w, h, CTR, fill=S.BG, fill_opacity=0.95, radius=0.08, stroke=2)
    return VGroup(fr, mono(name, CAPTION, INK).move_to(fr))


class LoadChroma(VoiceScene):
    def construct(self):
        assert len(SAY) == 12, f"S09 has {len(SAY)} SAY lines; this scene times 12"

        tr = tracker("Load")
        mm = MiniMap(MINI_CENTER)

        # ========================================================== 0 · why a vector database
        lr = lref("A30–A31")
        tbl = table_glyph(rows=5, cols=3, w=2.8, h=1.75).move_to(TAB_C)
        tbl_lab = note("an ordinary database").next_to(tbl, DOWN, buff=0.2)
        row_h = 1.75 / 5
        hits = VGroup(*[Rectangle(width=2.8, height=row_h, stroke_width=0).set_fill(DATA, 0.4)
                        .move_to([TAB_C[0], tbl.get_top()[1] - (k + 0.5) * row_h, 0]) for k in (2, 4)])
        sql = chip("WHERE price BETWEEN 10 AND 50", S.GREY, size=CAPTION, font=MONO).next_to(tbl, UP, buff=0.35)
        tick = check_mark(0.32, DATA).next_to(sql, RIGHT, buff=0.2)
        q = question_card("chunks that mean something like this", font=None)
        q_start = np.array([0.55, -1.75, 0])
        q.move_to(q_start)
        q_hit = np.array([tbl.get_right()[0] + 0.04 + q.width / 2, TAB_C[1] - 0.25, 0])
        q_back = np.array([0.9, -1.55, 0])
        cross = cross_mark(0.55, ERR).move_to(tbl)
        cyl = cylinder(1.45, 1.6).move_to(CYL_C)
        cyl_lab = note("vector database").next_to(cyl, DOWN, buff=0.25)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(lr), FadeIn(mm), run_time=0.6)
            self.play(mm.light("database"), FadeIn(tbl), FadeIn(tbl_lab), run_time=0.6)
            self.play(FadeIn(sql, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("like a price between 10 and 50")
            self.play(Indicate(sql.text, color=TURN, scale_factor=1.05), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(h) for h in hits], lag_ratio=0.3), Create(tick), run_time=0.7)
            vo.wait_until("but it can't find rows")
            self.play(FadeIn(q, shift=UP * 0.2), run_time=0.5)
            self.play(q.animate.move_to(q_hit), run_time=0.55)
            self.play(q.animate.move_to(q_back), Create(cross), Indicate(tbl, color=ERR, scale_factor=1.03),
                      run_time=0.6)
            vo.wait_until("whose meaning is like a question")
            self.play(Indicate(q, color=LOOKUP, scale_factor=1.06), run_time=0.8)
            vo.wait_until("A vector database can")
            self.play(FadeIn(cyl), FadeIn(cyl_lab), run_time=0.4)
            self.play(q.animate.move_to(cyl).scale(0.3).set_opacity(0), run_time=0.7)
            self.remove(q)
            self.play(Indicate(cyl, color=TURN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 1 · a record: id, text, metadata, vector
        rt = RecordTable(3, show=("header",))
        rt.shift(np.array([-rt.get_center()[0], TABLE_TOP - rt.get_top()[1], 0]))
        drops = VGroup()
        for i in range(3):
            a = rt.cell(i, "embedding")
            d = Arrow(a[0].get_start(), a[0].get_end(), buff=0, color=DATA, stroke_width=4,
                      max_tip_length_to_length_ratio=0.35, tip_length=0.14)
            drops.add(d.move_to([a.get_center()[0], 3.15, 0]))
        cbox = rt.col_box("id")
        p_meta = src_panel("cli.py", 132, 138)
        p_meta.shift(np.array([-6.3 - p_meta.get_left()[0], PANEL_TOP - p_meta.get_top()[1], 0]))
        meta_bars = VGroup(*[p_meta.bar(n, TURN, 0.16) for n in (133, 137, 138)])
        p_id = src_panel("cli.py", 127, 130)
        p_id.shift(np.array([-6.3 - p_id.get_left()[0], PANEL_TOP - p_id.get_top()[1], 0]))
        hash_bars = VGroup(*[p_id.bar(n, TURN, 0.16) for n in (128, 129)])
        row_bar = p_id.bar(130, TURN, 0.16)
        suffixes = VGroup(*[rt.cell(i, "id")[-2:] for i in range(3)])
        hashes = VGroup(*[rt.cell(i, "id")[:-2] for i in range(3)])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(tbl, tbl_lab, hits, sql, tick, cross, cyl, cyl_lab)), FadeOut(lr),
                      FadeOut(mm), run_time=0.4)
            self.play(FadeIn(rt), LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in drops], lag_ratio=0.25),
                      run_time=0.5)
            self.play(LaggedStart(*[d.animate.move_to(rt.cell(i, "embedding")) for i, d in enumerate(drops)],
                                  lag_ratio=0.25), run_time=0.6)
            self.play(*rt.parts_in("row0", "row1", "row2"), run_time=0.35)
            self.remove(*drops)                  # (and the LaggedStart's wrapper group around them)
            vo.wait_until("an ID")
            self.play(Create(cbox), run_time=0.35)
            vo.wait_until("the text")
            self.play(Transform(cbox, rt.col_box("document")), run_time=0.35)
            vo.wait_until("metadata with book")
            self.play(Transform(cbox, rt.col_box("metadata")), FadeIn(p_meta, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(meta_bars), run_time=0.4)
            vo.wait_until("and the vector")
            self.play(Transform(cbox, rt.col_box("embedding")), run_time=0.4)
            vo.wait_until("The ID hashes")
            self.play(FadeOut(meta_bars), Transform(cbox, rt.col_box("id")), run_time=0.3)
            self.play(ReplacementTransform(p_meta, p_id), run_time=0.7)
            self.play(FadeIn(hash_bars), Indicate(hashes, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("plus the row number")
            self.play(FadeIn(row_bar), Indicate(suffixes, color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("so it's stable")
            self.play(Indicate(rt.column("id"), color=TURN, scale_factor=1.04), run_time=0.8)

        # ========================================================== 2 · a collection, rebuilt on every load
        coll = compact_collection("char-split-collection")
        coll.move_to([-6.2 + coll.width / 2, COLL_Y, 0])
        slabs = coll.stack
        c_chip = excerpt_chip(COLL_CHIP, "cli.py · line 277", line=excerpt("cli.py", 277, 277))
        c_chip.move_to([6.3 - c_chip.width / 2, COLL_Y - 0.1, 0])
        h_chip = excerpt_chip(HNSW, "cli.py · line 288", line=excerpt("cli.py", 288, 288))
        h_chip.move_to([6.3 - h_chip.width / 2, COLL_Y - 0.1, 0])
        p2 = src_panel("cli.py", 280, 290, wrap=True)
        p2.shift(np.array([-6.3 - p2.get_left()[0], PANEL2_TOP - p2.get_top()[1], 0]))
        del_bar = p2.bar(282, ERR, 0.22)
        new_bars = VGroup(p2.bar(287, DATA, 0.2), p2.bar(288, DATA, 0.2))
        cos_span = p2.span(288, '"cosine"')

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p_id, hash_bars, row_bar, cbox)), run_time=0.4)
            self.play(rt.animate.scale(0.16).move_to(slabs).set_opacity(0),
                      LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in slabs], lag_ratio=0.12),
                      FadeIn(coll.name), run_time=1.0)
            self.remove(rt)
            vo.wait_until("one per chunk type")
            self.play(FadeIn(c_chip, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(c_chip.text, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("The load step")
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("deletes it")
            self.play(FadeIn(del_bar), *[s.animate.set_fill(opacity=0).set_stroke(ERR) for s in slabs],
                      run_time=0.6)
            vo.wait_until("and creates it again")
            self.play(FadeIn(new_bars), *[s.animate.set_stroke(DATA) for s in slabs], run_time=0.6)
            vo.wait_until("with cosine")
            self.play(FadeOut(c_chip, shift=UP * 0.2), FadeIn(h_chip, shift=UP * 0.2),
                      Indicate(cos_span, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("every load is a full rebuild")
            self.play(LaggedStart(*[s.animate.set_fill(opacity=1) for s in slabs], lag_ratio=0.15), run_time=1.0)

        # ========================================================== 3 · the slow scan and the index (HNSW)
        lr = lref("A32–A38")
        st = StageStrip(box_w=2.2, h=0.55, gap=0.4, show=("boxes",))
        st.shift(np.array([-st.boxes.get_center()[0], 2.32 - st.boxes.get_center()[1], 0]))
        idx_frame = st.boxes[0][0]
        sc = ScanColumn(n=28).move_to(SCAN_C)
        big_digits(sc.counter)
        slow = note("slow").next_to(sc.counter, DOWN, buff=0.2).align_to(sc.counter, LEFT)
        hg = HnswGraph(width=HNSW_W, gap=HNSW_GAP, show=()).move_to(HNSW_C)
        bottom = hg.nodes[-1]
        bot_ids = hg.sets[-1]
        ill = our_illustration_tag("of HNSW")
        ill.move_to([HNSW_C[0] + HNSW_W / 2 - ill.width / 2, HNSW_C[1] + HNSW_GAP + 0.6, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p2, del_bar, new_bars, coll, h_chip)), FadeIn(lr), FadeIn(mm),
                      FadeIn(st), run_time=0.6)
            self.play(idx_frame.animate.set_stroke(TURN, 4), FadeIn(sc), run_time=0.4)
            self.play(*sc.walk(8248, run_time=1.6))
            sc.counter.freeze()
            vo.wait_until("is slow at scale")
            self.play(FadeIn(slow, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("So the database builds an index")
            self.add(hg)
            targets = [Dot(bottom[bot_ids[k % len(bot_ids)]].get_center(), radius=0.07, color=DATA)
                       for k in range(len(sc.rows))]
            self.play(*[Transform(r, d) for r, d in zip(sc.rows, targets)],
                      sc.pointer.animate.set_opacity(0), sc.counter.animate.set_opacity(0),
                      slow.animate.set_opacity(0), *hg.parts_in("layer2"), run_time=1.1)
            self.remove(sc, slow)
            self.play(LaggedStart(*hg.parts_in("layer1"), *hg.parts_in("layer0", "links"), lag_ratio=0.4),
                      run_time=1.0)
            vo.wait_until("in these slides' sense")
            self.play(Indicate(st.boxes[0], color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("a layered graph")
            self.play(FadeIn(ill, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("where a search hops down")
            ptr, hops = hg.hop()
            self.play(FadeIn(ptr, scale=1.4), run_time=0.25)
            for h in hops:
                self.play(h)

        # ========================================================== 4 · step 1, the first run: 0 files
        t = term(P_CTR, rows=13, container=True)
        first_tag = grey_tag("first run · before any embeddings existed")
        zero_note = note("0 here = your embed step didn't finish")

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(st, hg, ptr, ill)), FadeOut(lr), FadeOut(mm), tr.goto(1), run_time=0.45)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.3)
            vo.wait_until("python cli.py")
            cmd = type_cmd(self, t, LOAD_CMD, type_time=1.6)
            assert hasattr(cmd, "rows") and len(cmd.rows) == 2
            self.play(Indicate(substring(cmd.rows[1], "--load"), color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("chunk type char split")
            self.play(Indicate(substring(cmd.rows[1], "--chunk_type char-split"), color=TURN, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("On our first run")
            pin(self, cmd.rows[0], beside(first_tag, t, cmd.rows[0], buff=0.5), run_time=0.4)
            out = t.print(self, FIRST.at((2, 8)), wrap=True, run_time=0.6)
            l5 = row_with(out, "did not exist")
            l8 = row_with(out, "Number of files to process")
            vo.wait_until("it made an empty collection")
            self.play(substring(l5, "did not exist. Creating new.").animate.set_color(TURN), run_time=0.6)
            vo.wait_until("and found 0 files")
            self.play(l8.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("If you see 0")
            pin(self, l8, beside(zero_note, t, l8, buff=0.5), run_time=0.5)
            self.play(Indicate(glyph_range(l8, len(l8.text) - 1), color=TURN, scale_factor=1.5), run_time=0.8)

        # ========================================================== 5 · the staff's vectors: 8,248 records
        stf = staff_tag()
        counter = big_digits(Counter("records", 8248, DATA, size=32))   # placed at its widest, then reset
        counter.move_to([6.3 - counter.width / 2, 3.08, 0])
        counter.tracker.set_value(0)
        counter.num.set_value(0)

        with self.voiceover(SAY[5]) as vo:
            t.clear(self)
            cmd2 = type_cmd(self, t, LOAD_CMD, type_time=1.2)
            pin(self, cmd2.rows[0], beside(stf, t, cmd2.rows[0], buff=0.5), run_time=0.4)
            vo.wait_until("the same command")
            self.play(Indicate(cmd2.rows[1], color=TURN, scale_factor=1.04), run_time=0.6)
            out = t.print(self, REC1_HEAD, wrap=True, run_time=0.6)
            self.play(substring(row_with(out, "Deleted existing collection"), "Deleted existing collection")
                      .animate.set_color(TURN), run_time=0.5)
            vo.wait_until("and reads 11 files")
            self.play(row_with(out, "Number of files").animate.set_color(TURN), run_time=0.5)
            out2 = t.print(self, REC1_TABLE, wrap=True, run_time=0.6)
            vo.wait_until("with an embedding column")
            head_row = [r for r in out2 if r.text.rstrip().endswith("embedding")][0]
            vec_rows = [r for r in out2 if "[-0." in r.text]
            assert len(vec_rows) == 1
            v1 = vec_rows[0]
            v2 = out2[list(out2).index(v1) + 1]
            self.play(substring(head_row, "embedding").animate.set_color(DATA),
                      glyph_range(v1, v1.text.index("[-0.")).animate.set_color(DATA),
                      v2.animate.set_color(DATA), run_time=0.7)
            vo.wait_until("It inserts 8,248 records")
            batch = t.print(self, REC1_BATCH, wrap=True, run_time=0.4)
            self.play(FadeIn(counter, shift=DOWN * 0.1), run_time=0.25)
            self.play(counter.count_to(1355, 0.5))
            t.print(self, REC1_TAIL, wrap=True, run_time=0.4)
            self.play(counter.count_to(8248, 0.7))
            vo.wait_until("in batches of 500")
            b500 = row_with(batch, "Inserted 500 items")
            self.play(b500.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(b500, color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 6 · step 2: recursive split; your turn
        c1 = collection_glyph("char-split-collection", "8,248")
        c2 = collection_glyph("recursive-split-collection", "14,228")
        pair = VGroup(c1, c2).arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to([0, 2.0, 0])
        tc = turn_card([LOAD_CMD, LOAD2_CMD, (CHROMA_URL, "link · in Chrome · step 3, below")])
        tc.move_to([0, (STRIP_TOP + pair.get_bottom()[1]) / 2 - 0.08, 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(tr.goto(2), run_time=0.4)
            t.clear(self)                  # the char-split run leaves before step 2 is typed (as in beat 5)
            cmd3 = type_cmd(self, t, LOAD2_CMD, type_time=1.3)
            stf2 = staff_tag()
            pin(self, cmd3.rows[0], beside(stf2, t, cmd3.rows[0], buff=0.5), run_time=0.3)
            out3 = t.print(self, REC2_OUT, wrap=True, run_time=0.6)
            # the 13 rows hold only this command and its output (nothing of the char-split run), and
            # the output fills them exactly: nothing scrolls
            assert len(t.lines) == 13 and t.lines[0] is cmd3.rows[0] and len(out3) == 11, len(t.lines)
            fin = row_with(out3, "Finished inserting 35")
            # in the strip the line keeps only its first wrapped row: its last character becomes …
            assert len(fin.text) == 65 and fin.text.endswith("'recursive-split-coll"), fin.text
            last = glyph_range(fin, 64)[0]
            # the label leaves first (in the pause before the anchor): the number travels left through the
            # label's place, and morphing "records: 8,248" as a whole into "8,248" smears the glyphs mid-flight
            self.play(FadeOut(counter.label, shift=UP * 0.15), run_time=0.3)
            vo.wait_until("14,228 records")
            counter.freeze()
            # the number cross-fades into char-split-collection's count as it travels, while the terminal
            # shrinks (it stays above the shrinking frame), so recursive-split-collection's 14,228 lands while
            # "14,228 records" is still being said (in this line's clip the number runs from 2.5 s to 5.1 s; the
            # anchor, interpolated by characters, sits at 3.6 s), not after it
            resize(self, t, 3, keep=[cmd3.rows[0], cmd3.rows[1], fin], run_time=0.7,
                   extra=(FadeTransform(counter.num, c1.count),))
            ell = mono_line("…", t.size, OUTPUT).align_to(fin.strut, UP)
            ell.shift(RIGHT * (last.get_center()[0] - ell.glyphs.get_center()[0]))
            self.play(LaggedStart(FadeIn(VGroup(c1.stack, c1.name)), FadeIn(c2, shift=LEFT * 0.3), lag_ratio=0.35),
                      Transform(last, ell.glyphs[0]), run_time=0.7)
            vo.wait_until("Pause and run both loads")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.5)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 7 · extra: dimension 256
        tl = term(P_REPO, rows=9, title="laptop · second terminal")
        g_txt = mono(GHOST, CAPTION, S.GREY)
        g_fr = box(g_txt.width + 0.4, g_txt.height + 0.3, S.GREY, dashed=True, stroke=2)
        ghost = VGroup(g_fr, g_txt.move_to(g_fr))
        g_tag = grey_tag("before the first insert").next_to(ghost, RIGHT, buff=0.25)
        ghost_all = VGroup(ghost, g_tag)
        ghost_all.move_to([-6.0 + ghost_all.width / 2, tl.box.get_top()[1] + 0.55, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(caption_extra(tr, True), FadeOut(VGroup(tc, c1, c2)), FadeOut(t, shift=DOWN * 0.2),
                      run_time=0.5)
            self.play(FadeIn(tl, shift=UP * 0.2), run_time=0.4)
            cmd4 = _type_rows(self, tl, CURL_ROWS, len(P_REPO) + 1, 1.5, len(NAMES.cmd))
            pin(self, cmd4.rows[0], beside(extra_tag(), tl, cmd4.rows[0], buff=0.5), run_time=0.3)
            out4 = tl.print(self, NAMES.at((2, 5)), run_time=0.5)
            pin(self, out4[0], beside(staff_tag(), tl, out4[0], buff=0.6), run_time=0.3)
            vo.wait_until("dimension 256")
            self.play(*[r.animate.set_color(TURN) for r in (out4[1], out4[3])], run_time=0.6)
            vo.wait_until("fixed by the first insert")
            self.play(FadeIn(ghost_all, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(out4[1], color=TURN, scale_factor=1.08), run_time=0.7)

        # ========================================================== 8 · extra: one book without author or year
        for m in list(t.lines):          # the container strip comes back cleared
            t.lines.remove(m)
        ck = check_card("one metadata dict per book")
        ck.move_to([-6.3 + ck.width / 2, 2.3, 0])
        sp_chip = excerpt_chip(SPLIT, "cli.py · line 178 (excerpt)", line=excerpt("cli.py", 178, 178))
        sp_chip.move_to([-6.3 + sp_chip.width / 2, 2.25, 0])
        fname = mono(WOMAN_SHOWN, CAPTION, INK)
        fname.move_to([-6.2 + fname.width / 2, 1.11, 0])
        fname_head = note("its file name in input-datasets/books").next_to(fname, UP, buff=0.14).align_to(fname, LEFT)
        kept = fname[:len(WOMAN_SHOWN[:WOMAN_CUT].replace(" ", ""))]
        lost = fname[len(kept):]
        dot_x = (kept.get_right()[0] + lost.get_left()[0]) / 2
        cut = Line([dot_x, fname.get_top()[1] + 0.12, 0], [dot_x, fname.get_bottom()[1] - 0.12, 0],
                   color=ERR, stroke_width=4)
        fix_rows = [mixed(["`os.path.splitext(filename)[0]`", ("· split off only the extension", S.GREY)]),
                    mixed(["delete", "`outputs/*Womans Institute Library of Cookery.jsonl`"]),
                    mixed(["then chunk, embed, load"])]
        fix_items = VGroup(*fix_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fix_fr = box(fix_items.width + 0.6, fix_items.height + 0.55, DATA, fill=S.BG, fill_opacity=0.95,
                     radius=0.14)
        fix_items.move_to(fix_fr).align_to(fix_fr, LEFT).shift(RIGHT * 0.3)
        fx_tag = fix_tag().move_to(fix_fr.get_corner(UP + RIGHT)).shift(LEFT * (fix_tag().width / 2 + 0.3))
        fix_card = VGroup(fix_fr, fix_items, fx_tag)
        fix_card.move_to([-6.3 + fix_card.width / 2, -0.25, 0])   # clear of the strip below and the file name above

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(tl, ghost_all)), FadeIn(t, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(ck, shift=DOWN * 0.1), run_time=0.4)
            out5 = t.print(self, [META.line(11), "…", (META.line(22), ERR)], run_time=0.5)
            pin(self, out5[0], beside(staff_tag(), t, out5[0], buff=0.6), run_time=0.3)
            pin(self, out5[2], beside(erratum_tag(), t, out5[2], buff=0.5), run_time=0.4)
            vo.wait_until("a small slip")
            self.play(FadeOut(ck), FadeIn(sp_chip, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(fname_head), FadeIn(fname), run_time=0.5)
            vo.wait_until("at the first dot")
            self.play(Create(cut), lost.animate.set_color(S.GREY_DARK), kept.animate.set_color(TURN),
                      Indicate(sp_chip.text, color=ERR, scale_factor=1.06), run_time=0.7)
            self.play(Indicate(out5[2], color=ERR, scale_factor=1.04), run_time=0.55)
            vo.wait_until("Split off only the extension")
            self.play(FadeIn(fix_fr), FadeIn(fx_tag), FadeIn(fix_rows[0], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("delete that book's old files")
            self.play(FadeIn(fix_rows[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("then chunk, embed and load again")
            self.play(FadeIn(fix_rows[2], shift=RIGHT * 0.15), run_time=0.5)

        # ========================================================== 9 · the database is a folder on your laptop
        for m in list(tl.lines):         # the second laptop terminal comes back cleared
            tl.lines.remove(m)
        z1 = collection_glyph("char-split-collection")
        z2 = collection_glyph("recursive-split-collection")
        zoom = VGroup(z1, z2).arrange(RIGHT, buff=0.8).move_to([0, PIC_Y, 0])
        chb = box(3.5, 1.58, CTR, fill_opacity=0.08, radius=0.14, stroke=3).move_to([-4.5, PIC_Y, 0])
        cht = sans("Chroma container", CAPTION, CTR)
        cht.move_to(chb.get_corner(UP + LEFT) + np.array([0.15 + cht.width / 2, -0.26, 0]))
        cyl9 = cylinder(0.72, 0.72).move_to([-5.45, PIC_Y - 0.22, 0])
        win = window("/data").move_to([-3.85, PIC_Y - 0.22, 0])
        fold = folder_glyph(0.46, LAPTOP).move_to([0.75, PIC_Y + 0.2, 0])
        fold_name = mono("docker-volumes/chromadb/", CAPTION, INK).next_to(fold, RIGHT, buff=0.18)
        on_laptop = note("on your laptop").next_to(fold_name, UP, buff=0.12).align_to(fold_name, LEFT)
        route = Line(win.get_right() + RIGHT * 0.02, [fold.get_left()[0] - 0.08, win.get_center()[1], 0],
                     color=LOOKUP, stroke_width=4)
        bend = Line(route.get_end(), fold.get_left() + LEFT * 0.08, color=LOOKUP, stroke_width=4)
        pic = VGroup(route, bend, chb, cht, cyl9, win, fold, fold_name, on_laptop)
        idx_lab = label("2 index folders · one per collection", CAPTION, DATA)
        idx_lab.next_to(fold_name, DOWN, buff=0.16).align_to(fold_name, LEFT)
        rd_chip = readme_chip("README.md · line 160", "persistent")
        rd_chip.move_to([6.3 - rd_chip.width / 2, 3.22, 0])

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(t, sp_chip, fname_head, fname, cut, fix_card)), FadeIn(zoom), run_time=0.5)
            self.play(zoom.animate.scale(0.12).move_to(cyl9).set_opacity(0), FadeIn(pic), run_time=0.8)
            self.remove(zoom)
            path = VGroup(route.copy(), bend.copy()).set_stroke(LOOKUP, 9)
            self.play(ShowPassingFlash(path[0], time_width=0.6), Indicate(cyl9, color=DATA, scale_factor=1.08),
                      run_time=0.5)
            self.play(Indicate(win, color=TURN, scale_factor=1.1), Indicate(VGroup(fold, fold_name), color=TURN,
                                                                            scale_factor=1.06), run_time=0.55)
            self.play(FadeIn(tl, shift=UP * 0.2), run_time=0.3)
            cmd5 = type_cmd(self, tl, VOL.cmd, type_time=1.0)
            assert hasattr(cmd5, "rows") and len(cmd5.rows) == 2
            pin(self, cmd5.rows[-1], beside(extra_tag(), tl, cmd5.rows[-1], buff=0.5), run_time=0.3)
            out6 = tl.print(self, VOL_OUT, run_time=0.5)
            total, _, _, u1, sq, u2, du = out6
            vo.wait_until("a 60-megabyte SQLite file")
            self.play(substring(sq, "59781120").animate.set_color(TURN), substring(sq, "chroma.sqlite3")
                      .animate.set_color(TURN), substring(du, "82M").animate.set_color(TURN), run_time=0.6)
            pin(self, du, beside(staff_tag(), tl, du, buff=0.6), run_time=0.3)
            vo.wait_until("and two index folders")
            uu = [substring(u, u.text.split()[-1].rstrip("…")) for u in (u1, u2)]
            self.play(*[g.animate.set_color(DATA) for g in uu], run_time=0.5)
            for u in (u1, u2):
                pin(self, u, beside(sans("index", CAPTION, DATA), tl, u, buff=0.35), run_time=0.25)
            vo.wait_until("one per collection")
            self.play(FadeIn(idx_lab, shift=UP * 0.1), run_time=0.4)
            pin(self, total, beside(differ_tag(), tl, total, buff=0.6), run_time=0.3)
            vo.wait_until("owned by root")
            self.play(*[substring(r, "root root").animate.set_color(TURN) for r in (u1, sq, u2)], run_time=0.6)
            vo.wait_until("The README calls it persistent")
            self.play(FadeIn(rd_chip, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(rd_chip.phrase, color=TURN, scale_factor=1.1), Indicate(fold, color=TURN), run_time=0.8)

        # ========================================================== 10 · step 3: the course's Chroma UI
        br = browser_window(CHROMA_URL, width=7.0, height=3.2).move_to([-2.8, 1.2, 0])
        ill10 = illustration_tag()
        ill10.move_to(br.frame.get_corner(DOWN + RIGHT) + np.array([-0.3 - ill10.width / 2, 0, 0]))
        c_head = note("collections").move_to(br.content.get_corner(UP + LEFT) + np.array([0.3, -0.25, 0]),
                                             aligned_edge=LEFT)
        list_rows = VGroup()
        for nm in ("char-split-collection", "recursive-split-collection"):
            sl = Rectangle(width=0.42, height=0.2, stroke_color=DATA, stroke_width=2).set_fill(DATA, 0.35)
            list_rows.add(VGroup(sl, mono(nm, CAPTION, DATA)).arrange(RIGHT, buff=0.2))
        list_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(c_head, DOWN, buff=0.25, aligned_edge=LEFT)
        lan = note("if Chrome asks to reach your local network, allow it")
        lan.move_to([br.frame.get_center()[0], br.frame.get_bottom()[1] + 0.5, 0])
        dr = door(0.42, 0.7, LAPTOP).move_to([1.95, 1.2, 0])
        dr_lab = mono(":8000", CAPTION, LAPTOP).next_to(dr, DOWN, buff=0.15)
        chb10 = box(2.6, 2.2, CTR, fill_opacity=0.08, radius=0.14, stroke=3).move_to([5.0, 1.2, 0])
        cht10 = sans("Chroma container", CAPTION, CTR).move_to(chb10.get_top() + DOWN * 0.3)
        cyl10 = cylinder(0.9, 0.95).move_to(chb10.get_center() + DOWN * 0.25)
        chroma10 = VGroup(chb10, cht10, cyl10)
        ar = Arrow([br.frame.get_right()[0] + 0.05, 1.2, 0], [chb10.get_left()[0] - 0.05, 1.2, 0], buff=0,
                   color=LOOKUP, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.1)
        s_head = VGroup(mono(CORS_HEAD, CAPTION, S.GREY), extra_tag()).arrange(RIGHT, buff=0.3)
        s1_txt = mono(CORS_LINE, CAPTION, DATA)
        _k = CORS_LINE.index("https://")                        # the one site (Text glyphs skip spaces)
        site = s1_txt[_k - CORS_LINE[:_k].count(" "):]
        assert len(site) == len(CORS_LINE) - _k
        s1 = VGroup(box(s1_txt.width + 0.5, 0.5, S.GREY_DARK, fill=S.GREY_DARKER, fill_opacity=1, radius=0.1),
                    s1_txt)
        s1_txt.move_to(s1[0])
        s2_txt = label("no such line for another site", CAPTION, S.GREY)
        s2 = VGroup(box(s1[0].width, 0.5, S.GREY, dashed=True, stroke=2), s2_txt)
        s2_txt.move_to(s2[0])
        strips = VGroup(s_head, s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        strips.move_to([-6.3 + strips.width / 2, -1.85, 0])

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(tl, pic, idx_lab, rd_chip)), caption_extra(tr, False), run_time=0.5)
            self.play(tr.goto(3), FadeIn(br), FadeIn(ill10), run_time=0.6)
            self.play(FadeIn(c_head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in list_rows], lag_ratio=0.3),
                      run_time=0.7)
            vo.wait_until("Opened in Chrome")
            self.play(FadeIn(lan, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("it reads your local database")
            self.play(FadeIn(chroma10), FadeIn(dr), FadeIn(dr_lab), run_time=0.5)
            vo.wait_until("through port 8000")
            self.play(GrowArrow(ar), run_time=0.8)
            self.bring_to_front(dr, dr_lab)
            self.play(Indicate(dr, color=LOOKUP, scale_factor=1.15), Indicate(cyl10, color=TURN, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("Chroma's settings")
            self.play(FadeIn(s_head), FadeIn(s1, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(s2, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("allow that one site")
            self.play(Indicate(site, color=TURN, scale_factor=1.05), run_time=0.8)

        # ========================================================== 11 · part 1 done: the index is built
        rm = RagMap(show=RagMap.TOP + RagMap.BOTTOM + RagMap.LABELS)
        done = label("part 1: the index is built", 24, INK).move_to([0, -3.05, 0])

        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(br, ill10, c_head, list_rows, lan, ar, dr, dr_lab, chroma10, strips)),
                      run_time=0.4)
            self.play(FadeIn(rm), run_time=0.45)
            ticks = []                     # right of each box's top, clear of the labels and the arrows
            for n in ("chunking", "embedding", "database"):
                bx = rm.item(n)
                ticks.append(check_mark(0.32, DATA).move_to([bx.get_right()[0] + 0.2,
                                                             min(bx.get_top()[1] + 0.02, 1.5), 0]))
            self.play(rm.pulse_lane("top", DATA, run_time=0.85),
                      LaggedStart(*[Create(k) for k in ticks], lag_ratio=0.35, run_time=0.85))
            vo.wait_until("the index is built")
            self.play(FadeIn(done, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("In part 2")
            self.play(rm.pulse_lane("bottom", LOOKUP, run_time=1.0))
        self.play(FadeOut(VGroup(rm, *ticks, done)), FadeOut(tr), run_time=0.8)
        self.wait(0.3)
