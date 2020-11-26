import tkinter as tk
from Baza import sesja, Subject
from subject_add_edit import Subject_Add, Subject_Edit

def unpack(subject_list):
    finally_list = []
    for i in subject_list:
        finally_list.append(i[0])
    return finally_list

def unpack_choice(choice):
    finally_choice = choice[0]
    return finally_choice

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = "Przedmioty: ", font = 24).pack(anchor = 'w')

        subject_list = tk.Listbox(self, font = 2)
        subjects = unpack(sesja.query(Subject.name).order_by(Subject.name).all())
        for i in range(len(subjects)):
            subject_list.insert(i, subjects[i])
        subject_list.pack(anchor = 'w')

        def SubjectSelect(event):
            choice = unpack_choice(subject_list.curselection())
            print(subjects[choice]) #tymczasowe
        subject_list.bind('<<ListboxSelect>>', SubjectSelect)

        '''open_button = tk.Button(self, text="otwórz", width=20)
        open_button.pack(anchor = 'w')

        delete_button = tk.Button(self, text="usuń", width=20)
        delete_button.pack(anchor = 'w')'''

        tk.Button(self, text="Dodaj nowy", command=lambda: master.navigate_to(Subject_Add)).pack()
        tk.Button(self, text="Edytuj", command=lambda: master.navigate_to(Subject_Edit)).pack()

    def on_back(self):
        print("?")