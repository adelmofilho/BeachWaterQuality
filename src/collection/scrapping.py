import requests
from time import sleep
from tqdm import tqdm
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as bs
from .utils import get_logs
import json


def extract_info(chave, a, b):
    try:
        valor = chave[a][b]
    except IndexError:
        valor = "Null"
    return valor


def list_boletins(config):
    """
    List all Beach Water Quality Boletins.
    
    Parameters
    ----------
    config: dict
        A loaded config file
    
    Returns
    -------
    list_boletins: list
        A list of all avaliable Boletins
    """    
    website = config.get("website")
    home_url = "{}/{}".format(website.get("baseUrl"), website.get("homeIdx"))
    req = requests.get(home_url)
    soup = bs(req.content, 'html.parser')
    list_boletins = soup.find(id="idcampanha").find_all("option")[1:]
    return list_boletins


def _extract_boletim_info(boletim, logs_filepath):
    logs = get_logs(logs_filepath)
    dicionario = None
    # Get principal informations
    value = boletim.get("value")
    if not value in logs:   
        dicionario = dict()
        text = boletim.get_text()
        # Extract information from text
        info = [x.strip().split() for x in text.split("-")]
        campanha = extract_info(info, 0, 1)
        regiao = extract_info(info, 0, 2)
        dia =  extract_info(info, 1, 0)
        # Create dict
        dicionario[value] = {"regiao": regiao, "campanha": campanha, "dia": dia}
        # Return dictionary
    return value, dicionario


def _registry_boletim(dicionario, config, logs_filepath):
    if dicionario is not None:
        data_config = config.get("data")
        root_dir = data_config.get("root")
        logs_dir = config.get("logs").get("dir")
        filename = config.get("logs").get("file")
        logs = get_logs(logs_filepath)
        index = list(dicionario.keys())[0]
        logs[index] = dicionario[index]
        with open(logs_filepath, 'w') as f:
            json.dump(logs, f)


def download_boletim(list_boletins, config, logs_filepath, prefix="boletim"):
    
    website = config.get("website")
    base_url = website.get('baseUrl')
    down_url = website.get('downIdx')
    url = "{}/{}".format(base_url, down_url)

    root_dir = config.get('data').get('root')
    raw_dir = config.get('data').get("subfolder").get('raw')
    
    for boletim in tqdm(list_boletins):
        id_campanha, dicionario = _extract_boletim_info(boletim, logs_filepath)
        if dicionario is not None:
            sleep(3)
            boletim_url = f"{url}?idcampanha={id_campanha}"
            urlretrieve(boletim_url, f"{root_dir}/{raw_dir}/{prefix}_{id_campanha}.pdf")
            _registry_boletim(dicionario, config, logs_filepath)
