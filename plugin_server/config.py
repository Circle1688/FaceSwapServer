import configparser

config = configparser.ConfigParser()
config.read('config.ini')

USER_DATA_DIR = config['default']['user_data_dir']
UE_URL = config['workflow']['ue_url']
FACEFUSION_URL = config['workflow']['facefusion_url']
PIXVERSE_API_KEY = config['workflow']['pixverse_apiKey']
