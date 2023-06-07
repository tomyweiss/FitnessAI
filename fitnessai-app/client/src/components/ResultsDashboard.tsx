import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Unstable_Grid2';
import { GetTrainingResults } from '../api/api'
import { AppState } from '../store/reducer';
import { HideRegister } from '../store/actions';
import { connect } from 'react-redux';
import MuiAlert, { AlertProps } from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import ReactPlayer from 'react-player'
import Divider from '@mui/material/Divider';

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(
    props,
    ref,
) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const bull = (
    <Box
      component="span"
      sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
    >
      •
    </Box>
);

class Metric {
    title!: string;
    mainText!: string;
    secondaryText!: string;
    result!: string;

    constructor(title: string, mainText: string, secondaryText: string, result: string){
        this.title = title;
        this.mainText = mainText;
        this.secondaryText = secondaryText;
        this.result = result;
    }
}

class Insight {
    name!: string;
    description!: string;
    how!: string;

    constructor(name: string, description: string, how: string){
        this.name = name;
        this.description = description;
        this.how = how;
    }
}

interface AppLocalState {
    trackingDescription: Metric,
    trackingRhythm: Metric,
    duration: 0,
    insights: Insight[]
}

export class ResultsDashboard extends React.PureComponent<any, AppLocalState> {
    componentDidMount(){
        GetTrainingResults("1", "1").then((res:any) => {
            const results = res.data;
            
            this.setState({
                trackingDescription: new Metric("Training", results["tracking_type"], results["tracking_type"], results["status"]),
                trackingRhythm: new Metric("Rhythm", results["rhythm"], "", results["rhythm_analysis"]),
                duration: results["duration"],
                insights: []
            })

            results["insights"].map((insight:any) => {
                debugger;
                this.setState({
                    insights: [...this.state.insights, new Insight(insight["name"], insight["description"], insight["how"])]
                })
            })
        }).catch(err => {
            console.log(err);
        })
    }

    render() {
        return (
            <div>
                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                    <Grid xs={5} />
                    <Grid xs={2} >
                        <h1>
                            Results Dashboard
                        </h1>
                    </Grid>
                    <Grid xs={5} />
                </Grid>
                    <Snackbar
                    open={false}
                    autoHideDuration={1000}
                >
                    <Alert severity="error">{""}</Alert>
                    </Snackbar>
                    <div style={{marginTop:"70px"}}>
                        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                            <Grid xs={2} />
                            <Grid xs={1}>
                                <Card sx={{ minWidth: 170 }}>
                                    <CardContent>
                                        <Typography sx={{ fontSize: 17, color: "blue" }} color="text.secondary" gutterBottom>
                                            { this.state?.trackingDescription?.title }
                                        </Typography>
                                        <Typography variant="h5" component="div">
                                            { this.state?.trackingDescription?.mainText }
                                        </Typography>
                                        <Typography color={this.state?.trackingDescription?.result === "Passed"? "green": "red"} variant="body2">
                                            {this.state?.trackingDescription?.result}!
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid xs={2} />
                            <Grid xs={1}>
                                <Card sx={{ minWidth: 170 }}>
                                    <CardContent>
                                        <Typography sx={{ fontSize: 17, color: "blue" }} color="text.secondary" gutterBottom>
                                            { this.state?.trackingRhythm?.title }
                                        </Typography>
                                        <Typography variant="h5" component="div">
                                            { this.state?.trackingRhythm?.mainText }
                                        </Typography>
                                        <Typography color={this.state?.trackingRhythm?.result === "Passed"? "green": "red"} variant="body2">
                                            { this.state?.trackingRhythm?.result }!
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid xs={2} />
                            <Grid xs={1}>
                                <Card sx={{ minWidth: 170 }}>
                                    <CardContent>
                                        <Typography sx={{ fontSize: 17, color: "blue" }} color="text.secondary" gutterBottom>
                                            Duration
                                        </Typography>
                                        <Typography variant="h5" component="div">
                                            {this.state?.duration}
                                        </Typography>
                                        <Typography variant="body2">
                                            (seconds)
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid xs={3} />
                        </Grid>
                    </div>
                    <Divider style={{marginTop:"30px"}}/>
                    <div style={{marginTop:"10px"}}>
                        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                            <Grid xs={5} />
                            <Grid xs={2} >
                                <h2>Training Insights</h2>
                            </Grid>
                           
                            <Grid xs={5} />
                        </Grid>
                    </div>
                    <div style={{marginTop:"10px"}}>
                        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                            <Grid xs={3} />
                            <Grid xs={6}>
                                <TableContainer>
                                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                                        <TableHead>
                                        <TableRow>
                                            <TableCell sx={{ backgroundColor: 'gray', color:"white", textAlign:"center" }}>Name</TableCell>
                                            <TableCell sx={{ backgroundColor: 'gray', color:"white", textAlign:"center" }}>Description</TableCell>
                                            <TableCell sx={{ backgroundColor: 'gray', color:"white", textAlign:"center" }}>How</TableCell>
                                        </TableRow>
                                        </TableHead>
                                        <TableBody>
                                        {this.state?.insights?.map((insight: Insight) => (
                                            <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">{insight.name}</TableCell>
                                            <TableCell align="center">{insight.description}</TableCell>
                                            <TableCell align="center">{insight.how}</TableCell>
                                            </TableRow>
                                        ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Grid>
                            <Grid xs={3} />
                        </Grid>
                        </div>
                    <Divider style={{marginTop:"30px"}}/>
                    <div style={{marginTop:"10px"}}>
                        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                            <Grid xs={4} />
                            <Grid xs={5} >
                                <h2>What is the best way to perform the training?</h2>
                            </Grid>
                           
                            <Grid xs={3} />
                        </Grid>
                    </div>
                    <div style={{marginTop:"10px"}}>
                        <Grid container>
                            <Grid xs={4} />
                            <Grid xs={5} >
                                <ReactPlayer
                                    className='react-player fixed-bottom'
                                    url= 'https://www.youtube.com/watch?v=baA5UxbCN1k'
                                    width='80%'
                                    height='600px'
                                    controls = {true}
                                />
                            </Grid>
                            <Grid xs={3} />
                        </Grid>
                    </div>
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
      
export default connect(mapState, mapDispatchToProps)(ResultsDashboard);