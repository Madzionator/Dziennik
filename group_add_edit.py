from Baza import sesja, Subject, Group, SubjectGroup
import tkinter as tk
from tkinter import messagebox as msb

class Group_Add(tk.Frame):
    def __init__(self, master, subject, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Podaj nazwę grupy: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(anchor = 'w')
        self.master = master
        self.subject = subject

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
        exists = sesja.query(Group.name).filter_by(name = name_str).scalar() # None
        if exists:
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
