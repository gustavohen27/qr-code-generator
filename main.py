import tkinter as tk
from tkinter import ttk, Label, filedialog, messagebox, LabelFrame, Frame

import qrcode

import configurations
import multipleGenerator
import utils
from utils import choose_color
from PIL import Image, ImageTk


# Terminar o carregamento do QR Code
# Colocar opções para a Logo
# Adicionar botão para defaults
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x500')
        self.title("QR Code Generator")
        self.LOGO_PROPORTION = 0.2
        self.configurations_enabled = False
        self.multiple_generator_enabled = False
        self.configurations = None
        self.multiple_generator = None
        self.choose_logo_img = ImageTk.PhotoImage(Image
                                                  .open('file-icon.png')
                                                  .resize((20, 20)))
        self.choose_color_img = ImageTk.PhotoImage(Image
                                                   .open('color-wheel-icon.png')
                                                   .resize((15, 15)))
        self.delete_entry_img = ImageTk.PhotoImage(Image
                                                   .open('eraser.png')
                                                   .resize((15, 15)))
        # Top widgets
        self.menu1 = tk.Menu(self)
        self.config(menu=self.menu1)
        self.file_menu1 = tk.Menu(self.menu1,
                                 tearoff=0)
        self.file_menu1.add_command(
            label='Save QR Code',
            command=save_qr_code,
        )
        self.file_menu1.add_command(
            label='Load QR Code',
            command=lambda: utils.load_qr_code(self),
        )
        self.file_menu1.add_command(
            label='Exit',
            command=self.destroy,  # Adicionar comando
        )
        self.file_menu2 = tk.Menu(self.menu1,
                                  tearoff=0)
        self.file_menu2.add_command(
            label='Open configurations',
            command=lambda: self.open_configurations(),  # Adicionar comando
        )
        self.file_menu2.add_command(
            label='Open multiple generator',
            command=self.open_multiple_generator,  # Adicionar comando
        )
        # Menu title
        self.menu1.add_cascade(
            label="File",
            menu=self.file_menu1
        )
        self.menu1.add_cascade(
            label="Others",
            menu=self.file_menu2
        )
        # Left frame widgets
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.options1 = ttk.LabelFrame(self.left_frame, text='QR Code options')
        self.options1.pack(expand=tk.TRUE, fill=tk.BOTH)
        self.options2 = ttk.LabelFrame(self.left_frame, text="Logo options")
        self.options2.pack(expand=tk.TRUE, fill=tk.BOTH)
        # Selected Version
        self.selected_version = tk.StringVar()
        self.selected_version.set('1')
        tk.Label(self.options1, text="Version").pack(pady=(30,0))
        self.version_entry = ttk.Combobox(self.options1,
                                          textvariable=self.selected_version)
        self.version_entry['values'] = [i for i in range(1, 41)]
        self.version_entry.pack()
        # Selected box size
        self.selected_box_size = tk.StringVar()
        self.selected_box_size.set('10')
        tk.Label(self.options1, text="Box size").pack()
        self.box_size_entry = ttk.Combobox(self.options1,
                                           textvariable=self.selected_box_size)
        self.box_size_entry['values'] = [i for i in range(1, 11)]
        self.box_size_entry.pack()
        # Selected border
        self.selected_border = tk.StringVar()
        self.selected_border.set('4')
        tk.Label(self.options1, text="Border size").pack()
        self.border_entry = ttk.Combobox(self.options1,
                                         textvariable=self.selected_border)
        self.border_entry['values'] = [i for i in range(0, 11)]
        self.border_entry.pack()
        # Logo options frame
        self.logo_options_frame = Frame(self.options2)
        self.logo_options_frame.pack()
        # Logo resize
        self.resize_var = tk.IntVar()
        self.resize_var.set(1)
        self.logo_resize = tk.Checkbutton(self.logo_options_frame,
                                          text="Resize logo",
                                          variable=self.resize_var,
                                          command=self.choose_logo_size)
        self.logo_resize.pack(pady=(50, 0), anchor="w")
        # Logo aspect ratio
        self.aspect_ratio_var = tk.IntVar()
        self.aspect_ratio_var.set(1)
        self.logo_ratio = tk.Checkbutton(self.logo_options_frame,
                                         text="Logo aspect ratio",
                                         variable=self.aspect_ratio_var,
                                         command=self.choose_logo_aspect_ratio)
        self.logo_ratio.pack(pady=(0, 10), anchor="w")
        # Logo size
        tk.Label(self.logo_options_frame, text="Logo size").pack()
        self.logo_size_var = tk.StringVar()
        self.logo_size_var.set('0.2')
        self.logo_size = ttk.Combobox(self.logo_options_frame,
                                      textvariable=self.logo_size_var)
        self.logo_size['values'] = [i / 10 for i in range(1, 11)]
        self.logo_size.pack()
        # Center frame widgets
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.preview_frame = Frame(self.center_frame)
        self.preview_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=tk.TRUE)
        self.qr_code_preview = tk.Label(self.preview_frame)
        self.qr_code_preview.pack(anchor=tk.CENTER, expand=True)
        self.qr_code_info = tk.Label(self.center_frame)
        self.qr_code_info.place_configure(in_=self.preview_frame,
                                          anchor=tk.CENTER,
                                          relx=0.5,
                                          rely=1)
        self.qr_code_info.place()
        self.center_buttons_frame = tk.Frame(self.center_frame)
        self.center_buttons_frame.pack(side=tk.TOP, pady=(0, 25), fill=tk.X)
        self.save_qr_code = tk.Button(self.center_buttons_frame,
                                      text='Save QR Code',
                                      command=save_qr_code)
        self.load_qr_code = tk.Button(self.center_buttons_frame,
                                      text='Load QR Code',
                                      command=utils.load_qr_code)
        self.qr_code_entry = tk.Entry(self.center_buttons_frame, width=60)
        self.center_buttons_frame.columnconfigure(0, weight=1)
        self.center_buttons_frame.columnconfigure(1, weight=1)
        self.qr_code_entry.pack(pady=25)
        self.save_qr_code.pack(ipadx=20, pady=(0, 25))
        # self.load_qr_code.grid(row=1, column=1, ipadx=20)
        # Right frame widgets
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.colors_frame = tk.LabelFrame(self.right_frame,
                                          text="QR Code colors")
        self.colors_frame.pack(expand=True, fill=tk.BOTH, ipady=25)

        tk.Label(self.colors_frame, text="QR Code color").pack(pady=(40, 0))
        self.qr_code_color = tk.Entry(self.colors_frame, state=tk.DISABLED)
        self.qr_code_color.pack()
        self.qr_code_color_picker = tk.Label(self.colors_frame,
                                             image=self.choose_color_img,
                                             padx=10)
        self.qr_code_color_picker.bind('<Button-1>',
                                       func=self.change_qr_code_color)
        self.qr_code_color_picker.place_configure(anchor="sw",
                                                  in_=self.qr_code_color,
                                                  relx=1.1,
                                                  rely=1.03)

        self.qr_code_color_deleter = tk.Label(self.colors_frame,
                                             image=self.delete_entry_img,
                                             padx=10)
        self.qr_code_color_deleter.bind('<Button-1>',
                                       func=lambda e: self
                                        .delete_entry
                                       (self.qr_code_color))
        self.qr_code_color_deleter.place_configure(anchor="center",
                                                  in_=self.qr_code_color_picker,
                                                  relx=2.1,
                                                  rely=0.44)
        tk.Label(self.colors_frame, text="Background color").pack(pady=10)
        self.bg_color = tk.Entry(self.colors_frame, state=tk.DISABLED)
        self.bg_color.pack()
        self.bg_color_picker = tk.Label(self.colors_frame,
                                        image=self.choose_color_img, padx=10)
        self.bg_color_picker.bind('<Button-1>', func=self.change_bg_color)
        self.bg_color_picker.place_configure(anchor="sw", in_=self.bg_color,
                                             relx=1.1, rely=1.03)
        self.bg_color_deleter = tk.Label(self.colors_frame,
                                              image=self.delete_entry_img,
                                              padx=10)
        self.bg_color_deleter.bind('<Button-1>',
                                        func=lambda e: self
                                        .delete_entry
                                        (self.bg_color))
        self.bg_color_deleter.place_configure(anchor="center",
                                                   in_=self.bg_color_picker,
                                                   relx=2.1,
                                                   rely=0.44)
        # Logo widgets
        self.logo_frame = LabelFrame(self.right_frame, text="Logo")
        self.logo_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        tk.Label(self.logo_frame, text="Logo path").pack(pady=(40, 0))
        self.logo_entry = tk.Entry(self.logo_frame, width=30, state=tk.DISABLED)
        self.logo_entry.pack()

        self.choose_logo = Label(self.logo_frame, image=self.choose_logo_img)
        self.choose_logo.bind('<Button-1>', func=self.choose_image)
        self.choose_logo.place_configure(anchor="sw", in_=self.logo_entry,
                                         relx=1.1, rely=1.04)
        self.logo_deleter = tk.Label(self.logo_frame,
                                           image=self.delete_entry_img,
                                           padx=10)
        self.logo_deleter.bind('<Button-1>',
                                     func=lambda e: self
                                     .delete_entry
                                     (self.logo_entry))
        self.logo_deleter.place_configure(anchor="center",
                                                in_=self.choose_logo,
                                                relx=1.9,
                                                rely=0.44)
        # Logo color
        tk.Label(self.logo_frame, text="Logo color").pack(pady=10)
        self.logo_color = tk.Entry(self.logo_frame, width=30, state=tk.DISABLED)
        self.logo_color.pack()
        self.logo_color_picker = Label(self.logo_frame, image=self.choose_color_img)
        self.logo_color_picker.bind('<Button-1>', func=self.change_logo_color)
        self.logo_color_picker.place_configure(anchor="sw", in_=self.logo_color,
                                               relx=1.1, rely=1.04)
        self.logo_color_deleter = tk.Label(self.logo_frame,
                                         image=self.delete_entry_img,
                                         padx=10)
        self.logo_color_deleter.bind('<Button-1>',
                                   func=lambda e: self
                                   .delete_entry
                                   (self.logo_color))
        self.logo_color_deleter.place_configure(anchor="center",
                                              in_=self.logo_color_picker,
                                              relx=2.1,
                                              rely=0.44)
        # Others
        self.left_frame.pack_propagate(False)
        self.center_frame.pack_propagate(False)
        self.right_frame.pack_propagate(False)
        self.qr_code_entry.bind("<KeyPress>", self.update_preview)
        entries = self.colors_frame
        options_children = (self.options1.winfo_children()
                            + self.options2.winfo_children()
                            + self.logo_options_frame.winfo_children())
        for child in options_children:
            if isinstance(child, ttk.Combobox):
                child.bind('<<ComboboxSelected>>', self.update_preview)
                child['state'] = 'readonly'
        self.qr_code_info.lift()
        # Widgets methods
        self.methods = {
            'value': [self.qr_code_entry],
            'logo': [self.logo_entry],
            'color': [self.qr_code_color],
            'background': [self.bg_color],
            'logo_color': [self.logo_color],
            'logo_size': [self.logo_size_var],
            'version': [self.version_entry],
            'box_size': [self.box_size_entry],
            'border': [self.border_entry],
            'resize_logo': [self.resize_var],
            'logo_aspect_ratio': [self.aspect_ratio_var]
        }

    def change_qr_code_color(self, e=None):
        choose_color("Choose QR Code color", self.qr_code_color)
        self.update_preview()

    def change_bg_color(self, e=None):
        choose_color("Choose background color", self.bg_color)
        self.update_preview()

    def choose_image(self, e=None):
        utils.choose_file("Choose the logo", self.logo_entry)
        self.update_preview()

    def change_logo_color(self, e=None):
        choose_color("Choose logo color", self.logo_color)
        self.update_preview()

    def show_qr_code(self):
        try:
            for key, value in self.methods.items():
                new_value = utils.value_verifier(key, value[0].get())
                utils.change_entry(value[0], new_value)
            self.save_qr_code.config(state="normal")
            qr_code = generate_qr_code().convert("RGB")
            size = f'{qr_code.size[0]}x{qr_code.size[1]}'
            self.qr_code_info.config(text=f'Size: {size}')
            utils.paste_logo(main_window, qr_code)
            if qr_code.size[0] > 250:
                qr_code = qr_code.resize((250, 250))
            qr_code = ImageTk.PhotoImage(qr_code)
            self.qr_code_preview.config(image=qr_code)
            self.qr_code_preview.image = qr_code
        except (AttributeError, TypeError):
            warning_img = ImageTk.PhotoImage(Image
                                                      .open('warning-icon.png')
                                                      .resize((100, 100)))
            self.qr_code_preview.config(image=warning_img)
            self.save_qr_code.config(state=tk.DISABLED)

    def update_preview(self, e=None):
        self.show_qr_code()

    def choose_logo_size(self):
        self.update_preview()

    def choose_logo_aspect_ratio(self):
        self.update_preview()

    def delete_entry(self, entry):
        original_state = entry.cget('state')
        entry.config(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.config(state=original_state)
        self.update_preview()

    def open_configurations(self):
        def disable(e):
            self.configurations_enabled = False

        def enable():
            self.configurations = configurations.Configurations()
            self.configurations.bind('<Destroy>', disable)
            self.configurations_enabled = True
        if not self.configurations_enabled:
            enable()
        else:
            self.configurations.destroy()
            enable()

    def open_multiple_generator(self):
        def disable(e):
            self.multiple_generator_enabled = False

        def enable():
            self.multiple_generator = multipleGenerator.MultipleGenerator()
            self.multiple_generator.bind('<Destroy>', disable)
            self.multiple_generator_enabled = True
            self.multiple_generator.methods = list(self.methods.keys())
            self.multiple_generator.methods = dict(zip(self.multiple_generator.methods,
                                                  self.multiple_generator.entries,
                                                  strict=True))
            print(dict(self.multiple_generator.methods))

        if not self.multiple_generator_enabled:
            enable()
        else:
            self.multiple_generator.destroy()
            enable()


def generate_qr_code():
    print("GERANDO...")
    try:
        qr_code = qrcode.QRCode(version=main_window.selected_version.get(),
                                box_size=main_window.selected_box_size.get(),
                                border=main_window.selected_border.get(),
                                error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr_code.add_data(main_window.qr_code_entry.get())
        qr_code.make(fit=True)
        qr_code = qr_code.make_image(fill_color=main_window.qr_code_color
                                     .get() or 'black',
                                     back_color=main_window.bg_color
                                     .get() or 'white')

        return qr_code
    except ValueError:
        messagebox.showerror("There was an error", "Please review the values while generating the QR Code")



def save_qr_code():
    path = filedialog.asksaveasfilename(
        defaultextension='.png',
        filetypes=[
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("BMP", "*.bmp"),
            ("All files", "*.*"),
        ],
        title="Save QR Code as..."
    )
    if path:
        qr_code = qrcode.QRCode(version=main_window.version_entry.get(),
                                box_size=main_window.box_size_entry.get(),
                                border=main_window.border_entry.get(),
                                error_correction=qrcode.constants
                                .ERROR_CORRECT_L)
        qr_code.add_data(main_window.qr_code_entry.get())
        qr_code.make(fit=True)
        qr_code = qr_code.make_image(fill_color=main_window.qr_code_color.get()
                                                or 'black',
                                     back_color=main_window.bg_color.get()
                                                or 'white').convert("RGBA")
        utils.paste_logo(main_window, qr_code)
        qr_code.save(path, format="PNG")
        print(f"QR CODE GERADO COM SUCESSO! SALVO EM: {path}")
    else:
        return None


if __name__ == "__main__":
    main_window = MainWindow()
    # Updates the QR Code preview
    main_window.update_preview()
    main_window.mainloop()
