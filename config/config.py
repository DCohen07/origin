import yaml
import os


def read_yaml() -> dict:
    """Returns YAML file as dict,
    config_path must be filed in by user before everything else"""

    with open(config_path, 'r') as file_in:
        config = yaml.safe_load(file_in)
    return config
