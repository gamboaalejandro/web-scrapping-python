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
        for idx, link in enumerate(links):
            if url in link:
                content = self.another_strategy.extrac_content(link)
                if content is None:
                    continue
                return link
        return

