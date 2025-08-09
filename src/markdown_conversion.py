import os
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


def pdf_to_markdown(
    input_file_path: str, output_file_path: str, link_images: bool = False
) -> None:
    """
    Convert a PDF file to Markdown using Docling OCR with image extraction.

    Args:
        input_file_path: Path to the input PDF file
        output_file_path: Path to save the output Markdown file
        link_images: If True, replace image placeholders with markdown links; if False, keep placeholders
    """
    # Create images directory relative to output file
    output_path = Path(output_file_path)
    images_dir = output_path.parent / "images"
    images_dir.mkdir(exist_ok=True)

    # Configure pipeline to extract images
    pipeline_options = PdfPipelineOptions(generate_picture_images=True, images_scale=2)

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(input_file_path)
    doc = result.document

    # Save images to the images directory
    for i, picture in enumerate(doc.pictures):
        if picture.image:
            image_filename = f"{output_path.stem}_image_{i + 1}.png"
            image_path = images_dir / image_filename
            picture.image.pil_image.save(image_path)

    # Export to markdown
    markdown_content = doc.export_to_markdown()

    # Optionally replace image placeholders with references to saved images
    if link_images:
        image_count = 0
        for i, picture in enumerate(doc.pictures):
            if picture.image:
                image_count += 1
                image_filename = f"{output_path.stem}_image_{image_count}.png"
                replacement = f"![Image](images/{image_filename})"

                # Replace the specific <!-- image --> placeholder that Docling uses
                markdown_content = markdown_content.replace(
                    "<!-- image -->", replacement, 1
                )

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)


if __name__ == "__main__":
    for file in os.listdir("03_tinted/strategy"):
        if file.endswith(".pdf"):
            print(f"Converting {file} to Markdown...")
            input_file = f"03_tinted/strategy/{file}"
            output_file = f"04_markdown/strategy/{file.replace('.pdf', '.md')}"
            pdf_to_markdown(input_file, output_file)
            print(f"SUCCESS: {file} to Markdown...")
