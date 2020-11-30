import tkinter as tk
from tkinter import messagebox as msb
from tkinter import*
from Baza import sesja, Subject
from subject_add_edit import Subject_Add, Subject_Edit
from group_page import Group_Choice

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Przedmioty: ", font = ("Calibri", 14)).grid(row=0, columnspan=2, sticky=N+E+S+W)

        self.subject_list = tk.Listbox(self, font = ("Calibri", 13), width=100)
        self.subject_obj_list = []
        self.load_subject()
        self.subject_list.grid(row=1, columnspan=2, sticky=N+E+S+W)

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

        tk.Button(self, text="Otwórz", command= self.try_open, height=2).grid(row=2, column=0, sticky=N+E+S+W, pady=3, padx=3)
        tk.Button(self, text="Edytuj", command= self.try_edit, height=2).grid(row=2, column=1, sticky=N+E+S+W, pady=3, padx=3)
        tk.Button(self, text="Dodaj nowy", command=lambda: master.navigate_to(Subject_Add), height=2).grid(row=3, column=0, sticky=N+E+S+W, pady=3, padx=3)
        tk.Button(self, text="Usuń", command=self.delete_subject, height=2).grid(row=3, column=1, sticky=N+E+S+W, pady=3, padx=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 1, uniform=True)

    def load_subject(self):
        self.subject_list.delete(0, tk.END)
        self.subject_obj_list = []
        i=0
        for subject in sesja.query(Subject).order_by(Subject.name).all():
            self.subject_obj_list.append(subject)
            self.subject_list.insert(i, subject.name)
            i+=1

    def get_choice(self):
        try:
            choice = self.subject_list.curselection()
            return self.subject_obj_list[choice[0]]
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