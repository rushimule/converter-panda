import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

def convert_csv_to_pdf(csv_path, output_folder):
    """
    Converts a CSV file to a PDF table format and saves it.
    
    Parameters:
    - csv_path (str): Path to the input CSV file.
    - output_folder (str): Path to the folder where the PDF file will be saved.

    Returns:
    - str: Path to the saved PDF file.
    """

    # Check if the CSV file exists
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Ensure the output folder exists
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    # Generate the output PDF filename
    pdf_filename = os.path.basename(csv_path).replace('.csv', '.pdf')
    pdf_path = os.path.join(output_folder, pdf_filename)

    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file '{csv_path}': {e}")

    # Convert DataFrame to a list of lists (for Table input)
    data = [df.columns.tolist()] + df.values.tolist()

    # Create the PDF file
    try:
        pdf = SimpleDocTemplate(pdf_path)
        table = Table(data)

        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        # Build the PDF
        pdf.build([table])
    except Exception as e:
        raise ValueError(f"Error creating PDF file '{pdf_path}': {e}")

    print(f"Conversion successful! PDF file saved at: {pdf_path}")
    return pdf_path
