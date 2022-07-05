from flask import Flask
import flask
import os
import json
import logging

#import pandas
import pandas as pd

# importing classification module
from pycaret.classification import load_model, predict_model

loadedModel = load_model('saved_lr_model') 


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
    df = pd.DataFrame.from_dict(input_json, orient='index')
    print(df)
    
    #NER
    results = predict_model(loadedModel, data=df)
    results = results.to_json(orient="index")
    parsed = json.loads(results)
    results = json.dumps(parsed, indent=4)


    # Transform predictions to JSON
    result = {
        'output': results
        }

    resultjson = json.dumps(result)
    return flask.Response(response=resultjson, status=200, mimetype='application/json')