import tkinter as tk
from inspect import signature
from start_page import StartPage

class frame_data:
    def __init__(self, frame, arg):
        self.frame = frame
        self.arg = arg

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame_stack = []
        self.current_frame = None
        self.navigate_to(StartPage)

    def navigate_to(self, frame_class, arg = None):
        if self.current_frame is not None:
            self.current_frame.destroy()

        new_frame = frame_data(frame_class, arg)
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
        self.current_frame.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()