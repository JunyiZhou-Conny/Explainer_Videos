import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_on_merge", ROOT / "tools" / "release_on_merge.py")
rom = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rom)

REPO = "owner/repo"


def episode(root: Path, slug: str, spec: str = "video.yaml", review: str = "") -> None:
    d = root / "videos" / slug
    d.mkdir(parents=True)
    (d / spec).write_text("title: t\n")
    if review:
        (d / "REVIEW.md").write_text(review)


def test_added_episodes_routes_by_spec_and_skips_released_and_published(tmp_path):
    episode(tmp_path, "new-legacy")
    episode(tmp_path, "new-swiss", "episode.json")
    episode(tmp_path, "released")
    episode(tmp_path, "on-bilibili")
    added = ["videos/new-legacy/video.yaml", "videos/new-legacy/script.md", "videos/new-swiss/episode.json",
             "videos/released/video.yaml", "videos/on-bilibili/video.yaml", "videos/gone/video.yaml", "docs/x.md"]
    tags = ["episode/released-v1", "episode/new-legacy-extra-v1", "incubator-2026-10-12"]
    registry = {"episodes": {"on-bilibili": {"bvid": "BV1"}}}
    assert rom.added_episodes(added, tags, registry, tmp_path) == [
        ("new-legacy", "legacy-release.yml"), ("new-swiss", "episode-release.yml")]


def test_names_slug_needs_the_exact_slug():
    assert rom.names_slug("Files: `videos/portal-e5-verify/`.", "portal-e5-verify")
    assert rom.names_slug("branch episode/portal-e5-verify", "portal-e5-verify")
    assert rom.names_slug("see videos/portal-e5-verify", "portal-e5-verify")
    assert not rom.names_slug("videos/portal-e5-verify-b/", "portal-e5-verify")
    assert not rom.names_slug("portal-e5-verify alone", "portal-e5-verify")


def test_single_episode_pr_takes_its_closing_issue(tmp_path):
    episode(tmp_path, "ep")
    issues = [{"number": 7, "body": "no slug here"}, {"number": 9, "body": "videos/ep/"}]
    assert rom.pick_issue("ep", 1, [{"number": 7, "body": ""}], issues, REPO, tmp_path) == 7


def test_review_link_wins_for_a_multi_episode_pr(tmp_path):
    review = f"issue [#66](https://github.com/{REPO}/issues/66) … [#66](https://github.com/{REPO}/issues/66) and #12"
    episode(tmp_path, "e5", review=review)
    issues = [{"number": 66, "body": ""}, {"number": 67, "body": "videos/e5/ as an example"}]
    closing = [{"number": 66, "body": ""}, {"number": 67, "body": ""}]
    assert rom.pick_issue("e5", 2, closing, issues, REPO, tmp_path) == 66


def test_body_match_prefers_closing_issues_and_refuses_ties(tmp_path, capsys):
    episode(tmp_path, "ep")
    issues = [{"number": 3, "body": "example: videos/ep/"}, {"number": 5, "body": "Files: videos/ep/"},
              {"number": 8, "body": "episode/ep"}]
    assert rom.pick_issue("ep", 2, [{"number": 5, "body": "Files: videos/ep/"}], issues, REPO, tmp_path) == 5
    assert rom.pick_issue("ep", 2, [], issues, REPO, tmp_path) is None
    assert "::warning::ep: issues [3, 5, 8]" in capsys.readouterr().out


def test_no_issue_found_warns(tmp_path, capsys):
    episode(tmp_path, "ep")
    assert rom.pick_issue("ep", 1, [], [{"number": 1, "body": "other"}], REPO, tmp_path) is None
    assert "::warning::ep: no episode issue found" in capsys.readouterr().out


def test_closing_issue_of_a_released_episode_never_moves_to_another(tmp_path):
    episode(tmp_path, "old")
    episode(tmp_path, "new")
    added = ["videos/old/video.yaml", "videos/new/video.yaml"]
    issues = [{"number": 4, "body": "videos/old/"}, {"number": 9, "body": "videos/new/"}]
    planned = rom.plan(added, ["episode/old-v1"], {}, [{"number": 4, "body": "videos/old/"}], issues, REPO, tmp_path)
    assert planned == [("new", "legacy-release.yml", 9)]
