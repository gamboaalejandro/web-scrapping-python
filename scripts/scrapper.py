import config.settings
# code to get data from url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver



def get_data():
    # Configurar el navegador (opcionalmente en modo headless)
    options = Options()
    options.headless = True  # Ejecutar el navegador en segundo plano sin GUI (opcional)

    # Inicializar el WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome

    # Navegar a la URL deseada
    url = config.settings.WEB_BASE_URL
    driver.get(url)

    # Obtener el contenido de la página
    page_content = driver.page_source

    # Imprimir el contenido de la página (HTML)
    print(page_content)

    # Cerrar el navegador
    driver.quit()

    pass
