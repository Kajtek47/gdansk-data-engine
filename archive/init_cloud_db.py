import os
from archive.connection import get_db_connection

def init_db():
    print("Connecting to a database in cloud")
    conn = get_db_connection()
    cur = conn.cursor()
    
    sql_file_path = 'sql/create_table.sql'
    
    try:
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
            
        print("SQL script started")
        cur.execute(sql_script)
        conn.commit()
        
        print("Table created in cloud")
        
    except FileNotFoundError:
        print(f"File not found: {sql_file_path}")
    except Exception as e:
        print(f"Database error {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_db()