FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install dependencies for psql
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /app/

ENTRYPOINT ["/entrypoint.sh"]
