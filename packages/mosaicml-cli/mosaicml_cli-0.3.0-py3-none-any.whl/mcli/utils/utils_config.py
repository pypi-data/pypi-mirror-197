"""Utils for modifying MCLI Configs"""
import random
import string
import warnings
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Dict, Union

import yaml

from mcli.utils.utils_yaml import load_yaml


def uuid_generator(length: int = 10) -> str:
    allowed_characters = string.ascii_lowercase + string.digits
    items = random.choices(population=allowed_characters, k=length)
    return ''.join(items)


@dataclass
class BaseSubmissionConfig():
    """ Base class for config objects"""

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def empty(cls):
        return cls()

    @classmethod
    def from_file(cls, path: Union[str, Path]):
        """Load the config from the provided YAML file.
        Args:
            path (Union[str, Path]): Path to YAML file
        Returns:
            BaseConfig: The BaseConfig object specified in the YAML file
        """
        config = load_yaml(path)
        return cls.from_dict(config, show_unused_warning=True)

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = False):
        """Load the config from the provided dictionary.
        Args:
            dict_to_use (Dict[str, Any]): The dictionary to populate the BaseConfig with
        Returns:
            BaseConfig: The BaseConfig object specified in the dictionary
        """
        field_names = list(map(lambda x: x.name, fields(cls)))

        unused_keys = []
        constructor = {}
        for key, value in dict_to_use.items():
            if key in field_names:
                constructor[key] = value
            else:
                unused_keys.append(key)

        if len(unused_keys) > 0 and show_unused_warning:
            warnings.warn(f'Encountered fields {unused_keys} which were not used in constructing the run/deployment.')

        return cls(**constructor)
