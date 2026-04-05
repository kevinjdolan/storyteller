FROM python:3.12-slim AS python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

FROM python-base AS runtime

COPY requirements.runtime.txt .
RUN pip install -r requirements.runtime.txt

COPY alembic.ini .
COPY app ./app
COPY migrations ./migrations

EXPOSE 8565

CMD ["python", "-m", "app"]

FROM python-base AS development

COPY requirements.runtime.txt requirements.txt ./
RUN pip install -r requirements.txt

COPY alembic.ini .
COPY app ./app
COPY migrations ./migrations

EXPOSE 8565

CMD ["python", "-m", "app"]
