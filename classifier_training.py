import pandas as pd
import numpy as np


#Reading the data exported from dataset_for_training.py .
data = pd.read_csv('data.csv')



#Train Test split.
from sklearn.model_selection import train_test_split
x = data['article']
y = data['label']

x_train ,x_test, y_train,y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


#Vectorize the words and use logistic regression to train the data.
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=5000,
        ngram_range=(1,2),
        stop_words="english"
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])


pipeline.fit(x_train, y_train)


y_pred = pipeline.predict(x_test)






#Checking our model accuracy and statistics.
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))




"""precision    recall  f1-score   support

           0       0.70      0.82      0.76        61
           1       0.93      0.92      0.92       278
           2       0.78      0.73      0.75       114

    accuracy                           0.86       453
   macro avg       0.80      0.82      0.81       453
weighted avg       0.86      0.86      0.86       453  """


#Really good results, so we leave it as it is and save it. 
import joblib
joblib.dump(pipeline, "classifier.joblib")



