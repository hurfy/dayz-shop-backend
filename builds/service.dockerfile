# Build stage
FROM python:3.11-slim-bookworm AS builder

ARG ROOT_PATH

WORKDIR /${ROOT_PATH}

# Insall dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install shared lib
COPY src/shared ./shared
RUN pip install --user -e ./shared

# Install all requirements
COPY src/${ROOT_PATH}/requirements.txt .
RUN pip install --user -r requirements.txt

# Final stage
FROM python:3.11-slim-bookworm

ARG ROOT_PATH

WORKDIR /application

# Copy from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /${ROOT_PATH}/shared /${ROOT_PATH}/shared
COPY src/gateway/ .

# Set env
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/${ROOT_PATH}:/${ROOT_PATH}/shared"
