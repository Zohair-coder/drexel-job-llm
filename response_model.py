from pydantic import BaseModel


class ResponseModel(BaseModel):
    rating: int
    reasoning: str
