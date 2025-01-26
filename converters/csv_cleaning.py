import pandas as pd
import os

def clean_csv(input_path, output_folder, remove_duplicates=True, fill_missing=None):
    """
    Cleans a CSV file by removing duplicates and/or handling missing values.

    Args:
    - input_path (str): Path to the input CSV file.
    - output_folder (str): Directory to save the cleaned CSV file.
    - remove_duplicates (bool): Whether to remove duplicate rows.
    - fill_missing (str or dict): Value(s) to fill missing data. If None, rows with missing values are removed.

    Returns:
    - str: Path to the cleaned CSV file.
    """
    # Read the CSV file
    df = pd.read_csv(input_path)

    # Remove duplicate rows if specified
    if remove_duplicates:
        df.drop_duplicates(inplace=True)

    # Handle missing values
    if fill_missing is not None:
        df.fillna(fill_missing, inplace=True)
    else:
        df.dropna(inplace=True)

    # Save the cleaned CSV to the output folder
    filename = os.path.basename(input_path).replace('.csv', '_cleaned.csv')
    output_path = os.path.join(output_folder, filename)
    df.to_csv(output_path, index=False)

    return output_path
