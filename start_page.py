import tkinter as tk
from tkinter import messagebox as msb
from Baza import sesja, Subject
from subject_add_edit import Subject_Add, Subject_Edit

def unpack(subject_list):
    finally_list = []
    for i in subject_list:
        finally_list.append(i[0])
    return finally_list

def unpack_choice(choice):
    finally_choice = choice[0]
    return finally_choice

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Przedmioty: ", font = 24).pack(anchor = 'w')

        self.subject_list = tk.Listbox(self, font = 2)
        self.load_subject()
        self.subject_list.pack(anchor = 'w')

        self.choice = 0
        def SubjectSelect(event):
            self.choice = self.get_choice()  # by name

        self.subject_list.bind('<<ListboxSelect>>', SubjectSelect)

        '''open_button = tk.Button(self, text="otwórz", width=20)
        open_button.pack(anchor = 'w')

        delete_button = tk.Button(self, text="usuń", width=20)
        delete_button.pack(anchor = 'w')'''

        tk.Button(self, text="Dodaj nowy", command=lambda: master.navigate_to(Subject_Add)).pack()
        tk.Button(self, text="Edytuj", command=lambda: master.navigate_to(Subject_Edit)).pack()
        tk.Button(self, text="Usuń", command=self.delete_subject).pack()

    def load_subject(self):
        self.subject_list.delete(0, tk.END)
        subjects = unpack(sesja.query(Subject.name).order_by(Subject.name).all())
        for i in range(len(subjects)):
            self.subject_list.insert(i, subjects[i])

    def get_choice(self):
        choice = unpack_choice(self.subject_list.curselection())
        subjects = unpack(sesja.query(Subject.name).order_by(Subject.name).all())
        str_choice = subjects[choice]
        return str_choice

    def on_back(self):
        self.load_subject()

    def delete_subject(self):
        if not self.choice:
            msb.showinfo(None, "Nie wybrano przedmiotu do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(Subject).filter(Subject.name==self.choice).delete()
            self.load_subject()
            self.choice = 0