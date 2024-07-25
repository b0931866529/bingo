from matplotlib.pyplot import cla
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import unittest
from unittest.mock import Mock


class StateExclude:

    def __init__(self):
        pass

    def exclude(self, row: pd.Series) -> str:

        return 'cold'
        pass
    pass


class TestStateExclude(unittest.TestCase):
    pass
