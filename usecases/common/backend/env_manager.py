import os
import streamlit as st
import json
from typing import Type, TypeVar
from dataclasses import dataclass, fields

T = TypeVar('T')

@dataclass
class EnvManager:

    @classmethod
    def from_json(cls, data_cls: Type[T], json_str: str) -> T:
        data = json.loads(json_str)  # Convert JSON string to dictionary
        field_names = {f.name for f in fields(data_cls)}  # Get field names of the dataclass
        filtered_data = {k: v for k, v in data.items() if k in field_names}  # Filter out extra fields
        return data_cls(**filtered_data)  # Instantiate the dataclass

    @classmethod
    def make_instance(cls, data_cls: Type[T], json_str: str) -> T:
        """
        Make instance with strict dataclass fields
        :param data_cls:
        :param json_str:
        :return:
        """
        data = json.loads(json_str)
        return data_cls(**data)

    @classmethod
    def load_instance(cls, data_cls: Type[T], key: str) -> T:
        json = cls.get_secret(key)
        ret = cls.from_json(data_cls, json)
        return ret

    @classmethod
    def load_instances(cls, data_cls: Type[T], prefix: str) -> list:
        ret = []

        has_secrets = cls._has_secrets()

        if has_secrets:
            plugin_keys_secrets = [k for k in st.secrets.keys() if k.startswith(f"{prefix}_")]
        else:
            plugin_keys_secrets = []

        try:
            plugin_keys_env = [k for k in os.environ.keys() if k.startswith(f"{prefix}_")]
        except Exception as e:
            plugin_keys_env = []

        plugin_keys = list(set(plugin_keys_secrets + plugin_keys_env))
        for key in plugin_keys:
            # plugin = cls.from_json(data_cls, st.secrets[key])
            plugin = cls.from_json(data_cls, cls.get_secret(key))
            ret.append(plugin)

        return ret

    @classmethod
    def get_secret(cls, key, default: str = None) -> str:
        has_secrets = cls._has_secrets()

        try:
            if has_secrets and key in st.secrets.keys():
                return st.secrets[key]
            else:
                return os.getenv(key.upper(), default)
        except Exception as e:
            return os.getenv(key.upper(), default)

    @classmethod
    def _has_secrets(cls):
        secrets_file_path = os.path.join(os.path.expanduser("~"), ".streamlit", "secrets.toml")
        project_secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
        has_secrets = os.path.exists(secrets_file_path) or os.path.exists(project_secrets_path)
        return has_secrets
