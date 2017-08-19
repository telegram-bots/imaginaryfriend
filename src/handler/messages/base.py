from abc import ABC, abstractmethod


class Base(ABC):
    bot = None

    @abstractmethod
    def can_handle(self, message):
        pass

    @abstractmethod
    def handle(self, message):
        pass
