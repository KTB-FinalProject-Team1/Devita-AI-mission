from abc import ABCMeta, abstractmethod


class IRepository(metaclass=ABCMeta):
    @abstractmethod
    def daily(
            self,
            field: list[str]
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def autonomous(
            self,
            field: list[str]
    ) -> list[str]:
        raise NotImplementedError
