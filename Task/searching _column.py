import lancedb

# Connect to LanceDB
conn = lancedb.connect("./company_data_db")

# Open the table (for example, `company_embeddings`)
table_embeddings = conn.open_table("company_profiles")
if table_embeddings is None:
    raise ValueError("The table 'company_embeddings' could not be found.")

# Get the schema of the table
schema = table_embeddings.schema

# Print the schema to inspect the columns
print("Schema of company_profiles table:")
for field in schema:
    print(f"Column: {field.name}, Type: {field.type}")
