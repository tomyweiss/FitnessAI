from flask import Flask, json, request
from flask_cors import cross_origin, CORS
from datastore import getClient, getUserCollection, getTrainingCollection
import hashlib
import uuid
from models_integration import *

app = Flask(__name__)
CORS(app)

#############################################################################

user_name_field = "user_name"
training_id_field = "training_id"
image_hash_field = "image_hash"
password_field = "password"
name_field = "fullName"
age_field="age"
sex_field="sex"
height_field="height"
weight_field="weight"
training_status_field = "status"
images_field = "images"
id_field = "_id"
timestamp_field = "timestamp"

tracking_type_field = "tracking_type"
tracking_squat = "squat"
tracking_deadlift = "deadlift"
tracking_bench_press = "bench_press"

status_field = "status"
status_passed = "Passed"
status_failed = "Failed"

tracking_rhythm_analysis_field = "rhythm_analysis"
duration_field = "duration"

insights_fields = "insights"

#############################################################################

@app.route("/api/register", methods=["POST"])
@cross_origin()
def register():
    client = getClient()
    collection = getUserCollection(client)
    content = request.get_json()

    try:
        res = collection.insert_one({
            id_field: {
                user_name_field: content[user_name_field], 
            },
            user_name_field: content[user_name_field],
            password_field: getPasswordHash(content[password_field]),
            name_field: content[name_field],
            age_field: content[age_field],
            sex_field: content[sex_field],
            height_field: content[height_field],
            weight_field: content[weight_field]
        })

        return json.dumps(res.inserted_id),200,{'Content-Type':'application/json'}
    except Exception as e:
        return json.dumps(str(e)),500,{'Content-Type':'application/json'}

@app.route("/api/login", methods=["POST"])
@cross_origin()
def login():
    client = getClient()
    collection = getUserCollection(client)
    content = request.get_json()

    res = collection.find({ id_field : {
            user_name_field: content[user_name_field], 
        }})
 
    user = None
    for item in res:
        user = item

    if user is None:
        return json.dumps("User does not exist"),403,{'Content-Type':'application/json'}
    
    user[password_field] = ""

    return json.dumps(user),200,{'Content-Type':'application/json'}

@app.route("/api/start_tracking_training", methods=["POST"])
@cross_origin()
def start_tracking_training():
    client = getClient()
    content = request.get_json()
    user_name = content[user_name_field]
    training_id = str(uuid.uuid4())

    if validateUser(client, user_name) == False:
        return json.dumps("User does not exist"),403,{'Content-Type':'application/json'}
    
    trainingCollection = getTrainingCollection(client)
   
    ref = {
            training_id_field: training_id
     }
    
    trainingCollection.insert_one({
        id_field: ref,
        user_name_field: content[user_name_field],
        images_field:[],
        training_status_field: "In Progress"
    })

    return json.dumps(training_id),200,{'Content-Type':'application/json'}

@app.route("/api/track_training", methods=["POST"])
@cross_origin()
def track_training():
    client = getClient()
    content = request.get_json()
    user_name = content[user_name_field]
    training_id = content[training_id_field]
    image_hash = content[image_hash_field]
    timestamp = content[timestamp_field]

    if validateUser(client, user_name) == False:
        return json.dumps("User does not exist"),403,{'Content-Type':'application/json'}
    
    trainingCollection = getTrainingCollection(client)
    ref = {
        training_id_field: training_id
    }

    trainingCollection.update_one({id_field:ref}, {'$push': {images_field: {"content": image_hash, "timestamp":timestamp}}})

    return json.dumps(training_id),200,{'Content-Type':'application/json'}

@app.route("/api/delete_training", methods=["POST"])
@cross_origin()
def delete_training():
    client = getClient()
    content = request.get_json()
    user_name = content[user_name_field]
    training_id = content[training_id_field]

    if validateUser(client, user_name) == False:
        return json.dumps("User does not exist"),403,{'Content-Type':'application/json'}
    
    trainingCollection = getTrainingCollection(client)
    ref = {
        training_id_field: training_id
    }

    res = trainingCollection.delete_one({'_id':ref})    

    return json.dumps(res),200,{'Content-Type':'application/json'}


@app.route("/api/finish_training", methods=["POST"])
@cross_origin()
def finish_training():
    client = getClient()
    content = request.get_json()
    user_name = content[user_name_field]
    training_id = content[training_id_field]

    if validateUser(client, user_name) == False:
        return json.dumps("User does not exist"),403,{'Content-Type':'application/json'}
    
    trainingCollection = getTrainingCollection(client)
    ref = {
        training_id_field: training_id
    }

    res = trainingCollection.update_one({id_field:ref}, {"$set":{training_status_field:"Done"}})

    return json.dumps(""),200,{'Content-Type':'application/json'}

@app.route("/api/analyze", methods=["POST"])
@cross_origin()
def analyze():
    client = getClient()
    content = request.get_json()
    user_name = content[user_name_field]
    training_id = content[training_id_field]

    if validateUser(client, user_name) == False:
        return json.dumps("User does not exist"),403,{'Content-Type':'application/json'}
    
    photos = fetch_photos_from_mongodb(training_id)
    
    # exercise = analyse_xgboost_photos(photos, id)
    # analyse_sarima_photos(photos, id)
    # analyse_CNN_photos(photos, id, exercise)

    exercise = analyse_xgboost_photos_mock(photos, training_id)
    analyse_sarima_photos_mock(photos, training_id)
    analyse_CNN_photos_mock(photos, training_id, exercise)

    return json.dumps(""),200,{'Content-Type':'application/json'}

@app.route("/api/training_results", methods=["GET"])
@cross_origin()
def training_results():
    params = request.args.to_dict()
    user_name = params[user_name_field]
    training = params[training_id_field]

    return {
        user_name_field: user_name,
        training_id_field: training,
        status_field: status_passed,
        tracking_type_field: tracking_squat,
        tracking_rhythm_analysis_field: status_failed,
        duration_field: 90,
        insights_fields: [
            {
                "name": "xxx",
                "description": "xxx",
                "how": "xxx"
            },
            {
                "name": "xxx",
                "description": "xxx",
                "how": "xxx"
            },
            {
                "name": "xxx",
                "description": "xxx",
                "how": "xxx"
            }
        ]
    },200,{'Content-Type':'application/json'}


########################################################################################################################################################

def getPasswordHash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def validateUser(client, user_name):
    collection = getUserCollection(client)
   
    res = collection.find({ id_field : {
            user_name_field: user_name, 
        }})
 
    user = None
    for item in res:
        user = item

    if user is None:
        return False
    
    return True

########################################################################################################################################################

if __name__ == "__main__":
    app.run()
