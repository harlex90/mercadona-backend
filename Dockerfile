FROM python:3.8-slim

WORKDIR /app

COPY src .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
