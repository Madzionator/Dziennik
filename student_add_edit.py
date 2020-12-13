from Baza import sesja, Group, Student
import tkinter as tk
from tkinter import*
from tkinter import messagebox as msb

class Student_Add(tk.Frame):
    def __init__(self, master, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Dodaj studenta", font=("Calibri", 14)).grid(row = 0, columnspan=2)
        tk.Label(self, text="Imię studenta", font=("Calibri", 12)).grid(row = 1, columnspan=2)
        self.first_name_entry = tk.Entry(self, font=("Calibri", 12))
        self.first_name_entry.grid(row = 2, columnspan=2)

        tk.Label(self, text="Nazwisko studenta: ", font=("Calibri", 12)).grid(row = 3, columnspan=2)
        self.last_name_entry = tk.Entry(self, font=("Calibri", 12))
        self.last_name_entry.grid(row = 4, columnspan=2)

        self.master = master
        self.group = group

        tk.Button(self, text="✔ Zapisz", command = self.save, font=("Calibri", 10)).grid(row = 5, column=1, sticky=N + E + S + W, pady=3)
        tk.Button(self, text="⬅ Wróć", command=lambda: master.go_back(), font=("Calibri", 10)).grid(row = 5, column=0, sticky=N + E + S + W, pady=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

    def save(self):
        first_name_str = self.first_name_entry.get()
        last_name_str = self.last_name_entry.get()

        if len(first_name_str) == 0 and len(last_name_str) == 0:
            msb.showwarning("Błąd", "Nie podano imienia i nazwiska.")
            return
        elif len(first_name_str) == 0:
            msb.showwarning("Błąd", "Nie podano imienia.")
            return
        elif len(first_name_str) == 0:
            msb.showwarning("Błąd", "Nie podano nazwiska.")
            return

        if len(first_name_str) > 20 and len(last_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone nazwy są za długie.")
            return
        elif len(first_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone imie jest za długie.")
            return
        elif len(last_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone nazwisko jest za długie.")
            return

        sesja.add(Student(first_name = first_name_str, last_name = last_name_str, group_id = self.group.id))
        sesja.commit()
        self.master.go_back()

class Student_Edit(tk.Frame):
    def __init__(self, master, student):
        tk.Frame.__init__(self, master)
 
        self.master = master
        self.student = student

        tk.Label(self, text="Edytuj studenta", font=("Calibri", 14)).grid(row = 0, columnspan=2)
        tk.Label(self, text="Imię studenta", font=("Calibri", 12)).grid(row = 1, columnspan=2)
        self.first_name_entry = tk.Entry(self, font=("Calibri", 12))
        self.first_name_entry.grid(row = 2, columnspan=2)
        self.first_name_entry.insert(0, self.student.first_name)

        tk.Label(self, text="Nazwisko studenta: ", font=("Calibri", 12)).grid(row = 3, columnspan=2)
        self.last_name_entry = tk.Entry(self, font=("Calibri", 12))
        self.last_name_entry.grid(row = 4, columnspan=2)
        self.last_name_entry.insert(0, self.student.last_name)

        tk.Button(self, text="✔ Zapisz", command = self.save, font=("Calibri", 10)).grid(row = 5, column=1, sticky=N + E + S + W, pady=3)
        tk.Button(self, text="⬅ Wróć", command=lambda: master.go_back(), font=("Calibri", 10)).grid(row = 5, column=0, sticky=N + E + S + W, pady=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

    def save(self):
        first_name_str = self.first_name_entry.get()
        last_name_str = self.last_name_entry.get()

        if len(first_name_str) == 0 and len(last_name_str) == 0:
            msb.showwarning("Błąd", "Nie podano imienia i nazwiska.")
            return
        elif len(first_name_str) == 0:
            msb.showwarning("Błąd", "Nie podano imienia.")
            return
        elif len(first_name_str) == 0:
            msb.showwarning("Błąd", "Nie podano nazwiska.")
            return

        if len(first_name_str) > 20 and len(last_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone nazwy są za długie.")
            return
        elif len(first_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone imie jest za długie.")
            return
        elif len(last_name_str) > 20:
            msb.showwarning("Błąd", "Wprowadzone nazwisko jest za długie.")
            return
        
        sesja.query(Student).filter(Student.id == self.student.id).update({Student.first_name: first_name_str, Student.last_name: last_name_str})
        sesja.commit()
        self.master.go_back()
