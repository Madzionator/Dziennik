from Baza import sesja, Subject, Group, SubjectGroup, Grade, GradeCategory, Student
import tkinter as tk
#from tkinter import messagebox as msb

class Students_array(tk.Frame):
    def __init__(self, master, subject, group):
        tk.Frame.__init__(self, master)
        tk.Label(self, text=("Przedmiot: " + subject.name + "\nGrupa: " + group.name), font = 2)
        self.group = group
        self.subject = subject

        self.students_obj_list = []
        for student in sesja.query(Student).filter(Student.group_id == self.group.id).all():
            self.students_obj_list.append(student)
        
        self.grade_categories_list = []
        for grade_category in sesja.query(GradeCategory).all():
            self.grade_categories_list.append(grade_category)
        
        y = len(self.students_obj_list) + 1
        x = len(self.grade_categories_list) + 1

        for i in range(1, y):
            e = tk.Entry(self)
            e.grid(row=i, column=0)
            e.insert(tk.END, (self.students_obj_list[i-1].last_name + " " + self.students_obj_list[i-1].first_name))
            e.config(state='disabled')

        #print(self.students_obj_list[0].first_name)

        tk.Button(self, text="Wróć", command=lambda: master.go_back())

