from .utils import get_configs, init_logs, get_logs
from .scrapping import list_boletins, download_boletim

config = get_configs()
logs_filepath = init_logs(config)
logs = get_logs(logs_filepath)
list_boletins = list_boletins(config)
download_boletim(list_boletins, config, logs_filepath)