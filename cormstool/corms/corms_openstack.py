# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
import json
import csv
from token import LSQB
import numpy as np
from datetime import datetime
from cormstool.corms.active import activeness
from cormstool.corms.preprocess import process
import cormstool.corms.normalization as normalization
import cormstool.corms.ensemble_model as ensemble_model
import cormstool.corms.similarity_model as similarity_model
from cormstool.corms.clean import text_cleaning
import pandas as pd
    
def main_controller(f,project_h,platform):
  if(platform=="gerrit"):
    act_path = "cormstool/corms/files/"+project_h+"/reviewer_activeness.npy"
    proj_csv = "cormstool/corms/files/"+project_h+"/"+project_h+".csv"
    reviewer_activeness = np.load(act_path,allow_pickle='TRUE').item()
    rev_act = activeness(reviewer_activeness)

    header_list = ["Author", "Project/Subproject","Change_Size", "Final Reviewers","All Reviewers","File Info","Subject"]
    df = pd.read_csv(proj_csv, names=header_list)
    df,new_reviews = process(df)

    train_transformer,model_svm = ensemble_model.model_train(df,new_reviews)
    # f = open('cormstool/corms/files/sample.json',)
    new_review = json.load(f)

    author = new_review["author"]
    project = new_review["project"]
    subject = new_review["subject"]
    files = []
    for file in new_review["files"]:
        files.append(file["path"])

    final_score = similarity_model.measure(df,author,project,files)
    sub =  text_cleaning(subject)  
    rev = ensemble_model.predict(sub,train_transformer,model_svm)
    if rev in final_score:
      final_score[rev]+=1
    else:
      final_score[rev]=1
    normalization.normalize_in_place(final_score)
    final_score = dict(sorted(final_score.items(), key=lambda item: item[1],reverse=True))

    for key in rev_act:
      if key in final_score:
        if(rev_act[key]>12):
          del final_score[key]

    ls = []
    i=0
    for k in final_score:
      i+=1
      ls.append(k)
      if i==10:
        break
    
    rev = []
    for key in ls:
      rev.append(findrev(str(key),project_h))
    return rev,platform,project_h

def findrev(number,project):
    csv_path = "cormstool/corms/files/"+project+"/fp_"+project+".csv"
    csv_file = csv.reader(open(csv_path, "r", encoding='utf-8'), delimiter=",")
    #loop through the csv list
    for row in csv_file:
        #if current rows 1st value is equal to input, print that row
        if number == row[0]:
            return row
    # return [str(number),"-","-","-"]
# print("======")
# print("Actual assigned reviewers: ",new_reviews["Final Reviewers"][0])

#url = "http://review.openstack.org/accounts/14826/detail"