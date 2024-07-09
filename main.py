import logging
import os
from src.discord_bot import start_discord_bot

# Cria a pasta 'images' se não existir
os.makedirs("images", exist_ok=True)

# Limpa o arquivo de log antes de configurar o logging
if os.path.exists("bot.log"):
    os.remove("bot.log")

# Configura o logging para mostrar logs no console e salvar em um arquivo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("bot.log"),
    logging.StreamHandler()
])

if __name__ == "__main__":
    start_discord_bot()
