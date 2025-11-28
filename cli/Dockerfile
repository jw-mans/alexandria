FROM python:3.10-slim

WORKDIR /app

COPY cli/ /app/cli
COPY tracker/ /app/tracker
COPY cli/pyproject.toml /app/

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root 

WORKDIR /app/cli
CMD ["tail", "-f", "/dev/null"]
