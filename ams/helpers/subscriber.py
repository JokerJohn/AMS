#!/usr/bin/env python
# coding: utf-8

import yaml

from ams import AttrDict, logger
from ams.helpers import Topic, Event, Hook, Condition, Publisher
from ams.helpers import StateMachine as StateMachineHelper
from ams.structures import (
    EventLoop, Autoware, Vehicle, Dispatcher, AutowareInterface, TrafficSignal, TrafficSignalController, User
)


class Subscriber(object):

    @classmethod
    def get_request_get_config_topic(cls, to_target):
        return Topic.get_topic(
            from_target=None,
            to_target=to_target,
            categories=EventLoop.CONST.TOPIC.CATEGORIES.REQUEST_GET_CONFIG,
            use_wild_card=True
        )

    @classmethod
    def get_request_get_status_topic(cls, to_target):
        return Topic.get_topic(
            from_target=None,
            to_target=to_target,
            categories=EventLoop.CONST.TOPIC.CATEGORIES.REQUEST_GET_STATUS,
            use_wild_card=True
        )

    @classmethod
    def get_route_code_message_topic(cls, target_vehicle, target_autoware):
        return Topic.get_topic(
            from_target=target_vehicle,
            to_target=target_autoware,
            categories=Vehicle.CONST.TOPIC.CATEGORIES.ROUTE_CODE
        )

    @classmethod
    def get_state_cmd_topic(cls, target_vehicle, target_autoware):
        return Topic.get_topic(
            from_target=target_vehicle,
            to_target=target_autoware,
            categories=Vehicle.CONST.TOPIC.CATEGORIES.STATE_CMD
        )

    @classmethod
    def get_stop_route_point_message_topic(cls, target_vehicle, target_autoware):
        return Topic.get_topic(
            from_target=target_vehicle,
            to_target=target_autoware,
            categories=Vehicle.CONST.TOPIC.CATEGORIES.STOP_ROUTE_POINT
        )

    @classmethod
    def get_vehicle_schedule_topic(cls, target_dispatcher, target_vehicle):
        return Topic.get_topic(
            from_target=target_dispatcher,
            to_target=target_vehicle,
            categories=Dispatcher.CONST.TOPIC.CATEGORIES.SCHEDULE,
            use_wild_card=True
        )

    @classmethod
    def get_vehicle_event_topic(cls, target_dispatcher, target_vehicle):
        return Topic.get_topic(
            from_target=target_dispatcher,
            to_target=target_vehicle,
            categories=Dispatcher.CONST.TOPIC.CATEGORIES.EVENT,
            use_wild_card=True
        )

    @classmethod
    def get_user_event_topic(cls, target_dispatcher, target_user):
        return Topic.get_topic(
            from_target=target_dispatcher,
            to_target=target_user,
            categories=Dispatcher.CONST.TOPIC.CATEGORIES.EVENT,
            use_wild_card=True
        )

    @classmethod
    def get_current_pose_topic(cls, target_autoware, target_vehicle):
        return Topic.get_topic(
            from_target=target_autoware,
            to_target=target_vehicle,
            categories=AutowareInterface.CONST.TOPIC.CATEGORIES.CURRENT_POSE,
        )

    @classmethod
    def get_vehicle_location_topic(cls, target_autoware, target_vehicle):
        return Topic.get_topic(
            from_target=target_autoware,
            to_target=target_vehicle,
            categories=AutowareInterface.CONST.TOPIC.CATEGORIES.VEHICLE_LOCATION,
        )

    @classmethod
    def get_route_point_topic(cls, target_autoware, target_vehicle):
        return Topic.get_topic(
            from_target=target_autoware,
            to_target=target_vehicle,
            categories=AutowareInterface.CONST.TOPIC.CATEGORIES.ROUTE_POINT,
        )

    @classmethod
    def get_decision_maker_state_topic(cls, target_autoware, target_vehicle):
        return Topic.get_topic(
            from_target=target_autoware,
            to_target=target_vehicle,
            categories=AutowareInterface.CONST.TOPIC.CATEGORIES.DECISION_MAKER_STATE,
        )

    @classmethod
    def get_vehicle_config_topic(cls, target_vehicle):
        return Topic.get_topic(
            from_target=target_vehicle,
            categories=Vehicle.CONST.TOPIC.CATEGORIES.CONFIG,
            use_wild_card=True
        )

    @classmethod
    def get_vehicle_status_topic(cls, target_vehicle):
        return Topic.get_topic(
            from_target=target_vehicle,
            categories=Vehicle.CONST.TOPIC.CATEGORIES.STATUS,
            use_wild_card=True
        )

    @classmethod
    def get_traffic_signal_event_topic(cls, target_traffic_signal_controller, target_traffic_signal):
        return Topic.get_topic(
            from_target=target_traffic_signal_controller,
            to_target=target_traffic_signal,
            categories=TrafficSignalController.CONST.TOPIC.CATEGORIES.EVENT,
        )

    @classmethod
    def get_traffic_signal_cycle_topic(cls, target_traffic_signal_controller, target_traffic_signal):
        return Topic.get_topic(
            from_target=target_traffic_signal_controller,
            to_target=target_traffic_signal,
            categories=TrafficSignalController.CONST.TOPIC.CATEGORIES.CYCLE,
        )

    @classmethod
    def get_traffic_signal_schedule_topic(cls, target_traffic_signal_controller, target_traffic_signal):
        return Topic.get_topic(
            from_target=target_traffic_signal_controller,
            to_target=target_traffic_signal,
            categories=TrafficSignalController.CONST.TOPIC.CATEGORIES.SCHEDULE,
        )

    @classmethod
    def get_stop_signal_topic(cls, target_dispatcher, target_vehicle):
        return Topic.get_topic(
            from_target=target_dispatcher,
            to_target=target_vehicle,
            categories=Dispatcher.CONST.TOPIC.CATEGORIES.STOP_SIGNAL
        )

    @classmethod
    def on_request_get_config_message(cls, _client, user_data, topic, request_config_message):
        response_topic = Topic.get_response_topic(topic)
        message = Hook.get_response_config_message(
            user_data["kvs_client"], Topic.get_to_target(topic), request_config_message)
        user_data["pubsub_client"].publish(response_topic, message)

    @classmethod
    def on_request_get_status_message(cls, _client, user_data, topic, request_status_message):
        response_topic = Topic.get_response_topic(topic)
        message = Hook.get_response_status_message(
            user_data["kvs_client"], Topic.get_to_target(topic), request_status_message)
        user_data["pubsub_client"].publish(response_topic, message)

    @classmethod
    def on_route_code_message_publish_lane_array(cls, _client, user_data, _topic, route_code_message):
        route_code = route_code_message.body
        lane_array = user_data["maps_client"].route.generate_lane_array(route_code)
        set_flag = Hook.set_route_code_lane_array_id_relation(
            user_data["kvs_client"], user_data["target_autoware"], route_code, lane_array.id)
        if set_flag:
            user_data["ros_client"].publish(
                AutowareInterface.CONST.TOPIC.LANE_ARRAY, AttrDict.get_dict(lane_array),
                user_data["lane_array_structure"])

    @classmethod
    def on_lane_array(cls, _client, user_data, _topic, lane_array):
        decision_maker_state = Hook.get_decision_maker_state(user_data["kvs_client"], user_data["target_autoware"])
        if decision_maker_state.data.split("\n")[1] + "\n" in [
            Autoware.CONST.DECISION_MAKER_STATE.WAIT_ORDER,
            Autoware.CONST.DECISION_MAKER_STATE.DRIVING_MISSION_CHANGE
        ]:
            Hook.set_received_lane_array(user_data["kvs_client"], user_data["target_autoware"], lane_array)

    @classmethod
    def on_state_cmd(cls, _client, user_data, _topic, state_cmd):
        decision_maker_state = Hook.get_decision_maker_state(user_data["kvs_client"], user_data["target_autoware"])
        if state_cmd.data == Autoware.CONST.STATE_CMD.ENGAGE:
            if decision_maker_state.data.split("\n")[1] + "\n" in [
                Autoware.CONST.DECISION_MAKER_STATE.DRIVE_READY
            ]:
                Hook.set_state_cmd(user_data["kvs_client"], user_data["target_autoware"], state_cmd)
        elif state_cmd.data == Autoware.CONST.STATE_CMD.REQUEST_MISSION_CHANGE:
            if decision_maker_state.data.split("\n")[1] + "\n" in [
                Autoware.CONST.DECISION_MAKER_STATE.DRIVING
            ]:
                Hook.set_state_cmd(user_data["kvs_client"], user_data["target_autoware"], state_cmd)

        elif state_cmd.data == Autoware.CONST.STATE_CMD.RETURN_TO_DRIVING:
            if decision_maker_state.data.split("\n")[1] + "\n" in [
                Autoware.CONST.DECISION_MAKER_STATE.MISSION_CHANGE_SUCCEEDED,
            ]:
                Hook.set_state_cmd(user_data["kvs_client"], user_data["target_autoware"], state_cmd)
        elif state_cmd.data == Autoware.CONST.STATE_CMD.GOTO_WAIT_ORDER:
            if decision_maker_state.data.split("\n")[1] + "\n" in [
                Autoware.CONST.DECISION_MAKER_STATE.MISSION_ABORTED,
                Autoware.CONST.DECISION_MAKER_STATE.MISSION_COMPLETE,
            ]:
                Hook.set_state_cmd(user_data["kvs_client"], user_data["target_autoware"], state_cmd)
        else:
            Hook.set_state_cmd(user_data["kvs_client"], user_data["target_autoware"], state_cmd)

    @classmethod
    def on_state_cmd_publish(cls, _client, user_data, _topic, state_cmd):
        user_data["ros_client"].publish(
            AutowareInterface.CONST.TOPIC.STATE_CMD, state_cmd, user_data["state_cmd_structure"])

    @classmethod
    def on_stop_waypoint_index(cls, _client, user_data, _topic, stop_waypoint_index):
        Hook.set_stop_waypoint_index(
            user_data["kvs_client"], user_data["target_autoware"], stop_waypoint_index)

    @classmethod
    def on_route_point_message_publish_stop_waypoint_index(cls, _client, user_data, _topic, route_point_message):
        stop_waypoint_index = {
            "data": route_point_message.body.index
        }
        user_data["ros_client"].publish(
            AutowareInterface.CONST.TOPIC.STOP_WAYPOINT_INDEX, stop_waypoint_index,
            user_data["stop_waypoint_index_structure"])

    @classmethod
    def on_vehicle_schedule_message(cls, _client, user_data, _topic, schedule_message):
        if schedule_message.body.target != user_data["target_vehicle"]:
            return

        status = Hook.get_status(user_data["kvs_client"], user_data["target_vehicle"], Vehicle.Status)
        if status is not None and status.state in [
            Vehicle.CONST.STATE.WAITING_SCHEDULE
        ]:
            Hook.set_received_schedule(
                user_data["kvs_client"], user_data["target_vehicle"], schedule_message.body.schedule)

    @classmethod
    def on_vehicle_event_message(cls, _client, user_data, _topic, event_message):
        if event_message.body.target != user_data["target_vehicle"]:
            return
        status = Hook.get_status(user_data["kvs_client"], user_data["target_vehicle"], Vehicle.Status)
        event = event_message.body.event
        if event.name == Dispatcher.CONST.EVENT.END_NODE:
            if status is not None and status.state in [
                Vehicle.CONST.STATE.WAITING_EVENT,
            ]:
                Hook.set_event(user_data["kvs_client"], user_data["target_vehicle"], event)
        elif event.name == Dispatcher.CONST.EVENT.CHANGE_SCHEDULE:
            if status is not None and status.state in [
                Vehicle.CONST.STATE.WAITING_EVENT
            ]:
                Hook.set_event(user_data["kvs_client"], user_data["target_vehicle"], event)
        elif event.name == Dispatcher.CONST.EVENT.RETURN_TO_WAITING_EVENT:
            if status is not None and status.state in [
                Vehicle.CONST.STATE.REPLACING_SCHEDULE_SUCCEEDED,
                Vehicle.CONST.STATE.REPLACING_SCHEDULE_FAILED
            ]:
                Hook.set_event(user_data["kvs_client"], user_data["target_vehicle"], event)

    @classmethod
    def on_user_event_message(cls, _client, user_data, _topic, event_message):
        event = event_message.body.event
        if event.name == Dispatcher.CONST.EVENT.NOTICE:
            status = Hook.get_status(user_data["kvs_client"], user_data["target_user"], User.Status)
            status.target_vehicle = list(filter(lambda x: x.group == Vehicle.CONST.NODE_NAME, event.targets))[0]
            Hook.set_status(user_data["kvs_client"], user_data["target_user"], status)
        Hook.set_event(user_data["kvs_client"], user_data["target_user"], event)

    @classmethod
    def on_stop_signal_message(cls, _client, user_data, _topic, stop_signal_message):
        Hook.set_received_stop_signal(
            user_data["kvs_client"], user_data["target_vehicle"], stop_signal_message.body)

    @classmethod
    def on_current_pose(cls, _client, user_data, _topic, current_pose):
        Hook.set_current_pose(user_data["kvs_client"], user_data["target_vehicle"], current_pose)

    @classmethod
    def on_current_pose_publish(cls, _client, user_data, _topic, ros_message_object):
        current_pose = Autoware.ROSMessage.CurrentPose.new_data(**yaml.load(str(ros_message_object)))
        topic = Publisher.get_current_pose_topic(user_data["target_autoware"], user_data["target_vehicle"])
        user_data["pubsub_client"].publish(topic, current_pose)

    @classmethod
    def on_route_point_message(cls, _client, user_data, _topic, route_point_message):
        Hook.set_route_point(user_data["kvs_client"], user_data["target_vehicle"], route_point_message.body)

    @classmethod
    def on_vehicle_location_publish_route_point(cls, _client, user_data, _topic, ros_message_object):
        vehicle_location = Autoware.ROSMessage.VehicleLocation.new_data(**yaml.load(str(ros_message_object)))
        if vehicle_location.waypoint_index != -1:
            route_point = Hook.generate_route_point(
                user_data["kvs_client"], user_data["target_autoware"], vehicle_location)
            if route_point is not None:
                Publisher.publish_route_point(
                    user_data["pubsub_client"], user_data["target_autoware"], user_data["target_vehicle"], route_point)

    @classmethod
    def on_decision_maker_state(cls, _client, user_data, _topic, decision_maker_state):
        Hook.set_decision_maker_state(user_data["kvs_client"], user_data["target_vehicle"], decision_maker_state)

    @classmethod
    def on_decision_maker_state_update_state(cls, _client, user_data, _topic, decision_maker_state):
        vehicle_status = Hook.get_status(
            user_data["kvs_client"], user_data["target_vehicle"], Vehicle.Status)
        if vehicle_status is not None:
            vehicle_status.decision_maker_state = decision_maker_state
            vehicle_status.current_pose = Hook.get_current_pose(
                user_data["kvs_client"], user_data["target_vehicle"])
            vehicle_status.route_point = Hook.get_route_point(
                user_data["kvs_client"], user_data["target_vehicle"])
            if Hook.set_status(user_data["kvs_client"], user_data["target_vehicle"], vehicle_status):
                resource = StateMachineHelper.load_resource(user_data["state_machine_path"])
                state_machine_data = StateMachineHelper.create_data(resource)
                variables = {
                    "kvs_client": user_data["kvs_client"],
                    "pubsub_client": user_data["pubsub_client"],
                    "maps_client": user_data["maps_client"],
                    "target_vehicle": user_data["target_vehicle"],
                    "target_autoware": user_data["target_autoware"],
                    "target_dispatcher": user_data["target_dispatcher"],
                }
                if vehicle_status.state is not None:
                    StateMachineHelper.reset_state(state_machine_data, vehicle_status.state)
                StateMachineHelper.attach(
                    state_machine_data,
                    [
                        Hook.start_vehicle_event,
                        Hook.suspend_vehicle_event,
                        Hook.end_vehicle_event,
                        Hook.update_and_set_vehicle_pose,
                        Hook.update_vehicle_route_point,
                        Hook.initialize_vehicle_schedule,
                        Hook.initialize_vehicle_received_schedule,
                        Hook.initialize_received_stop_signal,
                        Hook.start_vehicle_schedule,
                        Hook.restart_vehicle_schedule,
                        Hook.replace_schedule,
                        Publisher.publish_vehicle_status,
                        Publisher.publish_route_code,
                        Publisher.publish_state_cmd,
                        Publisher.publish_stop_route_point,
                        Condition.on_vehicle_schedule,
                        Condition.on_vehicle_event,
                        Condition.vehicle_located,
                        Condition.vehicle_schedule_initialized,
                        Condition.vehicle_received_schedule_initialized,
                        Condition.received_stop_signal_initialized,
                        Condition.vehicle_route_point_updated,
                        Condition.vehicle_schedule_replaceable,
                        Condition.decision_maker_state_is_expected,
                        Condition.decision_maker_state_is_in_expected_states,
                        Condition.vehicle_location_is_ahead_event_route,
                        Condition.vehicle_location_is_on_event_route,
                        Condition.vehicle_location_is_behind_event_route,
                        Condition.vehicle_state_timeout,
                        Condition.vehicle_schedule_changed
                    ],
                    variables
                )

                event = Hook.get_event(user_data["kvs_client"], user_data["target_vehicle"])
                if event is not None:
                    if Hook.initialize_vehicle_event(user_data["kvs_client"], user_data["target_vehicle"]):
                        if StateMachineHelper.update_state(state_machine_data, event.name):
                            new_vehicle_status = Hook.get_status(
                                user_data["kvs_client"], user_data["target_vehicle"], Vehicle.Status)
                            if new_vehicle_status is not None and vehicle_status.state == new_vehicle_status.state:
                                new_vehicle_status.state = StateMachineHelper.get_state(state_machine_data)
                                new_vehicle_status.updated_at = Event.get_time()
                                Hook.set_status(
                                    user_data["kvs_client"], user_data["target_vehicle"], new_vehicle_status)
                                logger.info("Vehicle Event: {}, State: {} -> {}".format(
                                    event.name, vehicle_status.state, new_vehicle_status.state))
                                return

                event = None
                vehicle_schedule = Hook.get_schedule(user_data["kvs_client"], user_data["target_vehicle"])
                if vehicle_schedule is not None:
                    event = Event.get_event_by_id(vehicle_schedule.events, vehicle_status.event_id)
                if event is not None:
                    if StateMachineHelper.update_state(state_machine_data, event.name):
                        new_vehicle_status = Hook.get_status(
                            user_data["kvs_client"], user_data["target_vehicle"], Vehicle.Status)
                        if new_vehicle_status is not None and vehicle_status.state == new_vehicle_status.state:
                            new_vehicle_status.state = StateMachineHelper.get_state(state_machine_data)
                            new_vehicle_status.updated_at = Event.get_time()
                            Hook.set_status(
                                user_data["kvs_client"], user_data["target_vehicle"], new_vehicle_status)
                            logger.info("Vehicle Event: {}, State: {} -> {}".format(
                                event.name, vehicle_status.state, new_vehicle_status.state))
                            return

                update_flag = StateMachineHelper.update_state(state_machine_data, None)
                if vehicle_status.state is None or update_flag:
                    new_vehicle_status = Hook.get_status(
                        user_data["kvs_client"], user_data["target_vehicle"], Vehicle.Status)
                    if new_vehicle_status is not None and vehicle_status.state == new_vehicle_status.state:
                        new_vehicle_status.state = StateMachineHelper.get_state(state_machine_data)
                        new_vehicle_status.updated_at = Event.get_time()
                        Hook.set_status(user_data["kvs_client"], user_data["target_vehicle"], new_vehicle_status)
                        logger.info("Vehicle Event: {}, State: {} -> {}".format(
                            None, vehicle_status.state, new_vehicle_status.state))

    @classmethod
    def on_decision_maker_state_publish(cls, _client, user_data, _topic, ros_message_object):
        decision_maker_state = Autoware.ROSMessage.DecisionMakerState.new_data(**yaml.load(str(ros_message_object)))
        topic = Publisher.get_decision_maker_state_topic(user_data["target_autoware"], user_data["target_vehicle"])
        user_data["pubsub_client"].publish(topic, decision_maker_state)

    @classmethod
    def on_user_status_message(cls, _client, user_data, topic, user_status_message):
        user_data["target_user"] = Topic.get_from_target(topic)
        Hook.set_status(user_data["kvs_client"], user_data["target_user"], user_status_message.body)

    @classmethod
    def on_vehicle_config_message(cls, _client, user_data, topic, vehicle_config_message):
        user_data["target_vehicle"] = Topic.get_from_target(topic)
        Hook.set_config(user_data["kvs_client"], user_data["target_vehicle"], vehicle_config_message.body)

    @classmethod
    def on_vehicle_status_message(cls, _client, user_data, topic, vehicle_status_message):
        user_data["target_vehicle"] = Topic.get_from_target(topic)
        Hook.set_status(user_data["kvs_client"], user_data["target_vehicle"], vehicle_status_message.body)

    @classmethod
    def on_traffic_signal_event_message(cls, _client, user_data, _topic, event_message):
        if event_message.body.target != user_data["target_traffic_signal"]:
            return
        status = Hook.get_status(user_data["kvs_client"], user_data["target_traffic_signal"], TrafficSignal.Status)
        event = event_message.body.event
        if event.name == TrafficSignalController.CONST.EVENT.END_NODE:
            if status is not None and status.state in [
                TrafficSignal.CONST.STATE.WAITING_EVENT,
            ]:
                Hook.set_event(user_data["kvs_client"], user_data["target_traffic_signal"], event)

    @classmethod
    def on_traffic_signal_cycle_message(cls, _client, user_data, _topic, cycle_message):
        config = Hook.get_config(user_data["kvs_client"], user_data["target_traffic_signal"], TrafficSignal.Config)
        config.cycle = cycle_message.body.cycle
        Hook.set_config(user_data["kvs_client"], user_data["target_traffic_signal"], config)

    @classmethod
    def on_traffic_signal_schedule_message(cls, _client, user_data, _topic, schedule_message):
        Hook.set_received_schedule(
            user_data["kvs_client"], user_data["target_traffic_signal"], schedule_message.body.schedule)
