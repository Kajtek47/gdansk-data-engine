# 🚌 Gdańsk Data Engine

> A robust ETL pipeline for real-time monitoring and geospatial analysis of public transport delays in Gdańsk.

Traffic Map Preview<img width="1918" height="910" alt="map_overview" src="https://github.com/user-attachments/assets/045b9bbf-f929-4acb-b2ad-f08db24fc2ca" />

## 🎯 Project Overview
This project implements an automated **ETL (Extract, Transform, Load)** system that ingests GPS data from **all public transport vehicles** (buses & trams) in Gdańsk every 30 seconds. 

The goal is to archive historical movement data to identify city-wide traffic bottlenecks and analyze schedule adherence. The system distinguishes between vehicle types and allows for granular analysis of specific lines versus the entire transport network.

This solution is built with **scalability and reliability** in mind, utilizing containerization and professional database management.

## 🛠 Tech Stack
* **Core:** Python 3.10
* **Database:** PostgreSQL (Dockerized)
* **Infrastructure:** Docker & Docker Compose
* **Data Analysis:** Pandas, SQL
* **Visualization:** Streamlit (Web Dashboard), Folium (Heatmaps & Markers), Plotly (Charts)
* **Libraries:** `psycopg2-binary`, `requests`, `streamlit-folium`

## ⚙️ System Architecture

The pipeline consists of four main stages:

1.  **Extract:** A Python daemon connects to the *Open Gdańsk API* to fetch real-time positions of ~500 vehicles.
2.  **Transform:** Raw JSON data is validated and parsed. Timestamps are normalized.
3.  **Load:** Data is securely inserted into a **PostgreSQL** database running in a Docker container using optimized batch processing.
4.  **Analyze & Visualize:** A centralized **Streamlit Dashboard** provides real-time analytics, replacing manual script execution. It features:
    * **KPI Monitors:** Live tracking of active vehicles and average delays.
    * **Smart Mapping:** Automatically switches between **Heatmaps** (for city-wide overview) and **Detail Markers** (for single-line analysis).

---

## 📊 Analytics Showcase

### 1. Interactive Hybrid Map
A powerful visualization tool that adapts to the amount of data. Users can toggle between:
* 🔥 **Global View (Heatmap):** See density of delays across the entire city without clutter.
* 🔎 **Granular View (Markers):** Select a specific line (e.g., "Line 168") to inspect individual vehicle positions and delay details.

Map Screenshot<img width="1919" height="909" alt="map_details" src="https://github.com/user-attachments/assets/be2f7be3-34ed-4b6b-96fb-a8002e9f0ae7" />

### 2. Delay Trends
Interactive line charts showing how delays fluctuate for specific vehicles throughout the day, helping to identify peak traffic hours.

Chart Screenshot<img width="1917" height="908" alt="chart_details" src="https://github.com/user-attachments/assets/778e4f81-dfd7-4a8d-b943-7c82d60cf0df" />

### 3. Structured Data Storage
All data is persisted in a relational database, allowing for complex SQL queries across thousands of historical records.

---

## 🚀 How to Run

### Prerequisites
* Docker & Docker Compose
* Python 3.8+

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Kajtek_47/gdansk-data-engine.git](https://github.com/Kajtek_47/gdansk-data-engine.git)
    cd gdansk-data-engine
    ```

2.  **Start the infrastructure:**
    This command spins up the PostgreSQL container with persistent storage.
    ```bash
    docker-compose up -d
    ```

3.  **Set up Virtual Environment (Recommended):**
    Create and activate a clean Python environment to avoid conflicts.
    
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Pipeline:**
    Start collecting data in real-time. Keep this terminal open or run in background.
    ```bash
    python main.py
    ```

6.  **Launch the Dashboard:**
    Open a new terminal (remember to activate venv!) and run:
    ```bash
    streamlit run src/dashboard.py
    ```
    The application will automatically open in your browser at `http://localhost:8501`.