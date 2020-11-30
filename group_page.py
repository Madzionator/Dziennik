from Baza import sesja, Subject, Group, SubjectGroup
from group_add_edit import Group_Add, Group_Edit
from student_array_page import Students_array
import tkinter as tk
from tkinter import*
from tkinter import messagebox as msb

class Group_Choice(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text=subject.name, font = ("Calibri", 16)).grid(row = 0, columnspan=6, sticky=N+E+S+W)
        tk.Label(self, text="Grupy:", font = ("Calibri", 15)).grid(row = 1, columnspan=6, sticky=N+E+S+W)
        self.subject = subject
        self.group_list = tk.Listbox(self, font = ("Calibri", 14), width=100)
        self.group_list_object = []
        self.load_group()
        self.group_list.grid(row = 2, columnspan=6, sticky=N+E+S+W)

        self.group_choice = 0
        def GroupSelect(event):
            self.group_choice = self.get_group_choice()

        def SubjectOpen(event):
            self.group_choice = self.get_group_choice() 
            if self.group_choice != 0:
                self.master.navigate_to(Students_array, self.subject, self.group_choice)

        self.group_list.bind('<<ListboxSelect>>', GroupSelect)
        self.group_list.bind('<Double-1>', SubjectOpen)

        tk.Button(self, text="Otwórz", command= self.try_open, height=2).grid(row = 3, column=0, columnspan=2, sticky=N+E+S+W)
        tk.Button(self, text="Dodaj grupę", command=lambda: master.navigate_to(Group_Add, subject), height=2).grid(row = 3, column=4, columnspan=2, sticky=N+E+S+W)
        tk.Button(self, text="Edytuj", command= self.try_edit, height=2).grid(row = 3, column=2, columnspan=2, sticky=N+E+S+W)
        tk.Button(self, text="Usuń grupę z tego przedmiotu", command=self.delete_subject_here, height=2).grid(row = 4, column=0, columnspan=3, sticky=N+E+S+W)
        tk.Button(self, text="Usuń grupę całkowicie", command=self.delete_subject_everywhere, height=2).grid(row = 4, column=3, columnspan=3, sticky=N+E+S+W)
           
        tk.Button(self, text="Wróć", command=lambda: master.go_back(), font=("Calibri", 10), height=2).grid(row = 5, column=0, columnspan=2, sticky=N+E+S+W)

        for i in range(0, 6):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

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
        try:
            int_choice = self.group_list.curselection()[0]
            obj_choice = self.group_list_object[int_choice]
            return obj_choice
        except IndexError: 
            return 0

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