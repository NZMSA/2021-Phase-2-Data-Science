# Load libraries 
import json
import os 
import numpy as np
from xgboost import XGBClassifier

# Since model works with label encoded data, we can create a dictionary to get the acutal class names
classes = {0: "setosa", 1: "versicolor", 2: "virginica"}

# 1. Requried init function
def init():
    # Create a global variable for loading the model
    global model
    model = XGBClassifier(use_label_encoder = False)
    model.load_model(os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.json"))

# 2. Requried run function
def run(request):
    # Receive the data and run model to get predictions 
    data = json.loads(request)
    data = np.array(data["data"])
    res = model.predict(data)
    return [classes.get(key) for key in res]