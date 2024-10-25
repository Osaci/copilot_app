FROM python:3.10-slim

#container workdir
WORKDIR /app

#install chromium and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    libgl1-mesa-glx \
    libnss3 \
    libfontconfig1 \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x /usr/bin/chromium && chmod +x /usr/bin/chromedriver

#copy dir contents to container
COPY . /app

#install packages
RUN pip install --no-cache-dir -r requirements.txt

#expose app port
EXPOSE 8080

#headless
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

#run
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

#command to start
#CMD gunicorn -b 0.0.0.0:5000 app:app  #"app:create_app()"
#CMD gunicorn -b 0.0.0.0:${PORT:-8080} app:app
CMD ["python", "app.py"]
