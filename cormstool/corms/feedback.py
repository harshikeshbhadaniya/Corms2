import pandas as pd
import csv
from csv import writer

def check(collection):
    feed_details = collection.find({})
    total = 0
    score = 0
    for r in feed_details:
        score+=r["score"]
        total+=1
    if(total!=0):
        accuracy = (score/total) * 100
    else:
        accuracy = 100
    return score,total,round(accuracy,2)

def update(feedback,score,total,collection,project):
    if feedback == "yes":
        sc=1
    elif feedback == "no":
        sc=0
    else:    
        sc=0.5
    total+=1
    score+=sc
    feed_details = {
        "project":project,
        "score":sc
    }
    collection.insert_many([feed_details])
    if(total!=0):
        accuracy = (score/total) * 100
    else:
        accuracy = 100
    return round(accuracy,2)