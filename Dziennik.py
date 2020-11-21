
import tkinter as tk

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dziennik")
        self.label_1 = tk.Label(self.root, text = "Przedmioty: ")
        self.label_1.pack()

        self.subject_list = tk.Listbox()
        self.subject_list.pack()

        for item in Data.subject_list:
            self.subject_list.insert(0, item)

        self.root.mainloop()

class Subject(Data):
    def __init__(self, name):
        subject_name = name

class Group(Subject):
    def __iniy__(self, name):
        group_name = name

class Student(Group):
    def __init__(self, first, last):
        first_name = first
        last_name = last

app = Application()
