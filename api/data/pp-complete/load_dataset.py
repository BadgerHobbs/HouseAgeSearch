import csv
import sqlite3

# Delete the database file if it exists
try:
    conn = sqlite3.connect('pp_complete.db')
    conn.execute('DROP TABLE IF EXISTS pp_complete')
    conn.commit()
    conn.close()
except:
    pass

# Connect to database
connection = sqlite3.connect('pp_complete.db')
cursor = connection.cursor()

# Create table if it doesn't exist
cursor.execute(
    "CREATE TABLE IF NOT EXISTS pp_complete (id INTEGER PRIMARY KEY, transfer_uid TEXT, price INTEGER, date TEXT, postcode TEXT, property_type TEXT, is_new TEXT, tenure TEXT, paon TEXT, saon TEXT, street TEXT, locality TEXT, town_city TEXT, district TEXT, county TEXT, ppd_category_type TEXT, record_status TEXT)"
)

# Open csv file
with open('pp-complete.csv', 'r') as csv_file:

    # Create cs reader
    csv_reader = csv.reader(csv_file, delimiter=',')

    # Insert data into database
    for row in csv_reader:
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO pp_complete VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            row
        )

# Commit changes
connection.commit()

# Close connection
connection.close() 