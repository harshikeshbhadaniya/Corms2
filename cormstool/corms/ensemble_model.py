from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score
from cormstool.corms.clean import text_cleaning
def model_train(df,new_reviews):
    transformer_sub = CountVectorizer(analyzer=text_cleaning).fit(df["Subject"]) 
    subject_tr = transformer_sub.transform(df["Subject"])
    subject_tr_n = transformer_sub.transform(new_reviews["Subject"])
    tfidf_transformer_sub=TfidfTransformer().fit(subject_tr)
    subject_tfidf=tfidf_transformer_sub.transform(subject_tr)
    model_mb_sub = MultinomialNB().fit(subject_tfidf,df['Reviewer'])
    model_svm_sub = SVC(probability=True, kernel='rbf')
    model_svm_sub.fit(subject_tfidf,df['Reviewer'])
    model_rf_sub = RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=-1)
    model_rf_sub.fit(subject_tfidf,df['Reviewer'])
    model_knn_sub = KNeighborsClassifier(n_neighbors=43)
    model_knn_sub.fit(subject_tfidf,df['Reviewer'])

    y_pred = model_mb_sub.predict(subject_tr_n)
    # print(metrics.classification_report(new_reviews["Reviewer"], y_pred))
    # print("Multinomial Naive Bayes:",accuracy_score(new_reviews["Reviewer"], y_pred)*100)

    y_pred = model_svm_sub.predict(subject_tr_n)
    # print(metrics.classification_report(new_reviews["Reviewer"], y_pred))
    # print("SVM:",accuracy_score(new_reviews["Reviewer"], y_pred)*100)

    y_pred = model_rf_sub.predict(subject_tr_n)
    # print(metrics.classification_report(new_reviews["Reviewer"], y_pred))
    # print("Random forest:",accuracy_score(new_reviews["Reviewer"], y_pred)*100)

    y_pred = model_knn_sub.predict(subject_tr_n)
    # print(metrics.classification_report(new_reviews["Reviewer"], y_pred))
    # print("K Nearest Neighbour:",accuracy_score(new_reviews["Reviewer"], y_pred)*100)

    neighbors_and_accuracies = {}
    high_ac = 0
    high = 0
    for i in range(1,100):
        model_knn_sub = KNeighborsClassifier(n_neighbors=i)
        model_knn_sub.fit(subject_tfidf,df['Reviewer'].ravel())
        Y_pred = model_knn_sub.predict(subject_tr_n)
        ac = accuracy_score(new_reviews["Reviewer"],Y_pred)*100
        if(ac>high_ac):
            high_ac = ac
            high = i
        neighbors_and_accuracies[i] = ac
    # print("highest accuracy for subject in KNN: "+format(high_ac)+" at neighbours: "+format(high))
    
    return transformer_sub,model_svm_sub

def predict(test_sub,train_transformer,model_svm): 
    subject = train_transformer.transform(test_sub)
    svm_pr_sub = model_svm.predict(subject)
    