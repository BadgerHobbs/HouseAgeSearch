import csv
import sqlite3

# Delete the database file if it exists
try:
    conn = sqlite3.connect('gb_post_codes.db')
    conn.execute('DROP TABLE IF EXISTS gb_post_codes')
    conn.commit()
    conn.close()
except:
    pass

# Connect to database
connection = sqlite3.connect('gb_post_codes.db')
cursor = connection.cursor()

# Create table if it doesn't exist
cursor.execute(
    "CREATE TABLE IF NOT EXISTS gb_post_codes (id INTEGER PRIMARY KEY, country_code TEXT, postal_code TEXT, place_name TEXT, admin_name1 TEXT, admin_code1 TEXT, admin_name2 TEXT, admin_code2 TEXT, admin_name3 TEXT, admin_code3 TEXT, latitude TEXT, longitude TEXT, accuracy TEXT)"
)

# Open csv file
with open('gb-post-codes.csv', 'r') as csv_file:

    # Create cs reader
    csv_reader = csv.reader(csv_file, delimiter='\t')

    is_first_row = True

    # Insert data into database
    for row in csv_reader:

        # Skip first row
        if is_first_row:
            is_first_row = False
            continue
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO gb_post_codes VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            row
        )

# Commit changes
connection.commit()

# Close connection
connection.close() 