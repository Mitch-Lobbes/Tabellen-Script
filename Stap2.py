import pandas as pd
import xlsxwriter.worksheet
import Vraag2


class Step2:

    def __init__(self):
        self._dataframe_list = []
        self._titles = []
        self._kvs = []
        self._open_questions = []
        self._directory = ""

        self._data = pd.DataFrame

        self._workbook = xlsxwriter.workbook.Workbook
        self._start_tab = xlsxwriter.worksheet.Worksheet
        self._data_tab = xlsxwriter.worksheet.Worksheet
        self._open_tab = xlsxwriter.worksheet.Worksheet

        self._title_row = 0
        self._df_row = 1
        self._hyperlink = 10

        self._syntax = Vraag2.Vraag.syntax
        self._writer = pd.ExcelWriter

        self._alpha_numeric_dict = {"A": 1,"B": 2, "C": 3,"D": 4, "E": 5,"F": 6,"G": 7,"H": 8,"I": 9,"J": 10,
                                    "K": 11,"L": 12,"M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18,"S": 19,
                                    "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, "AA": 27, "AB": 28,
                                    "AC": 29, "AD": 30, "AE": 31, "AF": 32, "AG": 33,  "AH": 34, "AI": 35, "AJ": 36,
                                    "AK": 37, "AL": 38,"AM": 39, "AN": 40, "AO": 41, "AP": 42, "AQ": 43, "AR": 44,
                                    "AS": 45, "AT": 46,  "AU": 47, "AV": 48, "AW": 49, "AX": 50, "AY": 51, "AZ": 51, }

        self._numeric_alpha_dict = {value: key for (key, value) in self._alpha_numeric_dict.items()}

    def run(self, dfs: list, names: list, kvs: list, path_name: str, open_list: list, data: pd.DataFrame):
        self._dataframe_list = dfs
        self._titles = names
        self._kvs = kvs
        self._directory = path_name
        self._open_questions = open_list
        self._data = data

        output_path = f"{self._directory}\Tabellenboek.xlsx"
        self._writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

        self._workbook = self._writer.book
        self._start_tab = self._workbook.add_worksheet('Openingsscherm')
        self._data_tab = self._workbook.add_worksheet('Data')
        self._open_tab = self._workbook.add_worksheet('Tabellen Open')

        self._create_start_screen()
        self._write_tables()
        self._create_open_tables()
        self._writer.save()

    def _create_open_tables(self):
        self._kvs.extend(self._open_questions)

        df = self._data[self._kvs]
        (max_row, max_col) = df.shape
        start_row_df = 0
        start_col_df = -1

        self._open_tab.set_row(0, 50)
        self._open_tab.set_column(0, 30, 25)

        column_settings = []
        for j in self._kvs:
            column_settings.append({'header': j + ":    " + self._syntax[j].vraagtekst})
            start_col_df = start_col_df + 1
            start_row_df = 0
            self._open_tab.write(start_row_df, start_col_df, self._syntax[j].vraagtekst)
            start_row_df = start_row_df + 1
            for i in range(len(df)):
                try:
                    self._open_tab.write(start_row_df, start_col_df, df[j][i])
                    start_row_df = start_row_df + 1
                except:
                    self._open_tab.write(start_row_df, start_col_df, ' ')
                    start_row_df = start_row_df + 1

        self._open_tab.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    def _write_tables(self):

            # All Formats
            title_format = self._workbook.add_format({'bold': True, 'font_size': 9})
            merge_format = self._workbook.add_format({'bold': False, 'border': 1, 'font_size': 9, 'color': 'white',
                                                      'align': 'center', 'valign': 'vcenter', 'fg_color': '#46b6df'})

            header_format = self._workbook.add_format({'bold': False, 'font_size': 9, 'color': 'white',
                                                       'fg_color': '#46b6df', 'border': 1, 'top': 5})
            header_format2 = self._workbook.add_format({'bold': False, 'font_size': 9, 'color': 'white',
                                                        'fg_color': '#46b6df', 'border': 1, 'top': 5, 'right': 5})

            hyperlink_format = self._workbook.add_format({'color': '#0563C1', 'underline': True})

            bottom_format2 = self._workbook.add_format({'right': 1, 'bottom': 5, 'font_size': 9})
            bottom_format2.set_align('left')

            bottom_format22 = self._workbook.add_format({'right': 1, 'bottom': 5, 'font_size': 9})
            bottom_format22.set_align('Center')

            bottom_fmt2 = self._workbook.add_format({'bottom': 5, 'right': 5, 'font_size': 9})
            bottom_fmt2.set_align('Center')

            tekst_begin_fmt = self._workbook.add_format({'right': 1, 'font_size': 9})
            tekst_begin_fmt.set_align('left')

            percent_tussen_fmt = self._workbook.add_format({'num_format': '0%', 'right': 1, 'font_size': 9})
            percent_tussen_fmt.set_align('Center')

            percent_fmt = self._workbook.add_format({'num_format': '0%', 'right': 5, 'font_size': 9})
            percent_fmt.set_align('Center')

            semi_onder_fmt = self._workbook.add_format({'right': 1, 'font_size': 9})
            semi_onder_fmt.set_align('Center')

            bottom_fmt3 = self._workbook.add_format({'right': 5, 'font_size': 9})
            bottom_fmt3.set_align('Center')


            self._data_tab.set_column(0, 0, 30)
            self._data_tab.set_column(2, 20, 12)


            # Start Loop
            for i in range(len(self._dataframe_list)):

                # Define Question Type
                question_type = self._dataframe_list[i][1]

                # Define Starting Cell of Crossings
                kv_cell_begin = 'C'

                if question_type == 'NV':

                    # Write Question Title
                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:

                        # Define Ending Cell of Crossings
                        kv_cell_end = self._numeric_alpha_dict[self._alpha_numeric_dict[kv_cell_begin] +
                                                               len(self._syntax[kv].antwoorden) - 1]

                        # Merge Crossing Title
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)

                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    # Write Column Titles
                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)
                    self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)

                    # Write Hyperlink
                    self._start_tab.write(self._hyperlink, 3, '=HYPERLINK("#Data!A' + str(self._title_row + 1) + '", ' + '"'
                                          + self._titles[i] + '")', hyperlink_format)
                    self._hyperlink = self._hyperlink + 1

                    # Write Data
                    for j in range(len(self._dataframe_list[i][0])):

                        # If Last Row of Table
                        if j == len(self._dataframe_list[i][0]) - 1:

                            # Write All Answers & (N)
                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], bottom_format2)
                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1,
                                                 self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j], bottom_fmt2)

                        else:
                            # All Other Rows

                            # Write All Answers & (%'s
                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], tekst_begin_fmt)
                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j],
                                                     percent_tussen_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1,
                                                 self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j], percent_fmt)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

                elif question_type == "SIG":
                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:
                        kv_cell_end = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden) - 1]
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)
                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        if element[0] - 1 >= 1:
                            self._data_tab.write(self._df_row, element[0],
                                            self._dataframe_list[i][0].columns[element[0]] + " (" + self._numeric_alpha_dict[element[0] - 1] + ")",
                                            header_format)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1,
                                            self._dataframe_list[i][0].columns[-1] + " (" + self._numeric_alpha_dict[element[0]] + ")",
                                            header_format2)
                        else:
                            self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)

                    for j in range(len(self._dataframe_list[i][0])):
                        if j == len(self._dataframe_list[i][0]) - 1:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], bottom_format2)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt2)

                        else:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], tekst_begin_fmt)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], percent_tussen_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            percent_fmt)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

                elif question_type == 'NPS':

                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:
                        kv_cell_end = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden) - 1]
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)
                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)

                    self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)

                    self._start_tab.write(self._hyperlink, 3,
                                     '=HYPERLINK("#Data!A' + str(self._title_row + 1) + '", ' + '"' + self._titles[i] + '")',
                                     hyperlink_format)
                    self._hyperlink = self._hyperlink + 1

                    for j in range(len(self._dataframe_list[i][0])):
                        if j == len(self._dataframe_list[i][0]) - 1:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Net Promotor Score'][j], bottom_format2)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt2)

                        elif j == len(self._dataframe_list[i][0]) - 2:
                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Net Promotor Score'][j], tekst_begin_fmt)
                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], semi_onder_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt3)

                        else:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Net Promotor Score'][j], tekst_begin_fmt)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], percent_tussen_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            percent_fmt)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

                elif question_type == 'RC':

                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:
                        kv_cell_end = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden) - 1]
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)
                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)

                    self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)
                    self._start_tab.write(self._hyperlink, 3,
                                     '=HYPERLINK("#Data!A' + str(self._title_row + 1) + '", ' + '"' + self._titles[i] + '")',
                                     hyperlink_format)
                    self._hyperlink = self._hyperlink + 1

                    for j in range(len(self._dataframe_list[i][0])):

                        if j == len(self._dataframe_list[i][0]) - 1:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], bottom_format2)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt2)

                        else:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], tekst_begin_fmt)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], percent_tussen_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            percent_fmt)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

                elif question_type == 'GEM':

                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:
                        kv_cell_end = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden) - 1]
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)
                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)

                    self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)

                    for j in range(len(self._dataframe_list[i][0])):

                        if j == len(self._dataframe_list[i][0]) - 1:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Gemiddelde'][j], bottom_format2)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt2)

                        else:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Gemiddelde'][j], tekst_begin_fmt)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, round(self._dataframe_list[i][0][element[1]][j], 1),
                                                semi_onder_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1,
                                            round(self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j], 1), bottom_fmt3)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

                elif question_type == 'MR':

                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:
                        kv_cell_end = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden) - 1]
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)
                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)

                    self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)
                    self._start_tab.write(self._hyperlink, 3,
                                     '=HYPERLINK("#Data!A' + str(self._title_row + 1) + '", ' + '"' + self._titles[i] + '")',
                                     hyperlink_format)
                    self._hyperlink = self._hyperlink + 1

                    for j in range(len(self._dataframe_list[i][0])):
                        if j == len(self._dataframe_list[i][0]) - 1:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], bottom_format2)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt2)

                        else:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], tekst_begin_fmt)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], percent_tussen_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            percent_fmt)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

                elif "Top" in question_type:

                    self._data_tab.write(self._title_row, 0, self._titles[i], title_format)

                    for kv in self._kvs:
                        kv_cell_end = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden) - 1]
                        merge = kv_cell_begin + str(self._df_row) + ":" + kv_cell_end + str(self._df_row)
                        self._data_tab.merge_range(merge, self._syntax[kv].vraagtekst, merge_format)
                        kv_cell_begin = self._numeric_alpha_dict[
                            self._alpha_numeric_dict[kv_cell_begin] + len(self._syntax[kv].antwoorden)]

                    for element in enumerate(self._dataframe_list[i][0].columns[:-1]):
                        self._data_tab.write(self._df_row, element[0], self._dataframe_list[i][0].columns[element[0]], header_format)

                    self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1, self._dataframe_list[i][0].columns[-1], header_format2)

                    for j in range(len(self._dataframe_list[i][0])):
                        if j == len(self._dataframe_list[i][0]) - 1:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], bottom_format2)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j], bottom_format22)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1,
                                            self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            bottom_fmt2)

                        else:

                            self._df_row = self._df_row + 1
                            self._data_tab.write(self._df_row, 0, self._dataframe_list[i][0]['Properties (%)'][j], tekst_begin_fmt)

                            for element in enumerate(self._dataframe_list[i][0].columns[1:-1]):
                                self._data_tab.write(self._df_row, element[0] + 1, self._dataframe_list[i][0][element[1]][j],
                                                percent_tussen_fmt)
                            self._data_tab.write(self._df_row, len(self._dataframe_list[i][0].columns) - 1,
                                            self._dataframe_list[i][0][self._dataframe_list[i][0].columns[-1]][j],
                                            percent_fmt)

                    self._df_row = self._df_row + 3
                    self._title_row = self._title_row + len(self._dataframe_list[i][0]) + 3

    def _create_start_screen(self):

        # Hide Gridlines
        self._start_tab.hide_gridlines(2)

        # Define Formats
        format_1 = self._workbook.add_format({'color': '#46b6df', 'font_size': 16, 'font': 'Calibri', 'bold': True})
        format_2 = self._workbook.add_format({'font_size': 11, 'font': 'Calibri', 'bold': False})

        # Set Columns Lengths
        self._start_tab.set_column(0, 1, 10.36)
        self._start_tab.set_column(1, 2, 90.09)
        self._start_tab.set_column(2, 3, 8.55)
        self._start_tab.set_column(3, 4, 75.36)

        # Read Script
        my_script = open("Openingsscherm_tekst", "r")
        my_script = my_script.readlines()

        # Print Script
        for i in range(9, 27):
            if i == 9:
                self._start_tab.write(i, 1, my_script[i - 9], format_1)
            elif i == 21:
                self._start_tab.write(i, 1, my_script[i - 9], format_1)
            else:
                self._start_tab.write(i, 1, my_script[i-9], format_2)

        # Insert Image
        self._start_tab.insert_image('B3', 'MWM2_Startscherm.png')

        # Hide Headers
        self._start_tab.hide_row_col_headers()





