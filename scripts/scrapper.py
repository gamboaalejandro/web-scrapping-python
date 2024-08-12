from abc import ABC

import config.settings
# code to get data from url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver

from scripts.base.StrategyInterface import ExtractStrategy
from scripts.base.WebDriverSingleton import WebDriverSingleton
from scripts.base.asbtract_scrapper import ScrapperUrlInterface


class ChromeScrapper(ScrapperUrlInterface):
    html_to_scrap = ''

    def __init__(self, extraction_strategy:ExtractStrategy, headless=True):
        super().__init__(extraction_strategy)

    def scraper(self, url):
        super().scraper(url)

    def fetch_page(self, url):
        # Navegar a la URL deseada
        # url = config.settings.WEB_BASE_URL_PUBLIC
        WebDriverSingleton.get_instance().get(url)
        # Obtener el contenido de la página
        page_content = WebDriverSingleton.get_instance().page_source
        self.html_to_scrap = page_content
        return page_content

    def extract_data(self):
        return self.extraction_strategy.extrac_content(self.html_to_scrap)
    def process_data(self):
        pass




class UrlContentExtractionStrategy(ExtractStrategy):

    def extrac_content(self, data):
        a_labels = []
        container = data.find_element(By.ID, 'myTabContent')
        links = container.find_elements(By.TAG_NAME, 'a')
        # SE REQUIERE CREAR ALGUNA ESTRATEGIA O ABSTRACCION QUE MANEJE LOS DISTINTTOS ELEMENTOS EN EL HTML
        for link in links:
            href = link.get_attribute('href')
            text = link.text
            a_labels.append(href)
            print(f"Texto: {text} - URL: {href}")

        if not self.another_strategy:
            return data
        self.another_strategy.extrac_content(data)

        pass

class ExtractContentFromALabel(ExtractStrategy):

    def extrac_content(self):
