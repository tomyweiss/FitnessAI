import React from 'react';
import AppFrame from './AppFrame'
import LoginModal from './LoginModal'
import RegisterModal from './RegisterModal';
import mainFooter from '../assets/images/landing_page.png';
import solution from '../assets/images/solution.png';
import explanation from '../assets/images/explanation.png'
import humanSolutions from '../assets/images/human.png'
import team from '../assets/images/team.png'
import about from '../assets/images/about.png'
import Divider from '@mui/material/Divider';
import { AppState } from '../store/reducer';
import { connect } from 'react-redux';
import { UserData } from './UserData';
import ResultsDashboard from './ResultsDashboard';
import { SetCounter, PageState, LandingPageNumber, TeamPageNumber, AboutPageNumber, UserDataNumber, ResultsDashboardPage, SetTrainingID } from '../store/actions';

class LandingPage extends React.PureComponent<any, {}> {

  getCounter = () => {
    return this.props.counter
  }

  render() {
    return (
        <div>
           <AppFrame  />
           <LoginModal />
           <RegisterModal />
           {
            this.props.pageStatus == LandingPageNumber?
              <div>
                <img src={mainFooter} width="100%" style={{marginTop: "20px"}}/> 
                <Divider /> 
                <img src={solution} width="100%" style={{marginTop: "30px"}}/>
                <Divider /> 
                <img src={explanation} width="100%" style={{marginTop: "30px"}}/>
                <Divider />
                <img src={humanSolutions} width="100%" style={{marginTop: "30px"}}/>   
              </div>:
            this.props.pageStatus == TeamPageNumber?
              <img src={team} width="100%" style={{marginTop: "10px"}}/>: 
            this.props.pageStatus == AboutPageNumber?
              <img src={about} width="100%" style={{marginTop: "10px"}}/>:
            this.props.pageStatus == UserDataNumber?
              <UserData params={this.props.user} getCounter={this.getCounter} setCounter={this.props.setCounter} setPageStatus={this.props.setPageStatus} setTrainingID={this.props.setTrainingID} />:
            this.props.pageStatus == ResultsDashboardPage? 
              <ResultsDashboard />: null
           }
         </div>
    )
  } 
}

const mapState = (state: AppState) => {
  return {
    pageStatus: state.pageStatus,
    loggedIn: state.loggedIn,
    user: state.user,
    counter: state.counter
  }
}

const mapDispatchToProps = {
  setCounter: SetCounter,
  setPageStatus: PageState,
  setTrainingID: SetTrainingID
}

export default connect(mapState, mapDispatchToProps)(LandingPage);
