import csv
import sqlite3

# Delete the database file if it exists
try:
    conn = sqlite3.connect('postcodes.db')
    conn.execute('DROP TABLE IF EXISTS postcodes')
    conn.commit()
    conn.close()
except:
    pass

# Connect to database
connection = sqlite3.connect('postcodes.db')
cursor = connection.cursor()

# Create table if it doesn't exist
cursor.execute(
    "CREATE TABLE IF NOT EXISTS postcodes (id INTEGER PRIMARY KEY, postcode TEXT, in_use TEXT, latitude TEXT, longitude TEXT, easting TEXT, northing TEXT, grid_ref TEXT, county TEXT, district TEXT, ward TEXT, district_code TEXT, ward_code TEXT, country TEXT, county_code TEXT, constituency TEXT, introduced TEXT, terminated TEXT, parish TEXT, national_park TEXT, population TEXT, households TEXT, built_up_area TEXT, built_up_sub_division TEXT, lower_layer_super_output_area TEXT, rural_urban TEXT, region TEXT, altitude TEXT, london_zone TEXT, lsoa_code TEXT, local_authority TEXT, msoa_code TEXT, middle_layer_super_output_area TEXT, parish_code TEXT, census_output_area TEXT, constituency_code TEXT, index_of_multiple_deprivation TEXT, quality TEXT, user_type TEXT, last_updated TEXT, nearest_station TEXT, distance_to_station TEXT, postcode_area TEXT, postcode_district TEXT, police_force TEXT, water_company TEXT, plus_code TEXT, average_income TEXT, sewage_company TEXT, travel_to_work_area TEXT, itl_level_2 TEXT, itl_level_3 TEXT, uprns TEXT, distance_to_sea TEXT)"
    )

# Open csv file
with open('postcodes.csv', 'r') as csv_file:

    # Create cs reader
    csv_reader = csv.reader(csv_file, delimiter=',')

    is_first_row = True

    # Insert data into database
    for row in csv_reader:

        # Skip first row
        if is_first_row:
            is_first_row = False
            continue
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO postcodes VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            row
        )

# Commit changes
connection.commit()

# Close connection
connection.close() 