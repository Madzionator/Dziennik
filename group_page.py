from Baza import sesja, Subject, Group, SubjectGroup
from group_add_edit import Group_Add, Group_Edit
from register_page import Students_array
import tkinter as tk
from tkinter import messagebox as msb

def unpack(group_list):
    finally_list = []
    for i in group_list:
        finally_list.append(i[0])
    return finally_list

class Group_Choice(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text=subject.name, font = 2).pack(side="top", fill="x", anchor = 'w')
        tk.Label(self, text="Grupy:").pack(fill="x", pady=2, anchor = 'w')
        self.subject = subject
        self.group_list = tk.Listbox(self, font = 2)
        self.group_list_object = []
        self.load_group()
        self.group_list.pack(anchor = 'w')

        self.group_choice = 0
        def GroupSelect(event):
            self.group_choice = self.get_group_choice()

        self.group_list.bind('<<ListboxSelect>>', GroupSelect)

        tk.Button(self, text="Otwórz", command= self.try_open).pack()
        tk.Button(self, text="Dodaj nowy", command=lambda: master.navigate_to(Group_Add, subject)).pack()
        tk.Button(self, text="Edytuj", command= self.try_edit).pack()
        tk.Button(self, text="Usuń stąd grupę", command=self.delete_subject_here).pack()
        tk.Button(self, text="Usuń grupę całkowicie", command=self.delete_subject_everywhere).pack()
           
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()


    def load_group(self):
        i = 0
        self.group_list.delete(0, tk.END)
        self.group_list_object = []
        for group in sesja.query(Group).all():
            if sesja.query(SubjectGroup).filter(SubjectGroup.subject_id == self.subject.id, SubjectGroup.group_id == group.id).scalar():
                self.group_list.insert(i, group.name)
                self.group_list_object.append(group)
                i+=1

    def get_group_choice(self):
        int_choice = self.group_list.curselection()[0]
        obj_choice = self.group_list_object[int_choice]
        return obj_choice

    def try_edit(self):
        if self.group_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano grupy.")
            return
        self.master.navigate_to(Group_Edit, self.group_choice)

    def try_open(self):
        if self.group_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano przedmiotu.")
            return
        self.master.navigate_to(Students_array, self.subject, self.group_choice)

    def delete_subject_everywhere(self):
        if not self.group_choice:
            msb.showinfo(None, "Nie wybrano przedmiotu do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(Group).filter(Group.id==self.group_choice.id).delete()
            self.load_group()
            self.group_choice = 0
            sesja.commit()

    def delete_subject_here(self):
        if not self.group_choice:
            msb.showinfo(None, "Nie wybrano przedmiotu do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(SubjectGroup).filter(SubjectGroup.group_id == self.group_choice.id, SubjectGroup.subject_id == self.subject.id).delete()
            self.load_group()
            self.group_choice = 0
            sesja.commit()