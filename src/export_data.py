import pandas as pd
from archive.connection import get_db_connection

def export_data_to_parquet():
    print("Data export started")
    conn = get_db_connection()

    query = """SELECT * FROM bus_positions ORDER BY created_at ASC"""

    print("Downloading data from database")

    df = pd.read_sql(query, conn)
    conn.close()

    print(f"Downloaded {len(df)} rows")

    output_file = 'data/gdansk_traffic_history.parquet'
    df.to_parquet(output_file, index=False)
    print(f"Data exported to {output_file}")

if __name__ == "__main__":
    export_data_to_parquet()