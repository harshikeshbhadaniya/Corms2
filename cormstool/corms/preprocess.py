import pandas as pd
def process(df):
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
    df.shape
    # df.to_csv('exr_openstack.csv')
    new_reviews = df.head(344)
    df = df.iloc[344: , :]
    df = df.reset_index(drop=True)
    return df,new_reviews