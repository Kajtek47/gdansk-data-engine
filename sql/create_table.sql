CREATE TABLE bus_positions (
    id SERIAL PRIMARY KEY,
    line_number VARCHAR(10),
    vehicle_id VARCHAR(20),
    delay_seconds INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
