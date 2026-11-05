# استفاده از یک نسخه سبک پایتون
FROM python:3.11-slim

# تعیین دایرکتوری کاری در کانتینر
WORKDIR /app

# نصب پیش‌نیازها
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirror-pypi.runflare.com/simple -r requirements.txt

# کپی کردن کدهای پروژه
COPY . .

# اجرای اسکریپت (به صورت پیش‌فرض)
CMD ["python", "scripts/extract_load.py"]
