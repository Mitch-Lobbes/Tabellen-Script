import pandas as pd
import numpy as np


class Stap1:

    def __init__(self):
        pass

    def cross_tables(self, df: pd.DataFrame, kvs: list, column: str) -> pd.DataFrame:

        list_ = []

        for i in range(len(self._kvs)):
            # Create Cross Tabs
            cross = pd.crosstab(index=self._df[self._column], columns=self._data[self._kvs[i]]) \
                if i != len(self._kvs) - 1 \
                else pd.crosstab(index=self._df[self._column], columns=self._data[self._kvs[i]], margins=True)

            # Add Missing Answers to Crossings
            cross = self._missing_answers(df=cross)

            # Sort Crossing Categories
            cross = cross[self._syntax[cross.columns.name].antwoorden] if i != len(self._kvs) - 1 else \
                cross[self._syntax[cross.columns.name].antwoorden].join(cross['All'])

            list_.append(cross)

        base = list_.pop(0)

        # Combine Crossings Together
        for df in list_:
            for col in df:
                base.insert(len(base.columns), col, df[col])

        # Remove Total Row if Only 1 Crossing
        base = base[base.index != 'All'] if len(self._kvs) == 1 else base

        # Create New Total Row and Calculate Percentages
        total = base.sum()
        base = (100. * base / total).replace(np.nan, 0).astype(int)
        total.name = '(N)'
        base = base.append(total.transpose())

        # Move Total Column to Front of Dataframe
        base = base[['All'] + [col for col in base.columns if col != 'All']].reset_index(drop=False)

        print(base)

        return base
