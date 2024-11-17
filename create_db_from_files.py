import sqlite3
import pandas as pd
import os

# Define the database file name
db_filename = 'wow_raids_analysis.db'

# Define the directory containing your CSV files
csv_directory = r"C:\Users\The Madjutant\Desktop\CodeYou\Projects\Wow-Raid-Mythic-Dungeons-Cross-Analysis\Log files"

# List of specific CSV files to import
csv_files = [
    "Nov 5th DPS Logs.csv",
    "Nov 7th DPS Logs.csv",
    "Oct 24th DPS Logs.csv",
    "Oct 29th DPS Logs.csv",
    "Oct 31st DPS Logs.csv",
    "PLC Raiders - Overview.csv"
]

# Connect to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect(db_filename)

# Loop through each specified CSV file and import it into the SQLite database
for file in csv_files:
    # Construct the full file path
    file_path = os.path.join(csv_directory, file)

    # Extract the table name from the CSV file name (without extension)
    table_name = os.path.splitext(file)[0]

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Import DataFrame into SQLite (replaces existing table if it exists)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    print(f"Imported '{file}' as table '{table_name}'.")

# Close the database connection
conn.close()

print(f"Database '{db_filename}' created successfully with tables from the specified CSV files.")
