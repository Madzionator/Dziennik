from Baza import sesja, Group, Student
import tkinter as tk
from student_add_edit import Student_Add, Student_Edit
from tkinter import messagebox as msb


class Student_Choose(tk.Frame):
    def __init__(self, master, group):
        tk.Frame.__init__(self, master)
        self.group = group

        self.student_list = tk.Listbox(self, font = 2)
        self.student_list_obj = []
        self.load_student()
        self.student_list.pack(anchor = 'w')

        self.student_choice = 0
        def StudentSelect(event):
            self.student_choice = self.get_choice() 

        def StudentEdit(event):
            self.student_choice = self.get_choice() 
            self.master.navigate_to(Student_Edit, self.student_choice, self.group)

        self.student_list.bind('<<ListboxSelect>>', StudentSelect)
        self.student_list.bind('<Double-1>', StudentEdit)
        self.master = master

        tk.Button(self, text="Edytuj", command= self.try_edit).pack()
        tk.Button(self, text="Dodaj", command= self.master.navigate_to(Student_Add, self.group)).pack()
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
        choice = self.student_list.curselection()
        print(choice)   #wywal
        return self.student_list_obj[choice[0]]

    '''def delete_subject(self):
        if not self.student_choice:
            msb.showinfo(None, "Nie wybrano przedmiotu do usunięcia.")
            return
        if msb.askokcancel(None, ("Na pewno chcesz usunąć?") ):
            sesja.query(Student).filter(Subject.name==self.student_choice.name).delete()
            self.load_student()
            self.student_choice = 0
            sesja.commit()'''

    def try_edit(self):
        if self.student_choice == 0:
            msb.showwarning("Błąd", "Nie wybrano studenta.")
            return
        self.master.navigate_to(Student_Edit, self.student_choice)

