# -*- coding: utf-8 -*-
import json
import csv
from multiprocessing.dummy import active_children
import cormstool.corms.active as active
import cormstool.corms.preprocess as process
import cormstool.corms.normalization as normalization
import cormstool.corms.ensemble_model as ensemble_model
import cormstool.corms.similarity_model as similarity_model
from cormstool.corms.clean import text_cleaning
import pandas as pd
import numpy as np

def main_controller(f,project_h,platform):
  proj_csv = "data/"+project_h+"/corms_"+project_h+".csv"
  if(platform=="gerrit"):
    header_list = ["Author", "Project/Subproject","Reviewer","Change_Size","File Info","Subject","Status"]
    df = pd.read_csv(proj_csv, names=header_list,sep=";",encoding="unicode_escape",skiprows=[0])
  else:
    header_list = ["Author","Project/Subproject","Reviewer","Change_Size","File Info","Subject","Closed At","status"]
    df = pd.read_csv(proj_csv, names=header_list, sep=';', encoding= 'unicode_escape',skiprows=[0])
    
  if(platform=="gerrit"):
    df,new_reviews,workload = process.process_gerrit(df,project_h)
    rev_act = active.gerrit_act(project_h)
  else:
    df,new_reviews,workload = process.process_github(df)
    rev_act = active.github_act(df,new_reviews)

  ensemble_model.model_train(df,new_reviews,project_h)
  new_review = json.load(f)

  author = new_review["author"]
  project = new_review["project"]
  subject = new_review["subject"]
  files = []
  for file in new_review["files"]:
    files.append(file["path"])

  final_score = similarity_model.measure(df,author,project,files)
  sub =  text_cleaning(subject)  
  # rev = ensemble_model.predict(sub,train_transformer,model_svm)
  rev = ensemble_model.predict_new(sub,project_h,df["Subject"])
  if rev[0] in final_score:
    final_score[rev[0]]+=1
  else:
    final_score[rev[0]]=1
  normalization.normalize_in_place(final_score)
  final_score = dict(sorted(final_score.items(), key=lambda item: item[1],reverse=True))

  inactive = dict()
  for key in rev_act:
    if key in final_score:
      if(rev_act[key]>12):
        inactive[key] = final_score[key]
        del final_score[key]

  ls = []
  i=0
  for k in final_score:
    i+=1
    ls.append(k)
    if i==10:
      break
    
  rev = []
  i=0
  for key in ls:
    i=i+1
    rev.append(findrev(str(key),project_h,rev_act,i,final_score[key],workload))
  
  inrev = []
  i=0
  for key in inactive:
    i=i+1
    inrev.append(findrev(str(key),project_h,rev_act,i,inactive[key],workload))
  return rev,platform,project_h,inrev

def findrev(number,project,rev_act,i,score,workload):
    csv_path = "cormstool/corms/files/"+project+"/fp_"+project+".csv"
    csv_file = csv.reader(open(csv_path, "r", encoding='utf-8'), delimiter=",")
    #loop through the csv list
    for row in csv_file:
        #if current rows 1st value is equal to input, print that row
        if number == row[0]:
          if(int(row[0]) in rev_act):
            act = str(rev_act[int(row[0])])+" months ago"
          else:
            act = "-"
          if(int(row[0]) in workload):
            work = str(workload[int(row[0])])
          else:
            work = "-"
          return [i,round(score*100,2),row[0],row[1],act,work]
    # return [str(number),"-","-","-"]

#url = "http://review.openstack.org/accounts/14826/detail"