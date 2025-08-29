import tkinter as tk
from tkinter import Toplevel, messagebox

import utils


class Configurations(Toplevel):
    def __init__(self, methods):
        super().__init__()
        self.geometry('500x250')
        self.title("Configurations")
        self.methods = methods
        self.configurations1 = tk.Frame(self)
        self.configurations1.pack()
        self.reset_button = tk.Button(self.configurations1,
                                      text="Reset to default",
                                      command=self.reset_to_default,
                                      width=50)
        self.reset_button.pack(pady=100)

    def reset_to_default(self):
        response = messagebox.askyesno("Reset to default?", "Are you sure do you wa\
nt to reset all values to default?")
        if self.methods and response:
            for key, value in self.methods.items():
                utils.change_entry(value[0], value[1])


        # Implementar