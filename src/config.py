import os
from dotenv import load_dotenv

def get_config():
    load_dotenv()
    return {
        "LOGIN_URL": os.getenv("LOGIN_URL"),
        "USER_NAME": os.getenv("USER_NAME"),
        "USER_PASSWORD": os.getenv("USER_PASSWORD"),
        "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN"),
    }
