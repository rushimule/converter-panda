import fitz  # PyMuPDF
import os

def convert_pdf_to_jpg(pdf_path, converted_folder):
    # Open the PDF file
    pdf_file = fitz.open(pdf_path)

    # Create an output directory for images
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(converted_folder, base_filename)
    os.makedirs(output_folder, exist_ok=True)

    # Convert each page of the PDF to a JPG image
    image_paths = []
    for page_num in range(pdf_file.page_count):
        page = pdf_file.load_page(page_num)
        # Render page to image (pixmap)
        pix = page.get_pixmap()

        # Define the output path for each image
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)  # Save the image as PNG (can also be JPG if needed)
        image_paths.append(image_path)

    # Close the PDF
    pdf_file.close()

    # Return the folder path containing images
    return output_folder
