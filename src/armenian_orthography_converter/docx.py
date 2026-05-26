import posixpath
import zipfile
from xml.etree import ElementTree


WORD_TEXT = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"


def _is_word_xml(filename):
    if not filename.startswith("word/") or not filename.endswith(".xml"):
        return False

    basename = posixpath.basename(filename)
    return (
        filename == "word/document.xml"
        or basename.startswith("header")
        or basename.startswith("footer")
        or basename in {"footnotes.xml", "endnotes.xml", "comments.xml"}
    )


def _convert_xml(data, convert):
    root = ElementTree.fromstring(data)
    changed = False

    for text_node in root.iter(WORD_TEXT):
        if text_node.text:
            converted = convert(text_node.text)
            if converted != text_node.text:
                text_node.text = converted
                changed = True

    if not changed:
        return data

    return ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)


def convert_docx(input_path, output_path, convert):
    with zipfile.ZipFile(input_path, "r") as source:
        with zipfile.ZipFile(output_path, "w") as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if _is_word_xml(item.filename):
                    data = _convert_xml(data, convert)
                target.writestr(item, data)
