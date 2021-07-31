# Load libraries 
import json
import os 
import numpy as np
from xgboost import XGBClassifier
from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse

# Since model works with label encoded data, we can create a dictionary to get the acutal class names
classes = {0: "setosa", 1: "versicolor", 2: "virginica"}

# 1. Requried init function
def init():
    # Create a global variable for loading the model
    global model
    model = XGBClassifier(use_label_encoder = False)
    model.load_model(os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.json"))

# 2. Requried run function
@rawhttp
def run(request):
    # Receive the data and run model to get predictions 
    if request.method == 'GET':
        respBody = str.encode(request.full_path)
        return AMLResponse(respBody, 200)
    elif request.method == 'POST':
        reqBody = request.get_data(False)
        data = json.loads(reqBody)
        data = np.array(data["data"])
        res = model.predict(data)
        resp = AMLResponse([classes.get(key) for key in res], 200)
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp
    else:
        return AMLResponse("bad request", 500)
