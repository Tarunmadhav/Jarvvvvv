from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pathlib
import body
from time import sleep
import pandas as pd
from Body.Listen import MicExecution
from Body.Speak import Speak

scriptDirectory = pathlib.Path().absolute()

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument(f"user-data-dir={scriptDirectory}\\userdata")
os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"
PathofDriver = "DataBase\\chromedriver.exe"
driver = webdriver.Chrome(PathofDriver,options=options)

# Set window size
driver.set_window_size(1024, 768)

# Navigate to WhatsApp web
driver.get("https://web.whatsapp.com/")

# Wait for the QR code to appear
qr_code = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "side")))

# Wait for the chat window to appear
chat_window = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tab='1']")))

ListWeb = {'dhruv' : "+917011024588",
            'dost': "+91",
            "pote": '+91'}

def WhatsappSender(Name):
    Speak(f"Preparing To Send a Message To {Name}")
    Speak("What's The Message By The Way?")
    Message = MicExecution()
    Number = ListWeb[Name]
    LinkWeb = f'https://web.whatsapp.com/send?phone={Number}&text={Message}'
    driver.get(LinkWeb)
    try:
        send_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@title,"Send")]')))
        send_button.click()
        Speak("Message Sent")
        
    except:
        print("Invalid Number")