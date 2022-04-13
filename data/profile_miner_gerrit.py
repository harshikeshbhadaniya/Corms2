import numpy as np
import csv
from csv import writer
from Miner import *
import pandas as pd
import os

def make_profile(project):
    dir = os.getcwd()
    csv_path = dir+"/"+project+"/profiles_"+project+".csv"
    reviewer_path = dir+"/"+project+"/reviewer_activeness.npy"
    # print(reviewer_path)
    f = np.load(reviewer_path,allow_pickle=True)
    d = f.tolist()
    # print(d)
    for key in d:
        data_list = [str(key)]
        # print(data_list)
        with open(csv_path, 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data_list)
            f_object.close()
    
def load_profiles(miner: Miner,project):
    dir = os.getcwd()
    csv_path = dir+"/"+project+"/profiles_"+project+".csv"
    profile_path = dir+"/"+project+"/profiles/"
    # create the profiles list before calling this batch profile loading
    colnames=['account_id'] 
    df = pd.read_csv(csv_path, names=colnames, header=None)
    ids = df['account_id'].values
    for account_id in ids:
        miner.profile_mine(account_id=account_id,timeout=120)

def update_profile(project):
    dir = os.getcwd()
    csv_path = dir+"/"+project+"/fp_"+project+".csv"
    reviewer_path = dir+"/"+project+"/reviewer_activeness.npy"
    f = np.load(reviewer_path,allow_pickle=True)
    d = f.tolist()
    # print(d)
    names = []
    for key in d:
        profile_path = project+"/profile/profile_"+str(key)+".JSON"
        fj = open(profile_path,)
        npr = json.load(fj)
        try:
            id = npr["_account_id"]
            reg = npr["registered_on"]
            name = npr["name"]
        except:
            print("error occurred in: ",key)
        try:
            email = npr["email"]
            # username = npr["username"]
        except:
            email = "Not available"
        data_list = [str(id),str(name),str(reg),str(email)]
        # print(data_list)
        with open(csv_path, 'a', newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data_list)
            f_object.close()
    
def findrev(number,project):
    dir = os.getcwd()
    csv_path = dir+"/"+project+"/fp_"+project+".csv"
    csv_file = csv.reader(open(csv_path, "r", encoding='utf-8'), delimiter=",")
    #loop through the csv list
    for row in csv_file:
        #if current rows 1st value is equal to input, print that row
        if number == row[0]:
            print (row)

if __name__ == "__main__":
    # 1. Download change details status=Status.closed
    miner = Miner(gerrit=Gerrit.mano, replace=False)

project="mano"
make_profile(project)
load_profiles(miner,project)
update_profile(project)
# findrev('14250','openstack')