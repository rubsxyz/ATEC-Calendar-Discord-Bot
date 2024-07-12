FROM python:3.11-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && apt-get clean

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
RUN unzip -o /tmp/chromedriver.zip -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver-linux64/chromedriver
RUN ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your bot code
COPY . /app
WORKDIR /app

# Run the bot
CMD ["python", "discord_bot.py"]
