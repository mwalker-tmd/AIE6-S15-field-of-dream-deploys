# --- Frontend Build Stage ---
FROM node:18 AS frontend-build

WORKDIR /app/frontend

# Copy frontend source and env file
COPY frontend/package*.json ./
RUN npm install

# Ensure Vite uses .env.production
COPY frontend/ ./
RUN npm run build -- --mode production

# --- Backend Build Stage ---
FROM python:3.11-slim AS backend-build

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv (fast dependency resolver)
RUN curl -Ls https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.local/bin:$PATH"

# Copy backend source and pyproject.toml
COPY backend/ ./backend/
COPY pyproject.toml ./backend/pyproject.toml
WORKDIR /app/backend

# Compile requirements.txt using uv
RUN uv pip compile pyproject.toml -o requirements.txt

# --- Final Stage ---
FROM python:3.11-slim

WORKDIR /app

# Set environment variables early
ENV PYTHONPATH=/app/backend
ENV ENVIRONMENT=production

# Copy backend app code and compiled requirements
COPY --from=backend-build /app/backend /app/backend
COPY --from=backend-build /app/backend/requirements.txt ./backend/requirements.txt

# Install Python dependencies in runtime container
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy frontend build output
COPY --from=frontend-build /app/frontend/dist /app/backend/static

# Copy any other needed files (e.g., .env, static, etc.)

# Expose ports (adjust as needed)
EXPOSE 7860

# Start backend (adjust as needed for your app)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
