import os
import yaml
from os.path import expanduser
home = expanduser("~")

expected_env_variables = [
    'ACCOUNT',
    'DATABASE',
    'SCHEMA',
    'USER',
    'PASSWORD',
    'ROLE',
    'WAREHOUSE'
]

_default_path_to_profiles = '.dbt/profiles.yml'

def default_path_to_profiles():
    return os.path.join(home, _default_path_to_profiles)

def set_env_variables_from_local(project_name: str, target_name:str, local_path: str = None):
    """
    Reads a config file with the same structure as a dbt profiles.yml file and sets the environment variables
    :param local_path:
    :param project_name:
    :param target_name:
    :return:
    """
    if local_path is None:
        local_path = default_path_to_profiles()
    with open(local_path, 'r') as f:
        d = yaml.load(f, Loader=yaml.FullLoader)
    d = d[project_name]['outputs'][target_name]
    d = {k.upper(): v for k, v in d.items()}
    for e in expected_env_variables:
        if d.get(e) is not None:
            os.environ[e.upper()] = d.get(e)
    return None

def set_env_variables_if_missing(project_name: str, target_name:str, local_path: str = None):
    if not verify_env_variables_exist():
        print('Environment variables not set. Attempting to load from local path.')
        set_env_variables_from_local(project_name, target_name, local_path)

def verify_env_variables_exist():
    return all([os.environ.get(e) is not None for e in expected_env_variables])