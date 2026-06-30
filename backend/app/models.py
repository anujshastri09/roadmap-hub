from pydantic import BaseModel, EmailStr, Field as PydanticField
from typing import List, Optional
from datetime import datetime


# ---------- Auth schemas ----------

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str = PydanticField(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Bookmark schema ----------

class BookmarkToggleRequest(BaseModel):
    field_id: str
    topic_id: str


# ---------- AI feature schemas ----------

class GenerateRoadmapRequest(BaseModel):
    field_name: str = PydanticField(
        min_length=2, max_length=80, description="e.g. 'Rust Developer', 'Data Engineer'"
    )


class SummarizeTopicRequest(BaseModel):
    field_id: str
    topic_id: str
    force_refresh: bool = False


class ChatRequest(BaseModel):
    message: str = PydanticField(min_length=1, max_length=1000)
    field_id: Optional[str] = None  # if set, chat is grounded in that field's roadmap


class ChatMessageOut(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuizRequest(BaseModel):
    field_id: str
    topic_id: str
    force_refresh: bool = False


class ResumeBulletsRequest(BaseModel):
    field_id: str


class Resource(BaseModel):
    title: str
    url: str
    type: str  # "article" | "docs" | "video" | "course" | "practice"


class Topic(BaseModel):
    id: str
    title: str
    description: str
    level: str  # "beginner" | "intermediate" | "advanced"
    estimated_hours: int
    resources: List[Resource]


class Stage(BaseModel):
    id: str
    title: str
    subtitle: str
    order: int
    topics: List[Topic]


class Field(BaseModel):
    id: str
    name: str
    tagline: str
    icon: str
    color: str
    stages: List[Stage]


class FieldSummary(BaseModel):
    id: str
    name: str
    tagline: str
    icon: str
    color: str
    stage_count: int
    topic_count: int
    resource_count: int
