from get_data import read_config_data
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import json
import numpy as np
import joblib
import os
import argparse

def eval_metrics(actual, pred):
    mae = mean_absolute_error(actual, pred)
    mse = mean_squared_error(actual, pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(actual, pred)
    return (rmse, mae, r2)

def train_and_evaluate_model(config_path):
    config = read_config_data(config_path)
    train_data_path = config["data_path"]["processed_data_path"]["train_data_path"]
    test_data_path = config["data_path"]["processed_data_path"]["test_data_path"]
    train_data = pd.read_csv(train_data_path, sep=",", encoding="utf-8")
    test_data = pd.read_csv(test_data_path, sep=",", encoding="utf-8")
    target = config["others"]["target_column"]
    params_file = config["reports"]["params"]
    scores_file = config["reports"]["scores"]
    random_state = config["others"]["random_state"]
    l1_ratio_param = config["training_models"]["ElasticNet"]["params"]["l1_ratio"]
    alpha_param = config["training_models"]["ElasticNet"]["params"]["alpha"]
    model_path = config["model_dir"]
    lr = ElasticNet(
        l1_ratio=l1_ratio_param,
        alpha=alpha_param,
        random_state=random_state
    )
    train_y = train_data[target]
    train_x = train_data.drop(target, axis=1)
    test_y = test_data[target]
    test_x = test_data.drop(target, axis=1)
    lr.fit(train_x,train_y)
    predicted = lr.predict(test_x)
    rmse, mae, r2 = eval_metrics(test_y, predicted)
    with open(params_file, "w") as f:
        params = {
            "l1_ratio" : l1_ratio_param,
            "alpha": alpha_param
        }
        json.dump(params, f, indent=4)
 
    with open(scores_file, "w") as f:
        scores = {
            "rmse" : rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)       
    os.makedirs(model_path, exist_ok=True)
    model_file = os.path.join(model_path, "model.joblib")
    joblib.dump(lr, model_file)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate_model("params.yaml")