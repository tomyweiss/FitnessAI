import ipdb
from datastore import getTrainingCollection, getClient, getResultCollection
import cv2
import numpy as np 
import base64

from models.Ex_Classification_Methoods import calculate_clssification_from_db
from models.Sarimax import calc_decay
from models.Squat_majority import test_squat
from models.Dedlift_majority import test_deadlift
from models.Bench_majority import test_bench




############################# training_type
squat = 0
deadlift = 1
benchpress = 2

#############################

########################## XGBOOST ########################## 
# result = 0/1/2
def save_results_xgboost_in_mongodb(result, id):
    client = getClient()
    collection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    collection.insert_one(dict({"_id": ref, "training_type_field": result}))
    print("XGBOOST results have been saved to the DataBase successfully")


def analyze_xgboost_photos(id):
    exercise = calculate_clssification_from_db(id)
    save_results_xgboost_in_mongodb(exercise, id)
    return exercise

########################## XGBOOST ########################## 

########################## SARIMAX ########################## 


def analyze_sarima_photos(id,exercise):
    if exercise == 1:
        return calc_decay(id,'squat')
    elif exercise == 0:
        return calc_decay(id,'deadlift')
    else:
        return calc_decay(id,'bench')


# result is in format: ([numbers],[numbers])
def save_results_sarima_in_mongodb(result, id):
    client = getClient()
    collection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    doc = {"$set": {"sarima_history": result[0], "sarima_forecast": result[1]}}
    res = collection.update_one(
         {"_id": ref}, doc)
    print("Sarimax results have been saved to the DataBase successfully")


########################## SARIMAX ##########################

########################## CNN ##########################
# result is 0/1 (good/bad)
def save_results_CNN_in_mongodb(result, id):
    client = getClient()
    collection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    res = collection.update_one(
        {"_id": ref}, {"$set": {"CNN_result": result, "finished_analysis": True}})
    

def analyze_CNN_photos(exercise, id):
    if exercise == 1:
        print('Analyze squat')
        result = test_squat()
    elif exercise == 0:
        print('Analyze deadlift')
        result = test_deadlift()
    else:
        print('Analyze Bench Press')
        result = test_bench()
    save_results_CNN_in_mongodb(result, id)
    

########################## CNN ##########################

def fetch_exercise(id):
    client = getClient()
    results = getResultCollection(client)

    return results.find_one({"_id.training_id": id})