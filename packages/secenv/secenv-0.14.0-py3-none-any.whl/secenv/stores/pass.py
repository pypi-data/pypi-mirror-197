import passpy
from . import StoreInterface, cached, ask_secret


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        directory = super().get_from_config(
            name, "directory", infos, default="~/.password-store"
        )
        self.store = passpy.Store(store_dir=directory)

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        if res := self.store.get_key(secret):
            return res
        else:
            raise Exception(f"Secret '{secret}' not found in store '{self.name}'")

    def fill_secret(self, secret):
        value = ask_secret(self.name, secret)
        self.store.set_key(secret, value, force=True)
