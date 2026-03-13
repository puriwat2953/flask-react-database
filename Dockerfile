# Stage 1: Build React frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend

# Copy dependencies
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Python Flask backend
FROM python:3.11-slim

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Make start script executable
RUN chmod +x start.sh

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend-static

# Create instance directory for SQLite database
RUN mkdir -p /app/backend/instance && chmod 777 /app/backend/instance

# Environment setup
ENV PORT=8080
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Run the application
CMD ["bash", "start.sh"]
