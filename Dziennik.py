'''from Baza import sesja, Subject, Group, SubjectGroup, Student, Grade, GradeCategory
import tkinter as tk
#from subject_add_edit import Group_window

def unpack(subject_list):
    finally_list = []
    for i in subject_list:
        finally_list.append(i[0])
    return finally_list

def unpack_choice(choice):
    finally_choice = choice[0]
    return finally_choice

def editB():
    print("edit")

def deleteB():
    print("delete")

def addB():
    print("add")

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
            print(subjects[choice]) #tymczasowe
        self.subject_list.bind('<<ListboxSelect>>', SubjectSelect)

        open_button = tk.Button(self.root, text="otwórz", width=20, command = self.switch_frame(Group_window))
        open_button.pack(anchor = 'w')

        edit_button = tk.Button(self.root, text="edytuj", width=20, command = editB)
        edit_button.pack(anchor = 'w')

        delete_button = tk.Button(self.root, text="usuń", width=20, command = deleteB)
        delete_button.pack(anchor = 'w')

        add_button = tk.Button(self.root, text="dodaj", width=20, command = addB)
        add_button.pack(anchor = 'w')

        self.root.mainloop()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Group_window(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        print("cokolwiek")


app = Application()'''

import tkinter as tk
from subject_add_edit import PageOne, PageTwo

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()