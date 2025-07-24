import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

def init_driver():
    """
    Inicializa o WebDriver e realiza o login no sistema.
    """

    load_dotenv()

    apex_user = os.getenv("APEX_USER")
    apex_password = os.getenv("APEX_PASSWORD")

    try:
        options = Options()
        options.add_argument("--headless=new")  # modo sem janela
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        driver.get("https://apexdsv.hcrp.usp.br/apex/r/hc/gerenciamento-sati/home")
        wait.until(EC.presence_of_element_located((By.ID, "P9999_USERNAME")))

        # Realiza o login
        driver.find_element(By.ID, "P9999_USERNAME").send_keys(apex_user)
        driver.find_element(By.ID, "P9999_PASSWORD").send_keys(apex_password)

        time.sleep(1)

        btn_login = driver.find_element(By.ID, "B752443182379958634")
        btn_login.click()

        time.sleep(1)


        return driver, wait

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        if 'driver' in locals():
            driver.quit()
        raise