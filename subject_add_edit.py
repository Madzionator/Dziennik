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

        for group in sesja.query(Group).all():
            var = tk.IntVar()
            self.all_groups.append(group)
            self.groups_checkbox.append(tk.Checkbutton(self, text=group.name, variable=var))
            self.groups_checkbox_state.append(var);

        if len(self.all_groups) > 0:
            tk.Label(self, text="Wybierz przynależne grupy: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
            
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
            sesja.add(Subject(name = name_str, groups=self.get_selected_groups()))
            sesja.commit()
            self.master.go_back()

class Subject_Edit(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Zmień nazwę przedmiotu: ").pack(fill="x", pady = 4, anchor = 'w')
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, subject.name)
        self.name_entry.pack(anchor = 'w')
        self.master = master
        self.subject = subject
        
        self.all_groups = []
        self.groups_checkbox = []
        self.groups_checkbox_state = []

        tk.Label(self, text="Wybierz przynależne grupy: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        
        i = 0
        for group in sesja.query(Group).all():
            var = tk.IntVar()
            self.all_groups.append(group)
            self.groups_checkbox.append(tk.Checkbutton(self, text=group.name, variable=var))
            if sesja.query(SubjectGroup.group_id).filter(SubjectGroup.subject_id == subject.id, SubjectGroup.group_id == group.id).scalar():
                self.groups_checkbox[i].select()
            self.groups_checkbox_state.append(var);
            i+=1
            
        for group in self.groups_checkbox:
            group.pack(anchor = 'w')

        tk.Button(self, text="Zapisz", command = self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

    def get_selected_groups(self):
        selected_groups = []
        for i in range(len(self.all_groups)):
            if self.groups_checkbox_state[i].get():
                selected_groups.append(self.all_groups[i])
        return selected_groups

    def save(self):
        name_str = self.name_entry.get()
        if len(name_str)==0 :
            msb.showwarning("Błąd", "Nie wprowadzono nazwy przedmiotu.")
            return
        elif len(name_str)>100:
            msb.showwarning("Błąd", "Wprowadzona nazwa jest za długa.")
            return
        if name_str != self.subject.name:
            exists = sesja.query(Subject.name).filter_by(name = name_str).scalar() # None
            if exists:
                msb.showwarning("Błąd", "Podana nazwa jest już zajęta.")
                return        
        sesja.query(Subject).filter(Subject.id == self.subject.id).update({Subject.name: name_str})

        sesja.query(SubjectGroup.group_id).filter(SubjectGroup.subject_id==self.subject.id).delete()
        for group in self.get_selected_groups():
            sesja.add(SubjectGroup(subject_id=self.subject.id, group_id=group.id))
        sesja.commit()
        self.master.go_back()