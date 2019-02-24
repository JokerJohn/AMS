export const REDUX = {
  ACTION_TYPE: {
    //Page
    //ScheduleEditor
    SET_MAP_DATA_SCHEDULE_EDITOR: 'setMapDataScheduleEditor',

    //Route Code Editor
    SET_ACTIVE_STEP_ROUTE_CODE_EDITOR: 'setActiveStepRouteCodeEditor',
    BACK_STEP_ROUTE_CODE_EDITOR: 'backStepRouteCodeEditor',
    SET_IS_BACK_ROUTE_CODE_EDITOR: 'setIsBackScheduleEditor',
    SET_START_POINT_ROUTE_CODE_EDITOR: 'setStartPointRouteCodeEditor',
    SET_LANE_LIST_ROUTE_CODE_EDITOR: 'setLaneListRouteCodeEditor',
    SET_END_POINT_ROUTE_CODE_EDITOR: 'setEndPointRouteCodeEditor',
    SET_START_POINT_AND_LANE_LIST_SCHEDULE_EDITOR:
      'setStartPointAndLaneListScheduleEditor',
    CLEAR_ROUTE_CODE_DATA: 'clearRouteCodeData',
    SAVE_ROUTE_CODE: 'saveRouteCode',
    SAVE_AND_ANOTHER_SELECT_ROUTE_CODE: 'saveAndAnotherSelectRouteCode',
    RESET_ROUTE_CODE: 'resetRouteCode',

    //Schedule Editor
    SET_SCHEDULE_EDITOR_ACTIVE_STEP: 'setScheduleEditorActiveStep',
    SER_CURRENT_ROUTE_CODE_SCHEDULE: 'setCurrentRouteCodeSchedule',
    SET_CHECKED_SEND_ENGAGE: 'setCheckedSendEngage',
    SET_WAIT_TIME: 'setWaitTime',
    DELETE_LATEST_CHANGE_ROUTE: 'deleteLatestChangeRoute',
    SAVE_SCHEDULE: 'saveSchedule',
    // Change Route Editor
    SET_CHANGE_ROUTE_ACTIVE_STEP_NEXT: 'setChangeRouteActiveStepNext',
    SET_CHANGE_ROUTE_ACTIVE_STEP_PREVIOUS: 'setChangeRouteActiveStepPrevious',
    SET_CHANGE_ROUTE_ACTIVE_STEP_RESET: 'setChangeRouteActiveStepReset',
    CANCEL_SELECT_CHANGE_ROUTE: 'cancelSelectChangeRoute',
    SET_ROUTE_CODE_AFTER_CHANGE_ROUTE: 'setRouteCodeAfterChangeRoute',
    SET_DECISION_SECTION_END_POINT: 'setDecisionSectionEndPoint',
    SAVE_CHANGE_ROUTE: 'saveChangeRoute',
    //Route Code List
    ADD_CONTINUE_ROUTE: 'addContinueRoute',
    DELETE_ROUTE_CODE_FROM_ROUTE_CODE_LIST_BY_INDEX:
      'deleteRouteCodeFromRouteCodeListByIndex',
    SET_SELECT_ROUTE_CODE_DISPLAY_MAIN_VIEWER:
      'setSelectRouteCodeDisplayMainViewer',
    ADD_ROUTE_CODE_BY_TEXT: 'addRouteCodeByText',

    //Schedule List
    DELETE_LATEST_SCHEDULE_FROM_SCHEDULE_LIST:
      'deleteLatestScheduleFromScheduleList',
    OPEN_ADD_SCHEDULE_MODAL_AND_EDIT_SCHEDULE:
      'openAddScheduleModalAndEditSchedule',
    SET_SELECT_SCHEDULE_DISPLAY_MAIN_VIEWER:
      'setSelectScheduleDisplayMainViewer',

    //Modal
    SET_IS_IMPORT_DATA_MODAL_OPEN: 'setIsImportDataModalModal',
    SET_IS_ADD_ROUTE_MODAL_OPEN: 'setIsAddRouteModalOpen',
    SET_IS_ADD_ROUTE_BY_TEXT_MODAL_OPEN: 'setIsAddRouteByTextModalOpen',
    SET_IS_ADD_SCHEDULE_MODAL_OPEN: 'setIsAddScheduleModalOpen'
  }
};