from dependency_injector.wiring import inject
from api.interface.controllers.model.model import Field
from api.domain.repository.repo import IRepository


class Service:
    def __init__(
            self,
            repo: IRepository,
    ):
        self.repo = repo

    def daily(
            self,
            user_id: str,
            field: list[Field]
    # ) -> list[str]:
    ) -> str:
        missions = self.repo.daily(user_id, field)
        return missions

    def autonomous(
            self,
            user_id: str,
            field: list[Field]
    ) -> list[str]:
        missions = self.repo.autonomous(user_id, field)
        return missions
