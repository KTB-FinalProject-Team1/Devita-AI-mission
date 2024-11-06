from abc import ABCMeta, abstractmethod
from api.interface.controllers.model.model import Field


class IRepository(metaclass=ABCMeta):
    @abstractmethod
    def daily(
            self,
            user_id: str,
            field: list[Field]
    # ) -> list[str]:
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def autonomous(
            self,
            user_id: str,
            field: list[Field]
    # ) -> list[str]:
    ) -> str:
        raise NotImplementedError
