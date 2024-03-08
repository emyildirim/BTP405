# The base image is python 3.11 slim
FROM python:3.11-slim

# Install required dependencies
RUN pip install mysql-connector-python && \
    pip install python-dotenv

# Copy application files to the /app directory in the container
COPY . /app

# Set the working directory
WORKDIR /app

# Command to run the server
CMD ["python", "-u", "server.py"]

# Expose the application port
EXPOSE 8080