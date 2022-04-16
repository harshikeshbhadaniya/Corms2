from datetime import datetime
from dateutil import relativedelta
import numpy as np
def activeness(reviewer_activeness,plt):
    rev_act=dict()
    for key in reviewer_activeness:
        if plt=='gerrit':
            start_date = datetime.strptime(reviewer_activeness[key].split(".")[0], '%Y-%m-%d %H:%M:%S')
        else:
            start_date = datetime.strptime(reviewer_activeness[key].split(".")[0], '%Y-%m-%dT%H:%M:%SZ')
        end_date = datetime.now()
        num_months = relativedelta.relativedelta(end_date, start_date).months
        # num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        rev_act[int(key)] = num_months
    rev_act = dict(sorted(rev_act.items(), key=lambda item: item[1],reverse=True))
    return rev_act

def gerrit_act(project_h):
    act_path = "data/"+project_h+"/reviewer_activeness.npy"
    reviewer_activeness = np.load(act_path,allow_pickle='TRUE').item()
    rev_act = activeness(reviewer_activeness,'gerrit')
    return rev_act
    
def github_act(df,new_reviews):
    reviewer_activeness = dict()
    for i in range(df.shape[0]):
        last = df["Closed At"][i]
        if df['Reviewer'][i] in reviewer_activeness:
            if(reviewer_activeness[df['Reviewer'][i]] < last):
                reviewer_activeness[df['Reviewer'][i]]=last
        else:
            reviewer_activeness[df['Reviewer'][i]]=last
    
    for i in range(new_reviews.shape[0]):
        last = new_reviews["Closed At"][i]
        if new_reviews['Reviewer'][i] in reviewer_activeness:
            if(reviewer_activeness[new_reviews['Reviewer'][i]] < last):
                reviewer_activeness[new_reviews['Reviewer'][i]]=last
        else:
            reviewer_activeness[new_reviews['Reviewer'][i]]=last
    rev_act = activeness(reviewer_activeness,'github')
    return rev_act