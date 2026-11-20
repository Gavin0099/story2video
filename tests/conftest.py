import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_file():
    return FIXTURES / "episode.valid.json"


@pytest.fixture
def invalid_file():
    return FIXTURES / "episode.invalid.json"


@pytest.fixture
def episode_data(valid_file):
    return json.loads(valid_file.read_text(encoding="utf-8"))


@pytest.fixture
def write_episode(tmp_path):
    def write(data, filename="episode.json"):
        path = tmp_path / filename
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    return write
