import pandas as pd
import numpy as np
def process_github(df):
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df = df.reset_index(drop=True)
    
    sub = []
    closed_at= []
    reviewer = []
    file = []
    a_reviewers = []
    ch_size = []
    auth = []
    status = []
    countkey = 0
    for item in df["All Reviewers"]:
        for key in eval(item):
            sub.append(df['Project/Subproject'][countkey])
            file.append(df['File Info'][countkey])
            closed_at.append(df['Closed At'][countkey])
            a_reviewers.append(df['All Reviewers'][countkey])
            auth.append(df['Author'][countkey])
            status.append(df['status'][countkey])
            ch_size.append(df['Change_Size'][countkey])
            reviewer.append(key)
        countkey+=1
    df2 = pd.DataFrame({"Author":auth,"Project/Subproject":sub,"Reviewer":reviewer,"Change_Size":ch_size,"File Info":file,"Subject":sub,"Closed At":closed_at,"status":status,"All Reviewers":a_reviewers})
    df= df2

    df= df[df['Change_Size'] != 0]
    df = df.reset_index(drop=True)

    i = 0
    ls_r = []
    ongoing_workload = dict()
    for st in df['status']:
        if st=="open":
            ls_r.append(i)
            if df['Reviewer'][i] in ongoing_workload:
                ongoing_workload[df['Reviewer'][i]]=ongoing_workload[df['Reviewer'][i]]+1
            else:
                ongoing_workload[df['Reviewer'][i]]=1
        i=i+1

    df.drop(ls_r,axis=0,inplace=True)
    df = df.reset_index(drop=True)

    a = df.shape[0]
    x = int(0.2 * a)
    # df.to_csv('exr_openstack.csv')
    new_reviews = df.head(x)
    df = df.iloc[x: , :]
    df = df.reset_index(drop=True)
    return df,new_reviews,ongoing_workload

def process_gerrit(df,project):
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df = df.reset_index(drop=True)

    sub = []
    f_reviewers= []
    reviewer = []
    file = []
    a_reviewers = []
    ch_size = []
    auth = []
    countkey = 0
    for item in df["Final Reviewers"]:
        if(isinstance(item,str)):
            for key in eval(item):
                sub.append(df['Project/Subproject'][countkey])
                file.append(df['File Info'][countkey])
                f_reviewers.append(df['Final Reviewers'][countkey])
                a_reviewers.append(df['All Reviewers'][countkey])
                auth.append(df['Author'][countkey])
                ch_size.append(df['Change_Size'][countkey])
                reviewer.append(key)
        countkey+=1
            
    df2 = pd.DataFrame({"Author":auth,"Project/Subproject":sub,"Reviewer":reviewer,"Change_Size":ch_size,"File Info":file,"Subject":sub,"Final Reviewers":f_reviewers,"All Reviewers":a_reviewers})
    df= df2
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df = df.reset_index(drop=True)
    a = df.shape[0]
    x = int(0.2 * a)
    # df.to_csv('exr_openstack.csv')
    new_reviews = df.head(x)
    df = df.iloc[x: , :]
    df = df.reset_index(drop=True)
    workload_path = "cormstool/corms/files/"+project+"/ongoing_workload.npy"
    workload = np.load(workload_path,allow_pickle='TRUE').item()
    return df,new_reviews,workload