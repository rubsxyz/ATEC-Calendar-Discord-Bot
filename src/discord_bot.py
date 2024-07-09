import logging
import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from .web_interaction import setup_driver, login_to_site
from .calendar_interaction import navigate_to_calendar, navigate_to_next_calendar, capture_calendar_image
from .config import get_config

logging.getLogger('discord').setLevel(logging.ERROR)

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.tree.command(name="aulas", description="Capture and send the calendar")
async def aulas(interaction: discord.Interaction):
    await interaction.response.defer()  # Defer the response to indicate processing
    await run_selenium(interaction)

@bot.tree.command(name="proximasemana", description="Capture and send the calendar of the next week")
async def proximasemana(interaction: discord.Interaction):
    await interaction.response.defer()  # Defer the response to indicate processing
    await run_selenium_next_week(interaction)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    try:
        await bot.tree.sync()
        logging.info("Commands synchronized successfully.")
    except Exception as e:
        logging.error(f"Error synchronizing commands: {e}")

async def login_to_atec(driver, wait, config, interaction):
    if not await asyncio.to_thread(login_to_site, driver, wait, config):
        await interaction.followup.send(content="Falha ao fazer login no servidor ATEC.")
        driver.quit()
        return False
    return True

async def run_selenium(interaction):
    config = get_config()
    driver, wait = await asyncio.to_thread(setup_driver, config)
    if not await login_to_atec(driver, wait, config, interaction):
        return

    if not await asyncio.to_thread(navigate_to_calendar, driver, wait):
        await interaction.followup.send(content="Falha ao navegar para a página do calendário.")
        driver.quit()
        return

    await asyncio.to_thread(capture_calendar_image, driver)
    with open("images/calendar_screenshot_cropped.png", "rb") as f:
        picture = discord.File(f)
        today = datetime.now().strftime("%d/%m/%Y")
        await interaction.followup.send(content=f"Calendário desta semana. Dia {today}:", file=picture)
    driver.quit()

async def run_selenium_next_week(interaction):
    config = get_config()
    driver, wait = await asyncio.to_thread(setup_driver, config)
    if not await login_to_atec(driver, wait, config, interaction):
        return

    if not await asyncio.to_thread(navigate_to_calendar, driver, wait):
        await interaction.followup.send(content="Falha ao navegar para a página do calendário.")
        driver.quit()
        return

    if not await asyncio.to_thread(navigate_to_next_calendar, driver, wait):
        await interaction.followup.send(content="Falha ao navegar para o calendário da próxima semana.")
        driver.quit()
        return

    await asyncio.to_thread(capture_calendar_image, driver)
    with open("images/calendar_screenshot_cropped.png", "rb") as f:
        picture = discord.File(f)
        await interaction.followup.send(content="Calendário da próxima semana", file=picture)
    driver.quit()

def start_discord_bot():
    bot.run(DISCORD_TOKEN)
