import logging
import os
import sys
import pytest as pytest
from argparse import ArgumentParser

import yaml
from yaml import FullLoader
from start_tests import DIR, MyPlugin
from settings.converter_model import Converter


def run_tests(env: str):
    valid_envs = ['prod', 'dev']
    param_list = []

    if env not in valid_envs:
        raise TypeError(f"ENV '{env}' not found")

    if env == 'prod':
        param_list = ["-v",
                      "-s",
                      "--alluredir=./allureresult"]

    if env == 'dev':
        param_list = ["-v",
                      "-s",
                      "--alluredir=./allureresult"]

    sys.exit(pytest.main(param_list, plugins=[MyPlugin()]))


class ConfigLoader:
    __instance = None

    DEFAULT_CONFIG_PATH = 'settings/environments.yml'

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ConfigLoader, cls).__new__(cls)
        return cls.__instance

    def __del__(self):
        ConfigLoader.__instance = None

    def __init__(self, environments: dict = None):
        self.environments = environments

    @staticmethod
    def _create_parser():
        parser = ArgumentParser(
            prog='vgz_monitoring_tests',
            description='tests run settings'
        )
        parser.add_argument(
            '--env', type=str, default="prod",
            help='"prod" - run prod tests, "dev" - run dev tests'
        )

        return parser

    def load_yaml_config(self, path):
        path_to_file = os.path.join(path, self.DEFAULT_CONFIG_PATH)
        with open(path_to_file) as f:
            data = yaml.load(f, Loader=FullLoader)
            return data

    def set_env(self):
        parser = self._create_parser()
        args = parser.parse_known_args()[0].__dict__
        os.environ["ENV"] = args['env'] or "prod"

        return os.getenv("ENV")

    def merge_config(self):
        """
        Если переменные среды не заданы в '.env',
        то они заполняются данными из 'enviroments.yml'
        """
        env = self.set_env()
        config_yaml = self.load_yaml_config(DIR)

        self.environments = Converter(**config_yaml[env])

        if os.getenv("MP_LOGIN"):
            self.environments.mostro_pim.login = os.getenv("MP_LOGIN")
        if os.getenv("MP_PASSWORD"):
            self.environments.mostro_pim.password = os.getenv("MP_PASSWORD")

        if os.getenv("SEARCH_LOGIN"):
            self.environments.search.login = os.getenv("SEARCH_LOGIN")
        if os.getenv("SEARCH_PASSWORD"):
            self.environments.search.password = os.getenv("SEARCH_PASSWORD")

        if os.getenv("MSS_LOGIN"):
            self.environments.mostro_search_sync.login = os.getenv("MSS_LOGIN")
        if os.getenv("MSS_PASSWORD"):
            self.environments.mostro_search_sync.password = os.getenv("MSS_PASSWORD")

        if os.getenv("SYNC_LOGIN"):
            self.environments.sync.login = os.getenv("SYNC_LOGIN")
        if os.getenv("SYNC_PASSWORD"):
            self.environments.sync.password = os.getenv("SYNC_PASSWORD")

        if os.getenv("TOKEN"):
            self.environments.telegram.token = os.getenv("TOKEN")
        if os.getenv("CHAT_ID"):
            self.environments.telegram.chat_id = os.getenv("CHAT_ID")

        return self.environments


config_loader = ConfigLoader()
settings = config_loader.merge_config()
