from get_data import read_config_data
import pandas as pd
from sklearn.model_selection import train_test_split
import argparse
def process_raw_data(config_path):
    config = read_config_data(config_path)
    raw_data_path = config["data_path"]["loaded_data_path"]
    train_data_path = config["data_path"]["processed_data_path"]["train_data_path"]
    test_data_path = config["data_path"]["processed_data_path"]["test_data_path"]
    test_size = config["others"]["test_size"]
    random_state = config["others"]["random_state"]
    raw_data = pd.read_csv(raw_data_path, sep=',')
    train_data, test_data = train_test_split(raw_data, test_size=test_size, random_state=random_state)
    train_data.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test_data.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    process_raw_data("params.yaml")