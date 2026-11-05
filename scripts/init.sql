CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    date DATE,
    temperature_max FLOAT,
    precipitation_sum FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
