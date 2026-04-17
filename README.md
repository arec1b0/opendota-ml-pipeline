# OpenDota ML Pipeline

Production-ready Machine Learning pipeline for predicting match outcomes and analyzing data using the OpenDota API.

## Overview

This project provides an end-to-end MLOps pipeline for OpenDota data. It is built with:
- **FastAPI** for high-performance API endpoints
- **MLflow** for model registry and tracking
- **Prometheus** for monitoring and observability
- **uv** for fast and reproducible Python dependency management
- **Docker & Kubernetes** for containerization and deployment

## Features

- **Data Ingestion**: Streamlined data preparation.
- **Model Training**: Pipeline integration with MLflow tracking.
- **Serving**: FastAPI-based endpoints for predictions.
- **Monitoring**: Prometheus instrumentation for metrics tracking.

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- Docker (optional, for containerized execution)

### Installation

Clone the repository and install dependencies using `uv`:

```bash
git clone <repository_url>
cd opendota-ml-pipeline
uv sync
```

### Running the Application

Run the FastAPI application locally:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`. Metrics are exposed at `http://localhost:8000/metrics`.

### Docker

Build and run using Docker:

```bash
docker build -t opendota-ml-pipeline .
docker run -p 8000:8000 opendota-ml-pipeline
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
