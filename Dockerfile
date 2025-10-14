# Stage 1: Builder
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy requirements
COPY requirements.txt ./

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/

# Expose port
EXPOSE 80

# Run the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "src.api.main:app"]
