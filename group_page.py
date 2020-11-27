from Baza import sesja, Subject, Group, SubjectGroup
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
            print("choice", self.group_choice)  #czemu nie string, halo (tymczasowo, ale mimo wszystko)
        self.group_list.bind('<<ListboxSelect>>', GroupSelect)
        
        tk.Button(self, text="Return to start page",
                  command=lambda: master.go_back()).pack()


    def load_group(self):
        i = 0
        self.group_list.delete(0, tk.END)
        self.group_list_object = []
        for group in sesja.query(Group).all():
            if sesja.query(SubjectGroup).filter(SubjectGroup.subject_id == self.subject.id, SubjectGroup.group_id == group.id).scalar():
                self.group_list.insert(0, group.name)
                self.group_list_object.append(group)

    def get_group_choice(self):
        choice = self.group_list.curselection()[0]
        str_choice = self.group_list_object[choice]
        print("wybor", str_choice)
        return str_choice
        #return sesja.query(Group.id, Group.name).filter(Group.name == str_choice).one()