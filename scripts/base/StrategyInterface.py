from abc import ABC, abstractmethod

from scripts.base.WebDriverSingleton import WebDriverSingleton

driver = WebDriverSingleton.get_instance()


class ExtractStrategy(ABC):

    def __init__(self, strategy):
        self.another_strategy = strategy

    @abstractmethod
    def extrac_content(self, data):
        pass

    def extract_url_content(self, links, url):
        for link in links:
            href = link.get_attribute('href')
            if url in href:
                content = self.another_strategy.extrac_content(href)
                if content is None:
                    continue
                return href
                print("encontre detalle localidad")
            text = link.text
            print(f"Texto: {text} - URL: {href}")
        return "no se encontro la ruta"

