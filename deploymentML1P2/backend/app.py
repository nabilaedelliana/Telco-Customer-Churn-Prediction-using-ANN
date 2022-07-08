from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
from tensorflow import keras

app = Flask(__name__)

# initiate model & columns
LABEL = ["Your Customer Will Stay", "Your Customer Will Leave"]
#datacol = ['MinTemp', 'Humidity3pm', 'Cloud9am', 'Rainfall', 'WindGustSpeed', 'raintoday','month']

with open("prep_pipeline.pkl", "rb") as f:
    prep = pickle.load(f)

model = keras.models.load_model('churn_predictor.h5')

@app.route("/")
def welcome():
    return '<h3>Selamat Datang di Program Backend Saya<h3>'

@app.route("/predict", methods=["GET", "POST"])
def predict_churn():
    if request.method == "POST":
        content = request.json
        try:
            new_data = {'SeniorCitizen': content['Senior_Citizen'],
                        'Partner': content['Has_Partner?'],
                        'Dependents': content['Has_Dependents?'],
                        'tenure': content['Tenure_in_month'],
                        'PhoneService': content['Has_Phone_Service?'],
                        'InternetService': content['Has_Internet_Service?'],
                        'Contract': content['Select_Contract'],
                        'PaperlessBilling': content['Has_Paperless_Billing?'],
                        'PaymentMethod': content['Select_Payment_Method'],
                        'MonthlyCharges': content['Input_Monthly_Charges'],}
            new_data = pd.DataFrame([new_data])
            data_final = prep.transform(new_data)
            res = model.predict(data_final)
            res = np.where(res > 0.1, 1, 0)
            result = {'class':int(res[0]),
                      'class_name':LABEL[int(res[0])]}
            response = jsonify(success=True, result = result)
            return response, 200
        except Exception as e:
            response2 = jsonify(success=False, message=str(e))
            return response2, 400
    
    return "<p>Silahkan gunakan method POST untuk mode <em>inference model </em></p>"
#app.run(debug=True) # harus dihapus kalo mau deploy ke heroku