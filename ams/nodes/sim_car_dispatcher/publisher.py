#!/usr/bin/env python
# coding: utf-8

from ams.nodes.dispatcher import Publisher as DispatcherPublisher
from ams.nodes.sim_car_dispatcher import CONST


class Publisher(DispatcherPublisher):

    DISPATCHER = CONST
