import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
from  xgboost import XGBClassifier
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import Ex_Classification_Methoods as m



directory = r'/Users/rotemcohen/FitnessAI/models/data/for_test'
m.calculate_clssification(directory)






   

