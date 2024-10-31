from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.application.service import Service
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix='/ai')


class DailyRequestDTO(BaseModel):
    user_id: str
    fields: list[str]


class Mission(BaseModel):
    level: str
    content: list[str]


class DailyResponseDTO(BaseModel):
    missions: list[Mission]


@router.post('/daily')
@inject
def daily(
        req: DailyRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> DailyResponseDTO:
    pass
