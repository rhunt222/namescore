#!/usr/bin/env python3
"""
name_similarity.py

Compare two names for similarity, using RapidFuzz for fuzzy matching and NickNamer for nickname handling.
"""
import argparse
from rapidfuzz import fuzz
from nicknames import NickNamer

# initialize NickNamer
nn = NickNamer()

# default threshold for acceptable alias match
THRESHOLD = 80

def compute_score(name1: str, name2: str) -> tuple[int, int]:
    """
    Return a similarity score (0-100) between name1 and name2.
    If name2 is a known nickname of name1 or vice versa, return 100.
    Otherwise use RapidFuzz token_set_ratio.
    """
    # split into tokens for first/last names
    parts1 = name1.strip().split()
    parts2 = name2.strip().split()
    first1 = parts1[0] if parts1 else name1
    first2 = parts2[0] if parts2 else name2
    last1 = parts1[-1] if len(parts1) > 1 else ""
    last2 = parts2[-1] if len(parts2) > 1 else ""

    # compute first-name score (with nickname support)
    nick_set_1 = {nick.lower() for nick in nn.nicknames_of(first1)}
    if first2.lower() in nick_set_1:
        first_score = 100
    else:
        nick_set_2 = {nick.lower() for nick in nn.nicknames_of(first2)}
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


def main():
    parser = argparse.ArgumentParser(
        description="Compare two names and output a similarity score (0-100)"
    )
    parser.add_argument(
        "name1", help="Name as provided by the identity provider"
    )
    parser.add_argument(
        "name2", help="Alias name to compare"
    )
    args = parser.parse_args()

    parts1 = args.name1.strip().split()
    parts2 = args.name2.strip().split()
    first1 = parts1[0] if parts1 else args.name1
    first2 = parts2[0] if parts2 else args.name2
    last1 = parts1[-1] if len(parts1) > 1 else ""
    last2 = parts2[-1] if len(parts2) > 1 else ""

    first_score, last_score = compute_score(args.name1, args.name2)
    print(f"First-name similarity ({first1} vs {first2}): {first_score}")
    print(f"Last-name similarity ({last1} vs {last2}): {last_score}")

    if first_score >= THRESHOLD:
        print("Alias is an acceptable match based on first name.")
    else:
        print("Alias first name too different; manual verification needed.")


if __name__ == "__main__":
    main()

# requirements:
# pip install rapidfuzz nicknames