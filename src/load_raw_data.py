import pandas as pd
import argparse
from get_data import read_config_data
def load_raw_data(config_path):
    config = read_config_data(config_path)
    source_data_path = config["data_path"]["source_data_path"]
    raw_data_path = config["data_path"]["loaded_data_path"]
    df = pd.read_csv(source_data_path, sep=',', encoding='utf-8')
    cols_df = df.columns
    new_columns = [x.replace(" ","_") for x in cols_df]
    df.to_csv(raw_data_path, sep=',', index=False, header=new_columns)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    raw_data=load_raw_data('params.yaml')
    
    
    