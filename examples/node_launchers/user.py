#!/usr/bin/env python
# coding: utf-8

import sys
import random
from time import time
from ams import Waypoint, Arrow, Route, Schedule
from ams.nodes import User

WAYPOINT_FILE = "../../res/waypoint.json"
ARROW_FILE = "../../res/arrow.json"


if __name__ == '__main__':

    host = "localhost"
    port = 1883
    name = "u1"
    path_waypoint_json = WAYPOINT_FILE
    path_arrow_json = ARROW_FILE

    if 1 < len(sys.argv):
        host = sys.argv[1]
    if 2 < len(sys.argv):
        port = int(sys.argv[2])
    if 3 < len(sys.argv):
        name = sys.argv[3]
    if 4 < len(sys.argv):
        path_waypoint_json = sys.argv[4]
    if 5 < len(sys.argv):
        path_arrow_json = sys.argv[5]

    waypoint = Waypoint()
    waypoint.load(path_waypoint_json)

    arrow = Arrow(waypoint)
    arrow.load(path_arrow_json)

    stop_waypoint_ids = [
        "8910", "8911", "8912", "8913", "8914", "8915", "8916", "8917", "8918", "8919", "8920", "8921", "8922", "8923",
        "8924", "8925", "8926",
        "9362", "9363", "9364", "9365", "9366", "9367", "9368", "9369", "9370", "9371", "9372", "9373", "9374", "9375",
        "9376", "9377",
        "8883", "8884", "8885", "8886", "8887", "8888", "8889", "8890", "8891", "8892", "8893", "8894", "8895", "8896",
        "8897",
        "9392", "9393", "9394", "9395", "9396", "9397", "9398", "9399", "9400", "9401", "9402", "9403", "9404",
        "10350", "10351", "10352", "10353", "10354", "10355", "10356", "10357", "10358", "10359", "10360", "10361",
        "10362", "10363", "10364", "10365", "10366", "10367", "10368", "10369", "10370", "10371", "10372", "10373",
        "10374",
        "9697", "9698", "9699", "9700", "9701", "9702", "9703", "9704", "9705", "9706", "9707", "9708",
        "8936", "8937", "8938", "8939", "8940", "8941", "8942", "8943", "8944", "8945", "8946", "8947", "8948", "8949",
        "8950", "8951", "8952", "8953", "8954", "8955", "8956", "8957", "8958", "8959", "8960", "8961", "8962", "8963",
        "8964", "8965", "8966", "8967", "8968",
    ]

    start_waypoint_id = random.choice(stop_waypoint_ids)
    start_arrow_code = arrow.get_arrow_codes_from_waypoint_id(start_waypoint_id)[0]
    start_time = time() - 5

    stop_waypoint_ids.remove(start_waypoint_id)

    goal_waypoint_id = random.choice(stop_waypoint_ids)
    goal_arrow_code = arrow.get_arrow_codes_from_waypoint_id(goal_waypoint_id)[0]

    trip_schedule = Schedule.get_schedule(
        User.ACTION.REQUEST, start_time, start_time+9999,
        Route.get_route(start_waypoint_id, start_waypoint_id, [start_arrow_code])
    )

    user = User(
        name=name,
        trip_schedules=[trip_schedule],
        dt=3.0
    )
    user.start(host=host, port=port)
