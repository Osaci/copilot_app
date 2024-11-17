FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Install dependencies and Google Chrome
RUN apt-get update && apt-get install -y \
    net-tools \
    curl \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libx11-dev \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libfontconfig1 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Copy project files to container
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set Chrome binary paths
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Expose application port
EXPOSE 8080

# Set Flask app environment variable
ENV FLASK_APP=app_vm_new.py

# Command to start the Flask app
CMD ["gunicorn", "-w", "4", "-b", "192.168.65.1:8080", "app_vm_new:app"]
#CMD ["python", "app_vm_new.py"]
