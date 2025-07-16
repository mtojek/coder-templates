FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev git && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Default workdir
WORKDIR /workspace
