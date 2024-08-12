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
            options.headless = True  # Ejecutar el navegador en segundo plano sin GUI (opcional)
            cls._instance = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))
        return cls._instance

    @classmethod
    def close_instance(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance.quit()
            cls._instance = None
