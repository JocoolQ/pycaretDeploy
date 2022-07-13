from flask import Flask
import flask
import os
import json
import logging

#import pandas
import pandas as pd

# importing classification module
from pycaret.classification import load_model, predict_model




# The flask app for serving predictions
app = Flask(__name__)
@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    health = log_reg is not None
    status = 200 if health else 404
    return flask.Response(response= '\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    
    #Process input
    input_json = flask.request.get_json()
    print(input_json)
    loadedModel = load_model('saved_models/iforest'+str(input_json['user']['user_segment'])+'_pipeline') 
    df = pd.DataFrame.from_dict([input_json['transaction']])
    print(df)
    
    #NER
    results = predict_model(loadedModel, data=df)
    results = results.to_json(orient="index")
    parsed = json.loads(results)
      

    # Transform predictions to JSON
    resultjson = json.dumps(parsed, indent=4)
    return flask.Response(response=resultjson, status=200, mimetype='application/json')