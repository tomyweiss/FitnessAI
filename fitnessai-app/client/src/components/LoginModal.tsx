import React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Unstable_Grid2';
import Item from '@mui/material/ListItem';
import {Login} from '../api/api'
import { AppState } from '../store/reducer';
import { HideLogin, SetUserContext } from '../store/actions';
import { connect } from 'react-redux';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert, { AlertProps } from '@mui/material/Alert';

const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(
    props,
    ref,
) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

class LoginModal extends React.PureComponent<any, any> {
    state = {
        userName: "",
        password: "",
        showErrorDialog: false,
        errorMessage: ""
    };

    setErrorDialog = (res: { response: { data: string; }; }) => {
        this.setState({showErrorDialog: true, errorMessage:res.response.data});
    }

    login = () =>{
        Login(this.state.userName, this.state.password).then((res:any) => {
            if (res.status != 200){
                this.setErrorDialog(res);
                return;
            }

            this.props.setUserContext({
                userName: this.state.userName,
                fullName:res.data["fullName"],
                email:res.data["email"],
                height: res.data["height"],
                weight: res.data["weight"],
                sex: res.data["sex"],
                age: res.data["age"]
            });
        }).catch(res => {
            this.setState({error: "Error when trying to login"});
            return;
        })
    }

     render() {
        return (
            <div>
                <Snackbar
                    open={this.state.showErrorDialog}
                    autoHideDuration={6000}
                >
                    <Alert severity="error">{this.state.errorMessage}</Alert>
                 </Snackbar>
                <Modal
                    open={this.props.showModal}
                    onClose={() => {}}
                    aria-labelledby="modal-modal-title"
                    aria-describedby="modal-modal-description"
                >
                    <Box sx={style}>
                    
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                       Login
                    </Typography>
                    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                        <Grid xs={6}>
                            <Item>
                                <TextField id="standard-basic" label="User Name" variant="standard" 
                                onChange={ event => { this.setState({userName: event.target.value})} }/>
                            </Item>
                        </Grid>
                        <Grid xs={6} />
                        <Grid xs={6}>
                            <Item>
                                <TextField type="password" id="standard-basic" label="Password" variant="standard"
                                  onChange={ event => { this.setState({password: event.target.value})} }  />
                            </Item>
                        </Grid>
                        <Grid xs={6} />
                        <Grid xs={6} />
                        <Grid xs={3}>
                            <Button variant="contained" onClick={this.login}>Login</Button>
                        </Grid>
                        <Grid xs={3} >
                        <Button variant="text" onClick={event => {this.props.hideLogin()} }>Close</Button>
                        </Grid>
                    </Grid>
                    </Box>
                </Modal>
            </div>
          )
     } 
}

const mapState = (state: AppState) => ({
    showModal: state.showLoginModal
})

const mapDispatchToProps = {
    hideLogin: HideLogin,
    setUserContext: SetUserContext
}
      
export default connect(mapState, mapDispatchToProps)(LoginModal);