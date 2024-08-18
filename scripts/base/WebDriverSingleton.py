from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


class WebDriverSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            options = Options()
            options.add_argument("headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")  # Establecer tamaño de ventana para asegurar que el modo headless funcione
            options.add_argument("--log-level=3")  # Minimizar los logs del navegador
            cls._instance = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))
        return cls._instance

    @classmethod
    def close_instance(cls):
        if cls._instance:
            cls._instance.quit()
            cls._instance.close()
            cls._instance = None
