import argparse
from . import converter
from .docx import convert_docx


def _convert_text(text, direction, show_path=False):
    if direction == 'to_mashtots':
        return converter.soviet_to_mashtots(text, show_path=show_path)
    return converter.mashtots_to_soviet(text, show_path=show_path)


def _detect_format(input_path, output_path):
    paths = (input_path.lower(), output_path.lower())
    if any(path.endswith('.doc') for path in paths):
        raise ValueError("Only .docx Word files are supported; save .doc files as .docx first.")
    if any(path.endswith('.docx') for path in paths):
        return 'docx'
    return 'text'


def main():
    parser = argparse.ArgumentParser(description="Convert Armenian orthography")
    parser.add_argument('input', help='Input text or .docx file')
    parser.add_argument('output', help='Output text or .docx file')
    parser.add_argument('--direction', choices=['to_mashtots', 'to_soviet'], required=True,
                        help='Conversion direction')
    parser.add_argument('--show-path', action='store_true', help='Show intermediate steps')
    args = parser.parse_args()

    file_format = _detect_format(args.input, args.output)

    if file_format == 'docx':
        convert_docx(
            args.input,
            args.output,
            lambda text: _convert_text(text, args.direction, show_path=args.show_path),
        )
        return

    with open(args.input, encoding='utf-8') as f:
        text = f.read()

    result = _convert_text(text, args.direction, show_path=args.show_path)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(result)


if __name__ == '__main__':
    main()
