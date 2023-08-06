from pydantic import validator

from moontour_common.models.rooms.health_room import HealthRoom, START_HEALTH
from moontour_common.models.rooms.room import RoomMode
from moontour_common.models.user import User


class DuelPlayer(User):
    health: int = START_HEALTH


class DuelRoom(HealthRoom):
    @staticmethod
    def get_mode() -> RoomMode:
        return RoomMode.duel

    player_count: int = 2
    players: list[DuelPlayer] = []
