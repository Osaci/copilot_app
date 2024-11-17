FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Install dependencies and Google Chrome
RUN apt-get update && apt-get install -y \
    net-tools \
    curl

# Copy project files to container
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose application port
EXPOSE 8080

# Set Flask app environment variable
ENV FLASK_APP=app.py

# Command to start the Flask app
CMD ["python3", "app.py"]
