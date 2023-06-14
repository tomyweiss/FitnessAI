import Utils as u

import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
#from pmdarima import auto_arima
#from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import timedelta
import time
#import os
import matplotlib.pyplot as plt



#Name The Exercise
Exercise = 'squat'

#Opens the camera and record a figure doing an excersice.
data = {"dates" : [],
        "values" : [],
        "spike/deep": []
        }
samples = 0
time.sleep(5)

#truncates the 'Squat Downs' folder
relative_path = r'C:\Users\mosac\Git Repositories\FitnessAI\fitnessai_app\models\data\Flexing OR Stretching'
u.delete_folder(relative_path)


cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    counter = 0
    iter = 0
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #Extract landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark


            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )

            if Exercise != 'bench':
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
                angle = u.calculate_angle(R1, R2, R3)
            else:
                angle = u.calculate_angle(L1, L2, L3)
                
            counter+=1

                        # Visualize angle
            cv2.putText(image, str(angle), 
                            #tuple(np.multiply(L_knee, [1280, 720]).astype(int)), 
                            tuple(np.multiply(L2, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA

                                )
            if counter == 4:
                counter = 0
                iter += 1

            avg_y = (landmarks[11].y + landmarks[13].y + landmarks[15].y)/3

            if Exercise == 'deadlift':
                max_0 = 165
                min_0 = 135
            elif Exercise == 'squat':
                max_0 = 160
                min_0 = 110
            else:
                max_0 = 165
                min_0 = 95



            if angle > max_0:
                data["spike/deep"].append(1)
                data["values"].append(1-avg_y)
                data["dates"].append(datetime.today().strftime("%H:%M:%S:%f"))
            elif angle < min_0:
                data["spike/deep"].append(-1)
                data["values"].append(1-avg_y)
                data["dates"].append(datetime.today().strftime("%H:%M:%S:%f"))
                path = relative_path + '/frame' + str(samples) + '.jpg'
                samples+=1
                cv2.imwrite(path, frame)
                #cv2.imwrite(path, image)
            else:
                data["spike/deep"].append(0)
                data["values"].append(1-avg_y)
                data["dates"].append(datetime.today().strftime("%H:%M:%S:%f"))
        
            
            cv2.imshow('Mediapipe Feed', image)
            
            if ((cv2.waitKey(10) & 0xFF == ord('q')) | (iter == 100)):
                break

    cap.release()
    cv2.destroyAllWindows()

#to know the difference in ms between every frame
sum = 0
for i in range(len(data)-1):
    d1 = datetime.strptime(data["dates"][i], "%H:%M:%S:%f")
    d2 = datetime.strptime(data["dates"][i+1], "%H:%M:%S:%f")
    delta = d2 - d1
    delta_ms = round(delta.microseconds,0) / 1000
    sum = sum + delta_ms
avg_ms = sum // len(data)-1
print(f"avg_ms is {avg_ms}")


#insert missing rows, with spikes
for i in range(100):
    d1 = datetime.strptime(data["dates"][-1], "%H:%M:%S:%f")
    sum = d1 + timedelta(milliseconds=avg_ms)
    data["dates"].append(datetime.strftime(sum,"%H:%M:%S:%f"))
    data["values"].append(0)
    data["spike/deep"].append(0)

df = pd.DataFrame(data = data)
#Use of sarima with CF *FORECAST*
############## WITH SPIKES / DEEPS ##################
#train_df = df.iloc[:len(df)-100]
#test_df = df.iloc[len(df)-100:] 
#model = SARIMAX(endog=train_df["values"], order=(70,1, 0), exog=train_df["spike/deep"])
#res = model.fit()
#start = len(train_df)
#end = len(train_df) + len(test_df) -1
#prediction = res.predict(start, end,exog = test_df["spike/deep"]).rename("prediction")
#ax = df["values"].plot(legend=True,figsize=(16,8))
#prediction.plot(legend=True)

#forecast dots to the future
lead = 10
#calc the decay rate of the history


res = u.calculate_decay_rate(df,Exercise)
res_df = pd.DataFrame(data = res)

#add the 3 points between 2 points and the lead points to the future
new = u.add_points(res_df["values"],lead)
new_res_df = pd.DataFrame(data = new)

#Plot the data
#ax = new_res_df[5:].plot(legend=True,figsize=(16,8))
#ax.set_xlim([5,len(new_res_df)-lead])

res_df = new_res_df

#Auto Arima To the dacay list
train = res_df[1:-lead]
test = res_df[-lead:]

trend = []
for i in range(lead -1):
    trend.append(lead -10 -i)

#auto_arima(train["values"], exogenous = trend,trend="t").summary()



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

for i in range(len(prediction)):
    if prediction.iloc[i] < 0:
        prediction.iloc[i] = 0


ax = res_df["values"][1:].plot(legend=True,figsize=(16,8))
prediction.plot(legend=True)
print("issue plotting")
dates_to_plot = res_df["dates"][1:len(prediction)]

plt.plot(prediction)
plt.xlabel("Dates")
plt.ylabel("Values")
plt.title("Data Plot")
plt.show()


print(prediction)