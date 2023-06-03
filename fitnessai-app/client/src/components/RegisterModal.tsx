import React, { useState } from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Unstable_Grid2';
import Item from '@mui/material/ListItem';
import {Register} from '../api/api'
import { AppState } from '../store/reducer';
import { HideRegister } from '../store/actions';
import { connect } from 'react-redux';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import MuiAlert, { AlertProps } from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';

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


class RegisterModal extends React.PureComponent<any, any> {
    state = {
        userName: "",
        password:"",
        repeatedPassword: "",
        age:0,
        sex: "",
        weight:0,
        height:0,
        fullName:"",
        error: ""
    };

    handleChange = (event: SelectChangeEvent) => {
        this.setState({sex: event.target.value});
    };

    register = () => {
        if (this.state.password !== this.state.repeatedPassword){
            this.setState({error: "Passwords do not match!"});
            return;
        }

        if (this.state.fullName === ""){
            this.setState({error: "Full name is mandatory"});
            return;
        }

        Register(this.state.userName, this.state.password, this.state.age, this.state.sex, this.state.height, this.state.weight, this.state.fullName).then((res:any) => {
            if (res.status != 200){
                this.setState({error: res.response.data});
                return;
            }

            this.props.hideRegister();
        }).catch(res => {
            this.setState({error: "Error when trying to register a new user"});
            return;
        })
    }

     render() {
        return (
            <div>
                 <Snackbar
                    open={this.state.error != ""}
                    autoHideDuration={1000}
                >
                    <Alert severity="error">{this.state.error}</Alert>
                 </Snackbar>
                <Modal
                    open={this.props.showModal}
                    onClose={() => {}}
                    aria-labelledby="modal-modal-title"
                    aria-describedby="modal-modal-description"
                >
                    <Box sx={style}>
                    
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                       Register a new user
                    </Typography>
                    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                        <Grid xs={6}>
                            <Item>
                                <TextField id="standard-basic" label="Full Name" variant="standard" 
                                onChange={ event => { this.setState({fullName: event.target.value})} }/>
                            </Item>
                            <Item>
                                <TextField id="standard-basic" label="User Name" variant="standard" 
                                onChange={ event => { this.setState({userName: event.target.value})} }/>
                            </Item>
                            <Item>
                                <TextField type="password" id="standard-basic" label="Password" variant="standard"
                                 onChange={ event => { this.setState({password: event.target.value})} }  />
                            </Item>
                            <Item>
                                <TextField type="password" id="standard-basic" label="Repeat Password" variant="standard"
                                 onChange={ event => { this.setState({repeatedPassword: event.target.value})} }  />
                            </Item>
                            <Item>
                                <TextField id="standard-basic" label="Age" variant="standard"
                                 onChange={ event => { this.setState({age: event.target.value})} }  />
                            </Item>
                            <Item>
                                <TextField id="standard-basic" label="Weight" variant="standard"
                                 onChange={ event => { this.setState({weight: event.target.value})} }  />
                            </Item>
                            <Item>
                                <TextField id="standard-basic" label="Height" variant="standard"
                                 onChange={ event => { this.setState({height: event.target.value})} }  />
                            </Item>
                            <Item>
                                <InputLabel id="demo-simple-select-label">Sex</InputLabel>
                                <Select
                                    labelId="Sex"
                                    id="demo-simple-select"
                                    label="Sex"
                                    onChange={this.handleChange}
                                    value={this.state.sex === ""? "Male": this.state.sex}
                                >
                                    <MenuItem value={"Male"}>Male</MenuItem>
                                    <MenuItem value={"Female"}>Female</MenuItem>
                                    <MenuItem value={"Other"}>Other</MenuItem>
                                </Select>
                            </Item>
                        </Grid>
                        <Grid xs={24} />
                        <Grid xs={6} />
                        <Grid xs={6} />
                        <Grid xs={6} />
                        <Grid xs={3}>
                            <Button variant="contained" onClick={this.register}>Register</Button>
                        </Grid>
                        <Grid xs={3} >
                            <Button variant="text" onClick={event => {this.props.hideRegister()} }>Close</Button>
                        </Grid>
                    </Grid>
                    </Box>
                </Modal>
            </div>
          )
     } 
}

const mapState = (state: AppState) => ({
    showModal: state.showRegisterModal
})

const mapDispatchToProps = {
    hideRegister: HideRegister
}
      
export default connect(mapState, mapDispatchToProps)(RegisterModal);