import lancedb
import csv

# Initialize LanceDB connection
db = lancedb.connect('financial_data_db')  # Specify your database path

# Open the collection/table you want to back up
collection = db.open_table('breakouts')  # Adjust the collection name accordingly

# Fetch all data from the collection (modify as per actual API of LanceDB)
data = collection.to_arrow()  # Use the correct method to retrieve data as per LanceDB documentation

# Convert data to a list of dictionaries or rows if needed
data_list = data.to_pandas().to_dict(orient='records')  # Convert Arrow table to list of dictionaries

# Write data to CSV file
csv_file = 'backup_data.csv'
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys())  # Use dict keys as CSV headers
    writer.writeheader()
    writer.writerows(data_list)

print(f"Data successfully backed up to {csv_file}.")
