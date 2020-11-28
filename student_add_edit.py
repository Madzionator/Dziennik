from Baza import sesja, Group, Student
import tkinter as tk
from tkinter import messagebox as msb

class Student_Add(tk.Frame):
    def __init__(self, master, group):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Imię studenta: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.pack(anchor = 'w')

        tk.Label(self, text="Nazwisko studenta: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.pack(anchor = 'w')

        self.master = master
        self.group = group

        tk.Button(self, text="Zapisz", command = self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

    def save(self):
        first_name_str = self.first_name_entry.get()
        last_name_str = self.last_name_entry.get()

        if len(first_name_str)== 0 and len(last_name_str)== 0:
            msb.showwarning("Błąd", "Nie podano imienia i nazwiska.")
            return
        elif len(first_name_str)== 0:
            msb.showwarning("Błąd", "Nie podano imienia.")
            return
        elif len(first_name_str)== 0:
            msb.showwarning("Błąd", "Nie podano nazwiska.")
            return

        if len(first_name_str) > 20 and len(last_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone nazwy są za długie.")
            return
        elif len(first_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone imie jest za długie.")
            return
        elif len(last_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone nazwisko jest za długie.")
            return

        sesja.add(Student(first_name = first_name_str, last_name = last_name_str, group_id = self.group.id))
        sesja.commit()
        self.master.go_back()

class Student_Edit(tk.Frame):
    def __init__(self, master, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Zmień nazwę Grupy: ").pack(fill="x", pady = 4, anchor = 'w')
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, group.name)
        self.name_entry.pack(anchor = 'w')
        self.master = master
        self.group = group

        tk.Button(self, text="Zapisz", command = self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

    def save(self):
        name_str = self.name_entry.get()
        if len(name_str)==0 :
            msb.showwarning("Błąd", "Nie wprowadzono nazwy grupy.")
            return
        elif len(name_str)>100:
            msb.showwarning("Błąd", "Wprowadzona nazwa jest za długa.")
            return
        if name_str != self.group.name:
            exists = sesja.query(Subject.name).filter_by(name = name_str).scalar() # None
            if exists:
                msb.showwarning("Błąd", "Podana nazwa jest już zajęta.")
                return        
        sesja.query(Group).filter(Group.id == self.group.id).update({Group.name: name_str})
        sesja.commit()
        self.master.go_back()
