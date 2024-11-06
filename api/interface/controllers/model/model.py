from pydantic import BaseModel


class Field(BaseModel):
    main_category: str
    sub_category: str


class Mission(BaseModel):
    level: str
    content: str
