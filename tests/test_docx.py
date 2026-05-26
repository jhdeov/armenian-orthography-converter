import pathlib
import tempfile
import unittest
import zipfile
from xml.etree import ElementTree

from armenian_orthography_converter.docx import convert_docx


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
TEXT = f"{{{W_NS}}}t"


def make_docx(path, text):
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W_NS}">
  <w:body>
    <w:p><w:r><w:t>{text}</w:t></w:r></w:p>
  </w:body>
</w:document>
'''
    with zipfile.ZipFile(path, "w") as docx:
        docx.writestr("[Content_Types].xml", "")
        docx.writestr("word/document.xml", document)


def read_docx_text(path):
    with zipfile.ZipFile(path, "r") as docx:
        root = ElementTree.fromstring(docx.read("word/document.xml"))
    return "".join(node.text or "" for node in root.iter(TEXT))


class TestDocxConversion(unittest.TestCase):
    def test_convert_docx_text_nodes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = pathlib.Path(temp_dir) / "input.docx"
            output_path = pathlib.Path(temp_dir) / "output.docx"
            make_docx(input_path, "և")

            convert_docx(input_path, output_path, lambda text: text.replace("և", "եւ"))

            self.assertEqual(read_docx_text(output_path), "եւ")


if __name__ == "__main__":
    unittest.main()
