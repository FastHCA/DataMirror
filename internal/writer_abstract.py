from abc import ABC, abstractmethod


class WriterAbstract(ABC):
    @abstractmethod
    def table_writer(self, data):
        pass

    @abstractmethod
    def sp_writer(self, data):
        pass

    @abstractmethod
    def trigger_writer(self, data):
        pass

    @abstractmethod
    def data_writer(self, data):
        pass

    @abstractmethod
    def manifest_writer(self, driver):
        pass

    @abstractmethod
    def finish(self):
        pass
