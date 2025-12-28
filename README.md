# 🚌 Gdańsk Data Engine

> A robust ETL pipeline for real-time monitoring and geospatial analysis of public transport delays in Gdańsk.

![Traffic Map Preview]<img width="1918" height="910" alt="map_overview" src="https://github.com/user-attachments/assets/045b9bbf-f929-4acb-b2ad-f08db24fc2ca" />
()

## 🎯 Project Overview
This project implements an automated **ETL (Extract, Transform, Load)** system that ingests GPS data from **all public transport vehicles** (buses & trams) in Gdańsk every 30 seconds. 

The goal is to archive historical movement data to identify city-wide traffic bottlenecks and analyze schedule adherence. The system distinguishes between vehicle types and allows for granular analysis of specific lines versus the entire transport network.

This solution is built with **scalability and reliability** in mind, utilizing containerization and professional database management.

## 🛠 Tech Stack
* **Core:** Python 3.10
* **Database:** PostgreSQL (Dockerized)
* **Infrastructure:** Docker & Docker Compose
* **Data Analysis:** Pandas, SQL
* **Visualization:** Folium (Interactive Layered Maps), Plotly (Charts)
* **Libraries:** `psycopg2-binary`, `requests`

## ⚙️ System Architecture

The pipeline consists of four main stages:

1.  **Extract:** A Python daemon connects to the *Open Gdańsk API* to fetch real-time positions of ~500 vehicles.
2.  **Transform:** Raw JSON data is validated and parsed. Timestamps are normalized.
3.  **Load:** Data is securely inserted into a **PostgreSQL** database running in a Docker container using optimized batch processing.
4.  **Analyze:** On-demand scripts generate reports:
    * `visualizer.py`: Time-series analysis of delays for specific vehicles.
    * `bottlenecks_map.py`: Interactive HTML map with advanced filtering (All Lines vs. Single Line).

---

## 📊 Analytics Showcase

### 1. Interactive Hybrid Map
A powerful visualization tool that offers full control. Users can toggle between:
* 🔥 **Global View:** See all Buses or all Trams simultaneously to spot city-wide congestion.
* 🔎 **Granular View:** Filter specific lines (e.g., only "Line 168") to analyze individual routes.
![Map Screenshot](<img width="1919" height="909" alt="map_details" src="https://github.com/user-attachments/assets/be2f7be3-34ed-4b6b-96fb-a8002e9f0ae7" />
)

### 2. Delay Trends
Interactive line charts showing how delays fluctuate for specific vehicles throughout the day, helping to identify peak traffic hours.
![Chart Screenshot](<img width="1917" height="908" alt="chart_details" src="https://github.com/user-attachments/assets/778e4f81-dfd7-4a8d-b943-7c82d60cf0df" />
)

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
    git clone https://github.com/Kajtek_47/gdansk-data-engine.git
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

    # Generate interactive map (saves to bottlenecks_map.html)
    python -m src.map_generator
    ```

