# Armenian Orthography Converter (Python)

This project converts text between the Soviet orthography and the classical Mashtots orthography of the Armenian language.  All previous JavaScript code has been removed in favour of a pure Python implementation.

## Requirements

- Python 3.8+

## Installation

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then install the package in editable mode:

```bash
pip install -e .
```

## Usage

### Library

```python
from armenian_orthography_converter import converter

text = "Աղբյուրներ"
print(converter.soviet_to_mashtots(text))
```

### Command line

A simple command line interface is provided.  Use `--direction` to select the conversion direction.

To convert from Traditional orthography to Soviet orthography, use the following command.

```bash
aoc --direction to_mashtots sINPUT.txt mOUTPUT.txt
```

To convert from Soviet orthography to Traditional orthography, use the following command.

```bash
aoc --direction to_soviet mINPUT.txt sOUTPUT.txt
```

Word `.docx` files can also be converted directly:

```bash
aoc --direction to_mashtots sINPUT.docx mOUTPUT.docx
aoc --direction to_soviet mINPUT.docx sOUTPUT.docx
```

Options:
- `--direction` – either `to_mashtots` or `to_soviet`.
- `--show-path` – print each intermediate transformation.

## Running the tests

```bash
python -m unittest discover tests
```

## License

This project is distributed under the terms of the GNU GPL v3.
