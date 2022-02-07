import pandas as pd
import numpy as np
import Vraag2
import re
import math
from scipy.stats import norm


class TopBot:

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

        base = self._create_cross_tables()
        new_data = self._sort_answers(df=base)
        self._dataframe_list.append((new_data, 'NV'))

        sign_df = self._sign(df=new_data)
        self._dataframe_list.append((sign_df, 'SIG'))

        top1 = int(self._syntax[self._column].soort.split("'")[1][0]) - 1
        top2 = int(self._syntax[self._column].soort.split("'")[1][-1])

        bot1 = int(self._syntax[self._column].soort.split("'")[3][0]) - 1
        bot2 = int(self._syntax[self._column].soort.split("'")[3][-1])

        # Create top2bot
        top2bot2_list = []

        # Calculate top2
        top2 = new_data.iloc[top1:top2].sum()[1:].to_frame().transpose()

        # Calculate bot2
        bot2 = new_data.iloc[bot1:bot2].sum()[1:].to_frame().transpose()

        top2 = top2.append(bot2)
        top2['Properties (%)'] = ['Top-2', 'Bottom-2']

        # Move total column to the front
        top2 = top2[['Properties (%)'] + [col for col in top2.columns if col != 'Properties (%)']].reset_index(drop=True)

        top2.loc[len(top2)] = new_data.loc[len(new_data) - 1]

        self._dataframe_list.append((top2, 'Top2Bot2'))
        sign_df = self._sign(df=top2)
        self._dataframe_list.append((sign_df, 'SIG'))

        return self._dataframe_list

    def _sort_answers(self, df: pd.DataFrame) -> pd.DataFrame:

        given_answers = [str(x) for x in df[self._column][0:-1]]
        missing_answers = list(set(self._syntax[self._column].antwoorden) - set(given_answers))

        # Add Missing Answers To DataFrame
        for missing in missing_answers:
            df.loc[len(df)] = 0
            df.loc[len(df)-1, self._column] = missing

        # Move (N) Row to Bottom of DataFrame
        temp = df.iloc[-1]
        df.iloc[-1] = df.iloc[len(df)-len(missing_answers)-1]
        df.iloc[len(df)-len(missing_answers)-1] = temp

        data = pd.DataFrame(columns=[])

        if len(self._syntax[self._column].antwoorden) != 0:
            # Get Answers in the Right Order
            for answer in self._syntax[self._column].antwoorden:
                data = data.append(df.loc[df[self._column].astype(str) == answer])

            # Add (N) Row back and Rename Columns
            data = data.append(df.loc[df[self._column] == "(N)"]).reset_index(drop=True)
            data = data.rename(columns={self._column: 'Properties (%)', 'All': 'Totaal'})

            return data
        else:
            df = df.rename(columns={self._column: 'Properties (%)', 'All': 'Totaal'})
            return df

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
                    base.insert(len(base.columns), (col+(duplicate_counter*' ')), df[col])
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

    def ask_for_top_bot2(self, ui_call):
        potential_scale_questions = [k for k, v in self._syntax.items()
                                     if v.soort == 'NV' and (len(v.antwoorden) == 4 or len(v.antwoorden) == 5 or
                                                             len(v.antwoorden) == 6 or len(v.antwoorden) == 7)]

        scale_numbers = []

        for question in potential_scale_questions:
            if '_' in question:
                if re.search('(.*)_', question).group(1) not in scale_numbers:
                    scale_numbers.append(re.search('(.*)_', question).group(1))
            else:
                if question not in scale_numbers:
                    scale_numbers.append(question)

        return ui_call.choose_top_bot_questions(schaalnummers=scale_numbers)

    def define_top_bot2(self, ui_call, tb2):

        list_of_top_bots2 = [x.split(', ') for x in tb2]

        for question in list_of_top_bots2:
            for key in self._syntax.keys():
                if question[0] == key.partition("_")[0]:
                    answer_options = len(self._syntax[key].antwoorden)

            question.append(f"{question[0]} Top'1-2'-Bot'{answer_options - 1}-{answer_options}'")
            question.append(f"{question[0]} Top'1-2'-Bot'{answer_options - 2}-{answer_options - 1}'")
            question.append(f"{question[0]} Bot'1-2'-Top'{answer_options - 1}-{answer_options}'")

        return ui_call.choose_type_top_bot(questions=list_of_top_bots2)

    def parse_top_bot2(self, tb2):
        for question in tb2:
            number = question[0].split("'")[0].split(" ")[0]

            for question2 in self._syntax.keys():
                if number == question2.partition("_")[0]:

                    top = question[0].split("'")[1] if question[1] is False else question[0].split("'")[3]
                    bot = question[0].split("'")[3] if question[1] is False else question[0].split("'")[1]
                    top_bot = "Top'" + top + "'/" + "Bot'" + bot + "'"
                    self._syntax[question2].soort = top_bot

