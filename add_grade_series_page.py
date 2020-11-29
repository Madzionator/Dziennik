from Baza import sesja, Subject, Group, SubjectGroup, Grade, GradeCategory, Student
import tkinter as tk
import tkinter.ttk as ttk

class AddGradeSeries(tk.Frame):
    def __init__(self, master, group, subject):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Wybierz kategorię").pack(side="top", fill="x", pady = 4, anchor = 'w')
        self.group = group
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


        #tk.Button(self, text="Zapisz", command=self.save).pack()
        tk.Button(self, text="Wróć", command=lambda: master.go_back()).pack()

    def select_category(self, event):
        str_choice = self.cb_value.get()
        int_choice = sesja.query(GradeCategory.id).filter(GradeCategory.name == str_choice).one()
        self.category_choice = int_choice[0]