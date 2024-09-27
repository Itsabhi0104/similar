import lancedb

# Open the LanceDB connection and table (replace the path with your LanceDB path)
conn = lancedb.connect("financial_data_db")
table = conn.open_table("breakouts")

# Sample data to append (insert)
new_data = [
    {"symbol": "app", "date": "2024-11-16", "hour": 30,"price":30.12},
    {"symbol": "abh", "date": "2024-10-16", "hour": 40,"price":40.12}]
predicate = "symbol = 'app' Or symbol='abh'"


# 1. Append new data to the table
table.delete(predicate)
print("Data deleted to the table successfully.")

# Note: You cannot directly delete or update rows in append mode.
