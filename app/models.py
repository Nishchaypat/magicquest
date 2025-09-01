from pydantic import BaseModel
from typing import List, Optional

class StoryRequest(BaseModel):
    question: str

class StoryResponse(BaseModel):
    story: str
    learning_point: str
    badge: str
    badge_icon: str
    learning_path_badge: str

class StoryLog(BaseModel):
    question: str
    story: str
    learning_point: str
    badge: str
    badge_icon: str

class DashboardData(BaseModel):
    stories: List[StoryLog]
    badge_counts: dict
    learning_path_badge: str
