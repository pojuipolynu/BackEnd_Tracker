from uuid import uuid4, UUID
from sqlalchemy import String, Boolean, ForeignKey, Text, Integer, DateTime, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects import postgresql
from .enum_variables import InviteStatus

class Base(DeclarativeBase):
    pass

class BaseId(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

class User(BaseId):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    rooms_created: Mapped[list["Room"]] = relationship("Room", foreign_keys="[Room.creator_id]", back_populates="creator")
    rooms_visiting: Mapped[list["Room"]] = relationship("Room", foreign_keys="[Room.visitor_id]", back_populates="visitor")
    
    friends: Mapped[list["Friend"]] = relationship("Friend", foreign_keys="[Friend.user_1_id]", back_populates="user_1")
    requests: Mapped[list["Request"]] = relationship("Request", foreign_keys="[Request.creator_id]", back_populates="creator")

class Level(BaseId):
    __tablename__ = "levels"
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    rooms: Mapped[list["Room"]] = relationship("Room", back_populates="level")

class Room(BaseId):
    __tablename__ = "rooms"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)  
    creation_status: Mapped[InviteStatus] = mapped_column(SQLAlchemyEnum(InviteStatus), default=InviteStatus.PENDING, nullable=False)
    room_status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    level_id: Mapped[UUID] = mapped_column(ForeignKey('levels.id'), nullable=False)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    visitor_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)

    level: Mapped["Level"] = relationship("Level", back_populates="rooms")
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id], back_populates="rooms_created")
    visitor: Mapped["User"] = relationship("User", foreign_keys=[visitor_id], back_populates="rooms_visiting")

class Friend(BaseId):
    __tablename__ = "friends"
    user_1_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    user_2_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)

    user_1: Mapped["User"] = relationship("User", foreign_keys=[user_1_id], back_populates="friends")

class Request(BaseId):
    __tablename__ = "requests"
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[InviteStatus] = mapped_column(SQLAlchemyEnum(InviteStatus), default=InviteStatus.PENDING, nullable=False)

    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id], back_populates="requests")