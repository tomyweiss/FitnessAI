import ipdb
from datastore import getTrainingCollection, getClient, getResultCollection
import cv2
import numpy as np 
import base64

############################# training_type
squat = 0
deadlift=1
benchpress =2

#############################


# loads results from mongo(results collection)
def fetch_photos_from_mongodb(id):
    client = getClient()
    results = getTrainingCollection(client)

   # query photos by training id

    cursor = results.find({"_id.training_id": id})
    images = []
    print(cursor)
    for doc in cursor:
        for image in doc["images"]:
            np_arr = np.fromstring(base64.b64decode(image["content"]), np.uint8)
            images.append((np_arr, image["timestamp"]))

    return images


# result = 0/1/2
def save_results_xgboost_in_mongodb(result, id):
    client = getClient()
    collection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    
    collection.insert_one(dict({"_id": ref, "training_type_field": result}))



# result is in format: ([numbers],[numbers])
def save_results_sarima_in_mongodb(result, id):
    client = getClient()
    collection = getResultCollection(client)
    ref = {
        "training_id": id
    }

    doc = {"$set": {"sarima_result1": result[0], "sarima_result2": result[1]}}
    print(doc)
    res = collection.update_one(
         {"_id": ref}, doc)



# result is 0/1 (good/bad)
def save_results_CNN_in_mongodb(result, id):
    client = getClient()
    collection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    res = collection.update_one(
        {"_id": ref}, {"$set": {"CNN_result": result}})


def analyse_xgboost_photos(photos, id):
    # Omri& Rotem to implement xgboost(photos) that returns 0/1/2
    # ...
    # ...
    exercise = xgboost(photos)
    save_results_xgboost_in_mongodb(exercise, id)

    return exercise

def analyse_sarima_photos(photos, id):
    # Omri& Rotem to implement sarima(photos) that returns (list1, list2)
    # ...
    # ...
    save_results_sarima_in_mongodb(sarima(photos), id)

def analyse_CNN_photos(photos, id, exercise):
    # Omri& Rotem to implement CNN(photos) that returns 0/1
    # ...
    # ...
    save_results_CNN_in_mongodb(CNN(photos), id)


################################################################################################################################################

def analyse_xgboost_photos_mock(photos, id):
    exercise =1 
    save_results_xgboost_in_mongodb(exercise, id)
    
    return exercise

def analyse_sarima_photos_mock(photos, id):
    serima_mock = ([1, 1], [1,1])

    save_results_sarima_in_mongodb(serima_mock, id)

def analyse_CNN_photos_mock(photos, id, exercise):
    res =1
    save_results_CNN_in_mongodb(res, id)
