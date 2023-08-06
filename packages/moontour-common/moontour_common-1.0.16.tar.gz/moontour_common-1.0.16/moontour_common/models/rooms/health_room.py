from abc import ABC

from moontour_common.models.guess import Guess
from moontour_common.models.phase import HealthPhase
from moontour_common.models.rooms.room import BaseRoom

START_HEALTH = 5000


class HealthRoom(BaseRoom, ABC):
    start_health = START_HEALTH
    guess_duration: float = 15  # Time between first guess to phase ending
    phases: list[HealthPhase] = []
    guesses: list[dict[str, Guess]] = []  # User ID to guess
