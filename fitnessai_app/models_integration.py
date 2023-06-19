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

############################# training_type #############################
squat = 0
deadlift = 1
benchpress = 2


##########################################################################


# load results from mongo(results collection)
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


def fetch_exercise(id):
    client = getClient()
    results = getResultCollection(client)

    return results.find_one({"_id.training_id": id})


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

    doc = {"$set": {"sarima_forecast": result[0], "sarima_history": result[1]}}
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
        {"_id": ref}, {"$set": {"CNN_result": result, "finished_analysis": True}})


def analyze_xgboost_photos(id):
    exercise = calculate_clssification_from_db(id)
    save_results_xgboost_in_mongodb(exercise, id)
    return exercise


def analyze_sarima_photos(id,exercise):
    if exercise == 1:
        return calc_decay(id,'squat')
    elif exercise == 0:
        return calc_decay(id,'deadlift')
    else:
        return calc_decay(id,'bench')


def analyze_CNN_photos(exercise):
    if exercise == 1:
        print('Analyze squat')
        test_squat()
    elif exercise == 0:
        print('Analyze deadlift')
        test_deadlift()
    else:
        print('Analyze Bench Press')
        test_bench()


######################################################  MOCKS  ###########################################################################


def analyse_xgboost_photos_mock(photos, id):
    exercise = 1
    save_results_xgboost_in_mongodb(exercise, id)

    return exercise


def analyse_sarima_photos_mock(photos, id):
    serima_mock = ([ 9.444444444444445,
    9.444444444444445,
    9.444444444444445,
    9.444444444444445,
    7.488095238095238,
    5.9904761904761905,
    4.792380952380952,
    3.833904761904762,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0], [4.658850522173462,
    4.594248306782087,
    4.008110706335094,
    3.140606635938724,
    0.8291887120713248,
    0,
    0,
    0,
    0,
    0,
    0])

    save_results_sarima_in_mongodb(serima_mock, id)


def analyse_CNN_photos_mock(photos, id, exercise):
    res = 1
    save_results_CNN_in_mongodb(res, id)
