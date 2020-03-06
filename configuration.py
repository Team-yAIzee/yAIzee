# configuration.py
# Configuration management for more flexibility and switching between different environments

import json
from functools import lru_cache


@lru_cache(maxsize=10)
def obtain_configuration(file='resources/config.json'):
    """
    Obtain the configuration from a JSON file.
    @param file The configuration file, default resources/config.json
    @type file str
    """
    with open(file, 'r') as conf_file:
        configuration = json.loads(conf_file.read())

    return configuration
