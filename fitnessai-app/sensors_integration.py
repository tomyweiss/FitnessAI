from weakref import ref
from datastore import getSensorsCollection, getClient

# loads results from mongo(results collection)

def save_sensor_data_in_mongodb(result, id):
    client = getClient()
    collection = getSensorsCollection(client)
    # ref = {
    #     "training_id": id
    # }
    
    collection.insert_one(dict({"timestamp,number,pressure": ref, "training_type_field": result}))
