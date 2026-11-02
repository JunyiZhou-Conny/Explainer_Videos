"""S07 · Relational plus vectors: one database (V6: two shapes of data, one engine).
Lecture: L16 65–68, 71, 75–76.

Beats (script.md "## S07", one voiceover block each):
 0  LECTURE 16 · 76. V6 begins (illustration). Slide 76's triptych redrawn: headings "relational"
    (GREEN) and "vector" (PINK); GREEN `users` and `orders` tables drop in, a PINK FK line joins them,
    a GREEN bracket "transaction: all or nothing" under them; a PINK vector chip "find the 5 most
    similar cheeses" with distance rays; above both, "both → often PostgreSQL + pgvector".
 1  The triptych condenses into three requirement chips (foreign keys, transactions, similarity
    search) in a strip at the top. Left: CODE(cheese-app-v2/src/vector-db/docker-compose.yml: 19–28),
    lines 20 and 23 lit; a TEAL chromadb container beside it (vector store + metadata) with a GREY
    card "team patches + backs up".
 2  LECTURE 16 · 65–66. The panel fades. ChipSorter: TEAL "ChromaDB on a VM", BLUE "PostgreSQL
    service + pgvector", BLUE "vector search service", one by one as named. The vector chip lands in
    all three; the FK and transaction chips bounce RED off the first and third, then land in the second.
 3  The sorter dims. A fourth combo above it: a "relational DB" box and a "vector DB" box joined by a
    PINK sync arrow; an `order 42` row appears in the first, its embedding is missing (RED dashed) in
    the second, and the arrow drifts RED ("out of sync").
 4  The combo and the vector-only homes fade; the PostgreSQL + pgvector box (every chip) flashes and
    moves left. Its table `cheeses` (GREEN id, name, in_stock) gains a PURPLE `embedding vector(256)`
    column; below, the illustration SQL card `SELECT name FROM cheeses / WHERE in_stock / ORDER BY
    embedding <-> :q / LIMIT 5;`: the WHERE row lights with in_stock, the ORDER BY row with embedding.
 5  LECTURE 16 · 67–68. Two columns, "provider operates" (BLUE) and "team owns" (GREEN), under
    "managed PostgreSQL service"; the chips hosts, storage, patching, backup mechanisms drop into the
    BLUE one and schema, queries, migrations, pooling, restore tests into the GREEN one as named.
    Below: the GREY strip "Google Cloud: Cloud SQL for PostgreSQL · AlloyDB" and slide 68's line in
    YELLOW "High availability and recovery are configurations, not defaults."
 6  The canvas fades. TAKEAWAY, row by row as spoken; then an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedVMobject,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    Transform,
    VGroup,
    Write,
)

from common import *  # noqa: F401,F403
from common import _save_op, _set_op
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]

COMPOSE = "cheese-app-v2/src/vector-db/docker-compose.yml"
assert source_line(COMPOSE, 19).strip() == "chromadb:", source_line(COMPOSE, 19)
assert source_line(COMPOSE, 20).strip() == "image: chromadb/chroma:latest", source_line(COMPOSE, 20)
assert source_line(COMPOSE, 23).strip() == "- 8000:8000", source_line(COMPOSE, 23)

SQL = ["SELECT name FROM cheeses", "WHERE in_stock", "ORDER BY embedding <-> :q", "LIMIT 5;"]
PROVIDER = ["hosts", "storage", "patching", "backup mechanisms"]
TEAM = ["schema", "queries", "migrations", "pooling", "restore tests"]
TAKEAWAY = ("relational + vector needs in **ONE** managed database · think: **PostgreSQL + pgvector** · "
            "foreign keys, transactions and similarity search in one place")

SAFE_L, SAFE_R, SAFE_B, SAFE_T = -6.6, 6.6, -3.6, 3.6
TAG_X = 2.85          # the lecture tag occupies x > TAG_X above y 3.1


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


def inside(m, name="", t=SAFE_T):
    guard(m.get_left()[0] >= SAFE_L and m.get_right()[0] <= SAFE_R and m.get_bottom()[1] >= SAFE_B
          and m.get_top()[1] <= t, f"{name} outside the safe frame: {m.get_left()}, {m.get_right()}, "
          f"{m.get_bottom()}, {m.get_top()}")


def apart(a, b, name="", buff=0.03):
    """a and b must not overlap (bounding boxes)."""
    ok = (a.get_right()[0] + buff <= b.get_left()[0] or b.get_right()[0] + buff <= a.get_left()[0]
          or a.get_top()[1] + buff <= b.get_bottom()[1] or b.get_top()[1] + buff <= a.get_bottom()[1])
    guard(ok, f"overlap: {name}")


def within(a, b, name=""):
    """a's bounding box lies inside b's."""
    guard(a.get_left()[0] >= b.get_left()[0] and a.get_right()[0] <= b.get_right()[0]
          and a.get_bottom()[1] >= b.get_bottom()[1] and a.get_top()[1] <= b.get_top()[1],
          f"{name} not inside")


def flash(mob, color=TURN, k=1.12, run_time=0.6):
    return Indicate(mob, color=color, scale_factor=k, run_time=run_time)


def dim(mob, k=0.3):
    """Transform: every member of mob to k of its current opacity (undim() restores)."""
    _save_op(mob, "_dop7")
    target = mob.copy()
    _set_op(target, k, "_dop7")
    return Transform(mob, target)


def undim(mob):
    target = mob.copy()
    _set_op(target, None, "_dop7")
    return Transform(mob, target)


def mini_rays(color=ROUTE):
    """A query dot with short distance rays to four neighbours (the vector chip's glyph)."""
    pts = [np.array([np.cos(a), np.sin(a), 0]) * r for a, r in zip((0.5, 1.9, 3.4, 4.9), (0.2, 0.15, 0.19, 0.16))]
    return VGroup(*[Line(ORIGIN_, p, color=color, stroke_width=2) for p in pts],
                  *[Dot(p, radius=0.035, color=color) for p in pts], Dot(radius=0.05, color=TURN))


ORIGIN_ = np.array([0.0, 0.0, 0.0])


def need_chip(text, color, rays=False):
    """A compact requirement chip that fits a ChipSorter slot."""
    c = chip(text, color, size=CAPTION)
    if not rays:
        return c
    r = mini_rays(color).next_to(c, LEFT, buff=0.1)
    return VGroup(r, c)


def grey_card(lines):
    rows = VGroup(*[label(s, CAPTION, S.GREY) for s in lines]).arrange(DOWN, buff=0.06)
    fr = box(rows.width + 0.4, rows.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12, stroke=2)
    rows.move_to(fr)
    return VGroup(fr, rows)


def column(title, color, w=5.9, h=2.75):
    fr = box(w, h, color, fill_opacity=0.06, stroke=3)
    t = label(title, 24, color).next_to(fr.get_top(), DOWN, buff=0.16)
    g = VGroup(fr, t)
    g.frame, g.title = fr, t
    return g


def grid_spots(col, n, per_row, top_gap=0.95, dx=1.85, dy=0.6):
    """Chip centres inside a column: rows of per_row, centred."""
    fr = col.frame
    spots = []
    for i in range(n):
        r, c = divmod(i, per_row)
        in_row = min(per_row, n - r * per_row)
        x = fr.get_center()[0] + (c - (in_row - 1) / 2) * dx
        y = fr.get_top()[1] - top_gap - r * dy
        spots.append(np.array([x, y, 0]))
    return spots


class OneDatabase(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · slide 76: classify the data
        itag = illustration_tag()
        place(itag, left=-6.45, top=3.55)
        both = label("both → often PostgreSQL + pgvector", 24, INK)
        place(both, cx=-0.6, cy=2.05)
        brace = VMobject_corners([[-5.6, 1.45, 0], [-5.6, 1.65, 0], [5.6, 1.65, 0], [5.6, 1.45, 0]], S.GREY)
        h_rel = label("relational", 26, OWN)
        h_vec = label("vector", 26, ROUTE)
        place(h_rel, cx=-3.2, cy=0.95)
        place(h_vec, cx=3.3, cy=0.95)
        users = req_table("users", ("id", "email"))
        orders = req_table("orders", ("id", "user_id"))
        place(users, cx=-4.4, cy=-0.35)
        place(orders, cx=-2.0, cy=-0.35)
        fk = fk_line(users, orders)
        txn = txn_bracket(VGroup(users, orders))
        vch = vector_chip()
        place(vch, cx=3.3, cy=-0.35)
        for m, n in ((itag, "illustration tag"), (both, "both label"), (txn, "txn bracket"), (vch, "vector chip")):
            inside(m, n)
        guard(both.get_right()[0] <= TAG_X or both.get_top()[1] <= 3.08, "both label under the lecture tag")
        apart(vch, orders, "vector chip / orders")
        apart(h_rel, users, "relational heading / users")

        with self.voiceover(SAY[0]) as vo:
            lr = lref_swap(self, None, 16, "76")
            self.play(FadeIn(itag), FadeIn(h_rel, shift=DOWN * 0.15), FadeIn(h_vec, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("Classify it first")
            self.play(flash(h_rel, OWN, 1.15), flash(h_vec, ROUTE, 1.15), run_time=0.7)
            vo.wait_until("Users and orders")
            self.play(FadeIn(users, shift=DOWN * 0.6), run_time=0.5)
            self.play(FadeIn(orders, shift=DOWN * 0.6), run_time=0.5)
            vo.wait_until("linked by foreign keys")
            self.play(Create(fk[0]), FadeIn(fk[1]), run_time=0.6)
            self.play(flash(orders.cols[1], ROUTE, 1.2), flash(users.cols[0], ROUTE, 1.2), run_time=0.6)
            vo.wait_until("saved in transactions")
            self.play(Create(txn.bracket), Write(txn.label), run_time=0.8)
            vo.wait_until("that is relational")
            self.play(flash(h_rel, OWN, 1.15), run_time=0.6)
            vo.wait_until("Find the five")
            self.play(FadeIn(vch.chip, shift=DOWN * 0.6), run_time=0.5)
            self.play(LaggedStart(*[Create(r) for r in vch.rays], lag_ratio=0.08), run_time=0.8)
            vo.wait_until("that is vector search")
            self.play(flash(h_vec, ROUTE, 1.15), run_time=0.6)
            self.play(Create(brace), FadeIn(both, shift=DOWN * 0.1), run_time=0.7)

        # ========================================================== 1 · the course today: ChromaDB container
        c_fk = need_chip("foreign keys", OWN)
        c_tx = need_chip("transactions", OWN)
        c_vec = need_chip("similarity search", ROUTE, rays=True)
        strip = VGroup(c_fk, c_tx, c_vec).arrange(RIGHT, buff=0.3)
        place(strip, left=-6.45, top=3.5)
        guard(strip.get_right()[0] <= TAG_X - 0.1, "chip strip runs under the lecture tag")
        pnl = src_panel(COMPOSE, 19, 28, size=20)
        place(pnl, left=-6.45, top=2.55)
        inside(pnl, "compose panel")
        apart(pnl, strip, "panel / chip strip")
        bars = VGroup(pnl.bar(20), pnl.bar(23))
        ctr = container_box("chromadb", w=3.25, h=2.0)
        place(ctr, right=6.45, cy=pnl.get_center()[1] + 0.55)
        ctr_txt = VGroup(label("vector store", CAPTION, INK), label("+ metadata", CAPTION, INK)).arrange(DOWN, buff=0.06)
        place(ctr_txt, cx=ctr.get_center()[0], top=ctr.body_top() - 0.05)
        within(ctr_txt, ctr.frame, "container text")
        ops = grey_card(["team patches", "+ backs up"])
        place(ops, cx=ctr.get_center()[0], top=ctr.get_bottom()[1] - 0.25)
        apart(pnl, ctr, "panel / container")
        apart(pnl, ops, "panel / ops card")
        inside(ops, "ops card")
        img_span = pnl.span(20, "chromadb/chroma:latest")
        a_img = arrow_(img_span.get_right() + RIGHT * 0.05, ctr.frame.get_left(), CTR, stroke=3)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(h_rel, h_vec, both, brace, itag)),
                      ReplacementTransform(VGroup(users, orders, fk), c_fk),
                      ReplacementTransform(txn, c_tx), ReplacementTransform(vch, c_vec), run_time=1.0)
            self.play(FadeIn(pnl, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(bars), run_time=0.4)
            self.play(GrowArrow(a_img), FadeIn(ctr, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("It is a vector store")
            self.play(Write(ctr_txt), flash(c_vec, ROUTE, 1.1), run_time=0.8)
            vo.wait_until("and the team operates it")
            self.play(FadeIn(ops, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("patches, backups")
            self.play(flash(ops, TURN, 1.08), run_time=0.7)
            self.play(ctr.frame.animate.set_stroke(width=6), run_time=0.3)
            self.play(ctr.frame.animate.set_stroke(width=3), run_time=0.3)

        # ========================================================== 2 · slides 65–66: three homes
        cs = ChipSorter()
        cs.shift(DOWN * 0.8)
        for n in ("b0", "b1", "b2"):
            m = cs.parts[n]
            _save_op(m)
            _set_op(m, 0)
            m.hidden = True
        inside(cs, "chip sorter")
        row_y = 1.35
        strip_t = strip.copy().move_to([0, row_y, 0])
        guard(strip_t.get_bottom()[1] >= cs.get_top()[1] + 0.25, "chip row too close to the sorter")
        vec1, vec2 = c_vec.copy(), c_vec.copy()
        notes_b1 = cs.parts["b1"][2]
        base1 = cs.box(1).get_bottom()
        slot_vec, slot_fk, slot_tx = [base1 + UP * (0.3 + 0.52 * k) for k in range(3)]   # 0.42 pitch: borders touched
        guard(slot_tx[1] + c_tx.height / 2 + 0.03 <= notes_b1.get_bottom()[1], "slot 2 runs into box 1's note")

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(pnl, bars, a_img, ctr, ctr_txt, ops)), run_time=0.5)
            lr = lref_swap(self, lr, 16, "65–66")
            self.play(c_fk.animate.move_to(strip_t[0]), c_tx.animate.move_to(strip_t[1]),
                      c_vec.animate.move_to(strip_t[2]), run_time=0.7)
            self.add(cs)
            vo.wait_until("ChromaDB on a virtual machine")
            cs.reveal(self, "b0", run_time=0.5)
            vo.wait_until("a PostgreSQL service")
            cs.reveal(self, "b1", run_time=0.5)
            vo.wait_until("and a vector search service")
            cs.reveal(self, "b2", run_time=0.5)
            vo.wait_until("Vector chips land")
            vec1.move_to(c_vec)
            vec2.move_to(c_vec)
            self.add(vec1, vec2)
            self.play(cs.land(vec1, 0, 0), c_vec.animate.move_to(slot_vec), cs.land(vec2, 2, 0), run_time=0.9)
            self.play(*[flash(m, ROUTE, 1.08) for m in (vec1, c_vec, vec2)], run_time=0.5)
            vo.wait_until("Foreign keys and transactions bounce")
            self.play(*cs.bounce(c_fk, 0), *cs.bounce(c_tx, 2), run_time=0.9)
            self.play(*cs.bounce(c_fk, 2), *cs.bounce(c_tx, 0), run_time=0.9)
            self.play(c_fk.animate.move_to(slot_fk), c_tx.animate.move_to(slot_tx), run_time=0.7)
            self.play(flash(cs.box(1), TURN, 1.03), run_time=0.6)

        # ========================================================== 3 · two databases drift apart
        rel = box(3.8, 1.85, CLOUD, fill_opacity=0.06, stroke=3)
        vdb = box(3.8, 1.85, CLOUD, fill_opacity=0.06, stroke=3)
        place(rel, cx=-3.7, cy=1.95)
        place(vdb, cx=3.3, cy=1.95)
        rel_t = label("relational DB", CAPTION, INK).next_to(rel.get_top(), DOWN, buff=0.12)
        vdb_t = label("vector DB", CAPTION, INK).next_to(vdb.get_top(), DOWN, buff=0.12)
        r41 = mono("order 41", CAPTION, OWN)
        r42 = mono("order 42", CAPTION, OWN)
        VGroup(r41, r42).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(rel_t, DOWN, buff=0.15)
        e41 = mono("emb · order 41", CAPTION, ROUTE)
        e42 = mono("emb · order 42", CAPTION, ERR)
        VGroup(e41, e42).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(vdb_t, DOWN, buff=0.15)
        VGroup(e41, e42).align_to(vdb, LEFT).shift(RIGHT * 0.3)
        miss = DashedVMobject(box(e42.width + 0.2, e42.height + 0.08, ERR, fill_opacity=0), num_dashes=24)
        miss.move_to(e42)
        miss_q = label("missing", CAPTION, ERR).next_to(miss, RIGHT, buff=0.1)
        syn = DoubleArrow(rel.get_right() + RIGHT * 0.05, vdb.get_left() + LEFT * 0.05, color=ROUTE,
                          stroke_width=4, buff=0, tip_length=0.2)
        syn_t = label("sync", CAPTION, ROUTE).next_to(syn, UP, buff=0.08)
        syn_bad = label("out of sync", CAPTION, ERR).next_to(syn, DOWN, buff=0.08)
        combo = VGroup(rel, vdb, rel_t, vdb_t, r41, e41, syn, syn_t)
        inside(VGroup(combo, miss_q), "two-database combo", t=3.08)
        apart(VGroup(combo, miss_q), cs, "combo / sorter")
        within(r42, rel, "order 42 row")
        within(VGroup(e42, miss), vdb, "missing embedding")
        guard(miss_q.get_right()[0] <= vdb.get_right()[0] - 0.05, "missing note leaves the vector box")
        in_boxes = [vec1, c_vec, vec2, c_fk, c_tx]

        with self.voiceover(SAY[3]) as vo:
            self.play(dim(cs, 0.3), *[dim(m, 0.3) for m in in_boxes], run_time=0.6)
            self.play(FadeIn(VGroup(rel, rel_t, r41)), FadeIn(VGroup(vdb, vdb_t, e41)), run_time=0.7)
            vo.wait_until("But then they must stay in sync")
            self.play(GrowArrow(syn), FadeIn(syn_t), run_time=0.7)
            vo.wait_until("and one day an order exists")
            self.play(FadeIn(r42, shift=RIGHT * 0.15), flash(rel, OWN, 1.03), run_time=0.7)
            vo.wait_until("while its embedding is missing")
            self.play(Create(miss), FadeIn(miss_q), run_time=0.6)
            self.play(syn.animate.set_color(ERR).shift(DOWN * 0.08), syn_t.animate.set_color(ERR),
                      FadeIn(syn_bad), run_time=0.8)

        # ========================================================== 4 · one table, one query
        b1 = cs.parts["b1"]
        shift_b1 = np.array([-6.45 - b1.get_left()[0], 2.55 - b1.get_top()[1], 0])
        table = DbTable()
        place(table, right=6.45, cy=2.55 - b1.height / 2 + 0.35)
        guard(table.get_left()[0] >= b1.get_right()[0] + shift_b1[0] + 0.15, "table runs into the box")
        table.add_column()                       # only to measure; the column is shown below
        inside(table, "cheeses table")
        table.remove(table.new_col)
        sql = illustration_card(SQL)
        place(sql, cx=table.get_center()[0] - 0.4, top=table.get_bottom()[1] - 0.6)
        inside(sql, "SQL card")
        apart(sql, table, "SQL card / table")
        guard(sql.get_left()[0] >= b1.get_right()[0] + shift_b1[0] + 0.15
              or sql.get_top()[1] <= b1.get_bottom()[1] + shift_b1[1] - 0.15, "SQL card / box")
        link = arrow_(np.array([b1.get_right()[0] + shift_b1[0] + 0.05, table.get_center()[1], 0]),
                      table.frame.get_left() + LEFT * 0.05, CLOUD, stroke=3)
        pgv = chip("pgvector", TOOL, size=CAPTION)
        in_stock = table.cols[2]
        where_row, order_row = sql.rows[1], sql.rows[2]

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(combo, r42, miss, miss_q, syn_bad)), undim(cs),
                      *[undim(m) for m in in_boxes], run_time=0.7)
            self.play(*cs.parts_out("b0", "b2"), FadeOut(vec1), FadeOut(vec2), flash(b1[0], TURN, 1.04),
                      run_time=0.7)
            self.play(b1.animate.shift(shift_b1), *[m.animate.shift(shift_b1) for m in (c_vec, c_fk, c_tx)],
                      run_time=0.8)
            self.play(GrowArrow(link), FadeIn(table, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("The vector column sits")
            col_anims = table.add_column()
            place(pgv, cx=table.new_col.get_center()[0], bottom=table.frame.get_top()[1] + 0.1)
            inside(pgv, "pgvector chip", t=3.08)
            self.play(*col_anims, FadeIn(pgv, shift=DOWN * 0.1), run_time=0.7)
            self.play(flash(VGroup(*table.cols), OWN, 1.06), run_time=0.6)
            vo.wait_until("and one query filters")
            self.play(FadeIn(sql, shift=UP * 0.15), run_time=0.6)
            self.play(where_row.animate.set_color(OWN), flash(in_stock, OWN, 1.15), run_time=0.7)
            vo.wait_until("orders by similarity")
            self.play(order_row.animate.set_color(TOOL), flash(table.new_col, TOOL, 1.1), run_time=0.7)

        # ========================================================== 5 · slides 67–68: managed ≠ hands-off
        head = label("managed PostgreSQL service", 26, CLOUD)
        place(head, cx=-1.2, cy=2.85)
        guard(head.get_right()[0] <= TAG_X or head.get_top()[1] <= 3.08, "head under the lecture tag")
        prov = column("provider operates", CLOUD)
        team = column("team owns", OWN)
        place(prov, left=-6.3, top=2.4)
        place(team, right=6.3, top=2.4)
        prov_chips = [chip(s, CLOUD, size=CAPTION) for s in PROVIDER]
        team_chips = [chip(s, OWN, size=CAPTION) for s in TEAM]
        for c, p in zip(prov_chips, grid_spots(prov, 4, 2, dx=2.6)):
            c.move_to(p)
        for c, p in zip(team_chips, grid_spots(team, 5, 2, dx=2.4)):
            c.move_to(p)
        for c in prov_chips:
            within(c, prov.frame, "provider chip")
        for c in team_chips:
            within(c, team.frame, "team chip")
        for a, b in ((prov_chips[0], prov_chips[1]), (prov_chips[2], prov_chips[3]),
                     (team_chips[0], team_chips[1]), (team_chips[2], team_chips[3])):
            apart(a, b, "column chips")
        gcp = grey_chip("Google Cloud: Cloud SQL for PostgreSQL · AlloyDB")
        place(gcp, cx=0, top=prov.get_bottom()[1] - 0.3)
        ha = label("High availability and recovery are configurations, not defaults.", 24, TURN)
        place(ha, cx=0, top=gcp.get_bottom()[1] - 0.3)
        inside(ha, "slide 68 line")
        apart(prov, team, "the two columns")

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(cs, c_vec, c_fk, c_tx, link, table, pgv, sql)), run_time=0.6)
            lr = lref_swap(self, lr, 16, "67–68")
            self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(prov), FadeIn(team), run_time=0.7)
            vo.wait_until("runs the hosts")
            self.play(FadeIn(prov_chips[0], shift=DOWN * 0.5), FadeIn(prov_chips[1], shift=DOWN * 0.5), run_time=0.5)
            vo.wait_until("and the patching")
            self.play(FadeIn(prov_chips[2], shift=DOWN * 0.5), FadeIn(prov_chips[3], shift=DOWN * 0.5), run_time=0.5)
            vo.wait_until("Your team still owns")
            self.play(flash(team.title, OWN, 1.12), run_time=0.5)
            vo.wait_until("the schema")
            self.play(FadeIn(team_chips[0], shift=DOWN * 0.5), FadeIn(team_chips[1], shift=DOWN * 0.5),
                      FadeIn(team_chips[2], shift=DOWN * 0.5), run_time=0.5)
            vo.wait_until("pooling")
            self.play(FadeIn(team_chips[3], shift=DOWN * 0.5), run_time=0.4)
            vo.wait_until("restore tests")
            self.play(FadeIn(team_chips[4], shift=DOWN * 0.5), run_time=0.4)
            vo.wait_until("On Google Cloud")
            self.play(FadeIn(gcp, shift=UP * 0.1), run_time=0.5)
            self.play(Write(ha), run_time=1.0)
            vo.wait_until("or AlloyDB")
            self.play(flash(gcp, CLOUD, 1.06), run_time=0.7)

        # ========================================================== 6 · takeaway
        tk = takeaway(TAKEAWAY)
        inside(tk, "takeaway")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(head, prov, team, *prov_chips, *team_chips, gcp, ha)), FadeOut(lr),
                      run_time=0.6)
            self.play(FadeIn(VGroup(tk.frame, tk.head)), FadeIn(tk.rows[0], shift=RIGHT * 0.15), run_time=0.7)
            vo.wait_until("in one managed database")
            self.play(flash(tk.rows[0], TURN, 1.03), run_time=0.6)
            vo.wait_until("PostgreSQL plus pgvector")
            self.play(FadeIn(tk.rows[1], shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("Foreign keys, transactions")
            self.play(FadeIn(tk.rows[2], shift=RIGHT * 0.15), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(tk), run_time=0.6)
        self.wait(0.3)


def VMobject_corners(points, color, stroke=2.5):
    from manim import VMobject
    return VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(points)
