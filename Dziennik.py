import tkinter as tk
from inspect import signature
from start_page import StartPage

class frame_data:
    def __init__(self, frame, arg, arg2, arg3):
        self.frame = frame
        self.arg = arg
        self.arg2 = arg2
        self.arg3 = arg3

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Dziennik')
        self.geometry('1400x620')
        self.minsize(width = 550, height = 260)
        self.frame_stack = []
        self.current_frame = None
        self.navigate_to(StartPage)

    def navigate_to(self, frame_class, arg=None, arg2=None, arg3=None):
        if self.current_frame is not None:
            self.current_frame.destroy()

        new_frame = frame_data(frame_class, arg, arg2, arg3)
        self.frame_stack.append(new_frame)
        self.show_frame(new_frame)

    def go_back(self):
        self.current_frame.destroy()
        self.frame_stack.pop()
        
        last_frame = self.frame_stack[-1]
        self.show_frame(last_frame)

    def show_frame(self, frame_data):
        frame_arg_count = len(signature(frame_data.frame).parameters)
        if frame_arg_count == 1:
            self.current_frame = frame_data.frame(self)
        elif frame_arg_count == 2:
            self.current_frame = frame_data.frame(self, frame_data.arg)
        elif frame_arg_count == 3:
            self.current_frame = frame_data.frame(self, frame_data.arg, frame_data.arg2)
        elif frame_arg_count == 4:
            self.current_frame = frame_data.frame(self, frame_data.arg, frame_data.arg2, frame_data.arg3)
        self.current_frame.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()