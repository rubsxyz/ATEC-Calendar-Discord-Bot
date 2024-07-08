import logging
import os
from src.discord_bot import start_discord_bot

if not os.path.exists("images"): # cria folder images
    os.makedirs("images")

# Limpa o arquivo de log antes de configurar o logging
if os.path.exists("bot.log"):
    os.remove("bot.log")
    
# cria bot.log e mostra todos os log's do bot
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    start_discord_bot()