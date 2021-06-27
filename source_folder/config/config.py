import os
import yaml

this_dir = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(this_dir, "config.yml")


def read_yaml() -> dict:
    """Returns YAML file as dict,
    config_path must be filed in by user before everything else"""

    
    with open(config_file_path, 'r') as file_in:
        config = yaml.safe_load(file_in)
    return config
