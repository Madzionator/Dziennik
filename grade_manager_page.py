from Baza import sesja, Student, Subject
import tkinter as tk

class Grade_Manager(tk.Frame):
    def __init__(self, master, student, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text= ("Oceny studenta: " + student.last_name + " " + student.first_name)).pack(side="top", fill="x", pady = 4, anchor = 'w')

        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()
