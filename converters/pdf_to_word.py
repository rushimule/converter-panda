from pdf2docx import Converter
import os

def convert_pdf_to_word(pdf_path, output_folder):
    """
    Converts a PDF file to Word format and saves it in the specified output folder.
    
    Parameters:
        pdf_path (str): Path to the PDF file to be converted.
        output_folder (str): Path to the folder where the converted file will be saved.
        
    Returns:
        str: Path to the converted Word document.
    """
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate the output Word file path
        word_filename = os.path.basename(pdf_path).replace('.pdf', '.docx')
        word_path = os.path.join(output_folder, word_filename)

        # Convert PDF to Word
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)
        cv.close()

        return word_path

    except Exception as e:
        # Log the error and re-raise it for further handling
        raise ValueError(f"Failed to convert PDF to Word: {e}")
