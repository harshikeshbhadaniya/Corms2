import pandas as pd
import csv
from csv import writer

def check():
    new_path = "cormstool/corms/files/results.csv"
    header_list = ["yes", "no","some", "total"]
    df = pd.read_csv(new_path, names=header_list)
    if df["total"][0] != 0:
        accuracy = ((df["yes"][0] + (0.5 * df["some"][0]))/df["total"][0]) * 100
    else:
        accuracy = (df["yes"][0] + (0.5 * df["some"][0])) * 100
    return df,round(accuracy,2)

def update(feedback,df):
    new_path = "cormstool/corms/files/results.csv"
    if feedback == "yes":
        df["yes"][0] += 1
    elif feedback == "no":
        df["no"][0] += 1
    else:    
        df["some"][0] += 1
    df["total"][0] += 1
    with open(new_path, 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow([df["yes"][0],df["no"][0],df["some"][0],df["total"][0]])
    if df["total"][0] != 0:
        accuracy = ((df["yes"][0] + (0.5 * df["some"][0]))/df["total"][0]) * 100
    else:
        accuracy = (df["yes"][0] + (0.5 * df["some"][0])) * 100
    return round(accuracy,2)