import pandas as pd
from fpdf import FPDF
import openpyxl

def convert_excel_to_pdf(excel_file, output_folder):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file)
    
    # Create a PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the PDF
    pdf.set_font('Arial', size=10)

    # Create a list of column widths (start with 40 for each column)
    column_widths = [40] * len(df.columns)

    # Measure the maximum width needed for each column
    for col_num, col_name in enumerate(df.columns):
        # Set a temporary PDF cell to calculate the width based on the column data
        max_width = pdf.get_string_width(str(col_name))  # Get the width of the header
        for row in df[col_name]:
            # Get the width of the content in the column
            max_width = max(max_width, pdf.get_string_width(str(row)))
        
        # Set the column width dynamically based on the content
        column_widths[col_num] = max_width + 4  # Add a small padding to avoid text clipping

    # Add headers to PDF
    for col_num, col_name in enumerate(df.columns):
        pdf.cell(column_widths[col_num], 10, txt=str(col_name), border=1, align='C')
    pdf.ln()  # Line break after headers

    # Add rows of data to PDF
    for i, row in df.iterrows():
        for col_num, cell in enumerate(row):
            pdf.cell(column_widths[col_num], 10, txt=str(cell), border=1, align='C')
        pdf.ln()  # Line break after each row

    # Save the PDF
    output_path = f"{output_folder}/output.pdf"
    pdf.output(output_path)

    return output_path 