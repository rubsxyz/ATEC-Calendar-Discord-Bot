import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import discord
import aiohttp
import asyncio
import time
import sys

# Configuração de logging
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configurações do selenium para capturar a imagem
chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Caminho para o executável do Google Chrome
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')

# Certifique-se de que o caminho está correto para o chromedriver baixado
service = Service(executable_path="D:/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL do calendário e informações de login
calendar_url = "https://trainingserver.atec.pt/TrainingServer/GestaoFormacao/Horarios/UserCurrentSchedule.aspx?Hash=dC2fC6G+k7vQvwdTkmvRDar5j/lvWlLMPNLasC9jxSi3ci4tcaknwRg9xb4+a+LaXE5yUpZYP9TjqFwCMCy/viS5mo/T1wsoWyhqEUZ0eC0="
login_url = "https://trainingserver.atec.pt/trainingserver/"  # Substitua pela URL de login se for diferente
username = "t0118939"
password = "243816758"

# Função para realizar login
def login_to_site(login_url, username, password):
    driver.get(login_url)
    time.sleep(2)  # Aguarda a página carregar

    # Localiza os campos de entrada e insere o nome de usuário e senha
    user_field = driver.find_element(By.ID, "txtUser")  # Usando o ID correto para o campo de nome de usuário
    pass_field = driver.find_element(By.ID, "txtPwd")  # Usando o ID correto para o campo de senha

    user_field.send_keys(username)
    pass_field.send_keys(password)
    pass_field.send_keys(Keys.RETURN)

    time.sleep(2)  # Aguarda a página carregar após login

# Função para capturar a imagem do calendário
def capture_calendar_image(url):
    try:
        driver.get(url)
        time.sleep(3)
        driver.save_screenshot("calendar_screenshot.png")
        # Opcional: cortar a imagem para incluir apenas o calendário
        img = Image.open("calendar_screenshot.png")
        # Defina as coordenadas corretas para cortar a imagem
        left, top, right, bottom = 0, 0, img.width, img.height
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save("calendar_screenshot_cropped.png")
        logging.info("Imagem do calendário capturada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao capturar a imagem do calendário: {e}")

# Configurações do bot do Discord
DISCORD_TOKEN = 'MTI1MDc1NzE1OTc1OTc3NzgzMg.G_r2q8.-PUpAIZ-D8cO1zt9C5NE3ENMn-ONo-nRgE_SrE'
CHANNEL_ID = 1192533885632913498  # Substitua pelo ID do canal

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logado como {self.user}')
        await self.send_calendar_image()
        await self.close()

    async def send_calendar_image(self):
        try:
            channel = self.get_channel(CHANNEL_ID)
            async with aiohttp.ClientSession() as session:
                with open("calendar_screenshot_cropped.png", "rb") as f:
                    file = discord.File(f, filename="calendar_screenshot_cropped.png")
                    await channel.send(file=file)
            logging.info("Imagem do calendário enviada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao enviar a imagem do calendário: {e}")

# Realizar login no site
login_to_site(login_url, username, password)

# Capturar a imagem do calendário
capture_calendar_image(calendar_url)

# Iniciar o bot do Discord
intents = discord.Intents.default()
client = MyClient(intents=intents)
try:
    client.run(DISCORD_TOKEN)
except Exception as e:
    logging.error(f"Erro ao executar o bot do Discord: {e}")
    sys.exit(1)

# Encerrar o driver
driver.quit()
sys.exit(0)