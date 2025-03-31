import yaml


def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    mode = config['mode']
    return config[mode]