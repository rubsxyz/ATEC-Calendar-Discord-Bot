import logging
import discord
import aiohttp
import sys
from discord import File
from discord.ext import commands
from .config import get_config

# Get configuration
config = get_config()

DISCORD_TOKEN = config['DISCORD_TOKEN']
CHANNEL_ID = int(config['CHANNEL_ID'])

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        await self.send_calendar_image()
        await self.close()

    async def send_calendar_image(self):
        try:
            channel = self.get_channel(CHANNEL_ID)
            async with aiohttp.ClientSession() as session:
                with open("img/calendar_screenshot_cropped.png", "rb") as f:
                    file = discord.File(f, filename="calendar_screenshot_cropped.png")
                    await channel.send(file=file)
            logging.info("Calendar image sent successfully.")
        except Exception as e:
            logging.error(f"Error sending the calendar image: {e}")

def start_discord_bot():
    intents = discord.Intents.default()
    client = MyClient(intents=intents)
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        logging.error(f"Error running the Discord bot: {e}")
        sys.exit(1)
