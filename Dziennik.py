import tkinter as tk
from start_page import StartPage

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame_stack = []
        self.navigate_to(StartPage)

    def navigate_to(self, frame_class):
        if len(self.frame_stack) > 0:
            self.frame_stack[-1].pack_forget()
        self.frame_stack.append(frame_class(self))
        self.frame_stack[-1].pack()

    def go_back(self):
        self.frame_stack.pop().destroy()
        self.frame_stack[-1].pack()
        try:
            self.frame_stack[-1].on_back()
        except AttributeError:
            pass

if __name__ == "__main__":
    app = Application()
    app.mainloop()