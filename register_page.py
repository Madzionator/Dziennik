from Baza import sesja, Subject, Group, SubjectGroup, Grade, GradeCategory, Student
import tkinter as tk
from student_choose import Student_Choose
#from tkinter import messagebox as msb

class Students_array(tk.Frame):
    def __init__(self, master, subject, group):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text=("Przedmiot: " + subject.name + "\nGrupa: " + group.name), font = 2)
        label.grid(row = 0)
        self.group = group
        self.subject = subject

        self.students_obj_list = []
        for student in sesja.query(Student).filter(Student.group_id == self.group.id).order_by(Student.last_name).all():
            self.students_obj_list.append(student)
        
        self.grade_categories_list = []
        for grade_category in sesja.query(GradeCategory).all():
            self.grade_categories_list.append(grade_category)
        
        y = len(self.students_obj_list) + 2
        x = len(self.grade_categories_list) + 1

        for i in range(2, y):
            e = tk.Text(self, height = 1, width = 40)
            e.grid(row=i, column=0)
            e.insert(tk.END, (self.students_obj_list[i-2].last_name + " " + self.students_obj_list[i-2].first_name))
            e.config(state='disabled')

        for i in range(1, x):
            e = tk.Text(self, height = 1, width = 40)
            e.grid(row=1, column=i)
            e.insert(tk.END, (self.grade_categories_list[i-1].name))
            e.config(state='disabled')

        for i in range(1, x):
            for j in range(2, y):
                e = tk.Text(self, height = 1, wrap = 'word', width = 40)
                e.grid(row=j, column=i)
                grades = []
                for grade in sesja.query(Grade.value).filter(Grade.student_id == self.students_obj_list[j-2].id, Grade.grade_category_id == self.grade_categories_list[i-1].id).all():
                    grades.append(grade)
                e.insert(tk.END, grades)
                e.config(state='disabled')
        
        average_label = tk.Text(self, height = 1, width = 10)
        average_label.grid(column = x, row = 1)
        average_label.insert(tk.END, "Średnia")
        average_label.config(state='disabled')
        for i in range(2, y):
                e = tk.Text(self, height = 1, width = 10)
                e.grid(row=i, column=x)
                student_grades = []
                for grade in sesja.query(Grade.value).filter(Grade.student_id == self.students_obj_list[i-2].id):
                    student_grades.append(grade.value)
                iAverage = 0
                if len(student_grades) > 0:
                    iAverage = round(sum(student_grades)/len(student_grades), 2)
                e.insert(tk.END, iAverage)
                e.config(state='disabled')


        #print(self.students_obj_list[0].first_name)

        back_button = tk.Button(self, text="Wróć", command=lambda: master.go_back())
        back_button.grid(row = x+2, column = 0)

        edit_student_button = tk.Button(self, text="Edytuj listę studentów", command=lambda: master.navigate_to(Student_Choose, group))
        edit_student_button.grid(row = x+3, column = 0)

