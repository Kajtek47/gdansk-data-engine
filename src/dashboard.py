import streamlit as st
import pandas as pd
from src.connection import get_db_connection
import plotly_express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.set_page_config(
    page_title="Gdańsk Traffic Dashboard",
    page_icon="🚌",
    layout="wide"
)

st.title("Gdańsk Data Engine: Real-Time Traffic Monitor")

@st.cache_data(ttl=120)

def load_data():
    conn = get_db_connection()

    query = """
        SELECT 
            vehicle_id,
            line_number,
            latitude,
            longitude,
            delay_seconds,
            created_at
        FROM bus_positions
        WHERE created_at > NOW() - INTERVAL '24 hours'
        ORDER BY created_at DESC    
    """

    try:
        df = pd.read_sql(query, conn)
        df['created_at'] = pd.to_datetime(df['created_at'])
        return df
    except Exception as e:
        st.error(f"Connection error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

selected_line = 199

data_load_state = st.text("Downloading data...")
df = load_data()
data_load_state.text(f"Data downloaded! Number of records: {len(df)}")

# refresh button
if st.sidebar.button("Refresh page"):
    st.cache_data.clear()
    st.rerun()

# choosing line
st.sidebar.header("Line number")
all_lines = sorted(df['line_number'].unique())
line_options = ["All lines"] + list(all_lines)
selected_line = st.sidebar.selectbox("Choose a line number", line_options)

if selected_line != "All lines":
    df_display = df[df["line_number"] == selected_line]
else:
    df_display = df

# choosing vehicle
st.sidebar.header("Vehicle ID")
all_vehicles = sorted(df_display['vehicle_id'].unique())
vehicle_options = ["All vehicles"] + list(all_vehicles)
selected_vehicle = st.sidebar.selectbox(f"Choose a vehicle number for line {selected_line}", vehicle_options)

if selected_vehicle != "All vehicles":
    df_display = df_display[df_display["vehicle_id"] == selected_vehicle]
else:
    df_display = df_display

# KPIs
average_delay = round(df_display["delay_seconds"].mean(), 2)
max_delay = df_display["delay_seconds"].max()
number_of_vehicles = df_display["vehicle_id"].nunique()

st.subheader(f"Selected line: {selected_line}, selected vehicle: {selected_vehicle}")
left_column, middle_column, right_column = st.columns(3)

left_column.metric("Average delay (in seconds)", average_delay)
middle_column.metric("Maximum delay (in seconds)", max_delay)
right_column.metric("Number of vehicles", number_of_vehicles)

# lineplot of delay
st.subheader(f'Plot of delay for line: {selected_line}')

fig = px.line(df_display, x="created_at", y="delay_seconds",
                  labels={'created_at': 'Time of measurement', 'delay_seconds': 'Delay (in seconds)'},
                  color=df_display["vehicle_id"],
                  markers=True)    

fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Timetable")

st.plotly_chart(fig, width='stretch')

# entire map
st.subheader("Geospatial Map of delays")

map_center = [54.3520, 18.6466]
m = folium.Map(location=map_center, zoom_start=12)

if selected_line == "All lines":
    st.info("All lines chosen. Heatmap will be displayed for better readability. (only delayed buses included in the heatmap)")
    heat_data = df_display[df_display['delay_seconds'] > 120]

    heat_data_list = heat_data[['latitude', 'longitude', 'delay_seconds']].values.tolist()

    HeatMap(heat_data_list, radius=10, blur=15, max_zoom=1).add_to(m)

else:
    for index, row in df_display.iterrows():
        delay = row['delay_seconds']
        
        if delay < 120:
            color = 'green'
        elif 120 <= delay < 300:
            color = 'orange'
        else:
            color = 'red'

        popup_content = f"Line: {row['line_number']}<br>Delay: {delay}s<br>Time: {row['created_at'].strftime('%H:%M')}"
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=popup_content
        ).add_to(m)

st_folium(m, width=None, height=500)