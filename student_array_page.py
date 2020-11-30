from Baza import sesja, Subject, Group, SubjectGroup, Grade, GradeCategory, Student
import tkinter as tk
from student_choose import StudentChoose
from add_grade_series_page import AddGradeSeries
from tkinter import*

class Students_array(tk.Frame):
    def __init__(self, master, subject, group):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=(" Przedmiot: " + subject.name + "\nGrupa: " + group.name), font=("Calibri", 20), anchor = 'w')
        label.grid(row = 0, sticky=N+E+S+W, columnspan = 6)
        self.group = group
        self.subject = subject

        self.students_obj_list = []
        for student in sesja.query(Student).filter(Student.group_id == self.group.id).order_by(Student.last_name, Student.first_name).all():
            self.students_obj_list.append(student)
        
        self.grade_categories_list = []
        for grade_category in sesja.query(GradeCategory).all():
            self.grade_categories_list.append(grade_category)
        
        y = len(self.students_obj_list) + 2
        x = len(self.grade_categories_list) + 1

        for i in range(2, y):
            e = tk.Text(self, height = 2, wrap='word', font = ("Calibri", 12))
            e.grid(row=i, column=0, sticky=N+E+S+W)
            e.insert(tk.END, (self.students_obj_list[i-2].last_name + " " + self.students_obj_list[i-2].first_name))
            e.config(state='disabled')

        for i in range(1, x):
            e = tk.Text(self, height = 1, font = ("Calibri", 12))
            e.grid(row=1, column=i, sticky=N+E+S+W)
            e.insert(tk.END, (self.grade_categories_list[i-1].name))
            e.config(state='disabled')

        for i in range(1, x):
            for j in range(2, y):
                e = tk.Text(self, height = 2, wrap = 'word')
                e.grid(row=j, column=i, sticky=N+E+S+W)
                grades = []
                for grade in sesja.query(Grade.value).filter(Grade.student_id == self.students_obj_list[j-2].id, Grade.grade_category_id == self.grade_categories_list[i-1].id, Grade.subject_id == self.subject.id).all():
                    grades.append(grade)
                e.insert(tk.END, grades)
                e.config(state='disabled')
        
        average_label = tk.Text(self, height = 1, width = 10)
        average_label.grid(column = x, row = 1, sticky=N+E+S+W)
        average_label.insert(tk.END, "Średnia")
        average_label.config(state='disabled')
        for i in range(2, y):
                e = tk.Text(self, height = 2)
                e.grid(row=i, column=x, sticky=N+E+S+W)
                student_grades = []
                for grade in sesja.query(Grade.value).filter(Grade.student_id == self.students_obj_list[i-2].id, Grade.subject_id == self.subject.id):
                    student_grades.append(grade.value)
                iAverage = 0.0
                if len(student_grades) > 0:
                    iAverage = round(sum(student_grades)/len(student_grades), 2)
                e.insert(tk.END, iAverage)
                e.config(state='disabled')

        for i in range(0, x):
            self.grid_columnconfigure(i, weight = 2, uniform=True)
        self.grid_columnconfigure(x, weight = 1, uniform=True)

        empty_label = tk.Label(self)
        empty_label.grid(row = y+2, column = x)
        edit_students_button = tk.Button(self, text="Edytuj listę studentów", height = 2, command=lambda: master.navigate_to(StudentChoose, group))
        edit_students_button.grid(row = y+3, column = 0, sticky=N+E+S+W, pady=3, padx=3)
        edit_grades_button = tk.Button(self, text="Zarządzaj ocenami", height = 2, command=lambda: master.navigate_to(StudentChoose, group, subject))
        edit_grades_button.grid(row = y+3, column = 1, sticky=N+E+S+W, pady=3, padx=3)
        add_series_button = tk.Button(self, text="Dodaj serię ocen", height = 2, command=lambda: master.navigate_to(AddGradeSeries, group, subject))
        add_series_button.grid(row = y+3, column = 2, sticky=N+E+S+W, pady=3, padx=3)
        back_button = tk.Button(self, text="Wróć", command=lambda: master.go_back(), height=2)
        back_button.grid(row = y+4, column = 0, sticky=N+E+S+W, pady=3, padx=3)
