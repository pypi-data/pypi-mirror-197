# coding=utf-8

from typing import Any

import yaml


class Yaml:

    """ Manage Object to Yaml file affilitation
    """
    @staticmethod
    def load_with_loader(string: str) -> None | Any:
        return yaml.load(string, Loader=yaml.Loader)

    @staticmethod
    def load_with_safeloader(string: str) -> None | Any:
        return yaml.load(string, Loader=yaml.SafeLoader)

    @staticmethod
    def safe_load(string: str, **kwargs) -> None | Any:
        return yaml.safe_load(string, **kwargs)
        # return yaml.load(string, Loader=yaml.SafeLoader)

    @staticmethod
    def read(path: str) -> None | Any:
        with open(path) as fd:
            # The Loader parameter handles the conversion from YAML
            # scalar values to Python object format
            return yaml.load(fd, Loader=yaml.SafeLoader)
            # return yaml.load(fd, Loader=yaml.Loader)
        return None

    @staticmethod
    def write(obj: Any, path: str) -> None:
        with open(path, 'w') as fd:
            yaml.dump(
                obj, fd,
                Dumper=yaml.SafeDumper,
                sort_keys=False,
                indent=4,
                default_flow_style=False
            )
            #   block_seq_indent=2,
