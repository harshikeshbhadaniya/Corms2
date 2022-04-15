import json
import csv
from csv import writer
import os
import numpy as np
import pandas as pd
from sklearn.utils import check_random_state

def update(project):
    dir = os.getcwd()
    st = dir+"/"+project+"/"+project+".csv"
    header_list = ["Author","Author_Name", "Subject","Project/Subproject","All Reviewers","Reviewers Name","Created","Closed At","File Info","URL","commit_url","Change_Size","status"]
    df = pd.read_csv(st, names=header_list,sep=';',encoding="unicode_escape")
    print(df.shape)
    sub = []
    closed_at= []
    reviewer = []
    file = []
    ch_size = []
    auth = []
    status = []
    countkey = 0
    op=0
    cl=0
    for item in df["All Reviewers"]:
        if(isinstance(item,str)):
            for key in eval(item):
                if(df['status'][countkey] == "open"):
                    op+=1
                else:
                    cl+=1
                sub.append(df['Project/Subproject'][countkey])
                file.append(df['File Info'][countkey])
                closed_at.append(df['Closed At'][countkey])
                auth.append(df['Author'][countkey])
                status.append(df['status'][countkey])
                ch_size.append(df['Change_Size'][countkey])
                reviewer.append(key)
        countkey+=1
    df2 = pd.DataFrame({"Author":auth,"Project/Subproject":sub,"Reviewer":reviewer,"Change_Size":ch_size,"File Info":file,"Subject":sub,"Closed At":closed_at,"status":status})
    df2.reset_index(drop=True)
    st = dir+"/"+project+"/corms_"+project+".csv"
    df2.to_csv(st,header = True,index=False,sep=";")
    return cl,op

def merge(project):
    dir = os.getcwd()
    st = dir+"/"+project+"/"+project+".csv"
    header_list = ["ID","Author","Author_Name", "Subject","Project/Subproject","All Reviewers","Reviewers Name","Created","Closed At","File Info","URL","commit_url","Change_Size","status"]
    df = pd.read_csv(st, names=header_list,encoding="unicode_escape")
    st = dir+"/"+project+"/"+project+".csv"
    df.to_csv(st,header=False,sep=';',index=False)

# merge("joyent")
cl,op=update("tensorflow")
print(cl)
print(op)
print(cl+op)