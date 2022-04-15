import json
import csv
from csv import writer
import os
import numpy as np
import pandas as pd
from sklearn.utils import check_random_state
def process(data,pro,ongoing_workload,change_workload,reviewer_activeness):
    closed=0
    opened=0
    dir = os.getcwd()
    st = dir+"/"+pro+"/"+pro+".csv"
    header_list = ["Author", "Project/Subproject","Change_Size", "Final Reviewers","All Reviewers","File Info","Subject","Status"]
    for i in data:
        if(i['status']=='MERGED' or i['status']=='CLOSED'):
            try:
                project = i['project']
                subject = i['subject']
                author = i['owner']['_account_id']
                all_reviewer =[]
                status="closed"
                change_size = i['insertions']+i['deletions']
                reviewer = []
                for rev in i['reviewers']['REVIEWER']:
                    all_reviewer.append(rev['_account_id'])
                for label in i['labels']:
                    if(label=='Code-Review'):
                        for tag in i['labels'][label]:
                            if(tag=='all'):
                                for cr in i['labels'][label][tag]:
                                    if(cr['value']!=0):
                                        key = cr['_account_id']
                                        if key in reviewer_activeness.keys():
                                            if(reviewer_activeness[key] < cr['date']):
                                                    reviewer_activeness[key]=cr['date']
                                        else:
                                            reviewer_activeness[key]=cr['date']
                                        reviewer.append(cr['_account_id'])
                #mine comments to get collaboration
                file_path = []
                for revision in i['revisions']:
                    for r in i['revisions'][revision]:
                        if(r=='files'):
                            for re in i['revisions'][revision][r]:
                                if re not in file_path:
                                    file_path.append(re)
                data_list = [str(author),str(project),str(change_size),str(reviewer),str(all_reviewer),file_path,str(subject),status ]
                if(not os.path.exists(st)):
                    with open(st, 'w', newline='') as f_object:
                        writer_object = writer(f_object)
                        writer_object.writerow(header_list)
                        f_object.close()
                with open(st, 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(data_list)
                    f_object.close()
                closed+=1
            except:
                continue
        if(i['status']=='OPEN' or i['status']=='NEW'):
            try:
                project = i['project']
                subject = i['subject']
                author = i['owner']['_account_id']
                all_reviewer =[]
                status="new"
                change_size = i['insertions']+i['deletions']
                reviewer = []
                for label in i['labels']:
                    if(label=='Code-Review'):
                        for tag in i['labels'][label]:
                            if(tag=='all'):
                                for cr in i['labels'][label][tag]:
                                    # all_reviewer.append(cr['_account_id'])
                                    reviewer.append(cr['_account_id'])
                if len(reviewer)!=0:
                    for rev in reviewer:
                        if rev not in change_workload:
                            change_workload[rev]=change_size
                            ongoing_workload[rev] = 1
                        else:
                            change_workload[rev] = change_workload [rev] + change_size
                            ongoing_workload[rev] = ongoing_workload[rev] + 1
                else:
                    continue
                all_reviewer=reviewer
                data_list = [str(author),str(project),str(change_size),str(reviewer),str(all_reviewer),file_path,str(subject),status ]
                if(not os.path.exists(st)):
                    with open(st, 'w', newline='') as f_object:
                        writer_object = writer(f_object)
                        writer_object.writerow(header_list)
                        f_object.close()
                with open(st, 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(data_list)
                    f_object.close()
                opened+=1
            except:
                continue
    return closed,opened
def start(project):
    ongoing_workload = dict()
    change_workload = dict()
    reviewer_activeness = dict()   
    dir = os.getcwd() 
    closed=0
    opened=0
    for i in range(0,19):
        a = i*100
        b = (i+1)*100 
        st = dir+"/"+project+'/change/'+project+'__'+str(a)+'_'+str(b)+'.json'
        if(os.path.exists(st)):
            f = open(st)
            data = json.load(f)
            cl,op=process(data,project,ongoing_workload,change_workload,reviewer_activeness)
            closed+=cl
            opened+=op
        else:
            print("error while loading " + st)
    onst = dir+"/"+project+"/ongoing_workload.npy"    
    chst = dir+"/"+project+"/change_workload.npy"
    rast = dir+"/"+project+"/reviewer_activeness.npy"
    np.save(onst, ongoing_workload)
    np.save(chst, change_workload)
    np.save(rast, reviewer_activeness)
    dir = os.getcwd()
    onst = dir+"/"+project+"/reviewer_activeness.npy"
    onw = np.load(onst,allow_pickle=True)
    print(onw)
    print("closed: ",closed)
    print("open: ",opened)
    print("total: ",closed+opened)

def update(project):
    dir = os.getcwd()
    st = dir+"/"+project+"/"+project+".csv"
    header_list = ["Author", "Project/Subproject","Change_Size", "Final Reviewers","All Reviewers","File Info","Subject","Status"]
    df = pd.read_csv(st, names=header_list,encoding="unicode_escape",skiprows=[0])
    print(df.shape)
    sub = []
    reviewer = []
    file = []
    ch_size = []
    auth = []
    status = []
    countkey = 0
    cl=0
    op=0
    for item in df["Final Reviewers"]:
        if(isinstance(item,str)):
            for key in eval(item):
                if(df['Status'][countkey]=="new"):
                    op+=1
                else:
                    cl+=1
                sub.append(df['Project/Subproject'][countkey])
                file.append(df['File Info'][countkey])
                status.append(df['Status'][countkey])
                auth.append(df['Author'][countkey])
                ch_size.append(df['Change_Size'][countkey])
                reviewer.append(key)
        countkey+=1
            
    df2 = pd.DataFrame({"Author":auth,"Project/Subproject":sub,"Reviewer":reviewer,"Change_Size":ch_size,"File Info":file,"Subject":sub,"Status":status})
    df2.reset_index(drop=True)
    st = dir+"/"+project+"/corms_"+project+".csv"
    df2.to_csv(st,header = True,index=False,sep=";")
    return cl,op

project="softwarefactory"
# start(project)
cl,op = update(project) 
print(cl)
print(op)
print(op+cl)       