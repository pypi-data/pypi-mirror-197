# coding=utf-8

import toml
import rtoml

# from typing import Dict, List, Union


class Toml:
    """
    Manage Toml Configuration File
    """
    @staticmethod
    def write(obj, path, **kwargs):
        sw_rtoml = kwargs.get('sw_rtoml', True)
        sw_toml = kwargs.get('sw_toml', False)
        if sw_rtoml:
            with open(path, "w") as fd:
                rtoml.dump(obj, fd, pretty=True)
        elif sw_toml:
            with open(path, "wb") as fd:
                toml.dump(obj, fd)

    @staticmethod
    def to_obj(obj):
        # return toml.dumps(obj).decode('unicode-escape').encode('utf-8')
        return toml.dumps(obj).encode('utf-8').decode('unicode-escape')

    # @classmethod
    # def from_yaml(cls, path_yaml, path_toml):
    #     cls.write(path_toml, cls.to_obj(Yaml.read(path_yaml)))
