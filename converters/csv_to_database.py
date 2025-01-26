import pandas as pd
import os
from sqlalchemy import create_engine


def convert_csv_to_database(csv_path, output_folder, table_name):
    """
    Converts a CSV file to a SQLite database, saves it, and returns the database file path.

    Args:
        csv_path (str): Path to the input CSV file.
        output_folder (str): Path to the folder where the database file will be saved.
        table_name (str): Name of the table in the database.

    Returns:
        str: Path to the generated SQLite database file.
    """
        
    # Generate the SQLite database filename
    db_filename = os.path.basename(csv_path).replace('.csv', '.db')
    db_path = os.path.join(output_folder, db_filename)

    # Create a database engine (no schema argument)
    try:
        engine = create_engine(f'sqlite:///{db_path}')
    except Exception as e:
        raise ValueError(f"Error creating database engine: {e}")

    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Save the dataframe to the SQLite database
    try:
        
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except Exception as e:
        raise ValueError(f"Error saving data to the database: {e}")

    return db_path
