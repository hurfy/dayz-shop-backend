FROM python:3.12-slim-bookworm

WORKDIR /auth

# Insall dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Insall & Config poetry
ENV POETRY_VERSION=2.1.1
ENV POETRY_HOME=/opt/poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

# Install dzshop lib
COPY packages/dzshop ./packages/dzshop/

# Install python dependencies
COPY services/auth/pyproject.toml services/auth/poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root --only main

COPY services/auth ./
ENV PYTHONPATH=/auth

WORKDIR /auth/src