import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
from  xgboost import XGBClassifier
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle



def calculate_clssification(directory):
        #3 angale
        #every anagle creates from:a,b,c
        test = {
            'elbow': [],    
            'knee': [],    
            'shoulder': [],    
            'label': [] #The value of the character in terms of the X-axis
        }

        # Loop over all the images in images folder
        # 'C:\Users\Orel\Documents\GitHub\FitnessAI\images'
       # directory = r'C:\Users\mosac\Git Repositories\FitnessAI\Exercises Classification\for_test'

        # iterate over files in
        # that directory
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
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
                    
                    #Extract  the dots from the image,every dots contain x,y,z,visabillity and saved in arr
                    try:
                        landmarks = results.pose_landmarks.landmark
                    except:
                        pass
                    
                    # Get coordinates 
                    R_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    R_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    R_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    R_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    R_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    R_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    
                    # Visibility Extraction
                    R_K_V = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].visibility
                    R_E_V = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].visibility
                    R_S_V = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility + landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility
                    
                    
                    L_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    L_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    L_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    L_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    L_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    L_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    #Visibility Extraction
                    L_K_V = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].visibility
                    L_E_V = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility
                    L_S_V = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility + landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility
                        

                        # Calculate angles
                    if  R_K_V > L_K_V:
                        angle_K = calculate_angle(R_hip, R_knee, R_ankle)
                    else:
                        angle_K = calculate_angle(L_hip, L_knee, L_ankle)

                    if R_E_V > L_E_V:
                        angle_E = calculate_angle(R_shoulder, R_elbow, R_wrist)
                    else:
                        angle_E = calculate_angle(L_shoulder, L_elbow, L_wrist)
                    
                    if  R_S_V >  L_S_V:
                        angle_S = calculate_angle(R_elbow, R_shoulder, R_hip)
                    else:
                        angle_S = calculate_angle(L_elbow, L_shoulder, L_hip)
                

                #binary classification between d,s,b
                #ask in the folder give label by the name written in the image
            
            #add those angels values to the data array.
            test["elbow"].append(angle_E)
            test["knee"].append(angle_K)
            test["shoulder"].append(angle_S) 
            test["label"].append(0)

        df_test = pd.DataFrame(data=test)

        X_test = df_test.drop(['label'],axis=1) #3 angels
        y_test = df_test['label']


        try:
            filename = r'/Users/rotemcohen/FitnessAI/models/xgb_model.json'
            loaded_model = XGBClassifier()
            loaded_model.load_model(filename)

            # Use the loaded model for predictions
            xgb_predictions = loaded_model.predict(X_test)

        except Exception as e:
            print(e)

        print(xgb_predictions)

        # Perform majority vote
        deadlift_count = np.count_nonzero(xgb_predictions == 0)
        squat_count = np.count_nonzero(xgb_predictions == 1)
        bench_press_count = np.count_nonzero(xgb_predictions == 2)

        

        # Determine the output based on the majority
        if squat_count > deadlift_count and squat_count > bench_press_count:
            output = "squat"
            percent = squat_count
            to_return = 1
        elif deadlift_count > squat_count and deadlift_count > bench_press_count:
            output = "deadlift"
            percent = deadlift_count
            to_return = 0
        else:
            output = "bench press"
            percent = bench_press_count
            to_return = 2

        percent = (percent/ len(xgb_predictions) ) * 100

        #Print accuracy of train and test
        print(f"The Exercise that you preformed is: {output} in {round(percent, 2)}%")

        return to_return

