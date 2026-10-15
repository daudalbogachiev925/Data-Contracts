import os, glob
from src.contract import DataContract

class ContractRegistry:
    def __init__(self, folder="contracts"):
        self.folder = folder
        self.contracts = {}
        self.reload()

    def reload(self):
        self.contracts = {}
        for path in glob.glob(os.path.join(self.folder, "*.yaml")):
            c = DataContract.from_yaml(path)
            self.contracts[c.name] = c

    def get(self, name):
        return self.contracts.get(name)

    def all(self):
        return list(self.contracts.values())
