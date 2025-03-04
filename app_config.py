import json

CONFIG_FILE_PATH = 'config.json'


class AppConfig:
    _config = {}

    def __init__(self):
        with open(file=CONFIG_FILE_PATH, encoding="utf-8") as fp:
            AppConfig._config = json.loads(fp.read())

    @staticmethod
    def get_value(key: str):
        return AppConfig._config.get(key)

    @staticmethod
    def save_value(key: str, value: str | list | dict):
        AppConfig._config[key] = value
        AppConfig.save_config()

    @staticmethod
    def save_config():
        with open(file=CONFIG_FILE_PATH, mode='w', encoding="utf-8") as fp:
            fp.write(json.dumps(AppConfig._config, ensure_ascii=False))
