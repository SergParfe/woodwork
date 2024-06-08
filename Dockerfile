FROM python:3.9.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY /woodwork .

CMD ["python", "manage.py", "runserver", "0:8000"]
