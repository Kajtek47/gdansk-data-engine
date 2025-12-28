import pandas as pd
import plotly.express as px
from src.connection import get_db_connection

def generate_delay_chart():
    vehicle_id = input("Enter vehicle number to check: ")
    start_time = input("Enter timestamp of start time [YYYY-MM-DD HH:MM:SS] (clicking enter = last 24h): ")
    end_time = input("Enter timestamp of end time [YYYY-MM-DD HH:MM:SS] (clicking enter = current time): ")

    if not start_time:
        start_time = 'NOW() - INTERVAL \'24 hours\''
    else:
        start_time = f"'{start_time}"

    if not end_time:
        end_time = 'NOW()'
    else:
        end_time = f"'{end_time}'"

    conn = get_db_connection()

    query = f"""
        SELECT created_at, delay_seconds, line_number
        FROM bus_positions
        WHERE vehicle_id = '{vehicle_id}'
        AND created_at >= {start_time}
        AND created_at <= {end_time}
        ORDER BY created_at ASC;
    """

    print("Downloading data from database")

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("Data for this vehicle not found for specified time")
        return

    print(f"Found {len(df)} points. Generating the plot.")

    fig = px.line(df, x="created_at", y="delay_seconds",
                  title=f'Plot of delay for vehicle {vehicle_id} (Lane {df["line_number"].iloc[0]})',
                  labels={'created_at': 'Time of measurement', 'delay_seconds': 'Delay (in seconds)'},
                  markers=True)    

    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Timetable")

    fig.show()

if __name__ == "__main__":
    generate_delay_chart()