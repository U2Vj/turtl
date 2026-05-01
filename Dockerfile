FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt constraints.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/deploy/entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "turtl.asgi:application"]
