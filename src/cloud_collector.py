import requests
import psycopg2
from psycopg2 import extras
import os
import datetime

def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        sslmode='require'
    )

def fetch_and_save():
    print("Data download started")

    url = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/tristar_gps.json"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        last_update = data['lastUpdateData']
        vehicles = data['vehicles']
    except Exception as e:
        print(f"API error: {e}")
        return

    data_to_insert = []
    current_time = datetime.datetime.now()
    
    for v in vehicles:
        if v.get('lat') and v.get('lon'):
            data_to_insert.append((
                v.get('vehicleId'),
                v.get('routeShortName'),
                v.get('lat'),
                v.get('lon'),
                v.get('delay', 0),
                current_time
            ))

    if not data_to_insert:
        print("No data to save")
        return

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO bus_positions 
            (vehicle_id, line_number, latitude, longitude, delay_seconds, created_at) 
            VALUES %s
        """
        
        extras.execute_values(cur, query, data_to_insert)
        conn.commit()
        print(f"Saved {len(data_to_insert)} records to Neon database")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    fetch_and_save()