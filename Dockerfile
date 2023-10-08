FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set environment variables
ENV MODULE_NAME main
ENV VARIABLE_NAME app
ENV WORKERS_PER_CORE 2

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application to the container
COPY app /app
