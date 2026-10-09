from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, StringConstraints

Identifier = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]

class EventCreate(BaseModel):
    user_id: Identifier
    event_type: Identifier
    value: float = 0
class EventOut(EventCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}
class Summary(BaseModel):
    total_events: int
    unique_users: int
    total_value: float
    average_value: float
