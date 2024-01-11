import os
def test_params_yaml_file_exists():
    assert os.path.exists("params.yaml") == True
def test_dvc_yaml_file_exists():
    assert os.path.exists("dvc.yaml") == True