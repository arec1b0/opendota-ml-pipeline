FROM python:3.11-slim

# Install uv directly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# Install dependencies strictly for production
RUN uv sync --no-dev

# Copy application code
COPY . /app/

# Expose Uvicorn port
EXPOSE 8000

# Run Uvicorn via uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]