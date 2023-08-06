from abc import ABC, abstractmethod
from supextend.core import InternResource


class Cleaner(InternResource, ABC):

    @abstractmethod
    def list_intern_resource(self, **kwargs):
        pass

    @abstractmethod
    def delete_intern_resource(self, pk):
        pass

    @abstractmethod
    def create_intern_resource(self, **kwargs):
        pass

    @abstractmethod
    def update_intern_resource(self, pk, **kwargs):
        pass

    @abstractmethod
    def get_intern_resource(self, pk):
        pass


class ChartCleaner(Cleaner, ABC):
    pass


class DashboardCleaner(Cleaner, ABC):
    pass


class AirflowTaskInstanceCleaner(Cleaner, ABC):
    pass


class OwnerCleaner(Cleaner, ABC):
    pass


class TagCleaner(Cleaner, ABC):
    pass
