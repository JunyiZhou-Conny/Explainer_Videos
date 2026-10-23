"""The Studio data builder: stage derivation, the series map and the library model."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("studio_status", ROOT / "tools" / "studio_status.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

SERIES = st.load_series(ROOT / "catalog" / "series.json")
T0 = "2026-10-20T00:00:00Z"


def at(hours: float) -> str:
    return st.ts_iso(st.iso_ts(T0) + hours * 3600)


def issue(n, title="[episode] AC215 L09 · CI and unit testing", labels=("episode", "AC215",
          "state:scripting"), state="open", body="Planned slug: videos/ac215-l09-ci-testing"):
    return {"number": n, "title": title, "state": state, "body": body, "html_url": f"u/{n}",
            "updated_at": at(0), "labels": [{"name": x} for x in labels]}


def comment(hours, body):
    return {"created_at": at(hours), "body": body}


def labeled(hours, name):
    return {"event": "labeled", "created_at": at(hours), "label": {"name": name}}


CLAIM = "Claiming. Model: Claude, surface: cloud, branch claude/batch (moves to episode/x)."


def test_stage_weights_are_a_whole():
    assert sum(w for *_, w, _ in st.STAGES) == 100
    assert len(st.INDEX) == len(st.STAGES)
    assert st.percent("ready", "ready", None) == 94
    assert st.percent("published", "published", None) == 100


def test_checkpoint_marks_the_stage_done():
    d = st.derive(issue(1), [comment(0, CLAIM), comment(1, "CHECKPOINT captures"),
                             comment(2, "CHECKPOINT brief"), comment(3, "**CHECKPOINT script**")], [])
    assert (d["stage"], d["state"], d["source"]) == ("scenes", "active", "checkpoint")
    assert d["claim"]["branch"] == "claude/batch"
    colon = st.derive(issue(1), [comment(0, CLAIM), comment(1, "CHECKPOINT: scenes")], [])
    assert colon["stage"] == "qa"


def test_paused_checkpoint_stays_inside_its_stage():
    d = st.derive(issue(1), [comment(0, CLAIM), comment(5, "CHECKPOINT qa (paused for the night)")], [])
    assert d["stage"] == "qa"


def test_newer_stage_label_wins_over_older_checkpoint():
    # the L07 trail: a paused script checkpoint, later the session moved the scenes label
    i = issue(52, labels=("episode", "AC215", "state:scripting", "▶ 制作场景"))
    d = st.derive(i, [comment(0, CLAIM), comment(1, "CHECKPOINT script (paused)")],
                  [labeled(9, "▶ 制作场景")])
    assert (d["stage"], d["source"]) == ("scenes", "label")
    assert d["since"] == st.iso_ts(at(9))


def test_newer_checkpoint_advances_past_a_stale_label():
    i = issue(1, labels=("episode", "▶ 制作场景"))
    d = st.derive(i, [comment(0, CLAIM), comment(10, "CHECKPOINT scenes")], [labeled(2, "▶ 制作场景")])
    assert d["stage"] == "qa"


def test_lifecycle_tail_overrides_lingering_labels():
    # the L05 trail: closed, released, three state labels at once
    i = issue(38, state="closed", labels=("episode", "state:scripting", "state:publishing",
                                         "✔ 等待合并发布"))
    d = st.derive(i, [], [])
    assert (d["stage"], d["state"]) == ("publishing", "publishing")
    assert st.derive(issue(2, labels=("episode", "state:published"), state="closed"), [], [])["state"] == "published"
    assert st.derive(issue(3, labels=("episode", "state:scripting"), state="closed"), [], [])["state"] == "closed"


def test_pause_and_question_take_precedence():
    paused = st.derive(issue(34, labels=("episode", "⏸ 暂停")), [comment(0, CLAIM),
                       comment(1, "CHECKPOINT full-cut")], [])
    assert (paused["stage"], paused["state"]) == ("ready", "paused")
    q = st.derive(issue(5, labels=("episode", "blocked:question", "▶ 整片审查")), [comment(0, CLAIM)], [])
    assert q["state"] == "question"


def test_handoff_releases_the_claim():
    d = st.derive(issue(1), [comment(0, CLAIM), comment(1, "CHECKPOINT brief"),
                             comment(2, "HANDOFF\nDONE ...")], [])
    assert d["claim"] is None and d["stage"] == "script"


def test_quote_reply_is_not_a_protocol_event():
    d = st.derive(issue(1), [comment(0, CLAIM), comment(1, "> CHECKPOINT full-cut\nthanks")], [])
    assert d["stage"] == "brief"


def test_progress_line_refines_only_the_current_stage():
    body = "CHECKPOINT script\nDONE: script\n**Progress:** scenes 3/16"
    d = st.derive(issue(1), [comment(0, CLAIM), comment(1, "CHECKPOINT script"),
                             comment(4, "- Progress: 场景 12/16")], [])
    assert d["progress"] == {"stage": "scenes", "done": 12, "total": 16, "at": st.iso_ts(at(4))}
    assert st.percent(d["stage"], d["state"], d["progress"]) == 20 + round(30 * 12 / 16)
    stale = st.derive(issue(1), [comment(0, CLAIM), comment(1, "Progress: brief 2/3"),
                                 comment(2, body)], [])
    assert stale["stage"] == "scenes" and stale["progress"]["done"] == 3
    other = st.derive(issue(1), [comment(0, CLAIM), comment(1, "CHECKPOINT script"),
                                 comment(2, "Progress: qa 1/5")], [])
    assert other["progress"] is None


def snapshot():
    issues = [
        issue(46), issue(47, title="[episode] AC215 L10 · Cloud", body="videos/ac215-l10-cloud"),
        issue(48, title="[episode] AC215 L11 · Data", body="videos/ac215-l11-data"),
        issue(38, title="[episode] AC215 L05 · RAG", state="closed", body="episode/ac215-l05-rag",
              labels=("episode", "AC215", "state:publishing")),
        issue(35, title="[episode] AC215 L02 · Containers", state="closed",
              body="videos/ac215-l02-containers-1", labels=("episode", "AC215", "state:published")),
        issue(60, title="[episode] Why git?", body="videos/solo-git", labels=("episode", "state:full-review")),
        issue(61, title="[episode] Lonely", body="videos/lonely", labels=("episode", "state:scripting")),
    ]
    solo = "Claiming. Model: GPT, surface: cursor, branch episode/lonely."
    return {
        "issues": issues,
        "comments": {"46": [comment(0, CLAIM), comment(3, "CHECKPOINT script")],
                     "47": [comment(0, CLAIM), comment(2, "CHECKPOINT brief")],
                     "48": [comment(0, CLAIM)], "60": [], "61": [comment(1, solo)]},
        "events": {},
        "pulls": [{"number": 70, "title": "Why git", "html_url": "pr/70", "draft": True,
                   "updated_at": at(5), "head": {"ref": "episode/solo-git"}}],
        "releases": [],
    }


def test_build_status_queues_batch_siblings_and_maps_the_series():
    reg = {"episodes": {"ac215-l02-containers-1": {"bvid": "BV1x", "title": "第2讲"}}}
    s = st.build_status(snapshot(), SERIES, reg, "o/r", st.iso_ts(at(6)))
    by = {e["number"]: e for e in s["episodes"]}
    assert by[46]["state"] == "active" and by[46]["code"] == "L09" and by[46]["title"] == "CI and unit testing"
    assert by[48]["state"] == "queued" and by[48]["percent"] == 0          # waits for L09/L10
    assert by[61]["state"] == "active" and by[61]["stage"] == "brief"      # alone on its branch
    assert by[48]["branch_activity_at"] == at(3)                           # judged with siblings
    assert by[38]["state"] == "publishing" and by[60]["state"] == "ready"
    assert by[60]["pr"] == {"number": 70, "url": "pr/70", "draft": True}
    assert by[35]["bilibili"]["bvid"] == "BV1x" and by[35]["series"] == "ac215"
    assert [e["number"] for e in s["episodes"]][:5] == [35, 38, 46, 47, 48]   # lecture order
    ac = s["series"][0]
    cells = {c["n"]: c["state"] for c in ac["cells"]}
    assert ac["planned"] == 23 and len(ac["cells"]) == 23
    assert (cells[2], cells[5], cells[9], cells[11], cells[12], cells[1]) == (
        "published", "publishing", "active", "queued", "skip", "none")
    assert sum(ac["counts"].values()) == 23


def test_library_groups_orders_and_fills_from_releases():
    catalog = {"artifacts": [
        {"episode": "ac215-l03-x", "title": "L3", "variant": "English narration / clean",
         "download_url": "c3", "bytes": 1, "duration_seconds": 100},
        {"episode": "ac215-l03-x", "title": "L3", "variant": "English narration / bilingual captions (burned)",
         "download_url": "b3", "bytes": 1, "duration_seconds": 100},
        {"episode": "old-solo", "title": "Old", "variant": "English narration / bilingual captions",
         "download_url": "o", "bytes": 1},
        {"episode": "new-solo", "title": "New", "variant": "English narration / bilingual captions",
         "download_url": "n", "bytes": 1},
    ]}
    releases = [{"tag_name": "episode/ac215-l02-y-v1", "name": "AC215 · L2 (follow-along: z)",
                 "published_at": at(1), "assets": [
                     {"name": "ac215-l02-y.mp4", "size": 5, "browser_download_url": "r-clean"},
                     {"name": "ac215-l02-y.zh-en.mp4", "size": 5, "browser_download_url": "r-bi"},
                     {"name": "ac215-l02-y_part1.mp4", "size": 2, "browser_download_url": "r-p1"},
                     {"name": "ac215-l02-y.srt", "size": 1, "browser_download_url": "r-srt"}]},
                {"tag_name": "episode/ac215-l03-x-v2", "name": "ignored: catalog wins", "assets": []}]
    validations = {"ac215-l02-y": {"seconds": {"ac215-l02-y.zh-en.mp4": 1800.5}}}
    reg = {"episodes": {"new-solo": {"bvid": "BVn", "title": "新", "pubdate": 200},
                        "old-solo": {"bvid": "BVo", "title": "旧", "pubdate": 100}}}
    lib = st.build_library(catalog, reg, SERIES, releases, validations, 0)
    ac, solo = lib["series"]
    assert [e["code"] for e in ac["episodes"]] == ["L02", "L03"]
    l2, l3 = ac["episodes"]
    assert l2["title"] == "AC215 · L2" and l2["seconds"] == 1800.5
    assert l2["primary"]["url"] == "r-bi" and [v["url"] for v in l2["variants"]] == ["r-bi", "r-clean", "r-p1"]
    assert l3["primary"]["url"] == "b3"
    assert [e["slug"] for e in solo["episodes"]] == ["new-solo", "old-solo"]   # newest first
    assert (solo["episodes"][0]["title"], solo["episodes"][0]["subtitle"]) == ("新", "New")
    assert l2["title"] == "AC215 · L2"     # no Chinese title yet; nothing to strip but the release suffix
    assert lib["totals"] == {"episodes": 4, "published": 2, "seconds": 1900}


def test_main_writes_both_files(tmp_path):
    snap = tmp_path / "snap.json"
    snap.write_text(json.dumps(snapshot()), encoding="utf-8")
    assert st.main(["--snapshot", str(snap), "--out", str(tmp_path / "data"), "--now", at(6),
                    "--repo", "o/r"]) == 0
    status = json.loads((tmp_path / "data" / "status.json").read_text(encoding="utf-8"))
    library = json.loads((tmp_path / "data" / "library.json").read_text(encoding="utf-8"))
    assert status["generated_at"] == at(6) and status["episodes"]
    assert status["worker_command"].endswith("publish_worker.py --repo o/r --upload")
    assert library["series"][0]["id"] == "ac215"


def test_committed_series_registry_is_well_formed():
    ids = [s["id"] for s in SERIES]
    assert len(ids) == len(set(ids)) and ids[-1] == "standalone"
    for s in SERIES:
        if s.get("planned"):
            assert s.get("code") and s.get("_title") and s.get("_slug")
            assert all(1 <= int(k) <= s["planned"] for k in s.get("skip", {}))


def test_branch_pushes_count_as_activity():
    snap = snapshot()
    snap["branches"] = {"claude/batch": at(30), "episode/lonely": None}
    s = st.build_status(snap, SERIES, {}, "o/r", st.iso_ts(at(31)))
    by = {e["number"]: e for e in s["episodes"]}
    assert by[48]["branch_activity_at"] == at(30)        # a WIP push, not a checkpoint
    assert by[61]["branch_activity_at"] == at(1)         # no push recorded: protocol time


def test_display_titles_prefer_chinese_and_drop_series_prefixes():
    ac, solo = SERIES[0], SERIES[-1]
    assert st.display_titles(ac, "AC215 L2: Containers I — one image", "AC215 第2讲跟练 · 容器入门：一个 image",
                             "ac215-l02") == ("容器入门：一个 image", "Containers I — one image")
    assert st.display_titles(ac, "AC215 · Lecture 5 — Introduction to RAG", None, "x") == ("Introduction to RAG", None)
    assert st.display_titles(SERIES[1], "CareOneX E6: measuring search", "CareOneX Voice Agent EP6", "x") == (
        "Measuring search", None)                      # a Latin-only Bilibili title stays secondary
    assert st.display_titles(solo, None, None, "tictactoe-255168-short") == ("Tictactoe 255168 short", None)
