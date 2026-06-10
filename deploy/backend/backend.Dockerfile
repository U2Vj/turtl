# 1. Build stage
FROM python:3.12-slim AS builder

RUN mkdir /app

WORKDIR /app

# Envs to optimize python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 2. Production stage
FROM python:3.12-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Copy dependencies from build
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app 

COPY --chown=appuser:appuser --chmod=755 . .

RUN mkdir -p /app/staticfiles /app/media \
&& chown -R appuser:appuser /app/staticfiles /app/media

RUN apt-get update && apt-get install --no-install-recommends -y curl
# Envs to optimize python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser


EXPOSE 8000

# Start app with daphne
CMD ["daphne", "--proxy-headers", "-b", "0.0.0.0", "-p", "8000", "turtl.asgi:application"]


