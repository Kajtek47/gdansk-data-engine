import time

from src.connection import get_db_connection
from src.extractor import get_data_from_api
from src.loader import save_data_to_db

def run_pipeline():
    conn = get_db_connection()
    cur = conn.cursor()
    print("Connected to a database")

    try:
        while True:
            data = get_data_from_api()
            save_data_to_db(data, cur)
            conn.commit()
            print("Data saved to a database")
            
            time.sleep(300)

    except KeyboardInterrupt:
        print("Program closing")
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_pipeline()