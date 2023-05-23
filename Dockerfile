FROM python:3.8-slim


WORKDIR /app

# Install required packages for psycopg2
RUN apt-get update && apt-get install -y libpq-dev build-essential

COPY src .

RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

CMD ["python", "app.py"]
