# Class Imports
import UI
import Label_Parser
import Datapreparatie2
import Vraag2
import NV
import NVGEM
import RCGEM
import NPS
import Top_Bot
import MV
import Stap2


# Library Imports
import pandas as pd
import os
import re


class Main:
    pd.set_option('display.max_columns', 500)

    def __init__(self):

        # Class Variables
        self._UI = UI.UI()
        self._label_parser = Label_Parser.LabelParser()
        self._dataprep = Datapreparatie2.DataPreparation()
        self._NV = NV.NV()
        self._NV_GEM = NVGEM.NVGEM()
        self._RC_GEM = RCGEM.RCGEM()
        self._NPS = NPS.NPS()
        self._TB = Top_Bot.TopBot()
        self._MV = MV.MV()
        self._step2 = Stap2.Step2()

        # String Variables
        self._directory = str()
        self._data_file = str()
        self._label_file = str()

        # Int Variables
        self._number_kvs = 0

        # List Variables
        self._background_vars = list()
        self._rejections = list()
        self._open_questions = list()
        self._kvs = list()
        self._kvs_names = list()
        self._titles = list()
        self._dataframe_list = list()
        self._top2_bot2s = list()

        # DataFrame Variables
        self._data = pd.DataFrame

        # Dictionary Variables
        self._syntax = Vraag2.Vraag.syntax

    def run(self) -> None:
        self._directory = self._UI.ask_path()
        # self._directory = r"C:\Users\mlobbes\Documents\Tabellen Script\Files"

        self._retrieve_files()

        # Define Background Variables and Data file
        self._background_vars = self._label_parser.run(filename=self._label_file)
        self._data, self._rejections = self._dataprep.run(filename=self._data_file)

        # Ask for Data Check
        data_check = self._UI.ask_for_data_check()
        self._data = self._data.drop(self._rejections).reset_index(drop=True) if data_check is True else self._data

        # Ask for Top2 Bot2
        self._top2_bot2s = self._TB.ask_for_top_bot2(ui_call=self._UI)
        self._top2_bot2s = self._TB.define_top_bot2(ui_call=self._UI, tb2=self._top2_bot2s)
        self._TB.parse_top_bot2(tb2=self._top2_bot2s)

        # Safe All Open Check
        self._open_questions = [k for k, v in self._syntax.items() if v.soort == 'OPEN']

        self._number_kvs = self._UI.ask_for_kv()
        self._kvs = self._UI.specify_kv(self._data.columns)
        self._kvs_names = self._UI.name_kv()

        # self._kvs = ['V1', 'V2']

        for kv in self._kvs:
            for var in self._background_vars:
                if var[1].split(" ")[2] == kv:
                    Vraag2.Vraag('AV', kv, kv, var[2].split("'")[1::2])

        print("Creating Tabellenboek.xlsx....")

        self._create_tables()
        self._step2.run(dfs=self._dataframe_list, names=self._titles, kvs=self._kvs, path_name=self._directory,
                        open_list=self._open_questions, data=self._data, kv_names=self._kvs_names)

    def _retrieve_files(self) -> None:
        files = os.listdir(self._directory)

        for file in files:

            if file.endswith(".csv"):
                self._data_file = self._directory + "\\" + file

            elif file.endswith(".SPS"):
                self._label_file = self._directory + "\\" + file

    def _create_tables(self):
        checkpoint_list = []

        key_list = [k for k, v in self._syntax.items() if v.soort != 'OPEN']

        for i in range(len(key_list)):

            question = key_list[i]
            title = self._syntax[question].vraagtekst

            if self._syntax[question].soort == 'NV':
                self._titles.append(title)
                self._titles.append(title)

                self._dataframe_list.extend(self._NV.convert(df=self._data[question].to_frame(),
                                                             kvs=self._kvs,
                                                             data=self._data))

            elif self._syntax[question].soort == 'NV/GEM':
                self._titles.append(title)
                self._titles.append(title)
                self._titles.append(title)

                self._dataframe_list.extend(self._NV_GEM.convert(df=self._data[question].to_frame(), kvs=self._kvs,
                                                                 data=self._data))

            elif self._syntax[question].soort == 'RC/GEM':
                self._titles.append(title)
                self._titles.append(title)

                self._dataframe_list.extend(self._RC_GEM.convert(df=self._data[question].to_frame(), kvs=self._kvs,
                                                                 data=self._data))

            elif self._syntax[question].soort == 'NPS':
                self._titles.append(title)

                self._dataframe_list.extend(self._NPS.convert(df=self._data[question].to_frame(), kvs=self._kvs,
                                                              data=self._data))

            elif 'Top' in self._syntax[question].soort:
                self._titles.append(title)
                self._titles.append(title)
                self._titles.append(title)
                self._titles.append(title)

                self._dataframe_list.extend(self._TB.convert(df=self._data[question].to_frame(), kvs=self._kvs,
                                                             data=self._data))

            elif self._syntax[question].soort == 'MR':
                if i < len(key_list) - 1 and \
                        self._syntax[key_list[i + 1]].soort == 'MR' and \
                        re.search('V(.*)_', key_list[i]).group(1) == re.search('V(.*)_', key_list[i + 1]).group(1):
                    checkpoint_list.append(self._data[key_list[i]].to_frame())

                else:
                    checkpoint_list.append(self._data[key_list[i]].to_frame())

                    self._dataframe_list.extend(self._MV.convert(df_list=checkpoint_list, kvs=self._kvs,
                                                                 data=self._data))
                    checkpoint_list = []

                if title not in self._titles:
                    self._titles.append(title)
                    self._titles.append(title)

        # Truncate Title Lengths
        for t in range(len(self._titles)):
            if len(self._titles[t]) >= 225:
                self._titles[t] = self._titles[t].replace(self._titles[t], self._titles[t][:254])


main_file = Main()
main_file.run()
