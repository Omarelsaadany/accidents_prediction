# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

import uvicorn
from fastapi import FastAPI
from Accis_Pred import Accis_Pred
import numpy as np
import pickle
import pandas as pd

app = FastAPI()
pickle_in = open("traffic_pred.pkl","rb")
predict_acc=pickle.load(pickle_in)

@app.get('/')
def index():
    return {'message': 'Hello, welcome to my traffic accident prediction model'}


@app.post('/predict')
def predict_Accis(data:Accis_Pred):
    data = data.dict()
    yahr=data['yahr']
    monat=data['monat']
    #x0_Alkoholunfälle=data['x0_Alkoholunfälle']
    #x0_Fluchtunfälle=data['x0_Fluchtunfälle']
    #x0_Verkehrsunfälle=data['x0_Verkehrsunfälle']
    #x1_verletzte_und_getötete=data['x1_verletzte_und_getötete']
    #x1_insgesamt=data['x1_insgesamt']
    #3x1_mit_personenschäden=data['x1_mit_personenschäden']
   # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    '''prediction = predict_acc.predict([[yahr,monat,x0_Alkoholunfälle,x0_Fluchtunfälle,
                                      x0_Verkehrsunfälle,x1_verletzte_und_getötete,x1_insgesamt,
                                      x1_mit_personenschäden]])'''
    prediction = predict_acc.predict([[yahr,monat,1,0,0,0,1,0]])
    
    return {
        'prediction': prediction[0]
    }


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload
