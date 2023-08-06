from abc import ABC, abstractmethod
from supextend.core import InternResource


class Extension(InternResource, ABC):

    @abstractmethod
    def list_intern_resource(self):
        pass

    @abstractmethod
    def delete_intern_resource(self, pk):
        pass

    @abstractmethod
    def create_intern_resource(self,
                               title: str,
                               color: str,
                               created_by: str,
                               description: str
                               ):
        pass

    @abstractmethod
    def update_intern_resource(self,
                               pk,
                               title: str,
                               color: str,
                               created_by: str,
                               description: str
                               ):
        pass

    @abstractmethod
    def get_intern_resource(self, pk):
        pass


class WorkspaceExtension(Extension, ABC):
    pass
