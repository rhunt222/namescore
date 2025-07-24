# NameScore

`NameScore` provides a simple Python script for measuring the similarity
between two personal names. It leverages the
[rapidfuzz](https://github.com/maxbachmann/RapidFuzz) library for fuzzy string
matching and the [nicknames](https://pypi.org/project/nicknames/) package to
recognize common nicknames. The project also includes a small test suite using
`pytest`.

## Installation

Install the required dependencies:

```bash
pip install rapidfuzz nicknames
```

For running the tests you will also need `pytest`:

```bash
pip install pytest
```

## Usage

The main entry point is `name_similarity.py`. Run it from the command line with
two names to compare:

```bash
python name_similarity.py "John Smith" "Johnny Smith"
```

The script prints similarity scores for the first and last names and indicates
whether the alias name meets the default acceptance threshold.

## Testing

Execute the test suite with `pytest`:

```bash
pytest
```

This runs a few unit tests located in the `tests/` directory to verify the
scoring logic.
