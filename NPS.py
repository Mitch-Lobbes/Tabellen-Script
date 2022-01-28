import pandas as pd
import Vraag2
import numpy as np


class NPS:

    def __init__(self):
        self._df = pd.DataFrame
        self._data = pd.DataFrame

        self._column = str
        self._syntax = Vraag2.Vraag.syntax

        self._kvs = []
        self._dataframe_list = []
        self._alpha_numeric_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
                                    "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18,
                                    "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}
        self._numeric_alpha_dict = {value: key for (key, value) in self._alpha_numeric_dict.items()}

    def convert(self, df: pd.DataFrame, kvs: list, data: pd.DataFrame()) -> list:
        self._dataframe_list = []
        self._df = df
        self._kvs = kvs
        self._data = data
        self._column = self._df.columns[0]

        # Divide Answers in Categories
        criteria = [self._df[self._column].between(9, 10), self._df[self._column].between(7, 8),
                    self._df[self._column].between(0, 6)]
        values = ['Promoter', 'Passive', 'Detractor']
        self._df['category'] = np.select(criteria, values, 0)

        self._column = self._df.columns[1]
        base = self._create_cross_tables()
        self._column = self._df.columns[0]
        base = base.rename(columns={'category': self._column})

        new_data = self._sort_answers(values=values, df=base)

        # Calculate NPS
        NPS_list = ['NPS']

        for col in new_data.columns[1:]:
            promoter_score = new_data[col][0]
            detractor_score = new_data[col][2]
            NPS = round((promoter_score - detractor_score) * 100, 0)
            NPS_list.append(NPS)

        line = pd.DataFrame([NPS_list], columns=base.columns, index=[len(new_data)])
        new_data = pd.concat([new_data.iloc[:len(new_data) - 1],
                              line, new_data.iloc[len(new_data) - 1:]]).reset_index(drop=True)

        new_data = new_data.rename(columns={self._column: 'Net Promotor Score', 'All': 'Totaal'})
        self._dataframe_list.append((new_data, 'NPS'))

        return self._dataframe_list

    def _create_cross_tables(self) -> pd.DataFrame:

        list_ = []

        for i in range(len(self._kvs)):

            # Create Cross Table
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
        duplicate_counter = 0

        # Combine Crossings Together
        for df in list_:
            for col in df:
                if col in base.columns:
                    duplicate_counter = duplicate_counter + 1
                    base.insert(len(base.columns), (col + (duplicate_counter * ' ')), df[col])
                else:
                    base.insert(len(base.columns), col, df[col])

        # Remove Total Row if Only 1 Crossing
        base = base[base.index != 'All'] if len(self._kvs) == 1 else base

        # Create New Total Row and Calculate Percentages
        total = base.sum()
        base = (base / total).replace(np.nan, 0)
        total.name = '(N)'
        base = base.append(total.transpose())

        # Move Total Column to Front of Dataframe
        base = base[['All'] + [col for col in base.columns if col != 'All']].reset_index(drop=False)

        return base

    def _missing_answers(self, df: pd.DataFrame) -> pd.DataFrame:
        missing_answers = list(set(self._syntax[df.columns.name].antwoorden) - set(df.columns))

        for missing in missing_answers:
            df[missing] = 0

        return df

    def _sort_answers(self, values: list, df: pd.DataFrame):

        given_answers = list(df[self._column][0:-1])
        missing_answers = list(set(values) - set(given_answers))

        # Add Missing Answers To DataFrame
        for missing in missing_answers:
            df.loc[len(df)] = 0
            df.loc[len(df)-1, self._column] = missing

        # Move (N) Row to Bottom of DataFrame
        temp = df.iloc[-1]
        df.iloc[-1] = df.iloc[len(df) - len(missing_answers) - 1]
        df.iloc[len(df) - len(missing_answers) - 1] = temp

        data = pd.DataFrame(columns=[])

        # Get Answers in the Right Order
        for element in values:
            x = df.loc[df[self._column].astype(str) == element]
            data = data.append(x)

        # Add (N) Row back and Rename Columns
        data = data.append(df.loc[df[self._column] == "(N)"]).reset_index(drop=True)

        return data
