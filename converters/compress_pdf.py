from pypdf import PdfReader, PdfWriter
import os

def convert_compress_pdf(input_pdf_path, output_folder):
    """
    Compresses a PDF by reducing the file size using pypdf.
    
    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_folder (str): Path to the folder where the compressed PDF will be saved.
    
    Returns:
        str: Path to the compressed PDF file.
    """
    # Validate input PDF path
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"Input PDF file not found: {input_pdf_path}")

    # Generate the output PDF filename and path
    output_filename = os.path.basename(input_pdf_path).replace('.pdf', '_compressed.pdf')
    output_pdf_path = os.path.join(output_folder, output_filename)

    try:
        # Create a PdfReader object
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Iterate through all pages and add them to the writer
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Write the compressed PDF to the output file
        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)

    except Exception as e:
        raise ValueError(f"Error during PDF compression: {e}")

    return output_pdf_path
