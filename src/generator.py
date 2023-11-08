import random
import uuid
from datetime import datetime, timedelta

import bezier
import numpy as np

import config
import util
from object import Object
from point import Point


def generate_objects(start_time, end_time, number_of_objects, world):
    objects = []

    for _ in range(number_of_objects):

        int_delta = end_time - start_time
        random_second = random.randrange(int_delta.total_seconds())

        object_id : hex = uuid.uuid4().hex
        x : float = random.randint(config.MIN_X_KM, config.MAX_X_KM)
        y : float = random.randint(config.MIN_Y_KM, config.MAX_Y_KM)
        speed : int = random.randint(config.MIN_SPEED_METERS_SECOND, config.MAX_SPEED_METERS_SECOND)
        payload = f"{random.randrange(16**100):30x}"

        position = Point(x, y)
        waypoint = util.generate_random_waypoint(position)
        destination = util.generate_random_destination(position)

        nodes = np.asfortranarray([
            [position.x, waypoint.x, destination.x],
            [position.y, waypoint.y, destination.y]
        ])

        bezier_curve = bezier.Curve(nodes, degree=2)
        bezier_len = bezier_curve.length

        created_time : datetime = start_time + timedelta(seconds=random_second)
        expire_time : datetime = created_time + timedelta(seconds=(bezier_len*1000)/speed)

        objects.append(
            Object(
                id=object_id,
                speed=speed,
                created_time=created_time,
                expire_time=expire_time,
                payload=payload,
                world=world,
                position=position,
                waypoint=waypoint,
                destination=destination,
                bezier_curve=bezier_curve,
                bezier_len=bezier_len
                )
            )

    return objects
