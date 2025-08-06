import io
import os

import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageEnhance


def enhance_pdf_contrast(
    input_path,
    output_path,
    contrast_factor=2.0,
    brightness_factor=1.1,
    gamma_correction=0.8,
    threshold_low=50,
    threshold_high=200,
):
    """
    Enhance PDF contrast to remove light grey watermarks and improve readability.

    Args:
        input_path (str): Path to input PDF file
        output_path (str): Path to save enhanced PDF file
        contrast_factor (float): Contrast enhancement factor (1.0 = no change, >1.0 = more contrast)
            - If text appears washed out or faded, increase this value (try 2.0-3.0)
            - If image becomes too harsh or artifacts appear, decrease this value (try 1.5-1.8)
        brightness_factor (float): Brightness adjustment factor (1.0 = no change)
            - If image is too dark after contrast enhancement, increase this value (try 1.2-1.5)
            - If image becomes too bright and details are lost, decrease this value (try 0.8-0.9)
        gamma_correction (float): Gamma correction value (<1.0 = darker, >1.0 = lighter)
            - If watermarks are still visible, decrease this value to darken mid-tones (try 0.6-0.8)
            - If text becomes too dark and loses readability, increase this value (try 0.9-1.2)
        threshold_low (int): Lower threshold for removing light elements (0-255)
            - If watermarks are not being removed, decrease this value (try 30-40)
            - If important light text is being removed, increase this value (try 60-80)
        threshold_high (int): Upper threshold for preserving dark elements (0-255)
            - If watermarks with medium grey are not removed, increase this value (try 220-240)
            - If darker text is being affected, decrease this value (try 150-180)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open the PDF
        pdf_document = fitz.open(input_path)
        new_pdf = fitz.open()

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]

            # Get page as image
            mat = fitz.Matrix(2, 2)  # Higher resolution
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")

            # Convert to PIL Image
            image = Image.open(io.BytesIO(img_data))

            # Convert to RGB if not already
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Apply enhancements
            enhanced_image = _enhance_image(
                image,
                contrast_factor,
                brightness_factor,
                gamma_correction,
                threshold_low,
                threshold_high,
            )

            # Convert back to bytes
            img_buffer = io.BytesIO()
            enhanced_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Create new page with enhanced image
            new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_buffer.getvalue())

        # Save the enhanced PDF
        new_pdf.save(output_path)
        new_pdf.close()
        pdf_document.close()

        return True

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return False


def _enhance_image(
    image,
    contrast_factor,
    brightness_factor,
    gamma_correction,
    threshold_low,
    threshold_high,
):
    """
    Apply image enhancements to remove watermarks and improve contrast.
    """
    # Convert to numpy array for advanced processing
    img_array = np.array(image)

    # Apply gamma correction
    img_array = np.power(img_array / 255.0, gamma_correction) * 255.0
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)

    # Convert back to PIL for further processing
    image = Image.fromarray(img_array)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    # Convert to grayscale to identify light watermark areas
    gray_image = image.convert("L")
    gray_array = np.array(gray_image)

    # Create mask for watermark removal
    # Light areas (watermarks) will be set to white
    mask = (gray_array > threshold_low) & (gray_array < threshold_high)

    # Convert back to RGB array
    rgb_array = np.array(image)

    # Apply watermark removal - set light areas to white
    rgb_array[mask] = [255, 255, 255]

    # Apply additional contrast enhancement to the result
    result_image = Image.fromarray(rgb_array)

    # Final sharpening for better text clarity
    enhancer = ImageEnhance.Sharpness(result_image)
    result_image = enhancer.enhance(1.2)

    return result_image


def batch_enhance_pdfs(input_directory, output_directory, **kwargs):
    """
    Batch process multiple PDF files in a directory.

    Args:
        input_directory (str): Directory containing input PDF files
        output_directory (str): Directory to save enhanced PDF files
        **kwargs: Additional parameters to pass to enhance_pdf_contrast

    Returns:
        dict: Results of processing each file
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    results = {}

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f"enhanced_{filename}")

            print(f"Processing {filename}...")
            success = enhance_pdf_contrast(input_path, output_path, **kwargs)
            results[filename] = success

            if success:
                print(f" Successfully enhanced {filename}")
            else:
                print(f" Failed to enhance {filename}")

    return results


if __name__ == "__main__":
    for file in os.listdir("02_split"):
        if file.endswith(".pdf"):
            input_file = f"02_split/{file}"
            output_file = f"03_tinted/{file}"

            success = enhance_pdf_contrast(
                input_file,
                output_file,
                contrast_factor=1.8,  # higher = more contrast
                brightness_factor=1.25,  # higher = brighter
                gamma_correction=0.9,  # lower = darkened midtones
                threshold_low=255,  # lower = more light areas removed
                threshold_high=255,  # higher = more dark areas preserved
            )

            if success:
                print(f"PDF enhancement completed successfully for {file}!")
            else:
                print(f"PDF enhancement failed for {file}.")
