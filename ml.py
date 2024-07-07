#loading dataset
import pandas as pd
import numpy as np
#visualisation
import matplotlib.pyplot as plt
#matplotlib inline
import seaborn as sns
#EDA
from collections import Counter
# data preprocessing
from sklearn.preprocessing import StandardScaler
# data splitting
from sklearn.model_selection import train_test_split
# data modeling
from sklearn.metrics import confusion_matrix,accuracy_score,roc_curve,classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
#ensembling
from mlxtend.classifier import StackingCVClassifier


def entrenar():
    data = pd.read_csv('heart_2020_cleaned_numeric.csv')
    data.head()

    y = data["HeartDisease"]
    X = data.drop(['HeartDisease'],axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 0)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    m4 = 'Extreme Gradient Boost'
    xgb = XGBClassifier(learning_rate=0.01, n_estimators=25, max_depth=15,gamma=0.6, subsample=0.52,colsample_bytree=0.6,seed=27,
                        reg_lambda=2, booster='dart', colsample_bylevel=0.6, colsample_bynode=0.5)
    xgb.fit(X_train, y_train)
    xgb_predicted = xgb.predict(X_test)
    xgb_conf_matrix = confusion_matrix(y_test, xgb_predicted)
    xgb_acc_score = accuracy_score(y_test, xgb_predicted)
    # print("confussion matrix")
    # print(xgb_conf_matrix)
    # print("\n")
    # print("Accuracy of Extreme Gradient Boost:",xgb_acc_score*100,'\n')
    # print(classification_report(y_test,xgb_predicted))

def preprocess_and_predict(data):
    # Preprocesar el nuevo dato (aplicar el mismo escalado)
    new_data_scaled = scaler.transform(data)
    # Realizar la predicción
    new_prediction = xgb.predict(new_data_scaled)
    # Interpretar la predicción
    if new_prediction[0] == 1:
        return "Presentas una enfermedad cardiaca"
    else:
        return "No presentas una enfermedad cardiaca"