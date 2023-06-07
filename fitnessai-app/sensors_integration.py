from datastore import getSensorsCollection, getClient


def save_sensor_data_in_mongodb(result, id):
    client = getClient()
    collection = getSensorsCollection(client)
    # ref = {
    #     "training_id": id
    # }
    
    collection.insert_one(dict({"timestamp": ref, "training_type_field": result}))
