from Baza import sesja, Subject, Group, SubjectGroup, Grade, GradeCategory, Student
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msb

class AddGradeSeries(tk.Frame):
    def __init__(self, master, group, subject):
        tk.Frame.__init__(self, master)
        label_1 = tk.Label(self, text="Wybierz kategorię")
        label_1.grid(row = 0, column = 0)
        self.group = group
        self.subject = subject
        self.master = master

        self.cb_value = tk.StringVar()     
        self.combobox_grade_categories = ttk.Combobox(self, textvariable = self.cb_value, state="readonly")
        self.combobox_grade_categories.grid(row = 1, column = 0)
        grade_categories_obj = []
        grade_categories = []
        for category in sesja.query(GradeCategory).all():
            grade_categories_obj.append(category)
            grade_categories.append(category.name)
        self.combobox_grade_categories['values'] = grade_categories
        self.combobox_grade_categories.current(0)
        self.category_choice = 1
        self.combobox_grade_categories.bind("<<ComboboxSelected>>", self.select_category)

        self.student_obj_list = []
        for student in sesja.query(Student).filter(Student.group_id == self.group.id).order_by(Student.last_name, Student.first_name).all():
            self.student_obj_list.append(student)

        self.y = len(self.student_obj_list)
        self.cells = []

        for i in range(0, self.y):
            cell = [0, 1]
            cell[0] = tk.Entry(self, width=40)
            cell[0].insert(tk.END, (self.student_obj_list[i].last_name + " " + self.student_obj_list[i].first_name))
            cell[0].configure(state='disabled')
            cell[0].grid(row = i+2, column = 0)
            cell[1] = tk.Entry(self, width=10)
            cell[1].grid(row = i+2, column = 1)
            self.cells.append(cell)

        save_button = tk.Button(self, text="Zapisz", command=self.save)
        save_button.grid(row = self.y+2, column = 0)
        back_button = tk.Button(self, text="Wróć", command=lambda: master.go_back())
        back_button.grid(row = self.y+3, column = 0)

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
        
        for cell in self.cells:
            value_str = cell[1].get()
            if len(value_str) > 0:

                try:
                    value_float = float(value_str)
                except ValueError:
                    msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
                    return

                if value_float > 5 or value_float < 2 or too_much_precision(value_float):
                    msb.showwarning("Błąd", "Wprowadzona wartość oceny jest nieprawidłowa.")
                    return
        
        i = 0
        for cell in self.cells:
            value_str = cell[1].get()
            if len(value_str) > 0:
                value_float = float(value_str)
                sesja.add(Grade(value = value_float, grade_category_id = self.category_choice, student_id = self.student_obj_list[i].id, subject_id = self.subject.id))
            i+=1

        sesja.commit()
        self.master.go_back()