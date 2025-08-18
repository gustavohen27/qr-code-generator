import os
from tkinter import Toplevel, messagebox
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
import qrcode
import utils

window = None
enabled = False

# Implementar o gerador
class MultipleGenerator(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry('1000x600')
        self.title("Multiple Generator")
        self.methods = None
        self.file = None
        # Implementar
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(expand=True, fill=tk.X)
        tk.Label(self.status_frame, text="QR codes file").pack()
        self.file_entry = tk.Entry(self.status_frame, width=50, state=tk.DISABLED)
        self.file_entry.pack()
        self.choose_file_img = ImageTk.PhotoImage(Image
                                                  .open('file-icon.png')
                                                  .resize((20, 20)))
        self.file_button = tk.Label(self.status_frame,
                                     image=self.choose_file_img,
                                     padx=10)
        self.file_button.bind('<Button-1>',
                               func=lambda e: self
                               .choose_file
                               (self.file_entry))
        self.file_button.place_configure(anchor="center",
                                          in_=self.file_entry,
                                          relx=1,
                                          rely=0.44)
        tk.Label(self.status_frame, text="Save path").pack()
        self.save_path = tk.Entry(self.status_frame, width=50, state=tk.DISABLED, bg='black')
        self.save_path_button = tk.Label(self.status_frame,
                                    image=self.choose_file_img,
                                    padx=10)
        self.save_path_button.bind('<Button-1>',
                              func=lambda e: self
                              .choose_path_to_save
                              (self.save_path))
        self.save_path_button.place_configure(anchor="center",
                                         in_=self.save_path,
                                         relx=1,
                                         rely=0.44)
        self.save_path.pack()
        tk.Label(self, text="Status").pack()
        self.status = ttk.Progressbar(self,
                                      orient="horizontal",
                                      mode="determinate",
                                      length=280)
        self.status.pack()
        self.status_label = tk.Label(self)
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
        # Value entry
        tk.Label(self.entries_frame, text="value").pack()
        self.value_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.value_entry.pack()
        # Logo entry
        tk.Label(self.entries_frame, text="logo").pack()
        self.logo_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.logo_entry.pack()
        # Color entry
        tk.Label(self.entries_frame, text="color").pack()
        self.color_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.color_entry.pack()
        # Background entry
        tk.Label(self.entries_frame, text="background").pack()
        self.background_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.background_entry.pack()
        # Logo color entry
        tk.Label(self.entries_frame, text="logo_color").pack()
        self.logo_color_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.logo_color_entry.pack()
        # Logo size entry
        tk.Label(self.entries_frame, text="logo_size").pack()
        self.logo_size_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.logo_size_entry.pack()
        # Version entry
        tk.Label(self.entries_frame, text="version").pack()
        self.version_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.version_entry.pack()
        # Box size entry
        tk.Label(self.entries_frame, text="box_size").pack()
        self.box_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.box_entry.pack()
        # Border entry
        tk.Label(self.entries_frame, text="border").pack()
        self.border_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.border_entry.pack()
        # Resize entry
        tk.Label(self.entries_frame, text="Resize logo").pack()
        self.resize_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.resize_entry.pack()
        # Aspect ratio entry
        tk.Label(self.entries_frame, text="Aspect ratio").pack()
        self.aspect_ratio_entry = tk.Entry(self.entries_frame, state=tk.DISABLED)
        self.aspect_ratio_entry.pack()
        # Others
        self.entries = []
        for widget in self.entries_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                self.entries.append([widget])
                widget.configure(width=50)

    def choose_file(self, e):
        self.file = utils.load_qr_codes(self, self.file_entry)
        print(self.file)
        self.status["maximum"] = len(self.file)
        self.status["value"] = 0

    def choose_path_to_save(self, e):
        utils.choose_dir('Choose ".csv" or ".xslx" file',
                          self.save_path)

    def start_generation(self):
        self.status.start()
        if self.file and self.save_path.get():
            for index, line in enumerate(self.file):
                for key, value in line.items():
                    new_value = utils.value_verifier(key, value)
                    line[key] = new_value
                    entry = self.methods[key][0]
                    entry.config(state=tk.NORMAL)
                    entry.delete(0, tk.END)
                    entry.insert(0, str(new_value))
                    entry.config(state=tk.DISABLED)
                qr_code = qrcode.QRCode(
                    version=line['version'],
                    box_size=line['box_size'],
                    border=line['border'],
                    error_correction=qrcode.constants.ERROR_CORRECT_L
                )
                qr_code.add_data(line['value'])
                qr_code.make(fit=True)

                qr_code = qr_code.make_image(
                    fill_color=line['color'] or 'black',
                    back_color=line['background'] or 'white'
                ).convert("RGBA")

                utils.paste_logo_multi(line, qr_code)

                # Gera nome único para cada arquivo
                filename = utils.clear_file_name(line['value'], index + 1)
                full_path = os.path.join(self.save_path.get(), filename)

                try:
                    qr_code.save(full_path, format="PNG")
                    if self.status['value'] < 100:
                        self.status['value'] = index + 1
                        self.status.update_idletasks()
                        percent = int((index + 1) / len(self.file) * 100)
                        self.status_label.configure(text=f"{percent}% concluído")

                except PermissionError:
                    messagebox.showerror("Erro de Permissão", f"Não foi possível salvar o arquivo:\n{full_path}")
        else:
            messagebox.showerror("Please insert file and save path", "You didn't filled all the paths")
            self.status.stop()

    def pause_generation(self):
        pass

    def stop_generation(self):
        self.status.stop()