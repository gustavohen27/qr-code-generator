import os.path
import tkinter as tk
from re import match
from tkinter import colorchooser, filedialog, messagebox, ttk
from PIL import Image, ImageOps
from csv import DictReader
from os import path
import re
import pandas


def choose_color(prompt="Choose the color", entry=None):
    cor = colorchooser.askcolor(title=prompt)[1]
    if cor:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(cor))
            entry.config(state=tk.DISABLED)
        return cor


def choose_file(prompt="Choose the file", entry=None):
    file = filedialog.askopenfilename(title=prompt)
    if file:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(file))
            entry.config(state=tk.DISABLED)
        return file


def choose_img(prompt="Choose the file", entry=None):
    file = filedialog.askopenfilename(
        defaultextension='.csv',
        filetypes=[
            ("PNG", "*.png"),
            ("JPEG", "*.jpeg"),
            ("JPG", "*.jpg")
        ],
        title=prompt
    )
    if file:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(file))
            entry.config(state=tk.DISABLED)
        return file


def load_qr_code(obj):
    file_path = filedialog.askopenfilename(
        defaultextension='.csv',
        filetypes=[
            ("CSV", "*.csv"),
            ("XLSX", "*.xlsx"),
        ],
        title="Open QR Code file"
    )
    if file_path:
        name, extension = os.path.splitext(file_path)
        data = None
        if extension == '.xlsx':
            data = pandas.read_excel(file_path, engine="openpyxl")
            data = data.to_dict(orient="records")
            print(data)
        else:
            with open(file_path, mode='r') as file:
                print(file.readlines())
                file.seek(0)
                if len(file.readlines()) > 2:
                    messagebox.showerror("File too long",
                                         "Only 1 QR Code can be loaded by time, instead use the multi generator")
                    return None
                else:
                    file.seek(0)
                    reader = DictReader(file)
                    data = [row for row in reader]  # Converte para um dicionário
        for key, entry in obj.methods.items():
            value = data[0].get(key, "")
            if value:
                value = value_verifier(key, str(value))
            if isinstance(entry[0], tk.Entry):
                original_state = entry[0].cget('state')
                entry[0].config(state=tk.NORMAL)
                entry[0].delete(0, tk.END)
                entry[0].insert(0, str(value))
                entry[0].config(state=original_state)
            elif isinstance(entry[0], tk.IntVar):
                entry[0].set(value)
    return None


def load_qr_codes(obj, entry=None):
    file_path = filedialog.askopenfilename(
        defaultextension='.csv',
        filetypes=[
            ("CSV", "*.csv"),
            ("XLSX", "*.xlsx"),
        ],
        title="Open QR Codes file"
    )
    if file_path:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(file_path))
            entry.config(state=tk.DISABLED)
        name, extension = os.path.splitext(file_path)
        data = None
        if extension == '.xlsx':
            data = pandas.read_excel(file_path, engine="openpyxl")
            data = data.to_dict(orient="records")
        else:
            with open(file_path, mode='r') as file:
                reader = DictReader(file)
                data = [row for row in reader]  # Converte para um dicionário
        for key, entry in obj.methods.items():
            value = value_verifier(key, str(data[0].get(key, "")))
            if isinstance(entry[0], tk.Entry):
                original_state = entry[0].cget('state')
                entry[0].config(state=tk.NORMAL)
                entry[0].delete(0, tk.END)
                entry[0].insert(0, str(value))
                entry[0].config(state=original_state)
            elif isinstance(entry[0], tk.IntVar):
                entry[0].set(value)
        return data
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
            scale = (qr_width * obj.LOGO_PROPORTION) / max(logo_width, logo_height)
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


def paste_logo_multi(dictionary, qr_code):
    # MODIFICAR
    qr_width, qr_height = qr_code.size
    logo_size = int(qr_width * float(dictionary['logo_size']))

    try:
        logo = Image.open(dictionary['logo']).convert("RGBA")
    except (FileNotFoundError, AttributeError):
        return qr_code  # Retorna o QR original se não encontrar a logo

    logo_width, logo_height = logo.size

    # Redimensiona a logo
    if dictionary['aspect_ratio'] == 1:
        if dictionary['resize'] == 1:
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        else:
            scale = (qr_width * 0.2) / max(logo_width, logo_height)
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
    if dictionary['logo_color']:
        logo = (ImageOps.colorize(ImageOps.grayscale(logo),
                                  black="black",
                                  white=dictionary['logo_color'])
                .convert("RGBA"))
    # Cola com máscara para preservar transparência
    qr_code.paste(logo, pos, mask=logo)

    return qr_code


def value_verifier(value_type, value):
    value = str(value) if value is not None else ""

    if value_type == "value":
        return value or ""
    elif value_type == "logo":
        if path.exists(value):
            return value
        return ""
    elif value_type in ["color", "background", "logo_color"]:
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return value if match(pattern, value) else ""
    elif value_type == "logo_size":
        return value if value in [str(i / 10) for i in range(1, 10)] else '0.2'
    elif value_type == "version":
        return value if value in [str(i) for i in range(1, 41)] else '1'
    elif value_type == "box_size":
        return value if value in [str(i) for i in range(1, 11)] else '10'
    elif value_type == "border":
        return value if value in [str(i) for i in range(0, 11)] else '4'
    elif value_type in ["resize_logo", "logo_aspect_ratio"]:
        return int(value) if value in ['0', '1'] else 1
    return value


def change_entry(entry, value):
    try:
        if isinstance(entry, tk.Entry):
            original_state = entry.cget('state')
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, value or "")
            entry.config(state=original_state)
        elif isinstance(entry, (tk.IntVar, ttk.Combobox)):
            entry.set(value)
    except ValueError:
        return None


def choose_dir(prompt="Choose the directory", entry=None):
    file = filedialog.askdirectory(title=prompt)
    if file:
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, str(file))
            entry.config(state=tk.DISABLED)
        return file


def clear_file_name(texto, index=None):
    # Remove caracteres inválidos para nomes de arquivos
    texto_limpo = re.sub(r'[\\/*?:"<>|]', "", texto)
    texto_limpo = texto_limpo.strip().replace(" ", "_")

    # Adiciona índice se quiser garantir unicidade
    if index is not None:
        texto_limpo = f"{texto_limpo}_{index}"

    return f"{texto_limpo}.png"
