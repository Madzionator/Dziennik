from Baza import sesja, Group, Student
import tkinter as tk
from student_add_edit import Student_Add, Student_Edit
from grade_manager_page import Grade_Manager
from tkinter import messagebox as msb


class StudentChoose(tk.Frame):
    def __init__(self, master, group, subject):
        tk.Frame.__init__(self, master)
        self.group = group
        self.master = master
        self.subject = subject

        if subject == None:
            tk.Label(self, text=("Studenci grupy: " + self.group.name)).pack(side="top", fill="x", pady = 4, anchor = 'w')
        else:
            tk.Label(self, text="Zarządzaj ocenami studenta: ").pack(side="top", fill="x", pady = 4, anchor = 'w')

        self.student_list = tk.Listbox(self, font = 2)
        self.student_list_obj = []
        self.load_student()
        self.student_list.pack(anchor = 'w')

        if subject == None: #for student manager
            self.student_choice = 0
            def StudentSelect(event):
                self.student_choice = self.get_choice() 

            def StudentEdit(event):
                self.student_choice = self.get_choice() 
                if self.student_choice != 0:
                    self.master.navigate_to(Student_Edit, self.student_choice)

            self.student_list.bind('<<ListboxSelect>>', StudentSelect)
            self.student_list.bind('<Double-1>', StudentEdit)

            tk.Button(self, text="Dodaj", command=lambda: self.master.navigate_to(Student_Add, self.group)).pack()
            tk.Button(self, text="Edytuj", command= self.try_edit).pack()
            tk.Button(self, text="Usuń", command= self.try_delete).pack()

        else: # for grade manager
            self.student_choice = 0
            def StudentGrades(event):
                self.student_choice = self.get_choice() 
                if self.student_choice != 0:
                    self.master.navigate_to(Grade_Manager, self.student_choice, self.subject) #dodaj klase

            self.student_list.bind('<<ListboxSelect>>', StudentGrades)
            self.student_list.bind('<Double-1>', StudentGrades)

        tk.Button(self, text="Wróc", command=lambda: master.go_back()).pack()

    def load_student(self):
        self.student_list.delete(0, tk.END)
        self.student_list_obj = []
        i = 0
        for student in sesja.query(Student).filter(Student.group_id == self.group.id).order_by(Student.last_name).all():
            self.student_list.insert(i, (student.last_name + " " + student.first_name))
            self.student_list_obj.append(student)
            i+=1

    def get_choice(self):
        try:
            choice = self.student_list.curselection()
            return self.student_list_obj[choice[0]]
        except IndexError: 
            return 0

    def try_delete(self):
        if not self.student_choice:
            msb.showinfo(None, "Nie wybrano studenta do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(Student).filter(Student.id==self.student_choice.id).delete()
            self.load_student()
            self.student_choice = 0
            sesja.commit()

    def try_edit(self):
        if self.student_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano studenta.")
            return
        self.master.navigate_to(Student_Edit, self.student_choice)

