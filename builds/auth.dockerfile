# Build stage
FROM python:3.11-slim-bookworm AS builder

WORKDIR /auth

# Insall dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Install shared lib
COPY src/shared ./shared
RUN pip install --user -e ./shared

# Install all requirements
COPY src/auth/requirements.txt .
RUN pip install --user -r requirements.txt

# Generate JWT keys
COPY scripts/generate-keys.sh /auth/scripts/
RUN chmod +x /auth/scripts/generate-keys.sh \
    && /auth/scripts/generate-keys.sh

# Final stage
FROM python:3.11-slim-bookworm

WORKDIR /auth

# Copy from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /auth/certs /auth/certs
COPY --from=builder /auth/shared /auth/shared
COPY src/auth/ .

# Set env
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/auth:/auth/shared"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]