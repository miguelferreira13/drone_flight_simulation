from datetime import datetime, timedelta

import config
import db
from generator import generate_objects
from world import World


def begin_simulation():

    conn = db.get_conn()

    world = World(min_x=config.MIN_X_KM,
                  max_x=config.MAX_X_KM,
                  min_y=config.MIN_Y_KM,
                  max_y=config.MAX_Y_KM)

    objects = generate_objects(start_time=config.START_TIME,
                               end_time=config.END_TIME,
                               number_of_objects=config.N_OBJECTS,
                               world=world)

    current_time = config.START_TIME
    while current_time <= config.END_TIME:
        for obj in objects:
            if not obj.active(current_time):
                continue
            obj.log(conn, current_time)
            obj.update(current_time)

        current_time += timedelta(milliseconds=config.LOG_RATE_MILISECONDS)

    conn.close()

if __name__ == '__main__':
    s = datetime.now()
    begin_simulation()
    e = datetime.now() - s
    print('execution time:', e.total_seconds())
