import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
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
service = Service(executable_path="D:/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 60)

# URL de login e informações de login
login_url = "https://trainingserver.atec.pt/trainingserver/"
username = "t0118939"
password = "243816758"

# Função para realizar login
def login_to_site(login_url, username, password):
    driver.get(login_url)
    logging.info("Página de login carregada.")

    try:
        # Espera explícita para os campos de login
        user_field = wait.until(EC.presence_of_element_located((By.ID, "txtUser")))
        pass_field = wait.until(EC.presence_of_element_located((By.ID, "txtPwd")))

        user_field.send_keys(username)
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.RETURN)
        logging.info("Credenciais de login enviadas.")

        # Espera explícita para a página após o login
        wait.until(EC.url_contains("DesktopDefault"))
        logging.info("Login realizado com sucesso.")
        return True

    except TimeoutException:
        logging.error("Timeout ao tentar fazer login.")
        return False

# Função para navegar até a página do calendário e clicar no link "Agenda Pessoal"
def navigate_to_calendar():
    try:
        # Espera explícita para a página principal após o login
        wait.until(EC.presence_of_element_located((By.ID, "li_942")))
        
        # Mover o mouse sobre o menu dropdown para revelar o link "Agenda"
        logging.info("Tentando localizar o menu dropdown.")
        dropdown_menu = wait.until(EC.visibility_of_element_located((By.ID, "li_942")))  # Substitua pelo ID correto do menu dropdown
        ActionChains(driver).move_to_element(dropdown_menu).perform()
        logging.info("Mouse movido sobre o menu dropdown.")

        # Espera para garantir que o link "Agenda Pessoal" seja interativo
        time.sleep(2)

        # Clicar no link "Agenda Pessoal"
        logging.info("Tentando localizar o link 'Agenda Pessoal'.")
        agenda_link = wait.until(EC.element_to_be_clickable((By.ID, "link_level0_943")))  # Substitua pelo ID correto do link de agenda
        agenda_link.click()
        logging.info("Clicou no link 'Agenda Pessoal'.")

        # Espera explícita para garantir que a página do calendário foi carregada
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_details")))  # Substitua pelo ID de um elemento presente na página do calendário
        logging.info("Página do calendário carregada com sucesso.")

    except (TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"Falha ao carregar a página do calendário: {e}")
        return False

    return True

# Função para capturar a imagem do calendário
def capture_calendar_image():
    try:
        time.sleep(10)  # Aumenta o tempo de espera para garantir que a página esteja totalmente carregada
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
CHANNEL_ID = 1250759096274259988  # Substitua pelo ID do canal

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
if not login_to_site(login_url, username, password):
    logging.warning("Login falhou. Tentando novamente...")
    if not login_to_site(login_url, username, password):
        logging.error("Falha ao fazer login após duas tentativas.")
        driver.quit()
        sys.exit(1)

# Navegar até a página do calendário
if not navigate_to_calendar():
    logging.error("Falha ao navegar para a página do calendário.")
    driver.quit()
    sys.exit(1)

# Capturar a imagem do calendário
capture_calendar_image()

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
