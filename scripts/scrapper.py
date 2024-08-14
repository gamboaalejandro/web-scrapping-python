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

driver = WebDriverSingleton.get_instance()


class ChromeScrapper(ScrapperUrlInterface):
    html_to_scrap = ''

    def __init__(self, extraction_strategy: ExtractStrategy, headless=True):
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
        container = driver.find_element(By.ID, 'list-tab-pane')
        miclase = self.another_strategy.extrac_content(container)
        print(f"esta es mi clase {miclase}")
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


class ExtractDivClassStrategy(ExtractStrategy):

    def extrac_content(self, data):
        print("hola")
        print(data.find_element(By.CLASS_NAME, "col-1 text-uppercase fs-6 fw-bold").text)
        clase = self.get_text_and_a_label(data, 'IEU')
        # for c in clase:
        #     class_name = c.get_attribute("class")
        #     div_elementor = c.find_element(By.CLASS_NAME, class_name)
        #     print(div_elementor.text)
        return clase

    def get_text_and_a_label(self, divs, target_text):

        #if target_text in divs.text:
        #    return divs

        child_divs = divs.find_elements(By.TAG_NAME, "div")

        for div in child_divs:
            found = self.get_text_and_a_label(div, target_text)
            if found:
                return found

        return None
