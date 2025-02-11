# -Builder stage
FROM python:3.11.4-slim-buster as builder

# Upgrade pip to ensure the latest version
RUN pip install --upgrade pip

# Set work directory
WORKDIR /home/shop-auth

# Install python dependencies and create wheel archives
COPY ./auth/requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels


# -Final stage
FROM python:3.11.4-slim-buster

# Set work directory
WORKDIR /home/shop-auth

# Copy app files and dependencies from the builder stage
COPY ./auth .
COPY --from=builder /wheels /wheels

# Install python dependencies from the wheel archive
RUN pip install --no-index --find-links=/wheels -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED 1
