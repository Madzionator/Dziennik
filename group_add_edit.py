from Baza import sesja, Subject, Group, SubjectGroup
import tkinter as tk
from tkinter import*
from tkinter import messagebox as msb

class Group_Add(tk.Frame):
    def __init__(self, master, subject, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Podaj nazwę grupy: ", font=("Calibri", 12)).grid(row = 0, columnspan=2, sticky=N + E + S + W)
        self.name_entry = tk.Entry(self, font=("Calibri", 12))
        self.name_entry.grid(row = 1, columnspan=2, sticky=N + E + S + W)
        self.master = master
        self.subject = subject

        tk.Button(self, text="✔ Zapisz", command = self.save).grid(row = 2, column=1, sticky=N + E + S + W, pady=3)
        tk.Button(self, text="⬅ Wróć", command=lambda: master.go_back()).grid(row = 2, column=0, sticky=N + E + S + W, pady=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

    def save(self):
        name_str = self.name_entry.get()
        if len(name_str) == 0 :
            msb.showwarning("Błąd", "Nie wprowadzono nazwy grupy.")
            return
        elif len(name_str) > 100:
            msb.showwarning("Błąd", "Wprowadzona nazwa jest za długa.")
            return
        if sesja.query(Group.name).filter_by(name = name_str).scalar():
            msb.showwarning("Błąd", "Podana nazwa jest już zajęta.")
        else:
            sesja.add(Group(name = name_str))
            id = sesja.query(Group.id).filter(Group.name == name_str).one()
            sesja.add(SubjectGroup(group_id = id[0], subject_id = self.subject.id))
            sesja.commit()
            self.master.go_back()

class Group_Edit(tk.Frame):
    def __init__(self, master, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Zmień nazwę Grupy: ", font=("Calibri", 12)).grid(row = 0, columnspan=2, sticky=N + E + S + W)
        self.name_entry = tk.Entry(self, font=("Calibri", 12))
        self.name_entry.insert(0, group.name)
        self.name_entry.grid(row = 1, columnspan=2, sticky=N + E + S + W)
        self.master = master
        self.group = group

        tk.Button(self, text="✔ Zapisz", command = self.save).grid(row = 2, column=1, sticky=N + E + S + W, pady=3)
        tk.Button(self, text="⬅ Wróć", command=lambda: master.go_back()).grid(row = 2, column=0, sticky=N + E + S + W, pady=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

    def save(self):
        name_str = self.name_entry.get()
        if len(name_str) == 0 :
            msb.showwarning("Błąd", "Nie wprowadzono nazwy grupy.")
            return
        elif len(name_str) > 100:
            msb.showwarning("Błąd", "Wprowadzona nazwa jest za długa.")
            return
        if name_str != self.group.name:
            if sesja.query(Group.name).filter_by(name = name_str).scalar():
                msb.showwarning("Błąd", "Podana nazwa jest już zajęta.")
                return        
        sesja.query(Group).filter(Group.id == self.group.id).update({Group.name: name_str})
        sesja.commit()
        self.master.go_back()
