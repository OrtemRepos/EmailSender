FROM python:3.12.6-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.4.12 /uv /bin/uv

WORKDIR /app

COPY pyproject.toml /app

RUN uv venv

COPY src /app/src

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
