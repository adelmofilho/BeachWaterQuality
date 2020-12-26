import os
import json
import yaml


def get_configs(file="config.yaml"):
    """
    Load project config file.
    
    Parameters
    ----------
    file: str
        Filepath of config file
    
    Returns
    -------
    config: dict
        A loaded config file
    """    
    if file.endswith('.yaml') or file.endswith('.yml'):
        try:
            with open(file, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            return config
        except FileNotFoundError as err:
            print("File not found")
    else: 
        raise TypeError("Config file extension is not .yaml or .yml")


def init_logs(config):
    """
    Logs file inicialization.
    
    Parameters
    ----------
    config: dict
        Dictionary containing configuration variables
    
    Returns
    -------
    filepath: str
        Filepath of logs file
    """
    # Define environment variables
    logs_dir = config.get("logs").get("dir")
    filename = config.get("logs").get("file")
    filepath = f"{logs_dir}/{filename}"

    # Create directory if necessary
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create logs file if necessary
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            empty_file = dict()
            json.dump(empty_file, f)

    # return logs filepath
    return filepath


def get_logs(logs_filepath):
    """
    Load project config file.
    
    Parameters
    ----------
    logs_filepath: str
        Filepath of logs file
    
    Returns
    -------
    logs: dict
        A loaded logs file
    """    
    with open(logs_filepath, 'r') as f:
        logs = json.load(f)
    return logs


def extract_info(chave, a, b):
    try:
        valor = chave[a][b]
    except IndexError:
        valor = "Null"
    return valor   