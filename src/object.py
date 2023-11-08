from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json
import bezier
import numpy as np


from world import World
from point import Point




@dataclass
class Object:
    id : str
    speed : int
    created_time : datetime
    expire_time : datetime
    payload : str
    world : World
    position : Point
    waypoint : Point
    destination : Point
    bezier_curve: bezier.Curve
    bezier_len: float

    angle : Optional[bool] = None
    expired : Optional[bool] = False

    def get_sector(self) -> str:
        return self.world.get_sector_by_coordinates(self.position.x, self.position.y)

    def active(self, current_time) -> bool :

        if not self.expire_time >= current_time:
            self.expired = True
        active = current_time >= self.created_time

        return active and not self.expired

    def log(self, conn, current_time):

        cursor = conn.cursor()

        json_data = json.dumps({
            "x":self.position.x,
            "y":self.position.y,
            "angle":self.angle,
            "speed":self.speed,
            "expire_time":self.expire_time.isoformat(),
            "created_time":self.created_time.isoformat()
        })

        cursor.execute(
            "INSERT INTO logs (timestamp, object_id, sector_id, payload, data) \
                VALUES (?, ?, ?, ?, ?)",
                       (current_time.isoformat(),
                       self.id,
                       self.get_sector(),
                       self.payload,
                       json_data)
                       )

        conn.commit()

    def update(self, current_time):
        seconds_since_creation = (current_time - self.created_time).total_seconds()
        distance_traveled_km = (self.speed * seconds_since_creation) / 1000

        # calculate the object's position on the quadratic bezier curve using the distance traveled
        t = distance_traveled_km / self.bezier_len

        # if it finished the traject then stop
        if t >= 1:
            self.expired = True
        np_arr = self.bezier_curve.evaluate(t)

        # calculate angle
        tangent_vector = self.bezier_curve.evaluate_hodograph(t)
        angle = np.arctan2(tangent_vector[1], tangent_vector[0])
        if angle < 0:
            angle += 2 * np.pi
        self.angle = angle[0]

        # update the object's position
        self.position.x = np_arr[0][0]
        self.position.y = np_arr[1][0]
