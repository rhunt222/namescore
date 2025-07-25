#!/usr/bin/env python3
"""Utilities for comparing personal names with nickname support."""
import argparse
from rapidfuzz import fuzz
from nicknames import NickNamer

# initialize NickNamer
nn = NickNamer()

# default threshold for acceptable alias match
THRESHOLD = 80

# list of sample name pairs for the "samples" command
SAMPLES = [
    ("Robert Smith", "Bob Smith"),
    ("William Johnson", "Bill Johnson"),
    ("James Brown", "Jim Brown"),
    ("John Wilson", "Jonathan Wilson"),
    ("Margaret Taylor", "Maggie Taylor"),
    ("Elizabeth Thomas", "Liz Thomas"),
    ("Jennifer White", "Jen White"),
    ("Christopher Harris", "Chris Harris"),
    ("Patricia Martin", "Patty Martin"),
    ("Charles Thompson", "Charlie Thompson"),
    ("Michael Garcia", "Mike Garcia"),
    ("Steven Martinez", "Steve Martinez"),
    ("Barbara Robinson", "Barb Robinson"),
    ("Richard Clark", "Rick Clark"),
    ("Deborah Rodriguez", "Debby Rodriguez"),
    ("Anthony Lewis", "Tony Lewis"),
    ("Daniel Lee", "Dan Lee"),
    ("Joseph Walker", "Joe Walker"),
    ("Susan Hall", "Sue Hall"),
    ("Andrew Allen", "Andy Allen"),
    ("Matthew Young", "Matt Young"),
    ("Alexander King", "Alex King"),
    ("Nicholas Wright", "Nick Wright"),
    ("Benjamin Scott", "Ben Scott"),
    ("Joshua Green", "Josh Green"),
    # similar first names but different last names
    ("Robert Smith", "Bob Johnson"),
    ("Jennifer White", "Jen Brown"),
    ("Michael Garcia", "Mike Hernandez"),
    # entirely different first and last names
    ("Aaron Turner", "Eric Miller"),
    ("Hiroshi Tanaka", "Hiro Tanaka"),
    ("Wei Zhang", "William Zhang"),
    ("Santiago Ramirez", "Santi Ramirez"),
    # examples with middle names or compound surnames
    ("John Paul Jones", "John Jones"),
    ("Gabriel Garcia Marquez", "Gabriel Marquez"),
    ("Maria del Carmen Fernandez", "Maria Fernandez"),
    ("Juan Carlos de la Vega", "Juan de la Vega"),
]

def compute_score(
    name1: str, name2: str, *, ignore_middle: bool = False
) -> tuple[int, int]:
    """Compute the similarity between two names.

    Parameters
    ----------
    name1, name2 : str
        Names to compare.

    Returns
    -------
    tuple[int, int]
        ``(first_score, last_score)`` where each score ranges from ``0`` to ``100``.

    Notes
    -----
    ``first_score`` evaluates the first names and incorporates nickname
    recognition. If the second name is a known nickname of the first (or vice
    versa) it yields ``100``; otherwise it falls back to
    :func:`~rapidfuzz.fuzz.token_set_ratio`.
    ``last_score`` compares the last names with ``token_set_ratio`` when both
    last names are present. If one of the names is missing a last component, the
    score is ``0``.

    The function attempts to handle middle names and multi-part surnames. When a
    name contains exactly two tokens, the second token is treated as the last
    name. For longer names the default behaviour is to treat everything after
    the first token as the last name, allowing for compound surnames. Set
    ``ignore_middle=True`` to mimic the old behaviour of using only the final
    token as the surname.
    """
    # split into tokens for first/last names
    parts1 = name1.strip().split()
    parts2 = name2.strip().split()
    first1 = parts1[0] if parts1 else name1
    first2 = parts2[0] if parts2 else name2

    def _extract_last(parts: list[str]) -> str:
        if len(parts) < 2:
            return ""
        if len(parts) == 2 or ignore_middle:
            return parts[-1]
        return " ".join(parts[1:])

    last1 = _extract_last(parts1)
    last2 = _extract_last(parts2)

    # compute first-name score (with nickname support)
    nick_set_1 = {nick.lower() for nick in (nn.nicknames_of(first1) or [])}
    if first2.lower() in nick_set_1:
        first_score = 100
    else:
        nick_set_2 = {nick.lower() for nick in (nn.nicknames_of(first2) or [])}
        if first1.lower() in nick_set_2:
            first_score = 100
        else:
            first_score = fuzz.token_set_ratio(first1, first2)

    # compute last-name score (straight fuzzy)
    if last1 and last2:
        last_score = fuzz.token_set_ratio(last1, last2)
    else:
        last_score = 0

    # return a tuple of (first_score, last_score)
    return first_score, last_score


def _print_comparison(name1: str, name2: str) -> None:
    """Print comparison results for ``name1`` and ``name2``.

    This replicates the output of the ``compare`` CLI command and is
    reused by the ``samples`` command for each pair of names.
    """
    parts1 = name1.strip().split()
    parts2 = name2.strip().split()
    first1 = parts1[0] if parts1 else name1
    first2 = parts2[0] if parts2 else name2

    def _extract_last(parts: list[str]) -> str:
        if len(parts) < 2:
            return ""
        if len(parts) == 2:
            return parts[-1]
        return " ".join(parts[1:])

    last1 = _extract_last(parts1)
    last2 = _extract_last(parts2)

    first_score, last_score = compute_score(name1, name2)
    print(f"First-name similarity ({first1} vs {first2}): {first_score}")
    print(f"Last-name similarity ({last1} vs {last2}): {last_score}")
    if first_score >= THRESHOLD:
        print("Alias is an acceptable match based on first name.")
    else:
        print("Alias first name too different; manual verification needed.")


def main():
    parser = argparse.ArgumentParser(
        description="Compare two names and output a similarity score (0-100)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare_parser = subparsers.add_parser(
        "compare", help="Compare two full names"
    )
    compare_parser.add_argument("name1", help="First full name in quotes")
    compare_parser.add_argument("name2", help="Second full name in quotes")

    subparsers.add_parser(
        "samples", help="Display scores for a list of sample name pairs"
    )

    args = parser.parse_args()

    if args.command == "compare":
        if len(args.name1.split()) < 2 or len(args.name2.split()) < 2:
            compare_parser.error("Both names must include first and last name.")

        _print_comparison(args.name1, args.name2)
    elif args.command == "samples":
        for name1, name2 in SAMPLES:
            print(f"{name1} vs {name2}")
            _print_comparison(name1, name2)
            print()


if __name__ == "__main__":
    main()

# requirements:
# pip install rapidfuzz nicknames
