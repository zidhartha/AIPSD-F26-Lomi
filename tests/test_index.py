import json
from pathlib import Path

import pytest

from src.index import IndexMismatch, load, save


def test_index_refuses_vectors_from_another_model(index, tmp_path):
    save(index, tmp_path)
    meta_path = tmp_path / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["embed_model"] = "other/model"
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    with pytest.raises(IndexMismatch):
        load(tmp_path)


def test_saved_index_round_trip_keeps_the_model_name(index, tmp_path):
    save(index, tmp_path)
    loaded = load(Path(tmp_path))
    assert loaded.model == index.model
    assert len(loaded.chunks) == len(index.chunks)
