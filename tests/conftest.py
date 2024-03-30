from pathlib import Path

import pytest


@pytest.fixture
def html_content():
    single_bird_observation_path = Path("tests/test_data/single_bird_observation.html")
    multiple_bird_observations_path = Path(
        "tests/test_data/multiple_bird_observations.html"
    )
    return {
        "single_bird_observation": single_bird_observation_path.read_text(),
        "multiple_bird_observations": multiple_bird_observations_path.read_text(),
    }
