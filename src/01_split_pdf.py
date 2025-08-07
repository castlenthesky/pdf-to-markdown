import fitz  # PyMuPDF


def extract_pdf_pages(
    file_path: str, start_page: int, end_page: int, output_filename: str
) -> None:
    """
    Extract pages from a PDF and save them to a new file.

    Args:
        file_path: Path to the input PDF file
        start_page: Starting page number (1-based indexing)
        end_page: Ending page number (inclusive)
        output_filename: Name of the output PDF file
    """
    # Open the PDF document
    doc = fitz.open(file_path)

    # Create a new PDF document for the extracted pages
    new_doc = fitz.open()

    # Convert to 0-based indexing
    start_idx = start_page - 1
    end_idx = end_page - 1

    # Extract pages and add them to the new document
    for page_num in range(start_idx, end_idx + 1):
        if page_num < len(doc):
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    # Save the new PDF
    new_doc.save(output_filename)

    # Close both documents
    new_doc.close()
    doc.close()


if __name__ == "__main__":
    # Test the function
    # You can modify these values for testing
    test_input_file = "01_input/strategy/Course Packet - Strategy.pdf"  # Adjust path as needed  # Adjust path as needed
    test_start_page = 102
    test_end_page = 116
    test_output_file = "02_split/strategy/07_netflix.pdf"

    try:
        extract_pdf_pages(
            test_input_file, test_start_page, test_end_page, test_output_file
        )
        print(
            f"Successfully extracted pages {test_start_page}-{test_end_page} from {test_input_file}"
        )
        print(f"Output saved to: {test_output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{test_input_file}' not found.")
        print("Please ensure the file exists and the path is correct.")
    except Exception as e:
        print(f"Error occurred: {e}")
