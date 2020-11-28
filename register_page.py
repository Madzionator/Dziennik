from Baza import sesja, Subject, Group, SubjectGroup, Grade, GradeCategory
import tkinter as tk
#from tkinter import messagebox as msb

class Students_array(tk.Frame):
    def __init__(self, master, subject, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text=("Przedmiot: " + subject.name + "\nGrupa: " + group.name), font = 2).pack(fill="x", anchor = 'w')
        


        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

