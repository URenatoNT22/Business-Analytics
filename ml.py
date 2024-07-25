import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import joblib


def entrenar():
    datos = pd.read_csv('heart_2020_cleaned_numeric.csv')
    datosX=datos.drop(columns=['HeartDisease'])
    
    X_data = datosX
    y_data = datos['HeartDisease']

    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)

    # Crear y entrenar modelo
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)
    predicciones = modelo_rf.predict(X_test)
    joblib.dump(modelo_rf, 'modelo_rf.joblib')

    # data.head()

    # y = data["HeartDisease"]
    # X = data.drop(['HeartDisease'],axis=1)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 0)
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    # m4 = 'Extreme Gradient Boost'
    # xgb = XGBClassifier(learning_rate=0.01, n_estimators=25, max_depth=15,gamma=0.6, subsample=0.52,colsample_bytree=0.6,seed=27,
    #                     reg_lambda=2, booster='dart', colsample_bylevel=0.6, colsample_bynode=0.5)
    # xgb.fit(X_train, y_train)
    # xgb_predicted = xgb.predict(X_test)
    # xgb_conf_matrix = confusion_matrix(y_test, xgb_predicted)
    # xgb_acc_score = accuracy_score(y_test, xgb_predicted)
    # joblib.dump(modelo_rf, 'modelo_rf.joblib')
    # joblib.dump(xgb, 'xgb_model.joblib')
    # print("confussion matrix")
    # print(xgb_conf_matrix)
    # print("\n")
    # print("Accuracy of Extreme Gradient Boost:",xgb_acc_score*100,'\n')
    # print(classification_report(y_test,xgb_predicted))

def preprocess_and_predict(data):
    modelo_rf = joblib.load('modelo_rf.joblib')
    # xgb = joblib.load('xgb_model.joblib')
    # Preprocesar el nuevo dato (aplicar el mismo escalado)
    # new_data_scaled = scaler.transform(data)
    # Realizar la predicción
    new_prediction = modelo_rf.predict(data)
    # Interpretar la predicción
    if new_prediction[0] == 1:
        return "Presentas una enfermedad cardiaca"
    else:
        return "No presentas una enfermedad cardiaca"
    


entrenar()