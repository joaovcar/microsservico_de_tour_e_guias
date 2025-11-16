FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Default persistence (overridable via env)
ENV PERSISTENCE=sqlite
ENV DATABASE_URL=sqlite:///./data.db

EXPOSE 8000

# Run with Gunicorn + Uvicorn worker for production (single worker by default)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.app.main:app", "-b", "0.0.0.0:8000", "--workers", "1"]
