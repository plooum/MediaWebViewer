FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn

COPY app.py .
RUN mkdir media

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
