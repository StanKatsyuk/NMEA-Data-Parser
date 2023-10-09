from abc import ABC, abstractmethod


class BaseNMEAParser(ABC):
    @abstractmethod
    def parse(self, fields):
        pass
