from uuid import uuid4, UUID
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func, Enum as SQLAlchemyEnum
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
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    rooms_created: Mapped[list["Room"]] = relationship(
        "Room", foreign_keys="[Room.creator_id]", back_populates="creator", 
        cascade="all, delete-orphan", passive_deletes=True
    )
    rooms_visiting: Mapped[list["Room"]] = relationship(
        "Room", foreign_keys="[Room.visitor_id]", back_populates="visitor", 
        cascade="all, delete-orphan", passive_deletes=True
    )
    friends: Mapped[list["Friend"]] = relationship(
        "Friend", foreign_keys="[Friend.user_1_id]", back_populates="user_1", 
        cascade="all, delete-orphan", passive_deletes=True
    )
    requests: Mapped[list["Request"]] = relationship(
        "Request", foreign_keys="[Request.creator_id]", back_populates="creator", 
        cascade="all, delete-orphan", passive_deletes=True
    )
    user_progress: Mapped[list["Progress"]] = relationship(
        "Progress", foreign_keys="[Progress.user_id]", back_populates="users", 
        cascade="all, delete-orphan", passive_deletes=True
    )

class Friend(BaseId):
    __tablename__ = "friends"
    user_1_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user_2_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user_1: Mapped["User"] = relationship("User", foreign_keys=[user_1_id], back_populates="friends")

class Request(BaseId):
    __tablename__ = "requests"
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    status: Mapped[InviteStatus] = mapped_column(SQLAlchemyEnum(InviteStatus), default=InviteStatus.PENDING, nullable=False)

    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id], back_populates="requests")

class Room(BaseId):
    __tablename__ = "rooms"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    creation_status: Mapped[InviteStatus] = mapped_column(SQLAlchemyEnum(InviteStatus), default=InviteStatus.PENDING, nullable=False)
    room_status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    visitor_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id], back_populates="rooms_created")
    visitor: Mapped["User"] = relationship("User", foreign_keys=[visitor_id], back_populates="rooms_visiting")
    
    room_habbits: Mapped[list["Habbit"]] = relationship(
        "Habbit", foreign_keys="[Habbit.room_id]", back_populates="room", 
        cascade="all, delete-orphan", passive_deletes=True
    )

    room_pet: Mapped[list["Pet"]] = relationship(
        "Pet", foreign_keys="[Pet.room_id]", back_populates="room", 
        cascade="all, delete-orphan", passive_deletes=True
    )

class Pet(BaseId):
    __tablename__ = "pets"
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    max_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    current_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    is_dead: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    room_id: Mapped[UUID] = mapped_column(ForeignKey('rooms.id', ondelete="CASCADE"), nullable=False)

    room: Mapped["Room"] = relationship("Room", foreign_keys=[room_id], back_populates="room_pet")


class Point(BaseId):
    __tablename__ = "points"
    point_value: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    
    habbits: Mapped[list["Habbit"]] = relationship("Habbit", foreign_keys="[Habbit.points_id]", back_populates="points")


class Habbit(BaseId):
    __tablename__ = "habbits"
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    
    points_id: Mapped[UUID] = mapped_column(ForeignKey('points.id'), nullable=False)
    room_id: Mapped[UUID] = mapped_column(ForeignKey('rooms.id', ondelete="CASCADE"), nullable=False)

    points: Mapped["Point"] = relationship("Point", foreign_keys=[points_id], back_populates="habbits")
    room: Mapped["Room"] = relationship("Room", foreign_keys=[room_id], back_populates="room_habbits")

    habbit_progress: Mapped[list["Progress"]] = relationship(
        "Progress", foreign_keys="[Progress.habbit_id]", back_populates="habbits", 
        cascade="all, delete-orphan", passive_deletes=True
    )

class Progress(BaseId):
    __tablename__ = "progresses"

    habbit_id: Mapped[UUID] = mapped_column(ForeignKey('habbits.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    habbits: Mapped["Habbit"] = relationship("Habbit", foreign_keys=[habbit_id], back_populates="habbit_progress")
    users: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="user_progress")
