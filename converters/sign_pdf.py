from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def sign_pdf(input_pdf_path, output_pdf_path, signature_text):
    # Create a temporary in-memory PDF with the signature text
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.drawString(100, 100, signature_text)  # You can change the position here
    c.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Read the original PDF
    existing_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # Merge the original PDF with the signature PDF
    page = existing_pdf.pages[0]  # Select the page to sign (change if you need to sign multiple pages)
    page.merge_page(new_pdf.pages[0])

    output_pdf.add_page(page)

    # Write the signed PDF to a file
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)
    
    return output_pdf_path
