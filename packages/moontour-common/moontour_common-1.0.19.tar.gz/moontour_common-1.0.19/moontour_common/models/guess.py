from datetime import datetime

from pydantic import BaseModel, Field

from moontour_common.models import Coordinates
import geopy.distance


MAX_POINTS = 5000


class Guess(BaseModel):
    time: datetime = Field(default_factory=datetime.now)
    coordinates: Coordinates

    def get_points(self, target: Coordinates) -> int:
        distance = geopy.distance.geodesic(
            (target.latitude, target.longitude),
            (self.coordinates.latitude, self.coordinates.longitude)
        ).km
        return max(MAX_POINTS - int(distance), 0)
