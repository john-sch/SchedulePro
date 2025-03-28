# Stage 1: Build the React frontend
FROM node:16 as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Build the Python backend image
FROM python:3.9
WORKDIR /app

# Copy and install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code and other project files
COPY . .

# Copy the built React app from the first stage into the backend
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Expose port 8000 and run the FastAPI application with Uvicorn
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
