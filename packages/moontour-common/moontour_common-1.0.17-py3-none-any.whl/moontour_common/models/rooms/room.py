import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, validator


class RoomMode(StrEnum):
    streak = 'streak'
    duel = 'duel'
    teams = 'teams'


class RoomStatus(StrEnum):
    waiting = 'waiting'
    waiting_to_start = 'waitingToStart'
    running = 'running'
    closed = 'closed'


class BaseRoom(BaseModel, ABC):
    id: str = Field(alias='id_', default_factory=lambda: str(uuid.uuid4()))
    map: str = 'world'
    status: RoomStatus = RoomStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    start_time: datetime | None = None
    mode: str = None

    @validator("mode", always=True)
    def compute_mode(cls, value):
        return cls.get_mode()

    @staticmethod
    @abstractmethod
    def get_mode() -> RoomMode:
        pass

    class Config:
        allow_population_by_field_name = True
