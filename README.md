```markdown
# Weather ETL and Reporting Project

A lightweight, containerized data pipeline built for a GitHub portfolio. This project extracts weather forecast data from the Open-Meteo API, loads it into a PostgreSQL database, and processes monthly analytics to generate summary reports and trend visualizations using Python, Pandas, and Matplotlib.

---

## Project Structure

```text
weather-etl-project/
├── data/                  # Output directory for CSV reports and charts
├── scripts/
│   ├── init.sql           # Database initialization schema
│   ├── extract_load.py    # Weekly ingestion script (API to PostgreSQL)
│   └── transform_report.py# Monthly reporting script (PostgreSQL to CSV & PNG)
├── .env                   # Environment variables (ignored by git)
├── .gitignore             # Git exclusion rules
├── Dockerfile             # Container definition for Python services
├── docker-compose.yml     # Multi-container orchestration
└── requirements.txt       # Python dependencies
```

---

## Prerequisites

Ensure you have the following installed on your system:
- Docker and Docker Compose
- Git

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/weather-etl-project.git
cd weather-etl-project
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and define your database credentials:

```env
DB_NAME=weather_db
DB_USER=postgres
DB_PASS=your_secure_password
DB_HOST=db
DB_PORT=5432
```

### 3. Run the ETL Pipeline (Extract & Load)
Build and run the containers to fetch the weather data and load it into PostgreSQL:

```bash
docker compose up --build
```

This will spin up the PostgreSQL database, wait for it to initialize, and execute `extract_load.py` inside the Python container.

---

## Generating Reports & Analytics

The project uses Docker profiles to separate weekly ingestion from monthly analytics. 

To run the transformation and reporting script (which reads from the database, exports a CSV report to `data/monthly_weather_report.csv`, and generates a trend chart at `data/weather_trend.png`), run:

```bash
docker compose --profile reporting run --rm reporter_job
```

---

## Tech Stack

- **Language:** Python 3.11
- **Database:** PostgreSQL 15
- **Libraries:** Pandas, SQLAlchemy, Psycopg2, Requests, Matplotlib, Python-Dotenv
- **Containerization:** Docker & Docker Compose