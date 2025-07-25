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

The main entry point is `name_similarity.py`. Use the `compare` command with
both names quoted to ensure each is parsed correctly:

```bash
python name_similarity.py compare "John Smith" "Johnny Smith"
```

For a quick demonstration of how the scoring works, run the `samples`
command to print scores for a collection of common name pairs:

```bash
python name_similarity.py samples
```

The command prints information for each pair similar to running
`compare` on that pair individually. A short excerpt:

```text
Robert Smith vs Bob Smith
First-name similarity (Robert vs Bob): 100
Last-name similarity (Smith vs Smith): 100
Alias is an acceptable match based on first name.

If either argument omits a first or last name, the command exits with an
error message.

The script prints similarity scores for the first and last names and indicates
whether the alias name meets the default acceptance threshold.

## Testing

Execute the test suite with `pytest`:

```bash
pytest
```

This runs a few unit tests located in the `tests/` directory to verify the
scoring logic.
