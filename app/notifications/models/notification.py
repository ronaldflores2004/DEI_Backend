from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Notification(Base):

    __tablename__ = "notifications"
    
    __table_args__ = (

        Index(
            "ix_notifications_user_read",
            "user_id",
            "is_read"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    message = Column(
        String(1000),
        nullable=False
    )

    type = Column(
        String(50),
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    user = relationship(
        "User",
        back_populates="notifications"
    )