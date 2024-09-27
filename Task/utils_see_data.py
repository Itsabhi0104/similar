import lancedb
import pandas as pd

def connect_db():
    return lancedb.connect("./company_data_db")

def query_breakouts_table(db):
    table = db.open_table("company_profiles")
    df = table.to_pandas()
    return df

def main():
    db = connect_db()
    breakouts_data = query_breakouts_table(db)
    print("\nBreakouts Table Data:")
    print(breakouts_data)

if __name__ == "__main__":
    main()