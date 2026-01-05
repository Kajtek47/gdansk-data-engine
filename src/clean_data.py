import duckdb
import pandas as pd

def clean_data_with_sql():
    print("Data cleaning started")

    input_file = 'data/gdansk_traffic_history.parquet'
    output_file = 'data/gdansk_traffic_history_cleaned.parquet'

    con = duckdb.connect()

    query = f"""
        WITH lag_metrics AS (
            SELECT 
                *,
                LAG(created_at) OVER (PARTITION BY line_number, vehicle_id ORDER BY created_at) AS prev_created_at,
                LAG(delay_seconds) OVER (PARTITION BY line_number, vehicle_id ORDER BY created_at) AS prev_delay_seconds,
                LAG(latitude) OVER (PARTITION BY line_number, vehicle_id ORDER BY created_at) AS prev_latitude,
                LAG(longitude) OVER (PARTITION BY line_number, vehicle_id ORDER BY created_at) AS prev_longitude
            FROM '{input_file}'
        ),

        calculations AS (
            SELECT
                *,
                DATE_DIFF('second', prev_created_at, created_at) AS time_diff,
                (delay_seconds - prev_delay_seconds) AS delay_diff,
                SQRT(POW(latitude - prev_latitude, 2) + POW(longitude - prev_longitude, 2)) * 111000 AS dist_meters
            FROM lag_metrics
            WHERE prev_created_at IS NOT NULL
        ),

        history_check AS (
            SELECT
                *,
                LAG(delay_diff) OVER (PARTITION BY line_number, vehicle_id ORDER BY created_at) AS prev_step_delay_diff,
                LAG(time_diff) OVER (PARTITION BY line_number, vehicle_id ORDER BY created_at) AS prev_step_time_diff
            FROM calculations
        ),

        anomalies AS (
            SELECT
                *,
                CASE
                    WHEN time_diff > 60
                        AND dist_meters < 30
                        AND ABS(delay_diff) > (time_diff * 0.9)
                    THEN 'GHOST_BUS'
                    
                    WHEN time_diff > 0 AND (dist_meters / time_diff) * 3.6 > 200
                    THEN 'IMPOSSIBLE_SPEED'

                    WHEN dist_meters < 30
                        AND prev_step_time_diff > 0
                        AND ABS(prev_step_delay_diff) > (prev_step_time_diff * 0.9)
                    THEN 'GHOST_TAIL'
                    
                    ELSE 'OK'
                END AS status
            FROM history_check
        )

        SELECT *
        FROM anomalies
        WHERE status = 'OK';
        """
    
    total_rows = con.execute(f"SELECT COUNT(*) FROM '{input_file}'").fetchone()[0]
    df_cleaned = con.execute(query).df()
    cleaned_rows = len(df_cleaned)

    print("Cleaning results:")
    print(f"    Input records: {total_rows}")
    print(f"    Output records: {cleaned_rows}")
    print(f"    Removed: {total_rows - cleaned_rows} (anomalies)")

    df_cleaned.to_parquet(output_file, index=False)
    print(f"Saved {output_file}")

if __name__ == "__main__":
    clean_data_with_sql()