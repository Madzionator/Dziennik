from Baza import sesja, Student, Subject, Grade, GradeCategory
from grade_add_edit import Grade_Add, Grade_Edit
import tkinter as tk
from tkinter import*
from tkinter.simpledialog import askfloat
from tkinter import messagebox as msb

class Grade_Manager(tk.Frame):
    def __init__(self, master, student, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text= ("Oceny studenta: " + student.last_name + " " + student.first_name), font=("Calibri", 16)).grid(row = 0, columnspan = 3, sticky=N+S+W)
        self.student = student
        self.subject = subject

        self.grade_list = tk.Listbox(self, font = ("Calibri", 13), width=100)
        self.grade_list.grid(row = 1, columnspan=3)
        self.grade_list_obj = []
        self.load_grade()

        self.grade_choice = 0
        def GradeSelect(event):
            self.grade_choice = self.get_grade_choice() 

        def GradeEdit(event):
            self.grade_choice = self.get_grade_choice() 
            if self.grade_choice != 0:
                self.try_edit()

        self.grade_list.bind('<<ListboxSelect>>', GradeSelect)
        self.grade_list.bind('<Double-1>', GradeEdit)

        tk.Button(self, text="Dodaj", command=lambda: self.master.navigate_to(Grade_Add, self.student, self.subject), font=("Calibri", 10)).grid(row = 2, column = 0, sticky=N+E+S+W, pady=3, padx=3)
        tk.Button(self, text="Edytuj", command= self.try_edit, font=("Calibri", 10), height = 2).grid(row = 2, column = 1, sticky=N+E+S+W, pady=3, padx=3)
        tk.Button(self, text="Usuń", command= self.try_delete, font=("Calibri", 10), height = 2).grid(row = 2, column = 2, sticky=N+E+S+W, pady=3, padx=3)
        tk.Button(self, text="Wróć", command=lambda: master.go_back(), font=("Calibri", 10), height = 2).grid(row = 3, column = 0, sticky=N+E+S+W, pady=3, padx=3)

        for i in range(0, 3):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

    def load_grade(self):
        self.grade_list.delete(0, tk.END)
        self.grade_list_obj = []
        i = 0
        for grade in sesja.query(Grade).filter(Grade.student_id == self.student.id, Grade.subject_id == self.subject.id).all():
            category_name = sesja.query(GradeCategory.name).filter(GradeCategory.id == grade.grade_category_id).one()
            self.grade_list.insert(i, (str(grade.value) + " (" + category_name[0] + ")"))
            self.grade_list_obj.append(grade)
            i+=1

    def get_grade_choice(self):
        try:
            choice = self.grade_list.curselection()
            return self.grade_list_obj[choice[0]]
        except IndexError: 
            return 0

    def try_delete(self):
        if not self.grade_choice:
            msb.showinfo(None, "Nie wybrano oceny do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(Grade).filter(Grade.id==self.grade_choice.id).delete()
            self.load_grade()
            self.grade_choice = 0
            sesja.commit()

    def try_edit(self): # to do !!!
        if self.grade_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano oceny.")
            return
        self.master.navigate_to(Grade_Edit, self.subject, self.student, self.grade_choice)
