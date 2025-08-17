from tkinter import Toplevel
import tkinter as tk
from tkinter import ttk

window = None
enabled = False

# Implementar o gerador
class MultipleGenerator(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry('1000x500')
        self.title("Multiple Generator")
        # Implementar
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack()
        tk.Label(self, text="Status").pack()
        self.status = ttk.Progressbar(self,
                                      orient="horizontal",
                                      mode="determinate",
                                      length=280)
        self.status.pack()
        self.control_frame = tk.Frame(self)
        self.start_button = ttk.Button(
            self.control_frame,
            text='Start',
            command=self.start_generation
        )
        self.pause_button = ttk.Button(
            self.control_frame,
            text='Pause',
            command=self.pause_generation
        )
        self.stop_button = ttk.Button(
            self.control_frame,
            text='Stop',
            command=self.stop_generation
        )
        self.control_frame.pack(pady=20)
        self.start_button.pack(side=tk.LEFT, anchor=tk.CENTER)
        self.pause_button.pack(side=tk.LEFT, anchor=tk.CENTER)
        self.stop_button.pack(side=tk.LEFT, anchor=tk.CENTER)
        self.entries_frame = tk.Frame(self)
        self.entries_frame.pack()

    def start_generation(self):
        pass

    def pause_generation(self):
        pass

    def stop_generation(self):
        pass
