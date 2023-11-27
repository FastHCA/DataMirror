from abc import ABC, abstractmethod


class ExporterAbstract(ABC):
    @abstractmethod
    def export(self, writer):
        pass

    @abstractmethod
    def table_exporter(self, callback):
        pass

    @abstractmethod
    def sp_exporter(self, callback):
        pass

    @abstractmethod
    def trigger_exporter(self, callback):
        pass

    @abstractmethod
    def data_exporter(self, callback):
        pass

    @abstractmethod
    def manifest_exporter(self, callback):
        pass

    @abstractmethod
    def finish(self):
        pass
