from pydantic import BaseModel

from api.interface.controllers.model.model import Field, Mission


class DailyRequestDTO(BaseModel):
    user_id: int
    fields: list[Field]


class DailyResponseDTO(BaseModel):
    # missions: list[Mission]
    missions: str

class AutonomousRequestDTO(BaseModel):
    user_id: int
    fields: list[Field]


class AutonomousResponseDTO(BaseModel):
    # missions: list[Mission]
    missions: str