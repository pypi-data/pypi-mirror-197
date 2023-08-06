from dataclasses import dataclass

import pandas as pd


@dataclass
class CopyDF:
    df: pd.DataFrame

    def copy(self):
        return self.df.copy()
