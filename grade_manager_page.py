from Baza import sesja, Student, Subject, Grade, GradeCategory
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.simpledialog import askfloat
from tkinter import messagebox as msb

class Grade_Manager(tk.Frame):
    def __init__(self, master, student, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text= ("Oceny studenta: " + student.last_name + " " + student.first_name)).pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.student = student
        self.subject = subject

        self.grade_list = tk.Listbox(self, font = 2)
        self.grade_list_obj = []
        self.load_grade()
        self.grade_list.pack(anchor = 'w')

        self.grade_choice = 0
        def GradeSelect(event):
            self.grade_choice = self.get_grade_choice() 
            print(self.grade_choice.value)

        def GradeEdit(event):
            self.grade_choice = self.get_grade_choice() 
            if self.grade_choice != 0:
                self.try_edit()

        self.grade_list.bind('<<ListboxSelect>>', GradeSelect)
        self.grade_list.bind('<Double-1>', GradeEdit)

        tk.Button(self, text="Dodaj", command=lambda: self.master.navigate_to(Grade_Add, self.student, self.subject)).pack()
        tk.Button(self, text="Edytuj", command= self.try_edit).pack()
        tk.Button(self, text="Usuń", command= self.try_delete).pack()

        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

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

        def too_much_precision(value):
            str_value = str(value)
            for i in range(len(str_value)):
                if str_value[i] == '.':
                    if i+1 < len(str_value)-1:
                        return 1
                    if len(str_value) > i+1 and str_value[i+1] != '5' and str_value[i+1] != '0':
                        return 1
            return 0

        if self.grade_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano oceny.")
            return
        new_grade_value = askfloat(None, "Podaj nową wartość oceny")
        if new_grade_value == None:
            return
        if new_grade_value > 5 or new_grade_value < 2 or too_much_precision(new_grade_value):
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return
        sesja.query(Grade).filter(Grade.id == self.grade_choice.id).update({Grade.value: new_grade_value})
        sesja.commit()
        self.load_grade()

class Grade_Add(tk.Frame):
    def __init__(self, master, student, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Wybierz kategorię").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.student = student
        self.subject = subject
        self.master = master

        self.cb_value = tk.StringVar()     
        self.combobox_grade_categories = ttk.Combobox(self, textvariable = self.cb_value, state="readonly")
        self.combobox_grade_categories.pack()
        grade_categories_obj = []
        grade_categories = []
        for category in sesja.query(GradeCategory).all():
            grade_categories_obj.append(category)
            grade_categories.append(category.name)
        self.combobox_grade_categories['values'] = grade_categories
        self.combobox_grade_categories.current(0)
        self.category_choice = 1
        self.combobox_grade_categories.bind("<<ComboboxSelected>>", self.select_category)

        tk.Label(self, text="Podaj ocenę").pack(fill="x", pady = 4, anchor = 'w')
        self.value_entry = tk.Entry(self)
        self.value_entry.pack(anchor = 'w')

        tk.Button(self, text="Zapisz", command=self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()
    
    def select_category(self, event):
        str_choice = self.cb_value.get()
        int_choice = sesja.query(GradeCategory.id).filter(GradeCategory.name == str_choice).one()
        self.category_choice = int_choice[0]

    def save(self):

        def too_much_precision(value):
            str_value = str(value)
            for i in range(len(str_value)):
                if str_value[i] == '.':
                    if i+1 < len(str_value)-1:
                        return 1
                    if len(str_value) > i+1 and str_value[i+1] != '5' and str_value[i+1] != '0':
                        return 1
            return 0

        value_str = self.value_entry.get()
        if len(value_str) == 0:
            msb.showwarning("Błąd", "Nie podano wartości oceny.")
            return

        try:
            value_float = float(value_str)
        except ValueError:
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return

        if value_float > 5 or value_float < 2 or too_much_precision(value_float):
            msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
            return

        sesja.add(Grade(value = value_float, grade_category_id = self.category_choice, student_id = self.student.id, subject_id = self.subject.id))
        sesja.commit()
        self.master.go_back()
        