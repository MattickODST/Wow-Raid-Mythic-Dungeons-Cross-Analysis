import sqlite3
import pandas as pd
import os
import re

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

# Function to sanitize table names (replace spaces, dashes, and special characters) 
# Apparently the "-" in one of the file names didn't want to play nicely but it's part of the export from a WoW auditing software so I wanted to keep it
def sanitize_table_name(filename):
    table_name = os.path.splitext(filename)[0]
    table_name = re.sub(r'[^A-Za-z0-9_]', '_', table_name)  # Replace non-alphanumeric characters with underscores
    return table_name

# Connect to the SQLite database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Import each CSV file into the SQLite database as a sanitized table
table_names = []
for file in csv_files:
    file_path = os.path.join(csv_directory, file)
    table_name = sanitize_table_name(file)
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    table_names.append(table_name)
    print(f"Imported '{file}' as table '{table_name}'.")

# SQL query to join all tables on "Name" using the sanitized table names
create_joined_table_query = f"""
    CREATE TABLE IF NOT EXISTS JoinedDPSLogs AS
    SELECT *
    FROM {table_names[0]}
    JOIN {table_names[1]} ON {table_names[0]}."Name" = {table_names[1]}."Name"
    JOIN {table_names[2]} ON {table_names[0]}."Name" = {table_names[2]}."Name"
    JOIN {table_names[3]} ON {table_names[0]}."Name" = {table_names[3]}."Name"
    JOIN {table_names[4]} ON {table_names[0]}."Name" = {table_names[4]}."Name"
    JOIN {table_names[5]} ON {table_names[0]}."Name" = {table_names[5]}."Name";
"""

# Execute the query to create the joined table
cursor.execute(create_joined_table_query)
conn.commit()
print("Joined table 'JoinedDPSLogs' created successfully in the database.")

# Export the joined table to a new CSV file
output_csv = os.path.join(csv_directory, "JoinedDPSLogs.csv")
joined_df = pd.read_sql_query("SELECT * FROM JoinedDPSLogs;", conn)
joined_df.to_csv(output_csv, index=False)

print(f"Joined data exported successfully to '{output_csv}'.")

# Define the SQL query (example: total damage per player)
query = """
SELECT Name,i lvl%, i lvl%1, i lvl%2, i lvl%3, i lvl%4
FROM JoinedDPSLogs
GROUP BY Name
ORDER BY iLvl DESC;
"""

# Execute the query and fetch the results into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# Display the result
print(df)

# Export the result to a CSV file
df.to_csv('total_damage_per_player.csv', index=False)

# Close the database connection
conn.close()
