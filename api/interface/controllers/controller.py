from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.application.service import Service
from dependency_injector.wiring import inject, Provide
from containers import Container

router = APIRouter(prefix='/ai')


class DailyRequestDTO(BaseModel):
    user_id: str
    fields: list[str]


class Mission(BaseModel):
    level: str
    content: str


class DailyResponseDTO(BaseModel):
    missions: list[Mission]


@router.post('/daily')
@inject
def daily(
        req: DailyRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> DailyResponseDTO:
    missions = service.daily(req.user_id, req.fields)
    res = [
        Mission(level="상", content=missions[0]),
        Mission(level="중", content=missions[1]),
        Mission(level="하", content=missions[2])
    ]

    return DailyResponseDTO(missions=res)


class AutonomousRequestDTO(BaseModel):
    user_id: str
    fields: list[str]


class AutonomousResponseDTO(BaseModel):
    missions: list[str]


@router.post('/autonomous')
@inject
def autonomous(
        req: AutonomousRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> AutonomousResponseDTO:
    missions = service.autonomous(req.user_id, req.fields)
    print(len(missions))
    return AutonomousResponseDTO(missions=missions)
