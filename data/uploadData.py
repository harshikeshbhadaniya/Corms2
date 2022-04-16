import pymongo
import urllib

def addproj(collection,proj,platform,url,desc):
    proj_details = {
        "platform":platform,
        "project":proj,
        "url":url,
        "description":desc,
        "status":1
    }
    collection.insert_many([proj_details])
    print(proj + " added successfully")

USERNAME = urllib.parse.quote_plus("php4954")
PASSWORD = urllib.parse.quote_plus("php4954")
DB_NAME = "mongodb+srv://"+USERNAME+":"+PASSWORD+"@devconnector.0n90j.mongodb.net/CORMS?retryWrites=true&w=majority"
client = pymongo.MongoClient(DB_NAME)
db = client['CORMS']
proj_collection = db["Projects"]
desc = "TensorFlow is a free and open-source software library for machine learning and artificial intelligence. It can be used across a range of tasks but has a particular focus on training and inference of deep neural networks"

addproj(proj_collection,"tensorflow","github","https://github.com/tensorflow/",desc)
