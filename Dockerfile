FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN adduser --system --no-create-home --group --uid 1000 app

WORKDIR /app

COPY requirements.txt constraints.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app --chmod=0555 . .

RUN mkdir -p /app/staticfiles /app/media \
 && chown -R app:app /app/staticfiles /app/media

USER app

EXPOSE 8001

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "turtl.asgi:application"]
