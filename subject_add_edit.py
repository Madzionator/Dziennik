from Baza import sesja, Subject, Group, SubjectGroup
import tkinter as tk
from tkinter import messagebox as msb

class Subject_Add(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Podaj nazwę przedmiotu: ").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(anchor = 'w')

        tk.Label(self, text="Wybierz przynależne grupy: ").pack(side="top", fill="x", pady = 4, anchor = 'w')

        self.groups = []
        for i in sesja.query(Group.name).all():
            var = tk.IntVar()
            self.groups.append(tk.Checkbutton(self, text=i, variable=var))
            
        for i in self.groups:
            i.pack(anchor = 'w')

        tk.Button(self, text="Zapisz", command = self.save).pack()
        tk.Button(self, text="Return to start page", command=lambda: master.go_back()).pack()

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
            print("git", name_str) #tymczasowo
            #for i in self.groups:
            #    print (i)


class Subject_Edit(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Edit").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.go_back()).pack()