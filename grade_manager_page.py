from Baza import sesja, Student, Subject, Grade, GradeCategory
import tkinter as tk
import tkinter.ttk as ttk
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

    def try_edit(self):
        if self.grade_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano oceny.")
            return
        new_grade_value = askfloat(None, "Podaj nową wartość oceny")
        if new_grade_value == None:
            return
        if new_grade_value > 5 or new_grade_value < 2 or not (new_grade_value*2).is_integer():
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return
        sesja.query(Grade).filter(Grade.id == self.grade_choice.id).update({Grade.value: new_grade_value})
        sesja.commit()
        self.load_grade()

class Grade_Add(tk.Frame):
    def __init__(self, master, student, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Wybierz kategorię", font=("Calibri", 12)).grid(row = 0, columnspan = 2, sticky=N+E+S+W)
        self.student = student
        self.subject = subject
        self.master = master

        self.cb_value = tk.StringVar()     
        self.combobox_grade_categories = ttk.Combobox(self, textvariable = self.cb_value, state="readonly", font=("Calibri", 12))
        self.combobox_grade_categories.grid(row = 1, columnspan = 2, sticky=N+E+S+W)
        grade_categories_obj = []
        grade_categories = []
        for category in sesja.query(GradeCategory).all():
            grade_categories_obj.append(category)
            grade_categories.append(category.name)
        self.combobox_grade_categories['values'] = grade_categories
        self.combobox_grade_categories.current(0)
        self.category_choice = 1
        self.combobox_grade_categories.bind("<<ComboboxSelected>>", self.select_category)

        tk.Label(self, text="Podaj ocenę", font=("Calibri", 12)).grid(row = 2, columnspan = 2, sticky=N+E+S+W)
        self.value_entry = tk.Entry(self, font=("Calibri", 12))
        self.value_entry.grid(row = 3, columnspan = 2, sticky=N+E+S+W)

        tk.Button(self, text="Zapisz", command=self.save, font=("Calibri", 10)).grid(row = 4, column = 1, sticky=N+E+S+W, pady=3)
        tk.Button(self, text="Wróć", command=lambda: master.go_back(), font=("Calibri", 10)).grid(row = 4, column = 0, sticky=N+E+S+W, pady=3)

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

        sesja.add(Grade(value = value_float, grade_category_id = self.category_choice, student_id = self.student.id, subject_id = self.subject.id))
        sesja.commit()
        self.master.go_back()
        