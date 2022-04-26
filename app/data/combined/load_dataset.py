import sqlite3
import time

database_name = 'combined.db'

# Delete the database file if it exists
try:
    conn = sqlite3.connect(database_name)
    conn.execute('DROP TABLE IF EXISTS combined')
    conn.commit()
    conn.close()
except:
    pass

# Connect to database
print('Connecting to database...')
connection = sqlite3.connect(database_name)
cursor = connection.cursor()

# Create table if it doesn't exist
print('Creating table...')
cursor.execute(
    "CREATE TABLE IF NOT EXISTS combined (id INTEGER PRIMARY KEY, transfer_uid TEXT, price INTEGER, date TEXT, postcode TEXT, property_type TEXT, is_new TEXT, tenure TEXT, paon TEXT, saon TEXT, street TEXT, locality TEXT, town_city TEXT, district TEXT, county TEXT, ppd_category_type TEXT, record_status TEXT, latitude TEXT, longitude TEXT)"
)

# Connect to postcodes.db
print('Connecting to postcodes.db...')
postcodes_connection = sqlite3.connect('../postcodes/postcodes.db')
postcodes_cursor = postcodes_connection.cursor()

# Get all rows from postcodes.db selecting postcode, latitude and longitude
print('Getting all rows from postcodes.db...')
postcodes_cursor.execute(
    "SELECT postcode, latitude, longitude FROM postcodes"
)
postcodes_rows = postcodes_cursor.fetchall()

# Create a dictionary of postcode to latitude and longitude
print('Creating a dictionary of postcode to latitude and longitude...')
postcode_to_lat_long = {}
for row in postcodes_rows:
    postcode_to_lat_long[row[0]] = [row[1], row[2]]

# Connect to gb_post_codes.db
print('Connecting to gb_post_codes.db...')
gb_post_codes_connection = sqlite3.connect('../gb-post-codes/gb_post_codes.db')
gb_post_codes_cursor = gb_post_codes_connection.cursor()

# Get all rows from gb_post_codes.db selecting postcode, latitude and longitude
print('Getting all rows from gb_post_codes.db...')
gb_post_codes_cursor.execute(
    "SELECT postal_code, latitude, longitude FROM gb_post_codes"
)
gb_post_codes_rows = gb_post_codes_cursor.fetchall()

# Add to postcode_to_lat_long dictionary where postcode is not already in the dictionary
print('Adding to postcode_to_lat_long dictionary where postcode is not already in the dictionary...')
for row in gb_post_codes_rows:
    if row[0] not in postcode_to_lat_long:
        postcode_to_lat_long[row[0]] = [row[1], row[2]]

# Connect to pp_complete.db
print('Connecting to pp_complete.db...')
pp_complete_connection = sqlite3.connect('../pp-complete/pp_complete.db')
pp_complete_cursor = pp_complete_connection.cursor()

# Get all rows from pp_complete.db
print('Getting all rows from pp_complete.db...')
pp_complete_cursor.execute("SELECT * FROM pp_complete")
pp_complete_rows = pp_complete_cursor.fetchall()

# Loop through pp_complete.db rows
for pp_complete_row in pp_complete_rows:

    # Set execution start time
    start_time = time.time()

    # Get postcode from pp_complete.db
    postcode = pp_complete_row[4]

    latitude = None
    longitude = None
    
    # Get latitude and longitude from postcode_to_lat_long dictionary
    if postcode in postcode_to_lat_long:
        latitude = postcode_to_lat_long[postcode][0]
        longitude = postcode_to_lat_long[postcode][1]

    # Combine pp_complete.db row with lat/long
    combined_row = pp_complete_row + (latitude, longitude,)

    # Insert data into database
    cursor.execute(
        "INSERT INTO combined VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        combined_row
        )

    # If is every 10000 rows
    if pp_complete_row[0] % 10000 == 0:

        # Print rows completed out of total rows and percentage completed
        print(f"{pp_complete_row[0]}/{len(pp_complete_rows)} ({(pp_complete_row[0] / len(pp_complete_rows)) * 100:.2f}%)")

# Commit changes
connection.commit()

# Close connection
connection.close()
postcodes_connection.close()
pp_complete_connection.close()

# Print success message
print('Success!')

