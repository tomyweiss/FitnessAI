from pymongo import MongoClient

dataBaseName = "fitness-db"
usersDBTable = "users"
trainingDBTable = "training"
dataBaseURL ="localhost"
dataBasePort = "27017"

def getClient():
    return MongoClient("mongodb://" + dataBaseURL+":"+dataBasePort+"/")

def getUserCollection(client):
    db = client[dataBaseName]
    return db[usersDBTable]


def getTrainingCollection(client):
    db = client[dataBaseName]
    return db[trainingDBTable]