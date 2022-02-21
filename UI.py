from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Vraag2
import numpy as np
import pandas as pd
from tkscrolledframe import ScrolledFrame


class UI:

    def __init__(self):
        self._root = Tk()
        self._root.title("Powered By Datalab")
        self._root['bg'] = '#1fbcee'
        self._root.geometry('800x600')
        self._root.iconbitmap('favicon.ico')
        self._syntax = Vraag2.Vraag.syntax
        self._kv = str()

        self._directory = str()
        self._boolean = False
        self._kvs = 0

        self._background_vars = list()

        self._temp_dict = {}
        self._temp_dict2 = {}
        self._temp_dict3 = {}

        self.onthouden = []
        self.data = pd.DataFrame()

    def ask_path(self) -> str:
        picture = Image.open("MWM2WIT.png")
        my_img = ImageTk.PhotoImage(picture)
        my_label = Label(image=my_img, bg="#1fbcee")
        my_label.pack(pady=80)

        input_box = Entry(self._root, width=120)
        input_box.pack(pady=30)

        def my_click():
            self._directory = input_box.get()
            self._destroy_widgets()

        #my_button = Button(self._root, text="Fill in the path name ", command=my_click)
        my_button = Button(self._root, text="Bevestig Bestandsnaam",
                           command=my_click,
                           bg='#1fbcee',
                           fg='white',
                           bd='0',
                           font=('Trebuchet', 20),
                           activebackground='#46b6df')
        my_button.pack()

        self._root.mainloop()

        return self._directory

    def _destroy_widgets(self):
        for widget in self._root.winfo_children():
            widget.destroy()
        self._root.quit()

    def ask_for_data_check(self) -> bool:

        def my_click1():
            self._boolean = True
            self._destroy_widgets()

        def my_click2():
            self._boolean = False
            self._destroy_widgets()

        my_label = Label(self._root, text="Wil je een data check uitvoeren over jouw data?",
                         bg='#1fbcee',
                         fg='white',
                         font='Trebuchet')
        #my_label.place(x=240, y=100)
        my_label.pack(ipadx=10, ipady=100)

        my_button = Button(self._root, text="Ja, ik wil wel een data check uitvoeren",
                           command=my_click1,
                           bg='#004771',
                           fg='white',
                           bd='5',
                           font='Trebuchet',
                           activebackground='#46b6df')

        #my_button.place(x=10, y=200)
        my_button.pack(side=LEFT, expand=True)

        my_button2 = Button(self._root, text="Nee ik wil geen data check uitvoeren",
                            command=my_click2,
                            bg='#004771',
                            fg='white',
                            bd='5',
                            font='Trebuchet',
                            activebackground='#46b6df')
        #my_button2.place(x=520, y=200)
        my_button2.pack(side=RIGHT, expand=True)

        self._root.mainloop()

        return self._boolean

    def choose_top_bot_questions(self, schaalnummers: list) -> list:
        result = {}
        row, column = 1, 1

        for index, value in enumerate(schaalnummers):
            result[value] = IntVar()
            Checkbutton(self._root, text=value,
                        font="Trebuchet",
                        variable=result[value],
                        bg='#1fbcee', fg='white', selectcolor='#004771').grid(row=row, column=column)

            row = row + 1

            if index % 10 == 0 and index != 0:
                column = column + 1
                row = 1

        my_button = Button(self._root, text="Bevestig Top2/Bot2", command=self._destroy_widgets, bg="#004771",
                           fg="white", bd="5", font="Trebuchet", activebackground="#46b6df").place(x=320, y=500)



        self._root.mainloop()

        return [question for question in schaalnummers if result[question].get() == 1]

    def choose_type_top_bot(self, questions: list) -> list:
        event_list = []

        def new_selection(event):
            if event.widget.get().split(" ")[1][0] == "B":
                event_list.append((event.widget.get(), True))

            elif event.widget.get().split(" ")[1][0] == "T":
                event_list.append((event.widget.get(), False))

        y = 50
        for question in questions:
            x = 300

            my_label = Label(self._root, text=question[0], bg='#46b6df', fg='white', font="Trebuchet")
            my_label.place(x=x, y=y)

            x = x + 40

            my_combobox = ttk.Combobox(self._root, values=question[1:])
            my_combobox.place(x=x, y=y)
            my_combobox.bind("<<ComboboxSelected>>", new_selection)

            y = y + 30

        my_button = Button(self._root, text="Bevestig Soort Top2/Bot2",command=self._destroy_widgets,bg="#004771",
                           fg="white", bd="5", font="Trebuchet", activebackground="#46b6df").place(x=300, y=500)

        self._root.mainloop()

        return event_list

    def ask_for_kv(self) -> int:

        my_label = Label(self._root, text="Aantal Kruisvariabelen", bg='#1fbcee', fg='white', font="Trebuchet")
        #my_label.place(x=170, y=50)
        my_label.pack()

        def new_selection(event):
            self._kvs = int(event.widget.get())

        my_combobox = ttk.Combobox(self._root, values=list(range(0, 16)))
        #my_combobox.place(x=340, y=50)
        my_combobox.pack()
        my_combobox.bind("<<ComboboxSelected>>", new_selection)

        my_button = Button(self._root, text="Bevestig Aantal KV's", command=self._destroy_widgets, bg="#004771",
                           fg="white", bd="5", font="Trebuchet", activebackground="#46b6df").place(x=300, y=500)

        self._root.mainloop()

        return self._kvs

    def specify_kv(self, answers: list):
        result = {}
        event_list = []

        def new_selection(event):
            event_list.append(event.widget.get())

        y = 50
        for i in range(0, self._kvs):
            x = 300

            my_label = Label(self._root, text=f"KV{i+1}", bg='#46b6df', fg='white', font="Trebuchet")
            my_label.place(x=x, y=y)

            x = x + 50

            my_combobox = ttk.Combobox(self._root, values=list(answers))
            my_combobox.place(x=x, y=y)
            my_combobox.bind("<<ComboboxSelected>>", new_selection)

            y = y + 30

        my_button = Button(self._root, text="Bevestig KV's", command=self._destroy_widgets, bg="#004771",
                           fg="white", bd="5", font="Trebuchet", activebackground="#46b6df").place(x=340, y=500)

        self._root.mainloop()

        return event_list

    def name_kv(self):

        names = []

        y = 50

        entries = [Entry(self._root) for _ in range(0, self._kvs)]

        for i, entry in enumerate(entries):
            x = 300
            my_label = Label(self._root, text=f"KV{i + 1}", bg='#46b6df', fg='white', font="Trebuchet")
            my_label.place(x=x, y=y)

            x = x + 40

            entry.place(x=x, y=y)

            y = y + 30

        def save_names():
            for entry in entries:
                names.append(entry.get())
            self._destroy_widgets()


        my_button = Button(self._root, text="Bevestig Naam KV's", command=save_names, bg="#004771",
                            fg="white", bd="5", font="Trebuchet", activebackground="#46b6df").place(x=340, y=500)

        self._root.mainloop()

        return names

    def show_categories(self, event):

        current_x, current_y = 10, 75

        if event.widget.get():
            self._kv = event.widget.get()
            if self._kv in [var[1].split(" ")[2] for var in self._background_vars]:
                for v in self._background_vars:
                    if v[1].split(" ")[2] == self._kv:
                        Vraag2.Vraag('AV', f"{self._kv}_KV", f"{self._kv}_KV", v[2].split("'")[1::2])
                        break

        if self._kv in self._syntax:
            answer_list = self._syntax[self._kv].antwoorden
        else:
            answer_list = self._data[self._kv].unique()

        Label(self._root, text=f"{'Categorieen:'}", bg='#1fbcee', fg='white', font="Trebuchet").place(x=current_x,
                                                                                                      y=current_y)
        current_y = current_y + 150

        for k in self._temp_dict.keys():
            self._temp_dict[k].place_forget()
            self._temp_dict2[k].place_forget()

        for an in answer_list:
            self._temp_dict[an] = Label(self._root, text=f"{an}", bg='#1fbcee', fg='white', font="Trebuchet")
            self._temp_dict2[an] = Entry(self._root, width=40)
            if event.widget.get():
                self._temp_dict[an].place(x=current_x, y=current_y)
                self._temp_dict2[an].place(x=current_x+350, y=current_y)
                current_y = current_y + 25

            else:
                self._temp_dict[an].place_forget()
                self._temp_dict2[an].place_forget()

    def do_something(self):

        self._temp_dict2 = {key: val.get() for key, val in self._temp_dict2.items() if len(val.get()) != 0}


        # for k, v in self._temp_dict2.items():
        #     if len(v.get()) == 0:
        #         del self._temp_dict2[k]
        #     else:
        #         self._temp_dict2[k] = v.get()
        self._destroy_widgets()

    def specify_kv2(self, number: int, answers: list, backvar: list, data: pd.DataFrame()):
        self._data = data
        self._background_vars = backvar

        self._temp_dict = {}
        self._temp_dict2 = {}
        self._temp_dict3 = {}

        x, y = 10, 50

        my_label = Label(self._root, text=f"KV{number + 1}", bg='#1fbcee', fg='white', font="Trebuchet")
        my_label.place(x=x, y=y)

        x = x + 50

        my_combobox = ttk.Combobox(self._root, values=list(answers))
        my_combobox.place(x=x, y=y+5)
        my_combobox.bind("<<ComboboxSelected>>", self.show_categories)

        my_button = Button(self._root, text="Bevestig KV", command=self.do_something, bg="#004771",
                           fg="white", bd="5", font="Trebuchet", activebackground="#46b6df").place(x=340, y=500)

        self._root.mainloop()

        return self._temp_dict2, self._kv



