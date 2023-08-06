import json
import os
from contextlib import contextmanager, asynccontextmanager
from typing import TypeVar, AsyncContextManager

import redis
from redis.commands.json.path import Path

from moontour_common.database.rabbitmq import notify_room
from moontour_common.models import BaseRoom

RoomType = TypeVar('RoomType', bound=BaseRoom)
ROOM_KEY_PREFIX = 'room:'

host = os.getenv('REDIS_HOST', 'redis')
redis_client = redis.Redis(host=host)


def get_room_key(room_id: str) -> str:
    return f'{ROOM_KEY_PREFIX}{room_id}'


@contextmanager
def room_lock(room_id: str):
    with redis_client.lock(f'room-{room_id}'):
        yield


def create_room(room: BaseRoom):
    redis_client.json().set(get_room_key(room.id), Path.root_path(), json.loads(room.json()))


def delete_room(room_id: str):
    redis_client.json().delete(get_room_key(room_id), Path.root_path())


def get_room(room_id: str, model: type[RoomType]) -> RoomType:
    room_dict = redis_client.json().get(get_room_key(room_id), Path.root_path())
    return model.parse_obj(room_dict)


def set_room(room: RoomType):
    redis_client.json().set(get_room_key(room.id), Path.root_path(), json.loads(room.json()))


@asynccontextmanager
async def modify_room(
        room_id: str,
        model: type[RoomType] = BaseRoom,
        notify: bool = True
) -> AsyncContextManager[RoomType]:
    assert model.get_mode() is not None  # Modifying abstract models will lead to unexpected results

    with room_lock(room_id):
        room = get_room(room_id, model)
        try:
            yield room
        except Exception:
            raise
        else:
            set_room(room)

            if notify:
                await notify_room(room)
