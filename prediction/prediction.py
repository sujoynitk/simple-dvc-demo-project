from src.get_data import read_config_data
import joblib
import json

class NotInCols(Exception):
    def __init__(self, message="Not in columns defined in schema"):
        self.message = message
        super().__init__(self.message)

class NotInRange(Exception):
    def __init__(self, message="Value not in range"):
        self.message = message
        super().__init__(self.message)
        
def predict(data):
    config = read_config_data("params.yaml")
    prediction_model = config["prediction_model"]
    model = joblib.load(prediction_model)
    prediction = model.predict(data).tolist()[0]
    try:
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange("Unexpected result(prediction not in range)")
    except NotInRange:
        return "Unexpected result(prediction not in range)"

def read_schema(schema_path):
    with open(schema_path) as json_file:
        schema_data = json.load(json_file)
    return schema_data

def validate_input(data_dict_request):
    def _validate_column(col, schema_data):
        if col not in schema_data.keys():
            raise NotInCols(f"{col} not in schema")
    def _validate_value(value, col, schema_data):
        if not (schema_data[col]["min"] <= float(value) <= schema_data[col]["max"]):
            raise NotInRange(f"{col} value not in predefined range")        
    
    config = read_config_data("params.yaml")
    schema_data = read_schema(config["model_input_schema_path"])
    for key, value in data_dict_request.items():      
        _validate_column(key, schema_data)
        _validate_value(value, key, schema_data)
    return True

def form_response(data_dict_request):
    if validate_input(data_dict_request):
        data = data_dict_request.values()
        data = [list(map(float, data))]
        response = predict(data)
        return response

def api_response(data_dict_request):
    try:
        if validate_input(data_dict_request):
            data = data_dict_request.values()
            data = [list(map(float, data))]
            response = predict(data)
            response = {"response": response}
            return response
    except NotInCols as e:
        response = {"response" : str(e)}
        return response
    except NotInRange as e:
        response = {"response" : str(e)}
        return response
    except Exception as e:
        response = {"response" : str(e)}  
        return response