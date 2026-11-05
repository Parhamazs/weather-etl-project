import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def main():
    print("Connecting to database...")
    engine = create_engine(DATABASE_URL)

    # 1. خواندن داده‌ها از دیتابیس
    query = "SELECT date, temperature_max, precipitation_sum FROM weather_data ORDER BY date ASC;"
    df = pd.read_sql(query, engine)

    if df.empty:
        print("No data found in database!")
        return

    df['date'] = pd.to_datetime(df['date'])

    # 2. ذخیره خروجی CSV
    os.makedirs("data", exist_ok=True)
    csv_path = "data/monthly_weather_report.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data exported successfully to {csv_path}")

    # 3. گزارش متنی ساده در کنسول
    print("\n--- Summary Statistics ---")
    print(f"Total Days: {len(df)}")
    print(f"Average Max Temp: {df['temperature_max'].mean():.2f} °C")
    print(f"Hottest Day: {df.loc[df['temperature_max'].idxmax()]['date'].strftime('%Y-%m-%d')} ({df['temperature_max'].max()} °C)")
    print(f"Total Precipitation: {df['precipitation_sum'].sum():.2f} mm")

    # 4. رسم و ذخیره نمودار
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # نمودار خطی دما
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Max Temperature (°C)', color=color)
    ax1.plot(df['date'], df['temperature_max'], color=color, marker='o', label='Max Temp (°C)')
    ax1.tick_params(axis='y', labelcolor=color)

    # نمودار ستونی بارندگی روی محور دوم
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Precipitation (mm)', color=color)
    ax2.bar(df['date'], df['precipitation_sum'], color=color, alpha=0.3, width=0.5, label='Precipitation (mm)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Tehran Weather Summary Report')
    fig.tight_layout()

    chart_path = "data/weather_trend.png"
    plt.savefig(chart_path, dpi=300)
    print(f"Chart saved successfully to {chart_path}")

if __name__ == "__main__":
    main()
