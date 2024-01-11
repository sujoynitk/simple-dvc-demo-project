import yaml
import argparse
def read_config_data(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
        return config

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parse_args = args.parse_args()
    config_data = read_config_data(parse_args)
        