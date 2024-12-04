import sqlite3
import pandas as pd
import os
import re
import matplotlib.pyplot as plt 

# Define the database file name
db_filename = 'wow_raids_analysis.db'

# Define the directory containing your CSV files
csv_directory = r"db"

# List of specific CSV files to import. These are files obtained during weekly raids via a tool called WarcraftLogs as well as a Overview file that comes from another tool that audits all of the players.
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

# Create the joined table
cursor.execute(create_joined_table_query)
conn.commit()
print("Joined table 'JoinedDPSLogs' created successfully in the database.")

# Export the joined table to a new CSV file
output_csv = os.path.join(csv_directory, "JoinedDPSLogs.csv")
joined_df = pd.read_sql_query("SELECT * FROM JoinedDPSLogs;", conn)
joined_df.to_csv(output_csv, index=False)

print(f"Joined data exported successfully to '{output_csv}'.")

# SQL Query to extract name, ilvl% by week (cleaned formatting) and Mythic Dungeons Done (as an integer otherwise it wouldn't sort it)
query = """
SELECT
    Name,
    CAST("Ilvl %" AS INTEGER) AS Ilvl_Percent,
    CAST("Ilvl %:1" AS INTEGER) AS Ilvl_Percent_1,
    CAST("Ilvl %:2" AS INTEGER) AS Ilvl_Percent_2,
    CAST("Ilvl %:3" AS INTEGER) AS Ilvl_Percent_3,
    CAST("Ilvl %:4" AS INTEGER) AS Ilvl_Percent_4,
    CAST("Unnamed: 60" AS INTEGER) AS "Mythic Dungeons Done",
    -- Calculate the average of ilvl% values
    (
        CAST("Ilvl %" AS INTEGER) +
        CAST("Ilvl %:1" AS INTEGER) +
        CAST("Ilvl %:2" AS INTEGER) +
        CAST("Ilvl %:3" AS INTEGER) +
        CAST("Ilvl %:4" AS INTEGER)
    ) / 5 AS Average_Ilvl_Percent,
    CAST("Unnamed: 60" AS INTEGER) / (
        (
            CAST("Ilvl %" AS INTEGER) +
            CAST("Ilvl %:1" AS INTEGER) +
            CAST("Ilvl %:2" AS INTEGER) +
            CAST("Ilvl %:3" AS INTEGER) +
            CAST("Ilvl %:4" AS INTEGER)
        ) / 5
    ) AS Mythic_To_Ilvl_Ratio
FROM JoinedDPSLogs
ORDER BY "Mythic Dungeons Done" DESC
"""

# Execute the query and fetch the results into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# Display the result
print(df)

# Export the result to a CSV file
df.to_csv('IlvlParsePerPlayer.csv', index=False)

# Close the database connection
conn.close()

# Bar graph 1: Mythic Dungeons Done by Name
plt.style.use('fivethirtyeight')
plt.figure(figsize=(10, 6))
plt.bar(df['Name'], df['Mythic Dungeons Done'], color='blue')
plt.xlabel('Name')
plt.ylabel('Mythic Dungeons Done')
plt.title('Mythic Dungeons Done by Player')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Bar graph 2: Each Ilvl % value by Name
plt.figure(figsize=(10, 6))
bar_width = 0.15
names = df['Name']
x = range(len(names))

# Create stacked bars for ilvl % values
plt.bar(x, df['Ilvl_Percent'], width=bar_width, label='Ilvl %')
plt.bar([p + bar_width for p in x], df['Ilvl_Percent_1'], width=bar_width, label='Ilvl %:1')
plt.bar([p + 2 * bar_width for p in x], df['Ilvl_Percent_2'], width=bar_width, label='Ilvl %:2')
plt.bar([p + 3 * bar_width for p in x], df['Ilvl_Percent_3'], width=bar_width, label='Ilvl %:3')
plt.bar([p + 4 * bar_width for p in x], df['Ilvl_Percent_4'], width=bar_width, label='Ilvl %:4')

plt.xlabel('Name')
plt.ylabel('Ilvl % Values')
plt.title('Ilvl % by Player')
plt.xticks([p + 2 * bar_width for p in x], names, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()

# Bar graph 3: Mythic to Ilvl Ratio by Name
plt.figure(figsize=(10, 6))
plt.bar(df['Name'], df['Mythic_To_Ilvl_Ratio'], color='green')
plt.xlabel('Name')
plt.ylabel('Mythic Dungeons Done / Average Ilvl %')
plt.title('Mythic to Ilvl Ratio by Player')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()