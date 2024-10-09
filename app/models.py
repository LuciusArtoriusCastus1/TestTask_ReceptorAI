from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class RoutingIntent(BaseModel):
    destinationName: str
    important: Optional[bool] = False
    bytes: Optional[int] = 0


class Event(BaseModel):
    payload: Dict[str, Any]
    routingIntents: List[RoutingIntent]
    strategy: Optional[str] = None


class Destination(BaseModel):
    destinationName: str
    transport: str
    url: Optional[str] = None


class User(BaseModel):
    email: str
    password: str
