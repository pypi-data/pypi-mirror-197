from abc import ABC, abstractmethod
from supextend.core import ExternResource


class Superset(ExternResource, ABC):

    @abstractmethod
    def list_superset_resource(self,
                               page: int,
                               page_size: int,
                               filter_value: str,
                               column: str,
                               opr: str
                               ):
        pass

    @abstractmethod
    def delete_superset_resource(self, pk: int):
        pass

    @abstractmethod
    def create_superset_resource(self, **kwargs):
        pass

    @abstractmethod
    def update_superset_resource(self, pk: int, title: str):
        pass

    @abstractmethod
    def get_superset_resource(self, pk: int):
        pass


class ChartSuperset(Superset, ABC):
    pass


class DashboardSuperset(Superset, ABC):
    pass
