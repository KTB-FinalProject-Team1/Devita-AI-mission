from dependency_injector.wiring import inject

from api.domain.repository.repo import IRepository


class Service:
    def __init__(
            self,
            repo: IRepository,
    ):
        self.repo = repo

    def daily(
            self,
            field: list[str]
    ) -> list[str]:
        missions = self.repo.daily(field)
        return missions

    def autonomous(
            self,
            field: list[str]
    ) -> list[str]:
        missions = self.repo.daily(field)
        return missions
