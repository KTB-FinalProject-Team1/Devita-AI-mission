from api.domain.repository.repo import IRepository
from model.llm import LLMManager
from api.interface.controllers.model.model import Mission
import json


class Repository(IRepository):
    def daily(
            self,
            userId: int,
            categories: list[str]
    ) -> str:
        res = LLMManager.get_instance().mission_generator_daily(categories)
        print(str(res))
        return res

    def autonomous(
            self,
            userId: int,
            subCategory: str
    ) -> list[Mission]:
        res = LLMManager.get_instance().mission_generator_free(subCategory)
        return [Mission(level=1, missionTitle=res[0]),
                Mission(level=2, missionTitle=res[1]),
                Mission(level=3, missionTitle=res[2])
        ]
