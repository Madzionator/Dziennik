from Baza import sesja, Subject, Group, SubjectGroup
import tkinter as tk
from tkinter import messagebox as msb

class Subject_Add(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Podaj nazwę przedmiotu: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(anchor = 'w')

        self.all_groups = []
        self.groups_checkbox = []
        self.groups_checkbox_state = []
        self.master = master

        tk.Label(self, text="Wybierz przynależne grupy: ").pack(side="top", fill="x", pady = 4, anchor = 'w')

        for group in sesja.query(Group).all():
            var = tk.IntVar()
            self.all_groups.append(group)
            self.groups_checkbox.append(tk.Checkbutton(self, text=group.name, variable=var))
            self.groups_checkbox_state.append(var);
            
        for group in self.groups_checkbox:
            group.pack(anchor = 'w')

        tk.Button(self, text="Zapisz", command = self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

    def get_selected_groups(self):
        checked_groups = []
        for i in range(len(self.all_groups)):
            if self.groups_checkbox_state[i].get():
                checked_groups.append(self.all_groups[i])
        return checked_groups

    def save(self):
        name_str = self.name_entry.get()
        if len(name_str)==0 :
            msb.showwarning("Błąd", "Nie wprowadzono nazwy przedmiotu.")
            return
        elif len(name_str)>100:
            msb.showwarning("Błąd", "Wprowadzona nazwa jest za długa.")
            return
        exists = sesja.query(Subject.name).filter_by(name = name_str).scalar() # None
        if exists:
            msb.showwarning("Błąd", "Podana nazwa jest już zajęta.")
        else:
            sesja.add(Subject(name = name_str))
            id = sesja.query(Subject.id).filter_by(name = name_str).one()
            for x in self.get_selected_groups():
                sesja.add(SubjectGroup(subject_id = id[0], group_id = x.id))
            self.master.go_back()

class Subject_Edit(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Podaj nową nazwę przedmiotu: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(anchor = 'w')

        '''
        self.all_groups = []
        self.groups_checkbox = []
        self.groups_checkbox_state = []
        self.master = master

        tk.Label(self, text="Wybierz przynależne grupy: ").pack(side="top", fill="x", pady = 4, anchor = 'w')

        for group in sesja.query(Group).all():
            var = tk.IntVar()
            self.all_groups.append(group)
            self.groups_checkbox.append(tk.Checkbutton(self, text=group.name, variable=var))
            self.groups_checkbox_state.append(var);
            
        for group in self.groups_checkbox:
            group.pack(anchor = 'w')'''

        tk.Button(self, text="Zapisz", command = self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()
'''
    def get_selected_groups(self):
        checked_groups = []
        for i in range(len(self.all_groups)):
            if self.groups_checkbox_state[i].get():
                checked_groups.append(self.all_groups[i])
        return checked_groups

    def save(self):
        name_str = self.name_entry.get()
        if len(name_str)==0 :
            msb.showwarning("Błąd", "Nie wprowadzono nazwy przedmiotu.")
            return
        elif len(name_str)>100:
            msb.showwarning("Błąd", "Wprowadzona nazwa jest za długa.")
            return
        exists = sesja.query(Subject.name).filter_by(name = name_str).scalar() # None
        if exists:
            msb.showwarning("Błąd", "Podana nazwa jest już zajęta.")
        else:
            sesja.add(Subject(name = name_str))
            id = sesja.query(Subject.id).filter_by(name = name_str).one()
            for x in self.get_selected_groups():
                sesja.add(SubjectGroup(subject_id = id[0], group_id = x.id))
            self.master.go_back()'''