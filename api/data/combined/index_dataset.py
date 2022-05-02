import sqlite3

database_name = 'combined.db'

# Connect to database
print('Connecting to database...')
connection = sqlite3.connect(database_name)
cursor = connection.cursor()

columns_to_index = [    
    "price", 
    "date",
    "is_new",
    "postcode",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status",
    "latitude",
    "longitude",
]

# Delete existing indexes
print('Deleting existing indexes...')
for column in columns_to_index:
    cursor.execute("DROP INDEX IF EXISTS idx_{0}".format(column))

# Create index for each column
for column in columns_to_index:
    print('Creating index for column: {}...'.format(column))
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_{} ON combined ({})".format(
            column,
            column
        )
    )

# Commit changes
connection.commit()

# Close connection
connection.close()