import logging
import os
from src.discord_bot import start_discord_bot

# Ensure img directory exists, if not, create one
if not os.path.exists("images"):
    os.makedirs("images")

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Start the bot
start_discord_bot()
