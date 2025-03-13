# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Set the command to run the application (add gunicorn)
CMD ["gunicorn", "heatstroke.asgi:application", "-w", "2", "-k", "uvicorn.workers.UvicornWorker"]
