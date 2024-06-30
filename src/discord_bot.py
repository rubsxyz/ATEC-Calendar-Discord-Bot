import logging
import discord
from discord.ext import commands
import os
import asyncio
import threading
from datetime import datetime
from dotenv import load_dotenv
from .web_interaction import setup_driver, login_to_site
from .calendar_interaction import navigate_to_calendar, navigate_to_next_calendar, capture_calendar_image
from .config import get_config

# Set logging level for discord.py to suppress warnings
logging.getLogger('discord').setLevel(logging.ERROR)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure you have the necessary intent

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Comando normal para screenshot das aulas
@bot.tree.command(name="aulas", description="Capture and send the calendar")
async def aulas(interaction: discord.Interaction):
    thread = threading.Thread(target=run_selenium_in_thread, args=(interaction,))
    thread.start()

# Comando para screenshot das aulas da proxima semana
@bot.tree.command(name="proximasemana", description="Capture and send the calendar of the next week")
async def proximasemana(interaction: discord.Interaction):
    thread = threading.Thread(target=run_selenium_next_week_in_thread, args=(interaction,))
    thread.start()

# Sync command tree with Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        await bot.tree.sync()
        print("Commands synchronized successfully.")
    except Exception as e:
        print(f"Error synchronizing commands: {e}")

async def run_selenium(interaction):
    await interaction.response.send_message("A buscar o calendário...")

    # Load configuration
    config = get_config()

    # Ensure img directory exists
    if not os.path.exists("images"):
        os.makedirs("images")

    # Set up the driver
    driver, wait = setup_driver(config)

    # Log in to the site
    if not login_to_site(driver, wait, config):
        await interaction.edit_original_response(content="Falha ao fazer login no servidor de treinamento ATEC.")
        driver.quit()
        return
 
    # Navigate to the calendar page
    if not navigate_to_calendar(driver, wait):
        await interaction.edit_original_response(content="Falha ao navegar para a página do calendário.")
        driver.quit()
        return

    # Capture the calendar image
    capture_calendar_image(driver)

    # Send the image to the Discord channel
    with open("images/calendar_screenshot_cropped.png", "rb") as f:
        picture = discord.File(f)
        today = datetime.now().strftime("%d/%m/%Y")
        await interaction.edit_original_response(content=f"Calendário desta semana. Dia {today}:", attachments=[picture])

    driver.quit()

async def run_selenium_next_week(interaction):
    await interaction.response.send_message("A buscar o calendário da próxima semana...")

    # Load configuration
    config = get_config()

    # Ensure img directory exists
    if not os.path.exists("images"):
        os.makedirs("images")

    # Set up the driver
    driver, wait = setup_driver(config)

    # Log in to the site
    if not login_to_site(driver, wait, config):
        await interaction.edit_original_response(content="Falha ao fazer login no servidor de treinamento ATEC.")
        driver.quit()
        return
 
    # Navigate to the calendar page
    if not navigate_to_calendar(driver, wait):
        await interaction.edit_original_response(content="Falha ao navegar para a página do calendário.")
        driver.quit()
        return

    # Navigate to next week's calendar
    if not navigate_to_next_calendar(driver, wait):
        await interaction.edit_original_response(content="Falha ao navegar para o calendário da próxima semana.")
        driver.quit()
        return

    # Capture the calendar image
    capture_calendar_image(driver)

    # Send the image to the Discord channel
    with open("images/calendar_screenshot_cropped.png", "rb") as f:
        picture = discord.File(f)
        today = datetime.now().strftime("%d/%m/%Y")
        await interaction.edit_original_response(content=f"Calendário da próxima semana", attachments=[picture])

    driver.quit()

def run_selenium_in_thread(interaction):
    asyncio.run_coroutine_threadsafe(run_selenium(interaction), bot.loop)

def run_selenium_next_week_in_thread(interaction):
    asyncio.run_coroutine_threadsafe(run_selenium_next_week(interaction), bot.loop)

def start_discord_bot():
    bot.run(DISCORD_TOKEN)
