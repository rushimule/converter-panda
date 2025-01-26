from PIL import Image
import os

def convert_jpg_to_pdf(input_path, output_folder):
    """
    Convert one or more JPG files to a single PDF.
    input_path: The path to the JPG file(s).
    output_folder: The directory to save the converted PDF file.
    """
    if isinstance(input_path, str):  # Single file case
        input_files = [input_path]
    else:  # Multiple files
        input_files = input_path

    images = []

    # Open the image files
    for file in input_files:
        if file.lower().endswith(('.jpg', '.jpeg')):
            image = Image.open(file)
            image = image.convert("RGB")  # Ensure it's in RGB mode for PDF
            images.append(image)
        else:
            raise ValueError(f"Invalid file format: {file}")

    # Create the PDF file
    output_pdf = os.path.join(output_folder, "output.pdf")
    if len(images) == 1:
        images[0].save(output_pdf, "PDF", resolution=100.0)
    else:
        images[0].save(output_pdf, "PDF", resolution=100.0, save_all=True, append_images=images[1:])

    # Return the path to the PDF file
    return output_pdf
