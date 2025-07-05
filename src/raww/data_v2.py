'''
trying to switch functional aproach to OOP
'''

from pathlib import Path


class Data:
    
    def __init__(self, dir: Path):
        self.dir = dir


DIR_PATH = Path.home() / 'Dev' / 'raww' / 'tests' # test path

data = Data(DIR_PATH)
