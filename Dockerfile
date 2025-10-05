# Multi-stage Docker build for HYPERION Elite Bot
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base as production

# Create non-root user for security
RUN groupadd -r hyperion && useradd -r -g hyperion hyperion

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/hits && \
    chown -R hyperion:hyperion /app

# Switch to non-root user
USER hyperion

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Expose port
EXPOSE 8080

# Default command
CMD ["python", "hyperion_elite_bot.py"]

# Development stage
FROM base as development

# Install development dependencies
RUN pip install pytest pytest-asyncio pytest-cov flake8 black bandit safety

# Copy application code
COPY . .

# Development command
CMD ["python", "hyperion_elite_bot.py", "--debug"]