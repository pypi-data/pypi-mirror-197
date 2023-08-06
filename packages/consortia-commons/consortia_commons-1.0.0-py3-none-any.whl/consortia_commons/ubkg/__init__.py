import requests
from consortia_commons.file import load_config_by_key
from consortia_commons.string import trim_dict_or_list
import json

ubkg_cache = dict()
_config_key = 'UBKG'


class Ubkg:
    def __init__(self, config_key: str = _config_key):
        self.error = None
        self.config_key = config_key

    def get_ubkg_valueset(self, node):
        return self.get_ubkg(node)

    def get_ubkg_by_key(self, node):
        key = get_from_node(node, 'key')
        return self.get_ubkg(node, key)

    def get_ubkg_by_endpoint(self, node):
        key = get_from_node(node, 'key')
        endpoint = get_from_node(node, 'endpoint')
        return self.get_ubkg(node, key, endpoint)

    def get_ubkg(self, node, key: str = 'valueset', endpoint: str = None):
        code = get_from_node(node)
        cache_key = f"{key}_{code}"
        try:
            self.error = None
            if cache_key not in ubkg_cache:
                server = load_config_by_key(self.config_key, 'server')
                endpoint = endpoint if endpoint is not None else load_config_by_key(self.config_key, f"endpoint_{key}")
                url = f"{server}{endpoint}"
                url = url.format(code=code)
                response = requests.get(url)
                if response.ok:
                    ubkg_cache[cache_key] = trim_dict_or_list(response.json())
        except Exception as e:
            self.error = e
            print(e)

        return ubkg_cache[cache_key] if cache_key in ubkg_cache else self.error


def get_from_node(node, key: str = 'code'):
    if type(node) is dict:
        code = node.get(key)
    else:
        code = node
    if type(code) is not str:
        return None
    else:
        return code


def initialize_ubkg(config_key: str = _config_key):
    try:
        ubkg_instance = Ubkg(config_key)
        codes_str = load_config_by_key(config_key, 'codes')
        codes = json.loads(codes_str)
        for node, code in codes.items():
            setattr(ubkg_instance, f"{node}", code)
        return ubkg_instance
    except Exception as e:
        print(e)



