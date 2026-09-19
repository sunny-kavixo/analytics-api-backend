from datetime import datetime
from pydantic import BaseModel, Field
class EventCreate(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    event_type: str = Field(min_length=1, max_length=100)
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
