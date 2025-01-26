from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io

# Add text watermark to the PDF
def add_text_watermark(input_pdf_path, output_pdf_path, watermark_text):
    # Create a temporary in-memory PDF with the watermark text
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 36)
    c.drawString(100, 100, watermark_text)  # Change position as needed
    c.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Read the original PDF
    existing_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # Merge the original PDF with the watermark PDF
    page = existing_pdf.pages[0]  # You can choose which page to watermark
    page.merge_page(new_pdf.pages[0])

    output_pdf.add_page(page)

    # Write the watermarked PDF to a file
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

    return output_pdf_path


# Add image watermark to the PDF
def add_image_watermark(input_pdf_path, output_pdf_path, watermark_image_path):
    # Open the image to overlay on the PDF
    watermark_image = Image.open(watermark_image_path)
    packet = io.BytesIO()
    watermark_image.save(packet, format="PDF")
    packet.seek(0)
    watermark_pdf = PdfReader(packet)

    # Read the original PDF
    existing_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # Add watermark to each page of the original PDF
    for page in existing_pdf.pages:
        page.merge_page(watermark_pdf.pages[0])

        output_pdf.add_page(page)

    # Write the watermarked PDF to a file
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

    return output_pdf_path
