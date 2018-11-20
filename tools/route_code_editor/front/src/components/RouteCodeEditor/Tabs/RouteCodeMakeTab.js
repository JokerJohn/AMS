import React from 'react';


import {
  Card,
  CardTitle,
  CardText,
  CardActions,
  Button,
  List,
  ListItem,
  ListItemContent,
} from 'react-mdl';

import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';

import {connect} from "react-redux";
import * as RouteCodeEditorActions from "../../../redux/Actions/RouteCodeEditorActions";
import {bindActionCreators} from "redux";

import {steps} from '../../../model/Redux/Page/RouteCodeEditor'

class AdvanceOrBackComponent extends React.Component {

  confirm() {
    this.props.routeCodeEditorActions.setActiveStep(steps.advanceOrBack.nextStep)
  }

  setIsBack(event) {
    console.log(event);
    this.props.routeCodeEditorActions.setIsBack(event.target.value === "back");
  };

  render() {
    return (
      <Card shadow={0}
            style={{width: "100%", minHeight: "100px"}}>
        <CardTitle>
          Select Advance or Back
        </CardTitle>
        <CardActions border>
          <RadioGroup
            name="AdvanceOrBack"
            value={this.props.isBack ? "back" : "advance"}
            onChange={this.setIsBack.bind(this)}
          >
            <FormControlLabel value="advance" control={<Radio/>} label="Advance"/>
            <FormControlLabel value="back" control={<Radio/>} label="Back"/>
          </RadioGroup>
          <div style={{float: "right"}}>
            <Button onClick={this.confirm.bind(this)}>Confirm</Button>
          </div>
        </CardActions>
      </Card>
    )
  }
}
const mapStateAdvanceOrBack = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep(),
  isBack: state.routeCodeEditor.getIsBack()
});
const mapDispatchAdvanceOrBack = (dispatch) => ({
  routeCodeEditorActions: bindActionCreators(RouteCodeEditorActions, dispatch),
});
let AdvanceOrBack = connect(mapStateAdvanceOrBack, mapDispatchAdvanceOrBack)(AdvanceOrBackComponent);


class SelectStartPointComponent extends React.Component {

  confirm() {
    if(this.props.startPoint !== "") {
      this.props.routeCodeEditorActions.setActiveStep(steps.selectStartPoint.nextStep)
    }else{
      alert("Start point is not selected!");
    }
  }

  back() {
    this.props.routeCodeEditorActions.resetRouteCode()
  }

  render() {
    return (
      <Card shadow={0}
            style={{width: "100%", minHeight: "100px"}}>
        <CardTitle>
          Select Start Point
        </CardTitle>
        <CardText><strong>Selected Point ID: {this.props.startPoint}</strong></CardText>
        <CardActions border>
          <div style={{float: "right"}}>
            <Button onClick={this.back.bind(this)}>Back</Button>
            <Button onClick={this.confirm.bind(this)}>Confirm</Button>
          </div>
        </CardActions>
      </Card>

    )
  }
}
const mapStateSelectStartPoint = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep(),
  startPoint: state.routeCodeEditor.getStartPoint()
});
const mapDispatchSelectStartPoint = (dispatch) => ({
  routeCodeEditorActions: bindActionCreators(RouteCodeEditorActions, dispatch),
});
let SelectStartPoint = connect(mapStateSelectStartPoint, mapDispatchSelectStartPoint)(SelectStartPointComponent);


class SelectLaneComponent extends React.Component {

  confirm() {
    this.props.routeCodeEditorActions.setActiveStep(steps.selectLane.nextStep)
  }

  back() {
    this.props.routeCodeEditorActions.setActiveStep(steps.selectLane.previousStep)
  }

  getLaneList(laneList) {

    let resList = [];
    let key = 0;

    for (let lane of laneList) {
      if (laneList.hasOwnProperty(key)) {
        resList.push((
          <ListItem key={key}>
            <ListItemContent icon="navigation" key={key}>
              <strong>
                Lane ID: {lane}
              </strong>
            </ListItemContent>
          </ListItem>
        ));
        key += 1;
      }
    }
    return resList
  };

  render() {

    return (
      <Card shadow={0}
            style={{width: "100%", minHeight: "100px"}}>
        <CardTitle>
          Select Lane
        </CardTitle>
        <CardText>
          <List>
            {this.getLaneList(this.props.laneList)}
          </List>
        </CardText>
        <CardActions border>
          <div style={{float: "right"}}>
            <Button onClick={this.back.bind(this)}>Back</Button>
            <Button onClick={this.confirm.bind(this)}>Confirm</Button>
          </div>
        </CardActions>
      </Card>
    )
  }
}
const mapStateSelectLane = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep(),
  laneList: state.routeCodeEditor.getLaneList()
});
const mapDispatchSelectLane = (dispatch) => ({
  routeCodeEditorActions: bindActionCreators(RouteCodeEditorActions, dispatch),
});
let SelectLane = connect(mapStateSelectLane, mapDispatchSelectLane)(SelectLaneComponent);


class SelectEndPointComponent extends React.Component {

  confirm() {
    if(this.props.endPoint !== "") {
      this.props.routeCodeEditorActions.setActiveStep(steps.selectEndPoint.nextStep)
    }else{
      alert("End point is not selected!");
    }
  }

  back() {
    this.props.routeCodeEditorActions.setActiveStep(steps.selectEndPoint.previousStep)
  }

  render() {
    return (
      <Card shadow={0}
            style={{width: "100%", minHeight: "100px"}}>
        <CardTitle>
          Select End Point
        </CardTitle>
        <CardText><strong>Selected Point ID: {this.props.endPoint}</strong></CardText>
        <CardActions border>
          <div style={{float: "right"}}>
            <Button onClick={this.back.bind(this)}>Back</Button>
            <Button onClick={this.confirm.bind(this)}>Confirm</Button>
          </div>
        </CardActions>
      </Card>
    )
  }
}
const mapStateSelectEndPoint = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep(),
  endPoint: state.routeCodeEditor.getEndPoint()
});
const mapDispatchSelectEndPoint = (dispatch) => ({
  routeCodeEditorActions: bindActionCreators(RouteCodeEditorActions, dispatch),
});
let SelectEndPoint = connect(mapStateSelectEndPoint, mapDispatchSelectEndPoint)(SelectEndPointComponent);


class ResultComponent extends React.Component {

  reselect() {
    this.props.routeCodeEditorActions.resetRouteCode()
  }

  back() {
    this.props.routeCodeEditorActions.setActiveStep(steps.result.previousStep)
  }

  getResult(startPoint, laneList, endPoint) {

    let lastPoint = "";
    let laneString = "";
    for (const lane of laneList) {
      const points = lane.split('_');

      const [arrow, startIndex, endIndex] = this.props.isBack ? ["<", 1, 0] : [">", 0, 1];

      laneString += points[startIndex] + arrow;
      lastPoint = points[endIndex];
    }
    laneString += lastPoint;

    return startPoint + ":" + laneString + ":" + endPoint
  }

  render() {
    return (
      <Card shadow={0}
            style={{width: "100%", minHeight: "100px"}}>
        <CardTitle>
          Result
        </CardTitle>
        <CardText>
          <div style={{wordWrap: "break-word"}}>
            <strong>Result: {this.getResult(this.props.startPoint, this.props.laneList, this.props.endPoint)}</strong>
          </div>
        </CardText>
        <CardActions border>
          <div style={{float: "right"}}>
            <Button onClick={this.back.bind(this)}>Back</Button>
            <Button onClick={this.reselect.bind(this)}>Reselect</Button>
          </div>
        </CardActions>
      </Card>

    )
  }
}
const mapStateResult = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep(),
  isBack: state.routeCodeEditor.getIsBack(),
  startPoint: state.routeCodeEditor.getStartPoint(),
  laneList: state.routeCodeEditor.getLaneList(),
  endPoint: state.routeCodeEditor.getEndPoint()
});
const mapDispatchResult = (dispatch) => ({
  routeCodeEditorActions: bindActionCreators(RouteCodeEditorActions, dispatch),
});
let Result = connect(mapStateResult, mapDispatchResult)(ResultComponent);


class RouteCodeMakeTabs extends React.Component {

  constructor(props) {
    super(props);

    this.component = {
      advanceOrBack: {
        component: (<AdvanceOrBack/>),
      },
      selectStartPoint: {
        component: (<SelectStartPoint/>),
      },
      selectLane: {
        component: (<SelectLane/>),
      },
      selectEndPoint: {
        component: (<SelectEndPoint/>),
      },
      result: {
        component: (<Result/>),
      }
    };
  }

  getShowTab() {
    return this.component[this.props.activeStep].component
  }

  render() {
    return (
      <div>
        {this.getShowTab()}
      </div>

    );
  }
}

const mapState = (state) => ({
  activeStep: state.routeCodeEditor.getActiveStep()
});

const mapDispatch = (dispatch) => ({
  routeCodeEditorActions: bindActionCreators(RouteCodeEditorActions, dispatch),
});

export default connect(mapState, mapDispatch)(RouteCodeMakeTabs);