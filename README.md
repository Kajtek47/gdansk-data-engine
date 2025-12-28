# 🚌 Gdańsk Data Engine

> A robust ETL pipeline for real-time monitoring and geospatial analysis of public transport delays in Gdańsk.

![Traffic Map Preview](DRAG_AND_DROP_MAP_IMAGE_HERE.png)

## 🎯 Project Overview
This project implements an automated **ETL (Extract, Transform, Load)** system that ingests GPS data from public buses every 30 seconds. The goal is to archive historical movement data to identify traffic bottlenecks and analyze schedule adherence for specific bus lines (e.g., 168, 199).

Unlike simple scripts, this solution is built with **scalability and reliability** in mind, utilizing containerization and professional database management.

## 🛠 Tech Stack
* **Core:** Python 3.10
* **Database:** PostgreSQL (Dockerized)
* **Infrastructure:** Docker & Docker Compose
* **Data Analysis:** Pandas, SQL
* **Visualization:** Plotly (Interactive Charts), Folium (Geospatial Heatmaps)
* **Libraries:** `psycopg2-binary`, `requests`

## ⚙️ System Architecture

The pipeline consists of four main stages:

1.  **Extract:** A Python daemon connects to the *Open Gdańsk API* to fetch real-time vehicle positions.
2.  **Transform:** Raw JSON data is filtered (specific lines), validated, and parsed. Timestamps are normalized.
3.  **Load:** Data is securely inserted into a **PostgreSQL** database running in a Docker container. The system uses parameterized queries to prevent SQL injection.
4.  **Analyze:** On-demand scripts generate reports:
    * `visualizer.py`: Time-series analysis of delays.
    * `map_generator.py`: Geospatial mapping of traffic congestion.

---

## 📊 Analytics Showcase

### 1. Geospatial Analysis
Identification of "red zones" where buses frequently experience delays > 5 minutes.
![Map Screenshot](DRAG_AND_DROP_MAP_IMAGE_HERE.png)

### 2. Delay Trends
Interactive line charts showing how delays fluctuate for specific vehicles throughout the day.
![Chart Screenshot](DRAG_AND_DROP_CHART_IMAGE_HERE.png)

### 3. Structured Data Storage
All data is persisted in a relational database for advanced SQL querying.
![Database Screenshot](DRAG_AND_DROP_DB_IMAGE_HERE.png)

---

## 🚀 How to Run

### Prerequisites
* Docker & Docker Compose
* Python 3.8+

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/gdansk-data-engine.git](https://github.com/YOUR_USERNAME/gdansk-data-engine.git)
    cd gdansk-data-engine
    ```

2.  **Start the infrastructure:**
    This command spins up the PostgreSQL container with persistent storage.
    ```bash
    docker-compose up -d
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Pipeline:**
    Start collecting data in real-time.
    ```bash
    python main.py
    ```

5.  **Generate Reports (after collecting data):**
    ```bash
    # Generate delay chart
    python -m src.visualizer

    # Generate traffic map (HTML file)
    python -m src.map_generator
    ```

## 📈 Future Improvements
* Add a BI dashboard (e.g., Streamlit or Metabase).
* Implement Airflow for workflow orchestration.
* Deploy to a cloud provider (AWS/Azure).