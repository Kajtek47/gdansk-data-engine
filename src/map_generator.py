import folium
import pandas as pd
from src.connection import get_db_connection

def generate_traffic_map():
    print("Downloading data for map creation")
    conn = get_db_connection()

    query = """
        SELECT latitude, longitude, delay_seconds, line_number, vehicle_id
        FROM bus_positions
        WHERE created_at > NOW() - INTERVAL '24 hours'
        ORDER BY created_at DESC
        LIMIT 1000
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("No data to display")
        return
    
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    print(f"Drawing {len(df)} points on the map")

    for index, row in df.iterrows():
        delay = row['delay_seconds']

        if delay < 120:
            color = 'green'
        elif 120 <= delay < 300:
            color = 'orange'
        else:
            color = 'red'

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Lane: {row['line_number']}<br>Vehicle: {row['vehicle_id']}<br>Delay: {delay}s"
        ).add_to(m)

    output_file = "bottlenecks_map.html"
    m.save(output_file)
    print("Map created")

if __name__ == "__main__":
    generate_traffic_map()