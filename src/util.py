import math
import random

import config
from point import Point


def generate_random_destination(point : Point):
    while True:
        # generate a random distance within the specified range
        distance = random.uniform(config.DESTINATION_MIN_DIST_KM, config.DESTINATION_MAX_DIST_KM)

        # generate a random angle
        angle = random.uniform(0, 2 * math.pi)

        # calculate the potential coordinates
        new_x = point.x + distance * math.cos(angle)
        new_y = point.y + distance * math.sin(angle)

        # check if the new coordinates are within the world bounds
        if (config.MIN_X_KM <= new_x <= config.MAX_X_KM) \
            and (config.MIN_Y_KM <= new_y <= config.MAX_Y_KM):
            return Point(new_x, new_y)

def generate_random_waypoint(point : Point):
    while True:
        # generate a random distance within the specified range
        distance = random.uniform(config.WAYPOINT_MIN_DIST_KM, config.WAYPOINT_MAX_DIST_KM)

        # generate a random angle
        angle = random.uniform(0, 2 * math.pi)

        # calculate the potential coordinates
        new_x = point.x + distance * math.cos(angle)
        new_y = point.y + distance * math.sin(angle)

        # check if the new coordinates are within the world bounds
        if (config.MIN_X_KM <= new_x <= config.MAX_X_KM) \
            and (config.MIN_Y_KM <= new_y <= config.MAX_Y_KM):
            return Point(new_x, new_y)
