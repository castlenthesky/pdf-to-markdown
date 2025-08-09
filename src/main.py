from src.markdown_conversion import pdf_to_markdown
from src.split_pdf import extract_pdf_pages
from src.tinting import adjust_pdf_contrast


def main(
  article_name: str,
  pdf_path: str,
  start_page: int,
  end_page: int,
  contrast_factor: float = 1.8,
  brightness_factor: float = 1.25,
  gamma_correction: float = 0.9,
  threshold_low: int = 255,
  threshold_high: int = 255,
):
  extract_pdf_pages(pdf_path, start_page, end_page, f"02_split/{article_name}.pdf")
  adjust_pdf_contrast(
    f"02_split/{article_name}.pdf",
    f"03_tinted/{article_name}.pdf",
    contrast_factor,
    brightness_factor,
    gamma_correction,
    threshold_low,
    threshold_high,
  )
  pdf_to_markdown(
    f"03_tinted/{article_name}.pdf",
    f"04_markdown/{article_name}.md",
  )


if __name__ == "__main__":
  main(
    article_name="strategy",
    pdf_path="01_input/strategy/Course Packet - Strategy.pdf",
    start_page=2,
    end_page=4,
  )
