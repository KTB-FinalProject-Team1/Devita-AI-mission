from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.application.service import Service
from dependency_injector.wiring import inject, Provide
from containers import Container

router = APIRouter(prefix='/ai')


class Field(BaseModel):
    major_category: str
    sub_category: str


class DailyRequestDTO(BaseModel):
    user_id: str
    fields: list[Field]


class Mission(BaseModel):
    level: str
    content: str


class DailyResponseDTO(BaseModel):
    missions: list[Mission]


@router.post(
    '/daily',
    response_model=DailyResponseDTO,
    summary="데일리 미션"
)
@inject
def daily(
        req: DailyRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> DailyResponseDTO:
    """
    데일리 미션을 생성하는 API입니다. 유저 ID와 원하는 분야를 함께 바디에 실어줘야 합니다.

    - **user_id**: 유저 식별 PK
    - **fields**: 미션 생성 분야

    Request Body 예시
    ```json
    {
        "user_id": "000",
        "fields": [
            {
                "major_category": "CS",
                "sub_category": "자료구조"
            },
            {
                "major_category": "language",
                "sub_category": "JavaScript"
            }
        ]
    }
    ```
    """
    missions = service.daily(req.user_id, req.fields)
    res = [
        Mission(level="상", content=missions[0]),
        Mission(level="중", content=missions[1]),
        Mission(level="하", content=missions[2])
    ]

    return DailyResponseDTO(missions=res)


class AutonomousRequestDTO(BaseModel):
    user_id: str
    fields: list[Field]


class AutonomousResponseDTO(BaseModel):
    missions: list[str]


@router.post(
    '/autonomous',
    response_model=AutonomousResponseDTO,
    summary="자율 미션"
)
@inject
def autonomous(
        req: AutonomousRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> AutonomousResponseDTO:
    """
    자율 미션을 생성하는 API입니다. 유저 ID와 원하는 분야를 함께 바디에 실어줘야 합니다.

    - **user_id**: 유저 식별 PK
    - **fields**: 미션 생성 분야

    Request Body 예시
    ```json
    {
        "user_id": "000",
        "fields": [
            {
                "major_category": "CS",
                "sub_category": "자료구조"
            },
            {
                "major_category": "language",
                "sub_category": "JavaScript"
            }
        ]
    }
    ```
    """
    missions = service.autonomous(req.user_id, req.fields)
    print(len(missions))
    return AutonomousResponseDTO(missions=missions)
