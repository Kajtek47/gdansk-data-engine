import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from src.connection import get_db_connection
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

def generate_delay_chart():
    vehicle_id = input("Enter vehicle number to check: ")
    start_input = input("Enter timestamp of start time [YYYY-MM-DD HH:MM:SS] (clicking enter = last 24h): ")
    end_input = input("Enter timestamp of end time [YYYY-MM-DD HH:MM:SS] (clicking enter = current time): ")

    now = datetime.now()

    if not end_input:
        end_time = now
    else:
        end_time = end_input

    if not start_input:
        if isinstance(end_time, str):
            end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_time = end_dt - timedelta(hours=24)
        else:
            start_time = end_time - timedelta(hours=24)
    else:
        start_time = start_input

    conn = get_db_connection()

    query = """
        SELECT created_at, delay_seconds, line_number
        FROM bus_positions
        WHERE vehicle_id = %s
        AND created_at >= %s
        AND created_at <= %s
        ORDER BY created_at ASC;
    """

    print("Downloading data from database")

    try:
        df = pd.read_sql(query, conn, params=(vehicle_id, start_time, end_time))
    except Exception as e:
        print(f"SQL uery error {e}")
        conn.close()
        return

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