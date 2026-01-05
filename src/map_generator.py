import folium
import pandas as pd
from archive.connection import get_db_connection

def generate_traffic_map():
    print("Downloading data for map creation...")
    conn = get_db_connection()

    query = """
        SELECT latitude, longitude, delay_seconds, line_number, vehicle_id
        FROM bus_positions
        WHERE created_at > NOW() - INTERVAL '24 hours'
        ORDER BY created_at DESC
        LIMIT 5000
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("No data to display")
        return
    
    map_center = [54.3520, 18.6466]
    m = folium.Map(location=map_center, zoom_start=12)

    unique_lines = sorted(df['line_number'].unique())

    print(f"Drawing {len(unique_lines)} lanes. Creating layers...")

    all_vehicles_layer = folium.FeatureGroup(name="ALL LINES", show=False)

    for line in unique_lines:
        line_layer = folium.FeatureGroup(name=f"Lane {line}", show=False)

        line_data = df[df['line_number'] == line]

        for index, row in line_data.iterrows():
            delay = row['delay_seconds']

            if delay < 120:
                color = 'green'
            elif 120 <= delay < 300:
                color = 'orange'
            else:
                color = 'red'

            popup_content = f"Lane: {row['line_number']}<br>Vehicle: {row['vehicle_id']}<br>Delay: {delay}s"

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=popup_content
            ).add_to(line_layer)

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=popup_content
            ).add_to(all_vehicles_layer)

        line_layer.add_to(m)
    
    all_vehicles_layer.add_to(m)
    
    folium.LayerControl(collapsed=False).add_to(m)

    output_file = "bottlenecks_map.html"
    m.save(output_file)
    print(f"Map created! Saved to {output_file}")

if __name__ == "__main__":
    generate_traffic_map()