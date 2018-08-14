#!/usr/bin/env python
# coding: utf-8

from ams.nodes.dispatcher import StateMachine as DispatcherStateMachine
from ams.nodes.autoware import CONST as AUTOWARE
from ams.nodes.autoware_dispatcher import CONST, Structure, Helper, Publisher


class Condition(DispatcherStateMachine.Transition.Condition):

    Helper = Helper


class BeforeHook(DispatcherStateMachine.Transition.BeforeHook):

    Helper = Helper
    Publisher = Publisher


class AfterHook(DispatcherStateMachine.Transition.AfterHook):

    Helper = Helper
    Publisher = Publisher


class Transition(DispatcherStateMachine.Transition):

    DISPATCHER = CONST
    Helper = Helper
    Condition = Condition
    BeforeHook = BeforeHook
    AfterHook = AfterHook

    VEHICLE = AUTOWARE


class StateMachine(DispatcherStateMachine):

    DISPATCHER = CONST
    Structure = Structure
    Helper = Helper
    Transition = Transition

    VEHICLE = AUTOWARE
