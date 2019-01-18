import React from 'react';
import PropTypes from 'prop-types';

import connect from 'react-redux/es/connect/connect';

import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DoneIcon from '@material-ui/icons/Done';
import Typography from '@material-ui/core/Typography';

class ChangeRouteList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      listHeight: 0
    };
    this.selectRouteCode.bind(this);
  }

  getItems() {
    let currentEditChangeRouoteList = this.props.currentEditChangeRouteList;

    const resList = [];
    for (const item of currentEditChangeRouoteList) {
      resList.push(
        <ListItem button onClick={event => this.selectRouteCode(event, item)}>
          <ListItemIcon>
            <DoneIcon />
          </ListItemIcon>
          <ListItemText
            primary={
              <div>
                <Typography component="span" color="textPrimary">
                  Route Code After Change Route:{' '}
                  {item.routeCodeAfterChangeRoute.routeCode}
                </Typography>
                <Typography component="span" color="textPrimary">
                  Decision Section Route Code:{' '}
                  {item.decisionSectionRouteCode.routeCode}
                </Typography>
              </div>
            }
          />
        </ListItem>
      );
    }
    return resList;
  }

  selectRouteCode(event, item) {
    console.log(item);
  }

  render() {
    const routeListStyle = {
      overflowY: 'auto',
      height: '100%'
    };

    return <List style={routeListStyle}>{this.getItems()}</List>;
  }
}
ChangeRouteList.propTypes = {
  currentEditChangeRouteList: PropTypes.array
};
const mapStateSelectEndPoint = state => ({
  currentEditChangeRouteList: state.scheduleEditor.getCurrentEditChangeRouteList()
});
const mapDispatchSelectEndPoint = () => ({});
export default connect(
  mapStateSelectEndPoint,
  mapDispatchSelectEndPoint
)(ChangeRouteList);
