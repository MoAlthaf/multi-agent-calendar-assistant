from typing import Literal, Optional

from pydantic import BaseModel, Field


class ScheduleEvent(BaseModel):
    summary: str
    description: str
    start_time_iso: str
    end_time_iso: str


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class Route(BaseModel):
    next_agent: Literal["scheduler", "availability", "editor", "deleter", "chat", "FINISH"]
    message: Optional[str] = Field(
        default=None,
        description=(
            "Required only when next_agent is 'chat'. A short natural-language reply "
            "to the user. Leave null for every other route — specialist agents and "
            "FINISH never need this field."
        ),
    )
