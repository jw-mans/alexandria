FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction
COPY ./cli /app/cli
ENTRYPOINT ["tail", "-f", "/dev/null"]
