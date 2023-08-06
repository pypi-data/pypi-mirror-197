import os
from . import StoreInterface, cached, ask_secret


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        res = os.getenv(secret)
        if res:
            return res
        else:
            raise Exception(f"Secret '{secret}' not found in store '{self.name}'")

    def fill_secret(self, secret):
        os.environ[secret] = ask_secret(self.name, secret)
