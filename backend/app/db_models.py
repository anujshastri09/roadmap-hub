from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress_entries = relationship(
        "TopicProgress", back_populates="user", cascade="all, delete-orphan"
    )
    bookmarks = relationship(
        "Bookmark", back_populates="user", cascade="all, delete-orphan"
    )


class TopicProgress(Base):
    """One row per (user, field, topic) marking that topic as completed."""

    __tablename__ = "topic_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "field_id", "topic_id", name="uq_user_topic"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    field_id = Column(String, nullable=False, index=True)
    topic_id = Column(String, nullable=False, index=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_entries")


class Bookmark(Base):
    """A topic a user has saved for later / starred."""

    __tablename__ = "bookmarks"
    __table_args__ = (
        UniqueConstraint("user_id", "field_id", "topic_id", name="uq_user_bookmark"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    field_id = Column(String, nullable=False, index=True)
    topic_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")


class GeneratedRoadmap(Base):
    """An AI-generated roadmap for a field not in the curated static set."""

    __tablename__ = "generated_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(String, unique=True, index=True, nullable=False)  # slug, e.g. "rust-developer"
    name = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    icon = Column(String, default="✨")
    color = Column(String, default="#A98CFF")
    content_json = Column(Text, nullable=False)  # full Field JSON (stages/topics/resources)
    requested_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TopicSummary(Base):
    """Cached AI-generated quick summary for a topic, shared across all users."""

    __tablename__ = "topic_summaries"
    __table_args__ = (
        UniqueConstraint("field_id", "topic_id", name="uq_field_topic_summary"),
    )

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(String, nullable=False, index=True)
    topic_id = Column(String, nullable=False, index=True)
    summary_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizCache(Base):
    """Cached AI-generated quiz questions for a topic, shared across all users."""

    __tablename__ = "quiz_cache"
    __table_args__ = (
        UniqueConstraint("field_id", "topic_id", name="uq_field_topic_quiz"),
    )

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(String, nullable=False, index=True)
    topic_id = Column(String, nullable=False, index=True)
    questions_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ResumeBulletCache(Base):
    """Cached AI-generated resume bullet points per (user, field), regenerated on demand."""

    __tablename__ = "resume_bullet_cache"
    __table_args__ = (
        UniqueConstraint("user_id", "field_id", name="uq_user_field_bullets"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    field_id = Column(String, nullable=False, index=True)
    bullets_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    """Stores career-assistant chat history per user for continuity/auditing."""

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
