import os

import fitz  # pymupdf


class PdfExtractor:

    @staticmethod
    def _get_unique_path(path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    @staticmethod
    def extract_text(input_path, output_path="output/extracted.txt", pages=None):
        """
        Extract text from a PDF file.

        Args:
            input_path: Path to the PDF file.
            output_path: Where to save the extracted text.
            pages: Optional page range, e.g. (0, 5) for first 5 pages.
                   Page numbers are 0-indexed.
        """
        doc = fitz.open(input_path)
        text_parts = []

        start = pages[0] if pages else 0
        end = pages[1] if pages else len(doc)

        for i in range(start, min(end, len(doc))):
            page = doc[i]
            text_parts.append(page.get_text())

        doc.close()
        full_text = "\n".join(text_parts)

        output_path = PdfExtractor._get_unique_path(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Extracted text from {end - start} page(s) to '{output_path}'")
        return full_text

    @staticmethod
    def extract_metadata(input_path):
        """Extract and return PDF metadata as a dict."""
        doc = fitz.open(input_path)
        metadata = doc.metadata
        doc.close()
        print(f"Metadata for '{input_path}': {metadata}")
        return metadata
