FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN apt-get update && apt-get install -y unzip
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
RUN unzip -o /tmp/chromedriver.zip -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver-linux64/chromedriver
RUN ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# Debugging: List the contents of the /usr/local/bin directory
RUN ls -la /usr/local/bin
RUN ls -la /usr/local/bin/chromedriver-linux64
RUN /usr/local/bin/chromedriver --version
RUN /usr/local/bin/chromedriver-linux64/chromedriver --version

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application
COPY . /app
WORKDIR /app

# Run the application!
CMD ["python", "main.py"]