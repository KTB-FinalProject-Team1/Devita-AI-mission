from fastapi import APIRouter, Depends
from api.application.service import Service
from dependency_injector.wiring import inject, Provide

from api.interface.controllers.dto.dto import DailyRequestDTO, DailyResponseDTO, AutonomousRequestDTO, \
    AutonomousResponseDTO
from api.interface.controllers.model.model import Mission
from containers import Container

router = APIRouter(prefix='/ai')


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
        "user_id": 1234,
        "fields": [
            {
                "main_category": "cs",
                "sub_category": "자료구조"
            },
            {
                "main_category": "language",
                "sub_category": "javascript"
            }
        ]
    }
    ```
    """
    missions = service.daily(req.user_id, req.fields)
    # res = [
    #     Mission(level="상", content=missions[0]),
    #     Mission(level="중", content=missions[1]),
    #     Mission(level="하", content=missions[2])
    # ]

    print(missions)
    print(type(missions))
    return DailyResponseDTO(missions=missions)


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
        "user_id": 1234,
        "fields": [
            {
                "main_category": "cs",
                "sub_category": "자료구조"
            },
            {
                "main_category": "language",
                "sub_category": "javascript"
            }
        ]
    }
    ```
    """
    missions = service.autonomous(req.user_id, req.fields)
    print(len(missions))
    return AutonomousResponseDTO(missions=missions)
