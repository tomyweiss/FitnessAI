import React from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Unstable_Grid2';
import { ShowLogin, SeShowRegister, PageState, LogOut, SetCounter } from '../store/actions';
import { connect } from 'react-redux';
import Box from '@mui/material/Box';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import HomeIcon from '@mui/icons-material/Home';
import Diversity3Icon from '@mui/icons-material/Diversity3';
import InfoIcon from '@mui/icons-material/Info';
import { AppState } from '../store/reducer';
import Fab from '@mui/material/Fab';

class AppFrame extends React.PureComponent<any, {}> {
    render() {
        return (
          <div style={{marginTop: "10px"}}>
            <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid xs={5} container />
              <Grid xs={5} container>
                <Box>
                  <BottomNavigation
                    showLabels
                    value={this.props.pageStatus}
                    onChange={(event, newValue) => {
                      this.props.pageState(newValue);
                    }}
                  >
                    <BottomNavigationAction label="Home" icon={<HomeIcon />} />
                    <BottomNavigationAction label="The team" icon={<Diversity3Icon />} />
                    <BottomNavigationAction label="About" icon={<InfoIcon />} />
                    {
                      this.props.loggedIn? <BottomNavigationAction label="User" icon={<InfoIcon />} />: null
                    }
                </BottomNavigation>
                </Box>
              </Grid>
              <Grid xs={2} container>
                {
                  this.props.loggedIn? 
                  <Grid container spacing={0.5}>
                    <Grid xs={6}>
                      <Fab variant="extended">
                        { this.props.user.fullName }
                      </Fab>
                    </Grid>
                    <Grid xs={6}>
                      <div style={{marginTop:"7px"}}>
                        <Button variant="contained" onClick={event => { this.props.logOut() }}> Logout </Button>
                      </div>
                    </Grid>
                  </Grid>: 
                  <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                    <Grid xs={6} container>
                      <Button variant="contained" onClick={event => {this.props.showLogin()}}>Login</Button> 
                    </Grid>
                    <Grid xs={6} container>
                      <Button variant="contained" onClick={event => {this.props.showRegister()}}>Register</Button>     
                    </Grid>
                  </Grid>
                }
              </Grid>
            </Grid>
          </div>
        )
    }
  }

const mapState = (state: AppState) => ({
  pageStatus: state.pageStatus,
  loggedIn: state.loggedIn,
  user: state.user
})

const mapDispatchToProps = {
  showLogin: ShowLogin,
  showRegister: SeShowRegister,
  pageState: PageState,
  logOut: LogOut,
  setCounter: SetCounter
}
  

export default connect(mapState, mapDispatchToProps)(AppFrame);