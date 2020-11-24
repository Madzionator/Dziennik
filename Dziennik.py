from Baza import sesja, Subject, Group, SubjectGroup, Student, Grade, GradeCategory
import tkinter as tk

def unpack(subject_list):
    finally_list = []
    for i in subject_list:
        finally_list.append(i[0])
    return finally_list

def unpack_choice(choice):
    finally_choice = choice[0]
    return finally_choice


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.title("Dziennik")
        
        self.label_1 = tk.Label(self.root, text = "Przedmioty: ", font = 24)
        self.label_1.pack(anchor='w')

        self.subject_list = tk.Listbox(font = 2)
        subjects = unpack(sesja.query(Subject.name).order_by(Subject.name).all())
        for i in range(len(subjects)):
            self.subject_list.insert(i, subjects[i])
        self.subject_list.pack(anchor = 'w')

        def SubjectSelect(event):
            choice = unpack_choice(self.subject_list.curselection())
            print(subjects[choice])
        self.subject_list.bind('<<ListboxSelect>>', SubjectSelect)

        self.root.mainloop()

app = Application()