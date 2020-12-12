from Baza import sesja, Student, Subject, Grade, GradeCategory
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import*
from tkinter import messagebox as msb

class Grade_Add(tk.Frame):
    def __init__(self, master, student, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Dodaj ocenę", font=("Calibri", 14)).grid(row = 0, columnspan=2)
        tk.Label(self, text="Wybierz kategorię i wagę oceny", font=("Calibri", 12)).grid(row = 1, columnspan = 2, sticky=N+E+S+W)
        self.student = student
        self.subject = subject
        self.master = master

        self.cb_value = tk.StringVar()     
        self.combobox_grade_categories = ttk.Combobox(self, textvariable = self.cb_value, state="readonly", font=("Calibri", 12))
        self.combobox_grade_categories.grid(row = 2, columnspan = 2, sticky=N+E+S+W)
        grade_categories_obj = []
        grade_categories = []
        for category in sesja.query(GradeCategory).all():
            grade_categories_obj.append(category)
            grade_categories.append(category.name)
        self.combobox_grade_categories['values'] = grade_categories
        self.combobox_grade_categories.current(0)
        self.category_choice = 1
        self.combobox_grade_categories.bind("<<ComboboxSelected>>", self.select_category)

        self.scale = Scale(self, from_ = 1, to = 10,  orient = HORIZONTAL, font=("Calibri", 12))
        self.scale.grid(row = 4, columnspan = 2, sticky=N+E+S+W)   

        tk.Label(self, text="Podaj ocenę", font=("Calibri", 12)).grid(row = 5, columnspan = 2, sticky=N+E+S+W)
        self.value_entry = tk.Entry(self, font=("Calibri", 12))
        self.value_entry.grid(row = 6, columnspan = 2, sticky=N+E+S+W)

        tk.Button(self, text="Zapisz", command=self.save, font=("Calibri", 10)).grid(row = 7, column = 1, sticky=N+E+S+W, pady=3)
        tk.Button(self, text="Wróć", command=lambda: master.go_back(), font=("Calibri", 10)).grid(row = 7, column = 0, sticky=N+E+S+W, pady=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 2, uniform=True)
    
    def select_category(self, event):
        str_choice = self.cb_value.get()
        int_choice = sesja.query(GradeCategory.id).filter(GradeCategory.name == str_choice).one()
        self.category_choice = int_choice[0]

    def save(self):

        value_str = self.value_entry.get()
        if len(value_str) == 0:
            msb.showwarning("Błąd", "Nie podano wartości oceny.")
            return

        try:
            value_float = float(value_str)
        except ValueError:
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return

        if value_float > 5 or value_float < 2 or not (value_float*2).is_integer():
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return
       
        grade_weight = self.scale.get()
        print (grade_weight)    ########################

        #### Add weight to base
        sesja.add(Grade(value = value_float, grade_category_id = self.category_choice, student_id = self.student.id, subject_id = self.subject.id))
        sesja.commit()
        self.master.go_back()
        
class Grade_Edit(tk.Frame):
    def __init__(self, master, student, subject, grade):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Edytuj ocenę", font=("Calibri", 14)).grid(row = 0, columnspan=2)
        tk.Label(self, text="Wybierz kategorię i wagę oceny", font=("Calibri", 12)).grid(row = 1, columnspan = 2, sticky=N+E+S+W)
        self.student = student
        self.subject = subject
        self.master = master
        self.grade = grade;

        self.cb_value = tk.StringVar()     
        self.combobox_grade_categories = ttk.Combobox(self, textvariable = self.cb_value, state="readonly", font=("Calibri", 12))
        self.combobox_grade_categories.grid(row = 2, columnspan = 2, sticky=N+E+S+W)
        grade_categories_obj = []
        grade_categories = []
        for category in sesja.query(GradeCategory).all():
            grade_categories_obj.append(category)
            grade_categories.append(category.name)
        self.combobox_grade_categories['values'] = grade_categories
        self.combobox_grade_categories.current(self.grade.grade_category_id-1)
        self.category_choice = grade.grade_category_id
        self.combobox_grade_categories.bind("<<ComboboxSelected>>", self.select_category)

        self.scale = Scale(self, from_ = 1, to = 10,  orient = HORIZONTAL, font=("Calibri", 12))
        self.scale.grid(row = 4, columnspan = 2, sticky=N+E+S+W)   

        tk.Label(self, text="Zmień ocenę", font=("Calibri", 12)).grid(row = 5, columnspan = 2, sticky=N+E+S+W)
        self.value_entry = tk.Entry(self, font=("Calibri", 12))
        self.value_entry.grid(row = 6, columnspan = 2, sticky=N+E+S+W)
        self.value_entry.insert(0, self.grade.value)

        tk.Button(self, text="Zapisz", command=self.save, font=("Calibri", 10)).grid(row = 7, column = 1, sticky=N+E+S+W, pady=3)
        tk.Button(self, text="Wróć", command=lambda: master.go_back(), font=("Calibri", 10)).grid(row = 7, column = 0, sticky=N+E+S+W, pady=3)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight = 2, uniform=True)

    def select_category(self, event):
        str_choice = self.cb_value.get()
        int_choice = sesja.query(GradeCategory.id).filter(GradeCategory.name == str_choice).one()
        self.category_choice = int_choice[0]

    def save(self):

        value_str = self.value_entry.get()
        if len(value_str) == 0:
            msb.showwarning("Błąd", "Nie podano wartości oceny.")
            return

        try:
            new_grade_value = float(value_str)
        except ValueError:
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return

        if new_grade_value > 5 or new_grade_value < 2 or not (new_grade_value*2).is_integer():
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return
       
        grade_weight = self.scale.get()
        print (grade_weight)    ########################

        #### Add weight to base
        sesja.query(Grade).filter(Grade.id == self.grade.id).update({Grade.value: new_grade_value, Grade.grade_category_id: self.category_choice})
        sesja.commit()
        self.master.go_back()