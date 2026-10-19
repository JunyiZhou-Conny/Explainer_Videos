import importlib.util
import json
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bilibili_registry", ROOT / "tools" / "bilibili_registry.py")
reg_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reg_mod)


def empty():
    return {"schema_version": 1, "mid": 1, "episodes": {}, "unmatched": []}


def test_record_is_idempotent_and_clears_unmatched():
    reg = empty()
    reg["unmatched"] = [{"bvid": "BV1", "title": "t", "pubdate": 5}]
    assert reg_mod.record(reg, "ep", "BV1", "t", 5)
    assert reg["unmatched"] == []
    assert not reg_mod.record(reg, "ep", "BV1", "t", 999)
    assert reg["episodes"]["ep"]["pubdate"] == 5


def test_match_records_exact_titles_and_keeps_the_rest():
    reg = empty()
    reg_mod.record(reg, "known", "BV0", "old", 1)
    archives = [
        {"bvid": "BV0", "title": "old", "pubdate": 1},          # already registered
        {"bvid": "BV1", "title": "标题一 ", "pubdate": 3},       # matches after strip
        {"bvid": "BV2", "title": "别的视频", "pubdate": 2},       # no episode by that title
        {"bvid": "BV3", "title": "旧标题", "pubdate": 4},        # names an episode that is already registered
    ]
    titles = {"标题一": "ep1", "旧标题": "known"}
    assert reg_mod.match(reg, archives, titles)
    assert reg["episodes"]["ep1"]["bvid"] == "BV1"
    assert reg["episodes"]["known"]["bvid"] == "BV0"
    assert [a["bvid"] for a in reg["unmatched"]] == ["BV3", "BV2"]
    assert not reg_mod.match(reg, archives, titles)


def test_known_titles_reads_script_json(tmp_path):
    ep = tmp_path / "videos" / "demo"
    ep.mkdir(parents=True)
    (ep / "script.json").write_text(json.dumps({"title_zh": "演示"}), encoding="utf-8")
    (tmp_path / "videos" / "legacy").mkdir()
    assert reg_mod.known_titles(tmp_path) == {"演示": "demo"}


def test_known_titles_reads_legacy_publish_blocks(tmp_path):
    # Legacy (video.yaml) episodes carry their Bilibili title in the publish block;
    # the worker uploads it capped at 80 chars, so the sync must match that form.
    ep = tmp_path / "videos" / "legacy-ep"
    ep.mkdir(parents=True)
    long_tail = "很" * 100
    (ep / "video.yaml").write_text(
        'title: internal\npublish:\n  title_zh: "AC215 跟练 · ' + long_tail + '"\n'
        '  description_zh: |\n    两行\n    说明\n', encoding="utf-8")
    titles = reg_mod.known_titles(tmp_path)
    assert list(titles.values()) == ["legacy-ep"]
    key = next(iter(titles))
    assert key.startswith("AC215 跟练") and len(key) == 80


def test_risk_control_refusal_is_unavailable(monkeypatch):
    def refuse(*a, **k):
        raise urllib.error.HTTPError("u", 412, "Precondition Failed", {}, None)
    monkeypatch.setattr(reg_mod.urllib.request, "urlopen", refuse)
    with pytest.raises(reg_mod.Unavailable):
        reg_mod.fetch_channel(1)


def test_committed_registry_names_catalog_episodes():
    reg = reg_mod.load()
    catalog = json.loads((ROOT / "catalog" / "videos.json").read_text(encoding="utf-8"))
    slugs = {a["episode"] for a in catalog["artifacts"]}
    assert set(reg["episodes"]) <= slugs
    bvids = [e["bvid"] for e in reg["episodes"].values()] + [a["bvid"] for a in reg["unmatched"]]
    assert len(bvids) == len(set(bvids))
