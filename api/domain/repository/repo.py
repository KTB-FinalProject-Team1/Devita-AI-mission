from abc import ABCMeta, abstractmethod


class IRepository(metaclass=ABCMeta):
    @abstractmethod
    def daily(
            self,
            user_id: str,
            field: list[str]
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def autonomous(
            self,
            user_id: str,
            field: list[str]
    ) -> list[str]:
        raise NotImplementedError
