import tkinter as tk
from tkinter import messagebox as msb
from Baza import sesja, Subject
from subject_add_edit import Subject_Add, Subject_Edit
from group_page import Group_Choice

def unpack(subject_list):
    finally_list = []
    for i in subject_list:
        finally_list.append(i[0])
    return finally_list

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Przedmioty: ", font = 24).pack(anchor = 'w')

        self.subject_list = tk.Listbox(self, font = 2)
        self.load_subject()
        self.subject_list.pack(anchor = 'w')

        self.choice = 0
        def SubjectSelect(event):
            self.choice = self.get_choice() 

        def SubjectOpen(event):
            self.choice = self.get_choice() 
            if self.choice != 0:
                self.master.navigate_to(Group_Choice, self.choice)

        self.subject_list.bind('<<ListboxSelect>>', SubjectSelect)
        self.subject_list.bind('<Double-1>', SubjectOpen)
        self.master = master

        tk.Button(self, text="Otwórz", command= self.try_open).pack()
        tk.Button(self, text="Dodaj nowy", command=lambda: master.navigate_to(Subject_Add)).pack()
        tk.Button(self, text="Edytuj", command= self.try_edit).pack()
        tk.Button(self, text="Usuń", command=self.delete_subject).pack()

    def load_subject(self):
        self.subject_list.delete(0, tk.END)
        subjects = unpack(sesja.query(Subject.name).order_by(Subject.name).all())
        for i in range(len(subjects)):
            self.subject_list.insert(i, subjects[i])

    def get_choice(self):
        try:
            choice = self.subject_list.curselection()
            subjects = unpack(sesja.query(Subject.name).order_by(Subject.name).all())
            str_choice = subjects[choice[0]]
            return sesja.query(Subject.id, Subject.name).filter(Subject.name == str_choice).one()
        except IndexError: 
            return 0

    def delete_subject(self):
        if not self.choice:
            msb.showinfo(None, "Nie wybrano przedmiotu do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(Subject).filter(Subject.name==self.choice.name).delete()
            self.load_subject()
            self.choice = 0
            sesja.commit()

    def try_edit(self):
        if self.choice == 0:
            msb.showwarning("Błąd", "Nie wybrano przedmiotu.")
            return
        self.master.navigate_to(Subject_Edit, self.choice)

    def try_open(self):
        if self.choice == 0:
            msb.showwarning("Błąd", "Nie wybrano przedmiotu.")
            return
        self.master.navigate_to(Group_Choice, self.choice)