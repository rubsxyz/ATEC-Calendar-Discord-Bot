from flask import Flask, after_this_request
import logging
import os
from src.discord_bot import start_discord_bot
from threading import Thread
from dotenv import load_dotenv
from waitress import serve

# Carregar variáveis de ambiente do .env
load_dotenv()

# Ensure img directory exists, if not, create one
if not os.path.exists("images"):
    os.makedirs("images")

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Vary'] = 'Cookie'
    return response

@app.route('/')
def hello_world():
    return 'Hello, this is your Discord Bot running!'

# Function to start the Flask server using waitress
def start_flask():
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Start the bot and Flask server in different threads
if __name__ == "__main__":
    Thread(target=start_flask).start()
    start_discord_bot()
