import os
import time
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# ساخت Connection String با درایور psycopg2
DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def wait_for_db(engine, retries=5, delay=3):
    """صبر می‌کند تا دیتابیس کاملاً آماده پذیرش اتصال شود"""
    for i in range(retries):
        try:
            with engine.connect() as conn:
                print("Connected to PostgreSQL successfully!")
                return True
        except Exception as e:
            # اینجا e دقیقاً به ما می‌گوید که مشکل چیست (مثلاً Authentication Failed یا Connection Refused)
            print(f"Attempt {i+1}/{retries} failed. Error: {e}") 
            time.sleep(delay)
    raise Exception("Could not connect to the database. Check your .env credentials and DB_HOST.")

def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.6892&longitude=51.3890&daily=temperature_2m_max,precipitation_sum&timezone=auto"
    response = requests.get(url)
    return response.json()

def main():
    engine = create_engine(DB_URL)
    wait_for_db(engine)

    print("Fetching weather data...")
    data = fetch_weather_data()
    daily = data['daily']
    
    df = pd.DataFrame({
        'date': pd.to_datetime(daily['time']),
        'temperature_max': daily['temperature_2m_max'],
        'precipitation_sum': daily['precipitation_sum']
    })

    print(f"Inserting {len(df)} records into database...")
    df.to_sql('weather_data', engine, if_exists='append', index=False)
    print("Done! Data loaded successfully.")

if __name__ == "__main__":
    main()

