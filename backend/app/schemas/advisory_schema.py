from pydantic import BaseModel


class AdvisoryResponse(BaseModel):
    id: int
    city_id: int
    category: str
    severity: str
    title: str
