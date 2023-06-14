try: 
    from .Utils import *
    import mediapipe as mp
    import cv2
    import pandas as pd
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    from datetime import datetime
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from datetime import timedelta
    import os
    import matplotlib.pyplot as plt
except Exception as e:
    print(e)

def calc_decay(id,exercise):
    try:
        #Opens the camera and record a figure doing an excersice.
        data = {"dates" : [],
            "values" : [],
            "spike/deep": []
            }
        #truncates the 'Squat Downs' folder
        relative_path = r'C:\Users\mosac\Git Repositories\FitnessAI\fitnessai_app\models\data\Flexing OR Stretching'
        delete_folder(relative_path)
        folder_name = id
        image_number = 0
        directory = r'C:\Users\mosac\Git Repositories\FitnessAI\fitnessai_app\trainings'
        folder_name = os.path.join(directory, folder_name)
        file_names = []
        for filename in os.listdir(folder_name):
            file_names.append(filename)

        file_names.sort()

        for filename in file_names:
            f = os.path.join(folder_name, filename)
            # checking if it is a file
            
            if os.path.isfile(f):
                with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                    
                    #run over the images inside the folders
                    #takes every image and put it inside a frame,f=image
                    frame = cv2.imread(f, cv2.IMREAD_ANYCOLOR)#read the image to frame of cv2
                    
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#paint the pose
                    image.flags.writeable = False
                    
                    results = pose.process(image)#the picther with the scale and dots
                    
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)#change the color format
                    
                    #Extract landmarks
                    if results.pose_landmarks:
                        landmarks = results.pose_landmarks.landmark


                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                                )

                        if exercise != 'bench':
                            # Get coordinates
                            R1 = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                            R2 = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                            R3 = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                            #Visibility Extraction
                            R_V = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].visibility
                            

                            L1 = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                            L2 = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                            L3 = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                            #Visibility Extraction
                            L_V = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].visibility
                                
                        else:
                            # Get coordinates
                            R1 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                            R2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                            R3 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                            #Visibility Extraction
                            R_V = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility
                            

                            L1 = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                            L2 = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                            L3 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                            #Visibility Extraction
                            L_V = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility
                                
                        if R_V > L_V:
                            angle = calculate_angle(R1, R2, R3)
                        else:
                            angle = calculate_angle(L1, L2, L3)


                        avg_y = (landmarks[11].y + landmarks[13].y + landmarks[15].y)/3
                        

                        if exercise == 'deadlift':
                            max_0 = 165
                            min_0 = 135
                        elif exercise == 'squat':
                            max_0 = 160
                            min_0 = 110
                        else:
                            max_0 = 165
                            min_0 = 95


                        time = int(filename.split(".")[0])
                        # Convert milliseconds to datetime object
                        timestamp = datetime.fromtimestamp(time / 1000.0)

                        # Format the datetime object as a string
                        formatted_timestamp = timestamp.strftime("%H:%M:%S:%f")

                        if angle > max_0:
                            data["spike/deep"].append(1)
                            data["values"].append(1-avg_y)
                            data["dates"].append(formatted_timestamp)
                        elif angle < min_0:
                            data["spike/deep"].append(-1)
                            data["values"].append(1-avg_y)
                            data["dates"].append(formatted_timestamp)
                            path = relative_path + '/frame' + str(image_number) + '.jpg'
                            #cv2.imwrite(path, frame)
                            cv2.imwrite(path, image)
                        else:
                            data["spike/deep"].append(0)
                            data["values"].append(1-avg_y)
                            data["dates"].append(formatted_timestamp)

                    
                image_number+=1

        #sum = 0
        #for i in range(len(data)-1):
        #    d1 = datetime.strptime(data["dates"][i], "%H:%M:%S:%f")
        #    d2 = datetime.strptime(data["dates"][i+1], "%H:%M:%S:%f")
        #    delta = d2 - d1
        #    delta_ms = round(delta.microseconds,0) / 1000
        #    sum = sum + delta_ms
        #avg_ms = sum // len(data)-1
        #print(f"avg_ms is {avg_ms}")


        #insert missing rows, with spikes
        for i in range(100):
            d1 = datetime.strptime(data["dates"][-1], "%H:%M:%S:%f")
            #sum = d1 + timedelta(milliseconds=avg_ms)
            sum = d1 + timedelta(milliseconds=50)        
            data["dates"].append(datetime.strftime(sum,"%H:%M:%S:%f"))
            data["values"].append(0)
            data["spike/deep"].append(0)

        df = pd.DataFrame(data = data)

        lead = 10
        #calc the decay rate of the history
        res = calculate_decay_rate(df,exercise)
        res_df = pd.DataFrame(data = res)
        print(res_df)
        #add the 3 points between 2 points and the lead points to the future
        new = add_points(res_df["values"],lead)

        new_res_df = pd.DataFrame(data = new)

        res_df = new_res_df

        #Auto Arima To the dacay list
        train = res_df[1:-lead]
        test = res_df[-lead:]

        trend = []
        for i in range(lead -1):
            trend.append(lead -10 -i)


        train["values"].iloc[-4] = train["values"].iloc[-4]*0.8
        train["values"].iloc[-3] = train["values"].iloc[-4]*0.8
        train["values"].iloc[-2] = train["values"].iloc[-3]*0.8
        train["values"].iloc[-1] = train["values"].iloc[-2]*0.8


        model = SARIMAX(endog=train["values"], order=(5,1,5))
        model_fit = model.fit()

        trend = list(range(lead - 1, -1, -1))

        start = len(train["values"])
        end = len(train["values"]) + lead
        prediction = model_fit.predict(start, end, exogenous = trend,trend="t").rename("prediction")

        #negative numbers consider as zeros
        for i in range(len(prediction)):
            if prediction.iloc[i] < 0:
                prediction.iloc[i] = 0


        #ax = res_df["values"][1:].plot(legend=True,figsize=(16,8))
        #prediction.plot(legend=True)
        #print("issue plotting")
        #dates_to_plot = res_df["dates"][1:len(prediction)]

        #plt.plot(prediction)
        #plt.xlabel("Dates")
        #plt.ylabel("Values")
        #plt.title("Data Plot")
        #plt.show()


        
    except Exception as e:
        print(e)
    
    #the return type is a tuple of two pandas.series
    #(series,series)
    return   prediction.tolist(), res_df["values"][1:].tolist()

