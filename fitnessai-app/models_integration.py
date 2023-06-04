import ipdb
from datastore import getTrainingCollection, getClient, getResultCollection


# loads results from mongo(results collection)
def fetch_photos_from_mongodb(id):
    client = getClient()
    results = getTrainingCollection(client)

   # query photos by training id
    cursor = results.find({})
    for doc in cursor:
        doc["images"][0]["timestamp"]

    # # images = // add casting from mongodb

    # Image.open(BytesIO(one_training["images"][1]["content"].encode('utf-8')))
    # image_bytes = base64.b64decode(base64_string)

    # Needed format is:
    #     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    #       run over the images inside the folders
    #       takes every image and put it inside a frame,f=image
    #       frame = cv2.imread(f, cv2.IMREAD_ANYCOLOR)#read the image to frame of cv2

    return [(frame1, timestamp), (frame2, timestamp, ...)]


# result = 0/1/2
def save_results_xgboost_in_mongodb(result, id):
    client = getClient()
    resultcollection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    res = resultcollection.update(
        {id_field: ref}, {"$set": {"training_type_field": result}})


# result is in format: ([numbers],[numbers])
def save_results_sarima_in_mongodb(result, id):
    client = getClient()
    resultcollection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    res = resultcollection.update(
        {id_field: ref}, {"$set": {"sarima_result": result}})


# result is 0/1 (good/bad)
def save_results_CNN_in_mongodb(result, id):
    client = getClient()
    resultcollection = getResultCollection(client)
    ref = {
        "training_id": id
    }
    res = resultcollection.update(
        {id_field: ref}, {"$set": {"CNN_result": result}})


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


# trigger models analysis after training
photos = fetch_photos_from_mongodb(id)
exercise = analyse_xgboost_photos(photos, id)
analyse_sarima_photos(photos, id)
analyse_CNN_photos(photos, id, exercise)
# display results in results page
