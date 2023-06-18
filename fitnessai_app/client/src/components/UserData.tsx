import { useRef, useState, useCallback, useEffect } from "react";
import Webcam from "react-webcam";
import { TrackingResource, StartTracking, DeleteTraining, FinishTraining, AnalyzeTraining } from '../api/api';
import Grid from '@mui/material/Unstable_Grid2';
import Button from '@mui/material/Button';

const videoConstraints = {
  width: 800,
  height: 600,
  facingMode: "user"
};

const waitIntervalSeconds = 1;
const trackingIntervalSeconds = 3;

let trackingNumber = "";

export const UserData = (props:any, _:any) => {
  const [trainingStatus, setTrainingStatus] = useState<number>(0);
  const webcamRef = useRef<Webcam>(null);

  const capture = useCallback(() => {

    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      TrackingResource(props.params.userName, trackingNumber, imageSrc);
    }
  }, [webcamRef]);

  const getUserNAme = () => {
    return props.params.fullName
  };

  useEffect(() => {
    let interval = setInterval(() => {
      if (trackingNumber === ""){
        return;
      }

      if (props.getCounter() === 0){
        return;
      }

      capture();
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const waitUntilCountdown = () => {
    setTrainingStatus(1);

    const interval = setInterval(() => {
      if (props.getCounter() === 0){
        clearInterval(interval)
        StartTracking(props.params.userName).then((response:any) => {
          trackingNumber = response.data;
          props.setTrainingID(trackingNumber)
          setTrainingStatus(2);
          trackingCountdown();
        });

        return
      }

     props.setCounter(props.getCounter() -1);
    }, 1000);
  };

  const trackingCountdown = () => {
    props.setCounter(trackingIntervalSeconds);

    const interval = setInterval(() => {
      if (props.getCounter() === 0){
        clearInterval(interval);
        setTrainingStatus(3);
        FinishTraining(props.params.userName, trackingNumber);
        return;
      }

     props.setCounter(props.getCounter() -1);
    }, 1000);
  };

  const startTrackingTimer = () => {
    props.setCounter(waitIntervalSeconds);
    waitUntilCountdown();
  };

  const retakeTracking = () => {
    DeleteTraining(props.params.userName, trackingNumber).then(res => {
      startTrackingTimer();
    })
  };

  const moveToResults = () => {
    AnalyzeTraining(props.params.userName, trackingNumber).then(res => {
      props.setPageStatus(4);
    }).catch(err => {
      console.log(err);
    })
  };

  return (
    <>
      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid xs={5} container />
        <Grid xs={5} container>
          <h1> Welcome {getUserNAme()}! </h1>
        </Grid>
        <Grid xs={2} container />
      </Grid>
      <div style={{marginTop:"30px"}}>
        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
          <Grid xs={5} container />
          <Grid xs={4} container>
            {
              trainingStatus == 0? null:
              trainingStatus == 1?
                <h2> Tracking workout in { props.getCounter() } seconds... </h2>:
                trainingStatus == 2?
                <h2> Let's Go! Only { props.getCounter() } seconds left</h2>:
                trainingStatus == 3?
                <div>
                  <div className="row">
                    <h2> Finished tracking!</h2>
                  </div>
                 <div className="row">
                  <Button variant="outlined" onClick={retakeTracking}> Retake </Button> 
                  <Button variant="outlined" onClick={moveToResults}> Analyze </Button>
                </div>
                </div>:null
            }
          </Grid>
          <Grid xs={3} container />
        </Grid>
      </div>
      {
         trainingStatus == 0?
          <div style={{marginTop:"300px"}}>
            <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
              <Grid xs={5} container />
              <Grid xs={5} container>
                <Button variant="contained" onClick={startTrackingTimer}>Start A New Workout</Button> 
              </Grid>
              <Grid xs={2} container />
            </Grid>
          </div>:null
      }
      {
        trainingStatus == 1 || trainingStatus == 2?
          <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
            <Grid xs={4} container />
            <Grid xs={4} container>
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
              />
            </Grid>  
            <Grid xs={6} />
          </Grid>: null
      }
      {
         trainingStatus == 2?
          <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
            <Grid xs={11} />
            <Grid xs={1} container>
              <Button variant="outlined" onClick={retakeTracking}> Retake </Button> 
            </Grid>
          </Grid>:null
      }
    </>
  );
};