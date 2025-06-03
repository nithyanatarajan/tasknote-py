# -------- Base Image --------
FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install uv binary (copied from official uv image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# -------- Builder Stage --------
FROM base AS builder

WORKDIR /app

# Copy dependency declarations
COPY pyproject.toml uv.lock ./

# Install dependencies only (no project code yet)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy full project code
COPY src ./src

# Install project (with src layout) into .venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# -------- Final Runtime Stage --------
FROM base AS final

# Copy built app and virtualenv from builder
COPY --from=builder /app /app

# Ensure .venv is active in the runtime container
ENV PATH="/app/.venv/bin:$PATH"

# Expose FastAPI port
EXPOSE 8081

# Start FastAPI via uvicorn using uv's runner
CMD ["uv", "run", "uvicorn", "src.tasknote.main:app", "--host", "0.0.0.0", "--port", "8081"]
