from Baza import sesja, Student, Subject, Grade, GradeCategory
import tkinter as tk

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
                self.master.navigate_to(Grade_Edit, self.grade_choice)

        self.grade_list.bind('<<ListboxSelect>>', GradeSelect)
        self.grade_list.bind('<Double-1>', GradeEdit)

        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

    def load_grade(self):
        self.grade_list.delete(0, tk.END)
        self.grade_list_obj = []
        i = 0
        for grade in sesja.query(Grade).filter(Grade.student_id == self.student.id).all():
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