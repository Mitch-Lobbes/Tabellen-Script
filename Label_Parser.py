from Vraag2 import Vraag
import re


class LabelParser:

    def __init__(self):
        self._label_file = str()
        self._syntax = []
        self._background_variables = []
        self._mr_dict = {}

    def run(self, filename: str) -> list:
        self._read_file(filename=filename)
        self._remove_white_lines()
        self._find_mr_questions()
        self._check_question_type()

        # for k, v in Vraag.syntax.items():
        #     print(k, v.soort)

        return self._background_variables

    def _read_file(self, filename: str) -> None:
        with open(filename, encoding="utf8") as file:
            test_list = file.readlines()[1:]

        size = len(test_list)
        idx_list = [idx + 1 for idx, val in
                    enumerate(test_list) if val == '\n']

        self._syntax = [test_list[i: j] for i, j in zip([0] + idx_list, idx_list +
                                                        ([size] if idx_list[-1] != size else []))]

    def _remove_white_lines(self) -> None:
        self._syntax = [[ele for ele in sub if ele != '\n'] for sub in self._syntax]

    def _find_mr_questions(self) -> None:
        lowest_number = float('inf')

        for question in self._syntax:

            if "MRSETS\n" in question:
                result = re.search('VARIABLES=(.*) VALUE', question[1]).group(1).split(" ")

                for element in result:
                    self._mr_dict[element] = question[1].split("'")[1::2][0]

                start_index = self._syntax.index(question) + 1
                del self._syntax[start_index - 1]
                del self._syntax[start_index - 1]

            elif question[1].split(" ")[2].startswith('V') is False and \
                    question[1].split(" ")[2].startswith('OPEN') is False:

                if self._syntax.index(question) <= lowest_number:
                    lowest_number = self._syntax.index(question)

        if lowest_number != float('inf'):
            self._background_variables = [i for i in self._syntax[lowest_number:]]
            Vraag('AV', 'AV', 0, lowest_number)
            self._syntax = self._syntax[0:lowest_number]

    def _check_question_type(self):

        name_list = [i[0].split(" ")[2] for i in self._syntax]
        questions = {key: None for key in name_list}

        for i in enumerate(self._syntax):

            if i[1][0].split(" ")[2] in self._mr_dict.keys():
                Vraag('MR', i[1][0].split(" ")[2], self._mr_dict[i[1][0].split(" ")[2]], i[1][0].split("'")[1::2])

            elif len(i[1]) == 3:
                Vraag('OPEN', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])

            elif "A2500" in i[1][2]:
                Vraag('OPEN', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])

            elif 'Scale' in i[1][1] and '_A' in i[1][0]:
                Vraag('NV/GEM', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])

            elif '_A' in i[1][0]:
                Vraag('Rangorde Vraagdeel', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])
                questions[str(list(questions.keys())[i[0]])] = 'Rangorde Vraagdeel'

            elif 'OPEN' in i[1][0] and questions[list(questions.keys())[i[0] - 1]] == 'Rangorde Vraagdeel':
                Vraag('NV/GEM', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])

            elif 'OPEN' in i[1][0]:
                Vraag('NV', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])

            elif 'Scale' in i[1][1]:
                Vraag('NV/GEM', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], [])

            elif i[1][3].split("'")[1::2][0] == '1' and i[1][3].split("'")[1::2][-1] == '10':
                Vraag('RC/GEM', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], i[1][3].split("'")[1::2])

            elif i[1][3].split("'")[1::2][0] == '0' and i[1][3].split("'")[1::2][-1] == '10':
                Vraag('NPS', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], i[1][3].split("'")[1::2])

            elif '_' in i[1][0]:
                Vraag('Schaal', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], i[1][3].split("'")[1::2])

            elif i[1][3].split("'")[1::2][0] == '1' and i[1][3].split("'")[1::2][1] == '2':
                Vraag('NV', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], i[1][3].split("'")[1::2])

            else:
                Vraag('NV', i[1][0].split(" ")[2], i[1][0].split("'")[1::2][0], i[1][3].split("'")[1::2])

        for k, v in Vraag.syntax.items():
            if Vraag.syntax[k].soort == 'Rangorde Vraagdeel':
                Vraag.syntax[k].soort = 'NV'
