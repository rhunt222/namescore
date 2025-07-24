import sys
from pathlib import Path

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
