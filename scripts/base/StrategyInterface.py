from abc import ABC, abstractmethod


class ExtractStrategy(ABC):

    def __init__(self, strategy):
        self.another_strategy = strategy

    @abstractmethod
    def extrac_content(self, data):
        pass
