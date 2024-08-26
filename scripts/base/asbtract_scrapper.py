from abc import ABC, abstractmethod


class ScrapperUrlInterface(ABC):
    def __init__(self, extraction_strategy):
        self.extraction_strategy = extraction_strategy

    @abstractmethod
    def scraper(self, url):
        self.fetch_page(url)
        self.extract_data()
        pass

    @abstractmethod
    def fetch_page(self, url):
        pass

    @abstractmethod
    def extract_data(self):
        pass

