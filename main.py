from flask import Flask
import logging
import os
from src.discord_bot import start_discord_bot
from threading import Thread

# Ensure img directory exists, if not, create one
if not os.path.exists("images"):
    os.makedirs("images")

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, this is your Discord Bot running!'

# Function to start the Flask server
def start_flask():
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Start the bot and Flask server in different threads
if __name__ == "__main__":
    Thread(target=start_flask).start()
    start_discord_bot()
