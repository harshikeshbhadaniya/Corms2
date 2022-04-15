from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score
import joblib
import os

from cormstool.corms.clean import text_cleaning
def model_train(df,new_reviews,project):
    filename = "data/"+project+"/model.sav"
    if(not os.path.exists(filename)):
        transformer_sub = CountVectorizer(analyzer=text_cleaning).fit(df["Subject"]) 
        subject_tr = transformer_sub.transform(df["Subject"])
        subject_tr_n = transformer_sub.transform(new_reviews["Subject"])
        tfidf_transformer_sub=TfidfTransformer().fit(subject_tr)
        subject_tfidf=tfidf_transformer_sub.transform(subject_tr)
        # model_mb_sub = MultinomialNB().fit(subject_tfidf,df['Reviewer'])
        model_svm_sub = SVC(probability=True, kernel='rbf')
        model_svm_sub.fit(subject_tfidf,df['Reviewer'])
        # model_rf_sub = RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=-1)
        # model_rf_sub.fit(subject_tfidf,df['Reviewer'])
        # model_knn_sub = KNeighborsClassifier(n_neighbors=43)
        # model_knn_sub.fit(subject_tfidf,df['Reviewer'])
        filename = "cormstool/corms/files/"+project+"/model.sav"
        joblib.dump(model_svm_sub, filename)

def predict(test_sub,train_transformer,model_svm): 
    subject = train_transformer.transform(test_sub)
    svm_pr_sub = model_svm.predict(subject)
    return svm_pr_sub

def predict_new(test_sub,project,train_data): 
    train_transformer = CountVectorizer(analyzer=text_cleaning).fit(train_data)
    subject = train_transformer.transform(test_sub)
    filename = "cormstool/corms/files/"+project+"/model.sav"
    model_svm = joblib.load(filename)
    svm_pr_sub = model_svm.predict(subject)
    return svm_pr_sub