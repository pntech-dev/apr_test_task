from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    text: str
    rubrics: list[str]
    created_date: datetime

    model_config = {"from_attributes": True}
