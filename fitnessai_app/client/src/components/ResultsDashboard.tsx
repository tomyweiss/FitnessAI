import React from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Unstable_Grid2';
import { GetTrainingResults, ResultsAvailable } from '../api/api'
import { AppState } from '../store/reducer';
import { connect } from 'react-redux';
import MuiAlert, { AlertProps } from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import ReactPlayer from 'react-player'
import Divider from '@mui/material/Divider';
import { Animation } from '@devexpress/dx-react-chart';
import { ArgumentAxis, ValueAxis, LineSeries, Chart } from '@devexpress/dx-react-chart-material-ui';
import Paper from '@mui/material/Paper';
import ClipLoader from "react-spinners/ClipLoader";

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(
    props,
    ref,
) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

 class ResultsDashboard extends React.PureComponent<any, any> {
    setTrainingType = () => {
        let trainingName, video = ""
        switch(this.state.training_type_field){
            case 1:
                trainingName = "Squat"
                video = "https://youtu.be/gcNh17Ckjgg"
                break
            case 0:
                trainingName = "Deadlift"
                video = "https://youtu.be/XxWcirHIwVo"
                break
            case 2:
                trainingName = "Bench Press" 
                video = "https://youtu.be/4Y2ZdHCOXok"
                break
            default:
                trainingName = "Unknown"
        }

        this.setState({trainingName: trainingName, video: video});
    }

    componentDidMount(){
        let interval = setInterval(() => {
            ResultsAvailable(this.props.trackingID).then((res:any) => {
                if (res){
                    GetTrainingResults(this.props.trackingID).then((res:any) => {
                        const results = res.data;
                        this.setState({
                            id: results._id.training_id,
                            CNN_result: results.CNN_result,
                            sarima_forecast: results.sarima_forecast,
                            sarima_history: results.sarima_history,
                            training_type_field: results.training_type_field,
                            finished: true
                        });

                        let graphResults:any = [];
                        results.sarima_forecast.map((item:any, index:number) => {
                            graphResults.push({arg1: index, val1: item})
                        })

                        results.sarima_history.map((item:any, index:number) => {
                            graphResults.push({arg2: index + results.sarima_forecast.length, val2: item})
                        })

                        this.setState({
                            graphResults: graphResults,
                        });
            
                        this.setTrainingType();
                    }).catch(err => {
                        console.log(err);
                    })

                    clearInterval(interval);
                }
            })
          }, 1000);
    }

    render() {
        return (
            <div>
                {
                    this.state?.finished?
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
                            <Grid xs={4} />
                            <Grid xs={1}>
                                <Card sx={{ minWidth: 170 }}>
                                    <CardContent>
                                        <Typography sx={{ fontSize: 17, color: "blue" }} color="text.secondary" gutterBottom>
                                             Training
                                        </Typography>
                                        <Typography variant="h5" component="div">
                                            { this.state?.trainingName }
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid xs={2} />
                            <Grid xs={1}>
                                <Card sx={{ minWidth: 170 }}>
                                    <CardContent>
                                        <Typography sx={{ fontSize: 17, color: "blue" }} color="text.secondary" gutterBottom>
                                            Training Status
                                        </Typography>
                                        <Typography color={this.state?.CNN_result === 1? "green": "red"} variant="h5">
                                           {this.state?.CNN_result === 1? "Correct": "Wrong"}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid xs={4} />
                        </Grid>
                    </div>
                    <Divider style={{marginTop:"30px"}}/>
                    <div style={{marginTop:"10px"}}>
                        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                            <Grid xs={4} />
                            <Grid xs={5} >
                                <h2>Training Analysis</h2>
                            </Grid>
                           
                            <Grid xs={3} />
                        </Grid>
                    </div>
                    <div style={{marginTop:"10px"}}>
                        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                            <Grid xs={4} />
                            <Grid xs={5} >
                                <Paper>
                                    <Chart
                                    data={this.state? this.state.graphResults? this.state.graphResults: []: []}
                                    >
                                    <ArgumentAxis />
                                    <ValueAxis />
                                    <LineSeries
                                        name="Training"
                                        valueField="val1"
                                        argumentField="arg1"
                                    />
                                    <LineSeries
                                        name="Forcast"
                                        valueField="val2"
                                        argumentField="arg2"
                                    />
                                    <Animation />
                                    </Chart>
                                </Paper>
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
                                    url= {this.state?.video}
                                    width='80%'
                                    height='600px'
                                    controls = {true}
                                />
                            </Grid>
                            <Grid xs={3} />
                        </Grid>
                    </div>
                    </div>:
                    <div>
                        <Grid container>
                            <Grid xs={5} />
                            <Grid xs={4} >
                            <h3 style={{marginTop:"300px"}}> Analyzing results... </h3>
                            <div className="sweet-loading">
                                <ClipLoader
                                    color={"blue"}
                                    loading={true}
                                    size={150}
                                    aria-label="Loading Spinner"
                                    data-testid="loader"
                                />
                            </div>
                            </Grid>
                            <Grid xs={3} />
                        </Grid>
                     </div>
                }
            </div>
            )
        } 
}

const mapState = (state: AppState) => ({
    trackingID: state.trackingID
})

const mapDispatchToProps = {}
      
export default connect(mapState, mapDispatchToProps)(ResultsDashboard);