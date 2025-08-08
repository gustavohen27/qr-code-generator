import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageOps
import qrcode


def choose_color(prompt="Choose the color", entry=None):
    cor = colorchooser.askcolor(title=prompt)[1]
    if cor:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(cor))
            entry.config(state=tk.DISABLED)
        return cor


def choose_img(prompt="Choose the color", entry=None):
    file = filedialog.askopenfilename(title=prompt)
    if file:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(file))
            entry.config(state=tk.DISABLED)
        return file


def load_qr_code():
    file = filedialog.askopenfile(
        defaultextension='.csv',
        filetypes=[
            ("CSV", "*.csv"),
            ("XSLX", "*.xslx"),
        ],
        title="Open QR Code file"
    )
    if file:
        file = file.readlines()
        if len(file) > 2:
            messagebox.showerror("File too long", "Only 1 QR Code can be loaded by time, else, use the multi generator")
        else:
            # Implementar
            return file
    return None

def paste_logo(obj, qr_code):
    qr_width, qr_height = qr_code.size
    logo_size = int(qr_width * float(obj.logo_size_var.get()))

    try:
        logo = Image.open(obj.logo_entry.get()).convert("RGBA")
    except FileNotFoundError:
        return qr_code  # Retorna o QR original se não encontrar a logo

    logo_width, logo_height = logo.size

    # Redimensiona a logo
    if obj.aspect_ratio_var.get() == 1:
        if obj.resize_var.get() == 1:
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        else:
            scale = (qr_width * obj.logo_proportion) / max(logo_width, logo_height)
            new_size = (int(logo_width * scale), int(logo_height * scale))
            logo = logo.resize(new_size, Image.Resampling.LANCZOS)
    else:
        # Mantém tamanho original
        pass

    # Recalcula posição com base no tamanho real da logo
    logo_width, logo_height = logo.size
    pos_x = (qr_width - logo_width) // 2
    pos_y = (qr_height - logo_height) // 2
    pos = (pos_x, pos_y)
    # Muda a cor da logo
    if obj.logo_color.get():
        logo = (ImageOps.colorize(ImageOps.grayscale(logo),
                                        black="black",
                                        white=obj.logo_color.get())
                .convert("RGBA"))
    # Cola com máscara para preservar transparência
    qr_code.paste(logo, pos, mask=logo)

    return qr_code
