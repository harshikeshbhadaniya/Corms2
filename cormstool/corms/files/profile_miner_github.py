import json
import pandas as pd
import csv
from csv import writer
def update_profile(project):
    csv_path = project+"/github_"+project+".csv"
    new_path = project+"/fp_"+project+".csv"
    header_list = ["Author","Author_Name", "Subject","Project/Subproject","All Reviewers","Reviewers Name","Created","Closed At","File Info","URL","commit_url","Change_Size","status"]
    df = pd.read_csv(csv_path, names=header_list, sep=';', encoding= 'unicode_escape')
    # print(d)
    names = dict()
    i=0
    for item in df["All Reviewers"]:
        j=0
        for key in eval(item):
            if key not in names:
                names[key]=eval(df["Reviewers Name"][i])[j]
            j=j+1
        i=i+1
    
    with open(new_path, 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in names.items():
            writer.writerow([key, value])

update_profile("shopify")