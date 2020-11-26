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
        '''self.group_list = tk.Listbox(self, font = 2)
        self.load_group()
        self.group_list.pack(anchor = 'w')

        self.choice = 0
        def GroupSelect(event):
            self.choice = self.get_choice()
            print(self.choice)
        self.group_list.bind('<<ListboxSelect>>', GroupSelect)'''

        tk.Button(self, text="Return to start page",
                  command=lambda: master.go_back()).pack()


    def load_group(self):
        self.group_list.delete(0, tk.END)
        groups = unpack(sesja.query(Group.name).order_by(Group.name).all())   # zmien
        for i in range(len(groups)):
            self.group_list.insert(i, groups[i])

    def get_choice(self):
        choice = self.group_list.curselection()[0]
        groups = unpack(sesja.query(Group.name).order_by(Group.name).all())
        str_choice = groups[choice]
        return sesja.query(Group.id, Group.name).filter(Group.name == str_choice).one()