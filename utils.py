import configparser
import os
import threading
from functools import wraps


def config_lock(func):
    def wrapper(*arg, **kwargs):
        with ConfigReader._instance_lock:
            return func(*arg, **kwargs)
    return wrapper


class ConfigReader():
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ConfigReader, "_instance"):
            with ConfigReader._instance_lock:
                if not hasattr(ConfigReader, "_instance"):
                    ConfigReader._instance = object.__new__(cls)
        return ConfigReader._instance

    def __init__(self):
        self._base_path = os.path.dirname(__file__)
        self._config_file = '{}/config/config.ini'.format(self._base_path)
        # self._data = configparser.ConfigParser()
        self._data = configparser.RawConfigParser()
        self._data.read(self._config_file)

    @config_lock
    def get(self, section, key):
        return self._data.get(section, key)


# retry wrapper
def retry(times):
    def outer_wrapper(func):
        @wraps(func)
        def inner_wrapper(*arg, **kwargs):
            for _ in range(times):
                try:
                    return func(*arg, **kwargs)
                except Exception:
                    continue
        return inner_wrapper
    return outer_wrapper
