import mediapipe as mp
import cv2
import numpy as np
from  matplotlib import pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import xgboost as xgb
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import pickle as p

if __name__ == '__main__':
    
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle


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
    directory = r'C:\Users\mosac\Git Repositories\FitnessAI\Exercises Classification\for_test'
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
                except Exception as e:
                    print(f"An error occurred: {e}")
                
                # Get coordinates 
                R_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            