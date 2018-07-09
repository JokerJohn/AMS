#!/usr/bin/env python
# coding: utf-8

from ams import get_namedtuple_from_dict


topic = {
    "CATEGORIES": {
        "CONFIG": ["config"],
        "STATUS": ["status"],
        "GEOTOPIC": ["geotopic"]
    }
}

mission_event = {
    "START_MISSION": "start_mission",
    "END_MISSION": "end_mission"
}

event = {
    "START": "start",
    "INITIALIZE": "initialize",
    "ACTIVATE": "activate",
    "DEACTIVATE": "deactivate",
    "END": "end"
}
event.update(mission_event)

state = {
    "START_PROCESSING": "start_processing",
    "INITIALIZED": "initialized",
    "ACTIVE": "active",
    "MISSION_STARTED": "mission_started",
    "MISSION_ENDED": "mission_ended",
    "INACTIVE": "inactive",
    "END_PROCESSING": "end_processing"
}

const = {
    "NODE_NAME": "vehicle",
    "TOPIC": topic,
    "EVENT": event,
    "STATE": state,
    "MISSION_EVENTS": mission_event.values(),
    "ACTIVATION_REQUEST_TIMEOUT": 10.0
}

CONST = get_namedtuple_from_dict("CONST", const)
