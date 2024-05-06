import toml

class Config:
    def __init__(self, fpath):
        self.__data = toml.load(fpath)
        pass

    @property
    def validator_dir(self):
        return self.__data["validator_dir"]

    @property
    def data_dir(self):
        return self.__data["data_dir"]