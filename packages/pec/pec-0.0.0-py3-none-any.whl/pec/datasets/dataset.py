import pkgutil
from io import StringIO

import pandas as pd


def _load_dataset(name):
    available = ['a1', 'a2', 'a3', 's1', 's2', 's3', 's4', 'unbalanced']
    if name not in available:
        raise RuntimeError(f'dataset name must be in {{available}}')

    csvString = str(pkgutil.get_data(__name__, f'csv/{name}.csv').decode())
    df = pd.read_csv(StringIO(csvString))
    return df


class DefaultDataset:
    @staticmethod
    def A1():
        """Returns the a1 dataset as a pandas dataframe"""
        return _load_dataset('a1')

    @staticmethod
    def A2():
        """Returns the a2 dataset as a pandas dataframe"""
        return _load_dataset('a2')

    @staticmethod
    def A3():
        """Returns the a3 dataset as a pandas dataframe"""
        return _load_dataset('a3')

    @staticmethod
    def S1():
        """Returns the s1 dataset as a pandas dataframe"""
        return _load_dataset('s1')

    @staticmethod
    def S2():
        """Returns the s2 dataset as a pandas dataframe"""
        return _load_dataset('s2')

    @staticmethod
    def S3():
        """Returns the s3 dataset as a pandas dataframe"""
        return _load_dataset('s3')

    @staticmethod
    def S4():
        """Returns the s4 dataset as a pandas dataframe"""
        return _load_dataset('s4')

    @staticmethod
    def Unbalanced():
        """Returns the Unbalanced dataset as a pandas dataframe"""
        return _load_dataset('unbalanced')
