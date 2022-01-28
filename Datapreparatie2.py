import numpy as np
import pandas as pd
from scipy import stats
import Vraag2
import re
from collections import Counter
from itertools import islice


class DataPreparation:

    def __init__(self):
        self._data = pd.DataFrame
        self._speed_runner_idx = list()
        self._syntax = Vraag2.Vraag.syntax
        self._straight_liners_idx = list()
        self._rejections_idx = list()

    def run(self, filename: str) -> (pd.DataFrame(), list):
        self._read_file(filename=filename)
        self._time_check()
        self._remove_html()
        self._scale_check()

        self._rejections_idx = [x for x in self._speed_runner_idx if x in self._straight_liners_idx]

        for k, v in self._syntax.items():
            if self._syntax[k].soort == 'Schaal':
                self._syntax[k].soort = 'NV'

        return self._data, self._rejections_idx

    def _read_file(self, filename: str) -> None:
        self._data = pd.read_csv(filename, sep=";").replace([-99, '-99'], np.nan)

    def _time_check(self) -> None:

        text = 'DOORLOOPTIJD' if 'DOORLOOPTIJD' in self._data.columns else 'DURATION'

        trimmed_mean = stats.trim_mean(self._data[text], 0.05 / 4)
        self._speed_runner_idx = list(self._data[self._data[text] <= trimmed_mean].index)

    def _remove_html(self):
        for col in self._data.columns:
            try:
                self._data[col] = self._data[col].str.replace('<[^<]+?>', '', regex=True)
            except:
                continue

    def _scale_check(self):
        self._data = self._data.drop(columns=self._data.columns[0:8], axis=1)
        scale_questions = [c for c in self._data.columns if c in self._syntax and self._syntax[c].soort == 'Schaal']
        scale_numbers = [re.search('V(.*)_', question).group(1) for question in scale_questions]
        counter = list(Counter(scale_numbers).values())

        listed_scale_questions = [list(islice(iter(scale_questions), elem)) for elem in counter]

        standard_devs = []

        for questions in listed_scale_questions:
            temp_dict = {}
            answer = self._syntax[questions[0]].antwoorden

            for index, value in enumerate(answer):
                temp_dict[value] = index

            df = self._data.applymap(lambda s: temp_dict.get(s) if s in temp_dict else s)
            standard_devs.append(df[questions].std(axis=1))

        dev_df = pd.concat(standard_devs, axis=1)
        dev_df = list(dev_df.std(axis=1))
        self._straight_liners_idx = [idx for idx, dev in enumerate(dev_df) if dev == 0]
