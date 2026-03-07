from pydantic import BaseModel


class TransportRouteResponse(BaseModel):
    route_id: int
    mode: str
    duration: int
    cost: float
    stops: int
