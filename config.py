import os
import json

config = {
    "secret": "",
    "uuid": "",
    "endpointURL": ""
}


def getDeviceSecret():
    return config["secret"]


def getDeviceUUID():
    return config["uuid"]


def getServerAddress():
    addr = config["endpointURL"]
    if addr.endswith("/"):
        addr = addr[:-1]
    return addr


def is_file_empty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0 and os.path.getsize(file_path) == 0

def load():
    with open('../../config.json', 'r') as file:
        configData = config
        if not is_file_empty('config.json'):
            configData = json.load(file)
        file.close()
        return configData


def save(config):
    with open('../../config.json', 'w') as file:
        json.dump(config, file)
        file.close()
