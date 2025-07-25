import sys
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from name_similarity import compute_score, THRESHOLD


def test_identical_names():
    assert compute_score("John Doe", "John Doe") == (100, 100)


def test_nickname_match():
    first, last = compute_score("Bob", "Robert")
    assert first == 100


def test_dissimilar_names_below_threshold():
    first, last = compute_score("Alice Johnson", "Zach Smith")
    assert first < THRESHOLD
    assert last < THRESHOLD


def test_cli_requires_full_names():
    script = ROOT / "name_similarity.py"
    result = subprocess.run(
        [sys.executable, str(script), "compare", "John", "Doe"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Both names must include first and last name" in result.stderr


def test_sample_command_outputs_pairs():
    script = ROOT / "name_similarity.py"
    result = subprocess.run(
        [sys.executable, str(script), "samples"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    messages = [line for line in lines if "Alias" in line]
    assert len(messages) >= 25
