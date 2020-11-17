from os.path import abspath, dirname, join

import json


MAP_FILE = join(dirname(dirname(abspath(__file__))), "config/mapping.json")


def read_mapping_file(filepath, encoding='utf-8'):
    with open(filepath, encoding=encoding) as mapping_file:
        return json.load(mapping_file)


def get_translation(word):
    mapping_dict = read_mapping_file(MAP_FILE)
    return mapping_dict.get(word)
