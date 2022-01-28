import pandas as pd
import Vraag2
import numpy as np
import math
from scipy.stats import norm


class MV:

    def __init__(self):
        self._df_list = []
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

    def convert(self, df_list: list, kvs: list, data: pd.DataFrame()) -> list:
        self._dataframe_list = []
        self._df_list = df_list
        self._kvs = kvs
        self._data = data

        n = 0
        mv_list = []

        for df in self._df_list:
            self._df = df

            for column in df:
                base = self._create_cross_tables()
                base = base.rename(columns={column: 'Properties (%)'})
                base.name = column
                n = base.loc[base['Properties (%)'] == '(N)'].iloc[0]
                mv_list.append(base)

        new_data = pd.DataFrame(columns=mv_list[0].columns)

        for element in mv_list:
            df = element.loc[element['Properties (%)'] == 1].reset_index(drop=True)
            df.name = element.name
            df.loc[0, 'Properties (%)'] = self._syntax[element.name].antwoorden[0]

            if len(df) != 0:
                new_data = new_data.append(df.iloc[0]).reset_index(drop=True)
            elif len(df) == 0:
                data = pd.DataFrame({"Properties (%)": self._syntax[df.name].antwoorden[0]}, index=[len(new_data)])
                new_data = new_data.append(data).reset_index(drop=True)

        new_data = new_data.replace(np.nan, 0)
        new_data = new_data.append(n).reset_index(drop=True)

        self._dataframe_list.append((new_data, 'MR'))
        sign_df = self._sign(df=new_data)
        self._dataframe_list.append((sign_df, 'SIG'))

        return self._dataframe_list

    def _create_cross_tables(self) -> pd.DataFrame:

        self._column = self._df.columns[0]

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

    def _sign(self, df: pd.DataFrame) -> pd.DataFrame:

        data = df.copy()
        data_df = data[data.columns[2:]]
        start = 0

        for kv in self._kvs:

            end = start + len(self._syntax[kv].antwoorden)
            kv_df = data_df[data_df.columns[start:end]]
            saved_columns = kv_df.columns

            for column in range(len(kv_df.columns)):
                kv_df = kv_df.rename(columns={kv_df.columns[column]: self._numeric_alpha_dict[column]})

            kv_df2 = pd.DataFrame(index=kv_df.index, columns=kv_df.columns)

            for i in range(len(kv_df.columns)):
                columns = list(kv_df.columns[0:i]) + list(kv_df.columns[i + 1:len(kv_df.columns)])

                for k in range(len(kv_df) - 1):
                    for col in columns:
                        x = kv_df[kv_df.columns[i]][k]
                        xn = kv_df[kv_df.columns[i]][len(kv_df) - 1]
                        y = kv_df[col][k]
                        yn = kv_df[col][len(kv_df) - 1]

                        if x != 0 and x != 1 and y != 0 and y != 1:
                            proportion = (x * xn + y * yn) / (xn + yn)
                            z_value = (x - y) / (math.sqrt((proportion * (1 - proportion)) * (1 / xn + 1 / yn)))
                            inv = norm.ppf(0.025)

                            if z_value > inv * -1:
                                kv_df2[kv_df2.columns[i]][k] = str(kv_df2[kv_df2.columns[i]][k]) + col
                            elif z_value < inv:
                                kv_df2[kv_df2.columns[i]][k] = str(kv_df2[kv_df2.columns[i]][k]) + col
                            else:
                                pass

            for k in range(len(kv_df2)):
                for col in kv_df2.columns:
                    if 'nan' in str(kv_df2[col][k]):
                        kv_df2[col][k] = str(kv_df2[col][k]).replace("nan", "")

            for c in range(len(kv_df2.columns)):
                kv_df2 = kv_df2.rename(columns={kv_df2.columns[c]: saved_columns[c]})

            for col in kv_df2.columns:
                data[col] = kv_df2[col]
            start = end

        return data
