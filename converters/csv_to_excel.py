import pandas as pd
import os

def convert_csv_to_excel(csv_path, output_folder):
    """
    Converts a CSV file to Excel format using pandas and saves it.
    """
    
    # Generate the output Excel filename
    excel_filename = os.path.basename(csv_path).replace('.csv', '.xlsx')
    excel_path = os.path.join(output_folder, excel_filename)

    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Save the dataframe as an Excel file
    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')  # Ensures Excel-compatible format
    except Exception as e:
        raise ValueError(f"Error saving Excel file: {e}")

    return excel_path
