import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from io import BytesIO
import logging


def pdf_to_markdown_without_poppler(pdf_path, markdown_path, dpi=300):
    """
    Converts a rasterized PDF into a Markdown file with extracted text using PyMuPDF.

    Args:
        pdf_path (str): Path to the input PDF file.
        markdown_path (str): Path to the output Markdown file.
        dpi (int): DPI for rendering the PDF pages. Adjust for better OCR quality.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        with fitz.open(pdf_path) as doc:
            extracted_text = []

            for page_number in range(len(doc)):
                logger.info(f"Processing page {page_number + 1}/{len(doc)}")
                
                # Render page to image
                pix = doc.load_page(page_number).get_pixmap(dpi=dpi)
                image = Image.open(BytesIO(pix.tobytes("png")))
                
                # Extract text via OCR
                text = pytesseract.image_to_string(image, lang="eng", config="--dpi 300")
                extracted_text.append(text)

        # Write the extracted text to a Markdown file
        with open(markdown_path, "w", encoding="utf-8") as md_file:
            md_file.write("# Extracted Text\n\n")
            md_file.write(f"Source: {pdf_path}\n\n")

            for page_number, page_text in enumerate(extracted_text, start=1):
                md_file.write(f"## Page {page_number}\n\n")
                md_file.write(page_text + "\n\n")

        logger.info(f"Text extracted and saved to {markdown_path}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from a rasterized PDF and save to a Markdown file.")
    parser.add_argument("pdf_path", type=str, help="Path to the input PDF file.")
    parser.add_argument("markdown_path", type=str, help="Path to the output Markdown file.")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for rendering the PDF pages (default: 300).")
    args = parser.parse_args()

    pdf_to_markdown_without_poppler(args.pdf_path, args.markdown_path, args.dpi)
