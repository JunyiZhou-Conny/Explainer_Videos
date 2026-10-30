import importlib.util
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pr_digest", ROOT / "tools" / "pr_digest.py")
pd = importlib.util.module_from_spec(spec)
sys.modules["pr_digest"] = pd  # dataclasses look their module up while the class is built
spec.loader.exec_module(pd)

TZ = ZoneInfo("America/New_York")


def run(repo, *args, when=None):
    env = {"GIT_AUTHOR_NAME": "Claude", "GIT_AUTHOR_EMAIL": "c@example.com",
           "GIT_COMMITTER_NAME": "Claude", "GIT_COMMITTER_EMAIL": "c@example.com",
           "PATH": "/usr/bin:/bin"}
    if when:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


def commit(repo, path, text, msg, when):
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_text(text)
    run(repo, "add", path)
    run(repo, "commit", "-m", msg, when=when)


def make_repo(tmp_path):
    """main with one merged PR (#1), an open PR branch (base) and a branch stacked on it (top)."""
    repo = tmp_path / "proj"
    repo.mkdir()
    run(repo, "init", "-b", "main")
    commit(repo, "README.md", "hi\n", "Start", "2026-10-20T09:00:00-04:00")
    run(repo, "switch", "-c", "feat/docs")
    commit(repo, "docs/decisions/0001-x.md", "# 0001: Keep it small\n", "Record decision 0001",
           "2026-10-26T10:00:00-04:00")
    run(repo, "switch", "main")
    run(repo, "merge", "--no-ff", "feat/docs", "-m",
        "Merge pull request #1 from owner/feat/docs\n\nWrite down the first decision",
        when="2026-10-26T11:00:00-04:00")
    run(repo, "switch", "-c", "base")
    commit(repo, "src/a.py", "a\n", "Add the engine", "2026-10-27T09:00:00-04:00")
    run(repo, "switch", "-c", "top")
    commit(repo, "ui/page.py", "p\n", "Draw the page", "2026-10-27T10:00:00-04:00")
    run(repo, "switch", "base")
    commit(repo, "src/b.py", "b\n", "Fix the engine", "2026-10-27T15:00:00-04:00")
    run(repo, "switch", "top")
    run(repo, "merge", "--no-ff", "base", "-m", "Merge branch 'base' into top",
        when="2026-10-27T15:30:00-04:00")
    commit(repo, "ui/page.py", "p2\n", "Polish the page", "2026-10-27T15:40:00-04:00")
    run(repo, "switch", "main")
    return repo


def window():
    return datetime(2026, 10, 26, tzinfo=TZ), datetime(2026, 11, 2, tzinfo=TZ)


def test_merged_open_and_stacked_branches_get_only_their_own_commits(tmp_path):
    repo = make_repo(tmp_path)
    text = pd.digest(repo, *window(), TZ)
    assert "| #1 Write down the first decision | merged | 1 |" in text
    assert "`docs/decisions/0001-x.md`: 0001: Keep it small" in text
    base = text.split("## `base`")[1].split("## ")[0]
    top = text.split("## `top`")[1]
    assert "Add the engine" in base and "Fix the engine" in base and "Draw the page" not in base
    assert "Draw the page" in top and "Polish the page" in top
    assert "Add the engine" not in top and "Fix the engine" not in top     # the base's work
    assert "2 commits (+1 merges)" in top
    # 10:00 -> 15:40 has a pause of more than 90 minutes: the timeline splits it
    assert "Draw the page\n\n- 10-27 15:40" in top


def test_prs_json_names_branches_and_filters_by_author(tmp_path):
    repo = make_repo(tmp_path)
    prs = [{"number": 7, "title": "Engine", "state": "open", "draft": False,
            "user": {"login": "me"}, "head": {"ref": "base"}},
           {"number": 8, "title": "Page", "state": "open", "draft": True,
            "user": {"login": "me"}, "head": {"ref": "top"}},
           {"number": 1, "title": "Docs", "state": "closed", "user": {"login": "someone"},
            "head": {"ref": "feat/docs"}}]
    text = pd.digest(repo, *window(), TZ, prs=prs, pr_author="me")
    assert "## #7 · Engine" in text and "## #8 · Page" in text
    assert "| #8 Page | draft |" in text
    assert "#1" not in text


def test_window_excludes_older_commits(tmp_path):
    repo = make_repo(tmp_path)
    text = pd.digest(repo, datetime(2026, 10, 27, 12, tzinfo=TZ), datetime(2026, 10, 28, tzinfo=TZ), TZ)
    assert "Fix the engine" in text and "Polish the page" in text
    assert "Add the engine" not in text and "#1" not in text


def test_reused_branch_maps_to_the_open_then_newest_pr():
    """GitHub lists newest first; a reused head ref must not fall back to its oldest closed PR."""
    def pr(n, state):
        return {"number": n, "state": state, "title": f"PR {n}", "head": {"ref": "claude/reused"},
                "user": {"login": "someone"}}

    unit = pd.Unit(branch="claude/reused", tip="abc", state="open")
    pd.apply_prs([unit], [pr(9, "closed"), pr(7, "open"), pr(4, "closed")])
    assert unit.number == 7

    unit = pd.Unit(branch="claude/reused", tip="abc", state="open")
    pd.apply_prs([unit], [pr(9, "closed"), pr(6, "closed"), pr(4, "closed")])
    assert unit.number == 9
